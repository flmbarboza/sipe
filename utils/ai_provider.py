"""
Provedor unificado de IA para o SIPE10 v2.
Suporta Anthropic (Claude), OpenAI e OpenRouter via uma interface única.
"""

import streamlit as st
from typing import Literal, Optional

Provider = Literal["anthropic", "openai", "openrouter"]


class AIProvider:
    def __init__(self, provider: Optional[Provider] = None):
        self.provider = provider or st.session_state.get("ai_provider_choice", "anthropic")
        self._client = None
        
    def _get_key(self, secret_name: str, session_name: str) -> Optional[str]:
        """Busca chave em secrets ou session_state."""
        if session_name in st.session_state and st.session_state[session_name]:
            return st.session_state[session_name]
        try:
            return st.secrets[secret_name]
        except Exception:
            return None
    
    @property
    def client(self):
        if self._client is None:
            if self.provider == "anthropic":
                key = self._get_key("ANTHROPIC_API_KEY", "api_key_anthropic")
                if not key:
                    raise ValueError("Chave Anthropic não configurada. Adicione em Secrets ou na sidebar.")
                import anthropic
                self._client = anthropic.Anthropic(api_key=key)
            elif self.provider in ("openai", "openrouter"):
                key = self._get_key("OPENAI_API_KEY", "api_key_openai")
                if not key:
                    raise ValueError("Chave OpenAI não configurada. Adicione em Secrets ou na sidebar.")
                from openai import OpenAI
                base_url = "https://openrouter.ai/api/v1" if self.provider == "openrouter" else None
                self._client = OpenAI(api_key=key, base_url=base_url)
        return self._client
    
    def ask(self, system_prompt: str, user_prompt: str, max_tokens: int = 800) -> str:
        try:
            if self.provider == "anthropic":
                response = self.client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=max_tokens,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}],
                )
                parts = [b.text for b in response.content if getattr(b, "type", None) == "text"]
                return "\n".join(parts).strip()
            else:
                model = "gpt-4o" if self.provider == "openai" else "openai/gpt-4o"
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=0.7,
                )
                return response.choices[0].message.content.strip()
        except Exception as e:
            return f"❌ Erro ao consultar a IA: {e}"
    
    @staticmethod
    def sidebar_selector():
        """Widget para escolher o provedor na sidebar."""
        st.sidebar.markdown("### 🤖 Provedor de IA")
        provider = st.sidebar.radio(
            "Modelo",
            ["anthropic", "openai", "openrouter"],
            index=0,
            key="ai_provider_choice",
            help="Escolha qual IA usar para as sugestões."
        )
        
        if provider == "anthropic":
            key = st.sidebar.text_input(
                "Chave da API Anthropic",
                type="password",
                value=st.session_state.get("api_key_anthropic", ""),
                help="Cole sua chave. Fica salva apenas na sessão.",
                key="api_key_anthropic"
            )
            st.session_state["api_key_anthropic"] = key
        else:
            key = st.sidebar.text_input(
                "Chave da API OpenAI / OpenRouter",
                type="password",
                value=st.session_state.get("api_key_openai", ""),
                help="Cole sua chave. Fica salva apenas na sessão.",
                key="api_key_openai"
            )
            st.session_state["api_key_openai"] = key
        
        if not key:
            st.sidebar.caption("⚠️ Sem chave configurada, os botões de IA ficarão desativados.")
        
        return provider
