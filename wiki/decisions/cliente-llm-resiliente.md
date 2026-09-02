---
name: cliente-llm-resiliente
description: "Por que o pipeline morria com 'cadeia de fallback esgotada' com o Google vivo: cota esgotada tratada como falha transitória, HTTP 200 sem bloco de texto abrindo circuito, e fallback de um salto só. Desenho da camada de resiliência (wave 6)."
metadata:
  type: decision
  created: 2026-09-02
---

O cliente LLM (`src/llm_client.py`) classifica toda falha numa taxonomia e reage por classe:
cota, chave ou modelo inexistente tiram o provedor da sessão na primeira resposta, sem retry;
429 transitório e 5xx repetem com backoff e contam no circuito; pedido rejeitado não repete;
HTTP 200 sem texto utilizável (só bloco de raciocínio, saída truncada) repete uma vez e não
abre circuito. O fallback é uma cadeia por provedor em `config/providers.yaml`
(`fallback_chain`), alinhada ao `task_routing` do geo-orchestrator, percorrida pulando quem
está morto, com circuito aberto ou sem chave; se ninguém responde, sobe
`FallbackExhaustedError` com o histórico de cada tentativa. A extração de texto concatena os
blocos de texto (Anthropic), ignora partes de raciocínio (Google) e diagnostica saída consumida
pelo raciocínio (OpenAI e compatíveis). O planejamento de aulas deixou de mascarar falha de
provedor como "aula única".

Relacionadas: [[geracao-por-aula-e-insumo-correto]], [[diretriz-editorial-v3-narrativa-sem-cota]].

---

## Linha do tempo (append-only, ordem reversa)

- **2026-09-02** — [criação] Segunda geração real do dia (curso de 6 aulas) morreu na primeira
  chamada do writer com "Cadeia de fallback esgotada apos 2 tentativas (ultimo: openai)", com
  US$ 0,04 gastos e o Google vivo. Causas medidas no log: (1) a OpenAI sem crédito
  (`credit_balance_exhausted`) respondia 429 e o cliente gastava três tentativas com backoff em
  cada chamada antes do fallback; (2) a Anthropic respondia 200 e o cliente quebrava em
  `content[0]["text"]` (KeyError `'text'`) porque o primeiro bloco não era texto; (3) o
  KeyError contava como falha de provedor e abriu o circuito da Anthropic por 60 s; (4) o
  fallback era um salto só (openai > anthropic > openai), então o Google nunca foi tentado.
  Correção: taxonomia de erro, extração tolerante, provedor morto na sessão, cadeia completa
  por provedor, erro de formato sem circuito, histórico na exceção final. Testes em
  `tests/test_llm_client_resiliente.py`.
