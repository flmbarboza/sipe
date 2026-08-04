import streamlit as st
from utils.page_template import setup_page, track_page
from utils.contextual_helper import render_contextual_helper

st.set_page_config(page_title="Planejamento Estratégico", page_icon="🧭", layout="wide")
data = setup_page("Planejamento Estratégico", "🧭")
tracker = track_page("Planejamento Estratégico")

st.title("🧭 Para onde sua empresa vai?")
st.caption("Defina missão, visão, valores, objetivos e KPIs.")

st.info("""
**O que é Missão, Visão e Valores?**

- **Missão** — Por que sua empresa existe? O que ela faz hoje?
- **Visão** — Onde você quer chegar em 3-5 anos? Qual o sonho grande?
- **Valores** — Quais princípios guiam as decisões da empresa?

> 💡 **Dica:** Não precisa ser poético. Use suas palavras. O importante é ser honesto.
""")

mvv = data["mvv"]

st.subheader("🎯 Missão")
mvv["missao"] = st.text_area(
    "Por que sua empresa existe?",
    value=mvv.get("missao", ""),
    help="Ex: 'Oferecer padaria artesanal de qualidade com preço justo para a comunidade local.'",
    placeholder="Escreva com suas palavras..."
)

st.subheader("🔭 Visão")
mvv["visao"] = st.text_area(
    "Onde você quer chegar em 3-5 anos?",
    value=mvv.get("visao", ""),
    help="Ex: 'Ser a padaria mais amada do bairro, conhecida pelo pão fresco e pelo atendimento caloroso.'",
    placeholder="Descreva o futuro que você sonha..."
)

st.subheader("💎 Valores")
valores = mvv.get("valores", [])
novos_valores = []
for i in range(max(len(valores) + 1, 3)):
    v = st.text_input(
        f"Valor {i+1}",
        value=valores[i] if i < len(valores) else "",
        key=f"valor_{i}",
        placeholder="Ex: Honestidade, Inovação, Respeito ao cliente..."
    )
    if v.strip():
        novos_valores.append(v)
mvv["valores"] = novos_valores

st.divider()

st.subheader("📈 Objetivos Estratégicos")
objetivos = data.get("objetivos", [])
novos_obj = []

for i in range(max(len(objetivos) + 1, 2)):
    with st.container():
        cols = st.columns([2, 1, 1, 1])
        with cols[0]:
            obj = st.text_input(
                "Objetivo",
                value=objetivos[i].get("objetivo", "") if i < len(objetivos) else "",
                key=f"obj_{i}",
                placeholder="Ex: Aumentar vendas em 30%",
                label_visibility="collapsed"
            )
        with cols[1]:
            kpi = st.text_input(
                "KPI (como medir?)",
                value=objetivos[i].get("kpi", "") if i < len(objetivos) else "",
                key=f"kpi_{i}",
                placeholder="Ex: faturamento mensal",
                label_visibility="collapsed"
            )
        with cols[2]:
            meta = st.text_input(
                "Meta",
                value=objetivos[i].get("meta", "") if i < len(objetivos) else "",
                key=f"meta_{i}",
                placeholder="Ex: R$ 50.000/mês",
                label_visibility="collapsed"
            )
        with cols[3]:
            prazo = st.text_input(
                "Prazo",
                value=objetivos[i].get("prazo", "") if i < len(objetivos) else "",
                key=f"prazo_obj_{i}",
                placeholder="Ex: 12 meses",
                label_visibility="collapsed"
            )
        if obj.strip():
            novos_obj.append({"objetivo": obj, "kpi": kpi, "meta": meta, "prazo": prazo})

data["objetivos"] = novos_obj

st.divider()
if st.button("Ir para Plano de Ação →", type="primary"):
    st.switch_page("pages/6_✅_Plano_de_Ação_5W2H.py")

render_contextual_helper("Planejamento Estratégico", data)
