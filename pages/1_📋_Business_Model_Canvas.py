import streamlit as st
from utils.page_template import setup_page, track_page
from utils.pdf_export import markdown_to_pdf_bytes
from utils.contextual_helper import render_contextual_helper

st.set_page_config(page_title="Relatório Completo", page_icon="📄", layout="wide")
data = setup_page("Relatório Completo", "📄")
tracker = track_page("Relatório Completo")

st.title("📄 Relatório Completo")
st.caption("Gere um documento profissional com todo o seu planejamento estratégico.")

def build_report(data):
    emp = data.get("empresa", {})
    bmc = data.get("bmc", {})
    swot = data.get("swot", {})
    mvv = data.get("mvv", {})
    objs = data.get("objetivos", [])
    acoes = data.get("acao_5w2h", [])
    fin = data.get("financeiro", {})

    report = f"""# Relatório Estratégico — {emp.get('nome', 'Empresa')}

## 1. Dados da Empresa
- **Nome:** {emp.get('nome', 'Não informado')}
- **Setor:** {emp.get('setor', 'Não informado')}
- **Local:** {emp.get('cidade_estado', 'Não informado')}
- **Responsável:** {emp.get('responsavel', 'Não informado')}

## 2. Modelo de Negócio (Business Model Canvas)
- **Clientes:** {bmc.get('segmentos_clientes', 'Não preenchido')}
- **Proposta de Valor:** {bmc.get('proposta_valor', 'Não preenchido')}
- **Canais:** {bmc.get('canais', 'Não preenchido')}
- **Relacionamento:** {bmc.get('relacionamento_clientes', 'Não preenchido')}
- **Receitas:** {bmc.get('fontes_receita', 'Não preenchido')}
- **Recursos:** {bmc.get('recursos_chave', 'Não preenchido')}
- **Atividades:** {bmc.get('atividades_chave', 'Não preenchido')}
- **Parcerias:** {bmc.get('parcerias_chave', 'Não preenchido')}
- **Custos:** {bmc.get('estrutura_custos', 'Não preenchido')}

## 3. Análise SWOT
### Forças
"""
    for f in swot.get("forcas", []):
        report += f"- {f.get('descricao', '')}\n"

    report += "### Fraquezas\n"
    for f in swot.get("fraquezas", []):
        report += f"- {f.get('descricao', '')}\n"

    report += "### Oportunidades\n"
    for f in swot.get("oportunidades", []):
        report += f"- {f.get('descricao', '')}\n"

    report += "### Ameaças\n"
    for f in swot.get("ameacas", []):
        report += f"- {f.get('descricao', '')}\n"

    report += f"""
## 4. Missão, Visão e Valores
- **Missão:** {mvv.get('missao', 'Não preenchido')}
- **Visão:** {mvv.get('visao', 'Não preenchido')}
- **Valores:** {', '.join(mvv.get('valores', [])) or 'Não preenchido'}

## 5. Objetivos Estratégicos
"""
    for o in objs:
        report += f"- **{o.get('objetivo', '')}** — KPI: {o.get('kpi', '')} | Meta: {o.get('meta', '')} | Prazo: {o.get('prazo', '')}\n"

    report += "\n## 6. Plano de Ação (5W2H)\n"
    for a in acoes:
        report += f"- **{a.get('what', '')}** — Quem: {a.get('who', '')} | Quando: {a.get('when', '')} | Como: {a.get('how', '')}\n"

    report += f"""
## 7. Orçamento
- **Investimento Inicial:** R$ {fin.get('investimento_inicial', 0):,.2f}
- **Receitas Mensais:** R$ {sum(r.get('valor', 0) for r in fin.get('receitas', [])):,.2f}
- **Custos Mensais:** R$ {sum(c.get('valor', 0) for c in fin.get('custos', [])):,.2f}

---
*Relatório gerado pelo SIPE10 — Planejamento Estratégico*
"""
    return report

st.subheader("📄 Pré-visualização")
report_md = build_report(data)
st.markdown(report_md)

st.subheader("⬇️ Exportar")
col1, col2 = st.columns(2)
with col1:
    st.download_button(
        "Baixar como Markdown",
        data=report_md,
        file_name="relatorio_estrategico.md",
        mime="text/markdown",
        use_container_width=True
    )
with col2:
    try:
        pdf_bytes = markdown_to_pdf_bytes(report_md)
        st.download_button(
            "Baixar como PDF",
            data=pdf_bytes,
            file_name="relatorio_estrategico.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Erro ao gerar PDF: {e}")
        st.info("💡 Para PDF com acentos corretos, baixe as fontes DejaVuSans e coloque em utils/fonts/")

render_contextual_helper("Relatório Completo", data)
