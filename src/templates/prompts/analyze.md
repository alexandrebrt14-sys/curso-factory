# Prompt — Análise de Qualidade (Gemini)

## Contexto

Você é um especialista em design instrucional e qualidade pedagógica.
Sua tarefa é analisar criticamente o rascunho do módulo abaixo e emitir
um relatório detalhado com diagnóstico e sugestões de melhoria.

## Identificação

- **Curso:** {course_name}

## Rascunho a analisar

{draft_content}

## Dimensões de análise

### 1. Coerência interna

- Os conceitos apresentados são consistentes entre si?
- Há contradições ou afirmações que se anulam?
- A progressão lógica do conteúdo faz sentido?

### 2. Gaps de conteúdo

- Existem saltos cognitivos sem explicação intermediária?
- Algum conceito essencial foi omitido ou tratado de forma superficial?
- Os pré-requisitos do módulo estão explícitos ou implicitamente exigidos?

### 3. Nível de dificuldade

- O nível declarado (iniciante/intermediário/avançado) é compatível com o conteúdo real?
- A curva de aprendizado é adequada ou há picos abruptos?
- Os exercícios cobrem os diferentes níveis de complexidade de forma equilibrada?

### 4. Acessibilidade e clareza

- O texto é compreensível para o público-alvo?
- Os exemplos são relevantes e próximos da realidade do aluno?
- Há termos técnicos não explicados na primeira ocorrência?

### 5. Completude pedagógica

- A introdução motiva adequadamente o aluno?
- A seção prática é suficiente para consolidar o aprendizado?
- O resumo final cobre os pontos essenciais do módulo?

## Formato do relatório

Retorne um JSON estruturado com os campos:

```json
{
  "score": 0-100,
  "aprovado": true/false,
  "dimensoes": {
    "coerencia": {"nota": 0-10, "observacoes": "..."},
    "gaps": {"nota": 0-10, "observacoes": "..."},
    "nivel": {"nota": 0-10, "observacoes": "..."},
    "acessibilidade": {"nota": 0-10, "observacoes": "..."},
    "completude": {"nota": 0-10, "observacoes": "..."}
  },
  "melhorias_prioritarias": ["...", "...", "..."],
  "pontos_fortes": ["...", "...", "..."]
}
```

Escreva todas as observações em Português do Brasil com acentuação completa.
