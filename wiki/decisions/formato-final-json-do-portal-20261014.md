---
name: formato-final-json-do-portal-20261014
description: "Desde 14/10/2026 a fábrica entrega o curso como src/content/cursos/<slug>.json do portal (schema zod espelhado), com sidecar de glossário, manifesto de mídia e steps.ts fino; TSX com conteúdo deixou de ser formato final."
metadata:
  type: decision
  created: 2026-10-14
---

O portal /educacao guarda o conteúdo de cada curso em `src/content/cursos/<slug>.json`,
lido do disco e validado pelo schema de `src/lib/educacao/conteudo/schema.ts` (piloto PR
#1409; #1421 e #1425 migrados; 55 cursos a migrar). A fábrica exporta nesse formato
(`python cli.py exportar-json`, `drafts-to-tsx --json`) e valida antes do PR com
`scripts/validar_curso_json.py`, que reproduz os gates do portal: schema estrito, ids
ASCII únicos, capítulo aberto até 72.000 caracteres (teto de 900 KB por página),
`language` em todo bloco de código, acentos até 20 (80 em arquivo grande), emoji zero.
Um PR por curso no portal; o JSON fica fora do modo foco do CI, então dividir por
capítulo só multiplica os 27 min da esteira. O que não se corta por velocidade: revisão
editorial humana, comparação de HTML servido, 5 a 10 variações antes do lote, revisão
cruzada entre modelos. Detalhe em `docs/portal-educacao-estado-20261014.md`.

Relacionadas: [[guia-aplicavel-e-fonte-recente-20260927]], [[boas-praticas-de-escrita-20260927]], [[involucro-copiado-de-curso-irmao]].

---

## Linha do tempo (append-only, ordem reversa)

- **2026-10-14** — [criação] pedido do dono depois do fechamento da Etapa 1 da reorganização do landing-page-geo: parar de gerar conteúdo no formato que o portal está abandonando.
