import streamlit as st
from utils.page_template import setup_page, track_page
from utils.contextual_helper import render_contextual_helper

st.set_page_config(page_title="Análise SWOT", page_icon="🎯", layout="wide")
data = setup_page("Análise SWOT", "🎯")
tracker = track_page("Análise SWOT")

st.title("🎯 O que você tem de bom e de ruim?")
st.caption("Análise SWOT: forças, fraquezas, oportunidades e ameaças.")

st.info("""
**O que é SWOT?**  
É uma forma honesta de olhar para a sua empresa:

- **Forças** — o que você faz bem? O que seus clientes elogiam?
- **Fraquezas** — o que precisa melhorar? O que te tira o sono?
- **Oportunidades** — o que está acontecendo no mundo que pode te ajudar?
- **Ameaças** — o que pode te prejudicar? Concorrentes, leis, crises?

> 💡 **Dica:** Forças e Fraquezas são **internas** (você controla). Oportunidades e Ameaças são **externas** (você não controla, mas pode se preparar).
""")

QUADRANTES = {
    "forcas": ("💪 Forças", "O que você faz bem?", "#dcfce7"),
    "fraquezas": ("😰 Fraquezas", "O que precisa melhorar?", "#fee2e2"),
    "oportunidades": ("🌟 Oportunidades", "O que pode te ajudar?", "#dbeafe"),
    "ameacas": ("⚠️ Ameaças", "O que pode te prejudicar?", "#fef3c7"),
}

swot_data = data["swot"]

for chave, (titulo, pergunta, cor) in QUADRANTES.items():
    with st.container():
        st.markdown(f"---")
        st.subheader(titulo)
        st.caption(pergunta)

        itens = swot_data.get(chave, [])
        novos = []

        for i in range(max(len(itens) + 1, 2)):
            texto = st.text_input(
                f"Item {i+1}",
                value=itens[i].get("descricao", "") if i < len(itens) else "",
                key=f"swot_{chave}_{i}",
                placeholder="Descreva com suas palavras..."
            )
            if texto.strip():
                novos.append({"descricao": texto})

        swot_data[chave] = novos

        if len(novos) < 2:
            st.info(f"💡 Recomendamos pelo menos 2 itens em {titulo.split()[1]}.")

st.divider()
if st.button("Ir para Planejamento Estratégico →", type="primary"):
    st.switch_page("pages/5_🧭_Planejamento_Estratégico.py")

render_contextual_helper("Análise SWOT", data)
