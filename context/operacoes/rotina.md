# Rotina de checagem

1. Rodar `hermeserenao check` (ou abrir o painel) e conferir o estado dos componentes.
2. Ler os últimos eventos em `state/events.jsonl` para entender o que aconteceu desde a última checagem.
3. Se um componente aparecer como `demo`, lembrar que ele é uma simulação local e não tem efeito externo.
4. Registrar apenas fatos operacionais no log. Nada de dados pessoais ou credenciais.

O agendador de exemplo mantém uma rotina habilitada (`healthcheck`) e uma desabilitada (`briefing`). Elas são configuração, não execução automática.
