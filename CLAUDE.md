# curso-factory — Instruções Claude Code

## Atualização editorial de 10/09/2026

A fonte vigente é `escrita-empreendedor` 1.8.0 (espelho ressincronizado em 27/09/2026), declarada em `DIRETRIZ_EDITORIAL.md`.
Leia `docs/ESCRITA_SEO_GEO.md` e `AGENTS.md` para aplicar fidelidade de trechos, pesquisa
orientada à decisão e preservação de fatos no pipeline em português. Esta orientação vence
os resumos históricos de v4 sobre abertura, número como prova e métricas de estilo.

## Memória de decisões do projeto

Decisões de arquitetura, erros-a-evitar e insights vivem em `wiki/decisions/` como
arquivos `.md` versionados — a fonte da verdade, com índice navegável em
[`wiki/decisions/INDEX.md`](wiki/decisions/INDEX.md) (inclui os ADRs existentes).
Formato: **Verdade Compilada** (topo, reescrito quando o entendimento muda) + **Linha
do Tempo** (append-only). Guia e template em `wiki/decisions/README.md`.

Três disciplinas ao registrar conhecimento:
1. **Dedup antes de gravar** — se a decisão já existe, atualize-a; não duplique.
2. **Cross-link na escrita** — toda decisão nova linka 2-3 relacionadas via `[[nome]]`.
3. **Candidate-gate** — o hook de fim de sessão rascunha em `candidates/` (não
   versionado, não autoritativo); promova destilando numa decisão real.

Orçamento de contexto: cada linha do `INDEX.md` < ~200 caracteres; o detalhe mora no
arquivo da decisão, nunca no índice. O histórico datado de abril/2026 foi movido para
`wiki/decisions/CLAUDE-CHANGELOG.md`.

## REGRA #0 — IDIOMA

Todo conteúdo gerado pelo orquestrador em PT-BR com acentuação completa. Exceção: código, commits, docstrings, identifiers técnicos.


## REGRA #1 — Contexto GEO/SEO 2026 antes de decidir

Em toda decisão de arquitetura do orquestrador, escolha de prompt por agente, quality gate,
FinOps por LLM ou desenho de pipeline para segmento novo, leia primeiro o índice
[`docs/BASE_DE_CONHECIMENTO_GEO.md`](docs/BASE_DE_CONHECIMENTO_GEO.md): a espinha didática
(`docs/GEO_50_CONCEITOS_CANONICAL.md`), as bases de conhecimento V1 a V3, a rubrica de
redação (`docs/GEO_REDACAO_CHECKLIST_2026.md`, cobrada sobre o curso inteiro, nunca por
aula) e as waves de pesquisa de maio a setembro de 2026, cada uma com a seção de aplicação
neste repositório.

Citar `§X.Y` dos KBs/INCREMENT/WAVE ao tomar decisões. **Em conflito de fato datado, prevalece a wave mais recente nos itens explicitamente marcados como correção: Setembro (§8 — spam update terminou 21-ago, AI Mode exige modelo declarado, regra de parada substitui N fixo, Reddit é insumo invisível, `search_queries` sumiu, Sonar morre 27-set, feed antes de página) > Agosto (§8 — `llms.txt` rebaixado, AI Mode 1 bi MAU × 0,13% visitas não se compõem, Reddit fora dos exemplos, core update de agosto inexistente, API xAI) > Julho (§7 — Adobe×Semrush, conversão por vertical) > Junho 19 (§7 — schema, llms.txt, "GEO = camada técnica separada") > 15B (§8); fora desses itens, o corpus anterior segue valendo.** Atualizar trimestralmente (próxima: agosto/2026).

## Histórico (changelog)

Mudanças aplicadas datadas de abril/2026 — refactors (multi-tenant, 5 waves), base de conhecimento GEO/AEO e auditorias (Waves A-D) — foram movidas para [`wiki/decisions/CLAUDE-CHANGELOG.md`](wiki/decisions/CLAUDE-CHANGELOG.md), mantendo este arquivo enxuto no contexto. As **regras vivas** seguem abaixo.

## Regras Fundamentais

