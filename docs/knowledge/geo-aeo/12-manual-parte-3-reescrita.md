---
titulo: Manual Operacional — Parte 3 — Reescrita e Geração de Conteúdo Longo
versao: 1.0
data: 2026-04-25
tipo: manual-operacional
escopo: Instruções 16 a 25
---

# Parte 3 — Reescrita e Geração de Conteúdo Longo (Instruções 16–25)

Dez diretivas que controlam **como** se escreve e reescreve conteúdo. Cobrem a estrutura padrão (TL;DR/BLUF), densidade de entidades, normas por plataforma e prevenção de alucinação.

---

## Instrução 16 — Estrutura padrão: TL;DR + BLUF + Corpo + Síntese

**DIRETIVA.** Toda reescrita ou geração de conteúdo longo segue:

1. **TL;DR** de 3–5 linhas no topo.
2. **BLUF (Bottom Line Up Front)** — primeira seção responde a pergunta central.
3. **Corpo** com 4–7 seções.
4. **Síntese** final que NÃO repete, mas conecta a implicações.

**RACIONAL.** A-RAG e Role-Augmented GSEO confirmam que *front-loading* da resposta aumenta tanto extração por agente quanto retenção humana. McKinsey Automation Curve (jan/2026) reforça: no nível 4+ de automação agêntica, o conteúdo precisa ser consumível pelo plano contínuo do agente, não apenas pelo clique humano.

**TEMPLATE.**

```
# Título orientativo (6–10 palavras, pergunta ou tese)

**TL;DR:** [3–5 linhas, autocontidas]

## [BLUF — pergunta central respondida em 80–150 palavras]

## [Seção 2 — contexto/dados]
## [Seção 3 — análise/mecanismo]
## [Seção 4 — contra-argumento ou limites]
## [Seção 5 — implicação prática]

## Síntese — o que muda a partir daqui
```

---

## Instrução 17 — Densidade de entidades nomeadas: 1 a cada 100 palavras

**DIRETIVA.** Conteúdo longo deve mencionar **entidades nomeadas** (pessoas, empresas, papers, produtos, padrões técnicos) com densidade de **1 entidade a cada 100 palavras**, com pelo menos 30% delas linkadas a Wikidata, arXiv ou site oficial.

**RACIONAL.** A solidificação de entidade (Instrução 9) e o grounding em KG (+26,5% de acurácia, arXiv:2502.13247) operam no nível de menção. Densidade alta de entidades reconhecíveis aumenta a probabilidade de o conteúdo ser usado como evidência em respostas geradas.

**CHECKLIST.**

- NER automático conta entidades por bloco de 100 palavras.
- Se densidade < 1, expandir com exemplos concretos (nomear empresas, citar autores).
- Linkar entidades novas a fonte canônica na primeira menção.

---

## Instrução 18 — Tom e formato específicos por plataforma

**DIRETIVA.** Adaptar tom, comprimento, densidade de quotes e CTA por plataforma. **Nunca publicar a mesma versão em todas.**

**RACIONAL.** Cada plataforma tem norma editorial e mecânica de descoberta distintas. Reddit-Reddit correlation (Discovery Gap) com descoberta confirma que tom nativo importa. Pinterest GEO (arXiv:2602.02961) entregou **+20% tráfego orgânico** e **+19% topic-query alignment** ao adaptar conteúdo a especificidades visuais e de busca da plataforma.

**MATRIZ POR PLATAFORMA.**

| Plataforma | Comprimento | Tom | Estrutura-chave | CTA |
|---|---|---|---|---|
| **Medium** | 1.500–2.500 palavras | Ensaístico, primeira pessoa moderada | TL;DR + 4–6 H2 + síntese narrativa | Newsletter subscribe |
| **Quora** | 600–1.200 palavras | Resposta direta, autoritativa, pessoal | BLUF nas 2 primeiras frases + bullets controlados + experiência concreta | Link único para recurso âncora |
| **LinkedIn Newsletter** | 1.000–1.800 palavras | Executivo, orientado a decisão | 3–5 *insights* numerados + dados + CTA profissional | Comentário-pergunta no fim |
| **Substack** | 2.000–4.000 palavras | Analítico-profundo, voz autoral | Manchete + lede jornalístico + análise + *paywall optional* | Assinatura + recomendação cruzada |

Detalhamento operacional em `32-checklist-publicacao-multi.md`.

---

## Instrução 19 — Regras editoriais para Medium

**DIRETIVA.** Abrir com TL;DR em itálico, usar imagens com legenda e *alt text* descritivo, **máximo 2 listas por artigo**, parágrafos de 2–4 frases, fechar com pergunta aberta + link para newsletter própria.

**RACIONAL.** O algoritmo de descoberta do Medium pondera *read ratio* e *highlights*; densidade narrativa em parágrafos curtos e *highlightable lines* (frases-tese isoladas) aumenta engajamento. Source Coverage (arXiv:2512.09483) mostra que `.com` TLD tem importância SHAP de 0,623 — Medium herda essa autoridade para o autor.

**CHECKLIST.**

- 1 *pull quote* destacável a cada 500 palavras.
- Tags Medium: 5 tags, sendo 2 amplas e 3 nichadas.
- Linkar para 2–3 artigos próprios anteriores (link juice interno).

---

## Instrução 20 — Regras editoriais para Quora

**DIRETIVA.** Primeira frase **responde literalmente a pergunta**. Segunda frase estabelece credencial ("Como [cargo/experiência]…"). Corpo traz 2–4 sub-respostas com dados. Encerrar com 1 link único e relevante.

