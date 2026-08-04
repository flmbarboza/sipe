import streamlit as st
from utils.page_template import setup_page, track_page
from utils.contextual_helper import render_contextual_helper

st.set_page_config(page_title="Orçamento", page_icon="💰", layout="wide")
data = setup_page("Orçamento", "💰")
tracker = track_page("Orçamento")

st.title("💰 Orçamento e Finanças")
st.caption("Projete receitas, custos e investimentos.")

fin = data.get("financeiro", {})

st.subheader("💵 Investimento Inicial")
fin["investimento_inicial"] = st.number_input(
    "Quanto você precisa para começar ou expandir?",
    value=float(fin.get("investimento_inicial", 0)),
    min_value=0.0,
    step=1000.0,
    format="%.2f",
    help="Inclua equipamentos, reforma, estoque inicial, capital de giro..."
)

st.subheader("📈 Receitas Mensais (projeção)")
receitas = fin.get("receitas", [])
novas_rec = []
for i in range(max(len(receitas) + 1, 3)):
    cols = st.columns([2, 1, 1])
    with cols[0]:
        desc = st.text_input(
            "Fonte de receita",
            value=receitas[i].get("descricao", "") if i < len(receitas) else "",
            key=f"rec_desc_{i}",
            placeholder="Ex: Vendas online",
            label_visibility="collapsed"
        )
    with cols[1]:
        valor = st.number_input(
            "Valor (R$)",
            value=float(receitas[i].get("valor", 0)) if i < len(receitas) else 0.0,
            min_value=0.0,
            step=100.0,
            key=f"rec_val_{i}",
            label_visibility="collapsed"
        )
    with cols[2]:
        freq = st.selectbox(
            "Frequência",
            ["Mensal", "Trimestral", "Anual"],
            index=0,
            key=f"rec_freq_{i}",
            label_visibility="collapsed"
        )
    if desc.strip():
        novas_rec.append({"descricao": desc, "valor": valor, "frequencia": freq})
fin["receitas"] = novas_rec

st.subheader("📉 Custos Mensais")
custos = fin.get("custos", [])
novos_custos = []
for i in range(max(len(custos) + 1, 3)):
    cols = st.columns([2, 1])
    with cols[0]:
        desc = st.text_input(
            "Custo",
            value=custos[i].get("descricao", "") if i < len(custos) else "",
            key=f"custo_desc_{i}",
            placeholder="Ex: Aluguel",
            label_visibility="collapsed"
        )
    with cols[1]:
        valor = st.number_input(
            "Valor (R$)",
            value=float(custos[i].get("valor", 0)) if i < len(custos) else 0.0,
            min_value=0.0,
            step=100.0,
            key=f"custo_val_{i}",
            label_visibility="collapsed"
        )
    if desc.strip():
        novos_custos.append({"descricao": desc, "valor": valor})
fin["custos"] = novos_custos

# Resumo
if novas_rec or novos_custos:
    total_rec = sum(r["valor"] for r in novas_rec)
    total_custo = sum(c["valor"] for c in novos_custos)
    saldo = total_rec - total_custo

    col1, col2, col3 = st.columns(3)
    col1.metric("Receitas mensais", f"R$ {total_rec:,.2f}")
    col2.metric("Custos mensais", f"R$ {total_custo:,.2f}")
    col3.metric("Saldo mensal", f"R$ {saldo:,.2f}", delta=f"{'+' if saldo >= 0 else ''}{saldo:,.2f}")

render_contextual_helper("Orçamento", data)
