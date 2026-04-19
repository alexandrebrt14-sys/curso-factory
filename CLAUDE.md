# curso-factory — Instruções Claude Code

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

## Regras Fundamentais

### Idioma
- TODO texto de curso DEVE ser em Português do Brasil com acentuação completa
- NUNCA: "nao", "voce", "producao" — SEMPRE: "não", "você", "produção"
- Exceção: código, variáveis, commits, nomes de arquivo em inglês

### Nomenclatura (cliente `default`)
- Credencial canônica: "Alexandre Caramaschi — CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil"
- NUNCA usar: "Especialista #1", "GEO Brasil", "Source Rank"
- Domínios válidos: alexandrecaramaschi.com, brasilgeo.ai
- NUNCA referenciar: geobrasil.com.br, sourcerank.ai

**Importante:** essas regras valem para o cliente `default`. Ao trabalhar com outro cliente (`--client <id>`), as regras de naming vêm do `config/clients/<id>/client.yaml`. Não misture: jamais hardcode credencial Alexandre no código — tudo passa pelo `ClientContext`.

### Sem Emojis
- Proibido emojis em qualquer conteúdo de curso ou documentação

## Arquitetura do Pipeline

5 LLMs com papéis fixos — NÃO interpretar como sub-agentes do Claude Code:
1. Perplexity (sonar-pro) → pesquisa, fundamentação acadêmica e análise competitiva
2. GPT-4o → redação de módulos com padrão editorial HSM/HBR/MIT Sloan e andragogia
3. Gemini (2.5-pro) → análise de qualidade pedagógica e andragógica em 7 dimensões
4. Groq (Llama 3.3) → classificação, tags e metadados
5. Claude (opus-4-6) → revisão final com correção ativa: acentuação PT-BR, qualidade editorial, formatação ($5 max/curso)

### Prompts Externos (IMPORTANTE)
- Os prompts dos 5 agentes ficam em `src/templates/prompts/*.md`
- Os agentes em `src/agents/` carregam automaticamente o prompt externo via `base.py`
- Para alterar o comportamento de um agente, edite o arquivo .md correspondente
- Se o arquivo .md não existir, o agente usa o TEMPLATE inline como fallback
- NUNCA duplicar instruções entre o prompt externo e o template inline

## Padrão Editorial — Regras de Qualidade

### Estilo HSM/HBR/MIT Sloan
- Tom analítico, direto, orientado por dados, sem jargão vazio
- Frases curtas. Parágrafos de 2-3 frases (máximo 5 linhas). Sem floreios
- Dados e estatísticas para sustentar argumentos — nunca afirmar sem evidência
- Evitar superlativos sem evidência ("o melhor", "revolucionário")

### Andragogia (6 Princípios de Knowles) — OBRIGATÓRIO
1. Necessidade de saber — POR QUE antes do COMO
2. Autoconceito — profissional autônomo, nunca condescendente
3. Experiência prévia — conectar com vivências profissionais
4. Prontidão — aplicabilidade imediata no trabalho
5. Orientação a problemas — problemas reais, não taxonomias
6. Motivação intrínseca — crescimento profissional e domínio

### Taxonomia de Bloom nos Objetivos
- ACEITOS (nível 3-6): analisar, comparar, diagnosticar, avaliar, justificar, criar, projetar, aplicar, implementar
- PROIBIDOS (nível 1-2): entender, conhecer, saber, compreender, lembrar, memorizar, listar, descrever, identificar

### Formatação Obrigatória por Módulo
- Ao menos 1 tabela comparativa (formato markdown com pipes)
- Ao menos 3 exercícios com contexto profissional e progressão Bloom
- Sub-headings (linha terminando com `:`) a cada 2-3 parágrafos
- Negrito em termos-chave na primeira ocorrência usando `**termo**`
- Blockquotes (`> `) para insights centrais — ao menos 1-2 por módulo
- Bullets com `-- ` (dois hífens), NUNCA `- ` (um hífen)
- Nunca mais de 3 parágrafos seguidos sem elemento visual
- 2.500-4.000 palavras por módulo

