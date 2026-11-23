# Acesso remoto privado (Tailscale Serve)

Este guia é para o operador abrir a Central no próprio celular, fora da rede de casa. **Não publica o projeto na internet.** Não use Tailscale Funnel nem encaminhamento de porta do roteador: o backend da Central não tem autenticação por usuário e repassa o chat ao Hermes, que dispõe de ferramentas locais.

## Topologia e limites

- A Central continua em `127.0.0.1:8765`; o API Server do Hermes continua em `127.0.0.1:8642`. Não alterar esses binds nem expor a porta do Hermes.
- Tailscale Serve oferece HTTPS e encaminha **somente a Central** aos dispositivos autorizados na tailnet. Confira os membros e as regras de acesso antes de ativar: qualquer membro com permissão para acessar este dispositivo pode atingir as rotas da Central, inclusive `/api/chat` e `/api/document`.
- A máquina precisa estar ligada e conectada ao Tailscale. O celular também precisa estar conectado ao Tailscale para abrir a URL privada.
- Não salvar no GitHub: URL/hostname da tailnet, IPs privados, chaves, tokens, configuração de acesso pessoal ou dados de contexto privados.

## Instalação e ativação (na máquina do operador)

A máquina usa Linux Mint baseado em Ubuntu. Instalar Tailscale é uma alteração de sistema e requer autorização administrativa do operador; o agente não executa `sudo`, não digita senhas e não faz o login por ele.

1. Instalar pelo instalador oficial **executado pelo operador** (ler a origem antes de executar):

   ```sh
   curl -fsSL https://tailscale.com/install.sh | sh
   ```

2. Conectar a máquina à sua tailnet e concluir o login na página aberta pelo Tailscale. Se o comando pedir privilégio administrativo, o próprio operador o fornece:

   ```sh
   sudo tailscale up
   ```

3. Verificar no painel do Tailscale se só os dispositivos autorizados podem acessar esta máquina. Na máquina, confirmar que os dois serviços locais ainda escutam em loopback e que a Central responde em `http://127.0.0.1:8765/api/status`.

4. Ativar o proxy privado, sem root quando as permissões do Tailscale permitirem:

   ```sh
   tailscale serve --bg 8765
   tailscale serve status
   ```

   Na primeira ativação, o Tailscale pode informar que **Serve não está habilitado na tailnet** e mostrar uma página de autorização. O operador deve abrir essa página no próprio navegador, entrar e aprovar **apenas Serve/HTTPS**, deixando Funnel desmarcado; em seguida, repetir o comando e conferir o status. Não copiar a URL de autorização, identificadores ou tokens para o repositório. Se o comando sem privilégios retornar `Access denied: serve config denied`, o operador pode executar **uma única vez** `sudo tailscale serve --bg 8765` no próprio terminal. Isso é mais restrito que dar ao usuário permissão permanente para administrar o Tailscale (`set --operator`); o agente nunca digita a senha nem roda `sudo`.

5. Instalar o app Tailscale no celular, entrar na mesma tailnet e abrir a URL HTTPS privada exibida por `tailscale serve status`, usando dados móveis (Wi-Fi desligado) para testar acesso remoto real. Testar painel e chat. Confirmar que a URL não abre em dispositivo/navegador fora da tailnet.

6. Para desativar o acesso, confira `tailscale serve status` e remova somente a configuração da Central conforme `tailscale serve --help`; não apague configurações de outros serviços por engano.

## Critérios de aceite

- Central local e Hermes local continuam saudáveis; ambas as portas permanecem em `127.0.0.1`.
- Celular autorizado consegue abrir a URL privada por dados móveis e conversar com o Hermes.
- Acesso de dispositivo fora da tailnet é recusado; ninguém recebeu URL pública.
- Nenhum segredo, identificador de tailnet ou dado privado foi enviado ao GitHub.

## Estado desta instalação (22/11/2026)

- Tailscale Serve ativado pelo operador; HTTPS privado encaminha somente a Central na porta local `8765`. Funnel não foi ativado.
- Verificações pela URL HTTPS privada **na própria máquina**: painel, `/api/status` e `/api/chat` responderam HTTP 200; Hermes permaneceu em loopback.
- **Pendente:** abrir a Central no celular pela rede móvel com Tailscale conectado e confirmar que um dispositivo sem Tailscale não consegue acessá-la. Não registrar aqui a URL ou IP da tailnet.

## Se a ideia mudar para acesso público

Este guia não serve para visitantes públicos. Antes disso será necessário separar o agente pessoal, autenticar cada usuário, restringir ferramentas, isolar dados, limitar uso e revisar o provedor/modelo e custos. Nunca trocar o bind para `0.0.0.0` nem ativar Funnel no app atual.
