# Multi-tenancy — curso-factory

A curso-factory foi extraída do pipeline original Brasil GEO / Alexandre Caramaschi para se tornar uma fábrica de cursos **replicável** para qualquer empresa. Esta documentação é o playbook de integração para um novo cliente.

## Conceito: ClientContext

Toda variação entre clientes — autor, domínio, branding, padrão editorial, voice guard rules, diretórios de output — está consolidada em um único objeto: `ClientContext`.

O objeto é carregado a partir de um YAML em `config/clients/<id>/client.yaml` e injetado em todo o pipeline: agentes, validadores, geradores, CLI.

```
config/clients/default/client.yaml   # Brasil GEO / Alexandre (cliente original)
config/clients/acme/client.yaml      # Exemplo fictício — ACME Consultoria
config/clients/_template/client.yaml # Template com TODOs para novo cliente
```

O `ClientContext` está definido em `src/clients/context.py` e é carregado por `src/clients/loader.py`.

## Fluxo de integração de um novo cliente

### 1. Criar diretório e YAML

```bash
cp -r config/clients/_template config/clients/minhaempresa
$EDITOR config/clients/minhaempresa/client.yaml
```

### 2. Preencher dados mínimos

Os campos obrigatórios para um cliente funcional:

```yaml
id: minhaempresa

author:
  name: "Nome Completo do Autor"
  credential: "CEO da Empresa X, ex-Y na Z"

domain:
  canonical_url: "https://empresa.com.br"
  educacao_path: "/cursos"

voice_guard:
  enabled: true
  min_score: 70
  canonical:
    company: "Empresa X"
    founder: "Nome Completo"
```

Os campos de branding (`hero_gradient_from`, `badge_color`) têm defaults azuis; edite se a empresa tem paleta própria.

### 3. Validar o cliente

```bash
python cli.py clients
```

Deve listar o novo cliente junto com `default`:

```
Clientes configurados (3):

  acme                 Maria Silva @ https://acme-consultoria.com.br
                       voice_guard=ON min_score=70 style=business
  default              Alexandre Caramaschi @ https://alexandrecaramaschi.com
                       voice_guard=ON min_score=70 style=hsm_hbr_mit_sloan
  minhaempresa         Nome Completo @ https://empresa.com.br
                       voice_guard=ON min_score=70 style=business
```

### 4. Gerar o primeiro curso

```bash
python cli.py create "Nome do Curso" --client minhaempresa
```

Ou, para uso em sessão (CI, lote), via env var:

```bash
export CURSO_FACTORY_CLIENT=minhaempresa
python cli.py create "Nome do Curso"
```

### 5. Onde os artefatos vão

| Cliente            | Diretório de output                   |
|--------------------|--------------------------------------|
| `default`          | `output/` (layout legado preservado) |
| qualquer outro ID  | `output/clients/<id>/`               |

Dentro de cada output: `drafts/`, `approved/`, `deployed/`, `costs.json`.

## Campos de `client.yaml` — referência completa

