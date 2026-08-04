import streamlit as st
from utils.page_template import setup_page, track_page
from utils.ai_helper import ai_assist_widget
from utils.contextual_helper import render_contextual_helper
from utils.ai_provider import AIProvider

st.set_page_config(page_title="Business Model Canvas", page_icon="📋", layout="wide")
data = setup_page("Business Model Canvas", "📋")
tracker = track_page("Business Model Canvas")

st.title("📋 Como sua empresa funciona?")
st.caption("Vamos desenhar o modelo de negócio — um mapa simples que mostra como sua empresa cria valor e ganha dinheiro.")

st.info("""
**O que é um modelo de negócio?**  
É como um blueprint da sua empresa. Responde perguntas simples: quem compra de você? O que você vende? Como entrega? Quanto custa para produzir? Quanto ganha?  
Empresas que têm isso claro crescem com mais segurança.

💡 **Não precisa preencher tudo de uma vez.** Clique em qualquer cartão abaixo para começar. 
Não sabe o que colocar? Use o botão "Consultar IA" — ele dá exemplos do seu setor.
""")

# ========== BMC GRID ==========
bmc = data["bmc"]
setor = data.get("empresa", {}).get("setor", "geral")

# Mapeamento dos 9 blocos com explicações leigas
BLOCOS = [
    ("segmentos_clientes", "🎯 Clientes", "Quem compra ou usa o que você oferece?", 
     "Pense em: quem compra? quem usa? Existem grupos diferentes? Ex: jovens de 18-25 anos, pequenas empresas, pais de crianças..."),
    ("proposta_valor", "💎 Proposta de valor", "Qual problema você resolve e qual valor entrega?",
     "Pense em: qual necessidade você atende? Que benefício entrega? O que diferencia sua solução? Ex: preço acessível, maior qualidade, conveniência..."),
    ("canais", "📡 Canais", "Como o cliente encontra, compra e recebe sua solução?",
     "Considere: divulgação, venda, entrega, atendimento. Ex: loja física, Instagram, site, WhatsApp..."),
    ("relacionamento_clientes", "❤️ Relacionamento", "Como sua empresa conquista e mantém clientes?",
     "Exemplos: atendimento personalizado, programa de fidelidade, comunidade, suporte pós-venda..."),
    ("fontes_receita", "💰 Receitas", "Como sua empresa ganha dinheiro?",
     "Considere: o que o cliente paga? Como paga? Qual modelo de cobrança? Ex: venda direta, assinatura mensal, comissão..."),
    ("recursos_chave", "🧱 Recursos", "Quais recursos são necessários para o negócio funcionar?",
     "Podem ser: pessoas, equipamentos, tecnologia, marca, capital. Ex: equipe especializada, máquinas, sistema de gestão..."),
    ("atividades_chave", "⚙️ Atividades", "Quais são as tarefas mais importantes do dia a dia?",
     "O que você faz todos os dias para entregar valor? Ex: produzir, vender, atender, entregar..."),
    ("parcerias_chave", "🤝 Parcerias", "Quem ajuda você a entregar valor?",
     "Fornecedores, distribuidores, parceiros estratégicos. Ex: fornecedor de matéria-prima, plataforma de pagamentos..."),
    ("estrutura_custos", "💸 Custos", "Quais são os principais gastos para manter tudo funcionando?",
     "Aluguel, salários, matéria-prima, marketing, impostos. Liste os maiores custos mensais."),
]

for chave, titulo, pergunta, dica in BLOCOS:
    with st.container():
        st.markdown(f"---")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(titulo)
            st.caption(pergunta)
        with col2:
            # Status de preenchimento
            if bmc.get(chave, "").strip():
                st.success("✅ Preenchido")
            else:
                st.info("⏳ Aguardando")

        # Campo com tooltip e fallback
        col_input, col_help = st.columns([3, 1])
        with col_input:
            valor = st.text_area(
                f"Descreva aqui",
                value=bmc.get(chave, ""),
                key=f"bmc_{chave}",
                help=dica,
                placeholder="Escreva com suas palavras. Não precisa ser perfeito."
            )
            if valor != bmc.get(chave, ""):
                bmc[chave] = valor

        with col_help:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🤷 Não sei ainda", key=f"help_{chave}"):
                st.info(f"""
                **Tudo bem!** Aqui estão perguntas para te ajudar:

                {dica}

                Ou use o botão "Consultar IA" abaixo para ver exemplos do setor **{setor}**.
                """)

        # IA Assist
        system = f"""Você é um consultor de negócios. O usuário está preenchendo o bloco \"{titulo}\" do Business Model Canvas para uma empresa do setor {setor}.
Dê sugestões práticas, exemplos reais e valide o que foi escrito. Seja encorajador."""

        def prompt_builder(instrucao):
            contexto = f"Setor: {setor}\nBloco: {titulo}\nPergunta: {pergunta}\nTexto atual: {bmc.get(chave, '')}"
            if instrucao.strip():
                return f"{contexto}\n\nPedido do usuário: {instrucao}"
            return f"{contexto}\n\nSugira preenchimentos ou exemplos para este bloco."

        sugestao = ai_assist_widget(f"bmc_{chave}", titulo, system, prompt_builder)
        if sugestao:
            bmc[chave] = sugestao
            st.rerun()

st.divider()

# Navegação
st.markdown("### Próximo passo")
st.markdown("Depois de entender seu modelo de negócio, vamos analisar o ambiente ao redor da sua empresa.")
if st.button("Ir para Análise PESTEL →", type="primary"):
    st.switch_page("pages/2_🌍_Análise_PESTEL.py")

# Sidebar: assistente contextual
render_contextual_helper("Business Model Canvas", data)
