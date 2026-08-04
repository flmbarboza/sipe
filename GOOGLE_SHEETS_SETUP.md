# Guia de Configuração — Google Sheets (Rastreamento UX)

Este guia explica passo a passo como configurar o rastreamento de UX no Google Sheets.

## Passo 1: Criar projeto no Google Cloud

1. Acesse [console.cloud.google.com](https://console.cloud.google.com/)
2. Clique no seletor de projeto (topo) → **New Project**
3. Dê um nome (ex: `sipe10-ux-tracking`) e clique **Create**

## Passo 2: Ativar a API do Google Sheets

1. No menu lateral, vá em **APIs & Services > Library**
2. Procure por **Google Sheets API**
3. Clique em **Enable**

## Passo 3: Criar Service Account

1. Vá em **IAM & Admin > Service Accounts**
2. Clique **Create Service Account**
3. Nome: `sipe10-ux-exporter`
4. Role: **Editor** (ou **Google Sheets Editor** se quiser mais restrito)
5. Clique **Done**

## Passo 4: Gerar chave JSON

1. Na lista de Service Accounts, clique no email criado
2. Vá na aba **Keys**
3. Clique **Add Key > Create New Key**
4. Selecione **JSON** e clique **Create**
5. Um arquivo `.json` será baixado — guarde com segurança

## Passo 5: Criar e compartilhar a planilha

1. Vá no [Google Sheets](https://sheets.google.com) e crie uma planilha em branco
2. Dê um nome (ex: `SIPE10_UX_Analytics`)
3. Clique em **Share** (compartilhar)
4. Cole o `client_email` do Service Account (está no JSON baixado)
5. Dê permissão de **Editor**
6. Copie o ID da planilha da URL (a parte entre `/d/` e `/edit`)

## Passo 6: Configurar no Streamlit

Crie o arquivo `.streamlit/secrets.toml` na raiz do projeto:

```toml
[google]
type = "service_account"
project_id = "SEU_PROJECT_ID"
private_key_id = "SEU_PRIVATE_KEY_ID"
private_key = "-----BEGIN PRIVATE KEY-----\nSUA_CHAVE_AQUI\n-----END PRIVATE KEY-----\n"
client_email = "sua-conta@seu-projeto.iam.gserviceaccount.com"
client_id = "SEU_CLIENT_ID"
client_x509_cert_url = "SEU_CERT_URL"
```

> ⚠️ **Importante:** A `private_key` deve ter `\n` (dois caracteres: backslash + n) no lugar de quebras de linha reais.

### Como converter a chave:

Se seu JSON tem a chave assim:
```json
"private_key": "-----BEGIN PRIVATE KEY-----
MIIE...
-----END PRIVATE KEY-----
"
```

No `secrets.toml`, troque `
` por `\n`:
```toml
private_key = "-----BEGIN PRIVATE KEY-----\nMIIE...\n-----END PRIVATE KEY-----\n"
```

## Passo 7: Testar

1. Rode o app: `streamlit run app.py`
2. Navegue por algumas páginas
3. Aguarde até 60 segundos (ou preencha 100 eventos)
4. Verifique a planilha — a aba "Eventos" será criada automaticamente

## Eventos rastreados

| Evento | Quando ocorre |
|--------|---------------|
| `page_view` | Ao carregar cada página |
| `field_focus` | Ao clicar em um campo |
| `field_blur` | Ao sair de um campo (com tempo e caracteres) |
| `ai_assist_open` | Ao abrir o expander de IA |
| `ai_assist_request` | Ao clicar em "Consultar IA" |
| `ai_assist_accept` | Ao aceitar uma sugestão da IA |
| `export_json` | Ao baixar dados em JSON |
| `export_pdf` | Ao gerar PDF |
| `error` | Ao ocorrer um erro |
| `section_complete` | Ao completar uma seção |

## Limites da API (gratuita)

- 500 requisições / 100 segundos / projeto
- 100 requisições / 100 segundos / usuário
- Sem custo — se exceder, recebe erro 429 (tenta novamente depois)
