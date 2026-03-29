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
3. Gemini (2.5-pro) → análise de qualidade pedagógica e andragógica
4. Groq (Llama 3.3) → classificação, tags e metadados
5. Claude (opus-4-6) → revisão final: acentuação PT-BR, qualidade editorial, formatação ($5 max/curso)

## Regras Anti-Retrabalho

### NUNCA usar heredocs para conteúdo grande
- Heredocs >50 linhas QUEBRAM no shell
- SEMPRE usar templates Jinja2 em src/templates/
- SEMPRE gerar arquivos via Python (Write tool ou script)

### NUNCA usar scripts de substituição por regex
- Scripts que leem template e substituem trechos são FRÁGEIS
- Se o ponto de inserção mudar, o script falha silenciosamente
- SEMPRE gerar o arquivo completo de uma vez (geração atômica)

### Validação ANTES de deploy
- Rodar accent_checker.py em todo conteúdo PT-BR
- Rodar html_validator.py em toda página HTML
- Rodar link_checker.py em todos os hrefs
- Se qualquer validador falhar, NÃO fazer deploy

### FinOps
- Budget guard ativo: $5 max Claude, $10 max total por curso
- Cache obrigatório — nunca reprocessar conteúdo já aprovado
- Verificar custo antes de executar pipeline completo
- API keys: fonte de verdade em geo-orchestrator/.env
- Geração de TSX via Jinja2 templates (NUNCA string replace)
- Validação automática: acentos + build + JSON Schema

## Estrutura de Arquivos

- config/courses.yaml — definição dos cursos
- config/quality_rules.yaml — regras de qualidade
- src/agents/ — um agente por LLM
- src/templates/ — templates Jinja2 (NUNCA heredoc)
- src/templates/prompts/ — prompts separados por arquivo
- src/validators/ — validadores automáticos
- output/drafts/ — rascunhos
- output/approved/ — aprovados
- output/deployed/ — em produção
- src/generators/ — geradores de TSX (Jinja2, schema builder, metadata sync, build validator)
- src/schemas/ — JSON Schema para CourseDefinition
- tests/ — testes unitários dos geradores

## Comandos CLI

```bash
python cli.py create "Nome do Curso"     # Cria curso completo
python cli.py validate output/drafts/    # Valida rascunhos
python cli.py cost-report                # Relatório de custos
python cli.py batch config/courses.yaml  # Criação em lote
```

## Workflow de Criação de Curso

1. Definir curso em courses.yaml (nome, nível, módulos, descrição)
2. Executar `python cli.py create "Nome"`
3. Pipeline automático: Research → Draft → Analyze → Classify → Review
4. Validação automática (acentos, HTML, links)
5. Se aprovado → output/approved/
6. Deploy manual ou via script

## Padrão Editorial de Conteúdo — Regras Permanentes

### Idioma
- TODO conteúdo em Português do Brasil (PT-BR) com acentuação COMPLETA
- Nunca: "nao", "voce", "producao" — Sempre: "não", "você", "produção"
- Exceção: código em inglês, slugs de URL (sempre ASCII)

### Estilo Editorial
- Mesclagem de MIT Sloan Management Review + Harvard Business Review + HSM Management
- Tom: analítico, direto, orientado por dados, sem jargão vazio
- Frases curtas. Parágrafos de 2-3 frases. Sem floreios
- Usar dados e estatísticas para sustentar argumentos
- Evitar superlativos sem evidência ("o melhor", "revolucionário")

### Estrutura Chunkável (para indexação por IA)
- Cada artigo deve ter 5-7 seções semânticas (h2/h3)
- Cada seção deve ser autocontida e compreensível isoladamente
- Incluir pelo menos 1 TABELA comparativa por artigo
- Respostas diretas ao ponto — LLMs priorizam informação concisa
- Usar listas quando comparar 3+ itens

### FAQ Obrigatório
- Cada artigo DEVE terminar com seção de Perguntas Frequentes
- 5-7 perguntas por artigo
- Perguntas devem refletir queries reais de executivos
- Respostas diretas em 2-3 frases (chunkáveis por LLMs)

### Tabelas Obrigatórias
- Cada artigo DEVE ter pelo menos 1 tabela comparativa
- Formato: HTML table com thead/tbody
- Usar para: antes/depois, comparativos, frameworks

### Termos Proibidos
- "Especialista #1", "GEO Brasil" (exceto contexto educacional), "Source Rank"
- Superlativos sem evidência
- Emojis no conteúdo

### Schema e Metadados
- Cada artigo deve ter JSON-LD (Article schema)
- Meta description: 150-160 caracteres
- Keywords: 5-10 termos relevantes
- Canonical URL obrigatória
- OG tags completas

### Credencial do Autor
- Nome: Alexandre Caramaschi
- Título: CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil
- URL: https://alexandrecaramaschi.com
- NUNCA usar: "Especialista #1", credenciais inventadas
