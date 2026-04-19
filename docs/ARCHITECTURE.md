# Arquitetura — Curso Factory

## Visão Geral

O Curso Factory é um pipeline multi-LLM orquestrado que transforma um nome
de curso em conteúdo educacional completo, revisado e pronto para publicação.
Cada estágio é executado pelo LLM mais adequado para aquela função específica.

Desde a refatoração 2026-04-19, o framework é **multi-tenant**: todo o pipeline
recebe um `ClientContext` injetado (ver `src/clients/context.py`) que encapsula
autor, domínio, branding, padrão editorial e regras de voice guard. Isso
permite rodar a fábrica para diferentes empresas sem mudar código.

---

## Camada de Multi-tenancy

```
config/clients/<id>/client.yaml
        |
        v
src/clients/loader.py::load_client(id)
        |
        v
ClientContext (author, domain, branding, editorial, voice_guard, ...)
        |
        +--> CourseFactory(client=...)
        +--> Orchestrator(client_context=...)
        +--> SchemaBuilder.build(..., client=...)
        +--> QualityGate(client=...)
        +--> voice_guard_check(text, client=...)
```

Cliente `default` preserva o comportamento pré-refactor (Brasil GEO /
Alexandre Caramaschi). Qualquer outro `<id>` é totalmente isolado em
`output/clients/<id>/`.

Playbook de integração de novo cliente: ver [MULTI-CLIENT.md](MULTI-CLIENT.md).

---

## Diagrama do Pipeline

```
Entrada: nome do curso
        |
        v
+------------------+
|  1. PERPLEXITY   |  Pesquisa de mercado, dados 2025-2026, competidores
|  (Research)      |
+------------------+
        |
        v  research_data (JSON + Markdown)
+------------------+
|  2. GPT-4o       |  Redação didática de cada módulo
|  (Draft)         |  Executa em paralelo por módulo
+------------------+
        |
        v  draft_content (Markdown por módulo)
+------------------+
|  3. GEMINI       |  Análise de qualidade pedagógica
|  (Analyze)       |  Score 0-100, gaps, coerência
+------------------+
        |
        v  quality_report (JSON)
+------------------+
|  4. GROQ         |  Classificação: nível, tags, pré-requisitos, duração
|  (Classify)      |  Latência baixa, alto throughput
+------------------+
        |
        v  metadata (JSON)
+------------------+
|  5. CLAUDE       |  Revisão final: acentuação PT-BR, consistência,
|  (Review)        |  validação técnica, aprovação para publicação
+------------------+
        |
        v
Saída: output/approved/{slug}/
```

---

## Circuit Breaker

Cada chamada aos LLMs passa por um circuit breaker com três estados:

- **FECHADO (normal):** requisições fluem normalmente
- **ABERTO (falha):** após 3 falhas consecutivas, o circuito abre e o agente
  retorna erro imediato, evitando chamadas desnecessárias ao provider
- **SEMI-ABERTO (recuperação):** após 60 segundos, permite uma requisição
  de teste; se bem-sucedida, fecha o circuito; se falhar, reabre

Configuração em `config/settings.yaml`:

```yaml
circuit_breaker:
  failure_threshold: 3
  recovery_timeout_seconds: 60
  half_open_max_calls: 1
```

---

## Fluxo de Dados entre Agentes

```
CourseFactory.run(nome)
  |
  +-- ResearchAgent.run(nome)          --> research_data: ResearchResult
  |
  +-- DraftAgent.run(módulo, research) --> draft: DraftResult
  |   (executado N vezes, um por módulo, em paralelo via ThreadPoolExecutor)
  |
  +-- AnalyzeAgent.run(draft)          --> quality: QualityReport
  |
  +-- ClassifyAgent.run(draft)         --> metadata: ClassificationResult
  |
  +-- ReviewAgent.run(draft, quality)  --> final: ReviewedContent
  |
  +-- OutputWriter.save(final, metadata)
```

