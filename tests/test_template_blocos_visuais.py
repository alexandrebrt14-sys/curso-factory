"""Testes do template page.tsx.j2 para os seis blocos visuais.

Cobre `figure`, `dataTable`, `comparison`, `statGrid`, `stepGuide` e
`timeline`: a marcação de cada um sai no TSX gerado, a carga sobrevive à
serialização com acentuação e aspas intactas, e nenhum bloco novo introduz cor
em hex, que é o defeito que some no tema escuro.
"""

import re
import sys
import unittest
from pathlib import Path

# Garante que o diretório raiz do projeto está no sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.generators import TsxGenerator
from src.models import CourseDefinition

#: Texto com acentuação completa e aspas duplas, para provar que a serialização
#: da carga não come acento nem quebra a string do TSX.
NOTA_COM_ASPAS = 'A régua exige "um bloco visual a cada 2.500 caracteres" de prosa.'

SECOES_BASE = [
    {
        "type": "text",
        "value": (
            "Este módulo mostra a diferença entre conteúdo que a IA cita e "
            "conteúdo que ela ignora, com verificação no navegador."
        ),
    },
    {
        "type": "code",
        "value": 'print("olá, mundo")',
        "language": "python",
    },
    {
        "type": "checkpoint",
        "value": "Você consegue explicar a diferença sem consultar a anotação.",
    },
]

SECOES_VISUAIS = [
    {
        "type": "figure",
        "value": (
            '<svg role="img" viewBox="0 0 120 40" xmlns="http://www.w3.org/2000/svg">'
            "<title>Fluxo da citação</title>"
            '<rect x="2" y="2" width="116" height="36" fill="var(--card)" '
            'stroke="var(--border)" />'
            '<text x="60" y="24" fill="var(--text)" text-anchor="middle">Índice</text>'
            "</svg>"
        ),
        "label": "Da página indexada à citação na resposta gerada.",
    },
    {
        "type": "dataTable",
        "data": {
            "title": "Comparação de canais",
            "columns": ["Canal", "Conversão"],
            "rows": [["Busca orgânica", "1,0x"], ["Resposta gerada", "4,4x"]],
            "source": "Medição interna, agosto de 2026",
            "note": NOTA_COM_ASPAS,
        },
    },
    {
        "type": "comparison",
        "data": {
            "title": "Como escrever a definição",
            "left": {
                "header": "Definição diluída",
                "items": ["Começa por história de fundação", "Adia a resposta"],
            },
            "right": {
                "header": "Definição direta",
                "items": ["Responde na primeira frase", "Traz o número com fonte"],
            },
            "leftChip": "Evite",
            "rightChip": "Recomendado",
        },
    },
    {
        "type": "statGrid",
        "data": {
            "title": "O tamanho do canal",
            "stats": [
                {"value": "4,4x", "label": "Conversão relativa", "sub": "Contra a busca clássica"},
                {"value": "62%", "label": "Respostas com citação", "sub": "Amostra de agosto"},
            ],
            "source": "Painel interno",
        },
    },
    {
        "type": "stepGuide",
        "data": {
            "title": "Publicar a página de definição",
            "intro": "A ordem importa: medir antes de publicar não prova nada.",
            "steps": [
                {
                    "label": "Escreva a definição em uma frase",
                    "detail": "Sem adjetivo e sem preâmbulo.",
                    "success": "A frase responde sozinha, fora de contexto.",
                    "pitfall": "Abrir com a história da empresa.",
                },
                {
                    "label": "Meça a página servida",
                    "detail": "Confira a frase nova presente e a antiga ausente.",
                    "success": "As duas contagens batem com o esperado.",
                    "pitfall": 'Contar com "grep -c" em HTML de uma linha.',
                },
            ],
            "outcome": "Uma página que a IA consegue citar sem reescrever.",
        },
    },
    {
        "type": "timeline",
        "data": {
            "title": "Marcos do canal generativo",
            "events": [
                {"date": "2023", "label": "Primeiras respostas geradas", "tone": "past"},
                {
                    "date": "2026",
                    "label": "Citação vira canal medido",
                    "detail": "O painel passa a separar tráfego por origem.",
                    "tone": "now",
                },
                {"date": "2027", "label": "Atribuição consolidada", "tone": "future"},
            ],
        },
    },
]

#: Regex de cor em hex. É o que a doutrina proíbe em bloco novo, porque hex
#: cravado some no tema escuro.
HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")


