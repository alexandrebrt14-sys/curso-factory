# CLAUDE-CHANGELOG — curso-factory

Log datado de mudanças aplicadas, extraído do `CLAUDE.md` em 2026-06-15 para manter o arquivo de regras vivas enxuto (princípio "Verdade Compilada + Linha do Tempo": o `CLAUDE.md` guarda o que vale AGORA; este changelog guarda como chegamos aqui).

Append-only, ordem reversa (mais recente no topo). Conteúdo movido verbatim — as **regras vivas** permaneceram no `CLAUDE.md`.

---


## 2026-04-29 — Refactor profundo em 5 waves (base reusável para outros segmentos)

Pivô para tornar o curso-factory base de arquitetura para portais educacionais em **outros segmentos**, sem fork. As waves:

1. **Auditoria** — mapa de bugs (4 subcomandos do CLI quebrados por imports inexistentes), código morto (`unified_finops.py`, `_build_writer_context`), duplicações de prompt e divergências entre CLAUDE.md e código real.
2. **Fundação** — CLI reescrito (`validate`, `cost-report`, `batch`, `cache-clear` agora funcionam; `cmd_cost_report` lê o log real do `CostTracker` em vez da API fictícia que existia antes). `writer.py` e `reviewer.py` adotam `**template_vars` para paridade com os outros 3 agents.
3. **Consolidação** — `unified_finops.py` removido (zero referências). `Cache` plugado no `LLMClient` (cache hit antes de circuit/retry). Defaults "Alexandre Caramaschi" / "Brasil GEO" removidos de `models.py:CourseDefinition` (`""` em vez de hardcode — quem instancia injeta via `ClientContext`). `SchemaBuilder` ganha clamp `max(30, duracao)`. Scripts ad-hoc movidos para `scripts/legacy/`.
4. **Testes** — bateria expandida de **24 → 74 testes**: `test_cli` (11), `test_parsers` (14), `test_converters` (7), `test_cost_cache` (8), `test_validators_smoke` (10). Cobre todos os 8 subcomandos, parser canônico, conversor de drafts, FinOps, accent_checker, quality_gate e voice_guard. Toda chamada `datetime.utcnow()` migrada para `datetime.now(timezone.utc)`.
5. **Docs** — `docs/ARCHITECTURE.md` reescrito como guia portal-agnóstico (camadas, o que é reusável, o que é segmento-específico, gaps conhecidos). Para novo portal: copiar `config/clients/_template/`, preencher YAML, eventualmente ajustar prompts.

**Estado final:** 74/74 pytest verde, 8/8 subcomandos do CLI funcionais, zero código morto detectado, zero default de identidade no model.


## 2026-04-25 — Base de conhecimento GEO/AEO/Agentic Commerce

Foi adicionada uma camada doutrinária permanente em [docs/knowledge/geo-aeo/](docs/knowledge/geo-aeo/) que sintetiza 25+ papers acadêmicos (2025–2026) em 30 instruções operacionais, 7 princípios mestres, 4 checklists e tabela de thresholds quantitativos.

**Quando usar.** Cursos sobre GEO, AEO, marketing por IA, comércio agêntico, MCP/A2A, RAG, knowledge graphs ou qualquer tema correlato devem usar este corpus como fonte primária. Cada agente do pipeline tem responsabilidades específicas:

- **Pesquisa (Perplexity)** → fontes-âncora aceitas em `50-fontes-e-links.md`. Toda afirmação factual deve casar com pelo menos um paper deste catálogo.
- **Redação (GPT-4o)** → princípios de `00-principios-mestres.md`, estrutura TL;DR/BLUF de `31-checklist-reescrita.md`, densidade de entidades 1/100 palavras (Instrução 17).
- **Análise (Gemini)** → verificar os 16 pilares de `30-checklist-auditoria-geo16.md` em cada módulo.
- **Classificação (Groq)** → tags com termos canônicos do `02-glossario.md`.
- **Revisão (Claude)** → varredura final contra `01-anti-patterns.md`.

**Princípio operacional.** Em conflito entre uma diretiva tática e um princípio mestre, **prevalece o princípio mestre**. A tese central: *GEO técnico é necessário, não suficiente. Estrutura validável vence prosa eloquente. Mídia conquistada explica a maior parte da variância de citação. Agent legibility é a nova SEO.*

**Manutenção.** Revisão trimestral. Novos papers entram simultaneamente em `2X-papers-bloco-*.md`, `40-thresholds-quantitativos.md` e `50-fontes-e-links.md`.


## 2026-04-19 — Refactor multi-tenant (Ondas 1-5)

### Mudança estrutural: ClientContext
- **Antes:** credencial Alexandre, domínio `alexandrecaramaschi.com`, padrão HSM/HBR/MIT Sloan e regras do voice guard estavam **hardcoded** em `models.py`, `voice_guard.py`, `pyproject.toml`, etc. Rodar a fábrica para outro cliente exigia fork.
- **Depois:** tudo que varia por cliente vem de `config/clients/<id>/client.yaml`. O framework carrega o YAML em um `ClientContext` (`src/clients/context.py`) e injeta em CourseFactory, Orchestrator, SchemaBuilder, QualityGate e voice_guard_check.
- **Cliente `default`** preserva 100% do comportamento pré-refactor (Brasil GEO). Qualquer `<id>` diferente escreve em `output/clients/<id>/`.
- **CLI:** `python cli.py create "Curso" --client minhaempresa` ou `export CURSO_FACTORY_CLIENT=<id>`.
- **Como listar:** `python cli.py clients`.
- **Playbook completo:** [docs/MULTI-CLIENT.md](docs/MULTI-CLIENT.md).

