---
titulo: Checklist — Reescrita TL;DR + BLUF + Corpo + Síntese
versao: 1.0
data: 2026-04-25
tipo: checklist-operacional
uso: aplicado a toda peça de conteúdo longo
---

# Checklist Operacional — Reescrita de Conteúdo Longo

Template editorial reutilizável para conteúdo entre 1.500 e 4.000 palavras. Aplicável a artigos do `alexandrecaramaschi.com`, módulos de curso do `curso-factory`, papers de pesquisa do repo `papers/` e drafts de Newsletter.

---

## Estrutura padrão (Instrução 16)

```
# Título orientativo (6–10 palavras, pergunta ou tese)

**TL;DR:** [3–5 linhas, autocontidas]

## [BLUF — pergunta central respondida em 80–150 palavras]

## [Seção 2 — contexto/dados]
## [Seção 3 — análise/mecanismo]
## [Seção 4 — contra-argumento ou limites]
## [Seção 5 — implicação prática]

## Síntese — o que muda a partir daqui
```

---

## Pré-redação — checklist de diagnóstico

Antes de escrever a primeira linha:

- [ ] Identifiquei a **intenção dominante** (informacional, transacional, navegacional, comparativa) — Instrução 24.
- [ ] Mapeei as **3–5 entidades centrais** (pessoas, empresas, papers) que ancoram o argumento.
- [ ] Listei as **fontes primárias** (links em `50-fontes-e-links.md`) que vou citar.
- [ ] Defini a **plataforma-alvo principal** (Medium / Quora / LinkedIn Newsletter / Substack / próprio site) — Instrução 18.
- [ ] Tenho **pelo menos 3 quotes diretas** atribuíveis disponíveis (pessoa + cargo + organização + data) — Instrução 8.

---

## Durante a redação — checklist progressivo

### TL;DR (3–5 linhas)
- [ ] Autocontido — pode ser citado isolado.
- [ ] Inclui a tese central explicitamente.
- [ ] Sem pronomes referenciais ambíguos.

### BLUF (80–150 palavras)
- [ ] Responde a pergunta central diretamente nas 2 primeiras frases.
- [ ] Indica a intenção com frase-âncora ("Este guia ajuda você a [decidir / comparar / implementar / entender]…").
- [ ] Linka pelo menos 1 fonte primária.

### Seções do corpo (cada uma)
- [ ] Heading responde uma pergunta (não é rótulo genérico como "Introdução") — Instrução 5.
- [ ] Bloco AEO de 40–80 palavras logo após o heading — Instrução 6.
- [ ] Densidade de entidades ≥ 1 a cada 100 palavras — Instrução 17.
- [ ] Densidade de outlinks ≥ 1 a cada 250 palavras — Instrução 7.
- [ ] Razão quote:estatística ≥ 2:1 — Instrução 8.
- [ ] Negrito limitado a 1–3 trechos por seção, máximo 12 palavras cada — Instrução 23.
- [ ] Toda afirmação factual tem fonte verificável — Instrução 25.

### Síntese final
- [ ] **Não repete** o BLUF — conecta a implicações novas.
- [ ] Aponta 1–3 ações práticas que o leitor pode tomar.
- [ ] Encerra com pergunta ou CTA específico para a plataforma.

---

## Pós-redação — varredura anti-IA

Antes de publicar, varredura ativa contra padrões "cara de IA" (já formalizados em `src/templates/prompts/draft.md` do `curso-factory`):

- [ ] Sem "nos dias de hoje", "é fundamental que", "vamos explorar".
- [ ] Sem "no fundo", "no fim, tudo se resume a".
- [ ] Sem "potencializar", "robusto", "estratégico" sem objeto concreto.
- [ ] Sem hedging excessivo ("possivelmente", "em alguma medida").
- [ ] Sem listas decorativas (bullet apenas para informação real).
- [ ] Sem nominalizações em excesso ("implementação" → "implementar").
- [ ] Voz autoral presente — texto não é neutro demais.

Se algum padrão aparecer: reescrever com **concretude, agente explícito e dado específico** ou marcar `[FALTA EVIDÊNCIA: <o que precisa ser buscado>]`.

---

## Pós-redação — varredura GEO

- [ ] Contagem de palavras alinhada à plataforma-alvo (matriz em `32-checklist-publicacao-multi.md`).
- [ ] Headings narram o argumento — alguém lendo só os headings entende a tese.
- [ ] JSON-LD da página foi atualizado (`dateModified` + `keywords` novos).
- [ ] `Article` ou `BlogPosting` com `author.sameAs` apontando para perfis canônicos.

---

## Exemplo — auditoria de um draft

Texto: "GEO 101 — O que mudou em 2026?"

| Item | Status | Nota |
|---|---|---|
| TL;DR autocontido | ✓ | 4 linhas |
| BLUF responde nas 2 primeiras frases | ✓ | OK |
| Headings responsivos | ✗ | "Introdução" → trocar por "Por que GEO 2024 não vale mais em 2026?" |
| Bloco AEO pós-heading | ✓ | OK em 5/5 seções |
| Densidade entidades 1/100 | ✓ | medido 1,2/100 |
| Outlinks 1/250 | ✗ | medido 0,7/250 — adicionar 4 links |
| Razão quote:stat ≥ 2:1 | ✗ | atual 1:1 — remover 3 estatísticas ou adicionar 3 quotes |
| Negrito ≤ 3/seção | ✓ | OK |
| Claims com fonte | ✓ | 100% das afirmações ancoradas |
| Síntese diferenciada | ✓ | aponta 3 ações |
| Anti-IA | ✗ | "potencializar" em 2 lugares — substituir |

→ Reescrever conforme apontamentos antes de publicar.

---

## Integração com o pipeline `curso-factory`

Este checklist se aplica a cursos do `curso-factory` da seguinte forma:

| Camada do pipeline | Item do checklist coberto |
|---|---|
| **Research (Perplexity)** | Pré-redação — fontes primárias |
| **Draft (GPT-4o)** | Estrutura TL;DR/BLUF, densidade entidades, anti-IA |
| **Analyze (Gemini)** | GEO-16 score, blocos AEO, headings responsivos |
| **Classify (Groq)** | tags do glossário, intenção declarada |
| **Review (Claude)** | varredura final anti-IA, claims com fonte |
| **Quality Gate** | densidade outlinks, JSON-LD válido, dateModified |

Quando o módulo de curso aborda tema GEO/AEO/Agentic, este checklist tem **prioridade sobre** o template editorial HSM/HBR — a estrutura TL;DR + BLUF substitui a abertura HBR padrão para esses temas.
