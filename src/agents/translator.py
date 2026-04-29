"""Agente de tradução do conteúdo final via Claude.

Wave 8 — Multi-idioma. Recebe o conteúdo aprovado pelo revisor e
produz uma versão fiel no idioma alvo, preservando Markdown, tabelas,
blockquotes, listas e padrões editoriais HSM/HBR/MIT Sloan.

Prompt externo: ``src/templates/prompts/translate.md`` (versões traduzidas
em ``src/templates/prompts/<lang>/translate.md``).
"""

from __future__ import annotations

from src.agents.base import Agent, _safe_substitute


class Translator(Agent):
    """Agente Claude para traduzir conteúdo curricular entre idiomas.

    O Translator herda do ``Agent`` base mas não usa o pipeline padrão
    de ``execute(context, ...)``. Em vez disso, expõe ``translate(...)``
    que monta o prompt com placeholders ``{source_lang}``, ``{target_lang}``
    e ``{content}``.

    Modo dry-run::

        Quando ``dry_run=True`` é passado ao construtor, ``translate``
        retorna uma resposta canônica (string não-vazia em Markdown) sem
        chamar nenhum LLM. Útil para testes e CI.
    """

    nome = "translator"
    provider = "anthropic"
    model = "claude-opus-4-6"
    prompt_file = "translate.md"

    # Fallback inline mínimo, caso o arquivo .md não exista.
    TEMPLATE = (
        "Você é um tradutor editorial de elite, com padrão Harvard Business "
        "Review / MIT Sloan / HSM Management. Traduza o conteúdo abaixo de "
        "{source_lang} para {target_lang} preservando integralmente o "
        "Markdown, tabelas, blockquotes e termos técnicos canônicos. Não "
        "resuma, não adicione comentários, não invente dados. Retorne apenas "
        "o texto traduzido.\n\n"
        "--- CONTEÚDO PARA TRADUZIR ---\n{content}"
    )

    def __init__(self, client, dry_run: bool = False) -> None:  # type: ignore[no-untyped-def]
        super().__init__(client)
        self.dry_run = dry_run

    def build_prompt(  # type: ignore[override]
        self,
        context: str = "",
        **template_vars: str,
    ) -> str:
        """Monta o prompt do Translator.

        Aceita os placeholders ``{source_lang}``, ``{target_lang}`` e
        ``{content}``. ``context`` é mantido por compatibilidade com a
        assinatura do ``Agent`` base, mas o Translator não o utiliza.
        """
        template = self._load_prompt_template()
        substitutions = {"context": context, **template_vars}
        if template:
            return _safe_substitute(template, substitutions)
        return _safe_substitute(self.TEMPLATE, substitutions)

    def translate(
        self,
        content: str,
        source_lang: str,
        target_lang: str,
    ) -> str:
        """Traduz ``content`` de ``source_lang`` para ``target_lang``.

        Args:
            content: Markdown do módulo/curso a traduzir. Deve estar
                pronto (já revisado), pois o Translator preserva — e não
                edita — o conteúdo.
            source_lang: Código do idioma de origem (ex.: ``"pt-br"``).
            target_lang: Código do idioma de destino (ex.: ``"en"``).

        Returns:
            String não-vazia em Markdown com a tradução. Em ``dry_run``,
            retorna uma resposta canônica que nunca aciona o LLM.
        """
        prompt = self.build_prompt(
            "",
            source_lang=source_lang,
            target_lang=target_lang,
            content=content,
        )

        if self.dry_run:
            # Resposta canônica determinística para testes e CI.
            preview = (content or "").strip().splitlines()
            head = preview[0] if preview else "(conteúdo vazio)"
            return (
                f"[DRY-RUN translator] {source_lang} -> {target_lang}\n\n"
                f"# Translated content (dry-run)\n\n"
                f"Source preview: {head}\n\n"
                f"Length: {len(content or '')} chars\n"
            )

        llm_kwargs: dict = {}
        if self.model:
            llm_kwargs["model"] = self.model
        return self.client.call(self.provider, prompt, **llm_kwargs)
