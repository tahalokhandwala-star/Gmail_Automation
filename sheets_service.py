from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from config import SHEET_ID, SERVICE_ACCOUNT_KEY_PATH, SHEETS_SCOPES

class SheetsService:
    def __init__(self):
        self.service = self._get_sheets_service()

    def _get_sheets_service(self):
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_KEY_PATH, scopes=SHEETS_SCOPES)
        return build('sheets', 'v4', credentials=creds)

    def set_headers(self, sheet_name='Trial 1', headers=None):
        """
        Set the header row for the sheet.
        headers should be a list of column names.
        """
        if not headers:
            return

        # Check if headers already exist
        result = self.service.spreadsheets().values().get(
            spreadsheetId=SHEET_ID,
            range=f'{sheet_name}!1:1'
        ).execute()
        existing = result.get('values', [])
        if existing and len(existing[0]) >= len(headers):
            print("Headers already exist, skipping set_headers.")
            return

        # Set the headers
        request = self.service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID,
            range=f'{sheet_name}!A1:{chr(ord("A") + len(headers) - 1)}1',
            valueInputOption='RAW',
            body={'values': [headers]}
        ).execute()
        print(f"Headers set for sheet {sheet_name}.")

    def append_row(self, sheet_name='Trial 1', row_data=None):
        """
        Append a row to the sheet with the given data.
        row_data should be a list of values in order of columns.
        """
        if not row_data:
            return

        # Assuming the sheet has headers, append below
        request = self.service.spreadsheets().values().append(
            spreadsheetId=SHEET_ID,
            range=f'{sheet_name}!A:ZZ',
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body={'values': [row_data]}
        )
        try:
            response = request.execute()
            print(f"Successfully appended to sheet. Response: {response}")
        except Exception as e:
            print(f"Error appending to sheet: {e}")
            raise  # Re-raise to propagate if needed
