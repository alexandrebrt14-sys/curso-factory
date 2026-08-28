"""Testes do contrato dos blocos visuais no modelo e no schema.

O gerador emitia cinco tipos de bloco, nenhum deles visual, e por isso todo
curso gerado nascia reprovado na doutrina de peso visual. Estes testes cobram o
contrato novo: os seis tipos existem, cada um cobra a sua carga, e o schema JSON
diz exatamente o mesmo que o modelo Pydantic.

A divergência entre modelo e schema é o defeito mais caro possível aqui, porque
produz bloco que um dos dois aceita e o outro recusa, dependendo do caminho de
validação que rodar primeiro.
"""

import json
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pydantic import ValidationError

from src.models import (
    PAYLOAD_SECTION_TYPES,
    VISUAL_SECTION_TYPES,
    CourseSection,
    SectionType,
)

SCHEMA_PATH = PROJECT_ROOT / "src" / "schemas" / "course.schema.json"

TABELA_OK = {
    "title": "As três réguas de volume",
    "columns": ["Régua", "O número", "De onde vem"],
    "rows": [
        ["Operador", "400 a 500 por mês", "Régua de quem operou"],
        ["Documentação", "250 anúncios ativos", "Orientação publicada"],
    ],
}

COMPARATIVO_OK = {
    "title": "Como escrever o parágrafo de abertura",
    "left": {"header": "A evitar", "items": ["Abrir pela história de fundação"]},
    "right": {"header": "Recomendado", "items": ["Abrir pelo problema do leitor"]},
}

PAINEL_OK = {
    "title": "O acervo medido",
    "stats": [
        {"value": "26", "label": "cursos sem bloco visual", "sub": "de 52 medidos"},
        {"value": "4.590", "label": "maior parágrafo", "sub": "em caracteres"},
    ],
}

GUIA_OK = {
    "title": "Publicar um curso novo",
    "steps": [
        {"label": "Registrar no catálogo", "success": "O curso aparece na listagem"},
        {"label": "Rodar os portões", "pitfall": "Pular a guarda de acentuação"},
    ],
}

LINHA_DO_TEMPO_OK = {
    "title": "A reforma do curso",
    "events": [
        {"date": "16/08/2026", "label": "Publicação", "tone": "past"},
        {"date": "17/08/2026", "label": "Cinco ondas de correção", "tone": "now"},
    ],
}

CARGAS_VALIDAS = {
    SectionType.DATA_TABLE: TABELA_OK,
    SectionType.COMPARISON: COMPARATIVO_OK,
    SectionType.STAT_GRID: PAINEL_OK,
    SectionType.STEP_GUIDE: GUIA_OK,
    SectionType.TIMELINE: LINHA_DO_TEMPO_OK,
}


class TestTiposVisuais(unittest.TestCase):
    """Os seis tipos existem e estão classificados corretamente."""

    def test_os_seis_tipos_visuais_existem(self):
        esperados = {"figure", "dataTable", "comparison", "statGrid", "stepGuide", "timeline"}
        self.assertEqual({t.value for t in VISUAL_SECTION_TYPES}, esperados)

    def test_figure_e_visual_mas_nao_tem_payload(self):
        self.assertIn(SectionType.FIGURE, VISUAL_SECTION_TYPES)
        self.assertNotIn(SectionType.FIGURE, PAYLOAD_SECTION_TYPES)

    def test_tipos_de_prosa_nao_contam_como_visuais(self):
        for tipo in (SectionType.TEXT, SectionType.CODE, SectionType.TIP,
                     SectionType.WARNING, SectionType.CHECKPOINT):
            self.assertNotIn(tipo, VISUAL_SECTION_TYPES)


