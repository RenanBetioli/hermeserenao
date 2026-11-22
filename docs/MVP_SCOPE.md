# Escopo do MVP local

## Objetivo

Executar uma experiência de agente pessoal nesta máquina, sem VPS, domínio ou serviço sempre ligado. A interface web do projeto deve usar o Hermes Agent instalado no host como runtime e cérebro. O Hermes já está autenticado no provider OpenAI/Codex Subscription; o projeto não deve criar uma segunda integração direta com a API da OpenAI nem exigir `OPENAI_API_KEY`.

## Princípios de arquitetura

1. **Um único agente e um único contexto.** A interface web, a CLI e futuros canais devem chegar ao mesmo runtime Hermes, mantendo memória, skills e ferramentas coerentes.
2. **Separar superfície e runtime.** `hermeserenao` fornece a central web, gestão dos materiais e UX; Hermes continua responsável por inferência, tool-calling, memória, skills e permissões.
3. **Local-first.** Serviços escutam apenas em loopback. Sem domínio, túnel público ou encaminhamento de porta no MVP.
4. **Fontes rastreáveis.** Materiais Markdown/PDF ficam na base local; respostas que dependem deles devem citar arquivo e, quando possível, página/linha.
5. **Aprovação humana.** Leitura e preparação podem ser automatizadas; envio de mensagens, publicação, escrita em serviços externos e outras ações irreversíveis exigem confirmação explícita.
6. **Integrações plugáveis.** Começar com adaptadores falsos/demonstração. OAuth e integrações reais entram depois, uma por vez, com escopo mínimo e tela de permissões.
7. **Multicanal depois do núcleo.** O primeiro canal é a interface web local. Mensageria, integrações e acesso móvel só entram após o fluxo local estar estável.

## Componentes do primeiro MVP

### 1. Central web

- Chat com o runtime Hermes; histórico mantido em memória pela página enquanto ela estiver aberta.
- Resposta não-streaming nesta fatia; streaming e eventos de ferramentas ficam para a próxima iteração.
- Painel com status do runtime, fontes e contexto recuperado; ainda não há fila visual de aprovações.
- Layout responsivo; informação de ambiente `LOCAL` sempre visível.

### 2. Conexão ao Hermes

Implementado via API Server oficial do Hermes no host (`127.0.0.1:8642`), usando o provider e a autenticação já configurados no Hermes. O container da Central usa rede host no Linux para falar com loopback; a porta da Central também fica em `127.0.0.1:8765`. `scripts/sync_hermes_key.py` copia apenas a chave local do API Server para um `.env` com modo `0600`, nunca versionado nem exibido. O navegador não recebe a chave.

### 3. Base de contexto

- A busca atual indexa arquivos Markdown em `context/`; o PDF fornecido foi lido nesta sessão, mas não foi copiado para o repositório nem há ingestão automática de PDF ainda.
- Guardar materiais pessoais em diretório local excluído do Git quando a ingestão de arquivos for implementada.
- A cada turno, recuperar até cinco trechos Markdown e passar caminho/linha ao Hermes; o painel mostra as fontes recuperadas.
- PDFs escaneados devem ser identificados como sem texto extraível; não fabricar conteúdo.
- O agente recebe materiais sob demanda, em vez de carregar transcrições grandes em toda conversa.

### 4. Integrações e automações

- Registrar conectores e permissões por ferramenta.
- Mostrar ações planejadas antes de executar.
- Implementar primeiro um modo simulado que registra o que faria sem chamar serviços externos.
- Agendamentos ficam desativados por padrão; executar só após revisão explícita.

### 5. Segurança local

- Bind de todos os serviços web em `127.0.0.1`.
- Segredos guardados pelo mecanismo de credenciais do Hermes, não em YAML versionado, frontend ou logs.
- Histórico de eventos sem credenciais, tokens ou conteúdo sensível desnecessário.
- Botão/ação visível para interromper uma execução longa.

## Fora do primeiro MVP

- VPS, domínio, Cloudflare, Tailscale e acesso público.
- WhatsApp, Slack, Telegram e bots ativos.
- OAuth de Composio ou de qualquer serviço de terceiros.
- Dashboard real de anúncios, e-mail, calendário ou contas pessoais.
- Execução autônoma recorrente e envio proativo de mensagens.
- Kubernetes; Compose basta para a camada web local, se ela realmente precisar de container.

## Critérios de aceite

1. O operador abre a central web em localhost e conversa com o Hermes que já está configurado no host.
2. O Hermes responde usando a sessão/provider atual, sem chave OpenAI API separada.
3. O operador consegue consultar materiais locais e recebe citações que apontam a arquivos existentes.
4. O modo simulado mostra uma ação externa proposta sem executá-la.
5. O sistema continua funcional se não houver arquivos de contexto e informa isso claramente.
6. Testes cobrem o conector e o modo simulado sem fazer chamadas pagas nem ações externas.

## Estado da decisão técnica

A conexão inicial foi validada pelo API Server do Hermes. O serviço concede acesso às ferramentas configuradas no Hermes, inclusive terminal; por isso, a Central deve permanecer em loopback e a chave deve ficar apenas no backend. A resposta ainda não é transmitida em streaming e o chat não exibe uma fila de aprovações própria. O próximo ciclo pode acrescentar streaming, sessões persistentes e um fluxo visual de aprovação antes de adicionar canais ou OAuth externos.
