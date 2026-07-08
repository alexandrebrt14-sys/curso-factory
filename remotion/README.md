# curso-factory / remotion

Subprojeto Node (isolado do Python) que produz a abertura animada de curso em
vídeo programático com React (Remotion). Técnica auditada no remotion.dev:
vídeo feito em React, embutido na página via player e exportável como MP4.

## O que é
- `src/CourseIntro.tsx` — composição parametrizada (título, nível, módulos,
  duração, cor). Espelha `landing-page-geo/src/remotion/compositions/CourseIntro`.
- `src/Root.tsx` / `src/index.ts` — catálogo e entry do Remotion.

## Como o curso-factory usa
O Python NÃO depende deste subprojeto para gerar conteúdo. Ele é acionado só no
passo opcional de divulgação:

```bash
# A partir de um JSON de CourseDefinition
python cli.py render-video --course output/deployed/<slug>/course.json

# Ou direto por flags
python cli.py render-video --titulo "MCP Avancado" --nivel avancado --modulos 12 --duracao "~245 min"
```
O `src/generators/video_generator.py` instala as deps na primeira execução
(`npm install` aqui dentro) e chama `npx remotion render`.

## Uso direto (preview/render manual)
```bash
cd remotion
npm install
npm run studio                       # preview interativo
npm run render -- out/intro.mp4      # export MP4 com props default
```

## Página gerada
Quando um curso define `intro_video: true` no `CourseDefinition`, o template
`src/templates/page.tsx.j2` embute `<CourseVideoPlayer>` (componente do
landing-page-geo) — auto-demo ao vivo na página, sem precisar do MP4.

## Regras
- Node-only. `@remotion/renderer` baixa um Chromium headless no primeiro render.
- Props de composição são `type`, não `interface` (exigência Record<string, unknown>).
- Literais JSX em ASCII; texto humano vem das props.
