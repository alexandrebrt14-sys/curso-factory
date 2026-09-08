# Bastidor fora da aula, lei como fato, forma livre (03/09/2026)

## Contexto

O dono leu aulas que explicavam a própria técnica, diziam que os dados tinham sido verificados e
fechavam com "consulte um advogado". A auditoria de 03/09/2026 achou três causas: o prompt de
redação proibia meta-discurso, mas nenhum código conferia (as famílias `bastidorDeVerificacao`
e `rotuloDeConfianca` estavam no espelho da fonte e nunca eram lidas); o prompt de pesquisa
carimba cada dado com [Alta]/[Média]/[Baixa] e nada impedia o rótulo de chegar à aula; e o
relatório do revisor só era separado da aula pelo marcador "REVISÃO CONCLUÍDA" em português,
que os prompts em inglês e espanhol mantinham por acaso.

## Decisão

1. O checker ganha cinco verificações: bastidor (erro, famílias da fonte mais regex de
   autorreferência; menção entre aspas fica livre), rótulo de pesquisa vazado (erro),
   comentário HTML fora do marcador de módulo (erro), relatório de revisão dentro da aula
   (erro, três idiomas) e muleta legal (aviso, com o conserto).
2. O separador do relatório aceita "REVIEW COMPLETE" e "REVISIÓN CONCLUIDA"; os prompts em
   inglês e espanhol usam o marcador do próprio idioma.
3. `disclosure` desligado no cliente padrão: aviso de IA e de lei não entra por regra geral;
   liga-se por cliente quando o contrato exigir. `min_quotations` cai a zero: cobrar uma citação
   literal por curso convidava a inventar a frase.
4. Forma livre nos três idiomas: analogia sem teto de uma, exercício com o tamanho que o aluno
   precisa em vez de cota, seção "Liberdade de forma" no prompt de redação.

## O que não mudou

Abertura sem cena nem personagem (é o vetor mais direto de invenção), travessão, emoji e
vírgula de Oxford continuam fora por decisão do dono.

## Passada de expansão (depois do teste real)

O teste real com as regras acima aprovou 7 de 8 unidades, sem bastidor e sem aviso legal. A
reprovação restante foi extensão: a aula 1.5 veio com 641 palavras e cinco de seis ficaram
abaixo do alvo. O redator (claude-sonnet-5, por fallback) encurta mesmo com os números no
prompt. Decisão: uma passada de expansão quando a aula volta abaixo do piso, com o rascunho e
os números na mão, e a segunda versão só fica se cresceu. Custa uma chamada por aula curta
(cerca de US$ 0,08) e é mais barato que reprovar o curso inteiro no fim.
