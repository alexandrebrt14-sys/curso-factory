# Frontend Playbook — Boas práticas, stacks premium e processo

Documento canônico de **layout, UX, navegabilidade, stacks de frontend, animação, acessibilidade e — sobretudo — processo de auditoria** para qualquer trabalho visual. Como este repositório é um **gerador** (templates Jinja → React/Tailwind), o objetivo é que **todo curso gerado já nasça** com estas práticas embutidas nos templates. Consolida aprendizados reais (incluindo erros recorrentes) para que não se repitam.

> Regra-mãe: **qualidade visual não é opinião, é verificação.** Contraste, legibilidade e "o conteúdo aparece" se medem no navegador renderizado, nos dois temas — não se confia no olho nem na leitura do código. Num gerador, isso significa: corrija no TEMPLATE e audite a SAÍDA renderizada.

---

## 1. Layout, UX e navegabilidade

- **Mobile-first de verdade.** Coluna estreita primeiro; desktop é progressive enhancement. Teste ≤ 390px e ≥ 1280px. Sem overflow horizontal; toque ≥ 44px.
- **Hierarquia visual explícita.** Um H1 por página; H2/H3 mapeando a estrutura; espaçamento por proximidade. Página compreensível em 5s de scan.
- **Navegabilidade de conteúdo longo (cursos!):** índice/TOC com âncoras, "voltar ao topo", navegação entre módulos/aulas clara (anterior/próximo), progresso visível. Resumo/objetivos no topo de cada módulo.
- **Legibilidade de leitura longa:** largura de medida confortável (~60-75ch), `line-height` ~1.6, **parágrafos justificados** (regra deste repo — ver seção 10), tipografia escalável.
- **Estados tratados:** vazio, carregando, erro, sucesso. Skeletons > spinners.
- **Glossário inline para jargão** na primeira ocorrência, além do glossário final.

## 2. Régua de decisão de stacks 2026 (não use "o mais popular", use o adequado)

Fonte: `C:/Sandyboxclaude/Frontend/MelhoresFrontends.pdf` + experiência. Monte um **portfólio de renderização** coerente com densidade, cadência e nível de edição.

**Renderização:** SVG = KPIs, fluxogramas leves, overlays, SEO/a11y (1ª escolha para poucos elementos ricos). Canvas 2D = muitos redraws. WebGL (PixiJS/Three) = 3D/milhares de elementos.

**Dashboards e charts estilo InsightDash:** para telas com densidade executiva, use cards de KPI, sparklines, comparação antes/depois, heatmaps leves e gráficos pequenos combinados com uma leitura executiva. **ECharts** = melhor all-rounder (comece por ele). D3 = custom/gauges. Chart.js = rápido/leve. Plotly = finance/científico. Recharts = React idiomático simples. Design handoff pode nascer em Figma/Sketch/Adobe XD, mas o template final precisa virar tokens e componentes versionados.

**Animação:** **GSAP** = orquestração premium/timeline. Framer Motion = animação declarativa em React. Anime.js = leve. Lottie = marca (não para dados). Regra de ouro na seção 4.

**Fluxograma/diagrama:** **Mermaid = documentação viva, NUNCA editor visual** — fonte pequena/contraste fraco; para fluxograma EXIBIDO num curso, prefira **HTML/CSS** (cartões claros + texto escuro) ou SVG controlado. **JointJS** entra quando o curso precisa de diagrama editável/interativo, conectores reposicionáveis, highlighters, routers/anchors, responsividade e alternância claro/escuro no próprio canvas. React Flow = alternativa open-source quando o caso é editor de nós em React e a licença/peso do JointJS não se justificam. GoJS = editor enterprise pago. Cytoscape = grafos.

**Estado/Build:** Zustand (default leve)/RTK (auditoria). Vite default; Next/Turbopack no ecossistema Next. Lib pesada só com build e justificativa.

**Regra-ouro:** não use a mesma stack para dashboard e editor de fluxograma; em saída estática sem build, prefira CSS a libs pesadas.

### Referências visuais externas (inspiração, não cópia)

- **InsightDash Chart Pack / Envato:** usar como direção para cards de dados, chart packs, hierarquia de métricas e densidade de dashboard. Não copiar asset licenciado para dentro do repo sem licença explícita; recriar como componentes próprios.
- **JointJS Flowchart:** referência para fluxos interativos em que o usuário move nós, alterna tema, acompanha conectores e entende sequência de ações. Use como padrão mental para diagramas vivos, não como dependência obrigatória.
- **Dribbble Flow Diagram:** referência de composição visual: nós claros, contraste forte, conectores legíveis, cor de destaque com parcimônia e espaço suficiente para leitura. Não copiar layout/paleta 1:1.

