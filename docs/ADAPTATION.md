# Adaptação: de VPS para máquina local

| Item | Desenho de servidor | Versão local |
| --- | --- | --- |
| Sistema | VPS Ubuntu 24.04 | Linux local (ou qualquer host Docker) |
| Acesso | SSH + domínio + DNS | `127.0.0.1:8765` |
| Agente | Hermes Agent rodando na VPS | Hermes Agent do host via API Server em loopback |
| Canais | WhatsApp/Slack/Telegram | chat web local; mensageria externa depois |
| Integrações | hub OAuth | adaptadores stub, sem autenticação externa |
| Modelo | provider configurado no agente | OAuth já configurado no Hermes; sem `OPENAI_API_KEY` no app |
| Persistência | disco da VPS | volumes locais do Compose; `.env` privado e ignorado pelo Git |

## Próximos passos antes de qualquer exposição externa

1. Implementar streaming e continuidade de sessões na interface.
2. Criar uma camada visual de aprovação para ferramentas e ações externas.
3. Adicionar autenticação de usuário e proteção contra CSRF.
4. Só então avaliar mensageria externa e OAuth de integrações, com permissões mínimas.
5. Nunca expor o API Server do Hermes em endereço público; manter sua chave apenas no backend.

## Docker

`python3.13 scripts/sync_hermes_key.py` cria um `.env` local de modo `0600` contendo apenas a chave do API Server. `docker compose up --build -d` sobe a Central. No Linux, o Compose usa `network_mode: host` para acessar o Hermes em `127.0.0.1:8642`; o app fica preso a `127.0.0.1:8765`. O volume `./state` preserva eventos; `./context` é somente leitura.
