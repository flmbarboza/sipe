"""
Template padrão para todas as páginas do SIPE10 v2.
Elimina o boilerplate repetido em cada arquivo de página.
"""

import streamlit as st
from utils.data_manager import init_data, get_data, sidebar_data_controls
from utils.ux_tracker import UXTracker
from utils.a11y import apply_accessibility


def setup_page(page_title: str, page_icon: str, layout: str = "wide"):
    """
    Configuração padrão que toda página deve chamar no início.
    Retorna os dados da sessão já inicializados.
    """
    st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
    init_data()
    data = get_data()
    apply_accessibility()

    # Sidebar comum
    st.sidebar.title("🧭 SIPE10 — Planejamento Estratégico")
    sidebar_data_controls()

    return data


def track_page(page_name: str):
    """Inicializa e retorna o tracker de UX para a página atual."""
    tracker = UXTracker()
    tracker.track_page_view(page_name)
    return tracker