### Frontend — layout, UX, animação, contraste (LEIA ANTES de mexer em template visual)
Playbook canônico: **`docs/FRONTEND_PLAYBOOK.md`** — como este repo é um GERADOR, corrija sempre no TEMPLATE para que todo curso gerado herde a prática. Cobre: layout/UX/navegabilidade de conteúdo longo, régua de stacks premium 2026, **REGRA inviolável de contraste WCAG AA nos dois temas** (dark/light; spans inline; `pre` com fundo escuro fixo), **parágrafos justificados** (`text-justify`), **animação à prova de falha** (nunca esconder dependendo de JS; CSS `fill:both`; `prefers-reduced-motion`), **auditoria da SAÍDA renderizada** (dois temas, transições mortas, cache-bust, iterar até zerar) e catálogo de **erros frequentes** (inclui acentuação em geração longa). Defeito no template multiplica por todos os cursos — pegue cedo.

### Peso visual do curso gerado (LEIA ANTES de gerar curso)
Doutrina canônica: **`docs/DOUTRINA_VISUAL_CURSOS.md`**. Desde 27/08/2026 a obrigação editorial é o TETO de apoios visuais por aula (`tetos.D.figuras_max` em `config/lexicos.json`), e só quando a peça substitui texto; o piso por módulo e o teto de 1.200 caracteres por parágrafo seguem como rede do motor de renderização da landing (`config/quality_rules.yaml > validation.visual_density`), não como régua de escrita. **O que mudou no gerador:** o contrato de geração passou a emitir seis tipos de bloco visual (`figure`, `dataTable`, `comparison`, `statGrid`, `stepGuide`, `timeline`), declarados sempre nos mesmos quatro lugares (`src/models.py`, `src/schemas/course.schema.json`, `src/templates/page.tsx.j2` e o filtro `js_json` de `src/generators/tsx_generator.py`); o parser promove sozinho tabela, lista numerada de passos e imagem com legenda; e a camada `visual_density` do `config/quality_rules.yaml` deixou de ser declarativa e é cobrada dentro de `TsxGenerator.render_page`. Curso que nasce como coluna de texto **não chega a virar arquivo**: a cobrança levanta `VisualDensityError` antes da renderização. Curso legado atravessa com `cobrar_peso_visual=False`, com os achados só no log.

### Idioma
- TODO texto de curso DEVE ser em Português do Brasil com acentuação completa
- NUNCA: "nao", "voce", "producao" — SEMPRE: "não", "você", "produção"
- Exceção: código, variáveis, commits, nomes de arquivo em inglês

### Nomenclatura (cliente `default`)
- Credencial oficial: "Alexandre Caramaschi, CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil" (com vírgula: travessão em texto de leitura reprova)
- NUNCA usar: "Especialista #1", "GEO Brasil", "Source Rank"
- URL do autor: https://alexandrecaramaschi.com; domínios válidos: alexandrecaramaschi.com, brasilgeo.ai
- NUNCA referenciar: geobrasil.com.br, sourcerank.ai; nenhuma credencial além da oficial

**Importante:** essas regras valem para o cliente `default`. Ao trabalhar com outro cliente (`--client <id>`), as regras de naming vêm do `config/clients/<id>/client.yaml` (seções `author:` e `voice_guard.canonical:`), e o voice guard bloqueia o que as violar. Jamais hardcode credencial Alexandre no código — tudo passa pelo `ClientContext`.

### Sem Emojis
- Proibido emojis em qualquer conteúdo de curso ou documentação


## Arquitetura do Pipeline

5 LLMs com papéis fixos — NÃO interpretar como sub-agentes do Claude Code:
1. Perplexity (sonar-deep-research) → pesquisa, fundamentação acadêmica e análise competitiva
2. GPT-5.5 → planeja as aulas de cada módulo e redige UMA aula por chamada, em linguagem simples (fonte de estilo escrita-empreendedor), com a pesquisa inteira
3. Gemini (3.1-pro-preview) → análise pedagógica do rascunho inteiro, aula a aula, em 7 dimensões
4. Gemini (3.7-flash) → classificação, tags e metadados, a partir do rascunho (a Groq saiu do parque do geo-orchestrator em 2026-07-08)
5. Claude (sonnet-5) → revisão final UMA aula por chamada, devolvendo o texto inteiro; revisão que encolhe o texto é descartada e o rascunho fica ($5 max/curso)