### Consolidação técnica
- **Parser compartilhado** `src/parsers/markdown_parser.py`: fonte única de `slugify`, `extract_module_blocks`, `parse_module_to_sections`. Antes, `schema_builder.py` e `draft_to_course.py` tinham implementações paralelas divergentes.
- **Providers em YAML** `config/providers.yaml` + `src/providers.py`: pricing, endpoints, default_model e fallback. `llm_client.py` só orquestra — mudança de preço/modelo é edição YAML.
- **Voice Guard no QualityGate**: agora é a 4ª camada bloqueante. Score < `client.voice_guard.min_score` (padrão 70) ou erro crítico → `aprovado=False`.

### Limpeza
- `.gitignore` exclui `output/`, `*.egg-info/`, `.pytest_cache/`, `.mypy_cache/`.
- `tests/fixtures/sample_course.json`: `nivel` corrigido de `intermediario` → `intermediário` (5/5 testes voltaram a verde).
- `src/indexer/course_indexer.py`: removido hardcode `C:/Sandyboxclaude/...`; lê `LANDING_PAGE_DIR` do env ou derive de path relativo.

### Commits da refatoração
- `d3c1077` — refactor: multi-tenancy via ClientContext + limpeza de fundação
- `203f126` — refactor: consolidação técnica (markdown_parser, providers.yaml, voice_guard em QualityGate)

### Regra para trabalhos futuros
Ao tocar em qualquer lógica sensível a autor/domínio/padrão editorial: passe pelo `ClientContext`, **não** hardcode. Se precisar de uma constante que varia por cliente, é campo de YAML.


## 2026-04-09 — Mudanças da auditoria de ecossistema (Wave D)

### NOVO: course_id propagado em cost_tracker (F32)
- **Commit:** `72ee757` — `feat(cost-tracker): propaga course_id em todas chamadas LLM`
- **Antes:** `cost_tracker.track()` sempre recebia `course_id=""`, tornando IMPOSSÍVEL responder "qual curso custou X" no `cost-report` ou aplicar budget guard granular por curso.
- **Depois:** `LLMClient.set_course_context(course_id)` é chamado pelo `Orchestrator.run()` no início. Todas as chamadas LLM subsequentes propagam automaticamente.
- **Como usar:** `python cli.py cost-report` agora pode agrupar por `course_id`. `cost_tracker.get_course_total('llm-finops')` retorna dados precisos por curso.
- **Compat backward:** se `set_course_context` não for chamado, comportamento idêntico ao anterior.


## 2026-04-09 — Mudanças da auditoria de ecossistema (Wave A-C)

### 1. CLI `drafts-to-tsx` (F12)
- **Commit:** `bc2f36e` — `feat(cli): drafts-to-tsx`
- **Arquivos:** `cli.py` (+novo subcomando), `src/converters/__init__.py`, `src/converters/draft_to_course.py`
- **Uso:** `python cli.py drafts-to-tsx [--input output/drafts] [--output output/converted_from_drafts]`
- **Resultado da execução desta sessão:** **12/12 drafts órfãos convertidos** para TSX deployable. Output em `output/converted_from_drafts/` com `page.tsx` + `layout.tsx` válidos por curso.
- **Próximo passo do owner:** revisar manualmente cada `output/converted_from_drafts/{slug}/page.tsx`, decidir quais publicar, mover aprovados para `output/deployed/`, commit final.
- **Cursos liberados:** automacao-com-n8n (×2), deploy-moderno, geo-para-educacao-financeira-40 e -sub-18, llm-finops (×2), mcp-avancado (×2), prompt-engineering-avancado, seo-e-geo-para-advogados, seo-e-geo-para-revendedoras-de-joias.
- **Conversor é best-effort:** parseia markdown da etapa `review` (preferida) ou `draft` (fallback), splita por headings, gera CourseSections (TEXT, CODE, TIP, CHECKPOINT). Cursos com 1 step só (sem headings claros) são clamped para 30 min mínimo.

### 2. Pre-commit secret_guard (F44)
- **Commit:** `8638b3f` — `sec(precommit): instala secret_guard`
- **Arquivos:** `.tools/secret_guard.py`, `.githooks/pre-commit`
- **Já ativado** localmente

### Achados pendentes neste repo

- **F13 (CRÍTICO):** ~~`voice_guard.py` programático ainda não existe.~~ **RESOLVIDO** na onda 2026-04-09 (B-012) e depois parametrizado por ClientContext em 2026-04-19.
- **F38 → BAIXO:** `curso-factory` chama LLMs direto em vez de usar `geo-orchestrator`. Crosscheck Gemini concordou que esse achado estava superdimensionado. Migração para SDK fica para uma onda futura.