## 3. Contraste e tipografia — REGRA INVIOLÁVEL

O **erro mais recorrente**. Trate com paranoia — e como é gerador, um erro no template multiplica por todos os cursos.

- **Cor do texto × fundo sempre fortemente contrastantes.** Mínimo **WCAG AA (4.5:1 normal, 3:1 grande)**; mire mais.
- **Dark/light:** NUNCA fixe cor de texto em hex quando o fundo é variável de tema. Use variáveis que **adaptam** ou override `[data-theme]`. Cuidado com variável em **contexto trocado** (ex.: `pre{background:var(--ink-900)}` que inverte para claro no dark e engole o texto do code).
- **Caixa de fundo FIXO exige cor de texto FIXA coerente** (cartão branco → texto quase-preto; cartão escuro sólido → texto branco). Não herdar variável que inverte.
- **Dark mode + container que escurece:** a regra `[data-theme="dark"]` que escurece um bloco tem de clarear TODOS os textos internos — inclusive `<span>`/`<b>` com **cor inline** (regras de `p`/`li`/`td` não os pegam). Use `[data-theme="dark"] #secao [style*="color:#HEX"]{color:CLARO!important}` ou classes.
- **Linhas de tabela / sub-caixas claras** (`#fafafa`/`#f9fafb`) que não escurecem no dark = claro sobre claro. Cubra por tema.
- **SVG `<text>` não herda `fill`** → regra própria por nó; `font-size` generoso no `viewBox`.
- **Especificidade importa:** regra de tema genérica pode vencer a regra de um nó sólido e quebrá-lo. Teste a precedência.

## 4. Animação robusta (CSS-first, à prova de falha)

- **NUNCA esconda conteúdo dependendo de JS para revelar.** Trigger que não dispara = conteúdo some. Incidente real: reveal por GSAP com `opacity:0` + ScrollTrigger que não disparava porque ícones/gráficos mudavam a altura após o load → "carrega e some".
- **Estado base SEMPRE visível.** Entrada via CSS com **`animation-fill-mode: both`** (o `from{opacity:0}` só no `@keyframes`; dispara no load; termina visível). Sem JS/lib = visível.
- **Scroll-reveal com JS:** `immediateRender:false` + safety-net que força visível + testar com layout final rolando tudo.
- **Respeite `prefers-reduced-motion: reduce`** (override que zera animação e força `opacity:1`).
- **Lib pesada só com build/justificativa**; em saída estática, CSS resolve.

## 5. Fluxogramas exibidos: sistema de cartões HTML/CSS

Para fluxograma que o aluno VÊ, prefira HTML/CSS a Mermaid: cartões de fundo claro fixo + texto escuro (ou sólido + branco), setas em `<i>`/SVG, ramos em flex/grid, animação CSS `fill:both`, tipos de nó coloridos sempre com contraste garantido nos dois temas. Mais controle, alto contraste, responsivo, acessível.

Quando o fluxo precisar de **edição, drag, reconfiguração de conectores, seleção, highlighter ou simulação de decisão**, considere JointJS/React Flow em componente isolado e com lazy-load. O aluno deve conseguir ver: estado atual, próximo passo, gargalo, custo, risco e decisão recomendada. Fluxograma bonito que não muda a decisão é decoração.

Padrão visual recomendado:

- Nós com título curto, métrica ou critério de decisão e uma linha de consequência.
- Conectores com rótulo de condição ("se ROI < 12 meses", "se risco regulatório alto").
- Uma legenda compacta para estado, risco, custo e prioridade.
- Dark/light testado: texto, rótulos de conectores e ícones precisam passar contraste nos dois temas.
- Mobile: reempilhar em trilha vertical ou permitir pan/zoom controlado, nunca overflow horizontal invisível.

## 6. Processo de AUDITORIA VISUAL ROBUSTA (o que mais falha)

Num gerador, audite a **saída renderizada**, não o template "no papel".

1. **Auditor renderizado, página inteira, dois temas.** JS sobre `getComputedStyle` de todos os textos folha; compor alpha sobre o fundo efetivo; pular gradientes; classificar large vs normal; ratio WCAG; listar `< AA`. Alterne `data-theme` dark E light. Meta: **0 falhas reais**.
2. **Mate transições/animações antes de medir.** `transition: background-color 360ms` no body faz `getComputedStyle` ler o fundo ANTIGO em transição → **falsos positivos**. Injete `*{transition:none!important;animation:none!important}`, troque o tema, force reflow (`void document.body.offsetHeight`), meça.
3. **Cuidado com cache.** Medição idêntica após deploy = cache. Use cache-bust (`?v=...`).
4. **Itere até zerar.** Corrigir template → regerar → re-auditar → repetir.
5. **Corrija na RAIZ (template), não na saída** — e não hex-a-hex. Override por seção+tema; caixa fixa → texto fixo; variável em contexto trocado → corrigir. Se usar `[style*="..."]`, case por HEX e confirme no navegador (formato com/sem espaço quebra em silêncio).
6. **Ao consertar 1 exemplo, varra TODOS os irmãos** (todos os templates/cursos afetados).
7. **Não mexa às cegas.** Validar renderizado; corrigir assumindo fundo errado introduz novo bug.