O cliente LLM (`src/llm_client.py`) classifica toda falha (cota, chave, modelo, rate limit, transitório, formato) e reage por classe: cota e modelo morto tiram o provedor da sessão sem retry; o fallback é a cadeia `fallback_chain` de `config/providers.yaml`; HTTP 200 sem texto não abre circuito. Detalhe em `wiki/decisions/cliente-llm-resiliente.md`. Os modelos seguem o `catalog/model_catalog.yaml` do geo-orchestrator (v4.6, task_routing: research, writing, analysis, classification, review); mudar modelo é mudar `config/providers.yaml` e o agente, nunca hardcode em prompt. Cada etapa recebe o RASCUNHO (não a saída da etapa anterior). Até 02/09/2026 a revisão recebia o JSON da classificação e devolvia um relatório no lugar do curso; ver `wiki/decisions/geracao-por-aula-e-insumo-correto.md`.

### Prompts Externos (IMPORTANTE)
- Os prompts ficam em `src/templates/prompts/pt-br/*.md` (en e es têm pasta própria, mas nenhum
  agente de produção troca de idioma hoje); a raiz guarda só o `tutor.md`
- Os agentes em `src/agents/` carregam automaticamente o prompt externo via `base.py`
- Para alterar o comportamento de um agente, edite o arquivo .md correspondente
- Se o arquivo .md não existir, o agente usa o TEMPLATE inline como fallback
- NUNCA duplicar instruções entre o prompt externo e o template inline


## Padrão Editorial — Regras de Qualidade

Fonte normativa: [`DIRETRIZ_EDITORIAL.md`](DIRETRIZ_EDITORIAL.md) (v3, 11/08/2026) e o anexo [`GUIA_ESCRITA_HUMANIZADA.md`](GUIA_ESCRITA_HUMANIZADA.md). Em conflito, a diretriz prevalece sobre o resumo desta seção.

### Registro: linguagem simples, com rigor de evidência
- O registro da aula é o da fonte de estilo: linguagem simples e jornalismo de serviço para o
  dono de pequeno negócio, no celular. HBR, MIT Sloan e HSM valem só como referência de rigor
  de evidência e de "resposta primeiro", nunca como registro (C1 de 27/09/2026)
- Tom direto, orientado por dados, sem jargão vazio
- Uma ideia central por parágrafo, desenvolvida até a ideia terminar. O ritmo vem do conteúdo: período longo para raciocínio com causa e ressalva, frase curta quando houver o que enfatizar. PROIBIDA qualquer cota de ritmo (frase curta por parágrafo, alternância programada, teto fixo de linhas), que produz staccato de manchete
- Dados e estatísticas para sustentar argumentos, nunca afirmar sem evidência
- Evitar superlativos sem evidência ("o melhor", "revolucionário")
- Abertura direta (R1 e fonte §2 regra 2): subtítulo de uma frase e parágrafos que dizem o problema do leitor em segunda pessoa, o que custa não resolver e o que muda; sem cena, sem hora do dia, sem personagem na abertura
- A aula é guia aplicável (27/09/2026): ensina a fazer, com passos, verificação, erro comum, decisão "se isto, faça aquilo" e critério de pronto. O exemplo é curto e percorre os passos; personagem é opcional e o fecho não volta a ele

### Andragogia (6 Princípios de Knowles), cobrada como aviso desde 02/09/2026
1. Necessidade de saber — POR QUE antes do COMO
2. Autoconceito — profissional autônomo, nunca condescendente
3. Experiência prévia — conectar com vivências profissionais
4. Prontidão — aplicabilidade imediata no trabalho
5. Orientação a problemas — problemas reais, não taxonomias
6. Motivação intrínseca — crescimento profissional e domínio

### Taxonomia de Bloom nos Objetivos
- ACEITOS (nível 3-6): analisar, comparar, diagnosticar, avaliar, justificar, criar, projetar, aplicar, implementar
- PROIBIDOS (nível 1-2): entender, conhecer, saber, compreender, lembrar, memorizar, listar, descrever, identificar