class TestCargaObrigatoria(unittest.TestCase):
    """Bloco sem a carga certa é recusado na geração, não na página."""

    def test_cada_tipo_com_payload_aceita_a_sua_carga(self):
        for tipo, carga in CARGAS_VALIDAS.items():
            with self.subTest(tipo=tipo.value):
                secao = CourseSection(type=tipo, value="", data=carga)
                self.assertEqual(secao.type, tipo)
                self.assertEqual(secao.value, "")

    def test_bloco_com_payload_sem_data_e_recusado(self):
        for tipo in PAYLOAD_SECTION_TYPES:
            with self.subTest(tipo=tipo.value):
                with self.assertRaises(ValidationError):
                    CourseSection(type=tipo, value="")

    def test_carga_com_forma_errada_e_recusada(self):
        with self.assertRaises(ValidationError):
            CourseSection(type=SectionType.DATA_TABLE, value="",
                          data={"columns": ["a", "b"]})

    def test_tabela_torta_e_recusada(self):
        """Linha com menos células que colunas desenha tabela quebrada."""
        torta = {"columns": ["a", "b", "c"], "rows": [["1", "2"]]}
        with self.assertRaises(ValidationError):
            CourseSection(type=SectionType.DATA_TABLE, value="", data=torta)

    def test_figura_precisa_de_conteudo_e_de_legenda(self):
        with self.assertRaises(ValidationError):
            CourseSection(type=SectionType.FIGURE, value="<svg/>")
        with self.assertRaises(ValidationError):
            CourseSection(type=SectionType.FIGURE, value="", label="Uma legenda")
        ok = CourseSection(type=SectionType.FIGURE, value="<svg/>", label="O funil")
        self.assertEqual(ok.label, "O funil")

    def test_bloco_de_prosa_vazio_e_recusado(self):
        for tipo in (SectionType.TEXT, SectionType.TIP, SectionType.WARNING):
            with self.subTest(tipo=tipo.value):
                with self.assertRaises(ValidationError):
                    CourseSection(type=tipo, value="   ")

    def test_prosa_continua_funcionando_sem_data(self):
        secao = CourseSection(type=SectionType.TEXT, value="Prosa com acentuação.")
        self.assertIsNone(secao.data)


class TestSchemaBateComOModelo(unittest.TestCase):
    """O schema JSON precisa dizer o mesmo que o Pydantic."""

    @classmethod
    def setUpClass(cls):
        with open(SCHEMA_PATH, encoding="utf-8") as f:
            cls.schema = json.load(f)
        cls.section = cls.schema["$defs"]["CourseSection"]

    def test_enum_do_schema_bate_com_o_enum_do_modelo(self):
        do_schema = set(self.section["properties"]["type"]["enum"])
        do_modelo = {t.value for t in SectionType}
        self.assertEqual(do_schema, do_modelo)

    def test_schema_tem_o_campo_data(self):
        self.assertIn("data", self.section["properties"])

    def test_value_nao_e_mais_obrigatoriamente_preenchido(self):
        """Bloco com payload nasce com `value` vazio, e o schema precisa deixar."""
        self.assertNotIn("minLength", self.section["properties"]["value"])

    def test_schema_cobra_data_em_cada_tipo_com_payload(self):
        cobrados = set()
        for regra in self.section.get("allOf", []):
            const = regra.get("if", {}).get("properties", {}).get("type", {}).get("const")
            if const and "data" in regra.get("then", {}).get("required", []):
                cobrados.add(const)
        self.assertEqual(cobrados, {t.value for t in PAYLOAD_SECTION_TYPES})

    def test_schema_e_modelo_concordam_nos_mesmos_casos(self):
        """A prova que importa: os dois validadores dão o mesmo veredito."""
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema não instalado neste ambiente")

        validador = jsonschema.Draft202012Validator(
            {"$defs": self.schema["$defs"], "$ref": "#/$defs/CourseSection"}
        )
        casos = [
            ({"type": "text", "value": "Prosa."}, True),
            ({"type": "dataTable", "value": "", "data": TABELA_OK}, True),
            ({"type": "dataTable", "value": ""}, False),
            ({"type": "comparison", "value": "", "data": COMPARATIVO_OK}, True),
            ({"type": "statGrid", "value": "", "data": PAINEL_OK}, True),
            ({"type": "stepGuide", "value": "", "data": GUIA_OK}, True),
            ({"type": "timeline", "value": "", "data": LINHA_DO_TEMPO_OK}, True),
            ({"type": "figure", "value": "<svg/>", "label": "O funil"}, True),
            ({"type": "figure", "value": "<svg/>"}, False),
        ]
        for instancia, esperado in casos:
            with self.subTest(caso=instancia["type"], esperado=esperado):
                pelo_schema = validador.is_valid(instancia)
                try:
                    CourseSection(**instancia)
                    pelo_modelo = True
                except ValidationError:
                    pelo_modelo = False
                self.assertEqual(pelo_schema, esperado)
                self.assertEqual(
                    pelo_modelo, esperado,
                    f"schema e modelo divergem em {instancia['type']}",
                )


if __name__ == "__main__":
    unittest.main()
