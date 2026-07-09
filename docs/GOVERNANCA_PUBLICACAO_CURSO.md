# Governança de publicação de curso (curso-factory to landing-page-geo)

Destilado do ciclo de publicação do curso "Reinforcement Learning para Vibecoding" (2026-07-09). Objetivo: parar a recorrência de gotchas que já apareceram em ciclos anteriores (curso agentic-operating-model, 2026-07-08) porque a lição não estava numa governança aplicada.

## Fluxo real (o `create` NÃO publica)

1. `python cli.py create "<Nome>"` gera apenas `output/drafts/<slug>_<ts>.json`. As etapas (research, draft, analyze, classify, review) são strings. **A etapa `review` às vezes recebe só o bloco de metadados JSON e devolve lixo** ("o material não contém conteúdo de curso") — use o conteúdo da etapa `draft`, não do `review`.
2. O curso precisa existir em `config/courses.yaml` antes do `create` (match por substring do nome). A `descricao` de cada módulo em `estrutura_modulos` vai direto ao redator como "conteúdo esperado" — é o único canal para injetar pesquisa externa; encha-a de densidade.
3. Chaves via `curso-factory/.env` (gitignorado). Espera `GOOGLE_API_KEY`, mas o geo-orchestrator usa `GOOGLE_AI_API_KEY` — **remapear**. `HTTP_TIMEOUT` (env, default 600s): 60s era curto demais para geração long-form e research deep, caía em espiral de fallback.
4. Montagem na landing é manual: converter o draft no formato `<CoursePage>`/`STEPS` e criar `src/app/educacao/<slug>/{layout.tsx,page.tsx}` (+ `modulos/*.ts`). Não há rota `[slug]`; conteúdo é TypeScript embutido, sem MD/MDX. O `docs/EDUCACAO_README.md` da landing está OBSOLETO — não use.

## Gotchas recorrentes na landing (verificar SEMPRE)

- **Tabela do `CourseFormattedText`:** a linha separadora `| --- |` faz o renderer pular o separador E a primeira linha de dados (`j++; continue`). Escreva tabelas markdown com header + linhas de dados, SEM a linha `| --- |`. Bullets exigem prefixo `-- `. Inline `` `code` `` não é processado (só `**negrito**`); código real vai em bloco `code`.
- **PT-BR Accent Guard (`scripts/ci/check-ptbr-accents.sh`):** bloqueia com >=10 palavras PT-BR sem acento em conteúdo de leitura. Mascara strings entre aspas SEM espaço (slugs/ids); texto de SVG com espaço É verificado. Portanto **o texto de exibição dentro dos SVGs (`<text>`, `<title>`) DEVE ter acentuação PT-BR completa** (SVG em string UTF-8 aceita acento). O `.sh` trava no Windows (replicar as regras em Python para validar local); o linter `ptbr_acentos_linter.py` tem lista de palavras DIFERENTE do `.sh` — validar contra os PATTERNS do `.sh`. Nunca acentuar identificador de código.
- **`stepIcons`** exige `Record<string, keyof typeof icons>` (de `courseIcons.tsx`), não `string`. `iconKey` do catálogo vem de outro dicionário (`src/app/educacao/page.tsx`). Labels de callout canônicos ficam em `CourseStepCard` (Conceito, Na prática, Regra de ouro, Analogia, Armadilhas comuns, Decisão...).
- **Catálogo:** obrigatório em `src/data/educacao-courses.ts` (com `iconKey`); `courses.ts` legado é opcional. IndexNow e sitemap derivam automático do catálogo + scan de `page.tsx`; `public/llms.txt` (+ `.well-known/`) é manual.
- **Densidade visual:** o padrão é o curso `frontends-com-vibecoding` (94 figuras SVG, 113 callouts). Não entregue paredão de texto. Figura = bloco `{type:"figure", value:<svg inline>, label}`, `role="img"` + `<title>`, cores por token + `#ffffff`. Ritmo: nunca mais que 2 blocos `text` seguidos sem um visual.

## Disciplina de Git (repos com escritor concorrente)

Os clones canônicos ficam sujos/trocando de branch (agentes concorrentes ao vivo). Regras:

1. **Nunca editar clone ocupado.** Trabalhe num `git worktree` isolado de `origin/master`. Ao final, remova-o (no Windows a pasta resiste por node_modules com path longo → PowerShell `Remove-Item -LiteralPath "\\?\<path>"`).
2. **Commit por path, nunca `git add -A`.** Reverta artefatos de prebuild antes de commitar (`crosslink-map.json`, `build-info.ts`, `next-env.d.ts`).
3. **`reset --hard` é bloqueado e force-push é proibido.** Se rebaseou um branch já pushado e o push foi rejeitado, use cherry-pick sobre o tip remoto (`git checkout -B tmp origin/<branch>; git cherry-pick <commit>; git push origin HEAD:<branch>`) — ou, melhor, não rebaseie: só empilhe commits novos (fast-forward) e deixe o merge do PR resolver o gap.
4. **Rode o build local antes do push** (o hook de pre-push do landing roda `next build`; o worktree precisa de `npm install` real — junction quebra o Turbopack).
5. **gh CLI atrás de proxy** (`127.0.0.1:8899`): limpe o proxy só para o gh (`HTTPS_PROXY= HTTP_PROXY= NO_PROXY='*' gh ...`); o `git push` funciona direto.
6. Merge via `gh pr merge --squash --delete-branch` (ambos os repos têm branch protection); cheque `mergeable`/checks verdes antes.

## FinOps

O `finops reset` do geo-orchestrator tem bug: `reset_daily()` zera o JSON snapshot mas NÃO o SQLite (`output/.finops/daily_spend.sqlite`, SoT desde o F23), e o `status` lê o SQLite. Reset de verdade: `UPDATE daily_spend SET amount=0 WHERE date=<hoje-UTC>` no sqlite. Fix de código pendente.
