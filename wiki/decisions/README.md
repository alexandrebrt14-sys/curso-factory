# Memória de decisões — curso-factory

Camada de memória persistente para o Claude Code, derivada do setup de "Memória
Persistente para LLM": **os arquivos `.md` versionados são a fonte da verdade**; o
índice é o que entra no contexto. Aqui moram decisões de arquitetura, erros-a-evitar
e insights técnicos do projeto — um arquivo por decisão, auditável via `git diff`.

Este diretório já abrigava os ADRs do projeto ([`ADR-001`](ADR-001-adopcao-llm-wiki.md),
[`ADR-002`](ADR-002-sync-automatico-courses-wiki.md)); a camada abaixo apenas padroniza
o formato e adiciona um índice navegável. Não substitui o `CLAUDE.md` (regras vivas).

## Como funciona

- **Fonte da verdade = arquivos.** Cada decisão (ou ADR) é um `.md` neste diretório.
- **Índice enxuto.** [`INDEX.md`](INDEX.md) lista 1 linha por decisão (< ~200 caracteres).
  O detalhe mora no arquivo, nunca no índice — linha longa incha o contexto.
- **Formato de página** ([`_TEMPLATE.md`](_TEMPLATE.md)): **Verdade Compilada**
  (topo, reescrito quando o entendimento muda) + **Linha do Tempo** (append-only,
  nunca editada). O topo responde "o que vale AGORA?"; a linha do tempo, "como
  chegamos aqui?". Os ADRs existentes seguem seu próprio formato — ambos convivem.

## Tipos (frontmatter `type:`)

- `decision` — escolha de arquitetura ou processo (decai devagar)
- `mistake` — erro-a-evitar, com o sintoma e a correção (retido por mais tempo)
- `insight` — descoberta técnica reaproveitável
- `feedback` — preferência declarada pelo dono (não decai)

## Três disciplinas (não pule nenhuma)

1. **Dedup antes de gravar** — busque no `INDEX.md`/pasta; se já existe, ATUALIZE a
   página (reescreva a Verdade Compilada, adicione 1 item na Linha do Tempo), não
   crie outra. Senão o corpus vira duplicatas.
2. **Cross-link na escrita** — toda decisão nova linka 2-3 relacionadas via
   `[[nome-do-arquivo-sem-extensao]]`. Senão o conhecimento fica em ilhas.
3. **Candidate-gate** — a captura automática (hook de fim de sessão) grava
   rascunhos em `candidates/` (NÃO versionado, NÃO autoritativo). Promover =
   destilar o aprendizado numa decisão real aqui e apagar o rascunho. Senão o
   ruído de captura polui tudo (o modo de falha número 1 de sistemas auto-capturadores).

## Manutenção (poda)

Revise periodicamente: uma decisão obsoleta vai para `archive/` (não some — vira
Linha do Tempo) com link para a sucessora. `mistake` e `feedback` raramente expiram;
uma `decision` superada por outra é arquivada apontando para a nova.

> Conceito e fluxo completos: `Setup-de-Memoria-Claude-Code.pdf` (máquina do dono,
> em `C:/Sandyboxclaude/Melhorias/`).
