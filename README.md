# SIPE10 v2 — Planejamento Estratégico

Assistente de planejamento estratégico para empresas de todos os tamanhos. 
Construído com foco em **usuários leigos**: sem jargão, com contexto, ajuda contextual e celebração de progresso.

## ✨ O que há de novo na v2

| Melhoria | Descrição |
|----------|-----------|
| 🏠 **Tela de boas-vindas** | Explica o que é planejamento estratégico e por que fazer |
| 🚀 **Onboarding guiado** | Coleta dados da empresa antes de jogar formulários na tela |
| 💬 **Assistente contextual** | Chat no sidebar que sabe em qual página você está |
| 🤖 **IA unificada** | Suporte a Anthropic, OpenAI e OpenRouter em uma única interface |
| 🛡️ **Chaves estáveis** | `data_editor` não perde mais o foco do usuário |
| 📊 **Rastreamento UX** | Eventos de uso enviados em lote para Google Sheets |
| ✅ **Validação de dados** | Identifica campos vazios e inconsistências com mensagens amigáveis |
| 📄 **PDF com acentos** | Usa fonte DejaVuSans para `ç`, `ã`, `é` corretos |
| 🎉 **Celebração de progresso** | Balões e toast em marcos de 20%, 50% e 90% |
| ♿ **Acessibilidade** | Texto grande, alto contraste, redução de animações |

## 🚀 Como rodar localmente

```bash
# 1. Clone ou copie os arquivos
cd sipe10_v2

# 2. Crie um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure os secrets (veja abaixo)
# Crie o arquivo .streamlit/secrets.toml

# 5. Rode o app
streamlit run app.py
```

## 🔐 Configuração de Secrets

Crie o arquivo `.streamlit/secrets.toml`:

```toml
# IA (escolha um ou mais)
ANTHROPIC_API_KEY = "sk-ant-..."
OPENAI_API_KEY = "sk-..."

# Google Sheets (para rastreamento UX)
[google]
type = "service_account"
project_id = "seu-projeto-id"
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "sua-conta@seu-projeto.iam.gserviceaccount.com"
client_id = "..."
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
```

> ⚠️ **Atenção:** A `private_key` deve ter `\n` no lugar de quebras de linha reais.

## 📊 Google Sheets — Rastreamento UX

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um projeto → **IAM & Admin > Service Accounts**
3. Crie uma Service Account com role **Editor**
4. Gere uma chave JSON e baixe
5. Compartilhe uma planilha no Google Sheets com o `client_email` da Service Account
6. Copie os valores do JSON para o `secrets.toml`

A planilha será criada automaticamente com as abas:
- **Eventos** — todos os eventos de UX (page_view, field_focus, ai_request, etc.)
- **Sessoes** — resumo de cada sessão do usuário

## 📁 Estrutura de arquivos

```
sipe10_v2/
├── app.py                          # Ponto de entrada
├── requirements.txt                # Dependências
├── .streamlit/
│   └── config.toml                 # Tema e configurações
├── utils/
│   ├── page_template.py            # Template padrão de página
│   ├── data_manager.py             # Gerenciamento de dados
│   ├── ai_provider.py              # Provedor unificado de IA
│   ├── ai_helper.py                # Widget de assistência IA
│   ├── editors.py                  # Data editor com chaves estáveis
│   ├── validators.py               # Validação de dados
│   ├── pdf_export.py               # Geração de PDF Unicode
│   ├── ux_tracker.py               # Rastreamento de UX
│   ├── google_sheets_exporter.py   # Exportador para Sheets
│   ├── contextual_helper.py        # Assistente no sidebar
│   ├── progress_celebration.py     # Celebração de marcos
│   └── a11y.py                     # Acessibilidade
└── pages/
    ├── 00_🏠_Início.py             # Home contextualizada
    ├── 0_🚀_Começar.py             # Onboarding
    ├── 1_📋_Business_Model_Canvas.py
    ├── 2_🌍_Análise_PESTEL.py
    ├── 3_⚔️_5_Forças_de_Porter.py
    ├── 4_🎯_Análise_SWOT.py
    ├── 5_🧭_Planejamento_Estratégico.py
    ├── 6_✅_Plano_de_Ação_5W2H.py
    ├── 7_📋_Planos_por_Função.py
    ├── 8_💰_Orçamento.py
    ├── 9_🛃_Monitoramento.py
    ├── 10_🔄_Revisão.py
    ├── 11_📈_Painel_de_Controle.py
    └── 12_📄_Relatório_Completo.py
```

## 📝 Notas importantes

- **Google Sheets API é gratuita** — não há custo para uso normal
- **A private_key no secrets.toml** deve ter `\n` (escapado) em vez de quebras de linha reais
- **Para PDF com acentos:** baixe [DejaVuSans](https://dejavu-fonts.github.io/) e coloque `DejaVuSans.ttf` e `DejaVuSans-Bold.ttf` em `utils/fonts/`
- **Dados ficam na sessão** — use o botão "Baixar dados (.json)" para persistir

## 🙏 Créditos

Desenvolvido por [flmbarboza](https://github.com/flmbarboza) com apoio de IA.
