---
name: geracao-por-aula-e-insumo-correto
description: "Por que os cursos saíam truncados e confusos: a revisão nunca via o curso, o writer recebia 3.000 caracteres de pesquisa e um módulo inteiro por chamada; a unidade virou a aula e cada etapa recebe o rascunho."
metadata:
  type: mistake
  created: 2026-09-02
---

O pipeline escreve, analisa, classifica e revisa UMA AULA por vez, e cada etapa recebe o
rascunho, nunca a saída da etapa anterior. O writer recebe a pesquisa inteira (até
`DRAFT_RESEARCH_CONTEXT_CHARS`, 40 mil caracteres) e os tetos da aula como variáveis lidas de
`config/lexicos.json`; o prompt não carrega número de régua. A revisão devolve o texto inteiro
da aula, e uma resposta com menos de `REVIEW_MIN_RATIO` (60%) das palavras recebidas é
comentário: o rascunho fica e o resultado ganha aviso. O conversor só prefere a revisão ao
rascunho quando ela tem ao menos 60% das palavras dele. O parser trata `# Aula i.j:` como
unidade, e o gate mede aula a aula.

Relacionadas: [[diretriz-editorial-v3-narrativa-sem-cota]], [[ADR-002-sync-automatico-courses-wiki]].

---

## Linha do tempo (append-only, ordem reversa)

- **2026-09-02 (noite)** — [waves 1, 2 e 5] Orçamento por curso e sessão com motivo, procedência do modelo por etapa, quality gate ao fim do pipeline e fechamento da trilha (`# Trilha n:`) com a camada GEO cobrada sobre o curso inteiro. Origem: teste ponta a ponta do mesmo dia (curso real de 6 aulas, US$ 2,14; três provedores em fallback; revisão cortada pelo teto diário; camada GEO reprovando toda aula do molde novo).

- **2026-09-02** — [criação] Auditoria dos três repositórios de escrita (curso-factory,
  Escrita-Empresarial, escrita-empreendedor) por texto truncado, confuso e subdividido. Medido
  em 12 drafts de `output/drafts/`: (1) as etapas eram encadeadas pela saída da anterior, então
  a classificação recebia o JSON da análise e a revisão recebia o JSON da classificação; o
  revisor nunca via o curso e devolvia de 80 a 1.300 palavras de relatório ("aguardando
  conteúdo completo dos módulos") para rascunhos de 1.400 a 17.400 palavras, e o conversor
  preferia essa "revisão" por ser "mais polida"; (2) `_draft_modules_iterative` pedia um módulo
  inteiro (4 a 6 aulas de 1.200 a 2.400 palavras, ou 24 mil tokens em português) numa chamada
  com teto de 16.384 tokens e entregava só `research_context[:3000]`; (3) o prompt de redação
  tinha 41 KB e 507 linhas com um checklist final que contradizia o molde da aula ("3
  exercícios", "3 apoios visuais por módulo", "5 estatísticas", "answer capsule após cada H2",
  "H2 > H3 > H4"), e o revisor recolocava o que o molde cortava; os módulos saíam com 6 H2 e até
  16 H3 em 1.400 palavras. Correção no PR desta data: geração por aula, insumo correto, revisão
  por aula com trava, prompts enxutos de 120 a 160 linhas com variáveis, parser por aula,
  guarda no conversor, `content_checker` sem pisos de enfeite. Pareceres de um designer
  instrucional (Coursera, Udemy, Duolingo, Mayer) e a pesquisa de plataformas sustentam a aula
  de 900 a 1.800 palavras com três H2 e um exercício.
