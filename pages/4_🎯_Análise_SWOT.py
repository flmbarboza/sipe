import streamlit as st
from utils.page_template import setup_page, track_page
from utils.contextual_helper import render_contextual_helper

st.set_page_config(page_title="5 Forças de Porter", page_icon="⚔️", layout="wide")
data = setup_page("5 Forças de Porter", "⚔️")
tracker = track_page("5 Forças de Porter")

st.title("⚔️ Quão competitivo é o seu mercado?")
st.caption("Avalie 5 forças que definem a intensidade da concorrência no seu setor.")

st.info("""
**O que são as 5 Forças de Porter?**  
É uma forma de entender **quão difícil** é competir no seu mercado. Quanto mais intensas essas forças, mais trabalho você terá para manter clientes e lucros.

As 5 forças são:
1. **Rivalidade entre concorrentes** — quantos concorrentes diretos você tem?
2. **Poder de barganha dos clientes** — seus clientes têm muitas opções? Conseguem exigir descontos?
3. **Poder de barganha dos fornecedores** — seus fornecedores são poucos? Eles ditam preços?
4. **Ameaça de novos entrantes** — é fácil para alguém novo começar a competir com você?
5. **Ameaça de produtos substitutos** — existe outra forma de resolver o mesmo problema do cliente?
""")

FORCAS = {
    "Rivalidade entre concorrentes": "Quantos concorrentes diretos? Eles brigam por preço?",
    "Poder de barganha dos clientes": "Clientes têm muitas opções? Exigem descontos?",
    "Poder de barganha dos fornecedores": "Fornecedores são poucos? Ditam preços?",
    "Ameaça de novos entrantes": "É fácil alguém novo entrar no mercado?",
    "Ameaça de produtos substitutos": "Existe outra forma de resolver o mesmo problema?",
}

porter_data = data["porter"]

for nome, desc in FORCAS.items():
    with st.container():
        st.markdown("---")
        st.subheader(nome)
        st.caption(desc)

        atual = porter_data.get(nome, {"intensidade": 3, "notas": ""})

        col1, col2 = st.columns([1, 2])
        with col1:
            intensidade = st.slider(
                "Intensidade (1 = fraca, 5 = muito intensa)",
                1, 5, atual.get("intensidade", 3),
                key=f"porter_int_{nome}"
            )
        with col2:
            notas = st.text_area(
                "Por quê? Justifique sua avaliação.",
                value=atual.get("notas", ""),
                key=f"porter_notas_{nome}",
                placeholder="Ex: Temos 5 concorrentes diretos na mesma rua, todos brigam por preço..."
            )

        porter_data[nome] = {"intensidade": intensidade, "notas": notas}

        # Cor baseada na intensidade
        if intensidade >= 4:
            st.warning("⚠️ Força intensa — exige atenção estratégica.")
        elif intensidade <= 2:
            st.success("✅ Força fraca — boa oportunidade.")

st.divider()
if st.button("Ir para Análise SWOT →", type="primary"):
    st.switch_page("pages/4_🎯_Análise_SWOT.py")

render_contextual_helper("5 Forças de Porter", data)
