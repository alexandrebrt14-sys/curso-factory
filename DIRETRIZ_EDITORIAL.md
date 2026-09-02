# Diretriz editorial deste repositório (ponteiro)

fonte: https://github.com/alexandrebrt14-sys/escrita-empreendedor
hash-fonte: 9faa6cb2c17eb3c7992b93da718a2e0ef8b7173f4279202a22d83338b7528f40
sincronizado-em: 2026-09-02

A régua de escrita, os moldes de página, a tabela de tetos, o perfil do leitor e o glossário
vivem na fonte acima. Este arquivo não repete nenhum número nem nenhuma lista. Quando algo aqui
contradiz a fonte, a fonte vence e este arquivo é corrigido.

A unidade de medida do curso-factory é a **aula** (tipo D da fonte). O que era diretriz própria
deste repositório — piso de palavras por módulo, pisos de exercício, tabela, blockquote,
estatística e fonte, cota de palavras por parte, orçamento de formatação, fluxo de revisão em
três passadas, vícios de português, estruturas proibidas — passou a viver na fonte, em
`DIRETRIZ.md`, `MOLDES_DE_PAGINA.md` (seções 2, 3-D e 6) e `PERFIL_DO_LEITOR.md`.

## O que é específico deste repositório

- **Motor de cursos.** O vocabulário de peças visuais que o gerador sabe emitir (`figure`,
  `dataTable`, `comparison`, `matrix`, `statGrid`, `timeline`, `flow`, `checklist`, `glossary`,
  `accordion`, `template`, `useCase`, `tabs`, `slides`, `tipCard`, `stepGuide`, `codeDownload`),
  o payload de cada uma e as armadilhas do renderizador estão em `docs/DOUTRINA_VISUAL_CURSOS.md`.
  `code`, `prompt` e `sourceNote` são aparato, não respiro, e não contam como peça visual.
- **Teto de parágrafo em caracteres, no motor.** A fonte mede parágrafo em palavras (a faixa
  da aula está em `tetos.D.paragrafo` do espelho). O motor de cursos mede também em caracteres
  (1.200), porque o bloco de prosa da landing rola dentro de si mesmo num celular de 390 pontos.
  Os dois valem: o de palavras é editorial, o de caracteres é de renderização. Parâmetros em
  `config/quality_rules.yaml > validation.visual_density`.
- **Unidade de geração.** Desde 02/09/2026 o pipeline escreve, analisa, classifica e revisa uma
  AULA por chamada, com a pesquisa inteira, e cada etapa recebe o rascunho (não a saída da
  anterior). Os tetos da aula entram no prompt de redação como variáveis lidas do espelho.
  Registro em `wiki/decisions/geracao-por-aula-e-insumo-correto.md`.
- **Acervo publicado entra por linha de base congelada.** A dívida de cada curso existente fica
  registrada e só pode diminuir; a régua nova é obrigatória e integral só para curso novo.
- **Configuração que ninguém lê não protege nada.** Antes de confiar num gate, verifique se o
  código realmente carrega o arquivo de regras. Foi o defeito de 11/08/2026, quando o YAML tinha
  56 clichês e o gate rodava com 18 em código.

## Como sincronizar

```
python -m escrita.sincronizar verificar DIRETRIZ_EDITORIAL.md   # reprova se o hash divergir
python -m escrita.cli lexicos --json > config/lexicos.json      # espelho lido pelos validadores
```

`config/lexicos.json` é gerado, nunca editado à mão. É dele que
`src/validators/content_checker.py` tira os tetos da aula e as listas de expressão vetada.
