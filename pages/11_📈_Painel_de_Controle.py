import streamlit as st
from utils.page_template import setup_page, track_page
from utils.contextual_helper import render_contextual_helper

st.set_page_config(page_title="Revisão", page_icon="🔄", layout="wide")
data = setup_page("Revisão", "🔄")
tracker = track_page("Revisão")

st.title("🔄 Revisão e Ajustes")
st.caption("O planejamento estratégico não é estático. Revise e ajuste conforme o mercado muda.")

st.info("""
**Quando revisar?**

- **Mensal:** Ações do 5W2H — o que funcionou? O que precisa mudar?
- **Trimestral:** Objetivos e KPIs — estamos no caminho certo?
- **Anual:** Missão, visão e modelo de negócio — ainda fazem sentido?

> 💡 **Dica:** A melhor estratégia é aquela que se adapta.
""")

revisao = data.get("revisao", {})

st.subheader("📝 Notas de Revisão")
revisao["notas"] = st.text_area(
    "Registre aqui o que mudou, o que funcionou e o que precisa ajustar.",
    value=revisao.get("notas", ""),
    height=200,
    placeholder="Ex: Em janeiro, percebemos que o canal Instagram trouxe mais vendas do que o esperado. Vamos dobrar o investimento em ads..."
)

st.subheader("📅 Próxima Revisão")
revisao["proxima_data"] = st.text_input(
    "Quando será a próxima revisão?",
    value=revisao.get("proxima_data", ""),
    placeholder="Ex: 15/03/2027"
)

revisao["responsavel_revisao"] = st.text_input(
    "Quem é responsável pela próxima revisão?",
    value=revisao.get("responsavel_revisao", ""),
    placeholder="Ex: João, gerente de operações"
)

render_contextual_helper("Revisão", data)
