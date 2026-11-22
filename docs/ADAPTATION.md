# Adaptação: de VPS para máquina local

| Item | Desenho de servidor | Versão local |
| --- | --- | --- |
| Sistema | VPS Ubuntu 24.04 | Linux local (ou qualquer host Docker) |
| Acesso | SSH + domínio + DNS | `127.0.0.1:8765` |
| Agente | harness instalado na VPS | núcleo demonstrado pela API |
| Canais | mensageria externa | log de eventos local |
| Integrações | CLI com OAuth | adaptadores stub |
| Modelo | assinatura ou API paga | nenhuma chamada |
| Persistência | disco da VPS | volumes locais do Compose |

## Como migrar depois

1. Trocar `run_server(host=...)` para escutar na interface desejada e colocar um proxy reverso na frente.
2. Substituir o gateway de eventos por um adaptador real de canal.
3. Substituir a busca determinística por um agente com modelo, mantendo o contrato de resposta com citação.
4. Implementar os adaptadores de integração com credenciais vindas de cofre, nunca de arquivos versionados.
5. Adicionar autenticação à API antes de expor o painel fora de localhost.

## Docker

`docker compose up --build`sobe o serviço na porta 8765. O volume `./state` preserva eventos entre recreações do container; `./context` é montado somente leitura.
