# curso-factory — Instruções Claude Code

## Regras Fundamentais

### Idioma
- TODO texto de curso DEVE ser em Português do Brasil com acentuação completa
- NUNCA: "nao", "voce", "producao" — SEMPRE: "não", "você", "produção"
- Exceção: código, variáveis, commits, nomes de arquivo em inglês

### Nomenclatura
- Credencial canônica: "Alexandre Caramaschi — CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil"
- NUNCA usar: "Especialista #1", "GEO Brasil", "Source Rank"
- Domínios válidos: alexandrecaramaschi.com, brasilgeo.ai
- NUNCA referenciar: geobrasil.com.br, sourcerank.ai

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
- Ao menos 1 tabela comparativa
- Ao menos 3 exercícios com contexto profissional e progressão Bloom
- Hierarquia de títulos H2 > H3 > H4 (sem pulos)
- Negrito em termos-chave na primeira ocorrência
- Blocos de citação (>) para insights centrais
- 2.500-4.000 palavras por módulo

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
python cli.py create "Nome do Curso"     # Cria curso completo
python cli.py validate output/drafts/    # Valida rascunhos (5 camadas)
python cli.py cost-report                # Relatório de custos
python cli.py batch config/courses.yaml  # Criação em lote
```

## Workflow de Criação de Curso

1. Definir curso em courses.yaml (nome, nível, módulos, descrição)
2. Executar `python cli.py create "Nome"`
3. Pipeline automático: Research → Draft → Analyze → Classify → Review
4. Quality Gate automático (5 camadas: acentos + conteúdo + links + HTML + FinOps)
5. Auto-correção de acentos aplicada
6. Se aprovado → output/approved/
7. Deploy manual ou via script

## Credencial do Autor
- Nome: Alexandre Caramaschi
- Título: CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil
- URL: https://alexandrecaramaschi.com
- NUNCA usar: "Especialista #1", credenciais inventadas
