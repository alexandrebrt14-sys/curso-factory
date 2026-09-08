# Playbook de Correção GEO em Massa no WordPress 2026 — boa prática canônica

> **Documento canônico operacional.** Registra o método validado na campanha de correção GEO em massa nos cerca de 280 posts do blog WordPress `blog.brasilgeo.ai`, executada em **29/06/2026**, aplicando a rubrica de citabilidade GEO 2026 diretamente no conteúdo ao vivo via WordPress REST.
>
> **Versão:** 1.0 · 2026-06-29 · Owner: Brasil GEO (Alexandre Caramaschi)
>
> **Para que serve:** transformar a rubrica de redação GEO (ver `GEO_REDACAO_CHECKLIST_2026.md`) em um procedimento seguro de correção em escala sobre conteúdo público já publicado, sem destruir estrutura, sem fabricar dados e sem duplicar inserções ao re-rodar.
>
> **Como usar:** este é o material de referência para qualquer agente ou pessoa que precise editar em massa o conteúdo ao vivo de um WordPress (ou superfície pública equivalente). Complementa, não substitui, a rubrica de redação e a governança de publicação no WordPress.

---

## 1. Contexto

A campanha aplicou os sinais da rubrica de citabilidade GEO 2026 diretamente no conteúdo ao vivo dos posts do blog `blog.brasilgeo.ai`, via WordPress REST. O objetivo foi elevar a citabilidade do conteúdo já publicado (normalização da grafia da marca, grounding de entidade, FAQPage e cross-links) sem reescrever os posts e sem qualquer risco de corromper a estrutura de blocos do Gutenberg.

O resultado da campanha está consolidado na seção 8.

---

## 2. Método inviolável de edição em massa de conteúdo público

As sete regras abaixo são obrigatórias e não admitem exceção. Qualquer edição em massa de conteúdo público deve segui-las na ordem.

1. **Backup completo antes de gravar.** Baixe e salve o `content.raw` de cada post (via `context=edit`) ANTES de qualquer gravação. Isso garante rollback completo.
2. **Dry-run com amostras ANTES e DEPOIS.** Antes de qualquer `--apply`, gere uma amostra mostrando o estado ANTES e o estado DEPOIS da transformação, e revise manualmente.
3. **Idempotência por marcador de classe.** Toda inserção deve carregar um marcador de classe (por exemplo `class="brasilgeo-entity-grounding"`). Antes de inserir, verifique a presença do marcador. Re-rodar a campanha nunca pode duplicar a inserção.
4. **Substituição textual, nunca estrutural.** Transforme apenas os segmentos de TEXTO entre tags. Nunca altere o conteúdo de tags, atributos `href`/`src`/`class`, comentários de bloco do Gutenberg, nem slugs dentro de URLs.
5. **Escrita serializada, um post por vez.** Grave de forma sequencial, com retry e backoff. Nunca rode múltiplos processos gravando em paralelo: o WAF do WordPress responde com 403 ou 500 sob escrita concorrente.
6. **Verificação ao vivo pós-gravação.** Após cada gravação, re-baixe o post e confira o resultado, e re-audite o sinal corrigido.
7. **Re-baixar antes de cada nova wave.** Antes de iniciar uma nova wave de correção, re-baixe o conteúdo atual. Nunca reutilize um backup antigo como base de uma nova transformação.

---

## 3. A lib de diagnóstico como fonte única da verdade

A campanha reusou exatamente as MESMAS funções puras que o painel `/admin/blog-geo` usa para diagnosticar o conteúdo:

- `checkEntityConsistency`
- `extractFaqFromContent` e `buildFaqPageJsonLd`
- `suggestCrosslinks`

Ao consumir o mesmo código do diagnóstico, a correção aplica EXATAMENTE aquilo que o painel aponta. Não há divergência (drift) entre o que o painel mostra e o que a execução faz.

**Lição canônica:** o gerador de correção deve consumir o mesmo código do diagnóstico. Diagnóstico e correção que evoluem em bases separadas inevitavelmente divergem, e a correção passa a "consertar" coisas que o painel não aponta (ou a ignorar o que ele aponta).

