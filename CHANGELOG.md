# Changelog

Histórico de mudanças relevantes do curso-factory. Formato baseado em [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) e versionamento [SemVer](https://semver.org/lang/pt-BR/).

Histórico narrativo de cada onda em [[Refactor-2026-04-29]] e demais páginas da [Wiki](https://github.com/alexandrebrt14-sys/curso-factory/wiki).

## [Unreleased]

### Alterado — A unidade de medida passa a ser a AULA, e a régua vem da fonte única (2026-08-27)

Os cursos gerados saíam rasos: apresentavam o conceito e não o explicavam. A causa não era o modelo, era a régua. O gate media **módulo** com piso de 2.500 palavras e uma bateria de pisos ("3+ exercícios", "5+ estatísticas", "3+ fontes", "1+ tabela", "1+ blockquote", "3+ blocos visuais"), e o prompt dava cota de palavras por parte. Cota se cumpre com abrangência, não com explicação: o redator listava seis conceitos em vez de explicar um, e emendava exercício em cima de exercício sem narrativa no meio.

A unidade agora é a **aula** do tipo D da fonte única de estilo (`alexandrebrt14-sys/escrita-empreendedor`, hash `a10ed133…`): piso 900 · alvo 1.200-2.400 · aviso 2.400 · erro 3.600 palavras; 2 a 4 H2; até 2 H3 por H2; até 3 apoios visuais; parágrafo de 15 a 45 palavras; 1 exercício por aula; 1 fonte datada e 1 cápsula por trilha; trilha de 4 a 6 aulas, 6.000-12.000 palavras, 30-60 min.

- **Nenhum número da régua mora mais neste repositório.** `config/lexicos.json` é espelho gerado da fonte (`python -m escrita.cli lexicos --json`) e `src/validators/lexicos_loader.py` o lê em runtime. `content_checker` tira dali piso, alvo, aviso, erro, H2, H3 por H2, teto de visuais e faixa de parágrafo, e **interpola o valor carregado na mensagem de erro** — código, configuração e mensagem não conseguem mais divergir. As constantes `FALLBACK_*` só entram se o espelho sumir.
- **Pisos viraram tetos.** Tabela, blockquote, estatística e fonte deixaram de ser obrigatórios: entram quando substituem texto ou respondem à pergunta do exemplo. "3+ blocos visuais" virou "até 3, e só quando substituem texto". "Mínimo 3 exercícios" virou 1, o "faça agora" de 5 a 15 minutos.
- **Compatibilidade com "módulo".** O pipeline ainda entrega módulos, então `check_content(..., unidade="modulo")` mede a peça como 4 a 6 aulas (4.800-14.400 palavras, piso 3.600, erro 21.600). `QualityGate.check_text` usa `unidade="modulo"` por padrão para não reprovar o acervo; quando o gerador emitir aula, o chamador passa `unidade="aula"`.
- **Parágrafo mede palavras, não linhas.** Contar linhas media a largura da janela de quem escreveu. A faixa é 15-45 palavras (`tetos.D.paragrafo`); `voice_guard` acompanha pelo mesmo import.
- **Anti-clichê deixou de ter duas cópias.** As 21 expressões que a fonte já trazia saíram de `config/quality_rules.yaml` e as 5 que ela cobria saíram de `FORBIDDEN_CLICHES`; a união em runtime tem três origens e uma poda de substring, para que "em um mundo cada vez mais" não seja cobrado duas vezes por conter "cada vez mais".
- **`DIRETRIZ_EDITORIAL.md` e `GUIA_ESCRITA_HUMANIZADA.md` viraram ponteiros** para a fonte, com hash e data de sincronização, guardando só o que é específico do motor de cursos. A bibliografia datada do guia desceu para `docs/research/HUMANIZACAO_AI_ESTADO_DA_ARTE_2026.md`.
- **Prompt de redação reescrito** (`src/templates/prompts/draft.md` e `pt-br/draft.md`): sequência do molde D (uma frase do que vai aprender; a ideia explicada com origem, custo, mudança e erro comum; o exemplo do negócio do aluno contado por inteiro com número; "faça agora" em etapas com o resultado esperado; resumo de 3 a 5 linhas), 1.200-2.400 palavras pedidas explicitamente, sem cota por parte.
- **`output/` saiu do índice do Git.** Sete rascunhos gerados estavam versionados apesar de `.gitignore` já os excluir.


### Adicionado — Contrato de geração com bloco visual e cobrança da régua (2026-08-17, PR #67)

A doutrina do PR #66 virou código. Até aqui o gerador emitia cinco tipos de bloco, todos de prosa ou código, e nenhum contava como peça visual: curso gerado pelo caminho padrão nascia reprovado na própria régua da casa.

- **Seis tipos visuais no contrato:** `figure`, `dataTable`, `comparison`, `statGrid`, `stepGuide` e `timeline`, exatamente os que o portão `gate-peso-visual.mjs` da landing conta. `figure` leva a imagem em `value` e a legenda em `label`; os outros cinco levam a estrutura em `data`. O modelo recusa bloco que sairia vazio (payload ausente, linha de tabela com tamanho diferente do cabeçalho, figura sem legenda), porque o motor da landing degrada bloco sem carga para nada, sem erro e sem console.
- **Quatro lugares que mudam sempre juntos** ao criar ou alterar tipo: `src/models.py` (enum e conjuntos `VISUAL_SECTION_TYPES`/`PAYLOAD_SECTION_TYPES`), `src/schemas/course.schema.json` (mesmo enum, com regra condicional de payload por tipo), `src/templates/page.tsx.j2` (o `switch (section.type)`) e o filtro `js_json` de `src/generators/tsx_generator.py` (serialização da carga). Mexer em um só produz bloco que o validador aceita e a página não desenha, ou o contrário.
- **Promoção automática no parser:** tabela em Markdown vira `dataTable`, lista numerada de passos vira `stepGuide` sob critério conservador, imagem com legenda vira `figure`. Carga que não bate mantém o conteúdo como `text` em vez de deixar a exceção subir. `comparison`, `statGrid` e `timeline` **não** são promovidos, por decisão: nenhuma construção de Markdown os sinaliza sem ambiguidade, e promover errado é pior que não promover. Entram por autoria explícita.
- **`visual_density` deixou de ser declarativa.** `src/validators/visual_density.py` lê a camada do `config/quality_rules.yaml` e `TsxGenerator.render_page` a cobra antes de renderizar: módulo reprovado levanta `VisualDensityError` e o curso não chega a virar arquivo. Nenhum dos três limites existe como constante em código. Legado passa com `cobrar_peso_visual=False`, que rebaixa todo achado a aviso no log.
- **`content_checker.MAX_PARAGRAPH_LINES` passou a ler o YAML.** Era constante com um comentário pedindo sincronia manual, e o número já tinha subido de 5 para 8 no arquivo sem o código saber. `voice_guard.py` herda o valor pelo mesmo import.
- **Dois defeitos consertados de raspão:** o prompt do redator mandava formatar tabela como **uma única linha**, o que impedia qualquer promoção a `dataTable`; e a expressão que reconhece cerca de código não casava em arquivo com quebra CRLF.

### Adicionado — Doutrina visual dos cursos gerados (2026-08-17, PR #66)

- **[`docs/DOUTRINA_VISUAL_CURSOS.md`](docs/DOUTRINA_VISUAL_CURSOS.md):** três limites verificáveis por máquina para todo curso novo: nenhum parágrafo acima de 1.200 caracteres (medida de tela, o que cabe num celular de 390 pontos sem rolagem interna), ao menos três blocos visuais por módulo e ao menos um bloco visual a cada 2.500 caracteres de prosa. O documento registra o caso que motivou a régua (`motor-de-crescimento-ia` publicado com 114 blocos de prosa acima do teto, o maior com 3.492 caracteres, e nenhuma figura, aprovado por todos os portões existentes) e a varredura do acervo, em que 26 dos 52 cursos medidos não tinham um único bloco visual.
- **`DIRETRIZ_EDITORIAL.md` §11.1:** forma curta e normativa da doutrina, para quem lê a diretriz e não o documento longo.

### Corrigido / Qualidade — Diretriz editorial v4: prova antes da escrita, promessa antes do esqueleto, config que finalmente é lida (2026-08-11)

Segunda rodada do mesmo dia, com a doutrina completa do curador aplicada de ponta a ponta e um achado de governança que explica parte do problema original.

- **Achado: `config/quality_rules.yaml` não era lido por nenhum código.** As "46 expressões banidas com gate de CI" eram, na prática, as 18 hardcoded em `content_checker.FORBIDDEN_CLICHES`. As 28 restantes nunca foram checadas, incluindo "especialistas apontam" e "estudos indicam", que a própria doutrina classifica como marcador grave de atribuição vaga. `require_source_for_percentages` e `fail_if_unresolved_markers_above` eram texto sem efeito. Corrigido com `src/validators/rules_loader.py` (carrega o YAML em runtime, com `lru_cache` e fallback para `{}` sem levantar exceção) e com a implementação dos dois checks: percentual sem sinal de fonte na mesma frase vira aviso (teto de 5 por documento, mensagem citando as quatro conferências), e marcador aberto acima do teto vira erro bloqueante. Lista ativa de expressões passou de 18 para 56, com as 10 novas de escassez fabricada e convite vazio.
- **Prova antes da escrita (§2.2)** — o material de evidência é levantado antes da primeira frase e limita o tamanho da peça: blocos que afirmam resultado em número menor ou igual ao de provas datadas. Quatro saídas antes do marcador (pesquisar, reduzir, restringir, segurar), marcador no lugar do dado e nunca da seção, teto de cinco, e divisão explícita entre `[FALTA EVIDÊNCIA:]` (pesquisa resolve) e `[PREENCHER-HUMANO:]` (só o autor humano tem).
- **Promessa e tensão antes do esqueleto (§3.1)** — teto de 12 palavras na manchete e portão de três condições antes de publicar promessa: experiência que o cliente reconhece, medida que a representa, rota de reparação quando falha. A tensão vem depois da promessa e antes do mecanismo, apontando custo presente em vez de castigo futuro; escassez fabricada foi vetada com a família inteira.
- **Esqueleto por gênero (§3.2), abertura (§3.3) e caso condutor (§3.4)** — ordem de blocos declarada para página comercial, artigo e aula; cena curta, banal e datada, com a regra gramatical de que o sujeito de toda frase sobre falha é um artefato ou um processo, nunca a pessoa; caso condutor único e rotulado como real (nome e fonte) ou hipotético (rótulo repetido colado a cada número, porque o número vira print e o print viaja sem cabeçalho).
- **Um pedido por peça (§3.6)** — fórmula de quatro peças (verbo de ação, valor concreto, tempo ou esforço, risco removido), lista de verbos que servem e veto a "saiba mais", "descubra o poder", "transforme" e "não perca". Opções equivalentes lado a lado são adiamento disfarçado de escolha.
- **Travas de revisão verificáveis (§13)** — porcentagem com origem, data, método e denominador na mesma frase; base pequena contada em unidades; rótulo em todo exemplo inventado, inclusive saída de cálculo; identificadores conferidos antes de citar; e o teste do parágrafo solto para frases de prova, limite e preço, com público, condição e exceção viajando dentro da mesma sentença.
- **Ajuste de pontuação** — travessão passa a ser vetado em prosa e tolerado em título e cabeçalho de seção. Uma analogia por peça, pertencente ao conceito central.
- **Propagação** — `draft.md`, `review.md` e `analyze.md` em `pt-br/`, raiz, `en/` e `es/`; `CLAUDE.md`, `AGENTS.md`, `GEMINI.md` e o anexo `GUIA_ESCRITA_HUMANIZADA.md`. Suíte: **277 passed, 7 skipped** (+10 testes novos dos validadores).

### Corrigido / Qualidade — Diretriz editorial v3: narrativa obrigatória, fim das cotas mecânicas (2026-08-11)

O curador reportou queda de qualidade nos textos gerados pelo pipeline. A causa não era falta de regra, era o tipo de regra: as instruções de estilo tinham virado aritmética, e o que era medida de diagnóstico virou fórmula de produção. Detalhe do diagnóstico em [`wiki/decisions/diretriz-editorial-v3-narrativa-sem-cota.md`](wiki/decisions/diretriz-editorial-v3-narrativa-sem-cota.md).

- **Bug de corrupção de texto no `accent_checker.py`** (achado colateral, o mais caro do lote). O `ACCENT_MAP` tratava homógrafos como erro de digitação e o gate roda com `auto_fix=True`, então cada curso gerado saía com erro de gramática introduzido pelo próprio validador: "nos projetos" virava "nós projetos", "esta análise" virava "está análise", "seria bom" virava "séria bom", o imperativo "Analise os dados" virava "Análise os dados". Descoberto ao rodar o validador contra a diretriz nova, que acusou 14 erros, todos falsos. Os nove pares ambíguos (`nos`, `esta`, `seria`, `analise`, `pratica`, `pratico`, `publico`, `valido` e a entrada no-op `ele`) saíram do dicionário de correção para `AMBIGUOUS_HOMOGRAPHS`, e o `review.md` ganhou a tabela de desambiguação por classe gramatical: regex cuida do inequívoco, contexto é trabalho do revisor LLM. Dois testes de regressão novos.
- **Piso de substância (§2.1 da diretriz)** — a doutrina era feita quase só de mecanismos de reprovação: 46 expressões banidas com `fail_on_found`, orçamento de formatação, tetos e trava de estilometria, sem nenhuma regra dizendo o que a peça precisa ter. As cinco camadas do quality gate medem forma e nenhuma mede argumento, então módulo curto, uniforme e sem tese passa em todas. Entram seis requisitos positivos (tese identificável, evidência ligada à tese, ganho de informação, critério de decisão explícito, arco de leitura, consequência executável), a regra de precedência "em conflito, o piso vence" e uma dimensão nova de aprovação no `analyze.md` (`substancia_narrativa`), que é a única camada capaz de medir substância por ser LLM e não regex. O `review.md` passa a verificar o piso antes de qualquer corte e a reportar os itens ausentes.
- **`DIRETRIZ_EDITORIAL.md` v3** — nova §3 (narrativa: abertura em situação, tensão antes da solução, caso condutor, promessa cumprida, fechamento com callback, mostrar em vez de qualificar); §4.1 troca o limiar único de amplitude por diagnóstico em duas faixas (abaixo de 15 é defeito, acima de 30 é folgado) e proíbe combiná-lo com qualquer outra regra de comprimento, porque o conjunto anterior era aritmeticamente insatisfazível: crescimento por frase mais ração de frase curta produzia amplitude de 13 a 16, e a mesma tabela reprovava abaixo de 30; §4.7 impede que medição do próprio corpus vire regra sem passar pelos testes de registro e de compatibilidade, e §4.8 veta cota mecânica de ritmo; §6 recoloca tabela, matriz de decisão e checklist como ferramentas obrigatórias quando há comparação, escolha ou passo verificável, separando o que é trabalho de prosa do que é trabalho de estrutura; §9 explica como cápsula de resposta para motores generativos convive com abertura narrativa. A diretriz passa a ser fonte única, com prompts e resumos subordinados.
- **`GUIA_ESCRITA_HUMANIZADA.md`** — seção 3 nova (tabela das seis técnicas narrativas com exemplo antes e depois), seção 2 reescrita com o contraexemplo de staccato, seção 8 passa a listar cota de ritmo entre as modinhas sem evidência.
- **Prompts do pipeline** (`draft.md`, `review.md`, `humanize.md` em `pt-br/`, raiz, `en/` e `es/`) — removidas as regras "uma frase de 6 palavras ou menos em CADA parágrafo", "nunca duas frases consecutivas na mesma faixa de comprimento", "parágrafo com no máximo 5 linhas", "sub-heading a cada 2-3 parágrafos" e "nunca mais de 3 parágrafos sem elemento visual". Entraram seções de narrativa, de ritmo diagnóstico e de estruturas vetadas (travessão, antítese em série, tríade de ritmo, conclusão-espelho, anglicismos de pontuação, vícios de português de LLM). Os exemplos internos dos prompts foram corrigidos, porque ensinavam travessão pelo exemplo enquanto o texto proibia.
- **`humanizer.py`** — `_build_diagnostic` deixou de mandar "adicione 1-2 frases curtas por seção" e "substitua termos repetidos por sinônimos" (esta última contradizia a regra de coerência terminológica do próprio `draft.md`); agora aponta o trecho uniforme e manda reescrever a estrutura. Fallback inline alinhado.
- **`stylometry_checker.py`** — mensagens de erro e aviso reescritas: a métrica continua sendo medida e reportada, mas deixou de instruir cota. O aviso de "zero frases curtas" virou sinal para inspecionar, não ordem para inserir.
- **`content_checker.py` / `voice_guard.py` / `quality_rules.yaml`** — teto de parágrafo de 5 para 8 linhas, com a constante única `MAX_PARAGRAPH_LINES` espelhada no YAML; a mensagem pede verificação de assunto duplo em vez de quebra automática.
- **`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`** — três blocos editoriais sobrepostos e divergentes viraram um, apontando para a diretriz; `writer.py` e `reviewer.py` tiveram os fallbacks inline alinhados.

### Corrigido / Qualidade — Onda de hardening + tooling de lint (2026-06-08)

Revisão transversal do código de produção (auditoria multiagente: arquitetura, robustez, testes, docs, segurança/FinOps) seguida de correções cirúrgicas de alto valor e baixo risco. Suíte: **232 → 245 passing** (+13), zero regressões.

- **Bugs reais corrigidos:**
  - `src/agents/humanizer.py` — chamava `self.client.completion(...)`, método inexistente em `LLMClient`; o `except Exception` engolia o `AttributeError` e o humanizer **falhava silenciosamente em toda execução** com cliente real (retornava sempre o texto original). Agora usa `self.client.call(self.provider, prompt, model=...)`.
  - `src/indexer/course_indexer.py` — `validate_config()` referenciava `_ENV_PATH` (nome nunca definido) → `NameError` no caminho de erro de config ausente. Corrigido para `_PROJECT_ROOT / ".env"`.
  - `src/cache.py` — comparação de TTL `>` tornava `test_cache_expira_apos_ttl` **flaky** (com `ttl=0`, `0.0 > 0` é falso quando set/get caem no mesmo tick). Trocado por `>=` (semântica correta: `ttl=0` expira imediatamente); determinístico em 5/5 execuções.
- **Robustez (aditivo, sem mudança de comportamento existente):**
  - `LLMClient` ganhou `close()` + protocolo de context manager (`__enter__`/`__exit__`) + `__del__` defensivo — fecha o `httpx.Client` e evita vazamento de conexões TCP ao processar muitos cursos no mesmo processo.
- **Refatoração de baixo risco:**
  - `course_indexer.py` — extratores de campo (`_extract_str`/`_extract_int`/`_extract_tags`) movidos de closures-dentro-do-loop (padrão frágil, B023) para funções de módulo testáveis.
  - `tests/test_voice_guard.py` — movido de `src/validators/` para `tests/` (teste não deve viver no pacote de produção).
- **Tooling de qualidade formalizado:**
  - `pyproject.toml` — config `[tool.ruff]` (regras E/W/F/I/UP/B, `per-file-ignores` para E402 legítimo de `sys.path`/`load_dotenv`, exclusão de `scripts/legacy`) + `[tool.pytest.ini_options]`. **Código de produção 100% limpo no ruff** (153 → 0 issues em `src/tests/cli`): imports ordenados (isort), anotações modernizadas (`Optional[X]`→`X | None`, `timezone.utc`→`UTC`), f-strings/vars/imports mortos removidos, `zip(strict=)` explícito, exceções específicas nos testes (`AttributeError`/`ValidationError` no lugar de `Exception` cego).
- **Testes novos (+13):** `tests/test_indexer.py` (9 — parser de TSX antes sem cobertura) e `tests/test_agents_robustez.py` (4 — regressão dos fixes do humanizer e do ciclo de vida do `LLMClient`).
- **Docs:** README — bloco "Uso (CLI)" reescrito com os subcomandos reais (`batch`, `clients`, `drafts-to-tsx`, `emit-catalog`, `emit-llms-txt`); removidos comandos fantasma (`create-module`, `run-step`, `status`) e a sintaxe obsoleta `create --config --course`.

### Adicionado — Citabilidade GEO operacional + KB V3 (2026-06-03)

**Fecha o gap entre a doutrina de GEO e o que o pipeline produz/valida.** O confronto com o conhecimento mais novo dos repos irmãos (`landing-page-geo`) mostrou que as "promessas de pipeline" do log de 2026-05-20 nunca tinham saído do papel. Esta wave implementa e adiciona o estado da arte de 20-mai a 03-jun-2026.

- **Documentação canônica nova (3 docs):**
  - [`docs/GEO_REDACAO_CHECKLIST_2026.md`](docs/GEO_REDACAO_CHECKLIST_2026.md) — rubrica empírica de 13 técnicas de redação com lift de citação medido (Aggarwal/Princeton, AutoGEO ICLR 2026, GEO-SFE/Berkeley), mapeada para módulos de curso, com números-alvo que viram gate.
  - [`docs/GEO_KNOWLEDGE_BASE_2026_V3.md`](docs/GEO_KNOWLEDGE_BASE_2026_V3.md) — V3 prevista pela V2: AutoGEO (GEO Score/GEU Score, +50,99%), earned media 84% (Muck Rack), Selection Rate × Absorption Rate (SIGIR 2026), super-geo (severidade + 4 tiers), Karpathy LLM Wiki (ingest/query/lint), Multi-LLM Sampling Wave, conceitos 51-63, papers Q2 2026 (FeatGEO, GhostCite, SIGIR AIO 51,5%), descobertas pós-I/O.
  - [`docs/GEO_EARNED_MEDIA_2026.md`](docs/GEO_EARNED_MEDIA_2026.md) — earned media = 84% das citações de IA (paid = 0,3%); framework EMGE, técnicas de colocação, KPIs K-EM-001 a 006.
- **`draft.md`** — nova seção "Checklist de Citabilidade GEO" (Cite Sources ≥3, Statistics ≥5, Quotation ≥1, answer capsule por H2, chunkability, Single Idea, Information Gain) + 4 itens na autoavaliação.
- **`content_checker.py`** — contadores `_count_cite_sources` / `_count_statistics` / `_count_quotations` + detector `_has_answer_capsule`; bloco GEO opt-in em `check_content(..., geo_config=...)` — erro bloqueante com playbook ligado, aviso quando desligado, ausente = retrocompatível.
- **`Geo2026Config`** — novo bloco `geo_2026` em `client.yaml` (`princeton_playbook_enabled`, `min_cite_sources/statistics/quotations`, `require_answer_capsule`, `schema_authority_stack_enabled`), carregado por `context.py` + `loader.py` e consumido pelo `quality_gate.py`. Ligado no cliente `default`, documentado e off no `_template`.
- **`classify.md`** — tags canônicas de GEO (`geo-2026`, `citation-ready`, `aeo`, `aso`, `b2a`, `entity-drift`, `query-fan-out`).
- `tests/test_validators_smoke.py` — **7 testes novos** (contadores, comportamento opt-in bloqueante/aviso, retrocompatibilidade sem config). Suíte: **213 passing** (+7; 1 flaky pré-existente de TTL de cache, não relacionado).

### Adicionado — Wave de Humanização (2026-05-17)

**Pipeline de medição e correção de "cara de IA" baseado em evidência científica 2024-2026** (papers ACL/EMNLP/NAACL/NeurIPS, datasets RAID/MULTITuDE/M4GT, benchmarks com Cohen's d). Dossiê técnico em [`docs/research/HUMANIZACAO_AI_ESTADO_DA_ARTE_2026.md`](docs/research/HUMANIZACAO_AI_ESTADO_DA_ARTE_2026.md) (1.014 linhas, 8.834 palavras, 21 papers, 9 datasets, 5 leaderboards, fórmulas formais + thresholds + corpora PT-BR + design de experimento de calibração).

- **PR-1 (XS)** — Burstiness control nos prompts do redator: nova seção "Cadência e Burstiness — INVIOLÁVEL" em `src/templates/prompts/draft.md` + traduções `pt-br/`, `es/`, `en/`. Instrui o LLM a variar comprimento de frase 4-35 palavras, garantir 1 frase ≤6 palavras por parágrafo, alternar faixas curta/média/longa. Ataca diretamente a métrica do GPTZero (`σ/μ` em comprimento de sentença).
- **PR-2 (M)** — `src/validators/stylometry_checker.py` (350 linhas, pure-Python). Mede 4 métricas estatísticas de "humanidade" — burstiness (Goh-Barabási 2008 + variante GPTZero), sentence-length variance, type-token ratio, repetition score (bigramas boilerplate). Backend opt-in para perplexity real via `lmppl` com `pierreguillou/gpt2-small-portuguese`. Integrado ao `quality_gate` como **camada 5** (report-only por default — bloquear só após calibração com 30+30+20 docs).
- **PR-5 (S)** — `voice_samples` no schema `client.yaml` (`VoiceSample`, `VoiceSamplesConfig` em `src/clients/context.py`). Permite anchor de 800-1500 palavras de escrita real do autor canônico para few-shot persona-conditioning. Estratégias `rotate | concat | random`. Default OFF; cliente declara amostras em `docs/voice/<cliente>/`.
- **PR-6 (S)** — `src/validators/disclosure_checker.py` (220 linhas) + integração `quality_gate` **camada 6**. Verifica presença do bloco padronizado de disclosure de IA exigido por **PL 2338/2023** (Marco Legal da IA, Brasil), **Posicionamento CFP 03/07/2025** (conteúdo psicológico), **Marco Referencial MEC 2025** (Educação Básica). Cobertura: autor canônico, credencial, norma citada, revisor humano. Modo report-only por default; `block_if_missing=true` para enforcement. Helper `build_disclosure_block()` gera o bloco parametrizado. `review.md` instrui Claude a inserir o bloco se ausente.
- **PR-4 (L)** — `src/agents/humanizer.py` (300 linhas) — agente de pós-processamento multi-pass com detector-in-the-loop. Roda **depois** do reviewer; mede stylometry, se score < target dispara reescrita instruída via Claude Opus 4.7 com diagnóstico cirúrgico (qual métrica está ruim, como corrigir). Itera até `target_score` ou `max_iters`. Opt-in via `client.yaml > pipeline.humanize_enabled`. Prompt em `src/templates/prompts/humanize.md` + tradução `pt-br/`. Inspirado em DIPPER (Krishna NeurIPS 2023) + Adversarial Paraphrasing 2025 (arXiv:2506.07001).
- **PR-8 (S)** — `src/detection_tracker.py` (210 linhas) — persiste `output/.detection/history.jsonl` análogo ao `cost_history.jsonl`. Cada run do quality_gate registra stylometry/voice_guard/disclosure score + aprovação + versão pipeline + client_id. Novo subcomando `python cli.py detection-report [--since YYYY-MM-DD] [--client ID]` agrega por cliente/curso com medianas e tendências, para auditar drift de qualidade quando algum LLM da banca muda.
- **PipelineConfig** novo bloco em `client.yaml > pipeline`: `humanize_enabled`, `humanize_target_stylometry_score`, `humanize_max_iters`.
- `tests/test_humanization_pipeline.py` — **33 testes novos** cobrindo fórmulas isoladas (burstiness Goh + GPTZero, TTR, repetition), `stylometry_check` em texto humano-like vs LLM-uniforme, `disclosure_check` em modos report-only e block, `voice_samples` schema, `detection_tracker` persistência+filtros+atalho de gate, `humanizer` diagnostic builder + short-circuit quando texto já atende target, `humanize_if_enabled` default OFF.

Suite total: **199 testes passing** (era 166 antes desta wave; +33 novos, 0 regressões).

### Adicionado — Templates GitHub e governança
- Templates GitHub: `.github/ISSUE_TEMPLATE/` (bug, feature, question, config), `pull_request_template.md`, `dependabot.yml`.
- `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`.
- 5 issues epic abertas para waves 6-10 (engagement, tutor IA, multi-idioma, certificação, comunidade).
- 4 milestones (v1.0 / v2.0 / v3.0 / v4.0) atribuídos às issues correspondentes.
- Project board público "curso-factory roadmap" com 19 itens.

### Mudado
- Topics do repo atualizados: `python, llm, openai, anthropic, claude, gemini, perplexity, groq, education, course-generation, multi-tenant, jinja2, pydantic, brasil-geo, portuguese, quality-gate, finops, cli, geo, aeo`.
- Description e homepage URL apontando para a Wiki.

### Segurança
- `dependabot.yml` configurado para atualização semanal de pip e GitHub Actions.
- Dependabot security updates habilitado.

## [1.0.0] — 2026-04-29

Refatoração profunda em 5 waves para tornar o curso-factory base reusável de outros portais educacionais. Detalhes completos em [Wiki / Refactor-2026-04-29](https://github.com/alexandrebrt14-sys/curso-factory/wiki/Refactor-2026-04-29).

### Adicionado
- 50 testes novos (24 → 74 totais): `test_cli.py` (11), `test_parsers.py` (14), `test_converters.py` (7), `test_cost_cache.py` (8), `test_validators_smoke.py` (10).
- `scripts/legacy/` com README explicando scripts ad-hoc preservados.
- Wiki completa (22 páginas, ~5.500 linhas): Home, Quick-Start, Architecture, CLI-Reference, Multi-Client-Setup, Pipeline-and-Agents, Quality-Gate, FinOps-and-Caching, Reusing-for-New-Segment, Testing, Project-Structure, Roadmap-and-Gaps, Refactor-2026-04-29, FAQ, Glossario, API-Reference, Prompt-Engineering, Observability-and-Debug, Lessons-Learned, Benchmarking-2026.

### Mudado
- `cli.py` reescrito (415 linhas) com imports corretos para todos os 8 subcomandos.
- `cmd_validate` agora usa `QualityGate` real (acentos + conteúdo + links + voice guard).
- `cmd_cost_report` lê o log JSON real do `CostTracker`.
- `cmd_batch` usa `CourseFactory` com `client` e `course_config` separados.
- `cmd_cache_clear` usa `Cache.clear()` real.
- `writer.py` e `reviewer.py` adotam `**template_vars` para paridade com Researcher/Analyzer/Classifier.
- `LLMClient` ganha `Cache` plugado por padrão (`use_cache=True`).
- `models.py:CourseDefinition` — defaults de identidade ("Alexandre Caramaschi", "Brasil GEO") zerados; quem instancia precisa injetar via `ClientContext`.
- `SchemaBuilder` ganha clamp `max(30, duracao)` paritário com `convert_drafts_directory`.
- `datetime.utcnow()` migrado para `datetime.now(timezone.utc)` em `cost_tracker.py`, `orchestrator.py`, `models.py`, `quality_gate.py` (zero `DeprecationWarning`).
- `docs/ARCHITECTURE.md` reescrito como guia portal-agnóstico.
- `README.md` ganha badge de status atualizado.
- `CLAUDE.md` ganha registro da refatoração no topo.

### Corrigido
- 4 subcomandos do CLI antes quebrados por imports inexistentes (`validate`, `cost-report`, `batch`, `cache-clear`):
  - `from src.validators.quality import QualityValidator` → `src.validators.quality_gate.QualityGate`
  - `from src.validators.accents import AccentValidator` → `src.validators.accent_checker`
  - `from src.config import load_config` → `src.config` não tem `load_config`; uso correto via `OUTPUT_DIR`/`CACHE_DIR`
  - `from src.agents.cost_tracker` → `src.cost_tracker`
- `cmd_cost_report` chamava API fictícia (`tracker.generate_report()`, `report.by_provider`); refatorado para usar `tracker.report()` real + agregação manual do log.

### Removido
- `src/unified_finops.py` — adapter para `geo-finops` calls.db unificado, zero referências, dependência implícita em path absoluto Windows.
- `Orchestrator._build_writer_context` — método de 19 linhas nunca chamado.
- 4 scripts ad-hoc movidos para `scripts/legacy/`: `clean_markdown_for_tsx.py`, `convert_drafts_to_tsx.py`, `generate_joias_course.py`, `generate_joias_course_v2.py`.

## [0.x.x] — Pré-refactor

Histórico narrativo das ondas anteriores em `CLAUDE.md` e `README.md`. Marcos:

### 2026-04-25 — Base de conhecimento GEO/AEO/Agentic Commerce
- Camada doutrinária permanente em `docs/knowledge/geo-aeo/` (17 arquivos, 2.640 linhas).
- 25+ papers acadêmicos (2025-2026) sintetizados em 30 instruções operacionais, 7 princípios mestres, 4 checklists.
- PR #1 aberto com este conteúdo.

### 2026-04-19 — Refactor multi-tenant (Ondas 1-5 originais)
- `ClientContext` introduzido em `src/clients/context.py`.
- `config/clients/<id>/client.yaml` como fonte única de identidade.
- `markdown_parser.py` consolidado (parser canônico).
- `providers.yaml` substituindo dicts hardcoded em `llm_client.py`.
- Voice Guard incorporado ao `QualityGate` como 4ª camada bloqueante.

### 2026-04-09 — Wave D
- `course_id` propagado no `cost_tracker` (achado F32) — antes recebia sempre `""`, impedia rastreamento por curso.

### 2026-04-08 — Auditoria de ecossistema (Ondas A-C)
- CLI `drafts-to-tsx` (achado F12) — recupera 13 cursos órfãos com investimento LLM já gasto.
- Pre-commit secret_guard (achado F44) ativado.

### 2026-03-28 — Inicial
- Repo público criado.
- Pipeline 5-LLM básico (Researcher → Writer → Analyzer → Classifier → Reviewer).

---

## Convenções

### Categorias

- **Adicionado** — features novas.
- **Mudado** — mudanças em features existentes (sem quebrar API).
- **Corrigido** — bug fixes.
- **Removido** — features ou código removidos.
- **Segurança** — vulnerabilidades patchedas.
- **Deprecado** — features marcadas para remoção em release futuro.

### Versionamento

- **MAJOR** — quebra de API pública (rebasear ClientContext, mudar contrato de Course/CourseDefinition, etc.).
- **MINOR** — features novas backward-compat (subcomandos novos, suporte a novo provider, etc.).
- **PATCH** — bug fix sem mudança de comportamento.

Pre-1.0: APIs ainda podem mudar entre minors.

## Como atualizar

Ao mergear PR, adicionar entrada em `## [Unreleased]`. Antes de tag de release, mover entradas para nova seção `## [X.Y.Z] — YYYY-MM-DD`.

## Links

- [Releases no GitHub](https://github.com/alexandrebrt14-sys/curso-factory/releases)
- [Wiki](https://github.com/alexandrebrt14-sys/curso-factory/wiki)
- [Roadmap (Project)](https://github.com/users/alexandrebrt14-sys/projects/2)
