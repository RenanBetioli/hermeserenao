# hermeserenao

Infraestrutura local de agente autônomo para experimentar, com uma interface própria e o Hermes Agent como runtime do agente. O MVP roda em `localhost`; não exige VPS nem domínio.

A interface conversa com o Hermes instalado nesta máquina, que usa o provider OpenAI/Codex Subscription. O app não usa uma chave da API OpenAI nem duplica o cérebro do Hermes.

## Estado atual

- Painel + API em Docker Compose, publicados apenas em `127.0.0.1:8765`.
- Busca determinística na base local, com arquivo e linha como citação.
- O chat se conecta ao API Server local do Hermes por rede loopback; o endpoint de busca permanece disponível para consulta rápida.
- Integrações e gateway multicanal são demonstrativos, sem acesso externo.
- Escopo do MVP local: [docs/MVP_SCOPE.md](docs/MVP_SCOPE.md).


## Rodando com Docker

    /usr/bin/python3.13 scripts/sync_hermes_key.py
    docker compose up --build -d
    # abrir http://127.0.0.1:8765
    docker compose down

Sem Docker (Python 3.13):

    set -a; . ./.env; set +a
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
- `POST /api/chat` — `{"messages": [{"role":"user","content":"..."}]}` → resposta do Hermes local com contexto recuperado

## Conexão com o cérebro Hermes

O endpoint `/api/chat` encaminha as mensagens ao API Server local do Hermes. A autenticação do modelo fica no Hermes; o app só usa a chave local do API Server, guardada no `.env` ignorado pelo Git. Não use `OPENAI_API_KEY` aqui.

## Segurança

A chave do API Server do Hermes fica em `.env` local (modo `0600`, ignorado pelo Git) e só é passada ao backend. `scripts/sync_hermes_key.py` copia apenas essa chave do arquivo privado do Hermes e nunca a imprime. O app e o API Server usam `network_mode: host` no Linux, mas escutam apenas em `127.0.0.1`. O API Server concede ao cliente acesso às ferramentas configuradas no Hermes, inclusive terminal; mantenha a porta local e revise permissões/solicitações do Hermes. Integrações de mensageria continuam stubs.

## Limitações

- O chat usa o Hermes já configurado; ele pode consumir os limites da assinatura escolhida. WhatsApp, Slack, Telegram e integrações de terceiros continuam fora do MVP.

## Licença

MIT.
