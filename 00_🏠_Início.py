import streamlit as st
from utils.data_manager import init_data, get_data, sidebar_data_controls
from utils.progress_celebration import celebrate_progress

st.set_page_config(page_title="SIPE10 — Planejamento Estratégico", page_icon="🎯", layout="wide")
init_data()
data = get_data()

# ========== HERO SECTION ==========
st.markdown("""
<div style="text-align:center; padding: 40px 20px 24px;">
    <div style="font-size: 56px; margin-bottom: 16px;">🎯</div>
    <h1 style="font-size: 30px; font-weight: 600; margin-bottom: 12px; color: #0f172a;">
        Planeje o futuro da sua empresa, passo a passo
    </h1>
    <p style="font-size: 17px; color: #64748b; max-width: 600px; margin: 0 auto; line-height: 1.7;">
        O <strong>SIPE10</strong> é um assistente de planejamento estratégico. 
        Você não precisa ser especialista em gestão — basta responder às perguntas 
        que vamos te fazer. No final, você terá um plano completo para crescer com segurança.
    </p>
</div>
""", unsafe_allow_html=True)

# ========== VALUE PROPS ==========
cols = st.columns(4)
value_props = [
    ("📄", "Documento pronto", "Gere um relatório em PDF para apresentar a bancos, investidores ou equipe."),
    ("🛡️", "Proteja seu negócio", "Identifique riscos antes que aconteçam e crie planos de ação claros."),
    ("🤖", "IA que traduz", "Não entendeu algum termo? Pergunte a qualquer momento. Sem jargão sem explicação."),
    ("🏢", "Para todos os tamanhos", "Funciona para pequenos negócios, startups, cooperativas e grandes empresas."),
]
for col, (icon, title, desc) in zip(cols, value_props):
    with col:
        st.markdown(f"""
        <div style="border:1px solid #e2e8f0; border-radius:12px; padding:18px; text-align:center; height:100%;">
            <div style="font-size:28px; margin-bottom:10px;">{icon}</div>
            <h3 style="font-size:15px; font-weight:600; margin-bottom:8px; color:#0f172a;">{title}</h3>
            <p style="font-size:13px; color:#64748b; line-height:1.6; margin:0;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# ========== CTA ==========
st.markdown("<div style='text-align:center; padding: 36px 0 24px;'>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 1.2, 1])
with c2:
    if st.button("🚀 Começar meu planejamento", use_container_width=True, type="primary", key="btn_start"):
        st.switch_page("pages/0_🚀_Começar.py")
st.markdown("</div>", unsafe_allow_html=True)

# ========== COMO FUNCIONA ==========
with st.expander("🤔 Nunca fez um planejamento estratégico? Clique aqui para entender"):
    st.markdown("""
    ### O que você vai construir aqui

    Imagine que você vai fazer uma viagem de carro. Você não sai dirigindo sem saber para onde vai, certo?
    O planejamento estratégico é o **mapa da sua empresa**. Ele responde:

    1. **Onde estamos hoje?** — Como funciona seu negócio? Quem são seus clientes? Quanto ganha?
    2. **O que tem ao redor?** — O que está acontecendo no mundo que pode ajudar ou atrapalhar?
    3. **Para onde vamos?** — Qual o sonho grande da empresa em 3 anos?
    4. **Como chegamos lá?** — Quais passos concretos, quem faz o quê, e até quando?

    > 💡 **Você não precisa fazer tudo de uma vez.** O SIPE10 salva automaticamente. 
    > Pode parar, voltar amanhã e continuar de onde parou.
    """)

# ========== PROGRESSO + ACESSIBILIDADE ==========
st.divider()

st.sidebar.title("🧭 SIPE10")
sidebar_data_controls()

with st.sidebar:
    st.markdown("---")
    st.markdown("### ♿ Acessibilidade")
    st.checkbox("Texto grande", key="a11y_large_text", help="Aumenta a fonte em 20%")
    st.checkbox("Alto contraste", key="a11y_high_contrast", help="Preto e branco para melhor legibilidade")
    st.checkbox("Reduzir animações", key="a11y_reduce_motion", help="Remove efeitos visuais")
    st.caption("Essas preferências ficam salvas apenas neste navegador.")

# Barra de progresso
st.subheader("📊 Seu progresso")
celebrate_progress(data)
