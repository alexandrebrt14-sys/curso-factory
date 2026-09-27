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
class VoiceSample:
    """Amostra real de escrita do autor canônico para few-shot persona-conditioning.

    A amostra é injetada antes do `{context}` no prompt do redator/revisor para
    ancorar idiossincrasias linguísticas reais. Sem amostras, o LLM produz
    "voz HBR genérica" — detectável estatisticamente por uniformidade de
    estilo. Com 800-1500 palavras de anchor por amostra, a saída herda
    cadência, vocabulário e construções típicas do autor.

    Referência: Liang et al. Patterns 2023 mostram que reescrita "no estilo X"
    derruba detecção a ~0%. DIPPER (Krishna NeurIPS 2023) confirma que
    persona-conditioning supera fine-tuning para volumes pequenos.
    """

    path: str
    length_words: int = 0
    tags: list[str] = field(default_factory=list)


@dataclass
class VoiceSamplesConfig:
    """Configuração de amostras de voz para persona-conditioning few-shot."""

    enabled: bool = False
    samples: list[VoiceSample] = field(default_factory=list)
    anchor_strategy: str = "rotate"  # rotate | concat | random
    anchor_max_words: int = 2000


@dataclass
class VoiceGuardConfig:
    """Configuração do voice guard para um cliente."""

    enabled: bool = True
    min_score: int = 70
    canonical: VoiceGuardCanonical = field(default_factory=VoiceGuardCanonical)
    forbidden: VoiceGuardForbidden = field(default_factory=VoiceGuardForbidden)
    voice_samples: VoiceSamplesConfig = field(default_factory=VoiceSamplesConfig)


@dataclass
class DisclosureConfig:
    """Disclosure programático de uso de IA — PL 2338/2023 (Brasil) + EEAT Google.

    Em curso para cliente brasileiro com `required_by` incluindo
    'PL_2338_2023', o pipeline injeta bloco padronizado no rodapé de cada
    módulo. Validator `disclosure_checker.py` bloqueia publicação se ausente.

    Para clientes em domínios regulados (saúde, psicologia, direito),
    `reviewer_extra` lista credenciais humanas obrigatórias
    (psicólogo CRP, médico CRM, advogado OAB).

    Referências regulatórias:
    - PL 2338/2023 (Marco Legal IA Brasil) — disclosure mandatório
    - CFP Posicionamento 03/07/2025 — IA em conteúdo psicológico exige
      supervisão e disclosure
    - MEC Marco Referencial 2025-07 — IA na Educação Básica
    """

    enabled: bool = False
    required_by: list[str] = field(default_factory=list)
    pipeline_models: list[str] = field(default_factory=list)
    reviewer_human: bool = True
    reviewer_extra: list[dict] = field(default_factory=list)
    block_if_missing: bool = True


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
class PipelineConfig:
    """Configuracao opcional de etapas extras do pipeline.

    Hoje cobre o Humanizer (PR-4 humanizacao). No futuro pode cobrir
    self-test Pangram (PR-3), RADAR-style proxy interno etc.
    """

    humanize_enabled: bool = False
    humanize_target_stylometry_score: int = 75
    humanize_max_iters: int = 2


@dataclass
class Geo2026Config:
    """Rubrica de citabilidade GEO (Generative Engine Optimization).

    Liga a validacao por contagem das tecnicas de redacao com lift de
    citacao medido (Aggarwal/Princeton, AutoGEO ICLR 2026). Ver
    docs/GEO_REDACAO_CHECKLIST_2026.md e docs/GEO_KNOWLEDGE_BASE_2026_V3.md.

    Default OFF para preservar o comportamento de clientes nao-GEO: quando
    desabilitado, as contagens viram avisos; quando habilitado, viram erros
    bloqueantes no quality gate.
    """

    princeton_playbook_enabled: bool = False
    min_cite_sources: int = 3
    min_statistics: int = 5
    min_quotations: int = 1
    require_answer_capsule: bool = True
    schema_authority_stack_enabled: bool = False


@dataclass
class CrosslinksConfig:
    """Crosslinks por aula para outros cursos do portal (27/09/2026). Opt-in.

    Desligado, nada é cobrado nem instruído. Ligado, cada aula liga para ao
    menos `min_por_aula` e no máximo `max_por_aula` cursos diferentes do
    catálogo (`catalogo`, JSON ou YAML com a lista `destinos`), e o curso
    inteiro para ao menos `min_destinos_distintos_no_curso`. Só contam links
    cujo caminho começa por um dos `prefixos_validos`. As regras de forma
    (âncora genérica, parágrafos de abertura sem link, instrução do prompt)
    vivem em `config/quality_rules.yaml > validation.crosslinks`.
    """

    enabled: bool = False
    min_por_aula: int = 0
    max_por_aula: int = 0
    min_destinos_distintos_no_curso: int = 0
    prefixos_validos: list[str] = field(default_factory=list)
    catalogo: Path | None = None


