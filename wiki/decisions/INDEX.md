# Índice de decisões — curso-factory

Uma linha por decisão (< ~200 caracteres). Este arquivo é o catálogo navegável; o
detalhe vive no arquivo de cada decisão. Mantenha curto — ele entra no contexto.

<!-- formato: - [Título curto](arquivo.md) — gancho de uma linha · `type` -->

## Decisões (ADRs)

- [ADR-001 — Adoção de LLM Wiki](ADR-001-adopcao-llm-wiki.md) — por que e como a base de conhecimento gerada por LLM · `decision`
- [ADR-002 — Sync automático courses↔wiki](ADR-002-sync-automatico-courses-wiki.md) — pipeline de sincronização entre cursos e wiki · `decision`

## Lições do portal /educacao (25-07-2026)

- [Invólucro copiado de curso irmão](involucro-copiado-de-curso-irmao.md) — curso novo por cópia serve FAQ/bio/JSON-LD do curso errado; FAQ como fonte única · `mistake`
- [Números de curso digitados derivam](numeros-de-curso-digitados-derivam.md) — contagem e duração derivam de STEPS, nunca à mão; gate provado por injeção · `mistake`
- [Arquivo de conteúdo sem consumidor](arquivo-de-conteudo-sem-consumidor.md) — módulo commitado sem import compila limpo e vira âncora morta · `mistake`
- [Acentuação: ferramentas e armadilhas](acentuacao-ferramentas-e-armadilhas.md) — perl grava mojibake invisível; lista fixa corrige pela metade; corretor cria o inverso · `mistake`
- [Integração: conflitos têm dono](integracao-conflitos-tem-dono.md) — linha a linha por autor; gerados regeneram; worktree inspeciona antes de remover · `insight`

## Histórico

- [CLAUDE-CHANGELOG](CLAUDE-CHANGELOG.md) — log datado de mudanças aplicadas, extraído do `CLAUDE.md` para mantê-lo enxuto

---

Como usar: ver [`README.md`](README.md). Template: [`_TEMPLATE.md`](_TEMPLATE.md).