## 7. Catálogo de erros frequentes (sintoma → causa → correção)

| Sintoma | Causa raiz | Correção |
|---|---|---|
| Texto some no tema escuro | cor fixa escura, ou `<span>` inline não coberto por regra de tema | variável que adapta / override `[data-theme]` por atributo |
| Texto claro sobre fundo claro no light | seção/template estilizado só para dark; `var` de fundo "dark-first" sem override light | override `[data-theme="light"]` |
| Fluxograma/figura "carrega e some" | reveal por JS esconde via `opacity:0` e trigger não dispara | animação CSS `fill:both`; estado base visível |
| Code/`pre` ilegível no dark | `background:var(--ink-900)` que inverte | fundo escuro FIXO no `pre` |
| Auditoria "não acha" / "acha demais" | medir durante transição; cache; um tema só; `[style*=]` com formato errado | matar transições + reflow; cache-bust; dois temas; casar por HEX e validar |
| Nós sólidos com texto escuro | regra de tema genérica mais específica venceu | aumentar especificidade do nó / restringir genérica |
| Número/simulação que "não fecha" | aritmética publicada sem conferência | refazer a conta; mostrar premissas; não publicar número não verificado |
| Acentuação faltando em geração longa | sub-agente "esquece" a regra de PT-BR | carimbar a regra explícita no prompt; validar contagem de acentos |
| Parágrafo não justificado | template não aplicou `text-justify`/`align="justify"` | garantir no template (ver seção 10) |

## 8. Acessibilidade (WCAG 2.2 = decisão de produto)

Reflow, contraste não-textual (3:1 em bordas/ícones), teclado, foco visível, target ≥ 24px, `prefers-reduced-motion`. Gráficos/fluxogramas: teclado, descrição alternativa, não depender só de cor. `role`/`aria-label` em interativos e SVGs informativos. Em curso, legendas/transcrições para mídia.

## 9. Performance e FinOps

Performance budget desde o início; lazy-load abaixo da dobra; imagens otimizadas; preload de fontes críticas. **FinOps:** agrupe regenerações/builds; rode o gate local antes; respeite o `FINOPS.md` do repo.

---

## 10. Aplicação neste repositório (curso-factory)

Este repo **gera** cursos (templates Jinja → React/Tailwind/Next). Corrija sempre no **template**, para que toda saída herde a prática.

- **Parágrafos justificados (regra do repo):** corpo de texto sai justificado. React/Tailwind → `className="text-justify"` (NÃO `align="justify"` em JSX). Export HTML/PDF/e-mail → literal `<p align="justify">`. O `FormattedText`/`page.tsx.j2` já deve cumprir; ao criar template novo, replicar. Esta regra vale junto com a camada editorial: PT-BR acentuado, didática para adultos, storytelling funcional e metáforas úteis.
- **Contraste no template de tema:** defina tokens de cor que adaptam (`--ink-*`, `--bg`) com override `[data-theme="light"]`/`[data-theme="dark"]`; garanta que cartões, callouts, tabelas e blocos de código respeitem a seção 3 nos DOIS temas. Bloco de código (`pre`) com fundo escuro FIXO.
- **Animação no template:** entradas via CSS `animation-fill-mode: both` (nunca esconder dependendo de JS); reveal com framer-motion só com `whileInView` + `once` que termina visível; respeitar `prefers-reduced-motion`.
- **Fluxogramas/diagramas dos cursos:** HTML/CSS (cartões alto contraste) em vez de Mermaid exibido.
- **Auditoria da saída:** após gerar, abra o curso no navegador e rode a auditoria da seção 6 (dois temas, transições mortas) — o defeito no template aparece multiplicado, então vale ouro pegá-lo cedo.
- **Geração de copy longa:** carimbe a regra de PT-BR acentuado explicitamente no prompt do sub-agente e valide a contagem de acentos (erro recorrente em geração longa).

Memórias de origem (operador): `reference_stacks_frontend_2026`, `feedback_contraste_fontes_frontend`, `feedback_animacao_entrada_nao_esconder`, `feedback_auditoria_robusta_visual`, `feedback_curso_factory_paragrafos_justificados`.
