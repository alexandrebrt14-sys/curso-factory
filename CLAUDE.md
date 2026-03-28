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
1. Perplexity (sonar-pro) → pesquisa e fontes atualizadas
2. GPT-4o → redação de módulos
3. Gemini (2.0-flash) → análise de qualidade
4. Groq (Llama 3.3) → classificação e tags
5. Claude (sonnet-4-6) → revisão final e acentuação

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
- Budget guard ativo — respeitar limites diários por provider
- Cache obrigatório — nunca reprocessar conteúdo já aprovado
- Verificar custo antes de executar pipeline completo
- API keys: fonte de verdade em geo-orchestrator/.env

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
