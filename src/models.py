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
    duracao_horas: Optional[float] = Field(default=None, ge=0.5, description="Duração total estimada")
    modulos: list[Module] = Field(default_factory=list, description="Módulos do curso")

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

    # Author / Schema.org — injetados pelo ClientContext via SchemaBuilder.
    # Defaults mantidos apenas para compatibilidade com fixtures antigas;
    # em uso real, SchemaBuilder.build(client=...) sobrescreve.
    autor_nome: str = "Alexandre Caramaschi"
    autor_credencial: str = "CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil"
    dominio: str = "https://alexandrecaramaschi.com"
    educacao_path: str = "/educacao"
    # Empresa — schema.org provider e bloco de autoria
    company_name: str = "Brasil GEO"
    company_description: str = (
        "Este curso faz parte do material educacional da Brasil GEO, empresa "
        "brasileira especializada em Generative Engine Optimization. Para dúvidas, "
        "entre em contato pelo WhatsApp ou LinkedIn."
    )
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
            dominio_norm = self.dominio.rstrip("/")
            path_norm = self.educacao_path if self.educacao_path.startswith("/") else f"/{self.educacao_path}"
            self.canonical_url = f"{dominio_norm}{path_norm}/{self.slug}"
        if not self.breadcrumb_label:
            self.breadcrumb_label = self.titulo
        if not self.titulo_seo:
            autor = self.autor_nome or "Curso"
            self.titulo_seo = f"{self.titulo} | Curso Completo | {autor}"
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
    tokens_out: int = Field(..., ge=0, description="Tokens de saída")
    custo_usd: float = Field(..., ge=0.0, description="Custo estimado em USD")
    sessao: str = Field(default="default", description="Identificador da sessão")


class QualityReport(BaseModel):
    """Relatório de qualidade gerado pelos validadores."""
    curso_id: str = Field(..., description="ID do curso avaliado")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    acentuacao_ok: bool = Field(default=False, description="Acentuação PT-BR correta")
    html_ok: bool = Field(default=False, description="HTML válido")
    links_ok: bool = Field(default=False, description="Links válidos e sem acentos")
    aprovado: bool = Field(default=False, description="Aprovado pelo quality gate")
    erros: list[str] = Field(default_factory=list, description="Lista de erros encontrados")
    avisos: list[str] = Field(default_factory=list, description="Lista de avisos")
