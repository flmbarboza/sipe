import streamlit as st
from utils.page_template import setup_page, track_page
from utils.editors import safe_data_editor
from utils.contextual_helper import render_contextual_helper

st.set_page_config(page_title="Plano de Ação 5W2H", page_icon="✅", layout="wide")
data = setup_page("Plano de Ação 5W2H", "✅")
tracker = track_page("Plano de Ação 5W2H")

st.title("✅ Quem faz o quê e até quando?")
st.caption("Transforme seus objetivos em ações concretas usando o método 5W2H.")

st.info("""
**O que é 5W2H?**  
É uma forma simples de não deixar nada para trás. Cada ação responde:

- **What** (O quê?) — Qual a ação?
- **Why** (Por quê?) — Por que isso é importante?
- **Where** (Onde?) — Onde vai acontecer?
- **When** (Quando?) — Qual o prazo?
- **Who** (Quem?) — Quem é responsável?
- **How** (Como?) — Como será feito?
- **How much** (Quanto custa?) — Qual o investimento?

> 💡 **Dica:** Seja específico. "Melhorar vendas" é vago. "Ligar para 10 clientes por dia" é acionável.
""")

acoes = data.get("acao_5w2h", [])

st.subheader("📋 Ações")

novas_acoes = safe_data_editor(
    acoes,
    columns=["what", "why", "where", "when", "who", "how", "how_much"],
    key_prefix="acoes_5w2h",
    column_configs={
        "what": st.column_config.TextColumn("O quê?", width="large"),
        "why": st.column_config.TextColumn("Por quê?", width="medium"),
        "where": st.column_config.TextColumn("Onde?", width="medium"),
        "when": st.column_config.TextColumn("Quando?", width="medium"),
        "who": st.column_config.TextColumn("Quem?", width="medium"),
        "how": st.column_config.TextColumn("Como?", width="medium"),
        "how_much": st.column_config.TextColumn("Quanto custa?", width="small"),
    }
)

data["acao_5w2h"] = novas_acoes

if novas_acoes:
    st.success(f"{len(novas_acoes)} ação(ões) cadastrada(s).")
else:
    st.info("Adicione sua primeira ação na tabela acima. Clique no + na última linha.")

st.divider()
if st.button("Ir para Orçamento →", type="primary"):
    st.switch_page("pages/8_💰_Orçamento.py")

render_contextual_helper("Plano de Ação 5W2H", data)