| Seção | Campo | Propósito |
|-------|-------|-----------|
| raiz | `id` | Identificador único (precisa bater com o nome do diretório) |
| `author` | `name` | Aparece no SEO, hero, schema.org |
| `author` | `credential` | Linha de credencial curta (ex: "CEO da X, ex-Y na Z") |
| `author` | `title_seo_suffix` | Sufixo do `<title>` (default = `author.name`) |
| `domain` | `canonical_url` | URL raiz (sem trailing slash, ex: `https://empresa.com`) |
| `domain` | `educacao_path` | Path dos cursos (ex: `/cursos`, `/educacao`, `/academy`) |
| raiz | `landing_page_dir` | Path relativo à raiz do repo apontando para a landing page; deixe vazio se não houver |
| raiz | `educacao_dir` | Path relativo para `<landing>/src/app/<cursos>/` (opcional) |
| `branding` | `hero_gradient_from/to` | Cores hex do gradiente do hero |
| `branding` | `badge_color` | Cor do badge de nível/duração |
| `editorial` | `style` | `hsm_hbr_mit_sloan` \| `business` \| `academic` \| `technical` |
| `editorial` | `reference_publications` | Lista de publicações de referência para tom (ex: HBR, McKinsey) |
| `editorial` | `bloom_min_level` | Nível Bloom mínimo em objetivos (3=aplicar, 4=analisar) |
| `editorial` | `knowles_min_principles` | Mínimo de princípios de Knowles detectáveis (de 6) |
| `editorial` | `words_per_module_min/max` | Faixa de contagem de palavras por módulo |
| `voice_guard` | `enabled` | `false` desabilita o gate editorial (útil em clientes sem padrão rígido) |
| `voice_guard` | `min_score` | Score mínimo (0-100) para aprovar (default 70) |
| `voice_guard.canonical` | `company/founder` | Nomes canônicos exigidos |
| `voice_guard.canonical` | `credential_fragments` | Lista de fragmentos de credencial que ganham bonus de naming |
| `voice_guard.canonical` | `domains` | Domínios legítimos do cliente |
| `voice_guard.forbidden` | `titles` | Títulos inventados que bloqueiam absolutamente (Especialista #1, Top Voice, etc.) |
| `voice_guard.forbidden` | `company_names` | Nomes errados da empresa (variantes confundíveis) |
| `voice_guard.forbidden` | `domains` | Domínios alucinados pelos LLMs |
| `voice_guard.forbidden` | `rhetoric_openers` | Aberturas retóricas a evitar |
| `voice_guard.forbidden` | `ai_disclaimers` | Padrões de "Como modelo de IA, ..." |
| `output` | `base_dir` | Diretório raiz de output (default `output`) |

## Cuidados ao preencher `forbidden.company_names`

O matching é **substring case-insensitive**. Evite listar uma palavra que seja prefixo/substring do nome canônico, ou você criará um auto-bloqueio.

Exemplo **errado**: canonical=`"ACME Consultoria"`, forbidden=`["Acme"]` — qualquer menção a ACME Consultoria é bloqueada porque `"acme" in "acme consultoria"`.

Exemplo **certo**: canonical=`"ACME Consultoria"`, forbidden=`["ACME Tech", "Grupo ACME", "Acme Brasil"]`.

## Padrões editoriais por `editorial.style`

Hoje o valor `style` é **documentação de intenção** — o voice guard programático não distingue estilos. O campo é consumido por:

1. Humanos lendo o YAML (saber qual é o tom alvo)
2. Futuros prompts externos (`src/templates/prompts/`) que podem ser selecionados por cliente
3. Convenções editoriais internas do cliente

| Valor | Sugestão de tom |
|-------|-----------------|
| `hsm_hbr_mit_sloan` | Analítico, dados, evidências, tom HBR/MIT Sloan (padrão da Brasil GEO) |
| `business` | Pragmático, orientado a resultado, menos denso |
| `academic` | Formal, citações, rigor científico |
| `technical` | Hands-on, código, documentação passo-a-passo |

Para customizar **os prompts** por cliente, o próximo passo é criar `config/clients/<id>/prompts/*.md` sobrescrevendo os arquivos em `src/templates/prompts/`. Essa feature está planejada mas não implementada nesta onda.

## Como o voice guard usa o client

```python
from src.clients import load_client
from src.validators.voice_guard import voice_guard_check

client = load_client("minhaempresa")
resultado = voice_guard_check(texto_do_modulo, client=client)

if not resultado.aprovado:
    print(resultado.report())
```

Sob o cliente `minhaempresa`, o voice guard:

- Bloqueia textos com menção a `voice_guard.forbidden.titles/company_names/domains`
- Bloqueia aberturas retóricas listadas em `forbidden.rhetoric_openers`
- Bloqueia disclaimers de IA listados em `forbidden.ai_disclaimers`
- Dá bonus se o texto menciona ≥2 fragmentos de `canonical.credential_fragments`
- Avisa se o texto fala de "consultoria/empresa" sem referenciar `canonical.company` nem `canonical.founder`

## Integração no QualityGate

O `QualityGate` recebe o ClientContext no construtor e roda o voice_guard_check como **4ª camada bloqueante**:

```python
from src.validators.quality_gate import QualityGate
from src.clients import load_client

gate = QualityGate(client=load_client("minhaempresa"), auto_fix=True)
resultado = gate.check_text(texto, curso_id="meu-curso")
# resultado.voice_guard_ok, resultado.voice_guard_score
```

Se o voice_guard_score < `min_score` (padrão 70) **ou** houver qualquer erro crítico (título proibido, nome errado, domínio proibido), `gate.aprovado = False`.

## Matriz de responsabilidades: o que é do cliente, o que é do framework

| Item | Cliente (YAML) | Framework (código) |
|------|----------------|---------------------|
| Nome do autor e credencial | ✔ | |
| Domínio canônico e path | ✔ | |
| Cores do hero | ✔ | |
| Naming canônico (empresa/fundador) | ✔ | |
| Listas de proibições (títulos, domínios, clichês abertura) | ✔ | |
| Limites editoriais (Bloom nível, Knowles, palavras) | ✔ | |
| Pipeline de 5 etapas (Perplexity → GPT-4o → Gemini → Groq → Claude) | | ✔ |
| Camadas do Quality Gate (acentos, conteúdo, links, HTML, voice_guard) | | ✔ |
| Templates TSX (page.tsx, layout.tsx) | | ✔ |
| Integração com cost tracker e budget guard | | ✔ |
| Clichés universais de IA (disclaimers, retórica barata) | (opcional override) | ✔ (defaults no _template) |

## Próximos passos para multi-tenant completo

Esta onda de refactor cobre o essencial. Próximas ampliações planejadas:

- `config/clients/<id>/prompts/*.md` — prompts por cliente sobrescrevendo `src/templates/prompts/`
- `config/clients/<id>/courses.yaml` — catálogo de cursos por cliente (hoje é único e global)
- Cost tracking segregado por cliente no `cost_tracker.py` (hoje é por `course_id`)
- `course_indexer.py` consciente de cliente (hoje puxa de um único `LANDING_PAGE_DIR`)
