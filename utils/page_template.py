"""
Exportador de eventos UX para Google Sheets via Service Account.
Envio em lote (batch) para respeitar as quotas da API.
"""

import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheetsExporter:
    def __init__(self, sheet_name="SIPE10_UX_Analytics"):
        self.sheet_name = sheet_name
        self.creds = self._get_credentials()
        self.client = gspread.authorize(self.creds)
        try:
            self.sheet = self.client.open(sheet_name)
        except gspread.SpreadsheetNotFound:
            self.sheet = self.client.create(sheet_name)
            self._init_worksheets()

    def _get_credentials(self):
        creds_dict = {
            "type": st.secrets["google"]["type"],
            "project_id": st.secrets["google"]["project_id"],
            "private_key_id": st.secrets["google"]["private_key_id"],
            "private_key": st.secrets["google"]["private_key"],
            "client_email": st.secrets["google"]["client_email"],
            "client_id": st.secrets["google"]["client_id"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": st.secrets["google"]["client_x509_cert_url"]
        }
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        return ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

    def _init_worksheets(self):
        ws_events = self.sheet.add_worksheet(title="Eventos", rows=10000, cols=10)
        ws_events.append_row([
            "timestamp", "session_id", "user_id", "event_type",
            "page", "element", "metadata", "screen_width", "screen_height"
        ])
        ws_sessions = self.sheet.add_worksheet(title="Sessoes", rows=1000, cols=10)
        ws_sessions.append_row([
            "session_id", "user_id", "start_time", "end_time",
            "pages_visited", "total_events", "duration_sec", "exported"
        ])

    def append_events(self, events: list):
        if not events:
            return
        try:
            ws = self.sheet.worksheet("Eventos")
        except gspread.WorksheetNotFound:
            ws = self.sheet.add_worksheet(title="Eventos", rows=10000, cols=10)
            ws.append_row([
                "timestamp", "session_id", "user_id", "event_type",
                "page", "element", "metadata", "screen_width", "screen_height"
            ])

        rows = []
        for e in events:
            rows.append([
                e.get("timestamp", ""),
                e.get("session_id", ""),
                e.get("user_id", ""),
                e.get("event_type", ""),
                e.get("page", ""),
                e.get("element", ""),
                e.get("metadata", "{}"),
                e.get("screen_width", ""),
                e.get("screen_height", ""),
            ])

        ws.append_rows(rows, value_input_option="USER_ENTERED")

    def append_session_summary(self, summary: dict):
        try:
            ws = self.sheet.worksheet("Sessoes")
        except gspread.WorksheetNotFound:
            ws = self.sheet.add_worksheet(title="Sessoes", rows=1000, cols=10)
            ws.append_row([
                "session_id", "user_id", "start_time", "end_time",
                "pages_visited", "total_events", "duration_sec", "exported"
            ])
        ws.append_row([
            summary.get("session_id", ""),
            summary.get("user_id", ""),
            summary.get("start_time", ""),
            summary.get("end_time", ""),
            ",".join(summary.get("pages_visited", [])),
            summary.get("total_events", 0),
            summary.get("duration_sec", 0),
            summary.get("exported", False),
        ])
