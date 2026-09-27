"""Testes de integridade dos prompts por idioma.

Existem por causa de um quase acidente. O `lang_resolver` procura o prompt em
`prompts/<lang>/` **antes** da raiz, e o idioma padrão é `pt-br`. Uma rodada
editou a regra nova só no arquivo da raiz, e a mudança teria ficado **inerte no
caminho padrão de geração**, sem erro, sem log e sem teste vermelho. O defeito
só apareceu porque alguém foi conferir à mão.

O invariante NÃO é identidade byte a byte. A cópia por idioma é legitimamente
mais rica que a raiz: `pt-br/classify.md` acrescenta as tags canônicas de GEO e
`pt-br/research.md` acrescenta a regra anti-GhostCite, e nenhuma das duas existe
no arquivo genérico. O invariante é mais fraco e mais útil:

    a cópia por idioma pode ACRESCENTAR, nunca PERDER.

Perder seção é o defeito real, e é o que estes testes pegam.

Desde 02/09/2026 o prompt de redação escreve UMA aula por chamada e recebe os
tetos da aula como variáveis (`{palavras_alvo_min}`, `{figuras_max}`...), lidas
de `config/lexicos.json`. O prompt não carrega número nenhum, então o que se
cobra aqui é a presença das variáveis em todos os idiomas: prompt sem elas
volta a inventar a régua por conta própria.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

PROMPTS = PROJECT_ROOT / "src" / "templates" / "prompts"

#: Idiomas que têm pasta própria. `pt-br` é o padrão e o que mais importa,
#: porque é ele que sombreia a raiz na geração do dia a dia.
IDIOMAS = ("pt-br", "en", "es")

#: Variáveis que o orquestrador injeta na redação de cada aula
#: (`Orchestrator._draft_lesson` e `_tetos_da_aula`).
VARIAVEIS_DA_AULA = (
    "{lesson_title}",
    "{lesson_idea}",
    "{previous_lessons}",
    "{next_lessons}",
    "{palavras_piso}",
    "{palavras_alvo_min}",
    "{palavras_alvo_max}",
    "{palavras_aviso}",
    "{h2_min}",
    "{h2_max}",
    "{h3_por_h2}",
    "{figuras_max}",
    "{paragrafo_min}",
    "{paragrafo_max}",
    "{context}",
)

#: Variáveis que o orquestrador injeta na revisão de cada aula
#: (`Orchestrator._review_iterative`).
VARIAVEIS_DA_REVISAO = ("{unit_title}", "{unit_position}", "{analysis_summary}", "{context}")

#: Números da régua antiga que NÃO podem voltar ao prompt: a régua vive na
#: fonte de estilo e chega por variável.
NUMEROS_PROIBIDOS = (
    "1.200 caracteres",
    "2.500 caracteres",
    "3 exercícios",
    "three exercises",
    "tres ejercicios",
)


def _titulos(caminho: Path) -> list[str]:
    """Devolve as linhas de cabeçalho Markdown, normalizadas.

    Compara só o texto do cabeçalho, sem o nível, porque promover ou rebaixar
    uma seção é reorganização legítima; sumir com ela não é.
    """
    linhas = caminho.read_text(encoding="utf-8").splitlines()
    return [linha.lstrip("#").strip() for linha in linhas if linha.startswith("#")]


class TestRaizSoGuardaOQueCarrega(unittest.TestCase):
    """Desde 27/09/2026 a raiz de `prompts/` não tem cópia de prompt com pasta por idioma.

    O quase acidente que criou este arquivo foi uma regra editada só na raiz,
    inerte porque `pt-br/` vence a cascata. A cura deixou de ser comparar as
    duas cópias: a cópia de raiz saiu. Aqui se prova que ela não volta e que
    todo agente resolve o prompt dentro de `pt-br/` (ou do idioma dele).
    """

    def test_raiz_nao_duplica_prompt_de_pasta_de_idioma(self):
        duplicados = [p.name for p in PROMPTS.glob("*.md") if (PROMPTS / "pt-br" / p.name).exists()]
        self.assertEqual(duplicados, [], f"cópia de raiz que nunca carrega: {duplicados}")

    def test_todo_agente_resolve_dentro_de_pt_br(self):
        from src.agents import analyzer, classifier, humanizer, researcher, reviewer, writer
        from src.agents.lang_resolver import resolve_prompt_path

        for modulo in (analyzer, classifier, humanizer, researcher, reviewer, writer):
            classe = next(
                v
                for v in vars(modulo).values()
                if isinstance(v, type)
                and getattr(v, "prompt_file", "")
                and v.__module__ == modulo.__name__
            )
            with self.subTest(agente=classe.__name__):
                caminho = resolve_prompt_path(classe.prompt_file, "pt-br")
                self.assertEqual(caminho.parent.name, "pt-br")


class TestVariaveisDaAulaChegaramAosIdiomas(unittest.TestCase):
    """O contrato do prompt de aula precisa valer em todos os idiomas.

    Variável atravessa tradução, então é o que se cobra aqui. Se o orquestrador
    ganhar uma variável nova, este teste fica vermelho em todos os idiomas de
    uma vez, que é o lembrete de atualizar os quatro arquivos.
    """

    def _alvos(self, nome: str) -> list[Path]:
        alvos = [PROMPTS / idioma / nome for idioma in IDIOMAS]
        return [c for c in alvos if c.exists()]

    def test_draft_recebe_as_variaveis_da_aula(self):
        for caminho in self._alvos("draft.md"):
            texto = caminho.read_text(encoding="utf-8")
            rotulo = caminho.relative_to(PROMPTS).as_posix()
            with self.subTest(prompt=rotulo):
                faltando = [v for v in VARIAVEIS_DA_AULA if v not in texto]
                self.assertEqual(
                    faltando,
                    [],
                    f"{rotulo} não traz as variáveis da aula {faltando}; sem elas o "
                    "redator não recebe os tetos da fonte de estilo.",
                )
                proibidos = [n for n in NUMEROS_PROIBIDOS if n in texto]
                self.assertEqual(
                    proibidos, [], f"{rotulo} voltou a carregar régua fixa: {proibidos}"
                )

    def test_review_recebe_as_variaveis_da_unidade(self):
        for caminho in self._alvos("review.md"):
            texto = caminho.read_text(encoding="utf-8")
            rotulo = caminho.relative_to(PROMPTS).as_posix()
            with self.subTest(prompt=rotulo):
                faltando = [v for v in VARIAVEIS_DA_REVISAO if v not in texto]
                self.assertEqual(faltando, [], f"{rotulo} não traz {faltando}")
                self.assertIn(
                    "REVIS",
                    texto,
                    f"{rotulo} precisa pedir o bloco 'REVISÃO CONCLUÍDA', que o "
                    "orquestrador separa do texto revisado.",
                )
                proibidos = [n for n in NUMEROS_PROIBIDOS if n in texto]
                self.assertEqual(
                    proibidos, [], f"{rotulo} voltou a carregar régua fixa: {proibidos}"
                )

    def test_o_prompt_manda_uma_linha_de_texto_por_linha_da_tabela(self):
        """A instrução antiga inviabilizava a promoção da tabela.

        Os prompts mandavam formatar a tabela como uma única linha, com `\\n`
        separando as rows, herança de quando o Markdown virava string TSX na
        mão. O parser promove tabela a bloco visual, e promoção depende de
        quebra de linha real. A cobrança é pela afirmativa: os prompts dizem
        "uma linha de texto por linha da tabela" como parte da instrução.
        """
        marcas = (
            "uma linha de texto por linha da tabela",
            "one line of text per table row",
            "una línea de texto por fila de la tabla",
        )
        for caminho in self._alvos("draft.md"):
            texto = caminho.read_text(encoding="utf-8")
            rotulo = caminho.relative_to(PROMPTS).as_posix()
            with self.subTest(prompt=rotulo):
                self.assertTrue(
                    any(m in texto for m in marcas),
                    f"{rotulo} precisa mandar uma linha de texto por linha da tabela.",
                )


if __name__ == "__main__":
    unittest.main()