### Abertura e distração (R1 a R9, 08/09/2026) — LEIA ANTES de mexer em prompt, template ou gate
Pedido do dono: o topo carregado dispersa o leitor e o card no meio compete com a leitura.
Regras completas e onde cada uma morde: `DIRETRIZ_EDITORIAL.md`, seção "Abertura e distração",
e `wiki/decisions/abertura-direta-sem-distracao-20260908.md`. Em resumo:
- R1 toda unidade abre com H1, subtítulo em UMA frase e parágrafos; nada antes nem entre eles
- R2 sem botão antes do corpo; R3 um único percurso; R4 uma descrição só
- R5 sem "mockup no seu negócio"; R6 sem exercício "faça agora" (a aula é leitura)
- R7 fontes só no rodapé, em `0.8rem`, nome e link; R8 sem card "checkpoint"; R9 sem "requer
  verificação" visível e sem menção à LGPD
- Garantia em três níveis: prompts (`draft.md`, `review.md`, `analyze.md`, nos três idiomas),
  gerador (`page.tsx.j2` sem rótulo pré-H1, sem barra de estatísticas, sem índice lateral, sem
  card "o que você vai aprender", sem `case checkpoint`, com bloco "Fontes" no rodapé; parser
  descarta `> CHECKPOINT:` e hasteia `## Fontes` para `CourseDefinition.fontes`) e gate
  (`src/validators/abertura_checker.py`: categoria `abertura` no `content_checker`, erro
  bloqueante; `AberturaError` em `TsxGenerator.render_page`). Teste:
  `tests/test_abertura_sem_distracao.py`

