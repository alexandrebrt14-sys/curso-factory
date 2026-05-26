---
name: accent-checker
type: entity
category: validator
status: stable
created: 2026-05-26
updated: 2026-05-26
related:
  - quality-gate-5-camadas
  - claude-reviewer
---

# accent_checker.py (camada 1 do quality gate)

Validator programático em `src/validators/accent_checker.py`. Camada
**1 — Acentuação** do [[quality-gate-5-camadas]]. Detecta e corrige
automaticamente palavras PT-BR sem acento na saída do pipeline.

## Como funciona

- 300+ mapeamentos de palavras sem acento → forma correta (`nao` →
  `não`, `producao` → `produção`, `voce` → `você`).
- `check_accents(texto)` retorna lista de erros com linha, palavra e
  contexto de 80 chars.
- `fix_accents(texto)` corrige automaticamente, preservando:
  - URLs (regex de href + url completas).
  - Código (rastreamento de blocos ` ``` `).
  - Variáveis JS/Python (camelCase, snake_case, com underscore ou
    ponto).
- Modo `auto_fix=True` é o default do quality gate. Texto corrigido
  retornado em `GateResult.texto_corrigido`.

## Por que é a camada 1

- Erro mais frequente em saída de LLMs em PT-BR.
- Cheque mais rápido (regex puro, sem chamada externa).
- Falha em camada 1 não bloqueia (auto-corrige); apenas reporta.

## Cobertura testada

`tests/test_validators_smoke.py` cobre 10 cenários incluindo
preservação de URL com acento (caso curioso: `alexandrecaramaschi.com`
não pode virar `alexandrecarámaschi.com`).

## Histórico de incidentes

- **2026-03-27**: incidente "55 hrefs corrompidos" por aceitar `~` em
  acentuação URL. Solução: regex de URL preservation.
- Memória global `feedback_acentuacao_portugues_brasil_canonica`
  documenta que nunca rodar `fix_accents` cego em arquivos com
  slugs/props JS.

## Cross-references

- Após `accent_checker`, [[content-checker]] (camada 2) valida
  estrutura.
- [[voice-guard]] (camada 4) bloqueia naming não-canônico do cliente.
- [[claude-reviewer]] (etapa 5 do pipeline LLM) tenta corrigir
  acentuação antes; `accent_checker` é a rede de segurança final.
