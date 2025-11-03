# Gmail Automation MVP

This Python project automates the processing of quotation-related emails from Gmail, parsing them with OpenAI, managing clients in SQLite, logging to Google Sheets, and sending acknowledgments.

## Features

- Checks Gmail every 5 minutes for new emails with "quotation", "quote", or "RFQ" in subject.
- Parses email body using OpenAI GPT for structured data.
- Manages client data in local SQLite database.
- Appends processed data to Google Sheets.
- Sends acknowledgment emails back to senders.

## Setup Instructions

### 1. Enable Google APIs

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Enable the following APIs:
   - Gmail API
   - Google Sheets API
4. Create credentials:
   - Go to "Credentials" > "Create Credentials" > "OAuth 2.0 Client IDs".
   - Choose "Desktop application".
   - Download the JSON file and rename/save it as `credentials.json` in the project root.

### 2. Set Up Environment Variables

Create a `.env` file in the project root with your keys:

```
OPENAI_API_KEY=sk-your_openai_api_key_here
GOOGLE_SHEET_ID=your_sheet_id_here  # From the URL, e.g., https://docs.google.com/spreadsheets/d/YOUR_ID/edit
```

### 3. Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
pip install beautifulsoup4
```

### 4. Prepare Google Sheet

- Create a new Google Sheet.
- Copy the "Sheet ID" from the URL.
- Optionally, add headers in row 1: Timestamp, Subject, Sender Name, Date, Client Name, Project Name, Location, Contact Person, Mobile, Email, Scope, Deadline, Client ID

### 5. Run the Application

```bash
python main.py
```

On first run, it will prompt for Google OAuth authentication in your browser (for Gmail and Sheets access).

The script will check for new emails immediately and then every 5 minutes. Press Ctrl+C to stop.

## Project Structure

- `config.py`: Configuration constants and API keys.
- `gmail_service.py`: Gmail reading and sending.
- `llm_parser.py`: OpenAI parsing.
- `db_manager.py`: SQLite client management.
- `sheets_service.py`: Google Sheets logging.
- `main.py`: Orchestrator with scheduler.
- `requirements.txt`: Dependencies.
- `README.md`: This file.

## Notes

- Last processed email timestamp is stored in `last_processed.txt` to avoid duplicates.
- Client data is stored in `clients.db`.
- OAuth tokens are cached in `token.pickle`.
- Ensure your Gmail account allows less secure apps or use app passwords if needed (though OAuth is preferred).
