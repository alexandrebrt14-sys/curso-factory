# Auditoria do pipeline do curso-factory (27/09/2026)

Leitura do repositório inteiro depois da rodada de boas práticas de escrita, com três frentes
em paralelo: regras escritas em mais de um lugar e divergência entre idiomas; eficiência,
sobreposição e configuração dos validadores; chamadas pagas, cache, retomada e ordem dos gates.
Nenhuma chamada paga e nenhuma execução do pipeline de geração: os custos em tokens e dólares
são estimativas calculadas a partir do código, dos prompts e dos preços de
`config/providers.yaml` (OpenAI US$ 5 e 15, Anthropic US$ 3 e 15, Google US$ 2 e 12 por milhão
de tokens de entrada e saída), para um curso de 16 aulas em 3 módulos, com 4 passadas de
expansão e a pesquisa no teto de 40 mil caracteres (cerca de 10,5 mil tokens).

Cada achado traz arquivo e linha (do estado anterior à correção quando ela já foi feita), o
custo, a correção e o estado: **feito** (com o commit), **parcial** ou **proposta**. Os números de
linha das propostas são do estado final da branch `feat/boas-praticas-escrita-20260927`.

## Resumo

| Tipo | Achados | Feitos | Parciais | Propostas |
|---|---|---|---|---|
| A. Regra em mais de um lugar | 11 | 2 | 5 | 4 |
| B. Idiomas | 4 | 1 | 0 | 3 |
| C. Validadores: trabalho repetido e sobreposição | 10 | 1 | 1 | 8 |
| D. Configuração sem leitor | 4 | 0 | 2 | 2 |
| E. Chamadas pagas que não mudam o resultado | 8 | 1 | 2 | 5 |
| F. Ordem dos gates | 4 | 2 | 0 | 2 |
| G. Retomada e resultado em disco | 5 | 2 | 0 | 3 |
| H. Código morto e testes | 4 | 1 | 1 | 2 |
| I. Documentação que descreve comportamento antigo | 3 | 1 | 1 | 1 |
| **Total** | **53** | **11** | **12** | **30** |

Toda refatoração pura desta rodada foi provada por `tests/test_saida_de_referencia.py`, que
guarda cada prompt enviado pelo pipeline (com cliente LLM falso) e o relatório do gate. As
mudanças intencionais regravaram a referência no mesmo commit, e o diff do arquivo mostra o
que mudou.

## A. Regra em mais de um lugar

**A1. Números escritos à mão nos prompts** (feito, `a9d3b47`). "Até 12 palavras" (glosa e
título), "até 25 palavras" (subtítulo), "acima de 350 palavras" (H3), "até 28" e "até 60"
(frase), "3 marcadores" e "2 a 4 H2" apareciam em `draft.md`, `review.md`, `trail.md` e
`analyze.md` de pt-br, raiz, en e es, enquanto os validadores liam os mesmos valores do espelho
e do YAML. Custo: trocar um teto exigia editar de 4 a 9 arquivos. Correção:
`src/validators/numeros_dos_prompts.py` entrega cada número da sua origem; o orquestrador passa
os tetos também para revisão, análise e trilha. Saída idêntica.

**A2. Cópias de raiz dos prompts** (feito, `a38dea0`). Nove arquivos em
`src/templates/prompts/` repetiam `pt-br/` e nunca carregavam (a cascata de
`src/agents/lang_resolver.py:57-72` para em `pt-br/`); `classify.md` e `research.md` de raiz já
tinham divergido. Custo: 931 linhas mantidas em dobro. Saíram; a raiz guarda só `tutor.md`.

**A3. Templates inline dos agentes contradizendo o prompt externo** (parcial). Redator e revisor
alinhados (`0da4228`), e o fallback do revisor deixou de pedir "um bloco final de resumo" que o
orquestrador não separa e que iria para dentro da aula (`3f86616`). Proposta para o resto:
`src/agents/analyzer.py:24-37` (registro HBR, negrito, Knowles, JSON sem `aprovado`),
`researcher.py:24-30` (sem a regra anti-GhostCite), `translator.py:38-39` (registro HBR),
`classifier.py:27-32` (chaves de JSON diferentes das do prompt) e `humanizer.py:89-116` (texto
sem acento). Correção proposta: fallback que falha alto (`raise`) em vez de publicar regra
vencida, já que o prompt externo existe no repositório.

