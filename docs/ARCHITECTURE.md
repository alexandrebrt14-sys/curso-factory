# Arquitetura — Curso Factory

## Visão Geral

O Curso Factory é um pipeline multi-LLM orquestrado que transforma um nome
de curso em conteúdo educacional completo, revisado e pronto para publicação.
Cada estágio é executado pelo LLM mais adequado para aquela função específica.

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

| Módulo                        | Responsabilidade                              |
|-------------------------------|-----------------------------------------------|
| `src/agents/pipeline.py`      | Orquestrador principal do pipeline            |
| `src/agents/research.py`      | Integração com Perplexity API                 |
| `src/agents/draft.py`         | Integração com OpenAI GPT-4o                  |
| `src/agents/analyze.py`       | Integração com Google Gemini                  |
| `src/agents/classify.py`      | Integração com Groq                           |
| `src/agents/review.py`        | Integração com Anthropic Claude               |
| `src/agents/cost_tracker.py`  | Rastreamento de custos por provider           |
| `src/validators/quality.py`   | Validação pedagógica local (pré-LLM)          |
| `src/validators/accents.py`   | Validação de acentuação PT-BR                 |
| `src/config.py`               | Carregamento de configuração e variáveis      |
