# curso-factory

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![5 LLMs](https://img.shields.io/badge/LLMs-5_orquestrados-0176d3)
![Quality Gate](https://img.shields.io/badge/Quality_Gate-4_camadas-green)
![Multi-tenant](https://img.shields.io/badge/multi--tenant-ClientContext-8e44ad)
![PT-BR](https://img.shields.io/badge/idioma-PT--BR_acentuado-yellow)

---

## O que é

O curso-factory é uma fábrica de cursos educacionais de altíssima qualidade, construída sobre um pipeline de 5 LLMs orquestrados. O sistema recebe a definição de um curso em YAML, executa um pipeline de 5 etapas (pesquisa, redação, análise, classificação, revisão) e entrega módulos completos, validados e prontos para deploy.

O padrão editorial do cliente padrão (`default`) segue o nível de publicações como **Harvard Business Review**, **MIT Sloan Management Review** e **HSM Management** — com profundidade analítica real, dados e evidências, formatação rica (tabelas, blocos de citação, hierarquia de títulos) e conformidade com os 6 princípios da andragogia de Malcolm Knowles. Cada cliente pode configurar o próprio padrão via `config/clients/<id>/client.yaml`.

Todos os cursos são gerados com dados atualizados, passam por **validação automática em 4 camadas** (acentuação com auto-correção, qualidade de conteúdo, links e voice guard) antes de serem aprovados para publicação.

## Multi-cliente (multi-tenancy)

A curso-factory nasceu para a Brasil GEO (Alexandre Caramaschi), mas foi refatorada para ser **replicável**. Toda variação entre clientes — autor, domínio, branding, padrão editorial, voice guard rules — está consolidada em `config/clients/<id>/client.yaml`.

```bash
# Lista clientes configurados
python cli.py clients

# Gera curso sob o cliente default (Alexandre/Brasil GEO)
python cli.py create "Meu Curso"

# Gera curso sob outro cliente
python cli.py create "Meu Curso" --client minhaempresa
```

Para adicionar um novo cliente em 3 passos, consulte o playbook em [docs/MULTI-CLIENT.md](docs/MULTI-CLIENT.md).

---

## Problema que resolve

### 1. Conteúdo superficial e genérico

LLMs sem orientação forte produzem conteúdo tipo "blog post" — superficial, cheio de clichês ("nos dias de hoje", "é fundamental que") e sem dados. O curso-factory usa **prompts externos de alta densidade** (~150 linhas cada, em `src/templates/prompts/`) que forçam profundidade analítica, evidências, tabelas comparativas, exercícios situados em contextos profissionais reais e verbos de Bloom de nível superior nos objetivos de aprendizagem.

### 2. Acentuação PT-BR inconsistente

LLMs frequentemente produzem texto em português sem acentos ("producao" em vez de "produção"). O curso-factory implementa **barreira quádrupla**:
1. Instrução no prompt do redator (GPT-4o) com tabela de 150+ palavras obrigatórias
2. Detecção no analisador (Gemini) que reporta cada erro
3. Correção na revisão final (Claude) com checklist exaustivo
4. **Auto-correção programática** (`accent_checker.py`) com 300+ mapeamentos que corrige automaticamente antes do deploy, preservando URLs, código e variáveis

### 3. Heredocs gigantes que quebram no shell

Scripts que embutem HTML ou Markdown em heredocs dentro de shell scripts quebram com caracteres especiais, aspas e acentos. O curso-factory usa **templates Jinja2 em arquivos separados** (`src/templates/`), eliminando completamente heredocs do pipeline de geração.

### 4. Scripts de substituição frágeis

Scripts Python que fazem `str.replace()` ou regex para inserir conteúdo em pontos específicos de um arquivo erram o ponto de inserção quando o template muda. A solução é **geração atômica com validação automática**: cada módulo é gerado inteiro a partir do template, nunca por inserção parcial.

### 5. Falta de validação de qualidade de conteúdo

Sem validação, módulos podem ser publicados sem tabelas, sem exercícios, sem princípios andragógicos ou com clichês proibidos. O **content_checker.py** valida automaticamente: presença de tabelas, contagem de palavras (2.500-4.000), hierarquia de títulos, blocos de citação, exercícios (mínimo 3), verbos de Bloom, princípios de Knowles e clichês proibidos.

### 6. Agentes falhando por API

Chamadas a APIs de LLMs falham por rate limiting, timeout ou indisponibilidade. O curso-factory implementa **circuit breaker**, **retry com backoff exponencial** e **fallback entre LLMs** — se o GPT-4o falha, Claude assume a redação; se Perplexity cai, Gemini faz a pesquisa.

### 7. FinOps ineficiente

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
                   (5 camadas de validação)
                        |
                   +----+----+----+----+----+
                   | Ac | Co | Fm | Lk | Ht |
                   +----+----+----+----+----+
                   Ac=Acentos (auto-fix) Co=Conteúdo Fm=Formatação
                   Lk=Links Ht=HTML

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
| **2. DRAFT** | OpenAI | gpt-4o | Redige módulos com padrão editorial HSM/HBR/MIT Sloan | Melhor redator longo em PT-BR, consistência de tom |
| **3. ANALYZE** | Google | gemini-2.5-pro | Revisa qualidade pedagógica, andragogia, formatação, acentuação | Análise profunda e estruturada com alto contexto |
| **4. CLASSIFY** | Groq | llama-3.3-70b | Classifica nível, tags, pré-requisitos, duração estimada | Latência ultra-baixa para classificação rápida |
| **5. REVIEW** | Anthropic | claude-opus-4-6 | Revisão final: acentuação PT-BR, qualidade editorial, formatação | Melhor em instruções complexas e revisão crítica |

### Prompts externos de alta densidade

Cada agente carrega seu prompt de um arquivo Markdown externo em `src/templates/prompts/`:

| Arquivo | Linhas | Conteúdo |
|---------|--------|----------|
| `research.md` | ~70 | Categorias de pesquisa, fontes prioritárias, formato de saída com nível de confiança |
| `draft.md` | ~200 | Estrutura obrigatória do módulo (6 seções), andragogia detalhada, verbos de Bloom, tabela de acentuação, exemplos de profundidade, autoavaliação |
| `analyze.md` | ~110 | 7 dimensões de análise com critérios, tabela andragógica, formato JSON de saída |
| `classify.md` | ~80 | 6 classificações obrigatórias, formato JSON padronizado |
| `review.md` | ~160 | Tabela de 150+ palavras para correção, checklist editorial, correção ativa (não apenas comentários) |

Os agentes carregam automaticamente o prompt externo. Se o arquivo não existir, usam um template inline como fallback.

---

## Pipeline de criação

### Etapa 1 — Pesquisa (Perplexity)

O agente pesquisador recebe o tópico do módulo e coleta:
- Dados atualizados de 2026 com fontes citáveis e nível de confiança
- Tendências de mercado e tecnologia com dados quantitativos
- Análise competitiva de 5+ cursos concorrentes em tabela
- 3-5 estudos de caso reais e verificáveis para exercícios

### Etapa 2 — Redação (GPT-4o)

O agente redator recebe os dados da pesquisa e gera módulos com:
- **Abertura com impacto** (dado surpreendente, caso real ou pergunta provocativa)
- **Objetivos de aprendizagem** com verbos de Bloom nível 3+ (aplicar, analisar, avaliar, criar)
- **Fundamentação conceitual** com evidências, dados e analogias sofisticadas
- **Estudo de caso** estruturado (Contexto → Desafio → Abordagem → Resultado → Lições)
- **Tabela comparativa** obrigatória (mínimo 1 por módulo)
- **3+ exercícios práticos** com contexto profissional, critérios de avaliação e progressão Bloom
- **Síntese executiva** com checklist de aplicação imediata

### Etapa 3 — Análise (Gemini)

O agente analista revisa o rascunho em 7 dimensões:
- Coerência e rigor intelectual (profundidade vs. superficialidade)
- Qualidade editorial (tom, clichês, parágrafos)
- Formatação visual (tabelas, hierarquia, negrito, citações)
- Conformidade andragógica (6 princípios de Knowles, nota por princípio)
- Gaps de conteúdo (saltos cognitivos, omissões)
- Exercícios (contexto profissional, Bloom, critérios)
- Acentuação PT-BR (lista de todas as palavras sem acento)

### Etapa 4 — Classificação (Groq)

O agente classificador atribui metadados estruturados:
- Nível com justificativa
- Tags temáticas (5-10)
- Pré-requisitos com nível esperado
- Duração estimada por módulo e total
- Categoria e perfil do público-alvo

### Etapa 5 — Revisão (Claude)

O agente revisor faz a passada final com **correção ativa** (não apenas comentários):
- Correção de acentuação PT-BR com tabela de 150+ palavras
- Reescrita de parágrafos superficiais com dados e análise
- Eliminação de clichês proibidos
- Adição de tabelas onde faltam
- Verificação e correção de exercícios
- Validação de princípios andragógicos

---

## Quality Gate — 4 Camadas de Validação + FinOps

O quality gate é a barreira final antes da publicação. Nenhum conteúdo é aprovado sem passar por todas as 4 camadas bloqueantes (+ FinOps como guarda pré-execução e HTML como camada opcional para conteúdo renderizado):

### Camada 1: Acentuação PT-BR (com auto-correção)

| Capacidade | Detalhe |
|------------|---------|
| Dicionário | 300+ mapeamentos (palavras sem acento → forma correta) |
| Auto-correção | `fix_accents()` corrige automaticamente, preservando capitalização |
| Proteção | Ignora URLs, blocos de código, slugs, variáveis, tags HTML, Markdown links |
| Detecção de blocos de código | Rastreia ``` para não alterar código |
| Relatório | Lista cada erro com linha, palavra errada, correção e contexto |

### Camada 2: Qualidade de Conteúdo (`content_checker.py`)

| Verificação | Critério | Tipo |
|-------------|----------|------|
| Contagem de palavras | 2.500-4.000 por módulo | Bloqueante |
| Tabelas | Mínimo 1 por módulo | Bloqueante |
| Subtítulos | Mínimo 5-7 seções (H2/H3) | Bloqueante |
| Hierarquia de títulos | Sem pulos (H2→H4 proibido) | Bloqueante |
| Blocos de citação | Ao menos 1 para insights centrais | Bloqueante |
| Exercícios | Mínimo 3 com contexto profissional | Bloqueante |
| Clichês proibidos | 18 expressões banidas | Bloqueante |
| Verbos de Bloom | Nível 3+ nos objetivos (proibido: "entender", "conhecer") | Bloqueante |
| Princípios andragógicos | 5 indicadores de Knowles verificados | Bloqueante (3+ ausentes) |
| Parágrafos longos | Máximo 5 linhas | Aviso |
| Emojis | Proibidos em todo conteúdo | Bloqueante |
| Termos em negrito | Mínimo 3 por módulo | Aviso |

### Camada 3: Links

- Detecção de acentos em URLs (bloqueante — incidente 2026-03-27: 55 hrefs corrompidos)
- Verificação de links internos

### Camada 4: Voice Guard (padrão editorial por cliente)

Barreira programática que bate o texto contra o `voice_guard` do `ClientContext` ativo. Score 0-100 em 4 dimensões ponderadas:

| Dimensão | Peso | O que mede |
|----------|------|------------|
| Anti-clichê editorial | 30 | 18 expressões proibidas ("nos dias de hoje", "é fundamental que", ...) |
| Bloom + andragogia | 30 | Verbos Bloom nível 3+ nos objetivos; bonus por ≥3 verbos aceitos |
| Naming canônico | 25 | Empresa/fundador canônicos vs. títulos/domínios/nomes proibidos do cliente |
| Estilo HBR/MIT Sloan | 15 | Sem disclaimers de IA, sem aberturas retóricas, parágrafos curtos |

Score < `min_score` (padrão 70) **ou** qualquer erro crítico (título inventado, domínio alucinado, nome errado da empresa) → `aprovado = False`. Configurável por cliente em `config/clients/<id>/client.yaml` → `voice_guard:`.

### Camada opcional: HTML (apenas para conteúdo renderizado)

- Fechamento de tags
- Elementos obrigatórios (meta charset, title, main, h1)
- Acessibilidade (lang, alt em imagens)

### Guarda de FinOps (pré-execução)

- Budget guard: $5 max Claude, $10 max total por curso
- Cache obrigatório: SHA-256, TTL 24h
- Pricing, endpoints e fallback entre providers em `config/providers.yaml`

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

1. **Necessidade de saber** — cada módulo abre explicando POR QUE o conhecimento é necessário, com dados quantitativos sobre o impacto
2. **Autoconceito** — o aluno é tratado como profissional autônomo, nunca de forma condescendente. Verbos: "considere", "analise", "avalie" (nunca "vamos aprender")
3. **Experiência prévia** — conceitos novos se conectam com vivências profissionais do aluno: "Se você já enfrentou...", "Na sua rotina profissional..."
4. **Prontidão** — demonstração de aplicabilidade imediata no contexto de trabalho: "aplique hoje", "na próxima reunião"
5. **Orientação a problemas** — conteúdo organizado em torno de problemas reais, não taxonomias abstratas. Comece com o problema, depois a solução.
6. **Motivação intrínseca** — aprendizado conectado com crescimento profissional e domínio

### Taxonomia de Bloom nos Objetivos

Objetivos de aprendizagem devem usar EXCLUSIVAMENTE verbos de nível 3-6:

| Nível | Verbos Aceitos | Exemplo |
|-------|---------------|---------|
| 3 - Aplicar | aplicar, implementar, executar, demonstrar, calcular | "Implementar um pipeline de dados com validação automática" |
| 4 - Analisar | analisar, comparar, diferenciar, diagnosticar, categorizar | "Diagnosticar gargalos de performance usando métricas de latência" |
| 5 - Avaliar | avaliar, justificar, priorizar, recomendar, defender | "Avaliar trade-offs entre consistência eventual e forte" |
| 6 - Criar | criar, projetar, formular, propor, desenvolver | "Projetar um plano de migração incremental com rollback" |

**Proibidos** (níveis 1-2, superficiais): entender, conhecer, saber, compreender, lembrar, memorizar, listar, descrever, identificar.

### Formatação Rica

Cada módulo inclui obrigatoriamente:

- **Tabelas comparativas** (ao menos uma por módulo): comparações, frameworks, antes/depois, matrizes de decisão
- **Listas numeradas** para processos sequenciais, **com marcadores** para enumerações
- **Hierarquia clara** de títulos (H2 > H3 > H4, sem pulos)
- **Negrito** para termos-chave na primeira ocorrência
- **Blocos de citação (>)** para insights centrais e conceitos memoráveis
- **Exercícios** com progressão de complexidade (Taxonomia de Bloom), contexto profissional real e critérios de avaliação

### Expressões Proibidas

O pipeline detecta e bloqueia automaticamente:

| Clichê Proibido | Substituição |
|-----------------|-------------|
| "nos dias de hoje" | Use o ano específico ou período |
| "é fundamental que" | Vá direto ao ponto |
| "não é segredo que" | Comece pela informação |
| "o futuro é agora" | Elimine |
| "em um mundo cada vez mais" | Seja específico |
| "vamos explorar" | Elimine |
| "como sabemos" | Cite a fonte |
| "é importante ressaltar" | Ressalte diretamente |
| "vale a pena destacar" | Destaque diretamente |

### Acentuação PT-BR — Barreira Quádrupla

O pipeline possui 4 barreiras contra palavras sem acento:

1. **Instrução ao redator (GPT-4o)**: prompt com tabela de palavras obrigatoriamente acentuadas
2. **Análise de qualidade (Gemini)**: detecta e reporta palavras sem acento no relatório
3. **Revisão final (Claude)**: corrige todas as ocorrências com tabela de 150+ palavras
4. **Auto-correção programática (accent_checker.py)**: barreira pré-deploy com 300+ mapeamentos, preservação de contexto (URLs, código, variáveis) e correção automática

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
│   ├── llm_client.py         # Cliente HTTP unificado com circuit breaker
│   ├── cost_tracker.py       # Rastreamento de custos em tempo real
│   ├── cache.py              # Cache de resultados (SHA-256, TTL 24h)
│   ├── agents/
│   │   ├── base.py           # Classe base com carregamento de prompt externo
│   │   ├── researcher.py     # Perplexity — pesquisa
│   │   ├── writer.py         # GPT-4o — redação
│   │   ├── analyzer.py       # Gemini — análise de qualidade
│   │   ├── classifier.py     # Groq — classificação
│   │   ├── reviewer.py       # Claude — revisão final
│   │   └── pipeline.py       # Orquestração em waves paralelas
│   ├── templates/
│   │   ├── layout.tsx.j2     # Template Jinja2 para layout Next.js
│   │   ├── page.tsx.j2       # Template para página interativa do curso
│   │   └── prompts/          # Prompts externos de alta densidade
│   │       ├── research.md   # (~70 linhas) Pesquisa e fundamentação
│   │       ├── draft.md      # (~200 linhas) Redação com andragogia e Bloom
│   │       ├── analyze.md    # (~110 linhas) Análise de qualidade 7D
│   │       ├── classify.md   # (~80 linhas) Classificação e metadados
│   │       └── review.md     # (~160 linhas) Revisão e correção ativa
│   ├── generators/
│   │   ├── schema_builder.py # Builds CourseDefinition from pipeline output
│   │   ├── metadata_sync.py  # Emits output/course_catalog.json (consumed externally, never writes to landing-page-geo)
│   │   └── build_validator.py # TSX build validation + syntax check
│   ├── schemas/
│   │   └── course.schema.json # JSON Schema para CourseDefinition
│   └── validators/
│       ├── accent_checker.py  # 300+ mapeamentos, detecção + auto-correção
│       ├── content_checker.py # Tabelas, exercícios, Bloom, andragogia, clichês
│       ├── html_validator.py  # Tags, acessibilidade, semântica
│       ├── link_checker.py    # Acentos em URLs, links internos
│       └── quality_gate.py    # Gate unificado de 5 camadas com auto-fix
├── tests/
│   ├── fixtures/sample_course.json
│   └── test_generators.py
├── docs/
│   └── FINOPS.md             # Documentação de custos e budget guard
└── output/
    ├── drafts/               # Rascunhos em progresso
    ├── approved/             # Aprovados pelo quality gate
    └── deployed/             # Deployados em produção
```

---

## Documentação

| Documento | Quando ler |
|-----------|-----------|
| [docs/MULTI-CLIENT.md](docs/MULTI-CLIENT.md) | Adicionar um novo cliente (empresa, nicho, autor). Inclui playbook passo-a-passo, campos de `client.yaml` e integração com QualityGate. |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Entender o pipeline interno (orchestrator, agents, validators, generators) e onde encaixar mudanças. |
| [docs/FINOPS.md](docs/FINOPS.md) | Pricing, cost tracking, budget guard, análise de custos por curso. |
| [docs/knowledge/geo-aeo/README.md](docs/knowledge/geo-aeo/README.md) | **Base de conhecimento GEO/AEO/Agentic Commerce.** Síntese de 25+ papers (2025–2026) em 30 instruções operacionais, 7 princípios mestres, checklists e thresholds quantitativos. Camada doutrinária dos 5 LLMs do pipeline. |
| [CLAUDE.md](CLAUDE.md) | Convenções, regras editoriais e decisões históricas — usado como contexto pelo Claude Code quando trabalha no repo. |

---

## Convenções

- **Idioma do conteúdo**: Português do Brasil com acentuação completa (enforced por 4 barreiras)
- **Idioma do código**: Inglês
- **Padrão editorial (cliente default)**: HSM Management + Harvard Business Review + MIT Sloan Management Review
- **Andragogia**: 6 princípios de Knowles aplicados e validados automaticamente
- **Bloom**: Verbos nível 3-6 nos objetivos (aplicar, analisar, avaliar, criar)
- **Arquivos Python**: snake_case (`cost_tracker.py`, `accent_checker.py`)
- **Comandos CLI**: kebab-case (`create-module`, `run-step`, `cost-report`)
- **HTTP**: httpx para todas as chamadas LLM (sem SDKs oficiais)
- **Models**: Pydantic v2 para domínio, dataclass para infraestrutura
- **Cache**: SHA-256 do input como chave, TTL 24h, em `output/.cache/`
- **Custos**: registrados por chamada em `output/cost_history.jsonl`
- **Templates**: Jinja2 para HTML/TSX, Markdown para prompts
- **Prompts**: Arquivos externos em `src/templates/prompts/`, carregados automaticamente pelos agentes
- **Sem emojis**: proibido em todo conteúdo de curso e documentação

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
