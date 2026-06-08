# Earned Media é a camada dominante do GEO — framework para portais educacionais

> **Documento canônico.** Consolida a evidência de que **a maioria do que os modelos de IA citam vem de mídia conquistada (earned media) e jornalismo**, não de mídia paga nem de conteúdo próprio — e traduz isso em framework, técnicas e KPIs para (a) o portal do cliente que o curso-factory atende e (b) o conteúdo dos cursos sobre GEO/marketing.
>
> **Versão:** 1.0 · 2026-06-03 · Owner: Brasil GEO (Alexandre Caramaschi)
>
> **Fonte primária:** Muck Rack / Generative Pulse — *"What is AI Reading?"* (edição mai/2026, 25M+ links, 17 setores). Reforço: Chen et al. (arXiv:2509.08919, set/2025). Deriva o item 13 de `GEO_REDACAO_CHECKLIST_2026.md` e o Conceito 63 de `GEO_50_CONCEITOS_CANONICAL.md`.

---

## 0. Tese em uma frase

**Se a empresa não está nas matérias e fontes de terceiros que a IA lê, ela não existe para a IA.** A máquina replica a lógica humana: ignora o banner e confia no jornalista. Para um curso, vale a mesma lógica — o módulo ganha citação quando ancora seus claims em fontes externas autoritativas, não em afirmações próprias.

---

## 1. A evidência dura (Muck Rack mai/2026)

Estudo do time Generative Pulse, analisando 25M+ links citados por ChatGPT, Claude e Gemini em 17 setores.

| Tipo de fonte | Share das citações de IA | Leitura |
|---|---|---|
| **Earned media** (jornalismo, academia, governo, comunidades) | **84%** (faixa 82-89%) | É onde a disputa acontece. Quase tudo. |
| **Jornalismo profissional** (subconjunto) | **27%** (estável) | A pauta de imprensa é o ativo mais previsível. |
| Conteúdo próprio / blog (owned) | minoria do restante | Importa para grounding de entidade, não como fonte de citação. |
| **Mídia paga / advertorial** (paid) | **0,3%** | Praticamente morta para GEO. Anúncio não vira citação. |
| **Não-pago no total** (earned + owned) | **99%** | A IA não busca o post patrocinado. |

> **Implicação:** investir em mídia paga esperando citação por IA é queimar orçamento — earned media é **280×** mais representada (84% vs 0,3%).

### Cada modelo lê diferente

| Modelo | % respostas com citação | Domínio mais citado | Viés |
|---|---|---|---|
| **ChatGPT** | 96% | Wikipedia | veículos grandes, mainstream, alto tráfego |
| **Gemini** | 82% | Reddit | comunidades, fóruns, UGC; espelha o top-10 do Google |
| **Claude** | 55% (o mais seletivo) | PubMed Central | trade/nicho; janela de citação ~10 semanas (cita conteúdo de 2-4 semanas atrás 3× mais que o ChatGPT) |

### O tipo de pergunta decide o tipo de fonte

- Perguntas de **tendência de setor** citam jornalismo a **2×+** a taxa das perguntas how-to.
- **Press releases** aparecem quase exclusivamente em respostas de tendência — **3,5×** a frequência das queries "melhores X".
- O gap acionável: jornalistas mais *pitchados* por PR e mais *citados* pela IA têm sobreposição de apenas **~2%**. Existe arbitragem para quem mapeia quem a IA realmente cita.

### Cross-evidence

Chen et al. (arXiv:2509.08919): AI Search tem viés sistemático por earned media; earned pesa **2,3-3,1×** o owned. Conteúdo brand-owned é só **5-10%** do que os motores extraem; apenas **~38%** das citações vêm do top-10 orgânico do Google.

---

## 2. Framework: Earned Media GEO Engine (EMGE)

Cinco estágios que ligam a pergunta do ICP à citação por IA, subordinando o PR a GEO mensurável:

