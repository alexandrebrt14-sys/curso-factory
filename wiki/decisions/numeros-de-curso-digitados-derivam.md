---
name: numeros-de-curso-digitados-derivam
description: "Contagem de módulos e duração digitadas à mão derivam entre 5 superfícies e quebram a barra de progresso; derivar de STEPS e gatear com teste provado por injeção"
metadata:
  type: mistake
  created: 2026-07-25
---

Todo número que descreve um curso é **derivado, nunca digitado**:
`numberOfCredits` = `STEPS.length`; duração declarada = soma real dos campos
`duration` dos Steps. Hero, FAQ, JSON-LD (`timeRequired`/`courseWorkload`/
`totalTime`) e catálogo alinham-se à soma. Quando a contagem vive em múltiplas
superfícies (no portal /educacao são cinco), um teste compara todas contra o
canônico — e um gate novo só existe depois de provar que morde: injetar a
regressão exata, ver a reprovação com mensagem acionável, restaurar, ver passar.

Corolário de verificação: relatório de terceiro (agente ou índice gerado) não
se aceita sem conferência independente contra o que a produção serve. Das 8
divergências que um índice apontava, só 2 eram reais; corrigir as 8 teria
introduzido 5 defeitos.

Relacionadas: [[involucro-copiado-de-curso-irmao]], [[arquivo-de-conteudo-sem-consumidor]].

---

## Linha do tempo (append-only, ordem reversa)

- **2026-07-25** — [criação] Auditoria do portal /educacao achou 47 contagens
  divergentes em 4 catálogos secundários (`claude-code` como 10 módulos tendo
  20; `seo-geo` como 12 tendo 25). As superfícies dividem o progresso salvo do
  aluno pelo total declarado: contagem menor marcava curso como concluído na
  metade. Sete cursos declaravam durações contraditórias — até três números na
  mesma página (`geo-saude`: 280, 290 e 295 min). O teste
  `course-catalogs-sync.test.ts` só comparava slugs, por isso nada quebrava o
  build; passou a comparar contagens e foi validado por injeção de regressão.
