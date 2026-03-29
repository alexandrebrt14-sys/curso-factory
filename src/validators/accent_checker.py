"""Verificador e corretor automático de acentuação PT-BR.

Detecta palavras comuns que DEVEM ter acento mas aparecem sem,
e oferece correção automática. Ignora URLs, slugs, blocos de
código e nomes de variáveis.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class AccentError:
    """Erro de acentuação encontrado."""
    linha: int
    palavra_errada: str
    correcao: str
    contexto: str


# Mapeamento de palavras sem acento → forma correta
# Apenas palavras que NUNCA existem sem acento no contexto educacional
ACCENT_MAP: dict[str, str] = {
    # --- Palavras comuns ---
    "nao": "não",
    "voce": "você",
    "tambem": "também",
    "ate": "até",
    "ja": "já",
    "so": "só",
    "apos": "após",
    "entao": "então",
    "sera": "será",
    "esta": "está",
    "ai": "aí",
    "alias": "aliás",
    "porem": "porém",
    "alem": "além",
    "atraves": "através",
    "dificeis": "difíceis",
    "possiveis": "possíveis",
    "disponiveis": "disponíveis",
    "voces": "vocês",
    "nos": "nós",
    "ele": "ele",  # não acentuado, excluir
    "obvio": "óbvio",
    "obvia": "óbvia",
    "serio": "sério",
    "seria": "séria",
    "varios": "vários",
    "varias": "várias",
    "necessaria": "necessária",
    "necessarias": "necessárias",
    "primaria": "primária",
    "secundaria": "secundária",
    "contrario": "contrário",
    "voluntario": "voluntário",
    "extraordinario": "extraordinário",
    "contemporaneo": "contemporâneo",
    "espontaneo": "espontâneo",
    "instantaneo": "instantâneo",
    "simultaneo": "simultâneo",
    "heterogeneo": "heterogêneo",
    "homogeneo": "homogêneo",
    # --- Substantivos -ção ---
    "producao": "produção",
    "informacao": "informação",
    "educacao": "educação",
    "solucao": "solução",
    "aplicacao": "aplicação",
    "funcao": "função",
    "avaliacao": "avaliação",
    "classificacao": "classificação",
    "publicacao": "publicação",
    "introducao": "introdução",
    "conclusao": "conclusão",
    "secao": "seção",
    "licao": "lição",
    "atencao": "atenção",
    "compreensao": "compreensão",
    "instrucao": "instrução",
    "descricao": "descrição",
    "configuracao": "configuração",
    "comunicacao": "comunicação",
    "organizacao": "organização",
    "situacao": "situação",
    "operacao": "operação",
    "integracao": "integração",
    "otimizacao": "otimização",
    "automatizacao": "automatização",
    "implementacao": "implementação",
    "geracao": "geração",
    "migracao": "migração",
    "interacao": "interação",
    "visualizacao": "visualização",
    "autenticacao": "autenticação",
    "verificacao": "verificação",
    "atualizacao": "atualização",
    "documentacao": "documentação",
    "navegacao": "navegação",
    "recomendacao": "recomendação",
    "apresentacao": "apresentação",
    "contribuicao": "contribuição",
    "execucao": "execução",
    "resolucao": "resolução",
    "validacao": "validação",
    "transformacao": "transformação",
    "explicacao": "explicação",
    "motivacao": "motivação",
    "preparacao": "preparação",
    "comparacao": "comparação",
    "utilizacao": "utilização",
    "programacao": "programação",
    "administracao": "administração",
    "investigacao": "investigação",
    "fundamentacao": "fundamentação",
    "argumentacao": "argumentação",
    "formulacao": "formulação",
    "elaboracao": "elaboração",
    "regulamentacao": "regulamentação",
    "inovacao": "inovação",
    "adocao": "adoção",
    "evolucao": "evolução",
    "prevencao": "prevenção",
    "protecao": "proteção",
    "deteccao": "detecção",
    "selecao": "seleção",
    "construcao": "construção",
    "destruicao": "destruição",
    "reducao": "redução",
    "conexao": "conexão",
    "expansao": "expansão",
    "decisao": "decisão",
    "precisao": "precisão",
    "dimensao": "dimensão",
    "extensao": "extensão",
    "comissao": "comissão",
    "permissao": "permissão",
    "submissao": "submissão",
    "discussao": "discussão",
    "promocao": "promoção",
    "emocao": "emoção",
    "nocao": "noção",
    "opcao": "opção",
    "excecao": "exceção",
    "relacao": "relação",
    "populacao": "população",
    "observacao": "observação",
    "orientacao": "orientação",
    "concentracao": "concentração",
    "colaboracao": "colaboração",
    "negociacao": "negociação",
    "certificacao": "certificação",
    "especializacao": "especialização",
    "personalizacao": "personalização",
    "padronizacao": "padronização",
    "monetizacao": "monetização",
    "digitalizacao": "digitalização",
    # --- Substantivos -ência/-ância ---
    "experiencia": "experiência",
    "eficiencia": "eficiência",
    "frequencia": "frequência",
    "competencia": "competência",
    "referencia": "referência",
    "sequencia": "sequência",
    "importancia": "importância",
    "relevancia": "relevância",
    "tolerancia": "tolerância",
    "consistencia": "consistência",
    "transparencia": "transparência",
    "dependencia": "dependência",
    "tendencia": "tendência",
    "ocorrencia": "ocorrência",
    "permanencia": "permanência",
    "excelencia": "excelência",
    "inteligencia": "inteligência",
    "audiencia": "audiência",
    "influencia": "influência",
    "urgencia": "urgência",
    "emergencia": "emergência",
    "prevalencia": "prevalência",
    "equivalencia": "equivalência",
    "diferenca": "diferença",
    "presenca": "presença",
    "ausencia": "ausência",
    "essencia": "essência",
    "potencia": "potência",
    "ciencia": "ciência",
    "consciencia": "consciência",
    "gerencia": "gerência",
    "resistencia": "resistência",
    "existencia": "existência",
    "persistencia": "persistência",
    "recorrencia": "recorrência",
    "concorrencia": "concorrência",
    "preferencia": "preferência",
    "transferencia": "transferência",
    "inferencia": "inferência",
    "aderencia": "aderência",
    "coerencia": "coerência",
    "seguranca": "segurança",
    "confianca": "confiança",
    "lideranca": "liderança",
    "governanca": "governança",
    "mudanca": "mudança",
    "alianca": "aliança",
    "esperanca": "esperança",
    "semelhanca": "semelhança",
    # --- Proparoxítonas (-ico, -ulo, -tico, etc.) ---
    "conteudo": "conteúdo",
    "modulo": "módulo",
    "topico": "tópico",
    "pratica": "prática",
    "tecnica": "técnica",
    "basico": "básico",
    "logica": "lógica",
    "pagina": "página",
    "codigo": "código",
    "metodo": "método",
    "numero": "número",
    "unico": "único",
    "valido": "válido",
    "analise": "análise",
    "possivel": "possível",
    "disponivel": "disponível",
    "util": "útil",
    "facil": "fácil",
    "dificil": "difícil",
    "necessario": "necessário",
    "obrigatorio": "obrigatório",
    "especifico": "específico",
    "diagnostico": "diagnóstico",
    "estrategico": "estratégico",
    "didatico": "didático",
    "pedagogico": "pedagógico",
    "inicio": "início",
    "indice": "índice",
    "exercicio": "exercício",
    "beneficio": "benefício",
    "capitulo": "capítulo",
    "curriculo": "currículo",
    "obstaculo": "obstáculo",
    "veiculo": "veículo",
    "titulo": "título",
    "proposito": "propósito",
    "criterio": "critério",
    "cenario": "cenário",
    "vocabulario": "vocabulário",
    "relatorio": "relatório",
    "formulario": "formulário",
    "calendario": "calendário",
    "usuario": "usuário",
    "horario": "horário",
    "temporario": "temporário",
    "automatico": "automático",
    "sistematico": "sistemático",
    "tematico": "temático",
    "grafico": "gráfico",
    "historico": "histórico",
    "economico": "econômico",
    "academico": "acadêmico",
    "pratico": "prático",
    "tecnico": "técnico",
    "teorico": "teórico",
    "critico": "crítico",
    "publico": "público",
    "ultimo": "último",
    "minimo": "mínimo",
    "maximo": "máximo",
    "otimo": "ótimo",
    "pessimo": "péssimo",
    "proximo": "próximo",
    "sintese": "síntese",
    "hipotese": "hipótese",
    "ambito": "âmbito",
    "especifica": "específica",
    "basica": "básica",
    "praticas": "práticas",
    "tecnicas": "técnicas",
    "modulos": "módulos",
    "topicos": "tópicos",
    "codigos": "códigos",
    "metodos": "métodos",
    "numeros": "números",
    "titulos": "títulos",
    "graficos": "gráficos",
    "relatorios": "relatórios",
    "cenarios": "cenários",
    "usuarios": "usuários",
    "criterios": "critérios",
    "exercicios": "exercícios",
    "beneficios": "benefícios",
    "capitulos": "capítulos",
    "obstaculos": "obstáculos",
    "diagnosticos": "diagnósticos",
    "orgao": "órgão",
    "orgaos": "órgãos",
    "agil": "ágil",
    "fragil": "frágil",
    "movel": "móvel",
    "nivel": "nível",
    "niveis": "níveis",
    "responsavel": "responsável",
    "sustentavel": "sustentável",
    "flexivel": "flexível",
    "acessivel": "acessível",
    "compativel": "compatível",
    "variavel": "variável",
    "notavel": "notável",
    "consideravel": "considerável",
    "provavel": "provável",
    "inevitavel": "inevitável",
    "viavel": "viável",
    "amigavel": "amigável",
    "mensuravel": "mensurável",
    "escalavel": "escalável",
    "razoavel": "razoável",
    "indispensavel": "indispensável",
    "vulneravel": "vulnerável",
    "gerenciavel": "gerenciável",
    "previsivel": "previsível",
    "imprevisivel": "imprevisível",
    # --- Verbos acentuados ---
    "estara": "estará",
    "devera": "deverá",
    "podera": "poderá",
    "tera": "terá",
    "fara": "fará",
    "dara": "dará",
    "havera": "haverá",
    "ficara": "ficará",
    "tornara": "tornará",
    "permitira": "permitirá",
    "contribuira": "contribuirá",
    "garantira": "garantirá",
    "e" : None,  # Não mapear "e" para "é" — ambiguidade com conjunção
}

# Remover entradas None (marcadores de exclusão)
ACCENT_MAP = {k: v for k, v in ACCENT_MAP.items() if v is not None}

# Padrões que indicam contexto a ignorar (URLs, código, slugs)
IGNORE_PATTERNS = [
    re.compile(r"https?://\S+"),
    re.compile(r"`[^`]+`"),
    re.compile(r"```[\s\S]*?```", re.MULTILINE),
    re.compile(r"\[.*?\]\(.*?\)"),  # Links Markdown
    re.compile(r"<[^>]+>"),  # Tags HTML
    re.compile(r"!\[.*?\]\(.*?\)"),  # Imagens Markdown
    re.compile(r"\{[^}]+\}"),  # Placeholders tipo {variable}
    re.compile(r"[a-zA-Z_]\w*\.[a-zA-Z_]\w*"),  # Atributos objeto.attr
    re.compile(r"[a-zA-Z_]\w*\("),  # Chamadas de função func(
    re.compile(r"/[a-z0-9_-]+(?:/[a-z0-9_-]+)*"),  # Caminhos de URL /path/to
]


def _mask_ignored(text: str) -> str:
    """Substitui regiões a ignorar por espaços para preservar posições."""
    masked = text
    for pattern in IGNORE_PATTERNS:
        masked = pattern.sub(lambda m: " " * len(m.group()), masked)
    return masked


def _is_in_code_block(lines: list[str], line_num: int) -> bool:
    """Verifica se a linha está dentro de um bloco de código (```)."""
    in_code = False
    for i in range(line_num):
        if lines[i].strip().startswith("```"):
            in_code = not in_code
    return in_code


def check_accents(text: str) -> list[AccentError]:
    """Verifica acentuação PT-BR no texto.

    Retorna lista de erros encontrados com linha, palavra e correção.
    """
    erros: list[AccentError] = []
    linhas = text.split("\n")

    for num_linha, linha in enumerate(linhas, start=1):
        # Ignorar linhas dentro de blocos de código
        if _is_in_code_block(linhas, num_linha - 1):
            continue

        masked = _mask_ignored(linha)
        palavras = re.findall(r"\b([a-zA-Z]+)\b", masked)
        for palavra in palavras:
            lower = palavra.lower()
            if lower in ACCENT_MAP:
                ctx_start = max(0, linha.lower().find(lower) - 20)
                ctx_end = min(len(linha), linha.lower().find(lower) + len(lower) + 20)
                erros.append(AccentError(
                    linha=num_linha,
                    palavra_errada=palavra,
                    correcao=ACCENT_MAP[lower],
                    contexto=linha[ctx_start:ctx_end].strip(),
                ))

    return erros


def fix_accents(text: str) -> tuple[str, int]:
    """Corrige automaticamente acentuação PT-BR no texto.

    Preserva URLs, blocos de código, slugs e variáveis.

    Returns:
        Tupla com (texto_corrigido, total_de_correções).
    """
    linhas = text.split("\n")
    resultado: list[str] = []
    total_correcoes = 0
    in_code_block = False

    for linha in linhas:
        stripped = linha.strip()

        # Rastrear blocos de código
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            resultado.append(linha)
            continue

        # Dentro de bloco de código: não alterar
        if in_code_block:
            resultado.append(linha)
            continue

        # Mascarar regiões protegidas
        masked = _mask_ignored(linha)

        # Encontrar palavras na versão mascarada e corrigir na original
        linha_corrigida = list(linha)
        correcoes_linha: list[tuple[int, int, str]] = []

        for match in re.finditer(r"\b([a-zA-Z]+)\b", masked):
            palavra = match.group(1)
            lower = palavra.lower()
            if lower in ACCENT_MAP:
                correcao = ACCENT_MAP[lower]
                # Preservar capitalização original
                if palavra[0].isupper():
                    correcao = correcao[0].upper() + correcao[1:]
                if palavra.isupper():
                    correcao = correcao.upper()

                start = match.start()
                end = match.end()
                correcoes_linha.append((start, end, correcao))
                total_correcoes += 1

        # Aplicar correções de trás para frente (para não deslocar posições)
        for start, end, correcao in reversed(correcoes_linha):
            linha_corrigida[start:end] = list(correcao)

        resultado.append("".join(linha_corrigida))

    return "\n".join(resultado), total_correcoes


def format_report(erros: list[AccentError]) -> str:
    """Formata relatório de erros de acentuação."""
    if not erros:
        return "Acentuação: nenhum erro encontrado."
    linhas = [f"Acentuação: {len(erros)} erro(s) encontrado(s):\n"]
    for e in erros:
        linhas.append(
            f"  Linha {e.linha}: '{e.palavra_errada}' → '{e.correcao}' "
            f"(contexto: ...{e.contexto}...)"
        )
    return "\n".join(linhas)
