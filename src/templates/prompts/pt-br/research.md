# Prompt — Pesquisa de Mercado e Fundamentação (Perplexity)

## Contexto

Você é um pesquisador educacional com rigor acadêmico, especializado em fundamentar cursos online de alta qualidade. Sua pesquisa deve fornecer a base factual e analítica para conteúdo com padrão editorial de publicações como Harvard Business Review, MIT Sloan Management Review e HSM Management.

## Curso

- **Nome:** {course_name}
- **Descrição:** {course_description}
- **Módulos previstos:** {target_modules}

## O que pesquisar

### 1. Dados de Mercado e Contexto (2025–2026)

- Tamanho do mercado e crescimento projetado para este segmento educacional
- Plataformas líderes (Udemy, Coursera, Hotmart, Alura etc.) e seus dados públicos
- Ticket médio de cursos semelhantes em português e em inglês
- Taxa de conclusão média em cursos desta categoria
- Dados demográficos do público-alvo (idade, formação, cargo, setor)

### 2. Fundamentação Acadêmica e Científica

- Pesquisas e artigos acadêmicos relevantes ao tema central do curso
- Frameworks teóricos consolidados na área (cite autores e publicações)
- Estudos de caso documentados em periódicos ou publicações de negócios
- Dados estatísticos com fontes primárias identificadas
- Meta-análises ou revisões sistemáticas quando disponíveis

**Regra anti-GhostCite (obrigatória para claims acadêmicos):** todo paper citado deve vir com identificador verificável (arXiv ID, DOI ou URL do abstract) e o número/afirmação atribuído deve constar do abstract ou do corpo consultado, nunca de memória. Se você não conseguir apontar o identificador, rebaixe o claim para [Baixa] ou remova. Atribuir a um paper real um achado que não está nele é o erro mais grave desta pesquisa (já ocorreu no corpus com o GEO-16 atribuído indevidamente ao paper de Princeton; a wave `docs/research/geo-wave-julho-22-2026/` mantém a lista de 32 papers de GEO com ID verificado para consulta).

### 3. Tendências e Inovações

- Metodologias pedagógicas eficazes para este tipo de conteúdo (andragogia, microlearning, problem-based learning)
- Formatos preferidos pelo público em 2026 (vídeo curto, projetos práticos, simulações)
- Ferramentas e tecnologias emergentes citadas por especialistas
- Pesquisas sobre retenção e engajamento em cursos online para adultos

### 4. Análise Competitiva

- Liste ao menos 5 cursos concorrentes com: nome, plataforma, preço, avaliação média, número de alunos
- Identifique pontos fortes e fracos recorrentes nas avaliações de alunos
- Aponte lacunas não atendidas pelo mercado atual (oportunidades de diferenciação)
- Analise o nível de profundidade dos concorrentes (superficial vs. aprofundado)

### 5. Fontes e Referências Recomendadas

Priorize a edição mais recente de cada fonte; fonte antiga só quando é a origem do conceito:

- **Relatórios de mercado**: HolonIQ, Ambient Insight, Class Central, Research and Markets
- **Publicações de negócios**: Harvard Business Review, MIT Sloan, McKinsey Insights, Deloitte Insights
- **Periódicos acadêmicos**: quando relevante ao tema do curso
- **Dados públicos de plataformas**: páginas de vendas, reviews, dados de redes sociais
- **Publicações brasileiras**: HSM Management, Exame, Valor Econômico, repositórios USP/Unicamp/FGV

### 6. Como fazer: procedimentos, erros comuns e decisões

A aula é um guia aplicável: o aluno sai sabendo fazer. Para cada tarefa central do curso:

- O procedimento documentado pela fonte primária (documentação oficial, norma, guia do
  fabricante), com os passos na ordem, o que precisa estar pronto antes e o sinal de que cada
  passo deu certo
- Os erros mais comuns registrados (suporte oficial, relatório, estudo) e o conserto de cada um
- As decisões do caminho: em que situação a resposta muda e o que fazer em cada uma
- Um ou dois exemplos aplicados, com número e fonte, que mostrem o procedimento funcionando
  num negócio pequeno; história sem passo ensinado não serve

## Pesquisa orientada à decisão e ao uso em busca

Desdobre a ideia do curso em perguntas que o aluno precisa resolver: condições de uso,
alternativas, custo, erro comum e limite. Agrupe variações que levam à mesma resposta.
Procure também evidências que contrariem a hipótese inicial. O conjunto de buscas orienta
a cobertura; não exige páginas ou aulas redundantes para cada expressão.

Para cada afirmação aproveitável, registre sujeito, período, público, unidade, denominador,
comparador, origem e limite. Diferencie observação, opinião, projeção e exemplo hipotético.
Um trecho com link só conta como evidência se a fonte consultada sustentar aquela afirmação.
Vários textos derivados de um mesmo estudo contam como uma origem.

Use a data de publicação e a data do fenômeno; procure a versão vigente de fatos perecíveis.
Registre a data de publicação de cada fonte (dia, mês e ano; mês e ano quando o documento não
traz o dia). Fundamento antigo entra como origem do conceito, dito assim; ele não autoriza dado
desatualizado.

{bloco_fontes_recentes_pesquisa} Se faltarem casos ou dados, registre a lacuna na pesquisa sem inventar
material para completar a quantidade pedida.

Quando o tema envolver SEO ou GEO, separe a documentação oficial, os estudos e as hipóteses
editoriais. Pesquisa de opinião não fornece pesos de ranking. Citação, menção de marca,
apoio à afirmação, visita e venda são observações distintas. Faixa de palavras, quantidade
de referências ou metadados não garantem presença em uma resposta de IA.

Liste as variantes da pergunta central que o aluno digitaria (sinônimos, a comparação entre
opções, o custo, o "como fazer" e o "vale a pena"), porque o motor desdobra a consulta em
buscas internas e recupera fontes para cada uma. O estudo de 19/09/2026 (arXiv 2609.23162,
observacional) registrou menção de marca entre 2,8% e 3,8% quando nem domínio nem marca
apareciam no caminho de recuperação, contra 91,4% a 100% quando o domínio era citado e a marca
aparecia nas buscas internas do motor. Ao trazer estado da arte de GEO, registre também estes limites, com a
data: as alavancas do paper de 2023 (estatísticas, citações e falas atribuídas) não moveram
citação em dez famílias de motores no reteste de 07/09/2026 (arXiv 2609.07559), então entram
só como origem do conceito; os motores quase não citam as mesmas URLs entre si e 67% das URLs
trocaram no mesmo motor de um dia para o outro (arXiv 2609.22655, 19/09/2026), então medição
de visibilidade de uma rodada só, num motor só, não sustenta conclusão; e o mesmo intento em
outro idioma expõe outro conjunto de fontes (arXiv 2609.24407, 21/09/2026), então dado medido
em inglês não descreve o Google em português sem ressalva.

Os níveis de confiança abaixo descrevem a procedência disponível. Eles não substituem
a avaliação do método, da população pertinente e do apoio à afirmação escrita.

## Formato de saída

Retorne um documento estruturado em Markdown com:

1. Seções numeradas correspondentes aos itens acima
2. **Tabelas comparativas** para dados de mercado e análise competitiva
3. **Referências completas** para cada dado citado (autor, título, publicação, data de publicação, URL quando disponível)
4. **Nível de confiança** para cada dado: [Alta] fonte primária verificável, [Média] fonte secundária confiável, [Baixa] estimativa ou dado parcial

Escreva em Português do Brasil com acentuação completa e ortografia correta.
