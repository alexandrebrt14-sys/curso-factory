---
name: content-checker
type: entity
category: validator
status: stable
created: 2026-05-26
updated: 2026-09-08
related:
  - quality-gate-5-camadas
  - andragogia-knowles
  - taxonomia-bloom
  - padrao-editorial-hsm-hbr
  - abertura-checker
  - abertura-direta-sem-distracao
---

# content_checker.py (camada 2 do quality gate)

Validator em `src/validators/content_checker.py`. Camada **2 —
Conteúdo** do [[quality-gate-5-camadas]]. Valida estrutura editorial e
pedagógica de cada módulo gerado.

## Atualização de 08/09/2026 — a unidade é a aula, e a aula não tem exercício

Os cheques abaixo descrevem o estado de 26/05/2026 e ficam como histórico. Desde
27/08/2026 a unidade medida é a **aula** (tetos em `config/lexicos.json`, `tetos.D`), e
desde 08/09/2026 valem as regras [[abertura-direta-sem-distracao]]:

- **Exercícios: zero por aula** (`min_exercises_per_lesson: 0`). O cheque 5 abaixo foi
  invertido: a presença de "faça agora"/"exercício" reprova, pela categoria `abertura`
  (regra R6), medida pelo [[abertura-checker]] e emitida por `check_content` (item 15).
- **Categoria `abertura`** (erro bloqueante, aula e trilha): R1 (subtítulo e parágrafo depois
  do H1), R3, R5, R6, R7 (fonte só no rodapé da trilha), R8, R9. `erros_de_abertura()` é a
  ponte; `QualityGate._check_content_por_unidade` passa a medir também a trilha.
- Tabela, blockquote e negrito não têm piso desde 02/09/2026; apoio visual é teto.

## Cheques (estado de 26/05/2026, histórico)

1. **Contagem de palavras** por módulo: 2.500 a 4.000.
2. **Presença de tabelas**: mínimo 1 tabela markdown (com pipes) por
   módulo.
3. **Hierarquia de títulos**: sem pulos (H2 → H4 sem H3 é erro).
4. **Blockquotes para insights**: mínimo 1-2 por módulo.
5. **Exercícios**: mínimo 3, com contexto profissional e progressão
   [[taxonomia-bloom]].
6. **Clichês proibidos**: 18 expressões banidas ("nos dias de hoje",
   "é fundamental que", "não é segredo que", "vamos explorar", etc).
7. **Verbos Bloom nos objetivos**: aceita 3-6; rejeita 1-2.
8. **Princípios andragógicos**: 5 indicadores que correlacionam com
   [[andragogia-knowles]] (POR QUE antes do COMO, conexão com
   experiência prévia, aplicabilidade imediata, etc).
9. **Parágrafos longos**: máximo 5 linhas por parágrafo.
10. **Emojis**: proibidos em qualquer saída.

## Camada bloqueante

Falha em camada 2 **bloqueia** a aprovação. Diferente da camada 1
(acentuação) que auto-corrige.

## Wave 2026-05-20 — adições opcionais

Para cursos GEO/SEO, validações opcionais foram adicionadas:

- Cite Sources count (Princeton checklist).
- Statistics count com fonte+ano.
- Quotation count atribuída.
- Compression Fidelity (resumo preserva tese).
- Schema-content parity (JSON-LD bate com HTML visível).

Estas validações são **bloqueantes** apenas se o curso tem tags
`geo-2026` ou `seo-2026`.

## Configuração por cliente

Limites podem variar por cliente em `config/clients/<id>/client.yaml`
seção `quality_rules.content`. Cliente `default` herda os defaults
acima. Cliente `herreira` (joalheria) pode aceitar parágrafos mais
descritivos (até 7 linhas) por nicho.

## Cross-references

- Camada 1 ([[accent-checker]]) corrige acentos antes do cheque de
  conteúdo.
- Camada 4 ([[voice-guard]]) valida naming/identidade do cliente
  ativo.
- [[taxonomia-bloom]] e [[andragogia-knowles]] são as referências
  conceituais para cheques 5, 7, 8.
