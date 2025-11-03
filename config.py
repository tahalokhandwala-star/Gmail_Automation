import os
from dotenv import load_dotenv

load_dotenv()

# Configuration for Gmail Automation MVP

# OpenAI API settings
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # From .env file
OPENAI_MODEL = 'gpt-3.5-turbo'  # Changed for reliability

# Google API settings
GMAIL_CREDENTIALS_PATH = 'credentials.json'  # Path to OAuth credentials
GMAIL_TOKEN_PATH = 'token.pickle'  # Path to OAuth token
SERVICE_ACCOUNT_KEY_PATH = 'service_account.json'  # Path to service account key for Sheets
sheet_url = os.getenv('GOOGLE_SHEET_ID')  # e.g., https://docs.google.com/spreadsheets/d/YOUR_ID/edit
SHEET_ID = sheet_url.split('/d/')[1].split('/')[0] if sheet_url and '/d/' in sheet_url else sheet_url

# Pub/Sub settings for Gmail notifications
PUBSUB_PROJECT_ID = os.getenv('PUBSUB_PROJECT_ID')
PUBSUB_TOPIC_NAME = os.getenv('PUBSUB_TOPIC_NAME', 'GmailUpdates')  # Just the topic name, not full path
PUBSUB_SUBSCRIPTION_NAME = os.getenv('PUBSUB_SUBSCRIPTION_NAME', 'gmail-sub')  # Just the subscription name
GMAIL_WATCH_LABEL_IDS = ['INBOX']  # Labels to watch for new emails

# Database settings
DATABASE_PATH = 'clients.db'

# Gmail query for new emails
EMAIL_QUERY = 'label:inbox subject:(quotation OR quote OR RFQ)'
# Note: For service account, the Gmail user to impersonate
GMAIL_USER = os.getenv('GMAIL_USER')  # The email to impersonate, e.g., taha.lokhandwala@rubikonlabs.com

# Acknowledgment email settings
ACK_SUBJECT = 'Acknowledgment: Your Quotation Request Received'
ACK_BODY_TEMPLATE = """
Dear {sender_name},

Thank you for your quotation request ({subject}). We have received and are processing your inquiry.

Best regards,
Gmail Automation System
"""

# Scopes for Google APIs
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/pubsub']  # Modify + spreadsheets + pubsub
SHEETS_SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/pubsub']
