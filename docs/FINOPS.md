# FinOps — Curso Factory

## Custo por Provider (referência março/2026)

| Provider    | Modelo              | Input (por 1M tokens) | Output (por 1M tokens) | Uso no pipeline      |
|-------------|---------------------|-----------------------|------------------------|----------------------|
| Perplexity  | sonar-pro           | $3,00                 | $15,00                 | Pesquisa (1x)        |
| OpenAI      | gpt-4o              | $2,50                 | $10,00                 | Redação (N módulos)  |
| Google      | gemini-1.5-pro      | $1,25                 | $5,00                  | Análise (N módulos)  |
| Groq        | llama-3.3-70b       | $0,59                 | $0,79                  | Classificação (1x)   |
| Anthropic   | claude-sonnet-4-5   | $3,00                 | $15,00                 | Revisão (1x)         |

Valores aproximados. Consulte os sites oficiais para preços atualizados.

---

## Custo Estimado por Curso

Um curso típico com 8 módulos de ~2.000 tokens cada custa aproximadamente:

| Estágio      | Tokens input | Tokens output | Custo estimado |
|--------------|-------------|---------------|----------------|
| Pesquisa     | ~2.000      | ~3.000        | $0,06          |
| Redação (x8) | ~4.000      | ~16.000       | $0,17          |
| Análise (x8) | ~16.000     | ~8.000        | $0,06          |
| Classificação| ~16.000     | ~1.000        | $0,01          |
| Revisão      | ~20.000     | ~22.000       | $0,39          |
| **Total**    |             |               | **~$0,70**     |

Com cache ativo, cursos semelhantes custam menos na segunda execução.

---

## Como Funciona o Budget Guard

O Budget Guard é uma camada de proteção que impede gastos acima do orçamento
definido em `config/settings.yaml`:

```yaml
budget:
  max_cost_per_course_usd: 5.00
  max_cost_per_run_usd: 50.00
  alert_threshold_pct: 80
```

Funcionamento:

1. Antes de cada chamada ao LLM, o custo estimado é calculado com base no
   número de tokens do payload (usando o tokenizador do provider)
2. Se o custo acumulado da sessão ultrapassar `alert_threshold_pct` do limite,
   um aviso é exibido no console
3. Se o limite `max_cost_per_course_usd` for atingido, o pipeline pausa e
   solicita confirmação antes de continuar
4. Se `max_cost_per_run_usd` for atingido, o pipeline encerra com erro

---

## Como Ler o Cost Report

Execute: `python cli.py cost-report`

O relatório exibe:

- **Provider:** nome do serviço LLM
- **Chamadas:** número de requisições feitas no período
- **Tokens:** total de tokens consumidos (input + output)
- **Custo (USD):** custo em dólares americanos

O período exibido corresponde ao histórico salvo em `.cache/cost_log.jsonl`.
Para ver custos de uma sessão específica, filtre o arquivo JSONL por data.

---

## Dicas para Otimização de Custos

**Use o cache ativamente.**
Ao reprocessar um curso com pequenas alterações, apenas os estágios cujo
input mudou serão recalculados. Mantenha o cache ativo em ambientes de
desenvolvimento.

**Ajuste o número de módulos.**
O custo de redação e análise escala linearmente com o número de módulos.
Comece com 4–5 módulos para validar o curso antes de expandir.

**Prefira Groq para tarefas de classificação.**
O Groq tem o menor custo por token entre os providers do pipeline e
latência inferior a 2 segundos, ideal para tarefas estruturadas.

**Monitore o cost_log.jsonl regularmente.**
O arquivo `.cache/cost_log.jsonl` registra cada chamada com timestamp,
provider, tokens e custo. Use-o para identificar estágios com custo
anormalmente alto e revisar os prompts correspondentes.

**Execute `cache-clear` apenas quando necessário.**
Limpar o cache elimina a proteção contra retrabalho. Prefira deletar
apenas a pasta do curso específico em vez de limpar todo o cache.
