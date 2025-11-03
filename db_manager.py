import sqlite3
from config import DATABASE_PATH

class DatabaseManager:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.create_table_if_not_exists()

    def create_table_if_not_exists(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_name TEXT,
                project_name TEXT,
                location TEXT,
                contact_person TEXT,
                mobile TEXT,
                email TEXT UNIQUE,
                scope TEXT,
                deadline TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def get_client_by_email(self, email):
        """
        Get full client data by email.
        Returns dict with all fields, or None if not found.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clients WHERE email = ?', (email,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                'id': row[0],
                'client_name': row[1],
                'project_name': row[2],
                'location': row[3],
                'contact_person': row[4],
                'mobile': row[5],
                'email': row[6],
                'scope': row[7],
                'deadline': row[8]
            }
        return None

    def insert_client(self, parsed_data):
        """
        Insert new client. Assumes not exists.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clients (client_name, project_name, location, contact_person, mobile, email, scope, deadline)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            parsed_data.get('client_name'),
            parsed_data.get('project_name'),
            parsed_data.get('location'),
            parsed_data.get('contact_person'),
            parsed_data.get('mobile'),
            parsed_data.get('email'),
            parsed_data.get('scope'),
            parsed_data.get('deadline')
        ))
        client_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return client_id

    def update_client(self, email, parsed_data):
        """
        Update existing client with new data.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE clients SET
            client_name = ?,
            project_name = ?,
            location = ?,
            contact_person = ?,
            mobile = ?,
            scope = ?,
            deadline = ?
            WHERE email = ?
        ''', (
            parsed_data.get('client_name'),
            parsed_data.get('project_name'),
            parsed_data.get('location'),
            parsed_data.get('contact_person'),
            parsed_data.get('mobile'),
            parsed_data.get('scope'),
            parsed_data.get('deadline'),
            email
        ))
        conn.commit()
        conn.close()
