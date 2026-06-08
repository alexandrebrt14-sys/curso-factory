# Arquitetura — curso-factory

Documento prático: o que cada bloco faz, onde tem dependência, e o que precisa mudar para reusar como base de outro portal educacional (em outro segmento, outro autor, outro domínio).

## Visão de 30 segundos

```
config/clients/<id>/client.yaml      identidade, naming, branding, editorial
        │
        ▼ load_client()
ClientContext  ──────────────►  Orchestrator  ─►  CourseFactory.run(...)
        │                            │
        │                            ▼
        │                     5 agents (Researcher → Writer → Analyzer → Classifier → Reviewer)
        │                            │
        │                            ▼
        │                     LLMClient  (cache + circuit breaker + retry + cost_tracker)
        │                            │
        │                            ▼
        │                     output/drafts/<slug>_<ts>.json
        ▼
SchemaBuilder ──► CourseDefinition ──► TsxGenerator ──► output/.../page.tsx + layout.tsx
        ▲                                       │
        │                                       ▼
QualityGate (acentos + conteúdo + links + voice_guard + html opcional)
```

## Camadas

### 1. Identidade — `src/clients/`
- `context.py` define `ClientContext` (autor, domínio, empresa, branding, regras editoriais, voice guard).
- `loader.py` lê `config/clients/<id>/client.yaml` e materializa o contexto.
- **Regra de ouro:** nada de identidade fica hardcoded no código. Tudo passa pelo `ClientContext`.

### 2. Pipeline — `src/agents/` + `src/orchestrator.py`
- `Agent` (base) carrega prompt externo de `src/templates/prompts/<x>.md`. Cada subagente só configura `provider`, `model`, `prompt_file`.
- `Orchestrator.run(course)` executa 5 etapas (Researcher → Writer → Analyzer → Classifier → Reviewer) com checkpoint incremental em `output/drafts/<slug>_checkpoint.json` para resume após desconexão.
- `CourseFactory` (`src/agents/pipeline.py`) é o entry-point amigável usado pelo CLI.

### 3. Provedores — `src/llm_client.py` + `config/providers.yaml`
- `LLMClient` une 3 protocolos (OpenAI-compat, Anthropic, Google) atrás de uma interface única.
- Inclui: token bucket (rate limit), circuit breaker, retry com backoff, fallback entre providers, `cost_tracker` e `cache` (`src/cache.py`).
- Pricing/endpoints/fallback vêm 100% de `config/providers.yaml` — trocar de modelo é editar YAML.

### 4. Modelo de domínio — `src/models.py`
- `Course` / `Module` / `Step` — entidade canônica antes da geração.
- `CourseDefinition` — entrada determinística para o gerador de TSX. Sem campos de identidade hardcoded; quem instancia precisa preencher autor/domínio via `ClientContext`.
- `CourseSection` — TEXT, CODE, WARNING, TIP, CHECKPOINT.

### 5. Parser canônico — `src/parsers/markdown_parser.py`
- Fonte única de `slugify`, `short_id`, `extract_module_blocks`, `parse_module_to_sections`.
- Usado pelo `SchemaBuilder` (caminho feliz) **e** pelo `draft_to_course` (recovery de drafts órfãos). Quando um deles muda, o outro herda a correção.

### 6. Geração — `src/generators/`
- `tsx_generator.py` — Jinja2 puro; templates em `src/templates/*.j2`. Sem regex de substituição.
- `schema_builder.py` — converte saída do pipeline em `CourseDefinition` validado.
- `metadata_sync.py` — escreve `output/course_catalog.json` (consumido por worker externo da landing page).
- `build_validator.py` — roda `npx next build` no diretório da landing page (opcional).

### 7. Validação — `src/validators/`
- `accent_checker.py` — 300+ palavras PT-BR sem acento, com auto-fix preservando código/URLs.
- `content_checker.py` — palavras por módulo, tabelas, hierarquia de títulos, exercícios, andragogia, Bloom, clichês.
- `link_checker.py` — acentos em URL = ERRO crítico (regressão histórica).
- `html_validator.py` — opcional, só quando o conteúdo é HTML.
- `voice_guard.py` — barreira programática do padrão editorial do **cliente ativo**.
- `quality_gate.py` — orquestra tudo; com `auto_fix=True` corrige acentos e devolve texto limpo.

### 8. FinOps — `src/cost_tracker.py` + `src/cache.py`
- `CostTracker` persiste cada chamada LLM em `output/costs.json` com `course_id`, `provider`, `model`, tokens e custo.
- Budget guard: $5 max Claude / $10 max total por curso (configurável via env).
- `Cache` SHA-256 com TTL evita reprocessar prompts já vistos. Plugado por padrão no `LLMClient`.