---

## 4. Princípio anti-fabricação (reforço)

NUNCA fabricar pergunta, resposta, estatística ou fonte.

- O FAQPage JSON-LD deve usar perguntas e respostas LITERAIS já presentes no post. Nada de inventar uma pergunta plausível ou redigir uma resposta nova.
- Estatística só entra com fonte real. Sem fonte verificável, não inserir número algum.

Este princípio é absoluto: a citabilidade GEO depende de o conteúdo ser verificável. Fabricar dados destrói a confiança que a campanha pretende construir.

---

## 5. Grounding de entidade (E-E-A-T / Knowledge Graph)

A wave de grounding insere um bloco idempotente que ancora a entidade do autor e da marca para os detectores que leem o corpo do conteúdo. O bloco contém:

- **Credencial canônica do autor PERTO da menção da marca**, dentro do corpo do post. O author box do tema NÃO conta, porque os detectores que leem o conteúdo não enxergam o box do tema; a credencial precisa estar na prosa.
- **Links canônicos visíveis** como `<a href>`: LinkedIn, Wikidata, ORCID, DOI/SSRN.
- **JSON-LD `sameAs`** com `Organization` e `Person`.
- **Triplas semânticas** com a entidade como sujeito.

Todo o bloco carrega o marcador de classe de idempotência (ver regra 3), para que re-rodar a wave nunca duplique o grounding.

---

## 6. Gotchas técnicos (WordPress REST e tooling)

- **User-Agent de navegador é OBRIGATÓRIO no REST.** O WAF responde 403 a User-Agent de `urllib`, `node` ou similar. Use um User-Agent de navegador real.
- **HTTP 500 ocasional em POST é transitório.** Retry com backoff resolve.
- **O REST rejeita Basic Auth com a SENHA DE LOGIN.** Só aceita Application Password.
- **`content.raw` só vem com `context=edit`.** Os blocos do Gutenberg em forma bruta exigem requisição autenticada com `context=edit`. Sem autenticação, o REST devolve apenas `content.rendered`.
- **A variante de marca em forma de slug casa dentro de URLs.** Por exemplo, `brasil-geo` aparece dentro de URLs e slugs. A substituição precisa de uma guarda para atuar apenas na prosa, nunca em `href`/`src`/slug.
- **Em-dash é proibido em copy.** Use vírgula ou dois-pontos no lugar.
- **`llms.txt` na raiz do WordPress NÃO é gravável via REST.** Gravar arquivo na raiz exige acesso a arquivo ou plugin dedicado. Entregue o `llms.txt` para upload manual.

---

## 7. Sequência operacional recomendada (resumo acionável)

1. Autentique no REST com Application Password e User-Agent de navegador.
2. Baixe `content.raw` de todos os posts (`context=edit`) e salve o backup.
3. Rode o diagnóstico reusando as funções puras do painel `/admin/blog-geo`.
4. Para cada wave, gere o dry-run ANTES e DEPOIS e revise as amostras.
5. Aplique a wave de forma serializada (um post por vez), com retry e backoff, respeitando os marcadores de idempotência.
6. Após cada gravação, re-baixe o post, confira a inserção e re-audite o sinal.
7. Antes de iniciar a próxima wave, re-baixe o conteúdo atual (não reutilize backup antigo).
8. Entregue o `llms.txt` para upload manual (não gravável via REST).

---

## 8. Resultado (29/06/2026)

| Wave | Sinal corrigido | Posts afetados |
|---|---|---|
| 1 | Grafia da marca normalizada (`BrasilGEO` para `Brasil GEO`) | 39 posts |
| 2 | Bloco de grounding de entidade inserido | 231 posts |
| 3 | FAQPage JSON-LD derivado de perguntas literais | 47 posts |
| 4 | Cross-links blog para site | 267 posts |

**Sinais de entidade do painel:** de 255 avisos para 0.
