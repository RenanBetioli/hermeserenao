# hermeserenao

Infraestrutura local de agente autônomo para experimentar, com uma interface própria e o Hermes Agent como runtime do agente. O MVP roda em `localhost`; não exige VPS nem domínio.

A primeira versão já oferece painel, API local, base Markdown com busca citável, diagrama e adaptadores demonstrativos. O próximo passo é conectar a interface ao Hermes instalado nesta máquina, que já usa o provider OpenAI/Codex Subscription. O app não deve usar uma chave da API OpenAI nem duplicar o cérebro do Hermes.

## Estado atual

- Painel + API em Docker Compose, publicados apenas em `127.0.0.1:8765`.
- Busca determinística na base local, com arquivo e linha como citação.
- O endpoint de resposta ainda não está conectado ao Hermes Agent.
- Integrações e gateway multicanal são demonstrativos, sem acesso externo.
- Escopo do MVP local: [docs/MVP_SCOPE.md](docs/MVP_SCOPE.md).


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

## Conexão com o cérebro Hermes

O MVP deve se conectar ao Hermes Agent instalado no host e aproveitar o provider OAuth já configurado nele. Não é necessário colocar `OPENAI_API_KEY` no projeto. A integração programática e a autenticação local ainda precisam ser implementadas e validadas; até lá, `/api/ask` continua usando busca determinística.

## Segurança

Nenhuma credencial é lida, enviada ou armazenada. O `.gitignore` exclui `.env` e chaves. O script `check_secrets.py` falha se encontrar padrões de token no repositório. As integrações são stubs: não autenticam em nada.

## Limitações

Isto **não é** o Hermes Agent e não executa tarefas autonomamente. O gateway e as integrações são simulações locais; não há chamada a LLM, WhatsApp, Slack ou Composio. A finalidade é demonstrar a arquitetura, a base de contexto e a interface de forma reproduzível e sem custo.

## Licença

MIT.