### Padrão de Layout (FormattedText — UX Microsoft Learn + Salesforce Trailhead)
O template `page.tsx.j2` inclui um componente `FormattedText` que renderiza:
- `**bold**` → `<strong>` com font-semibold
- Linha terminando com `:` → `<h4>` sub-heading com border-bottom
- `-- item` → bullet list com dot azul (accent color)
- `1. item` → ordered list com número azul
- `| col | col |` → `<table>` com header uppercase e zebra striping
- `> texto` → blockquote com borda lateral azul
- Parágrafos → text-justify com leading-[1.75]
- Warning/tip/checkpoint → text-justify aplicado

### Expressões Proibidas
- "nos dias de hoje", "é fundamental que", "não é segredo que"
- "o futuro é agora", "em um mundo cada vez mais", "vamos explorar"
- "como sabemos", "é importante ressaltar", "vale a pena destacar"
- "grosso modo", "vamos aprender", "agora você vai entender"

## Quality Gate — 5 Camadas de Validação

### Camada 1: Acentuação (accent_checker.py)
- 300+ mapeamentos de palavras sem acento → forma correta
- `check_accents()`: detecta erros com linha, palavra e contexto
- `fix_accents()`: corrige automaticamente, preservando URLs/código/variáveis
- Rastreamento de blocos de código (```) para não alterar código

### Camada 2: Conteúdo (content_checker.py)
- Contagem de palavras (2.500-4.000)
- Presença de tabelas (mínimo 1 por módulo)
- Hierarquia de títulos sem pulos
- Blocos de citação para insights
- Exercícios (mínimo 3)
- Clichês proibidos (18 expressões)
- Verbos de Bloom nos objetivos
- Princípios andragógicos (5 indicadores)
- Parágrafos longos (máximo 5 linhas)
- Emojis (proibidos)

### Camada 3: Links (link_checker.py)
- Acentos em URLs = ERRO CRÍTICO (incidente 2026-03-27: 55 hrefs corrompidos)
- Verificação de links internos

### Camada 4: HTML (html_validator.py)
- Fechamento de tags, elementos obrigatórios, acessibilidade

### Camada 5: FinOps (cost_tracker.py)
- Budget guard: $5 max Claude, $10 max total por curso
- Cache obrigatório: SHA-256, TTL 24h

### Auto-correção de Acentos
- O quality gate (`auto_fix=True` por padrão) corrige acentos automaticamente
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
- Budget guard ativo: $5 max Claude, $10 max total por curso
- Cache obrigatório — nunca reprocessar conteúdo já aprovado
- Verificar custo antes de executar pipeline completo
- API keys: fonte de verdade em geo-orchestrator/.env

## Estrutura de Arquivos

- config/courses.yaml — definição dos cursos
- config/quality_rules.yaml — regras de qualidade
- src/agents/ — um agente por LLM (carrega prompt de templates/prompts/)
- src/templates/prompts/ — prompts externos de alta densidade (.md)
- src/templates/ — templates Jinja2 para TSX (NUNCA heredoc)
- src/validators/ — 5 validadores (acentos, conteúdo, HTML, links, quality gate)
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
```

## Workflow de Criação de Curso

1. Definir curso em courses.yaml (nome, nível, módulos, descrição)
2. Executar `python cli.py create "Nome"`
3. Pipeline automático: Research → Draft → Analyze → Classify → Review
4. Quality Gate automático (5 camadas: acentos + conteúdo + links + HTML + FinOps)
5. Auto-correção de acentos aplicada
6. Se aprovado → output/approved/
7. Deploy manual ou via script

## Credencial do Autor (cliente `default`)
- Nome: Alexandre Caramaschi
- Título: CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil
- URL: https://alexandrecaramaschi.com
- NUNCA usar: "Especialista #1", credenciais inventadas

**Para outro cliente:** consulte `config/clients/<id>/client.yaml` → seção `author:` e `voice_guard.canonical:`. O voice guard bloqueia textos que violem o naming canônico do cliente ativo.
