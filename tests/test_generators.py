"""Testes unitários para os geradores do curso-factory.

Valida a geração de page.tsx e layout.tsx a partir de CourseDefinition,
e testa os filtros Jinja2 customizados.
"""

import json
import sys
import unittest
from pathlib import Path

# Garante que o diretório raiz do projeto está no sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models import CourseDefinition
from src.generators import TsxGenerator


FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


def _load_sample_course() -> CourseDefinition:
    """Carrega o sample_course.json e retorna um CourseDefinition validado."""
    sample_path = FIXTURES_DIR / "sample_course.json"
    with open(sample_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return CourseDefinition(**data)


class TestTsxGenerator(unittest.TestCase):
    """Testes para o TsxGenerator."""

    def setUp(self) -> None:
        self.generator = TsxGenerator()
        self.course = _load_sample_course()

    def test_tsx_generator_renders_page(self) -> None:
        """Verifica que page.tsx é renderizado corretamente."""
        output = self.generator.render_page(self.course)

        # Deve conter a diretiva "use client"
        self.assertIn('"use client"', output)

        # Deve conter o nome do componente
        self.assertIn(self.course.component_name, output)

        # Deve conter a chave de localStorage
        self.assertIn(self.course.local_storage_key, output)

    def test_tsx_generator_renders_layout(self) -> None:
        """Verifica que layout.tsx é renderizado corretamente."""
        output = self.generator.render_layout(self.course)

        # Deve conter metadados SEO
        self.assertIn(self.course.titulo_seo, output)
        self.assertIn(self.course.canonical_url, output)

        # Deve conter o slug no nome do layout
        self.assertIn("Layout", output)

        # Deve conter keywords
        for kw in self.course.keywords_seo:
            self.assertIn(kw, output)

    def test_pascal_case_filter(self) -> None:
        """Testa a conversão de kebab-case para PascalCase."""
        from src.generators.tsx_generator import _pascal_case

        self.assertEqual(_pascal_case("meu-curso"), "MeuCurso")
        self.assertEqual(_pascal_case("geo-para-iniciantes"), "GeoParaIniciantes")
        self.assertEqual(_pascal_case("teste"), "Teste")
        self.assertEqual(_pascal_case("a-b-c"), "ABC")
        self.assertEqual(_pascal_case("curso-de-seo-avancado"), "CursoDeSeoAvancado")

    def test_js_escape_filter(self) -> None:
        """Testa o escape de caracteres para strings JavaScript."""
        from src.generators.tsx_generator import _js_escape

        self.assertEqual(_js_escape('texto com "aspas"'), 'texto com \\"aspas\\"')
        self.assertEqual(_js_escape("linha1\nlinha2"), "linha1\\nlinha2")
        self.assertEqual(_js_escape("barra\\invertida"), "barra\\\\invertida")
        self.assertEqual(_js_escape("sem problemas"), "sem problemas")

    def test_course_definition_computed_fields(self) -> None:
        """Verifica que os campos computados do CourseDefinition estão corretos."""
        self.assertEqual(self.course.slug, "teste-geracao")
        self.assertEqual(
            self.course.local_storage_key, "teste-geracao-course-progress"
        )
        self.assertEqual(
            self.course.canonical_url,
            "https://alexandrecaramaschi.com/educacao/teste-geracao",
        )
        self.assertEqual(self.course.component_name, "TesteGeracaoCoursePage")


if __name__ == "__main__":
    unittest.main()
