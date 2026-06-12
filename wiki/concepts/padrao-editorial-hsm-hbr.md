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
Management Review**, **HSM Management**, **IT Forum** e **Revista Exame**.
Outros clientes podem
herdar ou customizar em `config/clients/<id>/client.yaml`.

## Regras de estilo

- Tom analítico, direto, orientado por dados. Sem jargão vazio.
- **Frases curtas**. Parágrafos de 2-3 frases (máximo 5 linhas).
- Dados e estatísticas para sustentar argumentos — nunca afirmar sem
  evidência.
- Evitar superlativos sem evidência ("o melhor", "revolucionário",
  "definitivo").
- Tese contraintuitiva explícita no lead.
- **Português do Brasil com acentuação completa** em todo conteúdo de
  leitura humana. Slugs, URLs, imports, nomes de arquivo e variáveis seguem
  ASCII quando necessário.
- **Didática aplicada**: cada parágrafo deve entregar uma distinção, decisão,
  exemplo, alerta ou passo de ação útil para um adulto em contexto
  profissional.
- **Storytelling funcional**: use cenas curtas, tensão de decisão, caso real
  ou micro-história apenas quando isso ajuda o aluno a entender o mecanismo.
- **Metáforas inteligentes**: analogias devem aproximar o conceito de uma
  experiência profissional conhecida e retornar ao conceito técnico; metáfora
  decorativa ou "bonita" sem função é proibida.
- **Tom profissional quente**: firme, humano e próximo, sem informalidade
  solta e sem frieza burocrática.
- **Clareza jornalística**: introduções sem floreios; o primeiro parágrafo
  entrega a tese e o valor prático da leitura.
- **Tradução executiva**: temas tecnológicos viram impacto operacional, ROI,
  governança, risco e trade-off de alocação.
- **Decisão sob estresse**: priorizar escolhas difíceis de liderança, não
  listas confortáveis de boas intenções.

## Perfil do leitor executivo

O leitor default é um tomador de decisão experiente: CEO, CIO, CMO, fundador,
conselheiro ou líder funcional sênior. A escrita presume repertório executivo.
Não defina jargões básicos de mercado; use o espaço para revelar mecanismos,
trade-offs e critérios de decisão.

Aplicação andragógica específica:

- **WIIFM no primeiro parágrafo**: explicitar o retorno prático sobre o tempo
  de leitura.
- **Experiência prévia**: conectar ideias a dores organizacionais reais que o
  leitor provavelmente já viveu.
- **Autonomia**: fornecer frameworks e perguntas, não ordens professorais.
- **Autorreflexão**: distribuir 2-3 perguntas executivas ao longo do módulo,
  ligadas a maturidade institucional, governança, ROI, risco ou alocação de
  recursos.

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
- Todo parágrafo de corpo deve ser justificado. No React/Tailwind do repo,
  isso é `className="text-justify"`; em export HTML/PDF/e-mail sem Tailwind,
  o artefato deve emitir `<p align="justify">`.

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
