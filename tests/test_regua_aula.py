"""A régua da aula (tipo D) vem da fonte, e o gate a aplica.

Estes testes existem porque a mudança de 27/08/2026 é fácil de desfazer sem
querer: basta alguém reintroduzir um número em código ou no YAML e a régua passa
a viver em dois lugares outra vez. O que se cobra aqui é o vínculo, não o valor:
se `config/lexicos.json` mudar (porque a fonte mudou e o espelho foi regerado),
os testes acompanham sozinhos.

O único valor literal afirmado é o do documento de plano — 900 de piso, 1.200 a
2.400 de alvo — e ele é afirmado UMA vez, contra o espelho, para que um espelho
regerado errado (por exemplo com os tetos do artigo, tipo A) fique vermelho.
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.validators.content_checker import (  # noqa: E402
    check_content,
    tetos_da_unidade,
)
from src.validators.lexicos_loader import expressoes_vetadas, tetos_da_aula  # noqa: E402


def _aula(palavras: int, h2: int = 3, exercicios: int = 1) -> str:
    """Monta uma aula sintética com o número de palavras e de H2 pedidos.

    Os parágrafos saem com 30 palavras, no meio da faixa de 15-45, para que a
    checagem de parágrafo não polua o resultado dos testes de extensão.
    """
    partes = ["# Aula de teste", ""]
    for i in range(h2):
        partes += [f"## Seção {i + 1}", ""]
    for i in range(exercicios):
        partes += [f"### Exercício {i + 1}: aplique no seu negócio", ""]
    faltam = palavras - len(" ".join(partes).split())
    while faltam > 0:
        n = min(30, faltam)
        partes += [" ".join(["palavra"] * n), ""]
        faltam -= n
    return "\n".join(partes)


def _categorias(erros, categoria: str, tipo: str) -> list[str]:
    return [e.mensagem for e in erros if e.categoria == categoria and e.tipo == tipo]


class TestEspelhoDaFonte(unittest.TestCase):
    """O espelho gerado precisa trazer o tipo D e os números do plano."""

    def test_lexicos_json_existe_e_tem_o_tipo_d(self):
        caminho = PROJECT_ROOT / "config" / "lexicos.json"
        self.assertTrue(
            caminho.exists(),
            "config/lexicos.json sumiu. Regere com: python -m escrita.cli lexicos --json",
        )
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        self.assertIn("tetos", dados)
        self.assertIn("D", dados["tetos"])
        self.assertEqual(dados["tetos"]["D"]["nome"], "aula")

    def test_o_tipo_d_traz_a_regua_de_27_08_2026(self):
        """Único ponto onde os números literais do plano são afirmados."""
        d = tetos_da_aula()
        self.assertEqual(d["palavras"]["piso"], 900)
        self.assertEqual(list(d["palavras"]["alvo"]), [1200, 2400])
        self.assertEqual(d["palavras"]["aviso"], 2400)
        self.assertEqual(d["palavras"]["erro"], 3600)
        self.assertEqual(list(d["h2"]), [2, 4])
        self.assertEqual(d["h3_por_h2"], 2)
        self.assertEqual(d["figuras_max"], 3)
        self.assertEqual(list(d["paragrafo"]), [15, 45])

    def test_a_fonte_alimenta_as_expressoes_vetadas(self):
        vetadas = {e.lower() for e in expressoes_vetadas()}
        self.assertIn("especialistas apontam", vetadas)
        self.assertIn("vagas limitadas", vetadas)


class TestTetosDaUnidade(unittest.TestCase):
    """A aula é o padrão; o módulo é a compatibilidade, multiplicada."""

    def test_aula_e_o_padrao_e_espelha_a_fonte(self):
        t = tetos_da_unidade()
        d = tetos_da_aula()
        self.assertEqual(t["unidade"], "aula")
        self.assertEqual(t["piso"], d["palavras"]["piso"])
        self.assertEqual(list(t["alvo"]), list(d["palavras"]["alvo"]))
        self.assertEqual(t["exercicios_min"], 1)

    def test_modulo_vale_de_quatro_a_seis_aulas(self):
        aula = tetos_da_unidade("aula")
        modulo = tetos_da_unidade("modulo")
        self.assertEqual(modulo["unidade"], "módulo")
        self.assertEqual(modulo["piso"], aula["piso"] * 4)
        self.assertEqual(modulo["alvo"], (aula["alvo"][0] * 4, aula["alvo"][1] * 6))
        self.assertEqual(modulo["erro"], aula["erro"] * 6)
        # A faixa do módulo é a que consta do PLANO_DE_MIGRACAO: 4.800-14.400.
        self.assertEqual(modulo["alvo"], (4800, 14400))


class TestExtensaoDaAula(unittest.TestCase):
    """Piso, alvo, aviso e erro do molde D chegam ao veredito."""

    def test_abaixo_do_piso_reprova(self):
        erros = check_content(_aula(400), "aula")
        bloqueantes = _categorias(erros, "profundidade", "error")
        self.assertEqual(len(bloqueantes), 1)
        self.assertIn("abaixo do piso", bloqueantes[0])
        self.assertIn("900", bloqueantes[0])

    def test_entre_o_piso_e_o_alvo_avisa(self):
        erros = check_content(_aula(1000), "aula")
        self.assertEqual(_categorias(erros, "profundidade", "error"), [])
        self.assertEqual(len(_categorias(erros, "profundidade", "warning")), 1)

    def test_dentro_do_alvo_nao_reclama(self):
        erros = check_content(_aula(1500), "aula")
        self.assertEqual(_categorias(erros, "profundidade", "error"), [])
        self.assertEqual(_categorias(erros, "profundidade", "warning"), [])

    def test_acima_do_aviso_avisa(self):
        erros = check_content(_aula(3000), "aula")
        self.assertEqual(_categorias(erros, "profundidade", "error"), [])
        self.assertEqual(len(_categorias(erros, "profundidade", "warning")), 1)

    def test_acima_do_teto_reprova(self):
        erros = check_content(_aula(4000), "aula")
        bloqueantes = _categorias(erros, "profundidade", "error")
        self.assertEqual(len(bloqueantes), 1)
        self.assertIn("3600", bloqueantes[0].replace(".", ""))

    def test_o_mesmo_texto_passa_como_modulo_e_reprova_como_aula(self):
        """O modo de compatibilidade não pode ser cosmético."""
        texto = _aula(5000, h2=10)
        como_aula = _categorias(check_content(texto, "x", unidade="aula"),
                                "profundidade", "error")
        como_modulo = _categorias(check_content(texto, "x", unidade="modulo"),
                                  "profundidade", "error")
        self.assertEqual(len(como_aula), 1)
        self.assertEqual(como_modulo, [])


class TestEstruturaDaAula(unittest.TestCase):
    """H2, H3, visuais e exercício viraram teto ou piso de 1."""

    def test_menos_de_dois_h2_reprova(self):
        erros = check_content(_aula(1500, h2=1), "aula")
        self.assertTrue(_categorias(erros, "formatação", "error"))

    def test_mais_de_quatro_h2_avisa(self):
        erros = check_content(_aula(1500, h2=6), "aula")
        avisos = _categorias(erros, "formatação", "warning")
        self.assertTrue(any("acima do teto" in m for m in avisos))

    def test_um_exercicio_basta(self):
        """Era 'mínimo 3'. Com 1 o gate não pode mais reprovar."""
        erros = check_content(_aula(1500, exercicios=1), "aula")
        self.assertEqual(_categorias(erros, "exercícios", "error"), [])

    def test_sem_exercicio_reprova(self):
        erros = check_content(_aula(1500, exercicios=0), "aula")
        self.assertEqual(len(_categorias(erros, "exercícios", "error")), 1)

    def test_tabela_nao_e_mais_obrigatoria(self):
        """Regressão: aula sem tabela e sem blockquote passa."""
        erros = check_content(_aula(1500), "aula")
        mensagens = " ".join(e.mensagem for e in erros if e.tipo == "error")
        self.assertNotIn("tabela", mensagens)
        self.assertNotIn("citação", mensagens)

    def test_mais_de_tres_visuais_avisa(self):
        base = _aula(1500)
        figuras = "\n\n".join(
            f"![Legenda que afirma o que a figura {i} mostra](fig{i}.svg)"
            for i in range(4)
        )
        erros = check_content(base + "\n\n" + figuras, "aula")
        avisos = _categorias(erros, "formatação", "warning")
        self.assertTrue(any("apoios visuais" in m for m in avisos))


class TestParagrafoEmPalavras(unittest.TestCase):
    """A faixa de parágrafo passou de linhas para palavras (15 a 45)."""

    def test_paragrafo_longo_avisa(self):
        texto = _aula(1500) + "\n\n" + " ".join(["palavra"] * 60)
        avisos = _categorias(check_content(texto, "aula"), "formatação", "warning")
        self.assertTrue(any("longo" in m for m in avisos))

    def test_paragrafo_curto_avisa(self):
        texto = _aula(1500) + "\n\nFrase curta demais."
        avisos = _categorias(check_content(texto, "aula"), "formatação", "warning")
        self.assertTrue(any("curto" in m for m in avisos))


if __name__ == "__main__":
    unittest.main()