Todos os resultados intermediários são serializados em `.cache/{course_slug}/`
como arquivos JSON com hash do input, permitindo retomada sem retrabalho.

---

## Estratégia de Cache

O cache é baseado em hash SHA-256 do payload de entrada de cada agente.
Se o hash já existe em `.cache/`, o resultado armazenado é retornado
sem chamar o LLM, eliminando custos de reprocessamento.

Estrutura do cache:

```
.cache/
  {course_slug}/
    research_{hash}.json
    draft_{module}_{hash}.json
    analyze_{module}_{hash}.json
    classify_{hash}.json
    review_{hash}.json
    cost_log.jsonl
```

Para invalidar o cache de um curso específico, delete sua pasta.
Para limpar todo o cache: `python cli.py cache-clear`.

---

## Estratégia Anti-Retrabalho

O pipeline implementa três camadas de proteção contra retrabalho desnecessário:

1. **Cache de conteúdo:** hash do input — se o input não mudou, o output é reutilizado
2. **Checkpoint de estágio:** ao falhar no estágio N, o pipeline retoma do N, não do início
3. **Validação antes de chamar o LLM:** se o rascunho já passou no validador local,
   o agente de análise usa o resultado anterior salvo em cache

---

## Módulos Principais

| Módulo                               | Responsabilidade                                             |
|--------------------------------------|--------------------------------------------------------------|
| `cli.py`                             | CLI principal (create/clients/batch/validate/cost-report)    |
| `src/clients/context.py`             | Dataclass `ClientContext` (author, domain, voice_guard, ...) |
| `src/clients/loader.py`              | `load_client(id)` + `list_clients()`                         |
| `src/providers.py`                   | Carregamento de `config/providers.yaml` (pricing, endpoints) |
| `src/agents/pipeline.py`             | `CourseFactory` — wrapper de alto nível para CLI             |
| `src/orchestrator.py`                | Orchestrator: 5 etapas, checkpoint incremental, resume       |
| `src/llm_client.py`                  | HTTP unificado: circuit breaker, retry, fallback, cost log   |
| `src/agents/researcher.py`           | Agente Perplexity (sonar-pro)                                |
| `src/agents/writer.py`               | Agente GPT-4o (draft)                                        |
| `src/agents/analyzer.py`             | Agente Gemini 2.5 Pro (analyze)                              |
| `src/agents/classifier.py`           | Agente Groq (classify)                                       |
| `src/agents/reviewer.py`             | Agente Claude Opus 4.6 (review)                              |
| `src/validators/quality_gate.py`     | QualityGate: 4 camadas (acentos, conteúdo, links, voice_guard) |
| `src/validators/accent_checker.py`   | 300+ mapeamentos + auto-correção PT-BR                       |
| `src/validators/content_checker.py`  | Bloom, Knowles, tabelas, clichês                             |
| `src/validators/link_checker.py`     | Acentos em URLs (bloqueante)                                 |
| `src/validators/voice_guard.py`      | 4 dimensões ponderadas por `ClientContext`                   |
| `src/validators/html_validator.py`   | Fechamento de tags, acessibilidade                           |
| `src/parsers/markdown_parser.py`     | Fonte única: slugify, extract_module_blocks, parse sections   |
| `src/generators/schema_builder.py`   | Markdown → `CourseDefinition` validado                       |
| `src/generators/tsx_generator.py`    | `CourseDefinition` → `page.tsx` + `layout.tsx` (Jinja2)      |
| `src/generators/metadata_sync.py`    | Emite `output/course_catalog.json` consumido via worker      |
| `src/converters/draft_to_course.py`  | Recovery: drafts órfãos JSON → `CourseDefinition`            |
| `src/indexer/course_indexer.py`      | Embeddings OpenAI + upsert Supabase pgvector                 |
| `src/cost_tracker.py`                | Registro de custo por chamada com budget guard               |
| `src/config.py`                      | Env vars, budgets, paths                                     |
| `src/unified_finops.py`              | Adapter pro calls.db unificado (geo-finops)                  |