1. **Mapear a pauta** — as perguntas de **tendência** que o ICP faz à IA sobre o mercado (não sobre o produto) são as pautas a gerar na imprensa especializada.
2. **Mapear o alvo** — descobrir quais veículos/jornalistas a IA **realmente cita** no setor (não a lista de mídia padrão — fechar o gap de 2%).
3. **Placear tendência** — matéria de **posicionamento de tendência**, não release de produto, com porta-voz nomeado + cargo + organização, stat-dense e com frase citável autossuficiente.
4. **Diversificar por LLM** — grandes publicações de negócios → ChatGPT; comunidades/fóruns → Gemini; revistas setoriais/trade → Claude.
5. **Medir como pipeline** — share de citação por LLM, overlap com jornalista citado, persistência (~10 semanas) — não volume de clipping.

---

## 3. Técnicas de colocação (como vira citação)

1. **Enquadrar como tendência, não como produto.**
2. **Porta-voz nomeado e atribuído** — aspas diretas com nome + cargo + organização (maior lift individual, +42,6%). Credencial canônica Brasil GEO: "CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil".
3. **Stat-dense com fonte** — mínimo 3 dados sourceados por material.
4. **Frase citável e autossuficiente** — a IA cita o trecho, não a matéria inteira.
5. **Claim verificável** — evitar adjetivação vaga ("líder", "o melhor") sem dado.
6. **Sustentar a cobertura por semanas** — cadência que cubra a janela de ~10 semanas.
7. **Não comprar advertorial esperando citação** — paid = 0,3%.

---

## 4. KPIs de earned media (K-EM-001 a 006)

| ID | KPI | Definição |
|---|---|---|
| **K-EM-001** | Earned Media Share of Citations | % das citações sobre a marca/categoria vindas de earned media. Target ≥80%. |
| **K-EM-002** | Journalist-Cited Overlap | % de sobreposição entre jornalistas pitchados e citados pela IA. Meta: fechar o gap de ~2%. |
| **K-EM-003** | Trend-Pauta Coverage | % das perguntas de tendência do ICP em que a marca aparece em ≥1 fonte citada. |
| **K-EM-004** | Citation Persistence (Earned) | quantas semanas a colocação segue citada (meia-vida; ideal ~10). |
| **K-EM-005** | Trade-vs-National Mix | proporção trade/nicho vs publicações nacionais grandes (calibra Claude vs ChatGPT). |
| **K-EM-006** | Paid Leakage | % do orçamento de paid que não retorna citação (esperado ≈0; guard-rail anti-desperdício). |

---

## 5. Anti-padrões (proibidos em GEO de earned media)

- Comprar mídia paga / advertorial esperando citação (paid = 0,3%).
- Pitchar a lista de mídia padrão sem validar contra a auditoria de citação (gap de 2%).
- Vender release de produto como GEO (só rende dentro de pauta de tendência).
- Concentrar tudo em tier-1 nacional (ignora o Claude, que prefere trade/nicho).
- Reportar clipping (volume de menções) como resultado — medir share de citação por IA.
- Tratar um pico de cobertura como suficiente — a janela é de semanas.

---

## 6. Aplicação no curso-factory

- **Conteúdo de curso (GEO/marketing):** este doc é fonte para os números 84% / 27% / 0,3% / 2%, substituindo formulações vagas como "a maioria das citações vem de terceiros". Material de aula de alto valor — um módulo "Por que a IA confia no jornalista e ignora o seu anúncio" é forte candidato.
- **Portal do cliente:** a seção de cobertura de imprensa no `llms.txt` deve listar cada cobertura datada (veículo + título + data), priorizando veículos de tendência/setor.
- **Propostas comerciais:** o EMGE e os KPIs K-EM dão lastro empírico ao argumento de que PR vira pipeline mensurável.

> **Disclaimer de número:** alguns posts de divulgação arredondam para "84% earned" (mai/2026) e outros para "25%" (jornalismo, mar/2026) conforme o recorte da edição. Número canônico Brasil GEO: **earned media 82-89% (84% mai/2026), jornalismo 25-27%, paid 0,3%, não-pago 99%**.

---

*Fim do documento. Próxima revisão: quando a Muck Rack publicar a próxima edição do "What is AI Reading?".*
