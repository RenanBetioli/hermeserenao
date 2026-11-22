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

- Chat com o runtime Hermes e histórico de sessões.
- Exibição de resposta em streaming e eventos de ferramentas/estado, caso suportados pelo endpoint escolhido.
- Painel lateral com status do runtime, fontes de contexto e ações pendentes.
- Layout responsivo; informação de ambiente `LOCAL` sempre visível.

### 2. Conexão ao Hermes

Usar a interface programática oficial do Hermes em execução no host, não chamar diretamente um modelo por API key. Antes de implementar o conector, validar no host o modo suportado e a autenticação local; não expor endpoint na rede local ou internet. Nenhuma chave ou token entra no repositório ou no frontend.

### 3. Base de contexto

- Ingerir arquivos Markdown e PDFs fornecidos pelo operador.
- Guardar arquivos no diretório local de materiais; nunca copiar documentos originais para Git sem autorização.
- Buscar trechos com metadados da fonte e oferecer citações verificáveis.
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

## Decisão técnica pendente antes do conector

O Hermes tem superfícies oficiais diferentes para integração programática. A escolha deve considerar streaming, aprovação de ferramentas, autenticação, persistência de sessões e se o processo precisa rodar no host ou pode ser acessado pelo container. Validar a configuração local atual primeiro; não habilitar um serviço global nem criar segredo sem revisão do operador.
