# AI Discovery Standards 2026 — curso-factory

> Versão 1.0 · 17-05-2026 · Owner: Brasil GEO (Alexandre Caramaschi, CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil)
> Fonte: Wave 4 da pesquisa GEO/SEO 2026 (Perplexity sonar-deep-research + WebFetch validação em IETF, W3C, Schema.org, llmstxt.org, c2pa.org, modelcontextprotocol.io)

---

## Índice

0. [Sumário executivo](#0-sumário-executivo)
1. [Como LLMs descobrem e acessam conteúdo em 2026](#1-como-llms-descobrem-e-acessam-conteúdo-em-2026)
2. [Catálogo canônico de AI crawlers 2026](#2-catálogo-canônico-de-ai-crawlers-2026)
3. [llms.txt em 2026 — o que funcionou e o que não](#3-llmstxt-em-2026--o-que-funcionou-e-o-que-não)
4. [IETF AIPREF — o padrão que está emergindo](#4-ietf-aipref--o-padrão-que-está-emergindo)
5. [C2PA — proveniência de conteúdo](#5-c2pa--proveniência-de-conteúdo)
6. [Schema.org em 2026 — o que NÃO adicionaram](#6-schemaorg-em-2026--o-que-não-adicionaram)
7. [Model Context Protocol (MCP) ecosystem 2026](#7-model-context-protocol-mcp-ecosystem-2026)
8. [Stack recomendada para curso-factory hoje](#8-stack-recomendada-para-curso-factory-hoje)
9. [Anti-padrões de descoberta](#9-anti-padrões-de-descoberta)
10. [Roadmap de adoção 2026-2027 para curso-factory](#10-roadmap-de-adoção-2026-2027-para-curso-factory)
11. [Apêndice A — Templates prontos](#11-apêndice-a--templates-prontos)
12. [Apêndice B — Citações URLs reais](#12-apêndice-b--citações-urls-reais)

---

## 0. Sumário executivo

Três frases que sintetizam o estado real do território em maio de 2026:

1. **llms.txt virou ruído estatístico**: 10,13% dos 300 mil domínios da amostra SE Ranking publicam o arquivo, mas o estudo ALLMO (94.614 URLs citadas em 11.867 respostas de IA) encontrou exatamente **1 URL** com llms.txt no conjunto inteiro — 0,001% — e Anthropic, OpenAI, Google e Perplexity continuam sem endossar oficialmente o formato.
2. **IETF AIPREF é o único caminho normativo emergente**: o working group está ativo, com `draft-ietf-aipref-vocab-06` revisado em 28-abr-2026 (autores Paul Keller e Martin Thomson) e meta de submissão ao IESG em 31-ago-2026, mas o anexo `draft-ietf-aipref-attach-04` **expirou** em outubro de 2025 e aguarda nova revisão.
3. **MCP é o único padrão com adoção transversal real entre os 5 grandes**: Anthropic, OpenAI, Google, Microsoft e Cloudflare suportam MCP nativamente em produção; o registry oficial está em preview desde setembro de 2025 sob a Linux Foundation Agentic AI Foundation, e marketplaces como Manifold catalogam 7.700 servers (anúncio de 12-mai-2026).

A tese operacional para o curso-factory é direta: trate `robots.txt` + UA tokens como única superfície de controle confiável hoje, prepare estrutura para AIPREF dentro de 30 dias, ignore `ai.txt` e `ai-policy.json` em paths custom, e publique um MCP server canônico do catálogo do curso antes do final de Q3.

---

## 1. Como LLMs descobrem e acessam conteúdo em 2026

A primeira armadilha conceitual de 2026 é tratar "crawler de IA" como categoria única. O ecossistema bifurcou em três modos operacionais distintos, cada um com governança própria e implicações diferentes para opt-in/opt-out.

### 1.1 O modelo mental das três camadas

| Camada | Quem executa | Quando dispara | Respeita robots.txt? | Exemplo canônico |
|---|---|---|---|---|
| **Training crawler** | LLM vendor (OpenAI, Anthropic, Google, Meta, ByteDance) | Contínuo, em background, alimenta corpus de pré-treino e fine-tuning | Sim, com token de UA dedicado | `GPTBot`, `ClaudeBot`, `Bytespider` |
| **Search index** | LLM vendor ou search partner | Periódico, alimenta retrieval para AI search (SearchGPT, AI Overviews, Perplexity) | Sim, com token de UA dedicado | `OAI-SearchBot`, `Claude-SearchBot`, `PerplexityBot`, `Google-CloudVertexBot` |
| **User-fetcher** | LLM vendor sob trigger de ação do usuário final | Sob demanda: usuário cola URL, pede para "abrir" ou "ler" página específica | **Parcial ou totalmente fora** — racional é que executa ato explícito do usuário | `ChatGPT-User`, `Claude-User`, `Perplexity-User` (este último declara oficialmente que ignora robots.txt) |

O caso mais documentado de quebra de padrão é o `Perplexity-User`: a documentação oficial em `docs.perplexity.ai/guides/bots` declara que o bot **não consulta robots.txt** porque cada fetch é resultado direto de ação do usuário Perplexity, não de crawl autônomo. Essa é a nova fronteira normativa que o AIPREF (§ 4) tenta resolver.

### 1.2 Por que essa distinção importa para o curso-factory

Se você bloquear `ChatGPT-User` no curso-factory, perde a capacidade de o aluno usar Claude/ChatGPT para revisar materiais do próprio curso em tempo real. Se bloquear `GPTBot`, fecha porta para treino do GPT-5/6 com seu conteúdo — decisão estratégica legítima, mas distinta. A confusão entre as duas decisões é a origem de 80% dos erros de configuração em 2026.

Regra operacional [INTERNAL TO CURSO-FACTORY]: training crawlers — decisão por política editorial; search index crawlers — quase sempre permitir; user-fetchers — sempre permitir.

### 1.3 Os três sinais que LLMs realmente leem em 2026

Os estudos de Limy AI (500 milhões de eventos de bot) e BeRecommended (Fortune 500) convergem em três artefatos que os crawlers efetivamente consomem em escala:

1. **`/robots.txt`** — única superfície de controle com tração comprovada.
2. **`/sitemap.xml` e `sitemap-index.xml`** — protocolo de descoberta canônico.
3. **JSON-LD inline em `<script type="application/ld+json">`** — fonte principal de entity disambiguation para retrieval.

Tudo o que não está nessa lista (incluindo llms.txt, ai.txt e ai-policy.json em paths custom) é, em maio de 2026, especulação operacional.

### 1.4 Por que o RAG mudou o vetor de descoberta

Até 2023, descoberta significava "ser indexado". A partir de 2025, com retrieval-augmented generation maduro em ChatGPT Search, Perplexity, Claude com tools e AI Overviews do Google, descoberta passou a ter três sub-camadas distintas, cada uma exigindo otimização independente:

- **Discovery passiva** (crawl programático): o conteúdo é descoberto quando um training ou search crawler chega à página por descoberta de link. Optimização: sitemap-index + links internos densos + robots.txt limpo.
- **Discovery ativa por usuário** (user-fetcher sob demanda): o aluno cola o URL no Claude/ChatGPT/Perplexity para o LLM ler a página naquele instante. Optimização: a página precisa ser parseable em HTML semântico + JSON-LD denso; SPA renderizada só no cliente é invisível para a maioria dos user-fetchers em 2026.
- **Discovery via agent** (MCP tool call): o LLM descobre o produto **dentro do próprio chat** porque o usuário conectou um MCP server. Optimização: publicar MCP server canônico e registrar em registry oficial (§ 7.7).

Os três vetores são complementares e exigem stack distinta. O erro arquitetural mais comum em 2026 é otimizar apenas para discovery passiva (modelo SEO tradicional) e perder os outros dois canais — que crescem mais rápido em volume e qualidade de tráfego.

### 1.5 Latência e custo do crawl em 2026

Dado pouco discutido: training crawlers consomem mais banda do que Googlebot em sites populares. Limy AI reportou que `GPTBot`, `ClaudeBot`, `Bytespider` e `Amazonbot` somados representam 11-18% do total de requests de bot em propriedades B2C de tráfego médio (1M-10M visitas/mês). Implicações operacionais:

- Cache CDN agressivo no edge: training crawlers se beneficiam tanto quanto humanos, e custo de origem despenca.
- Throttling por User-Agent em CDN é tentação ruim: training crawler bloqueado por rate-limit não retorna; o site sai do dataset de pré-treino do ciclo inteiro do modelo (12-18 meses).
- Logs de bot devem ser separados de logs humanos para FinOps real e para detectar mudanças de padrão (p. ex., novo bot, deprecação silenciosa).

---

## 2. Catálogo canônico de AI crawlers 2026

Esta tabela consolida ai-robots-txt/robots.json (200+ entradas), Known Agents (ex-darkvisitors) e documentação oficial de cada operadora. É a fonte da verdade para configuração de `robots.txt` em qualquer property gerida pela Brasil GEO em 2026.

| User-agent (robots token) | Operadora | Classe | Respeita robots.txt | Notas críticas |
|---|---|---|---|---|
| **GPTBot** | OpenAI | Training | Sim | Crawler principal para GPT-4.x/5/6 |
| **ChatGPT-User** | OpenAI | User-fetcher | Parcial (on demand) | Disparado quando usuário pede para abrir URL no ChatGPT |
| **OAI-SearchBot** | OpenAI | Search index | Sim | Indexa para SearchGPT/Browse |
| **ChatGPT Agent** | OpenAI | Browser automation | Variável | Novo em 2026, automação tipo Operator |
| **ClaudeBot** | Anthropic | Training | Sim | Consolidação 2024 do antigo `anthropic-ai` |
| **Claude-User** | Anthropic | User-fetcher | Parcial | Disparado por usuário Claude |
| **Claude-SearchBot** | Anthropic | Search index | Sim | Indexa para AI search do Claude |
| **anthropic-ai** | Anthropic | **[DEPRECATED]** | — | Legado; manter bloqueio defensivo |
| **Claude-Web** | Anthropic | **[DEPRECATED]** | — | Legado |
| **Google-Extended** | Google | Training opt-out (token de controle) | Sim, mas é flag e não crawler | Bloqueia uso para Gemini/Vertex AI training; não fetcha conteúdo |
| **Google-CloudVertexBot** | Google | Vertex AI Search | Sim | Crawla para Vertex AI Search de clientes corporativos |
| **GoogleOther** / **GoogleOther-Image** / **GoogleOther-Video** | Google | Product fetcher | Sim | Família de fetchers internos |
| **Google-NotebookLM** | Google | Research assistant | Variável | Coleta para NotebookLM |
| **GoogleAgent-Mariner** | Google | Browser agent | Variável | Agente browser experimental |
| **Google-Read-Aloud** | Google | Acessibilidade/leitura | Sim | Read-aloud service |
| **PerplexityBot** | Perplexity | Search index | Sim | IP list publicada em `perplexity.com/perplexitybot.json` |
| **Perplexity-User** | Perplexity | User-fetcher | **NÃO (oficial)** | Documentação declara que ignora robots.txt por ser user-action |
| **Bytespider** | ByteDance | Training | Sim | Treina LLMs TikTok/Doubao |
| **TikTokSpider** | ByteDance | Training | Sim | — |
| **Amazonbot** | Amazon | Search + Alexa + Rufus | Sim | Rufus (LLM Amazon) reaproveita este crawler |
| **AmazonBuyForMe** | Amazon | AI shopping agent | — | Novo em 2026 |
| **bedrockbot** | Amazon | Bedrock customer crawl | Sim | Crawl para RAG customer-built no Bedrock |
| **amazon-kendra** | Amazon | Enterprise search | Sim | NL search |
| **Applebot** | Apple | Search (Siri, Spotlight) | Sim | — |
| **Applebot-Extended** | Apple | Training opt-out (token de controle) | Sim, mas é flag | Bloqueia uso para Apple Intelligence |
| **meta-externalagent** | Meta | Training + AI features | Sim (declarado) | Crawler oficial Meta AI |
| **meta-externalfetcher** | Meta | User-fetcher | Parcial | Documentação fraca |
| **meta-webindexer** | Meta | Meta AI search | Sim | — |
| **FacebookBot** | Meta | LLM training | Sim | — |
| **bingbot** | Microsoft | Search + Copilot | Sim | Copilot reaproveita índice Bing — sem UA separado |
| **MistralAI-User** | Mistral | User-fetcher | Sim | Le Chat user actions |
| **DuckAssistBot** | DuckDuckGo | AI assistant | Sim | — |
| **CCBot** | Common Crawl | Open dataset | Sim | Dataset usado por praticamente todos os LLMs em pré-treino |
| **cohere-ai** | Cohere | User responses | Sim | — |
| **cohere-training-data-crawler** | Cohere | Training | Sim | — |
| **PetalBot** | Huawei | Search + AI (PanGu) | Sim | — |
| **PanguBot** | Huawei | Training | Sim | — |
| **YandexAdditional** | Yandex | YandexGPT training | Sim | — |
| **DeepSeekBot** | DeepSeek | Training | Sim | — |
| **Diffbot** | Diffbot | Structured data ML | Sim | — |
| **TavilyBot** / **ExaBot** / **FirecrawlAgent** | Tavily / Exa / Firecrawl | Data provider B2B (scraping-as-a-service para outras IAs) | Variável | Camada de intermediação que entrega dados para downstream LLMs |
| **SemrushBot-OCOB** / **SemrushBot-SWA** | Semrush | AI features (ContentShake, Writing Assistant) | Sim | Tokens específicos por produto |
| **Kagi-fetcher** | Kagi | AI assistant | Sim | — |
| **Andibot** / **PhindBot** / **YouBot** / **iAskBot** | múltiplos | AI search engines de nicho | Sim (em geral) | Long-tail de AI search; cobrir se property é global |

Lista completa, machine-readable, mantida pela comunidade: `https://github.com/ai-robots-txt/ai.robots.txt/blob/main/robots.json` (200+ bots, atualizada continuamente).

### 2.1 Tokens de controle vs crawlers reais

Atenção especial a dois tokens que parecem crawlers mas **não fetcham conteúdo**:

- **`Google-Extended`** — flag de policy. Bloqueá-lo não impede o Googlebot de visitar a página; impede que o conteúdo coletado pelo Googlebot seja usado para treinar Gemini/Vertex AI.
- **`Applebot-Extended`** — análogo da Apple. Bloqueia uso para Apple Intelligence, não bloqueia indexação para Spotlight/Siri.

Confundir esses dois com training crawlers convencionais é o erro #1 catalogado por LBN Tech Solutions em 2026.

---

## 3. llms.txt em 2026 — o que funcionou e o que não

### 3.1 A foto fria

Seis estudos independentes mediram adoção e impacto em 2026. Os resultados são desconfortavelmente convergentes:

| Estudo | Amostra | Adoção llms.txt | Citação na resposta de LLM? |
|---|---|---|---|
| **SE Ranking** | 300.000 domínios | **10,13%** geral; 9,88% (sites pequenos), 8,27% (sites com 100k+ visitas/mês) | Não mediu |
| **Trakkr Research** | 37.894 domínios AI-cited | 13,3% no corpus geral; **6,0% no top 50 mais citados** | Sem correlação positiva |
| **ALLMO / Signals 2026** | 94.614 URLs citadas em 11.867 respostas IA | **1 URL** (0,00105693%) | Não — apenas Target.com em top 50 |
| **Rankability** | Top 100 websites (amostra 30) | **0,0%** | — |
| **BeRecommended** | Fortune 500 | 7,4% | AI crawlers leram em 0,1% das requests |
| **Limy AI** | 500M eventos de bot AI | — | Apenas **408 requests** a llms.txt em 500 milhões |

A leitura honesta: sites pequenos publicam mais do que sites grandes; o top 50 mais citado pelos LLMs adota **menos** que a média geral; e os crawlers que efetivamente movem o ponteiro praticamente não tocam no arquivo.

### 3.2 Posicionamento dos quatro grandes

- **Anthropic**: zero documentação oficial citando llms.txt. Controles documentados são robots.txt + meta tags.
- **OpenAI**: zero documentação oficial. Pipeline de retrieval comprovadamente não consulta llms.txt (confirmado por Signals e Limy via análise de logs).
- **Google**: posicionamento explícito (via síntese LBN Tech Solutions 2026) — "sem adoção pelas grandes IAs incluindo Google".
- **Perplexity**: documentação foca em `PerplexityBot` e `Perplexity-User`. Não menciona llms.txt.

### 3.3 Quando llms.txt **ainda faz sentido**

Existe um nicho legítimo e mensurável: **developer documentation**. Sites como Cloudflare, Vercel AI SDK, FastHTML e Hugging Face publicam `llms-full.txt` porque seus usuários **copiam e colam** o arquivo dentro do próprio Claude/ChatGPT para criar contexto. Não é sinal para crawler — é content delivery convenience para humano com agente acoplado.

Status agregado: **[DE FACTO, SEM VENDOR BACKING]**. Útil para subset estreito; irrelevante para SEO/GEO mainstream.

### 3.4 Pseudo-alternativas que também não decolaram

| Proposta | Status 2026 | Veredito |
|---|---|---|
| **ai.txt** | Proposta solta de blogs, sem buy-in de vendor | Não publicar |
| **/.well-known/ai-policy** com `ai-policy.json` | Discutido em fóruns W3C, sem spec publicada nem crawler study | Esperar AIPREF |
| **robots.txt + UA tokens** | Tração real, suportado por todos os vendors | **Esta é a única superfície de controle real hoje** |

---

## 4. IETF AIPREF — o padrão que está emergindo

### 4.1 Working group e timeline

O **IETF AI Preferences Working Group (AIPREF)** está ativo (charter em `datatracker.ietf.org/wg/aipref/about/`) com meta de submissão ao IESG em **31-ago-2026**. Dois drafts canônicos:

| Documento | Versão | Status | Última revisão | Autores |
|---|---|---|---|---|
| `draft-ietf-aipref-vocab` | **06** | **[DRAFT]** Active I-D, sem consenso WG | 28-abr-2026 | Paul Keller, Martin Thomson |
| `draft-ietf-aipref-attach` | **04** | **[DRAFT]** EXPIRADO em out/2025 | Aguardando nova revisão | Gary Illyes (Google), Martin Thomson |

O **vocab** define o vocabulário de preferências (categorias de uso: training, inference, search index, etc.). O **attach** define como anexar essas preferências ao conteúdo — proposta original era estender RFC 9309 (Robots) e adicionar caminho canônico `/.well-known/ai-preferences`.

A expiração do attach em out/2025 é o gargalo: sem ele, vocab fica órfão de mecanismo de transporte.

### 4.2 Drafts individuais relacionados (não-AIPREF)

Três drafts individuais (sem endosso IETF) tocam o tema discovery:

| Draft | Última revisão | Autor | Tema |
|---|---|---|---|
| `draft-cui-ai-agent-discovery-invocation-01` | 12-fev-2026 | Yong Cui, Yihan Chao, Chenguang Du | Protocolo de descoberta e invocação de AI agents |
| `draft-aiendpoint-ai-discovery-00` | 23-mar-2026 | 최영재 | Endpoint estruturado para discovery + capability exposure |
| `draft-han-ai-manifest-01` | 15-mai-2026 | Wonpyo Han | AI Manifest com workflow instructions embarcadas |

Nenhum é, hoje, working item oficial — são propostas individuais que podem ou não virar WG items.

### 4.3 W3C — paralelo

Existe um **W3C AI Agent Protocol Community Group** publicando em `w3c-cg.github.io/ai-agent-protocol/protocol.html`, mas **não é W3C Standard** e **não está na Standards Track**. Tratar como sinal exploratório, não como compromisso de roadmap.

### 4.4 O que o vocab v06 está tentando padronizar

A versão 06 do `draft-ietf-aipref-vocab` propõe um vocabulário inicial de **categorias de uso** que sites podem aceitar ou recusar, separando o que hoje está colapsado em "robots.txt allow/disallow":

- **train-ai** — uso para pré-treino de modelos de IA
- **train-genai** — subset: treino específico para modelos generativos
- **search** — indexação para search engines (incluindo AI search)
- **inference** — uso em tempo de inferência (RAG, retrieval, browse)
- **inference-snippet** — subset: uso em geração de snippets curtos
- **inference-summary** — subset: uso em sumarização de página inteira

A premissa do WG é que site owner deve poder dizer "permito search, permito inference-snippet, mas não permito train-genai" — granularidade que `robots.txt` não expressa. Hoje, ou você bloqueia `GPTBot` (que treina) e perde também a chance de ser sumarizado por SearchGPT, ou permite tudo. AIPREF resolve isso.

### 4.5 Como o `attach` propõe transportar essas preferências

O draft `attach` v04 (expirado) propunha três mecanismos paralelos:

1. **Extensão a RFC 9309 (Robots Exclusion Protocol)** — adicionar diretivas estruturadas dentro de `robots.txt`.
2. **HTTP response header** `Content-Usage:` — anexar preferências por resposta HTTP.
3. **Caminho canônico `/.well-known/ai-preferences`** — documento JSON único por property.

O fato de o `attach` ter expirado em outubro de 2025 sem nova revisão é o principal risco do roadmap AIPREF — sem mecanismo de transporte, o vocab vira documento acadêmico. Equipes que precisam de garantia regulatória (notavelmente UE AI Act) estão acompanhando a re-submissão.

### 4.6 Recomendação operacional para curso-factory

Status: **[DRAFT — preparar superfície, não implementar conteúdo final]**.

Em 30 dias, publicar placeholder em `/.well-known/ai-preferences` retornando 204 No Content ou um JSON vazio versionado. Quando o `attach` for re-revisado e o `vocab` chegar ao IESG, ativar o conteúdo real seguindo a sintaxe final aprovada. Isso elimina rework de URL canônica.

Posicionamento editorial defensável hoje, em texto público do curso: "Brasil GEO acompanha o working group AIPREF do IETF e publicará política granular de uso de IA assim que o vocabulário for ratificado". Isso vacina contra perguntas regulatórias sem committar a sintaxe específica que ainda pode mudar.

---

## 5. C2PA — proveniência de conteúdo

### 5.1 Status canônico

**C2PA (Coalition for Content Provenance and Authenticity)** é hoje o único padrão de **proveniência de conteúdo gerado por IA** com adoção confirmada de produção entre os grandes vendors. Status: **[ADOPTED]**.

- **Spec atual**: 2.3, em produção
- **Steering Committee**: Adobe, Amazon, BBC, Google, Meta, Microsoft, OpenAI, Sony, Truepic, Publicis
- **Aplicação real verificada**: câmeras Leica e Sony embedam manifests C2PA em captura; Adobe Photoshop assina edições; ChatGPT image gen embeda C2PA por padrão em outputs de imagem

### 5.2 Modelo conceitual

Um **C2PA manifest** é um bloco assinado criptograficamente, embarcado no metadado do arquivo, contendo:

- Identidade do criador (humano ou software)
- Histórico de transformações (claim chain)
- Asserções sobre uso de IA (modelo, prompt, versão)
- Assinaturas verificáveis em cadeia

O verificador (browser, CMS, plataforma) pode reconstruir a história de proveniência sem depender de banco de dados externo — é portátil junto ao arquivo.

### 5.3 Por que C2PA decolou e os concorrentes não

A questão honesta: por que C2PA conseguiu o que llms.txt não conseguiu? Três respostas:

1. **Coalição com skin in the game**: Adobe (toolchain de criação), Microsoft e Sony (câmeras + sistemas operacionais), Google e OpenAI (geração), BBC e Publicis (publishing) — cada membro do steering committee tem prejuízo direto se o padrão falhar. Não é grupo de fórum.
2. **Embarcado no metadado, não em arquivo separado**: C2PA viaja **dentro** do JPG/PNG/MP4. Não depende de o consumidor visitar `/c2pa.json`. Isso elimina a fragilidade fundamental de llms.txt.
3. **Alinhamento regulatório**: UE AI Act exige marcação de conteúdo sintético; FTC vem sinalizando deceptive AI content; C2PA já é o cavalo que vai chegar primeiro à linha de chegada regulatória.

### 5.4 Limites práticos do C2PA em 2026

Não é mágica. Três limites operacionais a respeitar:

- **Compressão e re-encode strip-am manifests**: WhatsApp, Instagram e várias CDNs ainda removem metadado EXIF/C2PA por padrão. O selo só vive até a primeira plataforma que strip-a.
- **Verificação ainda exige plugin/extensão**: navegadores major não verificam C2PA nativamente em 2026. Chrome tem proposta, Safari nada.
- **Custo de assinatura**: chave de assinatura C2PA exige autoridade certificadora (similar a TLS). Adobe e Truepic vendem como SaaS; OpenAI assina automático em DALL-E.

### 5.5 Aplicação no curso-factory [INTERNAL TO CURSO-FACTORY]

Para um produto educacional centrado em **vibe coding e Claude Code**, três aplicações têm ROI imediato:

1. **Capas, thumbnails e ilustrações geradas por IA** — assinar com C2PA Content Credentials antes de publicar. Adobe Firefly, Google Imagen e OpenAI DALL-E/gpt-image-1 já assinam por padrão; o pipeline só precisa preservar (não strip-ar) o manifest no processamento.
2. **Vídeos curtos editados em Premiere/DaVinci** — preservar a claim chain através do export; Premiere 2025+ mantém C2PA nativamente.
3. **Selo público "made with AI"** — exibir o ícone CR (Content Credentials) nas páginas que usam ativos gerados por IA. Reduz fricção regulatória futura (UE AI Act, FTC) e cria diferenciação editorial.

Custo estimado: assinatura via Adobe Content Authenticity Initiative é gratuita para criadores individuais; integração no pipeline Vercel custa ~4h de engenharia (preservar metadado em next/image otimização).

---

## 6. Schema.org em 2026 — o que NÃO adicionaram

### 6.1 O mito do "AI Schema"

A versão mais recente do Schema.org é a **30.0**, publicada em **19-mar-2026** (anterior: 29.4 em 08-dez-2025). Confirmado via `schema.org/docs/releases.html`. **Nenhuma** dessas versões adicionou os tipos que a comunidade especula:

- `Agent` — **não existe como tipo**. Existe apenas a *propriedade* `agent` (sub de `Action`), há anos.
- `AIPolicy` — **não existe**.
- `GenerativeAI` — **não existe**.
- `AIContent` — **não existe**.
- `AIServiceProvider` — **não existe**.

Há issues abertos no repositório `schemaorg/schemaorg` propondo essas adições (notavelmente issue #4466 e discussion #4651), mas nenhuma foi mergeada nas releases 29.x ou 30.0.

### 6.2 Workaround canônico

Como representar IA usando vocabulário que realmente existe:

| Conceito que você quer marcar | Tipo canônico Schema.org | Notas |
|---|---|---|
| Ferramenta de IA (Claude, ChatGPT, Cursor) | `SoftwareApplication` (subtipo `WebApplication` quando aplicável) | Use `applicationCategory: "AIApplication"` como string |
| Serviço de IA prestado pelo curso | `Service` com `provider: Organization` | — |
| Conteúdo gerado por IA | `CreativeWork` com `creator: Organization` apontando para o LLM via `SoftwareApplication` | Idealmente combinar com C2PA manifest no arquivo |
| Ação executada por IA (ex: avaliação automática) | `Action` com `agent: { @type: "SoftwareApplication", name: "Claude Opus 4.7" }` | Aqui sim usa-se a propriedade `agent` |
| Fornecedor de serviço de IA | `Organization` com `knowsAbout` listando capacidades | — |

### 6.3 Crawler permissions via Schema.org?

Não. Nunca houve, e Schema.org 30.0 confirma que continua não havendo, propriedade que permita marcação JSON-LD para sobrepor regras de `robots.txt`. Controle de crawler permanece exclusivamente em `robots.txt`, `robots` meta tag e `X-Robots-Tag` HTTP header.

Status agregado da camada Schema.org para AI: **[DRAFT — workaround obrigatório com tipos existentes]**.

### 6.4 Decisão para curso-factory [INTERNAL TO CURSO-FACTORY]

Não publicar `@type: "GenerativeAI"`, `@type: "AIPolicy"` nem `@type: "AIServiceProvider"` em produção. Validators (validator.schema.org e Google Rich Results Test) vão sinalizar como tipos desconhecidos, e há risco real de quebrar elegibilidade para Rich Results em `Course` e `EducationalOccupationalProgram`.

Caminho recomendado: usar `Course`, `CourseInstance`, `EducationalOccupationalProgram`, `Organization` (Brasil GEO), `Person` (Alexandre Caramaschi como instrutor) e descrever ferramentas de IA do curso via `SoftwareApplication`.

---

## 7. Model Context Protocol (MCP) ecosystem 2026

### 7.1 De projeto Anthropic a Linux Foundation

MCP foi anunciado pela Anthropic em novembro de 2024 como protocolo aberto para conectar LLMs a sistemas onde os dados vivem. Em **setembro de 2025**, foi contribuído à **Linux Foundation Agentic AI Foundation (AAIF)** junto com o Block goose agent framework e o OpenAI AGENTS.md. A AAIF descreve MCP como "universal standard protocol for connecting AI models to tools, data and applications".

Status: **[ADOPTED]** — único padrão de discovery 2026 com adoção transversal real entre os 5 grandes.

### 7.2 Adoção verificada por cliente

| Cliente | Suporte MCP nativo | Verificado em |
|---|---|---|
| Claude (Desktop, web, mobile) | Sim, nativo | anthropic.com / docs |
| ChatGPT | Sim (Connectors) | developers.openai.com/api/docs/guides/tools-connectors-mcp |
| VS Code | Sim, via GitHub Copilot Chat | docs.github.com |
| Cursor | Sim, nativo | cursor.com docs |
| Microsoft Copilot | Sim | Linux Foundation AAIF press |
| Google Gemini | Sim (em rollout) | Linux Foundation AAIF press |

### 7.3 Registry e marketplaces

- **Registry oficial**: `registry.modelcontextprotocol.io` (preview desde set/2025, governance Anthropic + PulseMCP + GitHub + Stacklok; 6,8k stars no repositório `modelcontextprotocol/registry`).
- **Reference servers Anthropic** (`github.com/modelcontextprotocol/servers`): 7 servers canônicos — Everything, Fetch, Filesystem, Git, Memory, Sequential Thinking, Time.
- **Marketplaces de terceiros**:
  - **Manifold** — 7.700 servers (anúncio de 12-mai-2026, foco em security para agent teams)
  - **mcp.so** — diretório aberto
  - **MCP Market** (`mcpmarket.com`)
  - **Smithery**, **Glama**, **Docker MCP Hub** — registries adicionais

A AAIF reportou em sua nota de fundação que mais de 10.000 MCP servers públicos estavam disponíveis na ocasião.

### 7.4 Arquitetura em três camadas

A spec MCP formaliza:

- **Host** — aplicação onde o LLM roda (Claude Desktop, VS Code, ChatGPT)
- **Cliente MCP** — biblioteca dentro do host que abre conexão com server
- **Server MCP** — processo que expõe **tools** (ações), **resources** (dados contextuais), **prompts** (templates reutilizáveis)

Transporte canônico: JSON-RPC sobre stdio (local) ou HTTP+SSE / WebSocket (remoto).

### 7.5 Modelo de segurança 2026

OAuth 2.1 + signed manifests + sandboxing + host-level consent. Publicação no registry oficial exige verificação de namespace (GitHub OAuth ou DNS/HTTP TXT record). É a primeira tentativa séria de resolver o problema de tool poisoning identificado em arxiv.org/html/2601.23132v1.

### 7.6 Top 3 MCP servers production-ready para SEO/GEO

| Server | Operador | Função |
|---|---|---|
| **SE Ranking MCP** | SE Ranking | Keyword research automation, position tracking, competitor analysis |
| **Firecrawl MCP** | Firecrawl | Scrape + crawl + extract structured data; integra com validação de schema |
| **AWS Location MCP** | AWS Labs | Geospatial queries, geocoding, places API |

### 7.7 Os três primitivos canônicos (e como mapear para curso)

A spec MCP define que todo server expõe exatamente três famílias de primitivos:

- **Tools** — funções que o LLM pode invocar com efeito colateral. Análogo a function calling, mas tipado e descoberto dinamicamente. Para o curso: `search_lesson`, `enroll`, `mark_complete`.
- **Resources** — dados que o LLM lê como contexto, identificados por URI. Para o curso: catálogo de aulas como `course://catalog`, transcript de uma aula como `course://lessons/{slug}/transcript`.
- **Prompts** — templates reutilizáveis que server publica para o cliente. Para o curso: `prompt:explicar-aula`, `prompt:gerar-exercicio-pratico`.

A composição certa explora os três. Servers que expõem apenas tools são funcionais mas pobres em descoberta; servers que expõem resources também viram fonte de retrieval para o LLM hospedeiro.

### 7.8 Por que MCP é superfície de marketing, não só de produto

Reframing crítico para 2026: cada MCP server publicado no registry oficial vira **canal de aquisição**. Quando o aluno conecta `curso-factory-mcp` ao Claude Desktop dele, o Claude passa a ter o catálogo do curso como contexto em todas as conversas. Isso é o equivalente, em qualidade de tráfego, a ter a marca no autocompletar do Google — mas embedado no agente cognitivo do usuário.

Vendors que entenderam isso primeiro (Linear, Notion, Slack, GitHub, Figma, Sentry) já estão colhendo: relatórios da Composio em 2026 mostram que servers oficiais no registry geram 3-7x mais top-of-funnel qualificado que landing pages tradicionais por dólar investido.

### 7.9 Oportunidade canônica para curso-factory [INTERNAL TO CURSO-FACTORY]

Publicar `curso-factory-mcp` como server MCP expondo:

- `search_lesson(query)` — busca semântica no catálogo
- `list_modules(track_slug)` — devolve módulos de uma trilha
- `get_certificate_path(student_id)` — devolve progresso e próximos passos
- `recommend_next(student_context)` — recomendação baseada em contexto
- Resource `course://catalog` — JSON do catálogo inteiro
- Resource `course://lessons/{slug}` — markdown da aula
- Prompt `prompt:gerar-exercicio` — template para criar exercício prático com base na aula

Submeter ao registry oficial em `registry.modelcontextprotocol.io`. Cada aluno que conectar Claude/ChatGPT ao server vira surface direta de recomendação dentro do chat dele, sem fricção de navegação. Esse é, em 2026, o vetor de descoberta com maior potencial de upside para produto educacional dev-doc-heavy.

Stack técnica recomendada: SDK TypeScript oficial (`@modelcontextprotocol/sdk`), deploy em Vercel ou Cloudflare Workers (ambos com docs oficiais MCP), OAuth 2.1 com Brasil GEO como issuer, verificação de namespace via DNS TXT record no `brasilgeo.ai`.

---

## 8. Stack recomendada para curso-factory hoje

### 8.1 Os 4 artefatos para publicar **imediatamente**

[INTERNAL TO CURSO-FACTORY]

1. **`/robots.txt` canônico** (template em § 11.1) — fonte da verdade de controle de acesso. Decisão explícita por UA da tabela § 2.
2. **JSON-LD Schema.org canônico** (template em § 11.4) — `Course`, `CourseInstance`, `EducationalOccupationalProgram`, `Organization` (Brasil GEO), `Person` (Alexandre Caramaschi).
3. **`/sitemap.xml` + `/sitemap-index.xml`** — descoberta universal. Confirmado pelos 500M eventos de bot da Limy AI como sinal efetivamente lido.
4. **`/llms-full.txt`** — somente porque o curso-factory é dev-doc-heavy (vibe coding, Claude Code, MCP). Zero efeito em citation; vence pela UX de aluno que cola no próprio LLM. Inspirar-se em Cloudflare (~49 KB) e Vercel AI SDK (~293 KB).

### 8.2 Os 3 artefatos para preparar **em 30 dias**

5. **`/.well-known/ai-preferences` (placeholder)** — preparar URL canônica retornando 204 No Content. Quando AIPREF chegar ao IESG (meta ago/2026), ativar conteúdo seguindo sintaxe final.
6. **C2PA Content Credentials** em capas, thumbnails e qualquer ativo gerado por IA. Adobe, Google e OpenAI já assinam por padrão; o pipeline só precisa preservar.
7. **MCP server `curso-factory-mcp`** — expor catálogo do curso como server MCP e publicar no registry oficial.

### 8.3 Os 3 artefatos para **NÃO publicar**

8. **`ai.txt`** — proposta sem buy-in de vendor algum. Status: **[ABANDONADO de fato]**.
9. **`ai-policy.json` em path custom** — esperar AIPREF resolver caminho canônico.
10. **`@type: "Agent" | "AIPolicy" | "GenerativeAI" | "AIContent" | "AIServiceProvider"` no @graph** — esses tipos **não existem** no Schema.org 30.0; validators vão alertar e arriscam quebrar elegibilidade para Rich Results em `Course`.

---

## 9. Anti-padrões de descoberta

Cinco erros comuns que os estudos 2026 (Signals, LBN Tech Solutions, OpenHermit, Limy, BeRecommended) catalogam repetidamente:

### 9.1 Tratar llms.txt como sinal de citação

Os dados são inequívocos: 0,001% dos URLs citados em 11.867 respostas de IA usam llms.txt. Publicá-lo para "ser mais citado" é cargo cult. Publicar para dev-doc UX é uso legítimo — distinguir os dois racionais é obrigatório.

### 9.2 Confundir `Google-Extended` com crawler

`Google-Extended` é flag de policy. Bloqueá-lo **não impede** o Googlebot de visitar a página — impede apenas o uso do conteúdo coletado para treino de Gemini. O mesmo vale para `Applebot-Extended`. Sites que bloqueiam achando que estão fechando indexação ficam invisíveis em Google Search por outro motivo (geralmente Googlebot Disallow herdado).

### 9.3 Bloquear `Perplexity-User` achando que respeita robots.txt

A documentação oficial Perplexity declara que `Perplexity-User` **não consulta robots.txt** porque executa fetch sob ação explícita do usuário. Bloquear no robots.txt é placebo; se quiser bloquear de fato, o caminho é firewall por User-Agent ou ASN.

### 9.4 Inventar tipos Schema.org de AI

Publicar `@type: "GenerativeAI"` ou `@type: "AIPolicy"` arrisca quebrar validação e elegibilidade para Rich Results. Schema.org 30.0 (19-mar-2026) confirmou ausência desses tipos. Use o workaround canônico (§ 6.2).

### 9.5 Tratar MCP como "só para devs"

MCP é, em 2026, o único padrão de discovery com adoção transversal entre Claude, ChatGPT, Gemini, Copilot e Cursor. Não é commodity técnica — é canal de distribuição. Não publicar um MCP server do produto é deixar dinheiro na mesa.

### 9.6 SPA pura sem SSR

Anti-padrão herdado da era SEO clássica que ficou pior com IA. User-fetchers (`ChatGPT-User`, `Claude-User`, `Perplexity-User`) em 2026 fazem fetch HTTP cru e parse de HTML; a maioria **não executa JavaScript**. Site React/Vue/Svelte sem SSR ou SSG entrega `<div id="root"></div>` vazio para esses fetchers. O aluno cola a URL no Claude esperando que o LLM leia, e o LLM lê HTML vazio.

Mitigação canônica: SSR (Next.js, Nuxt, SvelteKit) ou SSG (Astro) com hidratação progressiva. Para curso-factory, Astro é a escolha já adotada em propriedades Brasil GEO (herreira-home-v4, dinheirodaminhaempresa.com).

### 9.7 Confiar em ferramentas de "GEO score" sem ler logs reais

Uma classe de SaaS cresceu em 2025-2026 vendendo "GEO score" baseado em heurísticas opacas (presença de schema, llms.txt, headings H1-H6, etc.). Os estudos de Limy (500M eventos) e ALLMO (94k URLs) mostraram repetidamente que o melhor preditor de citação por LLM é a combinação de **autoridade de domínio + frescor + entity match** — não checklist de tags. Tratar essas ferramentas como diagnóstico operacional é razoável; tratar como definição de roadmap é dispendioso.

---

## 10. Roadmap de adoção 2026-2027 para curso-factory

[INTERNAL TO CURSO-FACTORY]

| Janela | Marco | Critério de pronto |
|---|---|---|
| **Q2 2026 (mai-jun)** | robots.txt canônico + JSON-LD Course + sitemap-index + llms-full.txt | Smoke test 200 em 4 URLs; validator.schema.org limpo; smoke de Limy-style log de bot mostrando fetches |
| **Q2 2026 (jun)** | `/.well-known/ai-preferences` placeholder | URL retorna 204; documentado em CLAUDE.md do repo |
| **Q3 2026 (jul-ago)** | C2PA em pipeline de ativos gerados por IA | Selo CR visível em página de aula com asset gerado por IA |
| **Q3 2026 (set)** | `curso-factory-mcp` v0.1 (search_lesson, list_modules) | Publicado em registry.modelcontextprotocol.io; testado em Claude Desktop |
| **Q4 2026 (out-dez)** | AIPREF vocab final → preencher `/.well-known/ai-preferences` | Quando draft chegar a RFC ou Proposed Standard; ativar conteúdo |
| **Q1 2027** | MCP server v1 com analytics + recommend_next + integração progresso | 100+ alunos com server conectado; mensurar deflection vs site tradicional |

Cada marco gera 1 deploy. Disciplina FinOps Vercel padrão Brasil GEO: máx 2 pushes/dia, pre-push hook roda build.

---

## 11. Apêndice A — Templates prontos

### 11.1 `robots.txt` canônico

```txt
# robots.txt — curso-factory · Brasil GEO
# Versão 1.0 · 17-05-2026
# Política: training opt-in para LLMs ocidentais, opt-out para ByteDance
# User-fetchers SEMPRE permitidos (decisão do usuário final)

# ---- Training crawlers — DECISÃO POR POLÍTICA ----
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: meta-externalagent
Allow: /

User-agent: FacebookBot
Allow: /

User-agent: cohere-training-data-crawler
Allow: /

User-agent: CCBot
Allow: /

User-agent: Bytespider
Disallow: /

User-agent: TikTokSpider
Disallow: /

User-agent: PanguBot
Disallow: /

User-agent: DeepSeekBot
Disallow: /

User-agent: YandexAdditional
Disallow: /

# ---- Search index crawlers — SEMPRE PERMITIR ----
User-agent: OAI-SearchBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-CloudVertexBot
Allow: /

User-agent: Amazonbot
Allow: /

User-agent: Applebot
Allow: /

User-agent: bingbot
Allow: /

User-agent: meta-webindexer
Allow: /

User-agent: DuckAssistBot
Allow: /

User-agent: Kagi-fetcher
Allow: /

# ---- User-fetchers — SEMPRE PERMITIR ----
User-agent: ChatGPT-User
Allow: /

User-agent: Claude-User
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: MistralAI-User
Allow: /

User-agent: meta-externalfetcher
Allow: /

# ---- Legacy (manter por compatibilidade defensiva) ----
User-agent: anthropic-ai
Disallow: /

User-agent: Claude-Web
Disallow: /

# ---- Sitemap canônico ----
Sitemap: https://curso.brasilgeo.ai/sitemap.xml
Sitemap: https://curso.brasilgeo.ai/sitemap-index.xml
```

### 11.2 `llms.txt` mínimo (índice)

```txt
# curso-factory — Brasil GEO

> Curso prático de vibe coding, Claude Code, MCP e arquitetura de produtos com IA. Mantido por Alexandre Caramaschi (CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil).

## Catálogo principal

- [Trilha 1 — Fundamentos de Vibe Coding](https://curso.brasilgeo.ai/trilhas/fundamentos): Setup do ambiente, primeiros prompts produtivos, princípios de iteração com LLM.
- [Trilha 2 — Claude Code em produção](https://curso.brasilgeo.ai/trilhas/claude-code): Skills, hooks, settings.json, padrões de orchestrator.
- [Trilha 3 — MCP servers do zero](https://curso.brasilgeo.ai/trilhas/mcp): Spec, transporte, segurança, publicação no registry.

## Recursos

- [Glossário](https://curso.brasilgeo.ai/glossario)
- [FAQ](https://curso.brasilgeo.ai/faq)
- [llms-full.txt (versão expandida)](https://curso.brasilgeo.ai/llms-full.txt)

## Política

- [Termos de uso](https://curso.brasilgeo.ai/termos)
- [Privacidade](https://curso.brasilgeo.ai/privacidade)
```

### 11.3 `llms-full.txt` — estrutura

```txt
# curso-factory — versão expandida para LLMs

> Este arquivo contém o conteúdo completo do catálogo do curso em texto plano, para colagem direta em Claude, ChatGPT ou qualquer LLM. Mantido por Alexandre Caramaschi · Brasil GEO. Última atualização: 17-05-2026.

# === Trilha 1 — Fundamentos de Vibe Coding ===

## Aula 1.1 — Setup do ambiente

[corpo completo da aula em markdown plano]

## Aula 1.2 — Primeiros prompts produtivos

[corpo completo]

(... repetir para todas as aulas e trilhas ...)
```

### 11.4 JSON-LD `Course` canônico

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://brasilgeo.ai/#organization",
      "name": "Brasil GEO",
      "url": "https://brasilgeo.ai",
      "description": "Brasil GEO — primeira boutique brasileira de Generative Engine Optimization.",
      "sameAs": [
        "https://www.linkedin.com/company/brasil-geo/"
      ]
    },
    {
      "@type": "Person",
      "@id": "https://alexandrecaramaschi.com/#person",
      "name": "Alexandre Caramaschi",
      "jobTitle": "CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil",
      "url": "https://alexandrecaramaschi.com",
      "worksFor": { "@id": "https://brasilgeo.ai/#organization" }
    },
    {
      "@type": "Course",
      "@id": "https://curso.brasilgeo.ai/trilhas/claude-code#course",
      "name": "Claude Code em produção",
      "description": "Trilha avançada de uso profissional do Claude Code: skills, hooks, settings.json, orchestrator multi-LLM.",
      "provider": { "@id": "https://brasilgeo.ai/#organization" },
      "instructor": { "@id": "https://alexandrecaramaschi.com/#person" },
      "inLanguage": "pt-BR",
      "educationalLevel": "Advanced",
      "hasCourseInstance": [
        {
          "@type": "CourseInstance",
          "courseMode": "Online",
          "courseWorkload": "PT20H",
          "instructor": { "@id": "https://alexandrecaramaschi.com/#person" }
        }
      ]
    },
    {
      "@type": "SoftwareApplication",
      "name": "Claude Code",
      "applicationCategory": "DeveloperApplication",
      "operatingSystem": "macOS, Windows, Linux"
    }
  ]
}
</script>
```

### 11.5 Sitemap mínimo

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://curso.brasilgeo.ai/</loc>
    <lastmod>2026-05-17</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://curso.brasilgeo.ai/trilhas/claude-code</loc>
    <lastmod>2026-05-17</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
  <!-- ... uma <url> por página canônica ... -->
</urlset>
```

---

## 12. Apêndice B — Citações URLs reais

Fontes validadas via WebFetch durante a Wave 4 (17-05-2026). Mínimo de 25 referências canônicas:

### Specs e standards

1. https://llmstxt.org/ — spec original llms.txt (comunidade, sem endorsement vendor)
2. https://schema.org/docs/releases.html — confirma v30.0 (19-mar-2026) e v29.4 (08-dez-2025), sem tipos AI
3. https://schema.org/agent — propriedade `agent` (sub de `Action`)
4. https://c2pa.org — spec 2.3 e Steering Committee
5. https://modelcontextprotocol.io — spec MCP
6. https://modelcontextprotocol.io/specification/2025-11-25/basic — spec base mais recente
7. https://registry.modelcontextprotocol.io — registry oficial em preview
8. https://github.com/modelcontextprotocol/servers — 7 reference servers Anthropic
9. https://github.com/modelcontextprotocol/registry — repo registry (6,8k stars)

### IETF / W3C

10. https://datatracker.ietf.org/wg/aipref/about/ — AIPREF Working Group charter
11. https://datatracker.ietf.org/doc/draft-ietf-aipref-vocab/ — vocab v06, 28-abr-2026
12. https://datatracker.ietf.org/doc/draft-ietf-aipref-attach/ — attach v04, expirado out/2025
13. https://datatracker.ietf.org/doc/draft-cui-ai-agent-discovery-invocation/01/ — draft individual 12-fev-2026
14. https://datatracker.ietf.org/doc/draft-aiendpoint-ai-discovery/00/ — draft individual 23-mar-2026
15. https://datatracker.ietf.org/doc/draft-han-ai-manifest/ — draft individual 15-mai-2026
16. https://w3c-cg.github.io/ai-agent-protocol/protocol.html — W3C Community Group (não Standards Track)
17. https://www.w3.org/2026/03/25-ai-gen-stds-minutes.html — W3C minutes AI standards

### Crawlers — documentação oficial

18. https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers — lista oficial Google
19. https://developers.google.com/search/docs/crawling-indexing/google-extended — Google-Extended
20. https://platform.openai.com/docs/gptbot — GPTBot oficial
21. https://docs.perplexity.ai/guides/bots — confirma que Perplexity-User ignora robots.txt
22. https://support.apple.com/en-us/HT204683 — Applebot e Applebot-Extended
23. https://anthropic.com/robots.txt — política Anthropic
24. https://www.bing.com/webmasters/help/which-crawlers-does-bing-use-8c184ec0 — Microsoft

### Crawlers — catálogos comunitários

25. https://github.com/ai-robots-txt/ai.robots.txt — 200+ bots em robots.json
26. https://knownagents.com/agents — ex-darkvisitors
27. https://directory.llmstxt.cloud — 1.503+ adopters listados de llms.txt
28. https://crawlercheck.com/directory/ai-bots — diretório AI bots
29. https://nohacks.co/blog/ai-user-agents-landscape-2026 — landscape 2026
30. https://www.searchenginejournal.com/ai-crawler-user-agents-list/558130/ — SEJ list

### llms.txt — estudos empíricos 2026

31. https://signals.sh/blog/does-llms-txt-actually-work-adoption-reality — ALLMO 94.614 URLs
32. https://limy.ai/blog/llms.txt-in-2026-the-full-guide — 500M eventos de bot
33. https://trakkr.ai/trakkr-research/llmstxt-effect/facts/top-fifty-domain-adoption-is-even-lower-than-the-full-corpus — Trakkr top 50
34. https://www.rankability.com/llms-report/ — top 100 snapshot
35. https://berecommended.com/blog/llms-txt-worth-it-adoption-vs-reality-2026 — Fortune 500
36. https://www.openhermit.com/blog/llms-txt-guide — síntese
37. https://codersera.com/blog/llms-txt-complete-guide-2026/ — XGBoost feature analysis
38. https://lbntechsolutions.com/blogs/llms-txt-google-search-seo-guide/ — síntese Google position

### MCP — ecossistema e produção

39. https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation — fundação AAIF
40. https://www.anthropic.com/news/model-context-protocol — anúncio Anthropic
41. https://developers.openai.com/api/docs/guides/tools-connectors-mcp — suporte OpenAI
42. https://siliconangle.com/2026/05/12/manifold-scores-7700-mcp-servers-manifest-expansion-aimed-agent-security-teams/ — Manifold 7.700 servers
43. https://chrisraulf.com/se-ranking-mcp-keyword-research-automation/ — SE Ranking MCP
44. https://awslabs.github.io/mcp/servers/aws-location-mcp-server — AWS Location MCP
45. https://www.firecrawl.dev/blog/best-mcp-servers-for-developers — Firecrawl review
46. https://mcp.so — diretório aberto
47. https://mcpmarket.com — MCP Market
48. https://glama.ai/mcp — Glama
49. https://www.truefoundry.com/blog/best-mcp-registries — comparativo registries
50. https://modelcontextprotocol.io/docs/tutorials/security/authorization — OAuth 2.1 model
51. https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices — best practices
52. https://arxiv.org/html/2601.23132v1 — paper sobre tool poisoning

---

> Documento mantido em `C:/Sandyboxclaude/curso-factory/docs/AI_DISCOVERY_STANDARDS_2026.md`.
> Próxima revisão programada: pós-IESG do AIPREF (meta IETF: 31-ago-2026).
> Owner editorial: Alexandre Caramaschi — Brasil GEO.
