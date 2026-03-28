"""Modelos Pydantic para o curso-factory.

Define as estruturas de dados centrais: Step, Module, Course,
CostEntry e QualityReport.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


class NivelCurso(str, Enum):
    """Niveis possiveis para um curso."""
    INICIANTE = "iniciante"
    INTERMEDIARIO = "intermediario"
    AVANCADO = "avancado"


class Step(BaseModel):
    """Uma etapa individual dentro de um modulo."""
    titulo: str = Field(..., min_length=3, description="Titulo da etapa")
    conteudo: str = Field(default="", description="Conteudo textual da etapa")
    tipo: str = Field(default="texto", description="Tipo: texto, video, quiz, exercicio")
    duracao_minutos: int = Field(default=5, ge=1, le=120, description="Duracao estimada em minutos")

    @field_validator("titulo")
    @classmethod
    def titulo_nao_vazio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("O titulo da etapa nao pode ser vazio")
        return v.strip()


class Module(BaseModel):
    """Um modulo de curso, composto por etapas."""
    titulo: str = Field(..., min_length=3, description="Titulo do modulo")
    descricao: str = Field(default="", description="Descricao resumida do modulo")
    etapas: list[Step] = Field(default_factory=list, description="Lista de etapas do modulo")
    ordem: int = Field(default=1, ge=1, description="Ordem do modulo dentro do curso")

    @field_validator("titulo")
    @classmethod
    def titulo_nao_vazio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("O titulo do modulo nao pode ser vazio")
        return v.strip()


class Course(BaseModel):
    """Representacao completa de um curso."""
    id: str = Field(..., pattern=r"^[a-z0-9-]+$", description="Identificador unico (slug)")
    titulo: str = Field(..., min_length=5, description="Titulo do curso")
    descricao: str = Field(default="", description="Descricao do curso")
    nivel: NivelCurso = Field(default=NivelCurso.INICIANTE, description="Nivel de dificuldade")
    tags: list[str] = Field(default_factory=list, description="Tags de classificacao")
    pre_requisitos: list[str] = Field(default_factory=list, description="Pre-requisitos do curso")
    duracao_horas: Optional[float] = Field(default=None, ge=0.5, description="Duracao total estimada")
    modulos: list[Module] = Field(default_factory=list, description="Modulos do curso")

    @field_validator("id")
    @classmethod
    def id_sem_acentos(cls, v: str) -> str:
        """Garante que o ID/slug nao contenha caracteres acentuados."""
        import unicodedata
        nfkd = unicodedata.normalize("NFKD", v)
        if nfkd != v:
            raise ValueError(f"O ID do curso nao pode conter acentos: '{v}'")
        return v


class SectionType(str, Enum):
    """Tipos de seção de conteúdo dentro de um módulo."""
    TEXT = "text"
    CODE = "code"
    WARNING = "warning"
    TIP = "tip"
    CHECKPOINT = "checkpoint"


class CourseSection(BaseModel):
    """Uma seção de conteúdo dentro de um step/módulo."""
    type: SectionType
    value: str = Field(..., min_length=1, description="Conteúdo PT-BR com acentuação")
    language: Optional[str] = Field(default=None, description="Linguagem para blocos de código")
    label: Optional[str] = Field(default=None, description="Label opcional")


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

    # Author / Schema.org
    autor_nome: str = "Alexandre Caramaschi"
    autor_credencial: str = "CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil"
    dominio: str = "https://alexandrecaramaschi.com"
    badge_color: str = Field(default="#0176d3")

    # Computed
    local_storage_key: str = ""
    canonical_url: str = ""
    breadcrumb_label: str = ""
    component_name: str = ""

    def model_post_init(self, __context: Any) -> None:
        if not self.local_storage_key:
            self.local_storage_key = f"{self.slug}-course-progress"
        if not self.canonical_url:
            self.canonical_url = f"{self.dominio}/educacao/{self.slug}"
        if not self.breadcrumb_label:
            self.breadcrumb_label = self.titulo
        if not self.titulo_seo:
            self.titulo_seo = f"{self.titulo} | Curso Completo | Alexandre Caramaschi"
        if not self.descricao_curta:
            self.descricao_curta = self.descricao
        if not self.component_name:
            parts = self.slug.split("-")
            self.component_name = "".join(p.capitalize() for p in parts) + "CoursePage"


class CostEntry(BaseModel):
    """Registro de custo de uma chamada LLM."""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    provider: str = Field(..., description="Nome do provider LLM")
    model: str = Field(..., description="Modelo utilizado")
    tokens_in: int = Field(..., ge=0, description="Tokens de entrada")
    tokens_out: int = Field(..., ge=0, description="Tokens de saida")
    custo_usd: float = Field(..., ge=0.0, description="Custo estimado em USD")
    sessao: str = Field(default="default", description="Identificador da sessao")


class QualityReport(BaseModel):
    """Relatorio de qualidade gerado pelos validadores."""
    curso_id: str = Field(..., description="ID do curso avaliado")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    acentuacao_ok: bool = Field(default=False, description="Acentuacao PT-BR correta")
    html_ok: bool = Field(default=False, description="HTML valido")
    links_ok: bool = Field(default=False, description="Links validos e sem acentos")
    aprovado: bool = Field(default=False, description="Aprovado pelo quality gate")
    erros: list[str] = Field(default_factory=list, description="Lista de erros encontrados")
    avisos: list[str] = Field(default_factory=list, description="Lista de avisos")
