#!/usr/bin/env python3
"""
Captura passiva (candidate-gate) — hook Stop do Claude Code.

Ao fim de cada sessao, registra um marcador de rascunho em
<decisions>/candidates/_candidate_YYYY-MM-DD.md, para lembrar de DESTILAR os
aprendizados da sessao numa decisao real (ver <decisions>/README.md).

Principios (do setup de Memoria Persistente):
- Rascunho NAO e autoritativo. A pasta candidates/ e gitignored.
- O hook FALHA EM SILENCIO: nunca bloqueia o agente (sempre exit 0).
- 1 arquivo por dia, 1 linha por sessao — leve, sem explosao de arquivos.
"""
import sys
import os
import json
from datetime import datetime, timezone


def main():
    raw = ""
    try:
        if not sys.stdin.isatty():
            raw = sys.stdin.read()
    except Exception:
        raw = ""

    data = {}
    try:
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        data = {}

    cwd = data.get("cwd") or os.getcwd()
    session = (data.get("session_id") or "")[:8] or "sessao"

    base = None
    for candidate_dir in ("governance/decisions", "wiki/decisions"):
        path = os.path.join(cwd, candidate_dir)
        if os.path.isdir(path):
            base = path
            break
    if base is None:
        return  # repo sem a camada de decisoes; nada a capturar

    cands = os.path.join(base, "candidates")
    os.makedirs(cands, exist_ok=True)

    now = datetime.now(timezone.utc).astimezone()
    day = now.strftime("%Y-%m-%d")
    stamp = now.strftime("%H:%M %z")
    out = os.path.join(cands, "_candidate_" + day + ".md")

    is_new = not os.path.exists(out)
    with open(out, "a", encoding="utf-8") as fh:
        if is_new:
            fh.write("# Rascunhos de captura — " + day + "\n\n")
            fh.write(
                "> NÃO autoritativo (candidate-gate). Destile o que valer numa "
                "decisão real via `../_TEMPLATE.md`, registre em `../INDEX.md` e "
                "apague a linha aqui.\n\n"
            )
        fh.write(
            "- [ ] " + stamp + " — sessão `" + session + "` encerrada. "
            "Surgiu algum padrão, erro-a-evitar ou decisão a registrar?\n"
        )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