def _curso(secoes_extras: list[dict]) -> CourseDefinition:
    """Monta um curso de teste com as seções base mais as extras."""
    return CourseDefinition(
        slug="teste-blocos-visuais",
        titulo="Teste dos blocos visuais",
        descricao=(
            "Curso de teste para verificar a renderização dos seis blocos "
            "visuais no template TSX."
        ),
        steps=[
            {
                "id": "step-01",
                "title": "Blocos visuais do gerador",
                "duration": "20 min",
                "icon_key": "trendingUp",
                "description": "Cada bloco visual desenhado pelo template",
                "content": SECOES_BASE + secoes_extras,
            }
        ],
        autor_nome="Alexandre Caramaschi",
        autor_credencial="Founder da Brasil GEO",
        dominio="https://alexandrecaramaschi.com",
        company_name="Brasil GEO",
        company_description="Consultoria de GEO e SEO.",
    )


class TestBlocosVisuaisNoTemplate(unittest.TestCase):
    """O TSX gerado desenha os seis blocos visuais."""

    @classmethod
    def setUpClass(cls) -> None:
        gerador = TsxGenerator()
        cls.tsx = gerador.render_page(_curso(SECOES_VISUAIS))
        cls.tsx_base = gerador.render_page(_curso([]))

    def test_os_seis_tipos_aparecem_no_array_de_secoes(self) -> None:
        """Cada tipo novo sai na estrutura STEPS, e não engolido pelo default."""
        for tipo in (
            "figure",
            "dataTable",
            "comparison",
            "statGrid",
            "stepGuide",
            "timeline",
        ):
            with self.subTest(tipo=tipo):
                self.assertIn(f'type: "{tipo}"', self.tsx)

    def test_cada_bloco_tem_case_e_componente_proprio(self) -> None:
        """O switch trata os seis tipos, cada um com o seu componente."""
        pares = {
            "figure": "FigureBlock",
            "dataTable": "DataTableBlock",
            "comparison": "ComparisonBlock",
            "statGrid": "StatGridBlock",
            "stepGuide": "StepGuideBlock",
            "timeline": "TimelineBlock",
        }
        for tipo, componente in pares.items():
            with self.subTest(tipo=tipo):
                self.assertIn(f'case "{tipo}":', self.tsx)
                self.assertIn(f"function {componente}(", self.tsx)
                # O case precisa devolver o componente, nunca cair no default.
                trecho = self.tsx.split(f'case "{tipo}":', 1)[1]
                trecho = re.split(r"\n\s*(?:case |default:)", trecho, maxsplit=1)[0]
                self.assertIn(f"<{componente}", trecho)
                self.assertNotIn("return null;", trecho)

    def test_figura_tem_figure_e_figcaption(self) -> None:
        """A figura desenha `<figure>` com legenda, e a legenda vem do label."""
        self.assertIn("<figure", self.tsx)
        self.assertIn("<figcaption", self.tsx)
        self.assertIn("Da página indexada à citação na resposta gerada.", self.tsx)

    def test_tabela_rola_sozinha_no_celular(self) -> None:
        """O contêiner da tabela rola na horizontal em vez de esticar a página."""
        self.assertIn("overflow-x-auto", self.tsx)
        self.assertIn("<table", self.tsx)
        self.assertIn("<thead", self.tsx)
        self.assertIn("<tbody", self.tsx)
        # O contêiner limita a largura, então a página não rola junto.
        self.assertIn("max-w-full overflow-x-auto", self.tsx)

    def test_comparativo_mantem_a_valencia_dos_lados(self) -> None:
        """`left` é o lado a evitar e `right` o recomendado, com cor coerente."""
        corpo = self.tsx.split("function ComparisonBlock(", 1)[1].split(
            "function StatGridBlock(", 1
        )[0]
        self.assertLess(
            corpo.index("data.left.header"),
            corpo.index("data.right.header"),
            "O lado a evitar vem primeiro",
        )

        # Cada painel é medido isolado, pelo comentário que o abre.
        lado_evitar = corpo.split("{/* Lado a evitar */}", 1)[1].split(
            "{/* Lado recomendado */}", 1
        )[0]
        lado_recomendado = corpo.split("{/* Lado recomendado */}", 1)[1]
        self.assertIn("data.left.header", lado_evitar)
        self.assertIn("data.right.header", lado_recomendado)
        # O lado a evitar usa o token de perigo e o ícone de recusa.
        self.assertIn("var(--danger)", lado_evitar)
        self.assertIn("icons.circleX", lado_evitar)
        self.assertNotIn("var(--success)", lado_evitar)
        # O lado recomendado usa o token de sucesso e o ícone de acerto.
        self.assertIn("var(--success)", lado_recomendado)
        self.assertIn("icons.circleCheck", lado_recomendado)
        self.assertNotIn("var(--danger)", lado_recomendado)
        # Empilha no celular e fica lado a lado a partir do desktop.
        self.assertIn("grid-cols-1 md:grid-cols-2", corpo)

    def test_painel_de_numeros_hierarquiza_valor_rotulo_e_sub(self) -> None:
        """O `value` é o maior, o `label` vem abaixo e o `sub` é o menor."""
        corpo = self.tsx.split("function StatGridBlock(", 1)[1].split(
            "function StepGuideBlock(", 1
        )[0]
        self.assertLess(corpo.index("stat.value"), corpo.index("stat.label"))
        self.assertLess(corpo.index("stat.label"), corpo.index("stat.sub"))
        self.assertIn("text-[28px]", corpo)

    def test_guia_distingue_detalhe_sucesso_e_armadilha(self) -> None:
        """Os três campos do passo saem com marcação distinta entre si."""
        corpo = self.tsx.split("function StepGuideBlock(", 1)[1].split(
            "function TimelineBlock(", 1
        )[0]
        self.assertIn("step.detail", corpo)
        self.assertIn("step.success", corpo)
        self.assertIn("step.pitfall", corpo)
        self.assertIn("data.outcome", corpo)
        # Sucesso e armadilha não podem compartilhar cor.
        bloco_sucesso = corpo.split("step.success", 1)[1].split("step.pitfall", 1)[0]
        bloco_armadilha = corpo.split("step.pitfall", 1)[1]
        self.assertIn("var(--success)", bloco_sucesso)
        self.assertIn("var(--danger)", bloco_armadilha)
        # Os passos são numerados pela posição.
        self.assertIn("{i + 1}", corpo)

    def test_linha_do_tempo_muda_a_marcacao_por_tom(self) -> None:
        """`past`, `now` e `future` produzem marcação diferente."""
        corpo = self.tsx.split("function TimelineBlock(", 1)[1]
        self.assertIn('tone === "now"', corpo)
        self.assertIn('tone === "future"', corpo)
        self.assertIn("event.date", corpo)
        self.assertIn("event.label", corpo)
        self.assertIn("event.detail", corpo)

    def test_acentuacao_e_aspas_sobrevivem_a_serializacao(self) -> None:
        """A carga chega ao TSX com acento literal e aspas escapadas."""
        # Acentuação literal, sem virar sequência \\u00XX.
        self.assertIn("Comparação de canais", self.tsx)
        self.assertIn("Medição interna, agosto de 2026", self.tsx)
        self.assertIn("Definição diluída", self.tsx)
        self.assertIn("Citação vira canal medido", self.tsx)
        self.assertNotIn("\\u00e7", self.tsx)
        self.assertNotIn("\\u00E7", self.tsx)

        # Aspas duplas dentro da carga saem escapadas, e a string não quebra.
        self.assertIn(
            'A régua exige \\"um bloco visual a cada 2.500 caracteres\\" de prosa.',
            self.tsx,
        )
        self.assertIn('Contar com \\"grep -c\\" em HTML de uma linha.', self.tsx)

        # A serialização é um literal de objeto, não uma string solta.
        self.assertIn('data: {"title": "Comparação de canais"', self.tsx)

    def test_carga_serializada_e_javascript_valido(self) -> None:
        """Cada `data:` do array STEPS é um literal de objeto balanceado."""
        cargas = re.findall(r"\bdata: (\{.*?\}) \},\n", self.tsx)
        self.assertEqual(len(cargas), 5, "Cinco blocos com carga em `data`")
        for carga in cargas:
            with self.subTest(carga=carga[:40]):
                self.assertEqual(carga.count("{"), carga.count("}"))
                # Aspas não escapadas só delimitam chave e valor: fora delas,
                # nenhuma sobra ímpar.
                sem_escape = carga.replace('\\"', "")
                self.assertEqual(sem_escape.count('"') % 2, 0)

    def test_blocos_novos_nao_introduzem_cor_em_hex(self) -> None:
        """Nenhum hex novo entra no TSX por causa dos blocos visuais."""
        hex_base = set(HEX_RE.findall(self.tsx_base))
        hex_visual = set(HEX_RE.findall(self.tsx))
        novos = hex_visual - hex_base
        self.assertEqual(
            novos,
            set(),
            f"Os blocos visuais introduziram cor em hex: {sorted(novos)}",
        )

    def test_blocos_novos_pintam_por_token(self) -> None:
        """Os componentes novos usam token CSS, e `--surface` não existe."""
        inicio = self.tsx.index("/* ───────── BLOCOS VISUAIS ───────── */")
        fim = self.tsx.index("/* ───────── COMPONENT: StepCard ───────── */")
        corpo = self.tsx[inicio:fim]
        for token in ("var(--text)", "var(--border)", "var(--card)", "var(--accent)"):
            with self.subTest(token=token):
                self.assertIn(token, corpo)
        self.assertNotIn("var(--surface)", corpo)
        self.assertEqual(HEX_RE.findall(corpo), [])


if __name__ == "__main__":
    unittest.main()