**A4. `FORBIDDEN_CLICHES`** (proposta). `src/validators/content_checker.py:173` repete as 13
primeiras entradas de `validation.forbidden_expressions`. É a rede para YAML ausente; a
proposta é esvaziar a constante e deixar o espelho da fonte como rede, ou documentar a cópia
como intencional.

**A5. Verbos de Bloom em três listas** (proposta). `content_checker.py:189-233` contra
`quality_rules.yaml > editorial_style.bloom_*` (não lido) contra a lista de `pt-br/trail.md`;
"citar", "construir", "elaborar", "planejar", "sintetizar" e "integrar" só existem no código.
A checagem procura cabeçalho "Objetivos" e a trilha usa "O que você vai saber fazer", então
nunca roda sobre o texto que o prompt pede.

**A6. Números de didática em três cópias** (parcial, pendência do dono). `_PADRAO_*` de
`didatica_checker.py:90-130` repetem `validation.didatica`; o bloco `didatica` da fonte 1.8.0,
agora no espelho, tem valores diferentes (artigo definido 40% contra 50%, série 4 contra 3).
O subtítulo já lê da fonte (`a9d3b47`).

**A7. Menção entre aspas em quatro expressões** (proposta). `content_checker.py:350`,
`abertura_checker.py:92`, `didatica_checker.py:164` e `mascaras.py:22` aceitam aspas e
tamanhos diferentes: a mesma menção é isenta num checador e punida em outro. Unificar em
`mascaras.MENCAO_RE` muda veredito e pede decisão.

**A8. Teto do subtítulo em cinco lugares** (parcial). Prompt, didática e R1 leem o valor da
fonte (25). `markdown_parser.py:75` segue com 30 para extrair o subtítulo: uma frase de 26 a 30
palavras vira `description` e reprova no gate. Proposta: o parser ler o mesmo valor.

**A9. Blocos repetidos entre prompts** (proposta). "Fidelidade ao resumir e contribuir" tem
1.023 caracteres idênticos em `pt-br/draft.md` e `pt-br/review.md`; R1 a R9, léxico vetado e
cadência aparecem parafraseados em draft, review e analyze; o checklist "Antes de entregar" do
draft repete o corpo (cerca de 370 tokens por chamada, uns 12 mil tokens por curso). Proposta:
blocos em `pt-br/_blocos/` injetados por `{bloco_*}`, como já se faz com vocabulário, apuração,
crosslinks, peso visual e ordem do curso.

**A10. Faixa da cápsula** (parcial, pendência do dono). A mensagem dizia 40-60 e o código
aceitava 18 a 75 (alinhados em `df01a4f`). A fonte diz 25 a 60 (`limiares.capsulaPalavras`);
adotar a da fonte muda o veredito GEO.

**A11. Teto de marcadores `[FALTA EVIDÊNCIA]`** (parcial). Prompt 3 por aula, gate 5, publicado
0. Os dois números agora vêm do YAML (`marcadores_por_aula_no_rascunho` e
`fail_if_unresolved_markers_above`), e a diferença ficou documentada como intencional. Decidir
se o rascunho do default passa a zero.

## B. Idiomas

**B1. Prompts en e es nunca carregam** (proposta). Nenhum código de produção troca
`Agent.language`; `ClientContext.language` é lido em `src/clients/loader.py` e não chega a
agente nenhum. Custo: cerca de 70 KB de prompt parado. Se o idioma for ligado hoje, publica o
molde que o dono vetou.

**B2. `en/analyze.md` e `es/analyze.md` no molde antigo** (proposta). Registro HBR, abertura
"em situação concreta com tensão", negrito em termos, "H2 > H3 > H4", andragogia e JSON com
chaves diferentes do pt-br.

**B3. `draft.md` e `review.md` en e es sem as seções novas** (proposta). Sem título como
promessa, blocos auxiliares, fidelidade e os `{bloco_*}` de 27/09. Proposta: congelar en e es
com teste que falha enquanto divergirem do pt-br, ou regenerar pelo Translator quando o idioma
for ligado.

**B4. Marcador em inglês fora do teto** (feito, `3f86616`). `en/draft.md` manda usar
`[MISSING EVIDENCE:`, que `content_checker._UNRESOLVED_MARKER_RE` não contava.

## C. Validadores: trabalho repetido e sobreposição

**C1. A camada GEO rodava o gate inteiro de novo** (feito, `50e36dc`).
`QualityGate.check_geo` chamava `check_content` sobre o curso inteiro e descartava tudo que não
fosse GEO. Custo medido num curso sintético de 16 aulas: 426 ms; depois, 7 ms.

