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
class Company:
    """Dados da empresa que aparecem como `provider` em schema.org e no bloco
    de autoria do curso."""
    name: str = ""
    description: str = ""


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
class TutorConfig:
    """Wave 7 — configuração do Tutor IA conversacional (runtime).

    Tutor é o 6º agente que vive no servidor, fora do pipeline de geração.
    Aluno conversa com tutor que sabe tudo sobre o curso atual.
    """
    enabled: bool = False
    persona: str = "curiosa-paciente"
    name: str = ""
    model: str = "claude-haiku-4-5-20251001"
    budget_per_user_per_month: float = 2.0
    daily_budget: float = 10.0


@dataclass
class EngagementConfig:
    """Wave 6 — configuração da camada de engajamento."""
    gamification_enabled: bool = False
    streak_enabled: bool = True
    badges_enabled: bool = True
    leagues_enabled: bool = False
    srs_enabled: bool = True
    srs_interval_initial_days: int = 1
    quiz_pass_threshold: float = 0.7


@dataclass
class CertificationConfig:
    """Wave 9 — configuração de certificação."""
    enabled: bool = False
    pass_threshold: float = 0.7
    blockchain_opt_in: bool = False
    linkedin_integration: bool = False


@dataclass
class AgenticConfig:
    """Wave 10 — configuração de agent legibility (llms.txt + MCP/A2A)."""
    enabled: bool = False
    emit_llms_txt: bool = True
    mcp_server: bool = False
    a2a_endpoints: bool = False


@dataclass
class ClientContext:
    """Contexto completo de um cliente, injetado em todo o pipeline."""
    id: str
    author: Author
    domain: Domain
    company: Company = field(default_factory=Company)
    branding: Branding = field(default_factory=Branding)
    editorial: Editorial = field(default_factory=Editorial)
    voice_guard: VoiceGuardConfig = field(default_factory=VoiceGuardConfig)
    landing_page_dir: Path | None = None
    educacao_dir: Path | None = None
    output_base_dir: Path = field(default_factory=lambda: Path("output"))
    # Wave 6-10 — features opcionais (default off; ligar via client.yaml)
    tutor: TutorConfig = field(default_factory=TutorConfig)
    engagement: EngagementConfig = field(default_factory=EngagementConfig)
    certification: CertificationConfig = field(default_factory=CertificationConfig)
    agentic: AgenticConfig = field(default_factory=AgenticConfig)
    # Wave 8 — idioma default do cliente (override per curso possível)
    language: str = "pt-br"

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
