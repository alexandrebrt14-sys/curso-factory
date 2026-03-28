"""Modelos Pydantic para o curso-factory.

Define as estruturas de dados centrais: Step, Module, Course,
CostEntry e QualityReport.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

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