**C2. Expressões recompiladas a cada aula** (parcial). Apuração narrada compilada uma vez por
conjunto (`d7b5334`). Propostas: `_ocorrencias` (`content_checker.py:392`, um padrão por termo
a cada chamada), `_padroes` da abertura (`abertura_checker.py:228`, remonta termos por regra e
por seção no `check_abertura_definicao`) e a glosa da didática (`didatica_checker.py:349`).

**C3. O mesmo texto limpo várias vezes** (proposta). `_sem_mencoes` roda 4 vezes por aula
(`content_checker.py`), `_strip_noise` 5 vezes com GEO ligado, `_sem_codigo` cerca de 7 vezes e
`_linhas_rotuladas` 4 vezes na abertura, `_paragrafos_de_prosa` 4 vezes na didática.

**C4. `load_client` sem cache** (proposta). `src/clients/loader.py:48` relê o YAML a cada
chamada com `client=None` (voice guard, disclosure, schema builder).

**C5. Peso visual parseia a aula com Pydantic** (proposta). `peso_visual_aula.medir` roda
`parse_module_to_sections` completo só para contar peças; é a contagem fiel ao que o gerador
emite, e o custo é aceitável hoje.

**C6. Acentos corrigidos e medidos em duas passadas** (proposta). Com `auto_fix`,
`quality_gate.py:128` corrige e `:142` mede de novo com o mesmo mapa; a segunda nunca acha nada.

**C7. O mesmo defeito cobrado duas ou três vezes** (proposta). Clichê e verbo de Bloom no
`content_checker` e no `voice_guard`; "saiba mais" como clichê, âncora genérica e desconto do
voice guard; a lei de dados como R9 (erro) e muleta legal (aviso), e o `disclosure_checker`
emite "LGPD art. 20", que a R9 reprova; recapitulação como R8 e `fecho-resumo`; parágrafo longo
no conteúdo, no voice guard e na densidade visual; subtítulo longo na R1 e na didática.
Proposta: um dono por defeito, e o voice guard consumindo os achados do conteúdo.

**C8. Famílias da fonte que nunca casam** (proposta, muda veredito). `_termos_da_fonte`
(`abertura_checker.py:213`) escapa como literal as famílias que a fonte exporta como expressão
regular (`noSeuNegocio`, `exercicioRotulo`, `checkpointRotulo`, `lgpd`): o padrão gerado nunca
casa. Compilar como expressão passa a pegar mais texto.

**C9. Padrão duplicado na R6** (proposta, trivial). `"resultado esperado"` aparece duas vezes em
`_PADROES_PADRAO["R6"]`.

**C10. Padrão invertido entre gerador e densidade** (proposta). `tsx_generator.py:119` lê
`required_for_new_course` com padrão `False`; `visual_density.py:225`, com `True`.

## D. Configuração sem leitor

**D1. `config/quality_rules.yaml`** (parcial). Sem leitor: `accent_check.*`,
`content_quality.enabled`, `min_lessons_per_trail`, `max_lessons_per_trail`,
`min_sources_per_trail`, `min_capsules_per_trail`, `max_reading_time_per_lesson_minutes`,
`editorial_style.*`, `andragogy.*`, `forbidden_expressions.enabled` e `fail_on_found`,
`anti_invencao.enabled`, `allow_marker` e `ban_vague_attribution`, `link_check.*`,
`html_validation.*` (que diverge de `html_validator.REQUIRED_ELEMENTS`), `finops.*`,
`global_prohibitions.*` e `anti_retrabalho.*`. As chaves de trilhas por curso foram marcadas
como descritivas (`0da4228`). Proposta: bloco "documentação, não lido por código" e um teste
que falha quando o YAML tem chave fora da lista de chaves consumidas.

**D2. `config/clients/default/client.yaml`** (proposta). Sem consumidor: `editorial.*` (fora a
listagem do CLI), `disclosure.reviewer_human`, `pipeline.*` (o humanizador só é chamado por
teste), `voice_guard.voice_samples.*` (o comentário promete injeção que nenhum código faz),
`geo_2026.schema_authority_stack_enabled`, `canonical.domains`.