**RACIONAL.** Quora é fonte frequente de citação por LLMs por respostas autocontidas com autoria identificável (cumpre EEAT). O formato pergunta→resposta direta espelha o padrão de extração de AEO descrito no CC-GSEO-Bench.

**CHECKLIST.**

- Sem "Olá", sem "Boa pergunta", sem preâmbulo.
- Credencial verificável no perfil Quora antes de publicar.
- Quote direta de fonte autoritativa quando possível.
- Para o ecossistema Brasil GEO: credencial canônica no perfil ("CEO da Brasil GEO, ex-CMO da Semantix Nasdaq, cofundador da AI Brasil").

---

## Instrução 21 — Regras editoriais para LinkedIn Newsletters

**DIRETIVA.** Headline interrogativo ou de tese (≤ 70 caracteres). Lede de 3 linhas. Corpo em **3 a 5 *insights* numerados** com dado-âncora cada. Fechar com pergunta direta aos leitores e CTA de comentário.

**RACIONAL.** LinkedIn pondera *dwell time* e comentários no ranqueamento. Conteúdo executivo orientado a decisão (consistente com o público C-level) gera mais comentário substantivo. McKinsey Automation Curve — relevante para essa audiência — mostra que decisores buscam *frames* operacionais, não teoria.

**CHECKLIST.**

- 1 estatística-âncora por *insight*, com fonte hiperlinkada.
- Sem hashtags excessivas (máximo 5, todas profissionais).
- Mencionar 2–3 perfis relevantes do setor (não-spam).

---

## Instrução 22 — Regras editoriais para Substack

**DIRETIVA.** Formato de *long-form essay* analítico (2.000–4.000 palavras), com manchete jornalística, lede de 4–6 linhas, divisão em 5–8 seções, e **PS final com recomendação cruzada** de outras publicações.

**RACIONAL.** Substack premia profundidade e voz autoral; sua mecânica de *recommendations* entre publicações é multiplicador de descoberta. Substack frequentemente cai no top-20 de citações LLM por nicho (arXiv:2507.05301).

**CHECKLIST.**

- *Footnotes* numeradas com fontes primárias.
- 1 imagem original (gráfico próprio ou diagrama) por publicação.
- Recomendar 2 publicações Substack relacionadas no rodapé.

---

## Instrução 23 — Negrito estratégico em frases-tese, não em sentenças completas

**DIRETIVA.** Usar **negrito** apenas em 1–3 trechos curtos por seção que carreguem o *insight* central. **Nunca** negritar frases inteiras nem usá-lo decorativamente.

**RACIONAL.** Negrito é sinal de saliência tanto para humanos (escaneabilidade) quanto para extratores de chunk. Excesso dilui o sinal — princípio aplicado consistentemente em CC-GSEO-Bench e validado em testes de extração por Perplexity.

**PSEUDOCÓDIGO.**

```
for section in content.sections:
    teses = extract_top_insights(section, n=3)
    for tese in teses:
        section = bold_phrase(section, tese, max_words=12)
```

---

## Instrução 24 — Casar intenção do usuário com framing explícito

**DIRETIVA.** Identificar a **intenção dominante** (informacional, transacional, navegacional, comparativa) e declará-la explicitamente no primeiro parágrafo ou subtítulo.

**RACIONAL.** Role-Augmented Intent-Driven GSEO (arXiv:2508.11158) com a rubrica G-Eval 2.0 de 6 níveis demonstra que intenção precisa ser **sinal explícito**, não inferido. LLMs citam preferencialmente conteúdo cuja intenção declarada bate com a query.

**CHECKLIST.**

- Frase-âncora do tipo "Este guia ajuda você a [decidir / comparar / implementar / entender]…" no primeiro parágrafo.
- Headings refletem a intenção declarada.

---

## Instrução 25 — Prevenir alucinação com afirmações verificáveis

**DIRETIVA.** Toda afirmação factual no conteúdo gerado deve ser verificável contra (a) fonte primária linkada, (b) dado em JSON-LD da própria página, ou (c) tripla de KG referenciada. Sem fonte verificável → reescrever ou remover.

**RACIONAL.** Mitigação de alucinação por LLMs depende de conteúdo estruturado (KGs, Schema.org, JSON-LD), conforme síntese do corpus. MATRIX Ontology e LLM4Schema.org convergem nesse ponto.

**PSEUDOCÓDIGO.**

```
for claim in extract_factual_claims(content):
    if not (has_external_link(claim) or in_jsonld(claim) or in_kg(claim)):
        flag_for_rewrite(claim)
```

**INTEGRAÇÃO COM `curso-factory`.** O prompt do redator (`src/templates/prompts/draft.md`) já obriga uso de marcador `[FALTA EVIDÊNCIA: <o que precisa ser buscado>]` quando não há ancoragem disponível na pesquisa. O Voice Guard e o Quality Gate detectam claims não ancorados como aviso.

---

## Resumo da Parte 3

| Instrução | Foco | Bloqueante? |
|---|---|---|
| 16 — TL;DR + BLUF + Corpo + Síntese | estrutura | aviso |
| 17 — Densidade entidades 1/100 palavras | grounding | aviso |
| 18 — Adaptação por plataforma | distribuição | aviso |
| 19 — Medium | plataforma | regra editorial |
| 20 — Quora | plataforma | regra editorial |
| 21 — LinkedIn Newsletter | plataforma | regra editorial |
| 22 — Substack | plataforma | regra editorial |
| 23 — Negrito 1–3 trechos / seção | saliência | aviso |
| 24 — Intenção explícita no primeiro parágrafo | clareza | aviso |
| 25 — Claims verificáveis | anti-alucinação | aviso |
