import os
import json
import time
from gmail_service import GmailService
from llm_parser import LLMParser
from db_manager import DatabaseManager
from sheets_service import SheetsService
from config import PUBSUB_PROJECT_ID, PUBSUB_SUBSCRIPTION_NAME
from google.cloud import pubsub_v1

def update_status(progress, text):
    """Update progress status in file."""
    with open('temp_status.txt', 'w', encoding='utf-8') as f:
        f.write(f"{progress}\n{text}")

def process_email(gmail, parser, db, sheets, email):
    """Process a single email."""
    short_subject = email['subject'][:50] + "..." if len(email['subject']) > 50 else email['subject']
    print(f"[MAIL] Processing inquiry: {short_subject}")

    # Parse with LLM
    parsed = parser.parse_email_body(email['body'])
    if not parsed.get('email'):
        parsed['email'] = email['sender']  # Fallback

    # DB: check if client exists
    client_email = parsed['email']
    client_data = db.get_client_by_email(client_email)
    if not client_data:
        # New client, insert to db, use parsed for row
        db.insert_client(parsed)
        row_source = parsed
        print("[USER] New potential client added")
    else:
        # Client exists, use db data for row (do not update db)
        row_source = client_data
        print("[USER] Existing client updated")

    # Append to sheets with new column structure
    row_data = [
        str(email['internal_date']),  # ENQ NO
        "",  # SALES REP
        email['sender_name'],  # customer name
        email['date'],  # DATE
        row_source.get('client_name', ''),  # Client
        email['subject'],  # SUBJECT
        row_source.get('mobile', ''),  # MOBILE
        row_source.get('email', ''),  # Email address
        "",  # estimator
        "New",  # STATUS
        row_source.get('scope', ''),  # Comments
        "Normal",  # Priority
        "NEW",  # OLD/NEW
        "",  # CURRENT REP
        "",  # internal comments
        "",  # QTN NUMBER
        "",  # TO PRICE
        "",  # FORWARD TO
        "N",  # RECONFIRM Y/N
        row_source.get('project_name', ''),  # PROJ/G ENQ
        "",  # LINK
        "",  # priority
        row_source.get('deadline', ''),  # Tentative date
        "",  # Deciding Authority
    ]
    try:
        sheets.append_row(row_data=row_data)
        print("[BAR] Inquiry logged to tracking dashboard")
    except Exception as e:
        print("[X] Unable to save to spreadsheet. Check connection.")

    # Send acknowledgment
    gmail.send_acknowledgment(email['sender'], email['subject'], email['sender_name'], email['subject'])
    print(f"[OK] Automatic reply sent")

    print(f"[DONE] Inquiry fully processed!")

def main():
    if not PUBSUB_PROJECT_ID or not PUBSUB_SUBSCRIPTION_NAME:
        print("[INFO] Note: Real-time Gmail notifications not set up. Using regular scheduled checks.")

    print("[START] Initializing systems...")
    # Initialize services
    gmail = GmailService()
    parser = LLMParser()
    db = DatabaseManager()
    sheets = SheetsService()
    print("[OK] Systems ready")

    # Set headers for the Google Sheet if not already set
    headers = [
        "ENQ NO", "SALES REP", "customer name", "DATE", "Client", "SUBJECT", "MOBILE", "Email address", "estimator", "STATUS", "Comments", "Priority", "OLD/NEW", "CURRENT REP", "internal comments", "QTN NUMBER", "TO PRICE", "FORWARD TO", "RECONFIRM Y/N", "PROJ/G ENQ", "LINK", "priority", "Tentative date", "Deciding Authority"
    ]
    sheets.set_headers(headers=headers)

    # Initialize timestamp for polling
    if not os.path.exists('last_processed.txt'):
        # First run: set to 30 days ago to catch recent emails
        last_processed = int((time.time() - 30 * 24 * 3600) * 1000)  # milliseconds, 30 days ago
        with open('last_processed.txt', 'w') as f:
            f.write(str(last_processed))
        print("[CALENDAR] Reviewing past 30 days of inquiries...")
    else:
        # Subsequent runs: load timestamp, don't process historical emails
        with open('last_processed.txt', 'r') as f:
            content = f.read().strip()
            last_processed = int(content) if content else int((time.time() - 30 * 24 * 3600) * 1000)

    # Load processed email IDs to prevent duplicates
    processed_ids = set()
    processed_ids_file = 'processed_email_ids.txt'
    if os.path.exists(processed_ids_file):
        with open(processed_ids_file, 'r') as f:
            content = f.read().strip()
            if content:
                processed_ids = set(content.split('\n'))

    print("[RUNNING] Inquiry Tracker is active!")
    print("[CLOCK] Checking for new inquiries every 30 seconds...")
    update_status(0, "Waiting for new emails")

    while True:
        try:
            print("EVENT:FETCHING_EMAILS:START")
            update_status(0, "Fetching emails: Looking for new emails")
            # Poll for new emails since last processed
            new_emails = gmail.get_new_emails(last_processed)
            if new_emails:
                print("EVENT:FETCHING_EMAILS:COMPLETE")
                print(f"[ALERT] {len(new_emails)} new inquiry(s) detected!")
                update_status(25, "Parsing with LLM and checking database")
                processed_max_time = last_processed
                for email in new_emails:
                    if email['id'] not in processed_ids:
                        print("EVENT:LLM_PARSE:COMPLETE")
                        update_status(50, "Updating Google Sheet")
                        print("EVENT:SHEET_UPDATE:COMPLETE")
                        process_email(gmail, parser, db, sheets, email)
                        print("EVENT:ACK_EMAIL:COMPLETE")
                        update_status(100, "Sending acknowledgment email")
                        processed_ids.add(email['id'])
                        processed_max_time = max(processed_max_time, email['internal_date'])
                        update_status(0, "Waiting for new emails")
                        print("RESET_CYCLE")
                    else:
                        print("[SKIP] Skipped duplicate inquiry")

                # Update last_processed to max processed time
                last_processed = processed_max_time
                with open('last_processed.txt', 'w') as f:
                    f.write(str(last_processed))

                # Save processed IDs to prevent duplicates across restarts
                with open(processed_ids_file, 'w') as f:
                    f.write('\n'.join(processed_ids))

            time.sleep(30)  # Check every 30 seconds
        except Exception as e:
            print("[WARNING] Connection hiccup. Retrying shortly...")
            time.sleep(10)  # Wait before retry

if __name__ == '__main__':
    main()
