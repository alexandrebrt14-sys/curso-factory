"""27/09/2026: o número que o prompt cita é o mesmo que o validador lê."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.validators import lexicos_loader  # noqa: E402
from src.validators.numeros_dos_prompts import numero, numeros_dos_prompts  # noqa: E402

PROMPTS = PROJECT_ROOT / "src" / "templates" / "prompts"
PASTAS = (PROMPTS, PROMPTS / "pt-br", PROMPTS / "en", PROMPTS / "es")

#: Frases que carregavam o número escrito à mão até 27/09/2026.
LITERAIS_ANTIGOS = re.compile(
    r"até 12 palavras|até 25 palavras|de 350 palavras|até 28\b|até 60\b|de 3 marcadores|"
    r"up to 12|up to 25 words|exceeds 350|up to 28\b|of 3 markers|"
    r"hasta 12 palabras|hasta 25 palabras|de 350 palabras|hasta 28\b|de 3 marcadores"
)


def test_nenhum_prompt_traz_os_numeros_escritos_a_mao() -> None:
    for pasta in PASTAS:
        for nome in ("draft.md", "review.md", "trail.md", "analyze.md"):
            caminho = pasta / nome
            if caminho.exists():
                achados = LITERAIS_ANTIGOS.findall(caminho.read_text(encoding="utf-8"))
                assert achados == [], (caminho, achados)


def test_valores_saem_do_espelho_e_do_yaml() -> None:
    limiares = lexicos_loader.carregar_lexicos()["limiares"]
    assert numero("glosa_max_palavras") == limiares["glosaMaxPalavras"]
    assert numero("frase_max_palavras") == limiares["fraseMaxPalavras"]
    assert numero("h3_acima_de_palavras") == limiares["h3SoAcimaDePalavras"]


def test_mudar_o_espelho_muda_o_prompt(tmp_path, monkeypatch) -> None:
    from src.agents.writer import Writer
    from src.orchestrator import Orchestrator

    dados = json.loads(lexicos_loader.LEXICOS_PATH.read_text(encoding="utf-8"))
    dados["limiares"]["glosaMaxPalavras"] = 9
    espelho = tmp_path / "lexicos.json"
    espelho.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(lexicos_loader, "LEXICOS_PATH", espelho)
    lexicos_loader.carregar_lexicos.cache_clear()
    try:
        prompt = Writer(client=None).build_prompt("pesquisa", **Orchestrator._tetos_da_aula())
        assert "explicação de até 9 palavras" in prompt
        assert "{glosa_max_palavras}" not in prompt
    finally:
        lexicos_loader.carregar_lexicos.cache_clear()


def test_todas_as_variaveis_chegam_substituidas_em_todos_os_idiomas() -> None:
    from src.agents.writer import Writer

    variaveis = numeros_dos_prompts()
    for idioma in ("pt-br", "en", "es"):
        agente = Writer(client=None)
        agente.language = idioma
        prompt = agente.build_prompt("pesquisa", **variaveis)
        restos = [v for v in variaveis if "{" + v + "}" in prompt]
        assert restos == [], (idioma, restos)
