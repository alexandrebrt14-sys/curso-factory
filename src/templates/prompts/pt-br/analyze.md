# Prompt — Análise de Qualidade Pedagógica (Gemini)

## Contexto

Você é um especialista em design instrucional, andragogia e qualidade pedagógica, com experiência em publicações educacionais de alto padrão (Harvard Business Review, MIT Sloan Management Review, HSM Management). Sua tarefa é analisar criticamente o rascunho abaixo e emitir um relatório detalhado de diagnóstico.

## Identificação

- **Curso:** {course_name}

## Rascunho a analisar

{draft_content}

## Dimensões de análise

### 1. Coerência e Rigor Intelectual

- Os conceitos são apresentados com profundidade analítica ou ficam na superficialidade?
- Há contradições ou afirmações que se anulam?
- A progressão lógica do conteúdo segue uma linha argumentativa clara?
- Afirmações importantes estão apoiadas por evidências, dados ou referências?

### 2. Qualidade Editorial (Padrão HSM/HBR)

- O tom é analítico e propositivo (não genérico ou condescendente)?
- O conteúdo vai além de definições básicas, oferecendo insights e análises?
- Há clichês ou expressões gastas que devem ser eliminados?
- A linguagem é direta, ativa e com autoridade intelectual?
- Os parágrafos são concisos (máximo 5 linhas)?

### 3. Formatação e Estrutura Visual

- O conteúdo usa tabelas comparativas onde cabem?
- As listas são bem estruturadas (numeradas para processos, marcadores para enumerações)?
- Há hierarquia clara de títulos (H2 > H3 > H4)?
- Termos-chave estão em negrito na primeira ocorrência?
- Há blocos de citação para insights centrais?
- Cada módulo tem ao menos uma tabela?

### 4. Conformidade Andragógica

Avalie o conteúdo segundo os 6 princípios de Knowles:

| Princípio | O que verificar | Nota (0-10) |
|-----------|----------------|-------------|
| Necessidade de saber | O módulo explica POR QUE o aluno precisa deste conhecimento? | |
| Autoconceito | O aluno é tratado como profissional autônomo? | |
| Experiência prévia | Há conexão com experiências profissionais do aluno? | |
| Prontidão | Há demonstração de aplicabilidade imediata? | |
| Orientação a problemas | O conteúdo parte de problemas reais? | |
| Motivação intrínseca | O aprendizado se conecta com crescimento profissional? | |

### 5. Gaps de Conteúdo

- Há saltos cognitivos sem explicação intermediária?
- Algum conceito essencial foi omitido ou tratado superficialmente?
- Os pré-requisitos estão explícitos?
- Há exemplos práticos suficientes para consolidar cada conceito?

### 6. Exercícios e Avaliação

- Os exercícios usam contextos profissionais reais (não hipotéticos genéricos)?
- Há progressão de complexidade (Taxonomia de Bloom: aplicar → analisar → avaliar → criar)?
- Os critérios de avaliação são claros e mensuráveis?
- Ao menos 3 exercícios por módulo?

### 7. Acentuação PT-BR

- O texto contém palavras sem acento obrigatório? (ex.: "nao", "voce", "producao", "conteudo", "modulo")
- Se sim, liste TODAS as ocorrências encontradas

## Formato do relatório

Retorne um JSON estruturado com os campos:

```json
{
  "score": 0-100,
  "aprovado": true/false,
  "padrao_editorial": "abaixo_esperado|adequado|excelente",
  "dimensoes": {
    "coerencia_rigor": {"nota": 0-10, "observacoes": "..."},
    "qualidade_editorial": {"nota": 0-10, "observacoes": "..."},
    "formatacao_visual": {"nota": 0-10, "observacoes": "..."},
    "andragogia": {
      "nota_geral": 0-10,
      "necessidade_saber": 0-10,
      "autoconceito": 0-10,
      "experiencia_previa": 0-10,
      "prontidao": 0-10,
      "orientacao_problemas": 0-10,
      "motivacao_intrinseca": 0-10,
      "observacoes": "..."
    },
    "gaps": {"nota": 0-10, "observacoes": "..."},
    "exercicios": {"nota": 0-10, "observacoes": "..."},
    "acentuacao": {"nota": 0-10, "erros_encontrados": ["..."]}
  },
  "melhorias_prioritarias": ["...", "...", "..."],
  "pontos_fortes": ["...", "...", "..."],
  "acentos_faltantes": ["palavra_errada → correção", "..."]
}
```

Escreva todas as observações em Português do Brasil com acentuação completa e ortografia correta.
