---
name: abertura-checker
type: entity
category: validator
status: stable
created: 2026-09-08
updated: 2026-09-08
related:
  - abertura-direta-sem-distracao
  - content-checker
  - quality-gate-5-camadas
  - abertura-direta-sem-distracao-20260908
---

# abertura_checker.py (abertura direta e sem distração, R1 a R9)

Validator em `src/validators/abertura_checker.py`, criado em 08/09/2026. Cobra o conceito
[[abertura-direta-sem-distracao]] em duas superfícies e é a única camada do gate que também
morde a **publicação**: `TsxGenerator.render_page` chama `check_abertura_definicao` antes de
renderizar e levanta `AberturaError` quando há bloco proibido. Não há modo legado.

## Duas entradas

| Função | Entrada | Onde é chamada | Saída |
|---|---|---|---|
| `check_abertura(texto, unidade="aula" \| "trilha")` | Markdown de uma unidade | `content_checker.check_content` (item 15), e por ele `QualityGate.check_text`, `Orchestrator._quality_gate` e `python cli.py validate`; `QualityGate._check_content_por_unidade` chama direto para a trilha | `ResultadoAbertura.achados`: `AchadoAbertura(regra, mensagem, tipo="error")` |
| `check_abertura_definicao(course)` | `CourseDefinition` montado | `TsxGenerator.render_page` | lista de mensagens; vazia é aprovado |

No [[content-checker]] os achados saem na categoria `abertura`, tipo `error`, com a mensagem
prefixada pelo código da regra: `[R6] Exercício 'faça agora' ou variante (...)`.

## O que cada regra mede

| Código | Onde olha | Como |
|---|---|---|
| `R1` (`_check_r1`) | só unidade com H1 que não seja `# Trilha` | primeiro bloco após o H1 = subtítulo (prosa, 1 linha, 1 frase, até 30 palavras); segundo bloco = parágrafo liso; nada de `#`, `-`, `|`, `>`, `!`, `<`, número+ponto |
| `R3` (`_check_r3`) | cabeçalhos, rótulos em negrito no início da linha, blockquotes rotulados | regex "escolha seu caminho", "se você é ... vá para", "comece por aqui", "para quem é" |
| `R5` (`_check_r5`) | `mockup`/`maquete`/"aplique|simule|monte|faça ... no seu negócio" em qualquer linha; "no seu negócio" só em cabeçalho ou rótulo | prosa pode falar do negócio do leitor |
| `R6` (`_check_r6`) | cabeçalhos, rótulos, blockquotes rotulados | "faça agora", "exercício", "mão na massa", "sua vez", "pratique", "tarefa", "desafio", "checklist de ação", "atividade prática", "resultado esperado", "se travar" (e as formas em inglês e espanhol) |
| `R7` (`_check_r7_aula`) | aula | linha "Fonte:"/`**Fonte:**` ou cabeçalho "Fontes/Referências/Sources/Fuentes" |
| `R7` (`_check_r7_trilha`) | trilha | "Fontes" é o último H2 e único; cada linha até 25 palavras; sem `>` nem `|` |
| `R8` (`_check_r8`) | cabeçalhos, rótulos, blockquotes rotulados | "checkpoint", "ponto de verificação", "recapitulando", "resumo do capítulo", "você aprendeu", "o que você vai aprender", "quiz" |
| `R9` (`_check_r9`) | qualquer linha, mesmo entre aspas | "requer verificação", "a verificar", "[verificar]", "dado não confirmado", "fonte pendente", "LGPD", "Lei Geral de Proteção de Dados", "13.709" |
| definição | cada step e seção | `description` obrigatória; primeira seção é `text`; nenhuma seção `checkpoint`; nenhum `[FALTA EVIDÊNCIA:`/`[PREENCHER-HUMANO:`; nenhuma linha "Fonte:" em prosa; R3, R5, R6, R8 e R9 sobre `value`, `label` e os textos do `data`; `course.fontes` com até 25 palavras por linha |

Blocos de código são mascarados em todas as regras. Menção entre aspas (`"faça agora"`) é
liberada em R5, R6 e R8 (`_sem_mencoes`); em R9 vale mesmo entre aspas, porque o pedido é
não mencionar. R2 e R4 não têm regex: são cobradas no template por
`tests/test_abertura_sem_distracao.py`.

## Como rodar

```
python cli.py validate output/drafts/          # Markdown, categoria [abertura]
python cli.py create "Nome do curso"           # gate ao fim do pipeline, em etapas.gate_report
```

Saída com erro (capturada em 08/09/2026):

```
FAIL output/drafts/ruim.md
     - Conteúdo [abertura]: [R1] O primeiro bloco depois do H1 precisa ser o subtítulo em uma frase, em linha própria; veio: '## Faça agora'. ...
     - Conteúdo [abertura]: [R7] Fonte no meio da aula: 'Fonte: IBGE 2025.'. A fonte vai para o bloco 'Fontes' do rodapé da trilha, em uma linha curta.
     - Conteúdo [abertura]: [R6] Exercício 'faça agora' ou variante (conteúdo é leitura, não workbook): 'Faça agora'.
     - Conteúdo [abertura]: [R8] Card 'checkpoint' ou variante: 'CHECKPOINT'.
     - Conteúdo [abertura]: [R9] Marcador de verificação ou menção à LGPD visível ao leitor (verificação é bastidor): 'LGPD'.
```

Aprovado: `OK output/drafts/bom.md`, sem linha `[abertura]`. No cliente `default` a camada
GEO também roda sobre o arquivo isolado e pode acusar Cite Sources; é outra camada.

Na publicação:

```python
from src.validators.abertura_checker import AberturaError
try:
    TsxGenerator().render_page(course)
except AberturaError as e:
    print(e)  # "Abertura e distração reprovadas em N ponto(s) (R1 a R9): - modulo-um[2]: [R9] ..."
```

## Como estender os léxicos

Padrões padrão em `_PADROES_PADRAO` (chaves `R3`, `R5_qualquer`, `R5_rotulo`, `R6`, `R8`,
`R9`). A configuração **acrescenta** em `config/quality_rules.yaml`:

```yaml
validation:
  abertura:
    enabled: true
    termos:
      R6: ["mãos à obra", "re:\\bdin[aâ]mica\\s+de\\s+grupo\\b"]
      R9: ["dado a confirmar"]
```

Item é literal (escapado pelo código); prefixo `re:` passa regex. Cuidados: termo em `R3`,
`R5_rotulo`, `R6` e `R8` só reprova cabeçalho/rótulo; em `R5_qualquer` e `R9` reprova
qualquer linha, então teste contra um curso aprovado antes. A doutrina que explica R9
precisa citar a sigla da lei de dados; se algum documento de doutrina vier a passar pelo
gate, escreva a sigla em código inline ou mascarada, porque o checador mascara só bloco de
código. Desligar tudo: `enabled: false` (não recomendado; o dono pediu a regra).

## Testes

`tests/test_abertura_sem_distracao.py` (58 casos): as nove regras no Markdown, no
`CourseDefinition` e no TSX gerado. Testes antigos invertidos por esta decisão estão listados
em [[abertura-direta-sem-distracao]].

## Cross-references

- Conceito: [[abertura-direta-sem-distracao]]. Decisão: [[abertura-direta-sem-distracao-20260908]].
- Convive com [[content-checker]] (mesma categoria de relatório) dentro do [[quality-gate-5-camadas]].
- Página humana: https://github.com/alexandrebrt14-sys/curso-factory/wiki/Abertura-direta-e-sem-distracao-R1-R9
