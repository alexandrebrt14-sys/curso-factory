# Prompt: análise de qualidade pedagógica (Gemini)

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
- Cada parágrafo tem uma ideia central desenvolvida até terminar? Reprove os dois extremos: o bloco que empilha dois assuntos e a sequência de parágrafos de uma frase que fatia um único raciocínio.
- O ritmo dos períodos acompanha o argumento? Verifique num bloco de dez frases: diferença menor que 15 palavras entre a mais longa e a mais curta indica uniformidade de máquina; sequência de frases curtas de enchimento, uma por parágrafo, indica o defeito oposto (staccato de manchete). Nenhum dos dois é aceitável, e nenhuma cota de comprimento deve ser recomendada na correção.
- O texto está livre de travessão como recurso estilístico, de antítese em série ("não é X, é Y"), de tríade usada como ritmo e de conclusão-espelho?

### 2.5. Substância e narrativa (dimensão de aprovação, não de rejeição)

Esta dimensão pergunta o que o módulo TEM, e não apenas o que ele evitou. Um texto curto, uniforme e sem argumento passa em todos os gates automáticos do repositório, porque nenhum deles mede substância. Você é a camada que mede.

Avalie e pontue:

- **Tese própria**: o módulo defende uma posição identificável, ou é uma compilação neutra do que já existe? Aponte a frase que carrega a tese; se não houver, a nota desta dimensão não passa de 4.
- **Evidência que sustenta a tese**: os dados citados sustentam o argumento defendido, ou apenas decoram o texto com números soltos?
- **Information gain**: há pelo menos um dado, exemplo brasileiro, comparação ou framework que o aluno não encontraria nas três primeiras páginas de qualquer busca sobre o tema?
- **Abertura**: o módulo abre em situação concreta com tensão explícita (caso, decisão difícil, número que contraria a expectativa), ou abre em definição e cenário genérico?
- **Caso condutor**: existe um caso nomeado que atravessa o módulo e reaparece na fundamentação e nos exercícios, ou os exemplos são avulsos?
- **Promessa cumprida**: o que a abertura prometeu foi entregue no desenvolvimento?
- **Fechamento**: a síntese mostra o que mudou no caso ou na tensão inicial, ou apenas repete o que já foi dito?
- **Critério de decisão**: quando o módulo apresenta alternativas, ele compara com critérios explícitos e recomenda com justificativa, ou lista opções sem ajudar a escolher?

Referência normativa das duas dimensões acima: `DIRETRIZ_EDITORIAL.md`, seções 2, 3, 4 e 6.

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
    "substancia_narrativa": {
      "nota": 0-10,
      "tese_identificada": "frase que carrega a tese, ou null se ausente",
      "information_gain": "o que o módulo traz que não está em qualquer fonte, ou null",
      "abertura_em_situacao": true/false,
      "caso_condutor": "nome do caso que atravessa o módulo, ou null",
      "promessa_cumprida": true/false,
      "fechamento_com_callback": true/false,
      "observacoes": "..."
    },
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
