# Política de Segurança

## Versões suportadas

Apenas o branch `main` recebe correções de segurança. Não há versões taggeadas separadas neste momento.

| Branch | Suporte de segurança |
|---|---|
| main | sim |
| outras | não |

## Reportando vulnerabilidade

**Não abra issue pública** para vulnerabilidades de segurança.

Use uma das vias privadas:

1. **GitHub Security Advisories (preferido):** https://github.com/alexandrebrt14-sys/curso-factory/security/advisories/new
2. **E-mail:** alexandre.brt14@gmail.com com assunto começando com `[curso-factory security]`

Inclua no relato:

- Descrição do problema.
- Passos para reproduzir.
- Impacto esperado (vazamento de chave, RCE, exfiltração de dados, etc.).
- Versão / commit afetado.
- (Opcional) sugestão de correção.

## Tempo de resposta

- **Acknowledgment** em até 5 dias úteis.
- **Triagem inicial** em até 10 dias úteis.
- **Correção ou plano de mitigação** comunicado ao reporter assim que disponível.

## Escopo

### Em escopo

- Vazamento de credenciais via logs, cache ou output.
- Injeção de prompt que leva a vazamento de dados de outro cliente.
- Execução de código arbitrário via templates Jinja2 ou parsers.
- Bypass do voice guard ou quality gate em condições normais de uso.
- Vulnerabilidades em dependências diretas (listadas em `pyproject.toml`).

### Fora de escopo

- Ataques que exigem acesso físico à máquina onde o código roda.
- Engenharia social contra contributors.
- Vulnerabilidades em serviços de terceiros (OpenAI, Anthropic, Google, Groq, Perplexity, GitHub, Supabase) — reporte diretamente ao provider.
- Bugs sem implicação de segurança — abra issue normal.

## Práticas de segurança aplicadas

### Secret scanning

- `gitleaks` roda em todo PR via `.github/workflows/security-scan.yml`.
- Pre-commit hook `secret_guard.py` em `.githooks/pre-commit`.

### Static analysis

- `bandit` roda em todo PR (severity medium+).
- `pip-audit` roda em todo PR e semanalmente.

### Dependências

- `dependabot` configurado para atualização semanal de pip e GitHub Actions.
- Grupos de atualização para evitar PR-spam.

### Cache e logs

- `output/costs.json` registra apenas tokens, custo e provider — sem chaves nem prompt.
- `.cache/<hash>.json` armazena prompt e response — **trate como dado sensível** se prompts contiverem PII.
- Chaves de API só vivem em variáveis de ambiente. Nunca em código, nunca em testes.

### Pipeline LLM

- O voice guard tem blacklist de domínios de phishing / fake titles configurável por cliente.
- Disclaimers de IA são bloqueados (anti-vazamento de prompt do sistema via "Como modelo de linguagem...").

## Disclosure

Após correção mergeada, publicaremos GitHub Security Advisory creditando o reporter (a menos que solicite anonimato).

## Contato

Alexandre Caramaschi — alexandre.brt14@gmail.com