### Didática: explicar em vez de detalhar (22/09/2026) — LEIA antes de mexer em prompt ou gate
Pedido do dono: a régua de forma aprovava aula que o aluno abandona. Régua de tamanho é teto,
nunca alvo; a aula troca minúcia por explicação sem inchar. Regras, medição e nomes de achado
em `docs/ESPECIFICACAO_DIDATICA_20260922.md` e na decisão
`wiki/decisions/didatica-explicar-em-vez-de-detalhar-20260922.md`. Em resumo:
- Glosa com analogia na primeira aparição de todo termo (molde "spring: jeito de animar que
  imita uma mola"); frases ligadas: o que é, por que importa para o negócio, o que fazer
- Parágrafos vizinhos não abrem com a mesma palavra; a maioria não abre por "O"/"A" mais sujeito
- Título é promessa com verbo (sem dois-pontos, sem substantivo empilhado); o redator propõe
  `TÍTULO:` e o orquestrador troca. Subtítulo é UMA promessa, sem "Você sai" nem vírgulas em série
- Fecho com imperativo e critério de acerto; ponte de entrada em uma linha quando há aula anterior
- Ficha, dica, caso e legenda no registro da aula ("você", glosa, exemplo, conferência que diz o
  que aparece na tela); mais de seis fichas seguidas pedem frase de ligação
- Gate: `src/validators/didatica_checker.py`, categoria `didatica` (quase tudo aviso; erro só
  série de 3 aberturas iguais, fórmula em 3 subtítulos e conferência de fuga). Números em
  `config/quality_rules.yaml > validation.didatica`

### Molde da aula (unidade de geração desde 02/09/2026)
- A unidade que o pipeline escreve, revisa e mede é a AULA, uma por chamada de LLM
  (`Orchestrator._draft_lesson`), com a pesquisa inteira no prompt
- Os números da aula (palavras, H2, H3 por H2, figuras, parágrafo) vêm de `config/lexicos.json`,
  espelho da fonte de estilo `escrita-empreendedor`, e entram no prompt como variáveis
  (`{palavras_alvo_min}`, `{figuras_max}`...). NUNCA repita número de régua em prompt ou doc
- Abertura na ordem R1: subtítulo em uma frase (vira `description` do step) e dois ou três
  parágrafos diretos ao ponto; 2 a 4 H2, promessas com verbo (o normal: um para o porquê, um
  ou dois para o como fazer); H3 só em H2 longo; nada de H4 nem subtítulo por linha terminada
  em dois-pontos
- O corpo segue o esqueleto de aula-guia de `validation.guia_aplicavel.esqueleto` (resposta,
  porquê com fonte, pré-requisitos, passos, decisões, exemplo aplicado, critério de pronto,
  fontes), que chega aos prompts por `{bloco_molde_da_aula}`; parte sem conteúdo não entra
- NENHUM exercício por aula desde 08/09/2026 (R6). O passo a passo do procedimento é conteúdo
  (lista numerada, sem rótulo, com a verificação em prosa dentro do passo), nunca bloco "faça
  agora". `min_exercises_per_lesson: 0` no YAML
- Apoio visual é TETO (até `figuras_max` por aula), só quando substitui texto. Sem piso de
  tabela, blockquote, negrito ou figura
- Objetivos, pré-requisitos, glossário, FAQ e fontes datadas vivem no nível da trilha: o
  pipeline os escreve UMA vez por módulo, depois da última aula, como `# Trilha n: título`
  (`Orchestrator._close_trail`, prompt `trail.md`); a revisão pula essa unidade e o gate não
  aplica a ela a régua da aula. A camada GEO (fontes, estatísticas, citação, cápsula) é cobrada
  sobre o curso inteiro, nunca por aula
- Bullets com `-- ` (dois hífens), NUNCA `- ` (um hífen), no conteúdo renderizado pelo `FormattedText`

### Padrão de Layout (FormattedText — UX Microsoft Learn + Salesforce Trailhead)
O template `page.tsx.j2` inclui um componente `FormattedText` que renderiza:
- `**bold**` → `<strong>` com font-semibold
- Linha terminando com `:` → `<h4>` sub-heading com border-bottom
- `-- item` → bullet list com dot azul (accent color)
- `1. item` → ordered list com número azul
- `| col | col |` → `<table>` com header uppercase e zebra striping
- `> texto` → blockquote com borda lateral azul
- Parágrafos → text-justify com leading-[1.75]
- Warning/tip → text-justify aplicado (`checkpoint` saiu em 08/09/2026, R8)

### REGRA — Parágrafos SEMPRE justificados (invariável)
Todo conteúdo de texto gerado por este repositório (drafts → páginas) deve sair com
**parágrafos justificados** — o equivalente canônico do estilo `<p align="justify">`.
- No stack React/Tailwind deste repo, isso é materializado por `className="text-justify"`
  (NÃO usar o atributo HTML deprecado `align="justify"` em JSX/TSX).
- Todo `<p>` de corpo emitido pelo template deve conter `text-justify`. O parágrafo de corpo
  do `FormattedText` (`src/templates/page.tsx.j2`, ~linha 483) já cumpre — NUNCA remover esse
  utilitário ao editar o template, e replicá-lo em qualquer novo `<p>` de texto corrido.
- Vale para qualquer destino: se um curso for exportado para HTML cru / PDF / e-mail (onde o
  Tailwind não roda), emitir o atributo literal `<p align="justify">` no artefato exportado.
- Sub-agentes que escrevem páginas/drafts: carimbar esta regra no prompt junto ao bloco de
  acentuação (a justificação é invariante de saída, não opcional).

### Expressões proibidas e vocabulário de uso limitado
A lista viva é a união de `config/lexicos.json` (fonte de estilo) com
`config/quality_rules.yaml > validation.forbidden_expressions`; não repita a lista aqui.
Quatro famílias têm limite por aula ("travar", "canônico", "régua", "honesto" e variações):
`validation.palavras_de_uso_exagerado`, que também vale para documentação e commits.

### Boas práticas de 27/09/2026 (LEIA antes de mexer em prompt, gate ou client.yaml)
Decisão: `wiki/decisions/boas-praticas-de-escrita-20260927.md`. Cada regra tem configuração,
validador e teste; o prompt recebe o texto da mesma configuração por um `{bloco_*}`:
- a aula não narra a própria apuração (`validation.apuracao_narrada`, erro de bastidor)
- crosslinks por aula, opt-in no `client.yaml` (`crosslinks`), destino e capítulo conferidos
  contra o catálogo gerado por `scripts/gerar_catalogo_crosslinks.py`
- peso visual declarado por cliente ou curso (`visual`), sem mexer no espelho
- tamanho e ordem do curso (`validation.planejamento`): primeiras aulas curtas e práticas,
  teoria densa só da metade em diante, tese na primeira metade da aula
- tabela de proveniência como arquivo de trabalho (`python cli.py proveniencia`,
  `etapas["proveniencia"]`); o formato de retorno do pipeline não muda
- os números citados nos prompts saem da configuração (`src/validators/numeros_dos_prompts.py`);
  nunca escreva número de teto à mão num prompt

### Aula-guia aplicável e fonte recente (27/09/2026) (LEIA antes de mexer em prompt ou gate)
Pedido do dono: a aula vira guia de como fazer, a história só entra quando carrega o
procedimento e todo conceito se apoia em fonte recente e datada. Diagnóstico em
`docs/DIAGNOSTICO_GUIA_APLICAVEL_20260927.md`; decisão em
`wiki/decisions/guia-aplicavel-e-fonte-recente-20260927.md`. Cada regra liga no `client.yaml`
(default ligado, `_template` desligado) e nasce como aviso:
- completude do como fazer (`guia_aplicavel`; pisos por tipo de aula e marcadores em
  `validation.guia_aplicavel`; `src/validators/guia_aplicavel_checker.py`)
- orçamento de narrativa (`narrativa.parcela_max`; marcadores em
  `validation.orcamento_narrativa`; `src/validators/narrativa_checker.py`, que conta marcas de
  superfície e não entende se o exemplo carrega um passo)
- fonte recente (`fontes_recentes`, também por curso em `courses.yaml`; formatos de data em
  `validation.fontes_recentes`; `src/validators/fontes_recentes_checker.py`, com a data de
  referência sempre injetada; `python cli.py fontes-recentes`). A tabela de proveniência ganhou
  a coluna "Data de publicação"


## Quality Gate — 5 Camadas de Validação

### Camada 1: Acentuação (accent_checker.py)
- 300+ mapeamentos de palavras sem acento → forma correta
- `check_accents()`: detecta erros com linha, palavra e contexto
- `fix_accents()`: corrige automaticamente, preservando URLs/código/variáveis
- Rastreamento de blocos de código (```) para não alterar código

### Camada 2: Conteúdo (content_checker.py)
- Roda ao fim do pipeline, aula a aula, e grava `PipelineResult.gate` e a etapa `gate_report`
  (reprovação vira aviso, não falha); `python cli.py validate` continua servindo para rascunhos
- Medida por AULA quando o texto traz `# Aula i.j:` (`QualityGate._check_content_por_unidade`);
  texto sem esse cabeçalho é medido inteiro na unidade pedida (`unidade="modulo"` multiplica a
  régua da aula por 4 a 6)
- Extensão, H2, H3 por H2, teto de apoios visuais e faixa de parágrafo: números de `tetos.D` em
  `config/lexicos.json`
- Nenhum exercício por aula (R6; o bloco reprova); hierarquia de títulos sem pulos
- Abertura e distração (R1, R3, R5 a R9) na categoria `abertura`, erro bloqueante, aula e trilha
- Clichês proibidos: união de `lexicos.json`, `quality_rules.yaml` e fallback do módulo
- Verbos de Bloom só quando existe seção de objetivos; andragogia só avisa
- Emojis proibidos; teto de marcadores `[FALTA EVIDÊNCIA]`; percentual sem fonte avisa
- Desde 27/09/2026: `vocabulario` (palavras de uso limitado), `crosslinks` (opt-in do cliente),
  `peso visual` (quando declarado) e, sobre o curso inteiro, `planejamento` e a sequência de
  crosslinks (`QualityGate.check_curso`)
- Também desde 27/09/2026, quando o cliente liga: `guia aplicável`, `narrativa` e `fontes
  recentes` (`QualityGate.check_guia`, aula a aula; na trilha, só as fontes)

### Camada 3: Links (link_checker.py)
- Acentos em URLs = ERRO CRÍTICO (incidente 2026-03-27: 55 hrefs corrompidos)
- Verificação de links internos

### Camada 4: HTML (html_validator.py)
- Fechamento de tags, elementos obrigatórios, acessibilidade

### Camada 5: FinOps (cost_tracker.py)
- Budget guard: $5 max Claude e $10 max total por curso, mas o teto da SESSÃO
  (`SESSION_BUDGET_TOTAL`, $5 em `src/config.py`) é menor e corta antes; ver
  `docs/AUDITORIA_PIPELINE_20260927.md`
- Cache em disco: SHA-256, TTL de `CACHE_TTL_SECONDS` (3.600 s por padrão, não 24 h)

### Auto-correção de Acentos
- O quality gate (`auto_fix=True` por padrão) corrige acentos automaticamente; o gate que o
  orquestrador roda ao fim do pipeline usa `auto_fix=False` e só relata
- O texto corrigido é retornado em `GateResult.texto_corrigido`
- Correções residuais são detectadas e reportadas


## Regras Anti-Retrabalho

### NUNCA usar heredocs para conteúdo grande
- Heredocs >50 linhas QUEBRAM no shell
- SEMPRE usar templates Jinja2 em src/templates/
- SEMPRE gerar arquivos via Python (Write tool ou script)

### NUNCA usar scripts de substituição por regex
- Scripts que leem template e substituem trechos são FRÁGEIS
- SEMPRE gerar o arquivo completo de uma vez (geração atômica)

### Validação ANTES de deploy
- Rodar quality_gate.py com todas as 5 camadas
- Se qualquer camada bloqueante falhar, NÃO fazer deploy
- Auto-correção de acentos é aplicada automaticamente

### FinOps
- Budget guard ativo: $5 max Claude, $10 max total por curso, $5 por sessão (o menor vence)
- Cache obrigatório — nunca reprocessar conteúdo já aprovado
- Verificar custo antes de executar pipeline completo
- API keys: fonte de verdade em geo-orchestrator/.env


## Estrutura de Arquivos

- config/courses.yaml — definição dos cursos
- config/quality_rules.yaml — regras de qualidade (inclui a camada `visual_density`, cobrada em runtime)
- docs/DOUTRINA_VISUAL_CURSOS.md — doutrina de peso visual: tetos, os seis tipos de bloco e os quatro lugares que mudam juntos
- src/agents/ — um agente por LLM (carrega prompt de templates/prompts/)
- src/templates/prompts/ — prompts externos de alta densidade (.md)
- src/templates/ — templates Jinja2 para TSX (NUNCA heredoc)
- src/validators/ — validadores do gate (acentos, conteúdo, abertura, didática, vocabulário,
  crosslinks, peso visual, planejamento, proveniência, HTML, links, voice guard, quality gate)
- src/generators/ — geradores de TSX (Jinja2, schema builder, metadata sync, build validator)
- src/schemas/ — JSON Schema para CourseDefinition
- output/drafts/ — rascunhos
- output/approved/ — aprovados
- output/deployed/ — em produção
- tests/ — testes unitários dos geradores


## Comandos CLI

```bash
python cli.py clients                                # Lista clientes em config/clients/
python cli.py create "Nome do Curso"                 # Cria curso sob cliente default
python cli.py create "Nome do Curso" --client acme   # Cria sob cliente específico
python cli.py validate output/drafts/                # Valida rascunhos
python cli.py cost-report                            # Relatório de custos
python cli.py batch config/courses.yaml              # Criação em lote
python cli.py batch config/courses.yaml --client X   # Lote sob cliente X
python cli.py proveniencia aula.md --saida tab.md    # Frases com número, data, versão ou produto
```


## Workflow de Criação de Curso

1. Definir curso em courses.yaml (nome, nível, módulos, descrição)
2. Executar `python cli.py create "Nome"`
3. Pipeline automático: Research → Draft → Analyze → Classify → Review
4. Quality Gate automático (5 camadas: acentos + conteúdo + links + HTML + FinOps)
5. Auto-correção de acentos aplicada
6. O veredito fica em `etapas["gate_report"]`; mover para `output/approved/` é passo manual
7. Deploy manual ou via script


## Padrão editorial obrigatório

Antes de produzir qualquer texto de leitura humana neste repositório (documentação, cursos, páginas, relatórios, descrições de PR, mensagens longas de commit), leia e aplique [`DIRETRIZ_EDITORIAL.md`](DIRETRIZ_EDITORIAL.md) na raiz (ponteiro para a fonte `escrita-empreendedor`) e consulte o anexo prático [`GUIA_ESCRITA_HUMANIZADA.md`](GUIA_ESCRITA_HUMANIZADA.md), com exemplos antes e depois, heurísticas mensuráveis e fontes. Esta é a fonte única do padrão editorial do repositório: os prompts do pipeline (`src/templates/prompts/`) e o resumo da seção "Padrão Editorial" acima se subordinam a ela, e a duplicação de camadas editoriais divergentes foi o que degradou a qualidade entre julho e agosto de 2026 (ver `wiki/decisions/diretriz-editorial-v3-narrativa-sem-cota.md`).

Antes de qualquer regra de evitação vem o piso de substância (diretriz §2.1), porque os gates automáticos deste repo medem forma e nenhum deles mede argumento: texto raso e uniforme passa em todos. Toda peça precisa ter tese identificável, evidência ligada à tese, ganho de informação, critério de decisão explícito onde houver alternativas, arco de leitura e consequência executável para o leitor. Aprovação no gate não é aprovação editorial, e em conflito entre proibição e piso de substância o piso vence.

Antes da primeira frase vem a prova (diretriz §2.2). Levante o material de evidência, e ele define o tamanho da peça: o número de blocos que afirmam resultado é menor ou igual ao número de provas datadas disponíveis hoje. Faltando prova, tente as quatro saídas nesta ordem (pesquisar a origem, reduzir a afirmação ao que se sabe, restringir o uso, segurar a publicação) antes de usar marcador. `[FALTA EVIDÊNCIA: ...]` é lacuna que pesquisa resolve; `[PREENCHER-HUMANO: ...]` é o que só o autor humano tem. Teto de cinco marcadores abertos por documento, agora verificado pelo `content_checker.py`.

Promessa e tensão são escritas antes do esqueleto (§3.1), o esqueleto segue a ordem do gênero (§3.2), o pedido é um só por peça com as quatro peças da fórmula (§3.6), e toda porcentagem dispara quatro conferências na mesma frase: origem, data, método e denominador (§13).

O essencial, em uma passada: escrita de especialista sênior em português do Brasil com acentuação completa e tipografia brasileira (sem title case, numerais à brasileira); conclusão antes da sustentação e cada parágrafo acrescentando uma ideia nova; aula que ensina a fazer, com passos, verificação, decisão condicional e critério de pronto, exemplo curto amarrado aos passos e conceito apoiado em fonte recente e datada, com abertura direta e sem cena (fonte §2 regra 2); ritmo nascido do sentido, com o teste do bloco de dez frases servindo de diagnóstico depois de escrever e nunca de cota durante a escrita; proibido travessão como recurso estilístico; proibidas como padrão as construções que negam para afirmar ("não é X, é Y"), a regra de três mecânica, as conclusões-espelho e a atribuição vaga sem fonte nomeada; conectivos cortados por subtração, sem clichês nem vícios de português de LLM (gerundismo, "endereçar", "suportar", "eventualmente" como eventually); tabela, matriz de decisão e checklist usados sempre que houver comparação, escolha ou passo verificável, e prosa sempre que houver raciocínio encadeado; dado sem fonte e data não entra, e o que só o autor humano sabe vira marcador `[PREENCHER-HUMANO]`, nunca invenção; em superfícies HTML ou PDF, parágrafos com alinhamento justificado (`text-align: justify`); revisão final em três passadas (substância, estrutura, linguagem) com leitura em voz alta.

Sub-agentes que geram copy longa recebem o bloco de `C:/Sandyboxclaude/scripts/prompts/COPY_PROMPT_PREFIX.md` carimbado no prompt. Os documentos completos prevalecem sobre este resumo, e as convenções específicas deste repositório prevalecem sobre convenções genéricas, exceto quando comprometerem segurança ou corretude.