### 9. Conversão de drafts órfãos — `src/converters/draft_to_course.py`
- Quando um pipeline foi executado mas nunca convertido para TSX, este módulo lê o JSON em `output/drafts/`, parseia via `markdown_parser`, e gera `CourseDefinition` + TSX.
- Best-effort: drafts inválidos viram warning, batch continua.

### 10. CLI — `cli.py`
- 8 subcomandos: `create`, `clients`, `validate`, `cost-report`, `batch`, `emit-catalog`, `drafts-to-tsx`, `cache-clear`.
- Todos aceitam `--client <id>` para escolher cliente em `config/clients/<id>/`.

## O que é **portal-agnóstico** (já reusável)

- Pipeline de 5 LLMs, prompts externos, providers em YAML.
- Models Pydantic (`Course`, `CourseDefinition`, `CourseSection`).
- Parser de Markdown e geradores Jinja2.
- Quality gate (5 camadas).
- Voice guard parametrizado por cliente.
- Cost tracker / cache / budget guard.
- Conversor de drafts órfãos.

Para um novo portal de outro segmento (ex: ensino técnico, gastronomia, finanças pessoais), basta:

1. Copiar `config/clients/_template/` para `config/clients/<novo>/`.
2. Preencher `client.yaml` (autor, domínio, branding, voice guard, editorial).
3. Ajustar templates Jinja2 em `src/templates/*.j2` se a landing page tiver layout próprio (opcional — o template atual é genérico Tailwind).
4. Ajustar prompts em `src/templates/prompts/*.md` se o tom HSM/HBR não couber.
5. Rodar `python cli.py create "Nome do Curso" --client <novo>`.

## O que é **específico** do segmento atual (precisa adaptação)

- Prompts em `src/templates/prompts/*.md` mencionam "HSM/HBR/MIT Sloan", "andragogia Knowles", "Bloom" — adequados para B2B/corporativo. Para outros segmentos, ajuste o prompt.
- `content_checker.py` impõe 2.500-4.000 palavras/módulo, ≥1 tabela, ≥3 exercícios. Para cursos curtos (cooking class), relaxe via `client.yaml` (`editorial.words_per_module_min/max`) e via fork do checker.
- `src/indexer/course_indexer.py` integra com Supabase + OpenAI embeddings — substitua por outro provider de busca vetorial se preferir.
- `docs/knowledge/geo-aeo/` é base de conhecimento sobre GEO. Não venha junto se o portal não é sobre GEO.

## Limites e gaps conhecidos

- `course_indexer.py` é standalone — não está plugado no CLI principal.
- `metadata_sync` lê de `config/courses.yaml` + diretórios `output/`, não da pasta `output/clients/<id>/`. Quando rodar para múltiplos clientes, considere passar `--output-dir` apontando para a pasta do cliente.
- Não existe ainda integração Discord/Slack para notificar quando pipeline conclui.

## Módulos principais

| Módulo                               | Responsabilidade                                              |
|--------------------------------------|---------------------------------------------------------------|
| `cli.py`                             | CLI principal (8 subcomandos)                                 |
| `src/clients/context.py`             | Dataclass `ClientContext`                                     |
| `src/clients/loader.py`              | `load_client(id)` + `list_clients()`                          |
| `src/providers.py`                   | Carregamento de `config/providers.yaml`                       |
| `src/agents/pipeline.py`             | `CourseFactory` — wrapper de alto nível                       |
| `src/orchestrator.py`                | 5 etapas + checkpoint incremental                             |
| `src/llm_client.py`                  | HTTP unificado: cache + circuit breaker + retry + cost log    |
| `src/agents/{researcher,writer,analyzer,classifier,reviewer}.py` | 1 agente por LLM           |
| `src/validators/quality_gate.py`     | 5 camadas de validação                                        |
| `src/validators/accent_checker.py`   | 300+ mapeamentos + auto-correção PT-BR                        |
| `src/validators/voice_guard.py`      | 4 dimensões ponderadas por `ClientContext`                    |
| `src/parsers/markdown_parser.py`     | slugify, extract_module_blocks, parse_module_to_sections      |
| `src/generators/schema_builder.py`   | Markdown → `CourseDefinition`                                 |
| `src/generators/tsx_generator.py`    | `CourseDefinition` → `page.tsx` + `layout.tsx`                |
| `src/generators/metadata_sync.py`    | Emite `output/course_catalog.json`                            |
| `src/converters/draft_to_course.py`  | Recovery: drafts órfãos JSON → TSX                            |
| `src/cost_tracker.py`                | Registro de custo por chamada com budget guard                |
| `src/cache.py`                       | Cache SHA-256 com TTL                                         |
| `src/config.py`                      | Env vars, budgets, paths                                      |
