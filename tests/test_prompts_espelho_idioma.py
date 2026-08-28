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

#: Prompts que carregam a régua de peso visual. A doutrina vive em
#: docs/DOUTRINA_VISUAL_CURSOS.md; aqui só se cobra que ela chegou ao prompt.
PROMPTS_COM_REGUA = ("draft.md", "review.md")


def _titulos(caminho: Path) -> list[str]:
    """Devolve as linhas de cabeçalho Markdown, normalizadas.

    Compara só o texto do cabeçalho, sem o nível, porque promover ou rebaixar
    uma seção é reorganização legítima; sumir com ela não é.
    """
    linhas = caminho.read_text(encoding="utf-8").splitlines()
    return [linha.lstrip("#").strip() for linha in linhas if linha.startswith("#")]


class TestCopiaPorIdiomaNaoPerdeSecao(unittest.TestCase):
    """Nenhuma seção da raiz pode sumir na cópia de um idioma."""

    def test_pt_br_nao_perde_secao_da_raiz(self):
        """`pt-br` é o caminho padrão: perder seção aqui é perder na prática."""
        pasta = PROMPTS / "pt-br"
        self.assertTrue(pasta.is_dir(), "a pasta pt-br precisa existir")

        for arquivo in sorted(pasta.glob("*.md")):
            raiz = PROMPTS / arquivo.name
            if not raiz.exists():
                continue
            with self.subTest(prompt=arquivo.name):
                da_raiz = _titulos(raiz)
                do_idioma = set(_titulos(arquivo))
                faltando = [t for t in da_raiz if t not in do_idioma]
                self.assertEqual(
                    faltando, [],
                    f"pt-br/{arquivo.name} perdeu seção(ões) que existem na raiz: "
                    f"{faltando}. A cópia por idioma pode acrescentar, nunca perder, "
                    "e ela sombreia a raiz na geração em português.",
                )


class TestReguaDePesoVisualChegouAosIdiomas(unittest.TestCase):
    """A régua precisa estar em todos os idiomas, não só na raiz.

    Número atravessa tradução, então é o que se cobra aqui. Se alguém mudar o
    teto ou a densidade, este teste fica vermelho em todos os idiomas de uma
    vez, que é exatamente o lembrete de atualizar os quatro arquivos.
    """

    def _contem_regua(self, caminho: Path) -> tuple[bool, bool]:
        texto = caminho.read_text(encoding="utf-8")
        tem_teto = "1.200" in texto or "1,200" in texto
        tem_densidade = "2.500" in texto or "2,500" in texto
        return tem_teto, tem_densidade

    def test_a_regua_esta_na_raiz_e_em_todos_os_idiomas(self):
        for nome in PROMPTS_COM_REGUA:
            alvos = [PROMPTS / nome]
            alvos += [PROMPTS / idioma / nome for idioma in IDIOMAS]
            for caminho in alvos:
                if not caminho.exists():
                    continue
                rotulo = caminho.relative_to(PROMPTS).as_posix()
                with self.subTest(prompt=rotulo):
                    tem_teto, tem_densidade = self._contem_regua(caminho)
                    self.assertTrue(
                        tem_teto,
                        f"{rotulo} não traz o teto de 1.200 caracteres por parágrafo.",
                    )
                    self.assertTrue(
                        tem_densidade,
                        f"{rotulo} não traz a densidade de um apoio visual a cada "
                        "2.500 caracteres de prosa.",
                    )

    def test_o_prompt_manda_uma_linha_de_texto_por_linha_da_tabela(self):
        """A instrução antiga inviabilizava a promoção da tabela.

        Os prompts mandavam formatar a tabela como uma única linha, com `\\n`
        separando as rows, herança de quando o Markdown virava string TSX na
        mão. O parser promove tabela a bloco visual, e promoção depende de
        quebra de linha real. Sem esta instrução a tabela deixa de contar como
        bloco visual e o curso volta a nascer reprovado.

        A cobrança é pela afirmativa, e não pela ausência da frase antiga: os
        três idiomas dizem "nunca tudo numa linha só" como parte da instrução
        correta, então procurar a frase proibida acusa o texto certo.
        """
        marcadores = {
            "draft.md": "uma linha de texto por linha",
            "pt-br/draft.md": "uma linha de texto por linha",
            "en/draft.md": "one line of text per table row",
            "es/draft.md": "una línea de texto por fila",
        }
        for rotulo, marcador in marcadores.items():
            caminho = PROMPTS / rotulo
            if not caminho.exists():
                continue
            with self.subTest(prompt=rotulo):
                texto = caminho.read_text(encoding="utf-8").lower()
                self.assertIn(
                    marcador.lower(), texto,
                    f"{rotulo} não manda mais uma linha de texto por linha da "
                    "tabela. Sem isso o parser não promove a tabela a bloco "
                    "visual e o curso nasce reprovado no piso.",
                )


class TestConjuntoDeArquivosPorIdioma(unittest.TestCase):
    """Um prompt novo não pode nascer só num idioma sem que se saiba."""

    def test_todo_prompt_de_idioma_tem_par_na_raiz(self):
        """Arquivo que só existe numa pasta de idioma é órfão silencioso."""
        for idioma in IDIOMAS:
            pasta = PROMPTS / idioma
            if not pasta.is_dir():
                continue
            for arquivo in sorted(pasta.glob("*.md")):
                with self.subTest(prompt=f"{idioma}/{arquivo.name}"):
                    self.assertTrue(
                        (PROMPTS / arquivo.name).exists(),
                        f"{idioma}/{arquivo.name} não tem par na raiz. A raiz é o "
                        "recuo do lang_resolver: sem ela, outro idioma cai no vazio.",
                    )


if __name__ == "__main__":
    unittest.main()
