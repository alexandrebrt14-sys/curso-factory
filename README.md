# curso-factory

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![5 LLMs](https://img.shields.io/badge/LLMs-5_orquestrados-0176d3)
![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)

---

## O que é

O curso-factory é uma fábrica de cursos educacionais de altíssima qualidade, construída sobre um pipeline de 5 LLMs orquestrados. O sistema recebe a definição de um curso em YAML, executa um pipeline de 5 etapas (pesquisa, redação, análise, classificação, revisão) e entrega módulos completos, validados e prontos para deploy.

Todos os cursos são gerados com dados atualizados de 2026, passam por validação automática de qualidade, acentuação PT-BR e consistência editorial antes de serem aprovados para publicação.

---

## Problema que resolve

### 1. Heredocs gigantes que quebram no shell

Scripts que embutem HTML ou Markdown em heredocs dentro de shell scripts quebram com caracteres especiais, aspas e acentos. O curso-factory usa **templates Jinja2 em arquivos separados** (`src/templates/`), eliminando completamente heredocs do pipeline de geração.

### 2. Scripts de substituição frágeis

Scripts Python que fazem `str.replace()` ou regex para inserir conteúdo em pontos específicos de um arquivo erram o ponto de inserção quando o template muda. A solução é **geração atômica com validação automática**: cada módulo é gerado inteiro a partir do template, nunca por inserção parcial.

### 3. Agentes falhando por API

Chamadas a APIs de LLMs falham por rate limiting, timeout ou indisponibilidade. O curso-factory implementa **circuit breaker**, **retry com backoff exponencial** e **fallback entre LLMs** — se o GPT-4o falha, Claude assume a redação; se Perplexity cai, Gemini faz a pesquisa.

### 4. Retrabalho por falta de validação

Sem validação automática, erros de acentuação, links quebrados e HTML malformado só são descobertos após o deploy. O curso-factory inclui um **quality gate pré-deploy** com 4 validadores independentes: acentuação PT-BR, HTML, links e regras de qualidade configuráveis.

### 5. FinOps ineficiente

Sem controle de custos, o pipeline consome créditos desnecessariamente reprocessando conteúdo já gerado ou usando modelos caros para tarefas simples. A solução inclui **budget guard pré-execução**, **cost tracking em tempo real** e **cache de resultados** com TTL para evitar reprocessamento.

---

## Arquitetura

```
Definição YAML --> Orchestrator --> Pipeline (5 etapas)
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

O pipeline executa em **waves paralelas**: pesquisa e redação podem rodar em paralelo quando há módulos independentes. Análise e classificação também rodam juntas. A revisão final é sempre sequencial, garantindo consistência editorial.

---

## 5 LLMs e seus papéis

| Etapa | Provider | Modelo | Papel | Por que este LLM |
|-------|----------|--------|-------|-------------------|
| **1. RESEARCH** | Perplexity | sonar-pro | Coleta dados atualizados, fontes, tendências 2026 | Único LLM com acesso a web em tempo real e citações |
| **2. DRAFT** | OpenAI | gpt-4o | Redige módulos com base nos dados coletados | Melhor redator longo em PT-BR, consistência de tom |
| **3. ANALYZE** | Google | gemini-2.5-pro | Revisa qualidade pedagógica, andragogia, formatação, acentuação | Análise profunda e estruturada com alto contexto |
| **4. CLASSIFY** | Groq | llama-3.3-70b | Classifica nível, tags, pré-requisitos, duração estimada | Latência ultra-baixa para classificação rápida |
| **5. REVIEW** | Anthropic | claude-opus-4-6 | Revisão final: acentuação PT-BR, qualidade editorial HSM/HBR, formatação | Melhor em instruções complexas e revisão crítica |

Cada agente herda de `BaseAgent` (`src/agents/base.py`), que implementa retry com backoff exponencial, fallback para outro LLM e integração com o circuit breaker.

---

## Pipeline de criação

### Etapa 1 — Pesquisa (Perplexity)

O agente pesquisador recebe o tópico do módulo e coleta:
- Dados atualizados de 2026 com fontes citáveis
- Tendências de mercado e tecnologia
- Exemplos práticos e cases reais
- Estatísticas e métricas relevantes

### Etapa 2 — Redação (GPT-4o)

O agente redator recebe os dados da pesquisa e gera:
- Conteúdo completo do módulo em PT-BR
- Exemplos de código quando aplicável
- Exercícios práticos
- Resumo executivo

### Etapa 3 — Análise (Gemini)

O agente analista revisa o rascunho verificando:
- Coerência com o programa do curso
- Gaps de conteúdo
- Acessibilidade e clareza
- Nível de dificuldade consistente

### Etapa 4 — Classificação (Groq)

O agente classificador atribui metadados:
- Nível (iniciante, intermediário, avançado)
- Tags e palavras-chave
- Pré-requisitos
- Duração estimada de estudo

### Etapa 5 — Revisão (Claude)

O agente revisor faz a passada final:
- Acentuação PT-BR completa (dicionário expandido com 150+ palavras)
- Qualidade editorial padrão HSM/HBR/MIT Sloan
- Conformidade andragógica (6 princípios de Knowles)
- Formatação rica: tabelas, listas, hierarquia de títulos, blocos de citação
- Validação técnica do conteúdo e precisão factual

---

## Padrão de Qualidade Editorial

### Referências Editoriais

O conteúdo produzido segue o padrão de publicações de referência:

| Publicação | Contribuição ao Estilo |
|------------|----------------------|
| **Harvard Business Review** | Profundidade analítica, insights baseados em evidências, tom propositivo |
| **MIT Sloan Management Review** | Rigor acadêmico aplicado, frameworks de decisão, dados quantitativos |
| **HSM Management** | Contextualização para o mercado brasileiro, cases locais e internacionais |

### Andragogia (Malcolm Knowles)

Todo conteúdo aplica os 6 princípios da aprendizagem de adultos:

1. **Necessidade de saber** — cada módulo abre explicando POR QUE o conhecimento é necessário
2. **Autoconceito** — o aluno é tratado como profissional autônomo, nunca de forma condescendente
3. **Experiência prévia** — conceitos novos se conectam com vivências profissionais do aluno
4. **Prontidão** — demonstração de aplicabilidade imediata no contexto de trabalho
5. **Orientação a problemas** — conteúdo organizado em torno de problemas reais, não taxonomias abstratas
6. **Motivação intrínseca** — aprendizado conectado com crescimento profissional e domínio

### Formatação Rica

Cada módulo inclui obrigatoriamente:

- Tabelas comparativas (ao menos uma por módulo)
- Listas numeradas para processos, com marcadores para enumerações
- Hierarquia clara de títulos (H2 > H3 > H4)
- Negrito para termos-chave na primeira ocorrência
- Blocos de citação para insights centrais e conceitos memoráveis
- Exercícios com progressão de complexidade (Taxonomia de Bloom)

### Acentuação PT-BR

O pipeline possui tripla barreira contra palavras sem acento:

1. **Instrução ao redator (GPT-4o)**: prompt com lista explícita de palavras obrigatoriamente acentuadas
2. **Análise de qualidade (Gemini)**: detecta e reporta palavras sem acento no relatório
3. **Revisão final (Claude)**: corrige todas as ocorrências com dicionário de 150+ palavras
4. **Validador local (accent_checker.py)**: barreira programática pré-deploy com 150+ mapeamentos

---

## FinOps e governança

### Custos por provider

| Provider | Modelo | Custo/1M tokens (input) | Custo/1M tokens (output) | Limite diário | Papel |
|----------|--------|-------------------------|--------------------------|---------------|-------|
| Perplexity | sonar-pro | US$ 3,00 | US$ 15,00 | US$ 5,00 | Pesquisa |
| OpenAI | gpt-4o | US$ 2,50 | US$ 10,00 | US$ 8,00 | Redação |
| Google | gemini-2.5-pro | US$ 1,25 | US$ 10,00 | US$ 5,00 | Análise |
| Groq | llama-3.3-70b | US$ 0,59 | US$ 0,79 | US$ 1,00 | Classificação |
| Anthropic | claude-opus-4-6 | US$ 15,00 | US$ 75,00 | US$ 8,00 | Revisão |

### Mecanismos de controle

- **Budget guard**: antes de executar uma etapa, o sistema estima o custo e bloqueia se ultrapassar o limite diário do provider
- **Cost tracking**: cada chamada de API registra tokens consumidos e custo real em `output/cost_history.jsonl`
- **Cache de resultados**: resultados são cacheados por SHA-256 do input com TTL de 24h — reprocessamento desnecessário é eliminado
- **Alertas**: se o custo real excede 2x a estimativa, o pipeline emite alerta e pode pausar
- **Limites diários**: cada provider tem um teto diário configurável; ao atingir, o fallback assume

### Custo estimado por curso

Um curso completo com 10 módulos custa aproximadamente US$ 3,00 a US$ 8,00, dependendo da complexidade e do volume de pesquisa necessário.

---

## Instalação

### Pré-requisitos

- Python 3.11+
- pip ou uv

### Setup

```bash
# Clonar o repositório
git clone https://github.com/alexandrebrt14-sys/curso-factory.git
cd curso-factory

# Instalar dependências
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
# Criar um curso completo a partir de definição YAML
python cli.py create --config config/courses.yaml --course "nome-do-curso"

# Criar apenas um módulo específico
python cli.py create-module --config config/courses.yaml --course "nome-do-curso" --module 3

# Executar apenas uma etapa do pipeline
python cli.py run-step --step research --input "tópico do módulo"
python cli.py run-step --step draft --input output/drafts/modulo-3-research.json
python cli.py run-step --step analyze --input output/drafts/modulo-3-draft.md
python cli.py run-step --step classify --input output/drafts/modulo-3-draft.md
python cli.py run-step --step review --input output/drafts/modulo-3-analyzed.md

# Validar um módulo sem executar o pipeline
python cli.py validate --input output/drafts/modulo-3.md

# Ver status dos providers (limites, custos, circuit breaker)
python cli.py status

# Relatório de custos
python cli.py cost-report

# Limpar cache
python cli.py cache-clear
```

### Exemplos de definição YAML

```yaml
# config/courses.yaml
courses:
  geo-fundamentos:
    title: "GEO Fundamentos — Otimização para Motores Generativos"
    audience: "Profissionais de marketing digital e SEO"
    level: "intermediário"
    modules:
      - title: "O que é GEO e por que importa em 2026"
        topics: ["definição", "diferença-seo-geo", "métricas"]
      - title: "Entidades e Knowledge Graph"
        topics: ["schema-org", "wikidata", "entity-consistency"]
      - title: "llms.txt e ai-agents.json"
        topics: ["discovery-files", "implementação", "validação"]
```

---

## Estrutura do projeto

```
curso-factory/
├── cli.py                    # Entrada principal CLI
├── pyproject.toml            # Metadata e dependências
├── .env.example              # Template de configuração (5 API keys)
├── CLAUDE.md                 # Instruções Claude Code
├── README.md
├── config/
│   ├── courses.yaml          # Definição dos cursos a criar
│   └── quality_rules.yaml    # Regras de qualidade e validação
├── src/
│   ├── __init__.py
│   ├── config.py             # Configurações globais
│   ├── models.py             # Pydantic models (Course, Module, Step)
│   ├── orchestrator.py       # Orquestração do pipeline
│   ├── pipeline.py           # Execução em waves paralelas
│   ├── router.py             # Roteamento por tipo de tarefa
│   ├── llm_client.py         # Cliente HTTP unificado com circuit breaker
│   ├── rate_limiter.py       # Token bucket por provider
│   ├── cost_tracker.py       # Rastreamento de custos em tempo real
│   ├── finops.py             # Governança FinOps com budget guard
│   ├── cache.py              # Cache de resultados (SHA-256, TTL 24h)
│   ├── agents/
│   │   ├── base.py           # Classe base com retry e fallback
│   │   ├── researcher.py     # Perplexity — pesquisa
│   │   ├── writer.py         # GPT-4o — redação
│   │   ├── analyzer.py       # Gemini — análise de qualidade
│   │   ├── classifier.py     # Groq — classificação
│   │   └── reviewer.py       # Claude — revisão final
│   ├── templates/
│   │   ├── course.html.j2    # Template Jinja2 para página do curso
│   │   ├── module.html.j2    # Template para módulo individual
│   │   └── prompts/          # Prompts separados por agente
│   │       ├── research.md
│   │       ├── draft.md
│   │       ├── analyze.md
│   │       ├── classify.md
│   │       └── review.md
│   └── validators/
│       ├── accent_checker.py  # Valida acentuação PT-BR
│       ├── html_validator.py  # Valida HTML gerado
│       ├── link_checker.py    # Valida links e hrefs
│       └── quality_gate.py    # Gate de qualidade pré-deploy
├── scripts/
│   ├── create_course.sh      # Wrapper para criar curso completo
│   └── batch_create.sh       # Criação em lote
├── docs/
│   ├── ARCHITECTURE.md       # Documentação técnica da arquitetura
│   └── FINOPS.md             # Documentação de FinOps
└── output/
    ├── drafts/               # Rascunhos em progresso
    ├── approved/             # Aprovados pelo quality gate
    └── deployed/             # Deployados em produção
```

---

## Convenções

- **Idioma do conteúdo**: Português do Brasil com acentuação completa
- **Idioma do código**: Inglês
- **Arquivos Python**: snake_case (`cost_tracker.py`, `accent_checker.py`)
- **Comandos CLI**: kebab-case (`create-module`, `run-step`, `cost-report`)
- **HTTP**: httpx async para todas as chamadas LLM (sem SDKs oficiais)
- **Models**: Pydantic v2 para domínio, dataclass para infraestrutura
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
