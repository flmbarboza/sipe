"""
Rastreador de UX com buffer local e envio em lote para Google Sheets.
Taxonomia de eventos para entender o comportamento dos usuários.
"""

import streamlit as st
import time
import json
import hashlib
from datetime import datetime
from collections import deque


class UXTracker:
    """
    Rastreador de UX com buffer local (deque) e flush automático.
    Não quebra a experiência do usuário se a planilha falhar.
    """
    MAX_BUFFER = 100
    FLUSH_INTERVAL_SEC = 60

    def __init__(self):
        if "ux_events" not in st.session_state:
            st.session_state.ux_events = deque(maxlen=self.MAX_BUFFER)
        if "ux_session_id" not in st.session_state:
            st.session_state.ux_session_id = self._gen_session_id()
        if "ux_last_flush" not in st.session_state:
            st.session_state.ux_last_flush = time.time()
        if "ux_pages_visited" not in st.session_state:
            st.session_state.ux_pages_visited = set()
        if "ux_session_start" not in st.session_state:
            st.session_state.ux_session_start = time.time()
        if "ux_field_timers" not in st.session_state:
            st.session_state.ux_field_timers = {}

    def _gen_session_id(self):
        ip = st.query_params.get("client_ip", "unknown")
        base = f"{datetime.now().isoformat()}_{ip}"
        return hashlib.sha256(base.encode()).hexdigest()[:12]

    def _get_user_id(self):
        if "ux_user_id" not in st.session_state:
            st.session_state.ux_user_id = f"anon_{hashlib.sha256(str(time.time()).encode()).hexdigest()[:8]}"
        return st.session_state.ux_user_id

    def track(self, event_type: str, page: str, element: str = "", metadata: dict = None):
        event = {
            "timestamp": datetime.now().isoformat(),
            "session_id": st.session_state.ux_session_id,
            "user_id": self._get_user_id(),
            "event_type": event_type,
            "page": page,
            "element": element,
            "metadata": json.dumps(metadata or {}),
            "screen_width": st.query_params.get("sw", "unknown"),
            "screen_height": st.query_params.get("sh", "unknown"),
        }
        st.session_state.ux_events.append(event)
        self._maybe_flush()

    def _maybe_flush(self):
        buffer = st.session_state.ux_events
        last_flush = st.session_state.ux_last_flush
        if len(buffer) >= self.MAX_BUFFER or (time.time() - last_flush) > self.FLUSH_INTERVAL_SEC:
            self.flush()

    def flush(self):
        buffer = list(st.session_state.ux_events)
        if not buffer:
            return
        try:
            from utils.google_sheets_exporter import GoogleSheetsExporter
            exporter = GoogleSheetsExporter(sheet_name="SIPE10_UX_Analytics")
            exporter.append_events(buffer)
            st.session_state.ux_events.clear()
            st.session_state.ux_last_flush = time.time()
        except Exception as e:
            # Falha silenciosa — tenta no próximo flush
            print(f"[UXTracker] Falha ao enviar: {e}")

    def track_page_view(self, page: str):
        st.session_state.ux_pages_visited.add(page)
        self.track("page_view", page)

    def track_field_focus(self, page: str, field: str):
        st.session_state.ux_field_timers[field] = time.time()
        self.track("field_focus", page, field)

    def track_field_blur(self, page: str, field: str, chars: int = 0, used_ai: bool = False):
        start = st.session_state.ux_field_timers.pop(field, time.time())
        time_ms = int((time.time() - start) * 1000)
        self.track("field_blur", page, field, {
            "chars_typed": chars,
            "time_spent_ms": time_ms,
            "used_ai_suggest": used_ai
        })

    def track_ai_open(self, page: str, field: str):
        self.track("ai_assist_open", page, field)

    def track_ai_request(self, page: str, field: str, prompt_preview: str = ""):
        self.track("ai_assist_request", page, field, {"prompt_preview": prompt_preview[:100]})

    def track_ai_accept(self, page: str, field: str):
        self.track("ai_assist_accept", page, field)

    def track_export(self, export_type: str, page: str, metadata: dict = None):
        self.track(f"export_{export_type}", page, "", metadata or {})

    def track_error(self, error_msg: str, page: str, traceback: str = ""):
        self.track("error", page, "", {"error": error_msg, "traceback": traceback[:500]})

    def track_section_complete(self, page: str, section: str, time_spent_sec: int = 0):
        self.track("section_complete", page, section, {"time_spent_sec": time_spent_sec})

    def get_session_summary(self):
        return {
            "session_id": st.session_state.ux_session_id,
            "user_id": self._get_user_id(),
            "pages_visited": list(st.session_state.ux_pages_visited),
            "session_duration_sec": int(time.time() - st.session_state.ux_session_start),
            "events_in_buffer": len(st.session_state.ux_events),
            "last_flush": st.session_state.ux_last_flush,
        }
