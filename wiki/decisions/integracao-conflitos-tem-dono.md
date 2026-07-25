---
name: integracao-conflitos-tem-dono
description: "Conflito de catálogo se resolve linha a linha pelo autor da mudança; gerados se regeneram; worktree se inspeciona antes de remover; stash vira patch antes de limpar"
metadata:
  type: insight
  created: 2026-07-25
---

Quatro regras de integração quando múltiplas frentes tocam os mesmos arquivos:

1. **Conflito de catálogo tem dono por linha.** Resolver por bloco
   (`--ours`/`--theirs` no arquivo inteiro) regride trabalho alheio: um PR que
   nunca tocou um curso pode carregar a versão velha da linha vizinha. Resolver
   linha a linha, atribuindo cada uma a quem a reformou.
2. **Arquivos `.generated.ts` nunca se resolvem à mão**: tomar qualquer lado,
   regenerar com o script gerador em árvore limpa, commitar o resultado.
3. **Worktree se inspeciona antes de remover** (`git status` nela) — trabalho
   não commitado morre em silêncio junto com a worktree.
4. **Stash vira patch antes de `stash clear`** (`git stash show -p > backup.patch`)
   — a limpeza fica reversível. Medir obsolescência antes de decidir: se 100%
   dos arquivos do stash mudaram no master desde então, ele está morto.

Integração com sessões concorrentes no mesmo repositório pede worktree
separada; o working tree do master pertence a quem o estiver usando.

Relacionadas: [[arquivo-de-conteudo-sem-consumidor]], [[numeros-de-curso-digitados-derivam]].

---

## Linha do tempo (append-only, ordem reversa)

- **2026-07-25** — [criação] Integração de 3 PRs + 5 worktrees no portal
  /educacao. O merge do PR do curso de Deploy parecia conflito editorial e era
  vizinhança de linha: resolvê-lo em bloco teria regredido `llm-finops` de 24
  para 10 módulos em cinco arquivos de uma vez, sem nenhum gate acusar. Uma
  worktree prestes a ser removida guardava 194 linhas não commitadas. Os 4
  stashes antigos (100% dos 51 arquivos já alterados no master) foram
  exportados como patch para `_ops-logs/` antes do `stash clear`.
