---
name: arquivo-de-conteudo-sem-consumidor
description: "Arquivo de módulo/dados commitado sem o import que o consome compila limpo e vira conteúdo morto ou âncora falsa no índice de busca"
metadata:
  type: mistake
  created: 2026-07-25
---

**O import no `page.tsx` faz parte da mesma entrega que cria o arquivo de
conteúdo.** Export não usado compila limpo, então nenhum gate percebe o arquivo
órfão. Antes de dar a entrega por concluída: `grep` pelo nome do arquivo novo
fora dele mesmo — zero ocorrências é defeito, não detalhe.

Agrava o problema o fato de geradores de índice varrerem `modulos/*.ts` sem
verificar se a página importa: módulo órfão vira âncora morta no índice de
busca, apontando para aula que não renderiza. Ao substituir módulos numa
reforma, a remoção dos arquivos antigos precisa ser explícita no commit — a
árvore do merge preserva os dois conjuntos em silêncio.

Relacionadas: [[integracao-conflitos-tem-dono]], [[numeros-de-curso-digitados-derivam]].

---

## Linha do tempo (append-only, ordem reversa)

- **2026-07-25** — [criação] Duas ocorrências no mesmo dia durante a recuperação
  pós-queda do portal /educacao: `comece-por-aqui.ts` (299 linhas, a rampa de
  entrada de gestao-projetos-geo) e `concept-map.ts` (44KB, o mapa conceitual de
  letramento-ia-executivos) chegaram ao master sem que nada os importasse. No
  segundo caso, as 194 linhas que renderizavam o mapa estavam não commitadas
  numa worktree prestes a ser removida — inspecionar `git status` de toda
  worktree antes de removê-la foi o que salvou o trabalho.
