import streamlit as st
from utils.page_template import setup_page, track_page
from utils.editors import safe_data_editor
from utils.contextual_helper import render_contextual_helper

st.set_page_config(page_title="Planos por Função", page_icon="📋", layout="wide")
data = setup_page("Planos por Função", "📋")
tracker = track_page("Planos por Função")

st.title("📋 Planos por Departamento")
st.caption("Crie planos específicos para cada área da empresa.")

departamentos = data.get("departamentos", {})

# Lista de departamentos padrão
DEPTOS = ["Marketing", "Vendas", "Operações", "Financeiro", "RH", "Tecnologia"]

depto_selecionado = st.selectbox("Selecione o departamento", DEPTOS + ["Outro"])
if depto_selecionado == "Outro":
    depto_selecionado = st.text_input("Nome do departamento")

if depto_selecionado:
    if depto_selecionado not in departamentos:
        departamentos[depto_selecionado] = {"objetivos": [], "acoes": []}

    dept = departamentos[depto_selecionado]

    st.subheader(f"Objetivos de {depto_selecionado}")
    dept["objetivos"] = safe_data_editor(
        dept.get("objetivos", []),
        columns=["Objetivo", "Prazo", "Responsável", "Status"],
        key_prefix=f"depto_{depto_selecionado}_obj",
        column_configs={
            "Status": st.column_config.SelectboxColumn("Status", options=["Não iniciado", "Em andamento", "Concluído"]),
        }
    )

    st.subheader(f"Ações de {depto_selecionado}")
    dept["acoes"] = safe_data_editor(
        dept.get("acoes", []),
        columns=["Ação", "Prazo", "Responsável", "Status"],
        key_prefix=f"depto_{depto_selecionado}_acoes",
        column_configs={
            "Status": st.column_config.SelectboxColumn("Status", options=["Não iniciado", "Em andamento", "Concluído"]),
        }
    )

render_contextual_helper("Planos por Função", data)
