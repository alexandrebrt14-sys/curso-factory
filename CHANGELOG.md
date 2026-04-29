# Changelog

Histórico de mudanças relevantes do curso-factory. Formato baseado em [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) e versionamento [SemVer](https://semver.org/lang/pt-BR/).

Histórico narrativo de cada onda em [[Refactor-2026-04-29]] e demais páginas da [Wiki](https://github.com/alexandrebrt14-sys/curso-factory/wiki).

## [Unreleased]

### Adicionado
- Templates GitHub: `.github/ISSUE_TEMPLATE/` (bug, feature, question, config), `pull_request_template.md`, `dependabot.yml`.
- `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`.
- 5 issues epic abertas para waves 6-10 (engagement, tutor IA, multi-idioma, certificação, comunidade).
- 4 milestones (v1.0 / v2.0 / v3.0 / v4.0) atribuídos às issues correspondentes.
- Project board público "curso-factory roadmap" com 19 itens.

### Mudado
- Topics do repo atualizados: `python, llm, openai, anthropic, claude, gemini, perplexity, groq, education, course-generation, multi-tenant, jinja2, pydantic, brasil-geo, portuguese, quality-gate, finops, cli, geo, aeo`.
- Description e homepage URL apontando para a Wiki.

### Segurança
- `dependabot.yml` configurado para atualização semanal de pip e GitHub Actions.
- Dependabot security updates habilitado.

## [1.0.0] — 2026-04-29

Refatoração profunda em 5 waves para tornar o curso-factory base reusável de outros portais educacionais. Detalhes completos em [Wiki / Refactor-2026-04-29](https://github.com/alexandrebrt14-sys/curso-factory/wiki/Refactor-2026-04-29).

### Adicionado
- 50 testes novos (24 → 74 totais): `test_cli.py` (11), `test_parsers.py` (14), `test_converters.py` (7), `test_cost_cache.py` (8), `test_validators_smoke.py` (10).
- `scripts/legacy/` com README explicando scripts ad-hoc preservados.
- Wiki completa (22 páginas, ~5.500 linhas): Home, Quick-Start, Architecture, CLI-Reference, Multi-Client-Setup, Pipeline-and-Agents, Quality-Gate, FinOps-and-Caching, Reusing-for-New-Segment, Testing, Project-Structure, Roadmap-and-Gaps, Refactor-2026-04-29, FAQ, Glossario, API-Reference, Prompt-Engineering, Observability-and-Debug, Lessons-Learned, Benchmarking-2026.

### Mudado
- `cli.py` reescrito (415 linhas) com imports corretos para todos os 8 subcomandos.
- `cmd_validate` agora usa `QualityGate` real (acentos + conteúdo + links + voice guard).
- `cmd_cost_report` lê o log JSON real do `CostTracker`.
- `cmd_batch` usa `CourseFactory` com `client` e `course_config` separados.
- `cmd_cache_clear` usa `Cache.clear()` real.
- `writer.py` e `reviewer.py` adotam `**template_vars` para paridade com Researcher/Analyzer/Classifier.
- `LLMClient` ganha `Cache` plugado por padrão (`use_cache=True`).
- `models.py:CourseDefinition` — defaults de identidade ("Alexandre Caramaschi", "Brasil GEO") zerados; quem instancia precisa injetar via `ClientContext`.
- `SchemaBuilder` ganha clamp `max(30, duracao)` paritário com `convert_drafts_directory`.
- `datetime.utcnow()` migrado para `datetime.now(timezone.utc)` em `cost_tracker.py`, `orchestrator.py`, `models.py`, `quality_gate.py` (zero `DeprecationWarning`).
- `docs/ARCHITECTURE.md` reescrito como guia portal-agnóstico.
- `README.md` ganha badge de status atualizado.
- `CLAUDE.md` ganha registro da refatoração no topo.

### Corrigido
- 4 subcomandos do CLI antes quebrados por imports inexistentes (`validate`, `cost-report`, `batch`, `cache-clear`):
  - `from src.validators.quality import QualityValidator` → `src.validators.quality_gate.QualityGate`
  - `from src.validators.accents import AccentValidator` → `src.validators.accent_checker`
  - `from src.config import load_config` → `src.config` não tem `load_config`; uso correto via `OUTPUT_DIR`/`CACHE_DIR`
  - `from src.agents.cost_tracker` → `src.cost_tracker`
- `cmd_cost_report` chamava API fictícia (`tracker.generate_report()`, `report.by_provider`); refatorado para usar `tracker.report()` real + agregação manual do log.

### Removido
- `src/unified_finops.py` — adapter para `geo-finops` calls.db unificado, zero referências, dependência implícita em path absoluto Windows.
- `Orchestrator._build_writer_context` — método de 19 linhas nunca chamado.
- 4 scripts ad-hoc movidos para `scripts/legacy/`: `clean_markdown_for_tsx.py`, `convert_drafts_to_tsx.py`, `generate_joias_course.py`, `generate_joias_course_v2.py`.

## [0.x.x] — Pré-refactor

Histórico narrativo das ondas anteriores em `CLAUDE.md` e `README.md`. Marcos:

### 2026-04-25 — Base de conhecimento GEO/AEO/Agentic Commerce
- Camada doutrinária permanente em `docs/knowledge/geo-aeo/` (17 arquivos, 2.640 linhas).
- 25+ papers acadêmicos (2025-2026) sintetizados em 30 instruções operacionais, 7 princípios mestres, 4 checklists.
- PR #1 aberto com este conteúdo.

### 2026-04-19 — Refactor multi-tenant (Ondas 1-5 originais)
- `ClientContext` introduzido em `src/clients/context.py`.
- `config/clients/<id>/client.yaml` como fonte única de identidade.
- `markdown_parser.py` consolidado (parser canônico).
- `providers.yaml` substituindo dicts hardcoded em `llm_client.py`.
- Voice Guard incorporado ao `QualityGate` como 4ª camada bloqueante.

### 2026-04-09 — Wave D
- `course_id` propagado no `cost_tracker` (achado F32) — antes recebia sempre `""`, impedia rastreamento por curso.

### 2026-04-08 — Auditoria de ecossistema (Ondas A-C)
- CLI `drafts-to-tsx` (achado F12) — recupera 13 cursos órfãos com investimento LLM já gasto.
- Pre-commit secret_guard (achado F44) ativado.

### 2026-03-28 — Inicial
- Repo público criado.
- Pipeline 5-LLM básico (Researcher → Writer → Analyzer → Classifier → Reviewer).

---

## Convenções

### Categorias

- **Adicionado** — features novas.
- **Mudado** — mudanças em features existentes (sem quebrar API).
- **Corrigido** — bug fixes.
- **Removido** — features ou código removidos.
- **Segurança** — vulnerabilidades patchedas.
- **Deprecado** — features marcadas para remoção em release futuro.

### Versionamento

- **MAJOR** — quebra de API pública (rebasear ClientContext, mudar contrato de Course/CourseDefinition, etc.).
- **MINOR** — features novas backward-compat (subcomandos novos, suporte a novo provider, etc.).
- **PATCH** — bug fix sem mudança de comportamento.

Pre-1.0: APIs ainda podem mudar entre minors.

## Como atualizar

Ao mergear PR, adicionar entrada em `## [Unreleased]`. Antes de tag de release, mover entradas para nova seção `## [X.Y.Z] — YYYY-MM-DD`.

## Links

- [Releases no GitHub](https://github.com/alexandrebrt14-sys/curso-factory/releases)
- [Wiki](https://github.com/alexandrebrt14-sys/curso-factory/wiki)
- [Roadmap (Project)](https://github.com/users/alexandrebrt14-sys/projects/2)
