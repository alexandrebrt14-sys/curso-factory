---
name: acentuacao-ferramentas-e-armadilhas
description: "perl -i grava mojibake invisível aos gates; lista fixa de palavras corrige pela metade; corretor automático cria o defeito inverso até em nome de variável"
metadata:
  type: mistake
  created: 2026-07-25
---

Três armadilhas de ferramenta ao corrigir acentuação em massa:

1. **`perl -i` no Git Bash do Windows grava mojibake** (`memÃ³ria`) que nenhum
   gate detecta — tsc compila, lint aceita, e o guard de acentuação procura
   palavra SEM acento, então o texto corrompido passa como corrigido. Usar Node
   com `"utf8"` explícito e validar `/Ã[a-z]/` = 0 antes de commitar.
2. **Lista fixa de palavras corrige pela metade**: uma passada que "corrigiu"
   38 ocorrências deixou 60 no mesmo arquivo. Corrigir lendo a frase, com
   varredura autocalibrada — o dicionário das palavras que o próprio corpus
   escreve com acento denuncia as sem acento.
3. **Corretor automático cria o defeito inverso**: acentos indevidos ("quasé",
   "éxige"), conjunção "e" trocada pelo verbo "é" — e, no pior caso, um nome de
   variável acentuado (`preço`) num exemplo que declarava `preco`, quebrando o
   código que o aluno executa. Revisar nos dois sentidos.

O teste do que precisa de acento é "um humano lê isto?", não o rótulo do bloco:
blocos `prompt`, blocos `code` com `language: "text"`/`"markdown"` que o aluno
cola num assistente, copy visível de slide e modelos de e-mail são leitura
humana. Homógrafos exigem contexto, não regex: "media" pode ser imperfeito de
medir, "analise" imperativo, "marco" milestone ou março.

Relacionadas: [[involucro-copiado-de-curso-irmao]], [[integracao-conflitos-tem-dono]].

---

## Linha do tempo (append-only, ordem reversa)

- **2026-07-25** — [criação] Ciclo de correção de +740 defeitos de acentuação
  em 12 cursos do portal /educacao. O curso de Python tinha corrupção de mão
  dupla (acentos faltando E sobrando) e um `NameError` publicado — a aula
  declarava `preco` e imprimia `preço * 2`. O caso mais enganoso da rodada:
  "O resultado media ~9 telas" parecia erro e era o imperfeito de medir;
  acentuar teria criado um erro onde não havia.