@dataclass
class VisualConfig:
    """Peso visual por aula declarado pelo cliente ou pelo curso (27/09/2026).

    Sobrepõe o teto padrão de apoios visuais da aula (`tetos.D.figuras_max` do
    espelho `config/lexicos.json`) sem mexer no espelho. Cada campo é opcional:
    `None` significa "não declarado". Sem nenhum campo declarado, vale o
    comportamento anterior (só o teto do espelho, como aviso).

    - `min_por_aula`: piso de peças visuais na aula (abaixo, erro).
    - `max_por_aula`: teto de peças visuais na aula (acima, aviso).
    - `min_tipos_por_aula`: tipos diferentes de peça na aula (abaixo, aviso).
    - `max_paragrafos_sem_peca`: maior sequência de parágrafos sem peça (acima, aviso).
    """

    min_por_aula: int | None = None
    max_por_aula: int | None = None
    min_tipos_por_aula: int | None = None
    max_paragrafos_sem_peca: int | None = None

    @property
    def declarado(self) -> bool:
        return any(
            v is not None
            for v in (
                self.min_por_aula,
                self.max_por_aula,
                self.min_tipos_por_aula,
                self.max_paragrafos_sem_peca,
            )
        )

    @classmethod
    def de_dict(cls, dados: dict | None) -> VisualConfig:
        """Lê o bloco `visual` de um YAML; chave ausente ou ilegível fica `None`."""

        def _num(chave: str) -> int | None:
            try:
                valor = (dados or {}).get(chave)
                return None if valor is None else max(0, int(valor))
            except (TypeError, ValueError, AttributeError):
                return None

        return cls(
            min_por_aula=_num("min_por_aula"),
            max_por_aula=_num("max_por_aula"),
            min_tipos_por_aula=_num("min_tipos_por_aula"),
            max_paragrafos_sem_peca=_num("max_paragrafos_sem_peca"),
        )

    def sobreposto_por(self, outro: VisualConfig | None) -> VisualConfig:
        """Campos declarados em `outro` (o curso) vencem os deste (o cliente)."""
        if outro is None:
            return self
        return VisualConfig(
            *(
                b if b is not None else a
                for a, b in (
                    (self.min_por_aula, outro.min_por_aula),
                    (self.max_por_aula, outro.max_por_aula),
                    (self.min_tipos_por_aula, outro.min_tipos_por_aula),
                    (self.max_paragrafos_sem_peca, outro.max_paragrafos_sem_peca),
                )
            )
        )


def _severidade(valor: object) -> str:
    """`erro` reprova; qualquer outro valor (ou ausência) avisa."""
    return "erro" if str(valor or "").strip().lower() in ("erro", "error") else "aviso"


def _numero(dados: dict | None, chave: str, tipo=int):
    try:
        valor = (dados or {}).get(chave)
        return None if valor is None else tipo(valor)
    except (TypeError, ValueError, AttributeError):
        return None


@dataclass
class GuiaAplicavelConfig:
    """Aula-guia aplicável, medida por cliente (27/09/2026). Opt-in.

    Desligado, o gate não mede a completude do como fazer. Ligado, a aula é
    medida contra os pisos do `tipo_de_aula` em
    `config/quality_rules.yaml > validation.guia_aplicavel.tipos_de_aula`, com a
    `severidade` declarada (`aviso` ou `erro`).
    """

    enabled: bool = False
    severidade: str = "aviso"
    tipo_de_aula: str = ""

    @classmethod
    def de_dict(cls, dados: dict | None) -> GuiaAplicavelConfig:
        dados = dados if isinstance(dados, dict) else {}
        return cls(
            enabled=bool(dados.get("enabled", False)),
            severidade=_severidade(dados.get("severidade")),
            tipo_de_aula=str(dados.get("tipo_de_aula") or ""),
        )


