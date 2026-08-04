import streamlit as st
from utils.page_template import setup_page, track_page
from utils.validators import ValidadorPlanejamento
from utils.progress_celebration import celebrate_progress
from utils.contextual_helper import render_contextual_helper

st.set_page_config(page_title="Painel de Controle", page_icon="📈", layout="wide")
data = setup_page("Painel de Controle", "📈")
tracker = track_page("Painel de Controle")

st.title("📈 Painel de Controle")
st.caption("Visão geral do seu planejamento estratégico.")

# Progresso
st.subheader("📊 Progresso Geral")
celebrate_progress(data)

# Validação
st.subheader("🔍 Diagnóstico do Planejamento")
problemas = ValidadorPlanejamento.validar_tudo(data)
total_erros = sum(len(v) for v in problemas.values())

if total_erros > 0:
    st.warning(f"⚠️ {total_erros} observação(ões) encontrada(s):")
    for secao, erros in problemas.items():
        if erros:
            with st.expander(f"{secao.replace('_', ' ').title()} — {len(erros)} item(s)"):
                for e in erros:
                    st.write(e)
else:
    st.success("✅ Planejamento validado! Nenhum problema encontrado.")

# Resumo visual
st.subheader("📋 Resumo do Plano")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Empresa**")
    emp = data.get("empresa", {})
    st.write(f"Nome: {emp.get('nome', 'Não informado')}")
    st.write(f"Setor: {emp.get('setor', 'Não informado')}")
    st.write(f"Local: {emp.get('cidade_estado', 'Não informado')}")

with col2:
    st.markdown("**Objetivos**")
    objs = data.get("objetivos", [])
    st.write(f"{len(objs)} objetivo(s) definido(s)")
    for o in objs:
        st.write(f"• {o.get('objetivo', '')}")

st.markdown("**Ações 5W2H**")
acoes = data.get("acao_5w2h", [])
st.write(f"{len(acoes)} ação(ões) cadastrada(s)")

render_contextual_helper("Painel de Controle", data)
