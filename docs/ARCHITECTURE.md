# Arquitetura

O sistema é um painel de controle local para uma infraestrutura de agente autônomo. Todos os componentes são lidos do filesystem; nenhum dado sai da máquina.

```mermaid
flowchart TB
  USER["Operador"] --> ACCESS["Acesso local<br>CLI / navegador / gateway"]
  MODELS["Modelos de IA<br>opcionais"] -.-> CORE
  ACCESS --> CORE["hermeserenao<br>núcleo"]
  CORE <--> CONTEXT["Contexto<br>memória · base · skills"]
  CORE <--> EXEC["Execução<br>terminal · arquivos · código"]
  CORE <--> INTEG["Integrações<br>adaptadores stub"]
  CORE --> CENTRAL["Central de Operações<br>painel + API"]
  LOCAL["Localhost 127.0.0.1"] --> CENTRAL
```

## Camadas

- **Acesso**: CLI (`hermeserenao.py`) e navegador. O gateway local registra eventos em `state/events.jsonl`.
- **Núcleo**: coordena consultas, status e skills. Não chama modelo de linguagem nesta versão.
- **Contexto**: `context/AGENTS.md`, índices recursivos e documentos Markdown. A busca de `/api/ask` devolve trecho, arquivo e linha.
- **Execução**: ambiente Python local; terminal, arquivos e código disponíveis para o operador.
- **Integrações**: `integrations/adapters.py` descreve capacidades sem autenticar em nenhum serviço.
- **Central**: API HTTP e painel em `app/static/index.html`.

## States

`ok` = componente real e verificável. `demo` = simulação local, sem efeito externo. `off` = ausente ou desabilitado.
