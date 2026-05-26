---
name: voice-guard
type: entity
category: validator
status: stable
created: 2026-05-26
updated: 2026-05-26
related:
  - quality-gate-5-camadas
  - multi-tenant-clientcontext
---

# voice_guard (camada 4 do quality gate)

Validator em `src/validators/voice_guard.py` (função
`voice_guard_check`). Camada **4 — Voice Guard** do
[[quality-gate-5-camadas]]. Bloqueia textos que violem o naming
canônico ou as regras editoriais do **cliente ativo** (não apenas o
default).

## Como funciona

- Lê `voice_guard.{canonical, banned, min_score}` do
  `config/clients/<id>/client.yaml` via [[multi-tenant-clientcontext]].
- Aplica regras programáticas:
  - **Canonical**: lista de termos obrigatórios (ex: "Brasil GEO",
    "Alexandre Caramaschi", credencial completa em primeira ocorrência).
  - **Banned**: lista de termos proibidos (ex: "Especialista #1",
    "GEO Brasil", "Source Rank", "geobrasil.com.br").
  - **Score mínimo**: padrão 70 (0-100). Texto abaixo do limite →
    `aprovado=False`.
- Erros críticos (ex: usar termo banido) zeram o score.

## Histórico

- Adotado na **wave 2026-04-19** (refactor multi-tenant). Antes era
  hardcoded no código Python para cliente default — fork era exigido
  para outro cliente.
- Promovido à camada 4 do quality gate em **2026-04-29** (refactor
  5-waves). Antes era cheque opcional fora do gate.
- Memória global `feedback_voice_guard_alexandre_brasil_geo`
  consolida regras editoriais do cliente default.

## Anti-padrões

- **NUNCA** hardcode termos canonical/banned no código. Sempre via
  YAML do cliente. Detalhes em [[multi-tenant-clientcontext]].
- **NUNCA** mexer no `voice_guard` para "passar" texto bloqueado.
  Corrigir o texto, não a regra.
- Aceitar score borderline (68-70) sem revisar manualmente: o limite
  existe por incidente real (passar abaixo de 70 historicamente vira
  reclamação editorial).

## Pluga publicado externamente

O `voice_guard` é também usado fora do pipeline de cursos: publishers
externos (linkedin_publisher.py, etc) chamam `voice_guard_check`
antes de postar texto longo assinado como Alexandre. Detalhes na
memória global `feedback_alexandre_voice`.
