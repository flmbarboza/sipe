import streamlit as st
from utils.page_template import setup_page, track_page
from utils.contextual_helper import render_contextual_helper
from utils.ai_provider import AIProvider

st.set_page_config(page_title="Análise PESTEL", page_icon="🌍", layout="wide")
data = setup_page("Análise PESTEL", "🌍")
tracker = track_page("Análise PESTEL")

st.title("🌍 O que está acontecendo ao redor da sua empresa?")
st.caption("Mapeie fatores externos que podem ajudar ou atrapalhar seu negócio. Estes itens alimentarão a Análise SWOT depois.")

st.info("""
**O que é PESTEL?**  
É uma forma de olhar para o **mundo ao redor** da sua empresa em 6 áreas:
- **P**olítico (leis, governo, estabilidade)
- **E**conômico (inflação, juros, renda das pessoas)
- **S**ocial (cultura, comportamento, demografia)
- **T**ecnológico (inovações, internet, automação)
- **E**cológico (meio ambiente, sustentabilidade, clima)
- **L**egal (normas, direito do consumidor, trabalhista)

> 💡 **Dica:** Pense no que está acontecendo **agora** e no que pode acontecer nos próximos 2-3 anos.
""")

CATEGORIAS = {
    "Político": "Legislação, estabilidade política, políticas públicas, tributação...",
    "Econômico": "Inflação, câmbio, juros, renda, ciclo econômico, crédito...",
    "Social": "Comportamento do consumidor, demografia, cultura, tendências sociais...",
    "Tecnológico": "Inovações, automação, novas plataformas, obsolescência...",
    "Ecológico": "Sustentabilidade, clima, regulação ambiental, escassez de recursos...",
    "Legal": "Normas setoriais, direito do consumidor, trabalhista, regulatório...",
}

pestel_data = data["pestel"]

for categoria, descricao in CATEGORIAS.items():
    with st.expander(f"**{categoria}** — {descricao}"):
        st.caption(f"Liste fatores {categoria.lower()}s que afetam seu negócio. Use o botão + para adicionar mais.")

        itens = pestel_data.get(categoria, [])
        novos_itens = []

        for i in range(max(len(itens), 1)):
            cols = st.columns([3, 1, 1])
            with cols[0]:
                texto = st.text_input(
                    "Fator",
                    value=itens[i].get("descricao", "") if i < len(itens) else "",
                    key=f"pestel_{categoria}_{i}",
                    placeholder=f"Ex: {descricao.split(',')[0]}...",
                    label_visibility="collapsed"
                )
            with cols[1]:
                impacto = st.selectbox(
                    "Impacto",
                    ["Alto", "Médio", "Baixo"],
                    index=1,
                    key=f"pestel_imp_{categoria}_{i}",
                    label_visibility="collapsed"
                )
            with cols[2]:
                tipo = st.selectbox(
                    "Tipo",
                    ["Oportunidade", "Ameaça"],
                    index=0,
                    key=f"pestel_tipo_{categoria}_{i}",
                    label_visibility="collapsed"
                )

            if texto.strip():
                novos_itens.append({"descricao": texto, "impacto": impacto, "tipo": tipo})

        pestel_data[categoria] = novos_itens

        # IA
        if st.button(f"🤖 Sugerir fatores {categoria.lower()}s", key=f"ai_pestel_{categoria}"):
            with st.spinner("Consultando..."):
                provider = AIProvider()
                setor = data.get("empresa", {}).get("setor", "geral")
                prompt = f"Sugira 3 fatores {categoria.lower()}s relevantes para uma empresa do setor {setor}. Formato: descrição | impacto | tipo (Oportunidade/Ameaça)."
                resposta = provider.ask(
                    "Você é um analista de negócios. Dê sugestões práticas e específicas.",
                    prompt,
                    max_tokens=400
                )
                st.markdown(f"**Sugestões:**\n{resposta}")

st.divider()
if st.button("Ir para 5 Forças de Porter →", type="primary"):
    st.switch_page("pages/3_⚔️_5_Forças_de_Porter.py")

render_contextual_helper("Análise PESTEL", data)
