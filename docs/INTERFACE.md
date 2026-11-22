# Interface da Central de Operações

## Composição

A superfície principal é de operação: navegação lateral persistente, visão geral do workspace e ações de trabalho. O diagnóstico técnico e o diagrama ficam em uma área secundária, não no centro da experiência.

A interface é original e usa HTML, CSS e JavaScript nativos, sem framework, fonte externa ou CDN.

## Sistema visual

- Fundo: `#f1f4f7`; superfícies: `#ffffff`.
- Texto principal: `#0a1317`; texto secundário: `#5d6c7b`.
- Ações: `#0064e0`; hover principal: `#0457cb`.
- Divisores: `#dee3e9`.
- Tipografia: Segoe UI / Arial; monospace apenas para caminhos e metadados técnicos.
- Cartões de conteúdo com borda leve e raio de 16 px; botões principais em formato pill.
- Verde significa disponibilidade; amarelo indica demonstração. Os estados também têm rótulos, não dependem só de cor.

## Áreas funcionais

1. **Visão geral**: disponibilidade do runtime, quantidade real de materiais, início de conversa e registros recentes.
2. **Conversar com Hermes**: chat conectado ao API Server local. Contexto recuperado aparece como fonte, sem alegar que foi necessariamente usado na resposta. Histórico apenas na memória da aba.
3. **Materiais**: lista dos arquivos Markdown reais, filtros por domínio, busca citável e leitura em diálogo. O endpoint de leitura aceita somente arquivos registrados sob `context/`, não caminhos arbitrários.
4. **Atividade**: registros do portal em ordem de gravação inversa, com filtro por tipo. Não representa todo o histórico do Hermes.
5. **Integrações**: explica a etapa de consentimento. O botão prepara uma mensagem no chat, sem iniciar OAuth ou conceder permissões automaticamente.
6. **Sistema e rotinas**: componentes, skills do registro demonstrativo, rotinas de exemplo e arquitetura técnica recolhida.

## Limites de apresentação

- Não criar métricas de custo, tokens, produtividade ou tempo de execução sem fonte real.
- Não exibir integrações como conectadas sem verificação do serviço.
- Não simular importação de PDF nem incluir upload sem implementação.
- Não chamar o registro demonstrativo de skills de catálogo completo do Hermes.
- Não tratar o feed local como auditoria completa das ferramentas do agente.

## Acessibilidade e responsividade

- Navegação com botões semânticos e `aria-current`.
- Labels em todos os campos de entrada; diálogo com título e fechamento por Escape.
- Foco visível e respeito a `prefers-reduced-motion`.
- Menu lateral recolhível em telas pequenas.
- Conteúdo remoto inserido via `textContent`, sem interpretação de HTML.

## Verificações realizadas

- Navegação entre as seis áreas, busca por trechos, filtro de domínio e abertura de arquivos reais.
- Filtro de atividade e preparação de uma integração sem envio automático.
- Resposta real do Hermes pelo novo chat.
- Inspeção visual em desktop de 1440 px e celular de 390 px, sem rolagem horizontal nas telas verificadas.
- Testes de leitura de materiais e rejeição de caminhos fora da base.
