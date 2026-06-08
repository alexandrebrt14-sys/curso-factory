# Patch sugerido para `CLAUDE.md`

Esta wave criou a camada `wiki/` em branch isolada
(`wiki/karpathy-llm-wiki-pattern`) sem editar o `CLAUDE.md` para evitar
conflito com trabalho em progresso na branch
`feat/geo-seo-knowledge-2026-deep-research` (humanizer.py, wave maio
pós-IO, stylometry_checker, etc).

Em onda futura, após merge da `feat/geo-seo-knowledge-2026-deep-research`
para main, aplicar o bloco abaixo no `CLAUDE.md`, idealmente logo após
a seção "REGRA #0 — IDIOMA" e antes da "REGRA #1 — Contexto enriquecido
GEO/SEO 2026".

---

## REGRA #0.5 — Wiki workflow obrigatório (padrão Karpathy LLM Wiki)

Repositório adotou em 2026-05-26 o padrão LLM Wiki descrito por Andrej
Karpathy em
[gist.github.com/karpathy/442a6bf555914893e9891c11519de94f](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
Camada `wiki/` é mutável, atômica, cross-linkada e mantida por agentes
LLM. Convive com `docs/research/` (raw imutável), `docs/` (canônico
longo) e este `CLAUDE.md` (schema + ledger narrativo). Detalhes em
`docs/karpathy-llm-wiki-methodology.md` e ADR completo em
`wiki/decisions/ADR-001-adopcao-llm-wiki.md`.

**Disciplina inviolável:**

1. **Antes** de produzir curso novo via `python cli.py create`:
   consultar `wiki/index.md`, `wiki/clients/<id>.md` (cliente ativo),
   `wiki/overview/topologia-cobertura-cursos.md` para mapear o que já
   existe.
2. **Após** quality gate aprovar curso (status → `output/approved/`):
   rodar `python scripts/wiki/sync-courses.py` para registrar
   automaticamente em `wiki/courses/<slug>.md` com cross-links para
   cliente, conceitos editoriais aplicados e sources usadas.
3. **Antes** de qualquer push que toque `wiki/`: rodar
   `python scripts/wiki/lint.py`. Endereçar `broken_crosslinks` fora do
   backlog declarado em `wiki/index.md` e `missing_frontmatter` zero.
4. **Antes** de pesquisa nova (Perplexity, sub-agent Opus): consultar
   `wiki/concepts/` e `wiki/sources/` para evitar re-trabalho. Regra
   Karpathy K-07. Detalhes em `scripts/wiki/query-playbook.md`.
5. **Mensalmente**: review formal em `wiki/reviews/YYYY-MM-DD-mensal.md`
   com endereçamento de órfãos e stale claims acumulados.

**Tipos canônicos de página wiki:**

- `wiki/entities/` — LLMs do pipeline (Perplexity, GPT-4o, Gemini, Groq,
  Claude), validators (accent_checker, content_checker, link_checker,
  html_validator, voice_guard), autores canônicos.
- `wiki/concepts/` — definições atômicas reusáveis (andragogia Knowles,
  Bloom, HSM/HBR, ClientContext, Quality Gate, etc).
- `wiki/clients/` — uma página por cliente multi-tenant. Espelha
  `config/clients/<id>/client.yaml` mas legível e cross-linkada.
- `wiki/courses/` — uma página por curso aprovado. Populado via
  `sync-courses.py`.
- `wiki/queries/` — Q&A pré-sintetizado de decisões recorrentes
  (qual nível Bloom usar, qual padrão editorial para cliente Y, etc).
- `wiki/overview/` — mapas de cobertura por vertical, gaps,
  sobreposições.
- `wiki/decisions/` — ADRs cujo "porquê" não cabe em commit message.
- `wiki/sources/` — papers, gists, dossiês externos referenciados >1 vez.
- `wiki/reviews/` — relatórios periódicos de lint.

**Convenções inegociáveis:**

- Frontmatter YAML com `name`, `type`, `status`, `created`, `updated`,
  `sources`, `related`.
- Cross-links `[[slug]]` no corpo. Filenames ASCII kebab-case.
- Português PT-BR acentuado (REGRA #0).
- Sem emojis. Sem em-dash em copy editorial.
- Cada onda fecha pelo menos 1 item do backlog explícito ou justifica.

**Métricas (revisão em 30/60/90 dias após 2026-05-26):** crescimento de
5+ páginas wiki por wave de cursos; backlog reduz; 0 órfãos
não-justificados em review mensal; pelo menos 50% dos cursos aprovados
do trimestre com `wiki/courses/<slug>.md` correspondente.

---

## Plug-in opcional em `cli.py` (também proposto)

No próximo refactor do `cli.py`, adicionar sub-comando `wiki` com 3
ações, reduzindo fricção:

```python
def cmd_wiki(args: argparse.Namespace) -> int:
    """Sub-comando wiki: sync, lint ou query."""
    import subprocess
    from pathlib import Path

    script_dir = Path(__file__).parent / "scripts" / "wiki"

    if args.acao == "sync":
        return subprocess.call(["python", str(script_dir / "sync-courses.py")])
    if args.acao == "lint":
        extra = ["--fix-log"] if args.fix_log else []
        return subprocess.call(["python", str(script_dir / "lint.py"), *extra])
    if args.acao == "query":
        # Por enquanto: imprime hint para abrir wiki/index.md
        print("Abra wiki/index.md e procure pelo termo. Detalhes em")
        print("scripts/wiki/query-playbook.md.")
        return 0
    return 1


# No build_parser():
wiki_p = subparsers.add_parser("wiki", help="operacoes no grafo wiki/")
wiki_p.add_argument("acao", choices=["sync", "lint", "query"])
wiki_p.add_argument("--fix-log", action="store_true",
                    help="apenda entrada em wiki/log.md (apenas para lint)")
wiki_p.set_defaults(func=cmd_wiki)
```

Uso após o patch:

```bash
python cli.py wiki sync          # registra cursos aprovados sem entrada wiki
python cli.py wiki lint          # valida grafo
python cli.py wiki lint --fix-log
python cli.py wiki query         # hint para usar wiki/index.md
```
