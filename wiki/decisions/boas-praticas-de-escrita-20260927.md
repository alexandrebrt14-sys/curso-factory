---
name: boas-praticas-de-escrita-20260927
description: "Aprendizados da produção do curso de super agentes pessoais viram configuração lida por código: vocabulário de uso limitado, aula que não narra a apuração, crosslinks por aula, peso visual declarado, tamanho e ordem do curso, tabela de proveniência, contradições com a fonte corrigidas e espelho do léxico na 1.8.0."
metadata:
  type: feedback
  created: 2026-09-27
---

Oito pedidos do dono e dos dados de uso do portal, registrados durante a produção do curso de
super agentes pessoais (27/09/2026), passaram a ser regra de máquina: configuração no YAML ou no
`client.yaml`, validador que lê o valor do arquivo, teste que prova a leitura e teste de
retrocompatibilidade (sem a configuração, o comportamento anterior fica igual).

| Regra | Configuração | Validador | Severidade |
|---|---|---|---|
| Palavras de uso exagerado ("travar", "canônico", "régua", "honesto" e variações), limite por aula | `quality_rules.yaml > validation.palavras_de_uso_exagerado` | `vocabulario_checker.py` | aviso no primeiro excesso, erro a partir de três |
| A aula não narra a própria apuração ("verificamos", "conferido em", "não foi possível confirmar") | `validation.apuracao_narrada` (estende o bastidor, não duplica a R9) | `content_checker._check_bastidor` | erro |
| Crosslinks por aula, opt-in por cliente, destino e capítulo conferidos contra o catálogo do portal | bloco `crosslinks` do `client.yaml`; forma em `validation.crosslinks` | `crosslink_checker.py` | piso, destino e âncora genérica: erro; teto e link na abertura: aviso; repetição em aulas seguidas e piso do curso: erro |
| Peso visual declarado pelo cliente ou pelo curso, sem mexer no espelho | bloco `visual` do `client.yaml` ou da entrada em `courses.yaml` | `peso_visual_aula.py` | piso: erro; teto, tipos e ritmo: aviso |
| Tamanho e ordem do curso pelos dados de uso | `validation.planejamento` | `planejamento_checker.py` | aviso |
| Tabela de proveniência como entrega de bastidor | `validation.proveniencia` | `proveniencia.py`, `cli.py proveniencia`, `etapas["proveniencia"]` | não reprova: é arquivo de trabalho |

As instruções dos prompts saem do mesmo YAML, pelos blocos `{bloco_vocabulario}`,
`{bloco_apuracao}`, `{bloco_crosslinks}`, `{bloco_peso_visual}` e `{bloco_ordem_do_curso}` em
`draft.md` e `review.md` (pt-br). Em inglês e espanhol, entra a regra geral, sem lista.
Nenhum número ou lista dessas regras mora no código do validador.

Contradições entre documentos (briefing do redator, seção 13): onde o erro estava no
curso-factory, vence a fonte `escrita-empreendedor`. Abertura direta, sem cena (C1); três H2 no
molde da aula (C2); rubrica GEO sobre o curso inteiro, sem cota por aula (C4); credencial com
vírgula (C8); chave de trilhas por curso marcada como descritiva (C11); aviso de aula longa sem
apoio visual, lido do espelho (C12); tabela de três colunas no celular (C13); glosa curta colada
ao termo (C16); rótulo "Armadilha comum:" deixa de ser obrigatório (C18).

O espelho `config/lexicos.json` foi regerado na 1.8.0 com o comando documentado. O pacote
`escrita-empresarial` instalado no ambiente também se chama `escrita` e esconde o da fonte; o
caminho sem instalar nada é apontar o `PYTHONPATH` para o clone (ver `DIRETRIZ_EDITORIAL.md`,
"Como sincronizar").

**Pendências para o dono decidir**

1. O bloco `didatica` da fonte 1.8.0 está no espelho e o `didatica_checker` ainda lê os números
   próprios do YAML (artigo definido em 50% e série de 3, contra 40% e 4 na fonte). Adotar os da
   fonte muda avisos em curso publicado.
2. Marcador `[FALTA EVIDÊNCIA]`: o prompt admite 3 por aula no rascunho, o gate reprova acima de
   5, e o publicado não aceita nenhum (R9). O curso de super agentes usou zero. Decidir se o
   rascunho do pipeline passa a zero para o cliente default.
3. Piso de 8 destinos distintos por curso no default: o número veio das orientações do curso de
   super agentes. Confirmar para todo curso do default.
4. Cadência de regeração do catálogo de crosslinks (hoje do commit `a0f834b4` da landing, de
   26/09): curso novo só vira destino depois de publicado e de o catálogo ser regerado.
5. Segunda rodada: `TECNICAS_ADICIONAIS.md` (Parte C, acréscimos ao léxico, que pertencem à
   fonte e não a este repositório) e `visual/GUIA_VISUAL.md` (legenda de 12 a 40 palavras,
   tabela que vira cartão no celular) chegaram durante esta rodada e não viraram regra aqui.

Relacionadas: [[didatica-explicar-em-vez-de-detalhar-20260922]],
[[abertura-direta-sem-distracao-20260908]], [[bastidor-fora-da-aula-20260903]].

---

## Linha do tempo (append-only, ordem reversa)

- **2026-09-27**: [criação] produção do curso de super agentes pessoais. Os dados do admin
  (curso curto termina, abandono em teoria cedo e em apêndice de instalação, rolagem abaixo da
  metade da página, 55% no celular) e os pedidos do dono (quatro palavras de uso limitado, aula
  que não narra a apuração, crosslinks em toda aula, cinco a sete peças por aula num curso,
  proveniência de cada número) viraram configuração, validador e teste. Contradições C1, C2,
  C4, C8, C11, C12, C13, C16 e C18 corrigidas no curso-factory; espelho do léxico na 1.8.0.
