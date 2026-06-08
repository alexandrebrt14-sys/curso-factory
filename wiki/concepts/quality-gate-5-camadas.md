---
name: quality-gate-5-camadas
type: concept
category: architecture
status: stable
created: 2026-05-26
updated: 2026-05-26
related:
  - accent-checker
  - content-checker
  - voice-guard
  - claude-reviewer
---

# Quality Gate (5 camadas de validação)

Camada de validação automática que roda **após** o pipeline LLM
completo e **antes** de mover o curso de `output/drafts/` para
`output/approved/`. Implementado em `src/validators/quality_gate.py`.

## As 5 camadas em ordem

| # | Camada      | Arquivo                          | Bloqueante | Auto-fix |
|---|-------------|----------------------------------|------------|----------|
| 1 | Acentuação  | `accent_checker.py`              | Não        | Sim      |
| 2 | Conteúdo    | `content_checker.py`             | Sim        | Não      |
| 3 | Links       | `link_checker.py`                | Sim        | Não      |
| 4 | Voice Guard | `voice_guard.py`                 | Sim        | Não      |
| 5 | FinOps      | `cost_tracker.py`                | Sim        | Não      |

Cheques expandidos por camada:

- **1 — [[accent-checker]]**: 300+ mapeamentos PT-BR, auto-corrige
  preservando URLs/código/variáveis.
- **2 — [[content-checker]]**: 10+ cheques editoriais (palavras,
  tabelas, exercícios, Bloom, andragogia, clichês, parágrafos longos,
  emojis).
- **3 — link_checker**: acentos em URL = erro crítico (incidente
  2026-03-27: 55 hrefs corrompidos); verificação de links internos.
- **4 — [[voice-guard]]**: canonical/banned/min_score do cliente
  ativo via [[multi-tenant-clientcontext]].
- **5 — cost_tracker**: budget guard $5 max Claude, $10 max total
  por curso. Excede → aborta.

## Resultado `GateResult`

```python
@dataclass
class GateResult:
    aprovado: bool                    # True se todas camadas bloqueantes ok
    texto_corrigido: str              # texto após auto-fix de camada 1
    erros_por_camada: dict[str, list[str]]
    cost_total: float
```

## Comportamento

- Se camada 1 detecta acentos faltando → corrige automaticamente,
  reporta nas notas mas não bloqueia.
- Se camada 2-5 falha → `aprovado=False`, curso fica em
  `output/drafts/`.
- Pipeline tenta no máximo 1 re-rodada após auto-fix de camada 1.

## Wave 2026-05-20 — camada 2 expandida para GEO/SEO

Cursos com tags `geo-2026` ou `seo-2026` ganham cheques opcionais
bloqueantes em camada 2:

- Cite Sources count (Princeton checklist, [[sources/aggarwal-kdd-2024]]).
- Statistics count com fonte+ano.
- Quotation count atribuída.
- Compression Fidelity.
- Schema-content parity.

## Quality Gate vs Karpathy Lint

O **Quality Gate** valida **conteúdo de curso** antes de aprovação.
O **wiki lint** ([[llm-wiki-karpathy]]) valida **saúde do grafo
wiki** (cross-links, órfãos, stale claims). Camadas independentes;
ambas obrigatórias em momentos distintos:

- Quality Gate roda no pipeline LLM, após etapa 5 (Claude review).
- Wiki lint roda antes de qualquer push em `wiki/`.

## Anti-padrões

- Pular quality gate "porque é teste": testes têm fixtures
  pré-validadas; produção exige gate completo.
- Adicionar exceção temporária no gate "só pra esse curso": vira
  permanente. Corrigir o conteúdo, não a regra.
- Reduzir budget Claude para passar cursos caros: reescrever prompt
  ou reduzir escopo do curso.
