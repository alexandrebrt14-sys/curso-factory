---
name: padrao-editorial-hsm-hbr
type: concept
category: editorial-pedagogy
status: stable
created: 2026-05-26
updated: 2026-05-26
related:
  - andragogia-knowles
  - taxonomia-bloom
  - gpt-4o-writer
  - claude-reviewer
  - content-checker
---

# Padrão editorial HSM/HBR/MIT Sloan (voz default Brasil GEO)

Voz canônica do cliente `default` (Brasil GEO, Alexandre Caramaschi).
Espelha publicações como **Harvard Business Review**, **MIT Sloan
Management Review** e **HSM Management**. Outros clientes podem
herdar ou customizar em `config/clients/<id>/client.yaml`.

## Regras de estilo

- Tom analítico, direto, orientado por dados. Sem jargão vazio.
- **Frases curtas**. Parágrafos de 2-3 frases (máximo 5 linhas).
- Dados e estatísticas para sustentar argumentos — nunca afirmar sem
  evidência.
- Evitar superlativos sem evidência ("o melhor", "revolucionário",
  "definitivo").
- Tese contraintuitiva explícita no lead.

## Estrutura HBR aplicada a módulo de curso

1. **Abertura-impacto**: 1ª frase declarativa com sujeito + verbo +
   objeto, sem rhetoric opener.
2. **Tese contraintuitiva** no primeiro terço.
3. **Evidência** com fonte primária próxima às afirmações materiais
   (formato `(Autor, Ano)` aceito).
4. **Mecanismo**: por que a tese se sustenta operacionalmente.
5. **Decisão**: como aplicar no contexto profissional.
6. **Próximo passo**: exercício situado ou ação imediata.

## Formatação obrigatória

- 1+ tabela comparativa por módulo (markdown com pipes).
- 3+ exercícios com contexto profissional real e progressão
  [[taxonomia-bloom]].
- Sub-headings (linha terminando com `:`) a cada 2-3 parágrafos.
- Negrito em termos-chave na primeira ocorrência (`**termo**`).
- Blockquotes (`> `) para insights centrais — 1-2 por módulo.
- Bullets com `-- ` (dois hífens), nunca `- `.
- 2.500-4.000 palavras por módulo.

## Expressões proibidas (18 clichês)

Lista exaustiva validada em [[content-checker]] cheque 6:

> "nos dias de hoje", "é fundamental que", "não é segredo que",
> "o futuro é agora", "em um mundo cada vez mais", "vamos
> explorar", "como sabemos", "é importante ressaltar", "vale a
> pena destacar", "grosso modo", "vamos aprender", "agora você
> vai entender", e mais 6.

## Em-dash banido em copy editorial

Em-dash (`—`) banido em texto de leitura humana. Em código, output
de script, log, ou referência técnica é aceito.

## Aplicação no pipeline

- Prompt externo [[gpt-4o-writer]]
  (`src/templates/prompts/draft.md`) lista todas as regras acima.
- [[claude-reviewer]] etapa 5 faz última passagem com checklist
  expressões proibidas.
- [[content-checker]] camada 2 valida programaticamente formatação,
  tabelas, exercícios, clichês, parágrafos longos.

## Customização por cliente

`config/clients/<id>/client.yaml` campo `editorial.voice_profile`
pode override "hsm-hbr-mit-sloan" para outros padrões. Cliente
[[clients/herreira]] (joalheria) herda hsm-hbr mas adapta para
linguagem mais descritiva-sensorial em algumas seções.