**D3. `config/lexicos.json`** (parcial). Passaram a ser lidos `semVisualAcimaDePalavras`
(`0da4228`), `glosaMaxPalavras`, `fraseMaxPalavras`, `fraseToleranciaPalavras`,
`h3SoAcimaDePalavras` e `subtituloMaxPalavras` (`a9d3b47`). Seguem sem leitor, entre outras:
`antiteses`, `gerundismo`, `culpaNoLeitor`, `errataPublicada`, `aberturaEmCena`,
`legendaQueRotula`, `acentuacaoFaltando`, `limiares.paragrafo*`, `capsulaPalavras`,
`listaMaxItens`, `cabecalhosPorMil` e o bloco `didatica`.

**D4. Estilometria prometida no YAML que não existe** (proposta). `stylometry_checker.py:41` e
`quality_gate.py:206` dizem que os limiares vêm do YAML; a seção não existe e
`min_score=60` é fixo.

## E. Chamadas pagas que não mudam o resultado

**E1. Pesquisa inteira reenviada em 20 chamadas** (parcial). Cerca de 210 mil tokens de entrada
repetidos por curso (US$ 1,05). O prompt de aula agora tem prefixo estável (`da8bedc`), o que
habilita o cache automático; proposta complementar: dossiê de fatos por aula (2 a 3 mil tokens
no lugar de 10,5 mil).

**E2. Planejamento pago mesmo com aulas declaradas** (proposta). `src/agents/pipeline.py:92`
monta `Module` sem `etapas`, e o atalho de `_plan_lessons` nunca dispara pela CLI: 3 chamadas
por curso que traz as aulas no YAML.

**E3. Análise do curso inteiro, aproveitada em 3 mil caracteres** (proposta). O analisador
recebe cerca de 44 mil tokens; a revisão recebe `analysis[:3000]`, o mesmo trecho para toda
aula. Proposta: analisar só títulos, subtítulos e aberturas (uns 5 mil tokens) e recortar a
saída por aula.

**E4. Classificação sem consumidor, no caminho crítico** (proposta, decisão do dono). Nada lê
`etapas["classify"]`, e uma falha nela interrompe o pipeline antes da revisão. Proposta:
metadados determinísticos (nível e tags do YAML, duração por palavras) ou tirar a etapa do
caminho crítico.

**E5. Revisão descartada quando encolhe** (proposta). Cada descarte perde uma chamada Sonnet
(US$ 0,07 a 0,12); truncamento por `max_tokens` só gera aviso. Proposta: revisor devolvendo
lista de edições e truncamento tratado como erro próprio.

**E6. Repetição sem olhar a causa** (proposta). `src/llm_client.py:427-431` repete o
truncamento com os mesmos parâmetros; o resultado de fallback não entra no cache; o Google
recebe `maxOutputTokens` de 262.144.

**E7. Expansão das primeiras aulas contra o teto delas** (feito, `0f74a91`).

**E8. Cache de prompt** (parcial). Prefixo estável no prompt de aula (`da8bedc`). Propostas: o
`CostTracker` ler `cached_tokens` (OpenAI) e `cache_read_input_tokens` (Anthropic), para o custo
refletir o desconto; a revisão com as regras num bloco `system` com `cache_control`; contar
`thoughtsTokenCount` no Gemini. O marcador da Anthropic abaixo do mínimo de tokens do modelo é
ignorado sem aviso; confirmar o mínimo do `claude-sonnet-5` antes de mexer.

## F. Ordem dos gates

**F1. Gate só no fim, revisão às cegas** (feito, `11e158a`). O gate determinístico roda antes de
cada revisão e entrega os erros ao revisor.

**F2. Plano de aulas não validado antes de redigir** (proposta). O módulo 2 é planejado depois
de o módulo 1 estar escrito; a faixa de aulas do curso e os títulos só são medidos no fim.
Proposta: plano único do curso, validado (faixa, títulos, duplicatas, destinos de crosslink)
antes da primeira aula, o que também permite redigir e revisar aulas em paralelo.

**F3. Revisor sem as regras de crosslink e de peça visual** (feito, `11e158a`).

**F4. Revisor mandado conferir números na pesquisa que não recebe** (proposta). `review.md`
cita a pesquisa três vezes; o revisor recebe só a aula e o resumo da análise.

## G. Retomada e resultado em disco

**G1. Checkpoint por etapa** (feito, `44836ad`). Falha na aula 12 perdia as aulas 1 a 11
(US$ 1,4 e até 22 minutos para refazer, depois da hora de TTL do cache).

**G2. Parada por orçamento gravada como sucesso** (feito, `44836ad`).

