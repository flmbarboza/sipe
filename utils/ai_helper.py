"""
Acessibilidade: aplica preferências do usuário via CSS injetado.
"""

import streamlit as st


def apply_accessibility():
    """Aplica preferências de acessibilidade do usuário."""
    css_parts = []

    if st.session_state.get("a11y_large_text"):
        css_parts.append("""
            .stApp { font-size: 19px !important; }
            .stTextInput input, .stTextArea textarea { font-size: 17px !important; }
            .stButton button { font-size: 17px !important; }
            h1 { font-size: 32px !important; }
            h2 { font-size: 26px !important; }
            h3 { font-size: 22px !important; }
        """)

    if st.session_state.get("a11y_high_contrast"):
        css_parts.append("""
            .stApp { 
                --primary-color: #000000 !important;
                --background-color: #ffffff !important;
                --secondary-background-color: #ffffff !important;
                --text-color: #000000 !important;
            }
            .stInfo { background-color: #000000 !important; color: #ffffff !important; border-color: #000000 !important; }
            .stSuccess { background-color: #000000 !important; color: #ffffff !important; border-color: #000000 !important; }
            .stWarning { background-color: #000000 !important; color: #ffff00 !important; border-color: #000000 !important; }
            .stError { background-color: #000000 !important; color: #ff0000 !important; border-color: #000000 !important; }
        """)

    if st.session_state.get("a11y_reduce_motion"):
        css_parts.append("""
            * { animation: none !important; transition: none !important; }
        """)

    if css_parts:
        st.markdown(f"<style>{''.join(css_parts)}</style>", unsafe_allow_html=True)
