# Publicação de conteúdo e mídia

Atualizado em 08/10/2026. A fábrica gera artefatos locais; a publicação exige integração
e validação no repositório consumidor. O nome `output/deployed/` é uma convenção local:
`MetadataSync` deduz o status pela existência da pasta, sem consultar produção.

## Autoria, intermediários e consumidor

| Etapa | Fonte implementada | Destino e limite |
|---|---|---|
| Autoria | `config/courses.yaml`, configuração do cliente, prompts e templates | Versionados neste produtor. |
| Geração | `src/orchestrator.py`, `ClientContext.output_dir` | Rascunhos, checkpoints e resultados em `<output_dir>/drafts/`; não são páginas publicadas. |
| Conversão | `cli.py`, `src/converters/draft_to_course.py`, `src/generators/tsx_generator.py` | `page.tsx`, `layout.tsx` e `REVISAO_HUMANA.md` no destino escolhido; revisão antes de copiar o TSX. |
| Catálogo local | `src/generators/metadata_sync.py` | `output/course_catalog.json`; emissão e status não comprovam consumidor nem deploy. |
| Crosslinks | `scripts/gerar_catalogo_crosslinks.py` | Lê o catálogo da landing e grava `config/clients/default/crosslinks_catalogo.json`; não publica o catálogo da fábrica. |
| Integração | `LANDING_PAGE_DIR`, `EDUCACAO_DIR` em `src/config.py` | Identificam o consumidor esperado; em worktree, configure a raiz explicitamente. |

Não foi encontrado nesta inspeção um consumidor automático do `course_catalog.json`
da fábrica na landing. O endpoint `/api/educacao/catalog` do portal expõe seu próprio
catálogo para leitura externa; sua existência não demonstra a integração inversa.

`output/` e `.cache/` são ignorados pelo Git, mas precisam de retenção e backup conforme
o valor dos insumos. Não copie a árvore inteira para `public/` nem para `src/generated`
do consumidor. Esses gerados pertencem ao prebuild do portal.

## Proteção implementada e limites

`src/output_paths.py` protege os destinos intermediários usados pelo `Orchestrator`
(rascunhos/checkpoints) e pelo `MetadataSync` (catálogo), antes da escrita. A identidade
requer, na raiz configurada por `LANDING_PAGE_DIR`, três evidências: `package.json` com
`name: alexandrecaramaschi-com`, `next.config.ts` e a pasta `src/app/educacao`.
Os caminhos são resolvidos antes de comparar com `public/` e `src/generated`, incluindo
seus descendentes. O orquestrador recusa o destino antes de inicializar o cliente LLM;
o emissor de catálogo devolve `ok: false` com o motivo.

A proteção não se aplica quando a configuração ou os marcadores não identificam esse
portal. Ela não bloqueia genericamente uma pasta `public` de outro projeto e não cobre
cópias manuais, scripts legados, certificados ou exportações `llms.txt`. O fluxo de
conversão e o destino TSX autorizado permanecem disponíveis. Não se trata de isolamento
de segurança do sistema de arquivos.

## Exemplo de entrega revisada

Execute no clone ou worktree da fábrica, com dependências instaladas:

```powershell
$env:LANDING_PAGE_DIR = 'C:/Sandyboxclaude/_wt/landing-conteudo'
python cli.py drafts-to-tsx --input ./output/drafts --output ./output/converted_from_drafts
python cli.py emit-catalog --output-dir ./output
```

Revise conteúdo, fontes, `REVISAO_HUMANA.md`, metadados, links e direitos dos anexos.
Entregue apenas os arquivos TSX e módulos aprovados ao caminho correspondente em
`src/app/educacao/<slug>/` do worktree da landing. O checklist e os JSON intermediários
permanecem na fábrica. Registre o consumidor real, o commit de origem e os testes da
integração; um arquivo sem import ou rota não está disponível ao leitor.

## Mídia no portal

O contrato canônico está sendo preparado em
[landing-page-geo/docs/operacao/publicacao-de-conteudo-e-midia.md](https://github.com/alexandrebrt14-sys/landing-page-geo/blob/master/docs/operacao/publicacao-de-conteudo-e-midia.md),
com a
[decisão de armazenamento, velocidade e memória](https://github.com/alexandrebrt14-sys/landing-page-geo/blob/master/governance/decisions/armazenamento-velocidade-e-memoria.md).
**Dependência de publicação:** o novo runbook e a evolução do migrador fazem parte deste
conjunto de 08/10/2026; seus links em `master` só estarão disponíveis após publicação.

A fábrica não faz upload R2. Entregue uma lista explícita de mídias com origem, direito
de uso, tamanho, SHA-256, MIME e, para imagens, dimensões e texto alternativo. O fluxo no
consumidor deve inventariar, testar um piloto, copiar e verificar o CDN, produzir recibo
de cobertura exata e preservar backup antes de remover os arquivos locais.

Novos conteúdos usam URLs diretas `https://midia.brasilgeo.ai/...`; downloads de PDF que
exigem anexo usam explicitamente `/downloads/...`. A compatibilidade por redirect atende
URLs legadas. O contrato do portal mantém essa lista finita e confere o limite agregado
da Vercel; novas imagens não devem consumir um redirect cada.

Adapte e teste `Next/Image`, miniaturas, posters e exportações offline. Verifique MIME,
CORS, download, reprodução e avanço de vídeos, URLs antigas e leitura offline. A mesma
URL pode funcionar no navegador e falhar no otimizador de imagens ou no exportador.
Conclua os gates e o build do portal, incluindo referências e arquivos rastreados pelas
funções, antes de publicar. Retirar o arquivo atual não remove seu histórico Git;
checkout raso, esparso e caches mudam o custo de CI. Não apague o histórico neste fluxo.

## O que ainda precisa de automação

- Pacote de entrega validável que una curso, fontes, revisão humana, consumidor e mídia;
  os campos acima ainda não são emitidos nem exigidos por um schema da fábrica.
- Confirmação de integração e publicação que substitua a pasta `deployed/` como evidência.
- Cobertura dos destinos de outros exportadores quando houver um contrato inequívoco;
  a guarda atual cobre somente rascunhos e catálogo.

A proteção contra reintroduzir arquivos migrados e a gestão de redirects ficam no
landing-page-geo. A [proposta de aprendizado](../wiki/proposals/publicacao-conteudo-midia-20261008.md)
registra o caso sem aprovação nem injeção em prompts.
