# Como contribuir

Obrigado pelo interesse no curso-factory. Este guia cobre o essencial para abrir uma issue ou um PR útil.

## Antes de qualquer coisa

1. Veja se sua dúvida está respondida na [Wiki](https://github.com/alexandrebrt14-sys/curso-factory/wiki).
2. Confira se sua proposta já está em [Roadmap-and-Gaps](https://github.com/alexandrebrt14-sys/curso-factory/wiki/Roadmap-and-Gaps).
3. Procure issues existentes (abertas e fechadas) para evitar duplicata.

## Setup local

```bash
git clone https://github.com/alexandrebrt14-sys/curso-factory.git
cd curso-factory
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -e .
cp .env.example .env         # preencha as 5 chaves de API
python -m pytest tests/ -v   # 74 testes verde
```

## Princípios não negociáveis

### 1. Idioma

Todo conteúdo de curso e copy é **Português do Brasil com acentuação completa**.

- Proibido: "nao", "voce", "producao" (sem acento) em texto visível ao usuário.
- Exceção: código-fonte, variáveis, commit messages em inglês, slugs/URLs ASCII.

### 2. Sem identidade hardcoded

Nenhum cliente, autor ou domínio pode estar hardcoded no código. Tudo passa por `ClientContext` (carregado de `config/clients/<id>/client.yaml`).

Se você precisa de uma constante que varia por cliente, é campo de YAML.

### 3. Sem emojis

Em código, copy de curso, commits, PRs, issues — sem emojis.

### 4. Quality gate

Toda mudança que afeta validação precisa passar pelo `QualityGate` em pelo menos 1 teste novo.

### 5. FinOps real

Mudanças que aumentam custo de API precisam justificar. Budget guard ($5 max Claude / $10 max total por curso) é regra, não recomendação.

## Workflow para PR

### 1. Branch a partir de `main`

```bash
git checkout main
git pull
git checkout -b <tipo>/<descricao-curta>
```

Tipos: `feat`, `fix`, `refactor`, `docs`, `test`, `ci`, `chore`.

Exemplos:
- `feat/cli-index-subcommand`
- `fix/voice-guard-isolation`
- `refactor/parametrize-content-checker`

### 2. Faça mudanças pequenas e focadas

- Um PR cobre **um** tema. Misturar refactor + nova feature dificulta review.
- Cada commit tem mensagem clara. Convenção: `<tipo>(<area>): <descricao>` em inglês ou português, mas consistente.

### 3. Testes obrigatórios

Toda mudança de comportamento precisa de:
- Pelo menos 1 teste novo (`tests/test_*.py`).
- Não diminuir o número total de testes verde.
- `python -m pytest tests/` 100% passa antes de abrir o PR.

### 4. Abra o PR

Use o template (preenche automaticamente). Marque as áreas afetadas, faça o checklist honestamente, descreva como testar.

Se fechar uma issue, escreva `Closes #N` no body — o GitHub fecha automaticamente quando merged.

### 5. CI precisa estar verde

Os 2 workflows obrigatórios:
- **tests** — pytest em Python 3.11 e 3.12
- **Security scan (Python)** — bandit, pip-audit, gitleaks

### 6. Review

Atribua review se souber a quem. Se não, deixe a triagem mover.

## Convenções de código

### Imports

```python
# Stdlib primeiro
from __future__ import annotations
import json
import logging
from pathlib import Path
from typing import TYPE_CHECKING

# Terceiros
import httpx
import yaml
from pydantic import BaseModel

# Internos (sempre absolutos)
from src.cache import Cache
from src.cost_tracker import CostTracker
```

### Tipos

- Pydantic v2 para tudo que cruza camadas.
- `dataclass` para tipos internos sem validação.
- `TYPE_CHECKING` para imports que só servem aos type hints (evita circular).

### Naming

- Variáveis e funções: `snake_case`.
- Classes: `PascalCase`.
- Constantes: `SCREAMING_SNAKE_CASE`.
- Slugs/URLs: ASCII kebab-case (sem acento).

### Comentários

Default: zero. Só escrever quando o **porquê** é não óbvio (constraint oculto, workaround para bug específico, invariante sutil).

Não escrever:
- O **o quê** o código faz (nome da função já diz).
- Referência a tarefa atual (`# fix do issue #123`) — vai pro PR description.

## Convenções de commits

```
<tipo>(<area>): <resumo curto em imperativo>

<corpo opcional explicando contexto, motivação, trade-off>
```

**Tipos comuns:** `feat`, `fix`, `refactor`, `docs`, `test`, `ci`, `chore`, `perf`.

**Áreas:** `cli`, `pipeline`, `validators`, `voice-guard`, `multi-tenant`, `finops`, `cache`, `wiki`, etc.

Exemplos:

```
feat(cli): adiciona subcomando index para integração com Supabase
fix(voice-guard): isolamento entre clientes não estava ativo no auto_fix
refactor(content-checker): parametriza min_tables_per_module via client.yaml
docs(wiki): atualiza Roadmap-and-Gaps com 3 issues novos
```

## Reportando problemas

### Bug

Use o template de bug report. Inclua:
- Versão do Python e SO.
- Cliente em uso.
- Comando que falhou.
- Stack trace completo.
- Status dos testes locais.

### Feature

Use o template de feature request. Inclua:
- Caso de uso concreto.
- Proposta de API/comportamento.
- Esforço estimado em horas.
- Prioridade sugerida.

### Pergunta

Se a wiki não cobre, use o template de pergunta dizendo quais páginas você consultou.

## Reconhecimento

Mudanças significativas merecem entrada na wiki. Se seu PR mudou arquitetura, atualize:

- [[Architecture]] se você mudou camadas
- [[Roadmap-and-Gaps]] se resolveu um gap (mover de Gaps para Estado atual)
- [[Refactor-2026-04-29]] (ou crie novo `Refactor-AAAA-MM-DD.md` para refatoração grande)

## Conduta

Ver [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). TL;DR: respeito mútuo, foco técnico, sem ataque pessoal.