**G3. Teto da sessão abaixo do custo de um curso** (proposta, decisão do dono).
`SESSION_BUDGET_TOTAL` vale US$ 5 (`src/config.py`) e o curso de 16 aulas custa uns US$ 4,7 a
5,4 pela estimativa; o teto por curso é US$ 10.

**G4. `_context` gravado e nunca lido** (proposta, trivial). `Orchestrator._save_checkpoint`
duplica a saída da etapa no checkpoint.

**G5. Trilha escrita com aulas não revisadas** (proposta). O fechamento da trilha nasce na
redação e não passa pela revisão; as fontes podem citar trecho que a revisão tirou.

## H. Código morto e testes

**H1. Funções sem referência** (feito, `9523532`): `content_checker._find_blockquotes` e
`markdown_parser._detect_special_quote`.

**H2. API sem chamador em produção** (proposta): `QualityGate.check_html`, `full_report`,
`to_quality_report`, três `format_report`, `compute_burstiness_goh`, `build_disclosure_block`,
`humanize_if_enabled`, `try_compute_perplexity`. Confirmar consumidores fora do repositório
antes de apagar.

**H3. Testes que não provam o que dizem** (parcial). Corrigidos dois (`9523532`). Seguem:
`test_validators_smoke.py:136`, `test_voice_guard.py:216`, `:224` (só o caso aprovado),
`:256-268` (bônus limitado a 100), `test_humanization_pipeline.py:121`, `:144-151`, `:370`,
`:379`.

**H4. Testes duplicados** (proposta): `test_validators_smoke.py:124` e `:130` repetem
`test_voice_guard.py:249` e `:271`.

## I. Documentação

**I1. `CLAUDE.md`** (feito, `7b883ad`). De 413 para 340 linhas e de 62 para 28 KB: o índice das
waves foi para `docs/BASE_DE_CONHECIMENTO_GEO.md`; saíram afirmações que o código desmente (TTL
de 24 h, aprovação que move para `output/approved/`, teto por curso sem o da sessão).

**I2. Cabeçalho de prompt com modelo errado** (parcial). O draft deixou de citar "GPT-4o"
(`da8bedc`); `pt-br/classify.md` ainda diz "(Groq)" e o provedor é Google.

**I3. Resumos longos de regras que já têm decisão própria** (proposta). R1 a R9, didática e molde
no `CLAUDE.md` podem encolher para duas linhas cada, com o link da decisão (cerca de 50 linhas).

## Economia estimada

| O quê | Conta | Resultado |
|---|---|---|
| Linhas mantidas em dobro | 9 prompts de raiz removidos | 931 linhas a menos |
| Regras unificadas | 8 números de prompt com origem única, 52 ocorrências em 4 idiomas; 9 prompts sem cópia | 17 regras com um lugar só |
| Tokens em cache por curso | prefixo estável de cerca de 15,4 mil tokens (4,9 mil de regras e 10,5 mil de pesquisa) × 19 chamadas depois da primeira | cerca de 293 mil tokens elegíveis; US$ 0,73 a 1,32 por curso, com desconto de 50% a 90% sobre US$ 5 por milhão |
| Retomada | aulas já pagas não se refazem: 11 aulas × cerca de US$ 0,13 numa parada na aula 12; revisão, uns US$ 0,07 a 0,12 por unidade | US$ 1,4 a 2,5 por interrupção |
| Expansão das primeiras aulas | até 3 passadas que miravam o alvo errado | até 3 chamadas de cerca de US$ 0,13 |
| Camada GEO | 426 ms para 7 ms por curso | tempo de CPU |
| Contexto do Claude Code | `CLAUDE.md` de 62 KB para 28 KB | cerca de 9 mil tokens por sessão |

## A validar na primeira geração real

1. Cache de prompt: nas chamadas de aula a partir da segunda de cada curso,
   `usage.prompt_tokens_details.cached_tokens` maior que zero no log do cliente OpenAI.
2. Revisão dirigida: rodar um curso de teste e comparar o `gate_report` com e sem
   `validation.revisao_dirigida` (desligar com `enabled: false`), contando os erros de
   crosslink e de peso visual que sobram.
3. Crosslinks: conferir na página servida que cada link `/educacao/<slug>#<id>` abre o
   capítulo certo (o motor abre um capítulo por vez, então a conferência é no navegador).
4. Retomada: interromper um curso de teste por orçamento (`SESSION_BUDGET_TOTAL` baixo),
   retomar e confirmar no `costs.json` que as aulas já escritas não foram pagas de novo.