@dataclass
class NarrativaConfig:
    """Orçamento de narrativa por aula (27/09/2026). Opt-in.

    - `parcela_max`: fração máxima dos parágrafos de prosa com marcas de
      narrativa (0 a 1). `None` = parcela não medida.
    - `abertura_sem_narrativa`: a abertura em cena ou em história vira achado.
    """

    enabled: bool = False
    parcela_max: float | None = None
    abertura_sem_narrativa: bool = False
    severidade: str = "aviso"

    @classmethod
    def de_dict(cls, dados: dict | None) -> NarrativaConfig:
        dados = dados if isinstance(dados, dict) else {}
        return cls(
            enabled=bool(dados.get("enabled", False)),
            parcela_max=_numero(dados, "parcela_max", float),
            abertura_sem_narrativa=bool(dados.get("abertura_sem_narrativa", False)),
            severidade=_severidade(dados.get("severidade")),
        )


@dataclass
class FontesRecentesConfig:
    """Recência das fontes, por cliente ou por curso (27/09/2026). Opt-in.

    - `janela_meses`: idade máxima, em meses, de uma fonte recente.
    - `parcela_min_recente`: fração mínima de fontes recentes (0 a 1).
    - `estado_atual_max_meses`: idade máxima da fonte de uma alegação de estado atual.
    - `data_de_referencia`: data contra a qual a idade é medida (AAAA-MM-DD).
      Ausente, quem chama injeta a data da execução.
    Campo `None` = parte da regra não medida. O curso sobrepõe o cliente campo a campo.
    """

    enabled: bool = False
    janela_meses: int | None = None
    parcela_min_recente: float | None = None
    estado_atual_max_meses: int | None = None
    data_de_referencia: str | None = None
    severidade: str = "aviso"

    @classmethod
    def de_dict(cls, dados: dict | None) -> FontesRecentesConfig:
        dados = dados if isinstance(dados, dict) else {}
        ref = dados.get("data_de_referencia")
        return cls(
            enabled=bool(dados.get("enabled", False)),
            janela_meses=_numero(dados, "janela_meses"),
            parcela_min_recente=_numero(dados, "parcela_min_recente", float),
            estado_atual_max_meses=_numero(dados, "estado_atual_max_meses"),
            data_de_referencia=str(ref) if ref else None,
            severidade=_severidade(dados.get("severidade")),
        )

    def sobreposto_por(self, dados: dict | None) -> FontesRecentesConfig:
        """Chaves declaradas no curso (`dados`) vencem as do cliente."""
        if not isinstance(dados, dict) or not dados:
            return self
        outro = FontesRecentesConfig.de_dict({"enabled": self.enabled, **dados})
        return FontesRecentesConfig(
            enabled=outro.enabled,
            janela_meses=outro.janela_meses if "janela_meses" in dados else self.janela_meses,
            parcela_min_recente=(
                outro.parcela_min_recente
                if "parcela_min_recente" in dados
                else self.parcela_min_recente
            ),
            estado_atual_max_meses=(
                outro.estado_atual_max_meses
                if "estado_atual_max_meses" in dados
                else self.estado_atual_max_meses
            ),
            data_de_referencia=(
                outro.data_de_referencia
                if "data_de_referencia" in dados
                else self.data_de_referencia
            ),
            severidade=outro.severidade if "severidade" in dados else self.severidade,
        )


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
    disclosure: DisclosureConfig = field(default_factory=DisclosureConfig)
    landing_page_dir: Path | None = None
    educacao_dir: Path | None = None
    output_base_dir: Path = field(default_factory=lambda: Path("output"))
    # Wave 6-10 — features opcionais (default off; ligar via client.yaml)
    tutor: TutorConfig = field(default_factory=TutorConfig)
    engagement: EngagementConfig = field(default_factory=EngagementConfig)
    certification: CertificationConfig = field(default_factory=CertificationConfig)
    agentic: AgenticConfig = field(default_factory=AgenticConfig)
    pipeline: PipelineConfig = field(default_factory=PipelineConfig)
    # Rubrica de citabilidade GEO (default off; ligar via client.yaml geo_2026)
    geo: Geo2026Config = field(default_factory=Geo2026Config)
    # Crosslinks por aula (default off; ligar via client.yaml crosslinks)
    crosslinks: CrosslinksConfig = field(default_factory=CrosslinksConfig)
    # Peso visual por aula (default: não declarado, vale o teto do espelho)
    visual: VisualConfig = field(default_factory=VisualConfig)
    # Aula-guia, orçamento de narrativa e fonte recente (27/09/2026; default off)
    guia_aplicavel: GuiaAplicavelConfig = field(default_factory=GuiaAplicavelConfig)
    narrativa: NarrativaConfig = field(default_factory=NarrativaConfig)
    fontes_recentes: FontesRecentesConfig = field(default_factory=FontesRecentesConfig)
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
