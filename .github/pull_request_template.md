# Pull Request

## Resumo

<!-- 1-3 linhas. O quê e por quê. -->

## Tipo de mudança

- [ ] bug fix
- [ ] nova feature
- [ ] refatoração (sem mudança de comportamento)
- [ ] documentação
- [ ] testes
- [ ] CI / build / deps
- [ ] outro:

## Áreas afetadas

<!-- marque tudo que aplica -->

- [ ] cli
- [ ] agents / pipeline
- [ ] validators / quality-gate
- [ ] voice-guard
- [ ] multi-tenant (`ClientContext`, `config/clients/*`)
- [ ] finops / cost-tracker
- [ ] cache
- [ ] converters
- [ ] generators (TSX / Jinja2)
- [ ] parsers (markdown)
- [ ] indexer
- [ ] prompts (`src/templates/prompts/*.md`)
- [ ] docs / wiki

## Checklist

- [ ] Rodei `python -m pytest tests/` e está verde (74 testes ou mais)
- [ ] Adicionei testes cobrindo o novo comportamento (se aplicável)
- [ ] Atualizei a [wiki](https://github.com/alexandrebrt14-sys/curso-factory/wiki) ou docs locais (se aplicável)
- [ ] Atualizei `CLAUDE.md` se a mudança altera workflow para Claude Code
- [ ] Não introduzi defaults com identidade de cliente hardcoded — tudo via `ClientContext`
- [ ] Sem chaves de API, secrets ou paths absolutos no código
- [ ] Sem emojis no código, copy ou commits
- [ ] PT-BR com acentuação completa em conteúdo de curso e copy

## Como testar

```bash
# Comandos para o revisor reproduzir e validar
python -m pytest tests/ -v
python cli.py <comando relevante>
```

## Issues relacionadas

<!-- "Closes #N" para fechar automaticamente quando merged -->

Closes #
