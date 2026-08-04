"""
Assistente contextual no sidebar.
Sabe em qual página o usuário está e oferece ajuda relevante.
"""

import streamlit as st
from utils.ai_provider import AIProvider


QUICK_QUESTIONS = {
    "Business Model Canvas": [
        "O que é 'proposta de valor'?",
        "Dê exemplos de modelo de negócio para o meu setor",
        "Preciso preencher todos os 9 blocos de uma vez?",
    ],
    "Análise PESTEL": [
        "O que significa PESTEL?",
        "Como identificar oportunidades políticas?",
        "Dê exemplos de fatores econômicos",
    ],
    "5 Forças de Porter": [
        "O que são as 5 forças de Porter?",
        "Como avaliar a intensidade da rivalidade?",
        "Meu negócio é pequeno, preciso disso?",
    ],
    "Análise SWOT": [
        "O que é SWOT?",
        "Qual a diferença entre força e oportunidade?",
        "Como fazer a matriz cruzada?",
    ],
    "Planejamento Estratégico": [
        "O que é missão, visão e valores?",
        "Como definir objetivos estratégicos?",
        "O que são KPIs?",
    ],
    "Plano de Ação 5W2H": [
        "O que significa 5W2H?",
        "Como definir prazos realistas?",
        "Quem deve ser o responsável?",
    ],
}


def render_contextual_helper(page_name: str, data: dict):
    """Renderiza o assistente contextual na sidebar."""
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 💬 Assistente Estratégico")

        questions = QUICK_QUESTIONS.get(page_name, ["Como posso ajudar?"])
        st.markdown("<p style='font-size:12px; color:#64748b; margin-bottom:8px;'>Dúvidas comuns nesta etapa:</p>", unsafe_allow_html=True)

        for q in questions:
            if st.button(q, key=f"quick_q_{q[:20]}_{page_name}", use_container_width=True):
                _answer_question(page_name, q, data)

        pergunta = st.text_input(
            "Ou digite sua dúvida...",
            key=f"chat_input_{page_name}",
            placeholder="Ex: não entendi o que é SWOT",
            label_visibility="collapsed"
        )

        if pergunta:
            _answer_question(page_name, pergunta, data)


def _answer_question(page_name: str, pergunta: str, data: dict):
    with st.spinner("Pensando..."):
        provider = AIProvider()
        setor = data.get("empresa", {}).get("setor", "geral")

        system = f"""Você é um consultor de negócios amigável e paciente.
O usuário está na página '{page_name}' do planejamento estratégico.
Explique conceitos de forma simples, como se estivesse conversando com um amigo.
Use exemplos do setor {setor} quando possível.
Nunca use jargão sem explicar. Seja encorajador."""

        resposta = provider.ask(system, pergunta, max_tokens=500)
        st.markdown(f"<div style='background:#f8fafc; border-radius:8px; padding:12px; font-size:13px; line-height:1.6; margin-top:8px;'>{resposta}</div>", unsafe_allow_html=True)
