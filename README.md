# curso-factory

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![5 LLMs](https://img.shields.io/badge/LLMs-5_orquestrados-0176d3)
![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)

---

## O que e

O curso-factory e uma fabrica de cursos educacionais de altissima qualidade, construida sobre um pipeline de 5 LLMs orquestrados. O sistema recebe a definicao de um curso em YAML, executa um pipeline de 5 etapas (pesquisa, redacao, analise, classificacao, revisao) e entrega modulos completos, validados e prontos para deploy.

Todos os cursos sao gerados com dados atualizados de 2026, passam por validacao automatica de qualidade, acentuacao PT-BR e consistencia editorial antes de serem aprovados para publicacao.

---

## Problema que resolve

### 1. Heredocs gigantes que quebram no shell

Scripts que embutem HTML ou Markdown em heredocs dentro de shell scripts quebram com caracteres especiais, aspas e acentos. O curso-factory usa **templates Jinja2 em arquivos separados** (`src/templates/`), eliminando completamente heredocs do pipeline de geracao.

### 2. Scripts de substituicao frageis

Scripts Python que fazem `str.replace()` ou regex para inserir conteudo em pontos especificos de um arquivo erram o ponto de insercao quando o template muda. A solucao e **geracao atomica com validacao automatica**: cada modulo e gerado inteiro a partir do template, nunca por insercao parcial.

### 3. Agentes falhando por API

Chamadas a APIs de LLMs falham por rate limiting, timeout ou indisponibilidade. O curso-factory implementa **circuit breaker**, **retry com backoff exponencial** e **fallback entre LLMs** — se o GPT-4o falha, Claude assume a redacao; se Perplexity cai, Gemini faz a pesquisa.

### 4. Retrabalho por falta de validacao

Sem validacao automatica, erros de acentuacao, links quebrados e HTML malformado so sao descobertos apos o deploy. O curso-factory inclui um **quality gate pre-deploy** com 4 validadores independentes: acentuacao PT-BR, HTML, links e regras de qualidade configuraveis.

### 5. FinOps ineficiente

Sem controle de custos, o pipeline consome creditos desnecessariamente reprocessando conteudo ja gerado ou usando modelos caros para tarefas simples. A solucao inclui **budget guard pre-execucao**, **cost tracking em tempo real** e **cache de resultados** com TTL para evitar reprocessamento.

---

## Arquitetura

```
Definicao YAML --> Orchestrator --> Pipeline (5 etapas)
                                        |
                        +---------------+---------------+
                        |               |               |
                   Etapa 1-2        Etapa 3-4        Etapa 5
                   (paralelo)       (paralelo)       (sequencial)
                   +----+----+      +----+----+      +--------+
                   | Px | 4o |      | Gm | Gq |      | Claude |
                   +----+----+      +----+----+      +--------+
                   Px=Perplexity 4o=GPT-4o Gm=Gemini Gq=Groq

                        |
                        v
                   Quality Gate
                   (4 validadores)
                        |
                        v
                output/approved/
```

O pipeline executa em **waves paralelas**: pesquisa e redacao podem rodar em paralelo quando ha modulos independentes. Analise e classificacao tambem rodam juntas. A revisao final e sempre sequencial, garantindo consistencia editorial.

---

## 5 LLMs e seus papeis

| Etapa | Provider | Modelo | Papel | Por que este LLM |
|-------|----------|--------|-------|-------------------|
| **1. RESEARCH** | Perplexity | sonar-pro | Coleta dados atualizados, fontes, tendencias 2026 | Unico LLM com acesso a web em tempo real e citacoes |
| **2. DRAFT** | OpenAI | gpt-4o | Redige modulos com base nos dados coletados | Melhor redator longo em PT-BR, consistencia de tom |
| **3. ANALYZE** | Google | gemini-2.0-flash | Revisa qualidade, coerencia, gaps, acessibilidade | Rapido e barato para analise estruturada |
| **4. CLASSIFY** | Groq | llama-3.3-70b | Classifica nivel, tags, pre-requisitos, duracao estimada | Latencia ultra-baixa para classificacao rapida |
| **5. REVIEW** | Anthropic | claude-sonnet-4-6 | Revisao final, acentuacao PT-BR, consistencia editorial | Melhor em instrucoes complexas e revisao critica |

Cada agente herda de `BaseAgent` (`src/agents/base.py`), que implementa retry com backoff exponencial, fallback para outro LLM e integracao com o circuit breaker.

---

## Pipeline de criacao

### Etapa 1 — Pesquisa (Perplexity)

O agente pesquisador recebe o topico do modulo e coleta:
- Dados atualizados de 2026 com fontes citaveis
- Tendencias de mercado e tecnologia
- Exemplos praticos e cases reais
- Estatisticas e metricas relevantes

### Etapa 2 — Redacao (GPT-4o)

O agente redator recebe os dados da pesquisa e gera:
- Conteudo completo do modulo em PT-BR
- Exemplos de codigo quando aplicavel
- Exercicios praticos
- Resumo executivo

### Etapa 3 — Analise (Gemini)

O agente analista revisa o rascunho verificando:
- Coerencia com o programa do curso
- Gaps de conteudo
- Acessibilidade e clareza
- Nivel de dificuldade consistente

### Etapa 4 — Classificacao (Groq)

O agente classificador atribui metadados:
- Nivel (iniciante, intermediario, avancado)
- Tags e palavras-chave
- Pre-requisitos
- Duracao estimada de estudo

### Etapa 5 — Revisao (Claude)

O agente revisor faz a passada final:
- Acentuacao PT-BR completa
- Consistencia editorial
- Validacao tecnica do conteudo
- Formatacao e estrutura

---

## FinOps e governanca

### Custos por provider

| Provider | Modelo | Custo/1M tokens (input) | Custo/1M tokens (output) | Limite diario | Papel |
|----------|--------|-------------------------|--------------------------|---------------|-------|
| Perplexity | sonar-pro | US$ 3,00 | US$ 15,00 | US$ 5,00 | Pesquisa |
| OpenAI | gpt-4o | US$ 2,50 | US$ 10,00 | US$ 8,00 | Redacao |
| Google | gemini-2.0-flash | US$ 0,10 | US$ 0,40 | US$ 2,00 | Analise |
| Groq | llama-3.3-70b | US$ 0,59 | US$ 0,79 | US$ 1,00 | Classificacao |
| Anthropic | claude-sonnet-4-6 | US$ 3,00 | US$ 15,00 | US$ 8,00 | Revisao |

### Mecanismos de controle

- **Budget guard**: antes de executar uma etapa, o sistema estima o custo e bloqueia se ultrapassar o limite diario do provider
- **Cost tracking**: cada chamada de API registra tokens consumidos e custo real em `output/cost_history.jsonl`
- **Cache de resultados**: resultados sao cacheados por SHA-256 do input com TTL de 24h — reprocessamento desnecessario e eliminado
- **Alertas**: se o custo real excede 2x a estimativa, o pipeline emite alerta e pode pausar
- **Limites diarios**: cada provider tem um teto diario configuravel; ao atingir, o fallback assume

### Custo estimado por curso

Um curso completo com 10 modulos custa aproximadamente US$ 3,00 a US$ 8,00, dependendo da complexidade e do volume de pesquisa necessario.

---

## Instalacao

### Pre-requisitos

- Python 3.11+
- pip ou uv

### Setup

```bash
# Clonar o repositorio
git clone https://github.com/alexandrebrt14-sys/curso-factory.git
cd curso-factory

# Instalar dependencias
pip install -e .

# Configurar chaves de API
cp .env.example .env
# Editar .env com suas 5 chaves:
#   PERPLEXITY_API_KEY=pplx-...
#   OPENAI_API_KEY=sk-...
#   GOOGLE_API_KEY=AIza...
#   GROQ_API_KEY=gsk_...
#   ANTHROPIC_API_KEY=sk-ant-...
```

---

## Uso (CLI)

```bash
# Criar um curso completo a partir de definicao YAML
python cli.py create --config config/courses.yaml --course "nome-do-curso"

# Criar apenas um modulo especifico
python cli.py create-module --config config/courses.yaml --course "nome-do-curso" --module 3

# Executar apenas uma etapa do pipeline
python cli.py run-step --step research --input "topico do modulo"
python cli.py run-step --step draft --input output/drafts/modulo-3-research.json
python cli.py run-step --step analyze --input output/drafts/modulo-3-draft.md
python cli.py run-step --step classify --input output/drafts/modulo-3-draft.md
python cli.py run-step --step review --input output/drafts/modulo-3-analyzed.md

# Validar um modulo sem executar o pipeline
python cli.py validate --input output/drafts/modulo-3.md

# Ver status dos providers (limites, custos, circuit breaker)
python cli.py status

# Relatorio de custos
python cli.py cost-report

# Limpar cache
python cli.py cache-clear
```

### Exemplos de definicao YAML

```yaml
# config/courses.yaml
courses:
  geo-fundamentos:
    title: "GEO Fundamentos — Otimizacao para Motores Generativos"
    audience: "Profissionais de marketing digital e SEO"
    level: "intermediario"
    modules:
      - title: "O que e GEO e por que importa em 2026"
        topics: ["definicao", "diferenca-seo-geo", "metricas"]
      - title: "Entidades e Knowledge Graph"
        topics: ["schema-org", "wikidata", "entity-consistency"]
      - title: "llms.txt e ai-agents.json"
        topics: ["discovery-files", "implementacao", "validacao"]
```

---

## Estrutura do projeto

```
curso-factory/
├── cli.py                    # Entrada principal CLI
├── pyproject.toml            # Metadata e dependencias
├── .env.example              # Template de configuracao (5 API keys)
├── CLAUDE.md                 # Instrucoes Claude Code
├── README.md
├── config/
│   ├── courses.yaml          # Definicao dos cursos a criar
│   └── quality_rules.yaml    # Regras de qualidade e validacao
├── src/
│   ├── __init__.py
│   ├── config.py             # Configuracoes globais
│   ├── models.py             # Pydantic models (Course, Module, Step)
│   ├── orchestrator.py       # Orquestracao do pipeline
│   ├── pipeline.py           # Execucao em waves paralelas
│   ├── router.py             # Roteamento por tipo de tarefa
│   ├── llm_client.py         # Cliente HTTP unificado com circuit breaker
│   ├── rate_limiter.py       # Token bucket por provider
│   ├── cost_tracker.py       # Rastreamento de custos em tempo real
│   ├── finops.py             # Governanca FinOps com budget guard
│   ├── cache.py              # Cache de resultados (SHA-256, TTL 24h)
│   ├── agents/
│   │   ├── base.py           # Classe base com retry e fallback
│   │   ├── researcher.py     # Perplexity — pesquisa
│   │   ├── writer.py         # GPT-4o — redacao
│   │   ├── analyzer.py       # Gemini — analise de qualidade
│   │   ├── classifier.py     # Groq — classificacao
│   │   └── reviewer.py       # Claude — revisao final
│   ├── templates/
│   │   ├── course.html.j2    # Template Jinja2 para pagina do curso
│   │   ├── module.html.j2    # Template para modulo individual
│   │   └── prompts/          # Prompts separados por agente
│   │       ├── research.md
│   │       ├── draft.md
│   │       ├── analyze.md
│   │       ├── classify.md
│   │       └── review.md
│   └── validators/
│       ├── accent_checker.py  # Valida acentuacao PT-BR
│       ├── html_validator.py  # Valida HTML gerado
│       ├── link_checker.py    # Valida links e hrefs
│       └── quality_gate.py    # Gate de qualidade pre-deploy
├── scripts/
│   ├── create_course.sh      # Wrapper para criar curso completo
│   └── batch_create.sh       # Criacao em lote
├── docs/
│   ├── ARCHITECTURE.md       # Documentacao tecnica da arquitetura
│   └── FINOPS.md             # Documentacao de FinOps
└── output/
    ├── drafts/               # Rascunhos em progresso
    ├── approved/             # Aprovados pelo quality gate
    └── deployed/             # Deployados em producao
```

---

## Convencoes

- **Idioma do conteudo**: Portugues do Brasil com acentuacao completa
- **Idioma do codigo**: Ingles
- **Arquivos Python**: snake_case (`cost_tracker.py`, `accent_checker.py`)
- **Comandos CLI**: kebab-case (`create-module`, `run-step`, `cost-report`)
- **HTTP**: httpx async para todas as chamadas LLM (sem SDKs oficiais)
- **Models**: Pydantic v2 para dominio, dataclass para infraestrutura
- **Cache**: SHA-256 do input como chave, TTL 24h, em `output/.cache/`
- **Custos**: registrados por chamada em `output/cost_history.jsonl`
- **Templates**: Jinja2 para HTML, Markdown para prompts

---

## Autor

**Alexandre Caramaschi** — CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil.

- [alexandrecaramaschi.com](https://alexandrecaramaschi.com)
- [LinkedIn](https://www.linkedin.com/in/alexandrecaramaschi/)
- [DEV Community](https://dev.to/alexandrecaramaschi)
- [Medium](https://medium.com/@alexandrecaramaschi)
- [YouTube](https://www.youtube.com/@alexandrecaramaschi)

---

## License

[MIT](LICENSE)
