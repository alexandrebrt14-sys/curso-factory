---
name: involucro-copiado-de-curso-irmao
description: "Curso novo nascido de cópia de outro serve FAQ, bio e JSON-LD do curso errado; checklist de invólucro e FAQ como fonte única"
metadata:
  type: mistake
  created: 2026-07-25
---

Curso novo **nunca** nasce de cópia do `page.tsx` de um curso pronto sem checklist
de invólucro: hero, FAQ, bio do autor, breadcrumb, `Course.description`, `FAQPage`
e keywords. O modo de falha é sempre o mesmo — o token do nome é substituído, o
corpo do FAQ e da bio não. Detecção barata: grep pelo nome e pelos termos
característicos dos OUTROS cursos dentro dos arquivos do curso novo.

Prevenção estrutural: o FAQ vive numa constante única (`FAQ_ITEMS`) consumida
pelo HTML visível e pelo JSON-LD via `.map()` — divergência vira impossível.
No JSON-LD, `provider.name: "Brasil GEO"` anda com `url: "https://brasilgeo.ai"`;
o domínio pessoal pertence só ao `author`.

Relacionadas: [[numeros-de-curso-digitados-derivam]], [[arquivo-de-conteudo-sem-consumidor]].

---

## Linha do tempo (append-only, ordem reversa)

- **2026-07-25** — [criação] Auditoria dos 53 cursos do portal /educacao:
  `seo-ecommerce` servia em produção o invólucro inteiro de
  `digital-pr-link-building` — 6 perguntas de FAQ sobre Digital PR citando
  Connectively e Qwoted, bio do autor, `Course.description` e `FAQPage` do
  JSON-LD, lidos por crawlers e LLMs. Mesmo defeito já havia atingido
  `vendas-consultivas` (servia texto de CRO) e `gestao-projetos-geo`. Também
  encontrados: FAQ do `setup-claude-code` apontando para módulos 7 e 10
  (numeração do irmão Mac; no Windows são 6 e 11) e `provider.url` com domínio
  pessoal em 5 cursos.
