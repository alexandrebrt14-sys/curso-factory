# Guia de escrita humanizada (ponteiro)

fonte: https://github.com/alexandrebrt14-sys/escrita-empreendedor
hash-fonte: 6547f0ee6548d56a177b09c61984235e01fb5bf6b48617672368443cfdc28623
sincronizado-em: 2026-09-27

O diagnóstico de ritmo, as técnicas de narrativa, a tabela de vícios de português gerado por
LLM, o orçamento de formatação, o fluxo de revisão em três passadas e a lista do que não fazer
vivem na fonte acima (`DIRETRIZ.md` e `PERFIL_DO_LEITOR.md`). Este arquivo não repete nenhum
número nem nenhuma lista. Quando algo aqui contradiz a fonte, a fonte vence.

## O que é específico deste repositório

- **Onde as regras viram máquina.** `src/validators/voice_guard.py` (nota de voz e clichê),
  `stylometry_checker.py` (variância de comprimento de frase) e `content_checker.py` (tetos da
  aula) são a implementação; as listas e os números vêm de `config/lexicos.json`, espelho gerado
  da fonte. Nenhum dos três é a régua: os três a aplicam.
- **Validador mede forma, nunca substância.** Texto limpo de clichê, com acentuação perfeita e
  ritmo variado pode não ter tese nenhuma. O piso de substância é conferido por leitura humana
  antes do gate, não depois.
- **Pesquisa de base.** O estado da arte de humanização e detecção em 2026, com a bibliografia
  datada que sustenta cada afirmação, está em `docs/research/HUMANIZACAO_AI_ESTADO_DA_ARTE_2026.md`.
- **Lacuna declarada.** Não existe, até julho de 2026, estudo de corpus acadêmico sobre
  marcadores de LLM específicos do português brasileiro. Quando aparecer, a fonte é que deve ser
  revisada contra ele, não este ponteiro.

## Compatibilidade editorial de 10/09/2026

Fonte consultada e incorporada no commit `2479179e199f768c4e96aebbadfa5d864523b34e`, versão 1.7.1.
A aplicação de SEO e GEO às etapas de pesquisa, escrita, revisão e humanização está em
`docs/ESCRITA_SEO_GEO.md`. A fonte §10 rege a fidelidade; os prompts da raiz e de `pt-br/`
executam essa orientação sem alterar o formato de retorno do pipeline.

## Compatibilidade editorial de 27/09/2026

Espelho regerado a partir do commit `12d1baec475d161ae3ffae2213bd894bd2a606f0`, versão 1.8.0.
Detalhe e cuidado com o nome do pacote em `DIRETRIZ_EDITORIAL.md`, "Como sincronizar".

## Como sincronizar

```
python -m escrita.sincronizar verificar GUIA_ESCRITA_HUMANIZADA.md
python -m escrita.cli lexicos --json > config/lexicos.json
```
