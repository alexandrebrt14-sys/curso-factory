# Query playbook — wiki/ Karpathy no curso-factory

Receita canônica para responder uma pergunta operacional consultando
o grafo wiki/ antes de pesquisar externamente ou re-ler KB
monolítico. Não é script automático: é prompt de operação para
agente LLM.

## Quando usar

- Pergunta operacional pode ser respondida com conhecimento já
  catalogado.
- Suspeita que o tema já foi pesquisado em wave anterior.
- Antes de disparar nova chamada Perplexity ou spawn de sub-agent.
- Antes de re-ler um dos 7 KBs canônicos em `docs/` (29 KB+ cada).

## Passo a passo

### 1. Buscar no índice

Abrir `wiki/index.md` e procurar termos do pedido em:

- **Concepts** (se a pergunta menciona conceito editorial: andragogia,
  Bloom, padrão HBR, multi-tenant).
- **Entities** (se a pergunta menciona LLM ou validator do pipeline).
- **Clients** (se a pergunta é "qual regra para cliente Y").
- **Courses** (se a pergunta é "já produzimos curso de X?").
- **Queries** (se a pergunta é decisão recorrente já sintetizada).
- **Overview** (se a pergunta é sobre cobertura, gaps, topologia).
- **Sources** (se a pergunta é "o que aquele paper diz sobre Y").
- **Decisions** (se a pergunta é "por que escolhemos X").
- **Backlog** (se o tema está declarado como pendente).

### 2. Buscar cross-references nas páginas encontradas

Cada página wiki tem `related:` no frontmatter e cross-links
`[[slug]]` no corpo. Em geral 2 hops bastam para mapear o
território.

### 3. Decidir se a resposta está no grafo

Três cenários:

- **Resposta completa.** Sintetizar usando 2-5 páginas wiki como
  base. Citar slugs como referência.
- **Resposta parcial.** Cobrir o que está no grafo, sinalizar
  explicitamente o gap, considerar abrir ingest novo.
- **Sem cobertura.** Backlog tem o tema? Promover a ingest. Backlog
  não tem? Adicionar e considerar abrir wave de research.

### 4. Filar a resposta como página nova (se valiosa)

Karpathy K-07: **respostas valiosas viram páginas novas.** Critério
de "valiosa" no curso-factory:

- Resposta exigiu sintetizar 3+ páginas wiki existentes.
- Pergunta provavelmente vai se repetir (decisão recorrente sobre
  Bloom, andragogia, padrão editorial, escolha de cliente).
- Síntese contém claim novo não-explícito nas páginas-fonte.

Se sim, criar página em `wiki/queries/`. Estrutura:

```yaml
---
name: <pergunta-curta-kebab>
type: query
status: stable
created: YYYY-MM-DD
updated: YYYY-MM-DD
asked_count: 1
related: [...]
---

# Query: <pergunta completa>

## Pergunta
## Resposta canônica
## Decisões implementadas
## Anti-padrões observados em produção
## Cross-references
```

Incrementar `asked_count` a cada vez que a query for re-feita. Quando
chegar a 5+, considerar promover a `wiki/concepts/` dedicada.

### 5. Apendar `wiki/log.md`

```
YYYY-MM-DD | query | <agent-id> | <pergunta resumida> | <paginas consultadas ou criadas>
```

### 6. Responder ao usuário

Citar páginas wiki por slug, não só link externo. Permite que ele
abra no editor e itere.

## Exemplos de queries operacionais comuns no curso-factory

Queries recorrentes que valem ter página dedicada em
`wiki/queries/`:

- "Qual nível Bloom usar em objetivo?" → já existe
  `wiki/queries/qual-nivel-bloom-usar-em-objetivo.md`.
- "Quando relaxar regra de parágrafos curtos?" → candidata
  (cliente herreira faz isso, justificada).
- "Quando usar `sonar-deep-research` em vez de `sonar-pro`?" →
  candidata.
- "Como decidir se um draft vira approved sem revisão extra?" →
  candidata.
- "Qual budget Claude alocar para cliente novo?" → candidata.

## Anti-padrões

- Pular o índice e cair direto em busca externa. Custa tempo,
  perde acúmulo, viola Karpathy K-01.
- Filar como página toda resposta. Páginas devem ser densas e
  atômicas; ruído mata o grafo.
- Citar página wiki sem dar slug navegável.
- Responder sem registrar no log se a query foi "operacional
  relevante" (decisão de wave, mudança de prioridade, escolha
  técnica).

## Heurística de qualidade

Boa query operacional respondida via wiki:

1. Tempo total <2 minutos.
2. 0 chamadas externas (Perplexity, WebSearch, re-leitura de KB
   monolítico).
3. Resposta cita 2-4 slugs wiki.
4. Se for valiosa, vira página `wiki/queries/`.
5. Log apêndice registra.
