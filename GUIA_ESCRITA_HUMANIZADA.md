# Guia de escrita humanizada (ponteiro)

fonte: https://github.com/alexandrebrt14-sys/escrita-empreendedor
hash-fonte: 999d02ddc87cfa2897cb0fafda4f6b5fdd170103fddd74c14c7750f96f91beae
sincronizado-em: 2026-09-10

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

## Como sincronizar

```
python -m escrita.sincronizar verificar GUIA_ESCRITA_HUMANIZADA.md
python -m escrita.cli lexicos --json > config/lexicos.json
```
