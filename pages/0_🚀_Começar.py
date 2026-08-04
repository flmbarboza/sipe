import streamlit as st
from utils.data_manager import init_data, get_data
from utils.ai_provider import AIProvider

st.set_page_config(page_title="Vamos começar", page_icon="🚀", layout="wide")
init_data()
data = get_data()

st.title("🚀 Vamos conhecer sua empresa")
st.caption("Essas informações ajudam a IA a dar sugestões mais relevantes. Pode alterar tudo depois.")

st.info("""
💡 **Dica do assistente:** Se você ainda está na fase de ideia, sem CNPJ ou local físico, 
tudo bem. O planejamento serve tanto para negócios que já funcionam quanto para quem está começando do zero.
""")

with st.form("dados_empresa"):
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input(
            "Qual o nome da sua empresa ou projeto?",
            value=data["empresa"]["nome"],
            help="Se ainda não tem nome definitivo, pode colocar um provisório.",
            placeholder="Ex: Padaria do Bairro, TechStart Brasil"
        )
        setor = st.text_input(
            "Em qual setor você atua?",
            value=data["empresa"]["setor"],
            help="Escolha o que mais se aproxima do que você faz hoje.",
            placeholder="Ex: Alimentação, Tecnologia, Comércio, Saúde"
        )
    with col2:
        local = st.text_input(
            "Onde fica sua empresa?",
            value=data["empresa"]["cidade_estado"],
            help="Cidade e estado ajudam a analisar fatores locais.",
            placeholder="Ex: São Paulo, SP"
        )
        responsavel = st.text_input(
            "Quem é o responsável pelo planejamento?",
            value=data["empresa"]["responsavel"],
            help="Pode ser você ou outra pessoa da equipe.",
            placeholder="Ex: Maria Silva, sócia-proprietária"
        )

    # Botões de fallback para incerteza
    col_fallback, col_submit = st.columns([1, 1])
    with col_fallback:
        st.markdown("<br>", unsafe_allow_html=True)
        fallback = st.form_submit_button("🤷 Ainda estou definindo", use_container_width=True)
    with col_submit:
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Continuar →", use_container_width=True, type="primary")

    if fallback:
        data["empresa"].update({
            "nome": nome or "Projeto em definição",
            "setor": setor or "Ainda definindo",
            "cidade_estado": local or "A definir",
            "responsavel": responsavel or "A definir"
        })
        st.success("Tudo bem! Você pode alterar essas informações a qualquer momento.")
        st.switch_page("pages/1_📋_Business_Model_Canvas.py")

    if submitted:
        data["empresa"].update({
            "nome": nome, "setor": setor,
            "cidade_estado": local, "responsavel": responsavel
        })
        st.switch_page("pages/1_📋_Business_Model_Canvas.py")

st.divider()

st.markdown("""
**📋 O que vem depois?**

Depois de conhecer sua empresa, vamos construir juntos:

1. **Modelo de negócio** — quem compra, o que vende, como ganha dinheiro
2. **Análise do ambiente** — o que está acontecendo no mundo ao redor
3. **SWOT** — seus pontos fortes, fracos, oportunidades e ameaças
4. **Plano de ação** — metas concretas com prazos e responsáveis
5. **Relatório final** — um documento profissional em PDF

> Não se preocupe em fazer tudo perfeito. Você pode voltar e ajustar qualquer etapa.
""")
