# hermeserenao

Infraestrutura de agente autônomo adaptada para rodar **local**, sem VPS, domínio, Cloudflare ou assinatura paga. É um projeto de portfólio: implementação própria inspirada na arquitetura da Imersão Agentes Autônomos da PycodeBR.

A ideia original monta um Hermes Agent em uma VPS Ubuntu 24.04, atrás de domínio, com canais Slack/WhatsApp/Telegram, Composio, Tailscale e uma Central de Operações. Aqui o mesmo desenho é reduzido ao que roda em uma máquina comum: núcleo do agente, memória, base de contexto, skills, camada de execução, integrações e painel — tudo em `localhost`.

## O que mudou em relação ao desenho original

| Original (imersão) | hermeserenao (local) |
| --- | --- |
| VPS Ubuntu 24.04 + SSH | Mint1 local, um único processo Python |
| Domínio + Cloudflare | `127.0.0.1:8765` |
| Hermes Agent na VPS | núcleo local com interface para plugar um agente real depois |
| Gateway Slack/WhatsApp/Telegram | gateway local com log de eventos em `state/events.jsonl` |
| Composio CLI + OAuth | adaptadores stub em `integrations/` |
| Provedor de modelo pago | sem chamadas de modelo; busca determinística na base de contexto |
| Orca / Tailscale / Desktop | fora de escopo (dependem de servidor remoto) |

## Rodando com Docker

    docker compose up --build
    # a porta so escuta em 127.0.0.1: http://127.0.0.1:8765
    docker compose down

Sem Docker (Python 3.13):

    /usr/bin/python3.13 hermeserenao.py check
    /usr/bin/python3.13 hermeserenao.py serve
    # abrir http://127.0.0.1:8765

Consultar a base de contexto pela CLI:

    /usr/bin/python3.13 hermeserenao.py ask "como lidar com segredos"

Testes:

    /usr/bin/python3.13 -m unittest discover -s tests -v

Verificação de segredos:

    /usr/bin/python3.13 scripts/check_secrets.py

## Estrutura

    hermeserenao.py        CLI (check, serve, ask)
    app/server.py          API HTTP e arquivos estáticos (stdlib)
    app/architecture.py    gerador do diagrama SVG
    app/static/index.html  Central de Operações
    context/               base de contexto (segundo cérebro)
    skills/                registro de skills
    integrations/          adaptadores stub
    state/events.jsonl     eventos do gateway local
    docs/                  arquitetura e guia de adaptação
    Dockerfile
    docker-compose.yml

## Endpoints

- `GET /` — painel
- `GET /api/status` — estado dos componentes, lido do filesystem
- `GET /api/context` — documentos indexados
- `GET /api/skills` — skills registradas
- `GET /api/events` — últimos eventos
- `GET /api/architecture.svg` — diagrama gerado
- `POST /api/ask` — `{"question": "..."}` → trechos com citação de arquivo e linha

## Segurança

Nenhuma credencial é lida, enviada ou armazenada. O `.gitignore` exclui `.env` e chaves. O script `check_secrets.py` falha se encontrar padrões de token no repositório. As integrações são stubs: não autenticam em nada.

## Limitações

Isto **não é** o Hermes Agent e não executa tarefas autonomamente. O gateway e as integrações são simulações locais; não há chamada a LLM, WhatsApp, Slack ou Composio. A finalidade é demonstrar a arquitetura, a base de contexto e a interface de forma reproduzível e sem custo.

## Licença

MIT.
