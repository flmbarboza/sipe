"""
Integração com IA para o botão "🤖 Consultar IA".
Refatorado para usar AIProvider (unificado).
"""

import streamlit as st
from utils.ai_provider import AIProvider


def ai_assist_widget(field_key: str, contexto_label: str, system_prompt: str, prompt_builder):
    """
    Componente reutilizável de apoio da IA.

    field_key: chave única (usada nos widgets internos)
    contexto_label: texto mostrado no título do expander
    system_prompt: instrução de sistema para a IA
    prompt_builder: função que recebe (instrucao_usuario) e devolve o prompt final

    Retorna a sugestão aceita pelo usuário (string) ou None.
    """
    resp_key = f"ai_resp_{field_key}"
    with st.expander(f"🤖 Consultar IA — {contexto_label}"):
        st.caption("A IA pode sugerir preenchimentos, dar exemplos ou validar o que você já escreveu.")

        instrucao = st.text_area(
            "O que você precisa? (opcional)",
            key=f"ai_inst_{field_key}",
            placeholder="Ex: sugira 3 exemplos para o meu setor, ou valide o que escrevi",
            height=80,
        )

        col1, col2 = st.columns([1, 1])
        with col1:
            consultar = st.button("Consultar IA", key=f"ai_btn_{field_key}", use_container_width=True)
        with col2:
            limpar = st.button("Limpar resposta", key=f"ai_clear_{field_key}", use_container_width=True)

        if limpar and resp_key in st.session_state:
            del st.session_state[resp_key]
            st.rerun()

        if consultar:
            prompt = prompt_builder(instrucao)
            with st.spinner("Consultando a IA..."):
                provider = AIProvider()
                resposta = provider.ask(system_prompt, prompt, max_tokens=800)
                st.session_state[resp_key] = resposta

        if resp_key in st.session_state:
            st.markdown("**Sugestão da IA:**")
            st.markdown(st.session_state[resp_key])

            if st.button("✅ Usar esta sugestão", key=f"ai_use_{field_key}"):
                return st.session_state[resp_key]
    return None
