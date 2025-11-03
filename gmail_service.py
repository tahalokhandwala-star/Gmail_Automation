import base64
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from config import GMAIL_CREDENTIALS_PATH, GMAIL_TOKEN_PATH, GMAIL_SCOPES, EMAIL_QUERY, PUBSUB_PROJECT_ID, PUBSUB_TOPIC_NAME, PUBSUB_SUBSCRIPTION_NAME
import pickle
from google.cloud import pubsub_v1

class GmailService:
    def __init__(self):
        self.creds = None
        self.service = self._get_gmail_service()
        self.setup_gmail_watch()

    def _get_gmail_service(self):
        creds = None
        if os.path.exists(GMAIL_TOKEN_PATH):
            with open(GMAIL_TOKEN_PATH, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(GMAIL_CREDENTIALS_PATH, GMAIL_SCOPES)
                creds = flow.run_local_server(port=0)
            with open(GMAIL_TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)
        self.creds = creds
        return build('gmail', 'v1', credentials=creds)

    def setup_gmail_watch(self):
        if os.environ.get('DISABLE_GMAIL_WATCH') == '1':
            print("Gmail watch disabled via environment variable.")
            return
        from config import GMAIL_WATCH_LABEL_IDS
        if not PUBSUB_PROJECT_ID or not PUBSUB_TOPIC_NAME:
            print("Pub/Sub configuration missing. Skipping Gmail watch setup.")
            return
        topic_name = f"projects/{PUBSUB_PROJECT_ID}/topics/{PUBSUB_TOPIC_NAME}"
        request_body = {
            'labelIds': GMAIL_WATCH_LABEL_IDS,
            'topicName': topic_name
        }
        try:
            response = self.service.users().watch(userId='me', body=request_body).execute()
            print(f"Gmail watch set up: {response}")
            # Now create the subscription using service account
            self._create_subscription_if_needed(topic_name)
        except Exception as e:
            print(f"Error setting up watch: {e}")

    def _create_subscription_if_needed(self, topic_name):
        try:
            subscriber = pubsub_v1.SubscriberClient(credentials=self.creds)
            subscription_path = subscriber.subscription_path(PUBSUB_PROJECT_ID, PUBSUB_SUBSCRIPTION_NAME)
            try:
                subscriber.create_subscription(name=subscription_path, topic=topic_name)
                print(f"Subscription '{PUBSUB_SUBSCRIPTION_NAME}' created.")
            except Exception as e:
                if 'Resource already exists' in str(e):
                    print(f"Subscription '{PUBSUB_SUBSCRIPTION_NAME}' already exists. Deleting and recreating.")
                    # Delete existing subscription
                    try:
                        subscriber.delete_subscription(subscription=subscription_path)
                        print(f"Deleted existing subscription '{PUBSUB_SUBSCRIPTION_NAME}'.")
                    except Exception as delete_e:
                        print(f"Error deleting subscription: {delete_e}")
                        return
                    # Create new subscription
                    try:
                        subscriber.create_subscription(name=subscription_path, topic=topic_name)
                        print(f"Recreated subscription '{PUBSUB_SUBSCRIPTION_NAME}'.")
                    except Exception as create_e:
                        print(f"Error recreating subscription: {create_e}")
                else:
                    print(f"Error creating subscription: {e}")
        except Exception as e:
            print(f"Error setting up subscription: {e}")

    def get_email_by_id(self, msg_id):
        msg_data = self.service.users().messages().get(userId='me', id=msg_id).execute()
        return self._parse_message(msg_data)

    def get_new_emails(self, last_internal_date=None):
        """
        Get new emails matching query since last_internal_date.
        Returns list of dicts: {id, sender, subject, date, body, internal_date}
        """
        query = EMAIL_QUERY
        if last_internal_date:
            query += f' after:{last_internal_date // 1000}'  # Gmail after is seconds

        print(f"Query: {query}")
        results = self.service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        print(f"Gmail list returned {len(messages)} messages.")

        emails = []
        for msg in messages:
            msg_data = self.service.users().messages().get(userId='me', id=msg['id']).execute()
            email = self._parse_message(msg_data)
            emails.append(email)
            print(f"Retrieved email: {email['subject']}")

        return emails

    def _parse_message(self, msg_data):
        """Parse message to get sender, subject, date, body, internal_date"""
        headers = {h['name']: h['value'] for h in msg_data['payload']['headers']}
        sender = headers.get('From', '').split('<')[1].rstrip('>') if '<' in headers.get('From', '') else headers.get('From', '')
        subject = headers.get('Subject', '')
        date = headers.get('Date', '')
        internal_date = int(msg_data['internalDate'])

        # Get plain text body
        body = self._get_body_text(msg_data['payload'])

        return {
            'id': msg_data['id'],
            'sender': sender,
            'sender_name': headers.get('From', '').split('<')[0].strip(' "'),
            'subject': subject,
            'date': date,
            'body': body,
            'internal_date': internal_date
        }

    def _get_body_text(self, payload):
        """Extract plain text from payload"""
        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('mimeType') == 'text/plain':
                    return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                elif part.get('mimeType') == 'text/html':
                    html = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    soup = BeautifulSoup(html, 'html.parser')
                    return soup.get_text()
        else:
            if payload.get('mimeType') == 'text/plain':
                return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        return ''

    def send_acknowledgment(self, to, subject, sender_name, original_subject):
        """Send acknowledgment email"""
        from config import ACK_SUBJECT, ACK_BODY_TEMPLATE
        body = ACK_BODY_TEMPLATE.format(sender_name=sender_name, subject=original_subject)

        message = {
            'raw': base64.urlsafe_b64encode(f'''To: {to}
Subject: {ACK_SUBJECT}

{body}'''.encode('utf-8')).decode('utf-8')
        }
        self.service.users().messages().send(userId='me', body=message).execute()
