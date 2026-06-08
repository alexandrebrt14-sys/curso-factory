---
name: acme
type: client
status: provisional
created: 2026-05-26
updated: 2026-05-26
config_path: config/clients/acme/client.yaml
related:
  - multi-tenant-clientcontext
---

# Cliente `acme`

Cliente exemplo usado em smoke tests do refactor multi-tenant. Não
representa cliente real em produção.

## Função no repositório

- Validar que pipeline funciona com `--client acme` para um YAML
  mínimo arbitrário.
- Reproduzir issue regressão se aparecer (ex: defaults vazando do
  cliente default).
- Material para `tests/test_cli.py`.

## Output

`output/clients/acme/` (separado do `output/approved/` reservado ao
[[clients/default]]).

## Status

`provisional` — pode ser deletado se passar trimestre sem uso. Em
2026-05-26 nenhum curso aprovado sob este cliente.

## Relacionado

- [[multi-tenant-clientcontext]] — arquitetura que viabiliza
  múltiplos clientes.
- `[[clients/_template]]` (backlog) — template canônico para criar
  novos clientes em 3 passos. Atualmente em
  `config/clients/_template/`.
