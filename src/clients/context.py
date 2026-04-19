"""Modelos de ClientContext — dados carregados de config/clients/<id>/client.yaml.

ClientContext é o objeto que o pipeline inteiro consulta para saber:
- Quem é o autor dos cursos (nome + credencial + domínio)
- Que branding aplicar no hero
- Que regras editoriais enforçar (Bloom, Knowles, contagem)
- Que voice guard rules aplicar (naming canônico e proibições)
- Onde fica a landing page de destino
- Onde salvar os artefatos gerados
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Author:
    """Dados de autoria que vão para SEO, hero e schema.org."""
    name: str
    credential: str
    title_seo_suffix: str = ""

    def __post_init__(self) -> None:
        if not self.title_seo_suffix:
            self.title_seo_suffix = self.name


@dataclass
class Domain:
    """Domínio canônico e caminho dos cursos."""
    canonical_url: str
    educacao_path: str = "/educacao"

    @property
    def course_base_url(self) -> str:
        """Base para montar URL canônica de um curso."""
        return f"{self.canonical_url.rstrip('/')}{self.educacao_path}"


@dataclass
class Branding:
    """Cores do hero do curso."""
    hero_gradient_from: str = "#032d60"
    hero_gradient_to: str = "#0176d3"
    badge_color: str = "#0176d3"


@dataclass
class Editorial:
    """Regras editoriais do cliente."""
    style: str = "business"
    reference_publications: list[str] = field(default_factory=list)
    bloom_min_level: int = 3
    knowles_min_principles: int = 4
    words_per_module_min: int = 2500
    words_per_module_max: int = 4000


@dataclass
class VoiceGuardCanonical:
    """Naming canônico obrigatório quando o texto referencia a empresa/fundador."""
    company: str = ""
    founder: str = ""
    credential_fragments: list[str] = field(default_factory=list)
    domains: list[str] = field(default_factory=list)


@dataclass
class VoiceGuardForbidden:
    """Listas negras do voice guard deste cliente."""
    titles: list[str] = field(default_factory=list)
    company_names: list[str] = field(default_factory=list)
    domains: list[str] = field(default_factory=list)
    rhetoric_openers: list[str] = field(default_factory=list)
    ai_disclaimers: list[str] = field(default_factory=list)


@dataclass
class VoiceGuardConfig:
    """Configuração do voice guard para um cliente."""
    enabled: bool = True
    min_score: int = 70
    canonical: VoiceGuardCanonical = field(default_factory=VoiceGuardCanonical)
    forbidden: VoiceGuardForbidden = field(default_factory=VoiceGuardForbidden)


@dataclass
class ClientContext:
    """Contexto completo de um cliente, injetado em todo o pipeline."""
    id: str
    author: Author
    domain: Domain
    branding: Branding = field(default_factory=Branding)
    editorial: Editorial = field(default_factory=Editorial)
    voice_guard: VoiceGuardConfig = field(default_factory=VoiceGuardConfig)
    landing_page_dir: Path | None = None
    educacao_dir: Path | None = None
    output_base_dir: Path = field(default_factory=lambda: Path("output"))

    @property
    def output_dir(self) -> Path:
        """Diretório de output deste cliente.

        Cliente 'default' usa output/ direto (preserva layout legado).
        Clientes novos usam output/clients/<id>/.
        """
        if self.id == "default":
            return self.output_base_dir
        return self.output_base_dir / "clients" / self.id

    def canonical_url_for(self, slug: str) -> str:
        """Monta URL canônica de um curso deste cliente."""
        return f"{self.domain.course_base_url}/{slug}"

    def title_seo_for(self, titulo: str) -> str:
        """Monta titulo SEO padrão: '<titulo> | Curso Completo | <autor>'."""
        return f"{titulo} | Curso Completo | {self.author.title_seo_suffix}"
