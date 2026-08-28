"""Modelos Pydantic para o curso-factory.

Define as estruturas de dados centrais: Step, Module, Course,
CostEntry e QualityReport.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator


def _now_utc() -> datetime:
    """Wall-clock UTC; substitui datetime.utcnow() (deprecated em 3.12)."""
    return datetime.now(UTC)


class NivelCurso(str, Enum):
    """Níveis possíveis para um curso."""
    INICIANTE = "iniciante"
    INTERMEDIARIO = "intermediário"
    AVANCADO = "avançado"


class Step(BaseModel):
    """Uma etapa individual dentro de um módulo."""
    titulo: str = Field(..., min_length=3, description="Título da etapa")
    conteudo: str = Field(default="", description="Conteúdo textual da etapa")
    tipo: str = Field(default="texto", description="Tipo: texto, vídeo, quiz, exercício")
    duracao_minutos: int = Field(default=5, ge=1, le=120, description="Duração estimada em minutos")
    # Wave 6 (engagement): chave estável para SRS quando o step ensina conceito
    concept_id: str | None = Field(default=None, description="ID do conceito para SRS")
    # Wave 6 (engagement): payload de quiz quando tipo=='quiz'
    quiz_payload: dict | None = Field(default=None, description="Quiz inline opcional")

    @field_validator("titulo")
    @classmethod
    def titulo_nao_vazio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("O título da etapa não pode ser vazio")
        return v.strip()


class Module(BaseModel):
    """Um módulo de curso, composto por etapas."""
    titulo: str = Field(..., min_length=3, description="Título do módulo")
    descricao: str = Field(default="", description="Descrição resumida do módulo")
    etapas: list[Step] = Field(default_factory=list, description="Lista de etapas do módulo")
    ordem: int = Field(default=1, ge=1, description="Ordem do módulo dentro do curso")
    # Wave 6 (engagement): conceitos que viram cartões SRS ao concluir o módulo
    srs_concepts: list[str] = Field(default_factory=list, description="Conceitos para revisão espaçada")

    @field_validator("titulo")
    @classmethod
    def titulo_nao_vazio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("O título do módulo não pode ser vazio")
        return v.strip()


class Course(BaseModel):
    """Representação completa de um curso."""
    id: str = Field(..., pattern=r"^[a-z0-9-]+$", description="Identificador único (slug)")
    titulo: str = Field(..., min_length=5, description="Título do curso")
    descricao: str = Field(default="", description="Descrição do curso")
    nivel: NivelCurso = Field(default=NivelCurso.INICIANTE, description="Nível de dificuldade")
    tags: list[str] = Field(default_factory=list, description="Tags de classificação")
    pre_requisitos: list[str] = Field(default_factory=list, description="Pré-requisitos do curso")
    duracao_horas: float | None = Field(default=None, ge=0.5, description="Duração total estimada")
    modulos: list[Module] = Field(default_factory=list, description="Módulos do curso")
    # Wave 8 (i18n): idioma do curso. Fallback "pt-br" mantém compat.
    language: str = Field(default="pt-br", description="Idioma do curso (pt-br | en | es | ...)")
    # Wave 6 (engagement): badges que o curso destrava
    badges_alvo: list[str] = Field(default_factory=list, description="IDs do catálogo de badges")
    # Wave 9 (skill graph): skills tagueadas com schema.org URIs
    skills: list[str] = Field(default_factory=list, description="Schema.org/Skill IDs")

    @field_validator("id")
    @classmethod
    def id_sem_acentos(cls, v: str) -> str:
        """Garante que o ID/slug não contenha caracteres acentuados."""
        import unicodedata
        nfkd = unicodedata.normalize("NFKD", v)
        if nfkd != v:
            raise ValueError(f"O ID do curso não pode conter acentos: '{v}'")
        return v


class SectionType(str, Enum):
    """Tipos de seção de conteúdo dentro de um módulo.

    Os cinco primeiros carregam prosa ou código no campo `value`. Os seis
    seguintes são blocos visuais, com carga tipada em `data`, e existem para
    cumprir a doutrina de peso visual (`docs/DOUTRINA_VISUAL_CURSOS.md`):
    nenhum curso nasce como coluna de texto.

    As formas de payload são as do motor de cursos do `landing-page-geo`
    (`src/types/course-page.ts`). Curso gerado aqui é montado lá, então
    divergir de campo ou de opcionalidade quebra a montagem.
    """
    TEXT = "text"
    CODE = "code"
    WARNING = "warning"
    TIP = "tip"
    CHECKPOINT = "checkpoint"
    # Blocos visuais. Carga em `data`, e `value` fica vazio.
    FIGURE = "figure"
    DATA_TABLE = "dataTable"
    COMPARISON = "comparison"
    STAT_GRID = "statGrid"
    STEP_GUIDE = "stepGuide"
    TIMELINE = "timeline"


#: Tipos que produzem alívio visual. Espelha o conjunto VISUAL do portão
#: `scripts/gate-peso-visual.mjs` do `landing-page-geo`.
VISUAL_SECTION_TYPES: frozenset[SectionType] = frozenset({
    SectionType.FIGURE,
    SectionType.DATA_TABLE,
    SectionType.COMPARISON,
    SectionType.STAT_GRID,
    SectionType.STEP_GUIDE,
    SectionType.TIMELINE,
})

#: Tipos cuja carga vive em `data` e cujo `value` fica vazio de propósito.
PAYLOAD_SECTION_TYPES: frozenset[SectionType] = frozenset({
    SectionType.DATA_TABLE,
    SectionType.COMPARISON,
    SectionType.STAT_GRID,
    SectionType.STEP_GUIDE,
    SectionType.TIMELINE,
})


class DataTablePayload(BaseModel):
    """Tabela de dados. Alternativas nas colunas e critério nas linhas."""
    title: str | None = None
    columns: list[str] = Field(..., min_length=2)
    rows: list[list[str]] = Field(..., min_length=1)
    source: str | None = None
    note: str | None = None

    @field_validator("rows")
    @classmethod
    def validate_rows(cls, v: list[list[str]], info) -> list[list[str]]:
        colunas = info.data.get("columns")
        if not colunas:
            return v
        for i, linha in enumerate(v):
            if len(linha) != len(colunas):
                raise ValueError(
                    f"A linha {i + 1} tem {len(linha)} célula(s) para "
                    f"{len(colunas)} coluna(s). Tabela torta não renderiza."
                )
        return v


class ComparisonSide(BaseModel):
    """Um lado do comparativo."""
    header: str = Field(..., min_length=2)
    items: list[str] = Field(..., min_length=1)


class ComparisonPayload(BaseModel):
    """Comparativo de dois lados, com valência FIXA.

    `left` é sempre o lado a evitar e `right` é sempre o recomendado. Inverter
    carimba um certo justamente no que o texto manda descartar.
    """
    title: str = Field(..., min_length=3)
    left: ComparisonSide
    right: ComparisonSide
    leftChip: str | None = None
    rightChip: str | None = None


class StatItem(BaseModel):
    """Um número do painel, com o rótulo que o explica."""
    value: str = Field(..., min_length=1)
    label: str = Field(..., min_length=2)
    sub: str | None = None


class StatGridPayload(BaseModel):
    """Painel de números que só fazem sentido juntos."""
    title: str | None = None
    stats: list[StatItem] = Field(..., min_length=2)
    source: str | None = None


class StepGuideStep(BaseModel):
    """Um passo do guia, com o que se vê quando dá certo."""
    label: str = Field(..., min_length=3)
    detail: str | None = None
    success: str | None = None
    pitfall: str | None = None


class StepGuidePayload(BaseModel):
    """Passo a passo numerado, para processo em que a ordem importa."""
    title: str = Field(..., min_length=3)
    intro: str | None = None
    steps: list[StepGuideStep] = Field(..., min_length=2)
    outcome: str | None = None


class TimelineEvent(BaseModel):
    """Um marco da linha do tempo."""
    date: str = Field(..., min_length=1)
    label: str = Field(..., min_length=2)
    detail: str | None = None
    tone: Literal["past", "now", "future"] | None = None


class TimelinePayload(BaseModel):
    """Linha do tempo de marcos datados."""
    title: str | None = None
    events: list[TimelineEvent] = Field(..., min_length=2)


#: Mapeia cada tipo com payload ao modelo que o valida.
PAYLOAD_MODELS: dict[SectionType, type[BaseModel]] = {
    SectionType.DATA_TABLE: DataTablePayload,
    SectionType.COMPARISON: ComparisonPayload,
    SectionType.STAT_GRID: StatGridPayload,
    SectionType.STEP_GUIDE: StepGuidePayload,
    SectionType.TIMELINE: TimelinePayload,
}


class CourseSection(BaseModel):
    """Uma seção de conteúdo dentro de um step/módulo.

    Bloco de prosa ou de código carrega o conteúdo em `value`. Bloco visual com
    payload carrega em `data` e deixa `value` vazio, que é como o motor da
    landing espera. O bloco `figure` é a exceção entre os visuais: o SVG ou a
    marcação da imagem vai no `value` e a legenda vai em `label`.
    """
    type: SectionType
    value: str = Field(default="", description="Conteúdo PT-BR com acentuação")
    language: str | None = Field(default=None, description="Linguagem para blocos de código")
    label: str | None = Field(default=None, description="Label opcional")
    data: dict | None = Field(default=None, description="Carga tipada dos blocos visuais")

    @model_validator(mode="after")
    def validate_carga(self) -> "CourseSection":
        """Cobra a carga certa para cada tipo, e recusa bloco que sairia vazio.

        O motor da landing degrada bloco sem `data` para nada, sem erro e sem
        registro no console. É a falha mais silenciosa que ele tem, e o lugar
        de pegá-la é aqui, na geração.
        """
        if self.type in PAYLOAD_SECTION_TYPES:
            if not self.data:
                raise ValueError(
                    f"O bloco '{self.type.value}' precisa de `data`. Sem ele, "
                    "a página renderiza nada e não avisa."
                )
            modelo = PAYLOAD_MODELS[self.type]
            try:
                modelo.model_validate(self.data)
            except ValidationError as e:
                raise ValueError(
                    f"A carga do bloco '{self.type.value}' não bate com "
                    f"{modelo.__name__}: {e}"
                ) from e
            return self

        if self.type is SectionType.FIGURE:
            if not self.value.strip():
                raise ValueError(
                    "O bloco 'figure' precisa do SVG ou da imagem em `value`."
                )
            if not (self.label or "").strip():
                raise ValueError(
                    "O bloco 'figure' precisa de legenda em `label`. Figura sem "
                    "legenda não diz o que mostra."
                )
            return self

        if not self.value.strip():
            raise ValueError(
                f"O bloco '{self.type.value}' precisa de conteúdo em `value`."
            )
        return self


class StepDefinition(BaseModel):
    """Definição de um step/módulo para geração de TSX."""
    id: str = Field(..., pattern=r"^[a-z0-9-]+$", description="ID ASCII kebab-case")
    title: str = Field(..., min_length=3, description="Título PT-BR com acentos")
    duration: str = Field(..., pattern=r"^\d+ min$", description="Duração ex: '18 min'")
    icon_key: str = Field(default="trendingUp", description="Chave do ícone SVG")
    description: str = Field(..., min_length=5, description="Descrição em uma linha")
    content: list[CourseSection] = Field(default_factory=list)

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: list[CourseSection]) -> list[CourseSection]:
        if len(v) < 3:
            raise ValueError("Cada step precisa de pelo menos 3 seções de conteúdo")
        types = [s.type for s in v]
        if SectionType.CHECKPOINT not in types:
            raise ValueError("Cada step precisa de pelo menos 1 checkpoint")
        return v


class FAQItem(BaseModel):
    """Pergunta e resposta para FAQ do curso."""
    pergunta: str = Field(..., min_length=5)
    resposta: str = Field(..., min_length=10)


class CourseDefinition(BaseModel):
    """Modelo completo para geração determinística de layout.tsx + page.tsx."""
    # Identity
    slug: str = Field(..., pattern=r"^[a-z0-9-]+$", description="Slug ASCII para URL")
    titulo: str = Field(..., min_length=5, description="Título PT-BR")
    titulo_seo: str = Field(default="", description="Título para tag <title>")
    descricao: str = Field(..., min_length=20, description="Meta description")
    descricao_curta: str = Field(default="", description="Subtítulo do hero")

    # Classification
    nivel: NivelCurso = NivelCurso.INTERMEDIARIO
    nivel_display: str = Field(default="Intermediário")
    tags: list[str] = Field(default_factory=list)
    keywords_seo: list[str] = Field(default_factory=list)

    # Timing
    duracao_total_minutos: int = Field(default=180, ge=30)
    duracao_display: str = Field(default="~180 min")

    # Content
    steps: list[StepDefinition] = Field(default_factory=list)
    prerequisitos_display: list[str] = Field(default_factory=list)
    faq: list[FAQItem] = Field(default_factory=list)

    # Hero
    hero_gradient_from: str = Field(default="#032d60")
    hero_gradient_to: str = Field(default="#0176d3")

    # Author / Schema.org — injetados pelo ClientContext via SchemaBuilder.
    # Sem defaults com identidade — quem instancia CourseDefinition precisa
    # passar os campos do cliente. Isso garante que nenhuma identidade vaza
    # entre clientes por engano.
    autor_nome: str = ""
    autor_credencial: str = ""
    dominio: str = ""
    educacao_path: str = "/educacao"
    company_name: str = ""
    company_description: str = ""
    badge_color: str = Field(default="#0176d3")

    # Computed
    local_storage_key: str = ""
    canonical_url: str = ""
    breadcrumb_label: str = ""
    component_name: str = ""

    def model_post_init(self, __context: Any) -> None:
        if not self.local_storage_key:
            self.local_storage_key = f"{self.slug}-course-progress"
        if not self.canonical_url and self.dominio:
            dominio_norm = self.dominio.rstrip("/")
            path_norm = self.educacao_path if self.educacao_path.startswith("/") else f"/{self.educacao_path}"
            self.canonical_url = f"{dominio_norm}{path_norm}/{self.slug}"
        if not self.breadcrumb_label:
            self.breadcrumb_label = self.titulo
        if not self.titulo_seo:
            sufixo = self.autor_nome or self.company_name or "Curso Completo"
            self.titulo_seo = f"{self.titulo} | Curso Completo | {sufixo}"
        if not self.descricao_curta:
            self.descricao_curta = self.descricao
        if not self.component_name:
            parts = self.slug.split("-")
            self.component_name = "".join(p.capitalize() for p in parts) + "CoursePage"


class CostEntry(BaseModel):
    """Registro de custo de uma chamada LLM."""
    timestamp: datetime = Field(default_factory=_now_utc)
    provider: str = Field(..., description="Nome do provider LLM")
    model: str = Field(..., description="Modelo utilizado")
    tokens_in: int = Field(..., ge=0, description="Tokens de entrada")
    tokens_out: int = Field(..., ge=0, description="Tokens de saída")
    custo_usd: float = Field(..., ge=0.0, description="Custo estimado em USD")
    sessao: str = Field(default="default", description="Identificador da sessão")


class QualityReport(BaseModel):
    """Relatório de qualidade gerado pelos validadores."""
    curso_id: str = Field(..., description="ID do curso avaliado")
    timestamp: datetime = Field(default_factory=_now_utc)
    acentuacao_ok: bool = Field(default=False, description="Acentuação PT-BR correta")
    html_ok: bool = Field(default=False, description="HTML válido")
    links_ok: bool = Field(default=False, description="Links válidos e sem acentos")
    aprovado: bool = Field(default=False, description="Aprovado pelo quality gate")
    erros: list[str] = Field(default_factory=list, description="Lista de erros encontrados")
    avisos: list[str] = Field(default_factory=list, description="Lista de avisos")
