"""CLI principal do Curso Factory.

Comandos:
    create        — gera curso completo via pipeline multi-LLM
    clients       — lista clientes em config/clients/
    validate      — valida rascunhos (acentuação, conteúdo, links, voice guard)
    cost-report   — relatório de custos por provider e por curso
    batch         — gera múltiplos cursos a partir de YAML
    emit-catalog  — escreve output/course_catalog.json
    drafts-to-tsx — converte drafts JSON órfãos em TSX deployable
    cache-clear   — limpa o cache LLM em disco

Todos os subcomandos que precisam de identidade/branding aceitam --client
para selecionar um cliente em config/clients/<id>/. Sem flag, usa "default".
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Any


def _setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def _resolve_client(args: argparse.Namespace):
    from src.clients import load_client
    client_id = getattr(args, "client", None) or "default"
    return load_client(client_id)


# ─── create ────────────────────────────────────────────────────────────

def cmd_create(args: argparse.Namespace) -> int:
    _setup_logging()
    from src.agents.pipeline import CourseFactory
    from src.config import load_courses

    try:
        client = _resolve_client(args)
    except FileNotFoundError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1

    course_config: dict[str, Any] | None = None
    for c in load_courses():
        if args.nome.lower() in c.get("nome", "").lower():
            course_config = {
                "nivel": c.get("nivel", "intermediario"),
                "descricao": c.get("descricao", ""),
                "tags": c.get("tags", []),
                "pre_requisitos": c.get("prerequisitos", []),
                "modulos": [
                    {"titulo": m["titulo"], "descricao": m.get("descricao", "")}
                    for m in c.get("estrutura_modulos", [])
                ],
            }
            break

    factory = CourseFactory(client=client)
    print(f"Iniciando criação do curso: {args.nome}")
    print(f"Cliente: {client.id} ({client.author.name})")
    print("Pipeline: Perplexity > GPT-4o > Gemini > Groq > Claude")
    try:
        result = factory.run(args.nome, course_config=course_config)
    except Exception as exc:
        print(f"Erro ao criar curso: {exc}", file=sys.stderr)
        return 1

    custo_total = sum(factory.cost_tracker.get_session_total().values())
    status = "concluído com sucesso" if result.sucesso else "interrompido com erros"
    print(f"\nPipeline {status}")
    print(f"Etapas executadas: {', '.join(result.etapas.keys()) or '(nenhuma)'}")
    for e in result.erros:
        print(f"  ERRO: {e}")
    print(f"Custo total: ${custo_total:.4f}")
    print(factory.cost_tracker.report())
    return 0 if result.sucesso else 1


# ─── clients ───────────────────────────────────────────────────────────

def cmd_clients(args: argparse.Namespace) -> int:
    from src.clients import list_clients, load_client

    ids = list_clients()
    if not ids:
        print("Nenhum cliente configurado em config/clients/.")
        print("Copie config/clients/_template/ para criar um novo.")
        return 1

    print(f"Clientes configurados ({len(ids)}):")
    print()
    for cid in ids:
        try:
            c = load_client(cid)
            vg = "ON" if c.voice_guard.enabled else "off"
            print(f"  {cid:<20} {c.author.name} @ {c.domain.canonical_url}")
            print(
                f"  {'':<20} voice_guard={vg} min_score={c.voice_guard.min_score} "
                f"style={c.editorial.style}"
            )
        except Exception as exc:
            print(f"  {cid:<20} ERRO ao carregar: {exc}")
    return 0


# ─── validate ──────────────────────────────────────────────────────────

def cmd_validate(args: argparse.Namespace) -> int:
    """Roda o QualityGate (acentos + conteúdo + links + voice guard) num path."""
    _setup_logging()
    from src.validators.quality_gate import QualityGate

    try:
        client = _resolve_client(args)
    except FileNotFoundError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1

    path = Path(args.path)
    if not path.exists():
        print(f"Caminho não encontrado: {path}", file=sys.stderr)
        return 1

    gate = QualityGate(client=client, auto_fix=False)
    files = sorted(path.rglob("*.md")) if path.is_dir() else [path]
    if not files:
        print(f"Nenhum arquivo .md em {path}")
        return 0

    reprovados = 0
    for f in files:
        text = f.read_text(encoding="utf-8")
        result = gate.check_text(text, curso_id=f.stem)
        if result.aprovado:
            print(f"OK   {f}")
        else:
            reprovados += 1
            print(f"FAIL {f}")
            for err in result.erros:
                print(f"     - {err}")

    print(f"\nTotal: {len(files)} arquivo(s); aprovados: {len(files) - reprovados}; reprovados: {reprovados}")
    return 0 if reprovados == 0 else 1


# ─── cost-report ───────────────────────────────────────────────────────

def cmd_cost_report(args: argparse.Namespace) -> int:
    """Relatório de custos a partir do log persistido em output/costs.json."""
    from src.cost_tracker import CostTracker

    tracker = CostTracker()
    entries = tracker._entries  # leitura direta — fonte única do log
    if not entries:
        print("Nenhum custo registrado em output/costs.json.")
        return 0

    by_provider: dict[str, dict[str, float | int]] = {}
    by_course: dict[str, float] = {}
    total_calls = 0
    total_tokens = 0
    total_cost = 0.0

    for e in entries:
        prov = e["provider"]
        slot = by_provider.setdefault(prov, {"calls": 0, "tokens": 0, "cost": 0.0})
        slot["calls"] = int(slot["calls"]) + 1
        slot["tokens"] = int(slot["tokens"]) + int(e.get("tokens_in", 0)) + int(e.get("tokens_out", 0))
        slot["cost"] = float(slot["cost"]) + float(e["custo_usd"])

        cid = e.get("course_id") or "(sem curso)"
        by_course[cid] = by_course.get(cid, 0.0) + float(e["custo_usd"])

        total_calls += 1
        total_tokens += int(e.get("tokens_in", 0)) + int(e.get("tokens_out", 0))
        total_cost += float(e["custo_usd"])

    print("\n=== Relatório de Custos — Curso Factory ===\n")
    print(f"{'Provider':<15} {'Chamadas':>10} {'Tokens':>12} {'Custo (USD)':>14}")
    print("-" * 55)
    for prov, slot in sorted(by_provider.items()):
        print(f"{prov:<15} {int(slot['calls']):>10} {int(slot['tokens']):>12} ${float(slot['cost']):>13.4f}")
    print("-" * 55)
    print(f"{'TOTAL':<15} {total_calls:>10} {total_tokens:>12} ${total_cost:>13.4f}")

    if len(by_course) > 1 or "(sem curso)" not in by_course:
        print("\nPor curso:")
        for cid, cost in sorted(by_course.items(), key=lambda x: -x[1]):
            print(f"  {cid:<40} ${cost:>10.4f}")

    return 0


# ─── batch ─────────────────────────────────────────────────────────────

def cmd_batch(args: argparse.Namespace) -> int:
    """Cria múltiplos cursos a partir de um YAML de lote."""
    _setup_logging()
    import yaml
    from src.agents.pipeline import CourseFactory

    try:
        client = _resolve_client(args)
    except FileNotFoundError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Arquivo de configuração não encontrado: {config_path}", file=sys.stderr)
        return 1

    with config_path.open(encoding="utf-8") as fh:
        batch_config = yaml.safe_load(fh) or {}

    courses = batch_config.get("courses", batch_config) if isinstance(batch_config, dict) else batch_config
    if not courses:
        print("Nenhum curso definido no arquivo de configuração.", file=sys.stderr)
        return 1

    factory = CourseFactory(client=client)
    falhas = 0

    print(f"Processando {len(courses)} curso(s) em lote (cliente: {client.id})...\n")
    for i, course in enumerate(courses, 1):
        nome = course.get("nome") or course.get("name") or f"Curso {i}"
        print(f"[{i}/{len(courses)}] {nome}")
        course_config: dict[str, Any] = {
            "nivel": course.get("nivel", "intermediario"),
            "descricao": course.get("descricao", ""),
            "tags": course.get("tags", []),
            "pre_requisitos": course.get("prerequisitos", []),
            "modulos": [
                {"titulo": m["titulo"], "descricao": m.get("descricao", "")}
                for m in course.get("estrutura_modulos", course.get("modulos", []))
            ],
        }
        try:
            result = factory.run(nome, course_config=course_config)
            custo = sum(factory.cost_tracker.get_session_total().values())
            status = "ok" if result.sucesso else "FALHOU"
            print(f"  {status} — {len(result.etapas)} etapas — sessão até aqui: ${custo:.4f}")
            if not result.sucesso:
                falhas += 1
        except Exception as exc:
            print(f"  EXCEÇÃO: {exc}", file=sys.stderr)
            falhas += 1

    print(f"\nLote concluído. Sucesso: {len(courses) - falhas} / Falhas: {falhas}")
    return 0 if falhas == 0 else 1


# ─── emit-catalog ──────────────────────────────────────────────────────

def cmd_emit_catalog(args: argparse.Namespace) -> int:
    _setup_logging()
    from src.generators.metadata_sync import MetadataSync

    output_dir = Path(args.output_dir) if args.output_dir else None
    syncer = MetadataSync(output_dir=output_dir)
    result = syncer.sync()

    if result["ok"]:
        print(f"Catálogo gerado: {result['catalog_path']}")
        print(f"Cursos incluídos: {result['course_count']}")
        return 0
    for err in result["errors"]:
        print(f"ERRO: {err}", file=sys.stderr)
    return 1


# ─── drafts-to-tsx ─────────────────────────────────────────────────────

def cmd_drafts_to_tsx(args: argparse.Namespace) -> int:
    from src.converters.draft_to_course import convert_drafts_directory

    try:
        client = _resolve_client(args)
    except FileNotFoundError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1

    input_dir = Path(args.input)
    output_dir = Path(args.output)

    print(f"Convertendo drafts de {input_dir} -> {output_dir}")
    print(f"Cliente: {client.id} ({client.author.name})")
    print()

    result = convert_drafts_directory(input_dir, output_dir, client=client)

    if "error" in result:
        print(f"ERRO: {result['error']}")
        return 1

    print(f"Total de drafts: {result['total']}")
    print(f"Convertidos: {result['converted']}")
    print(f"Falhados: {result['failed']}")
    print()

    for item in result["files"]:
        if item["status"] == "ok":
            print(f"  OK   {item['file']} -> {item['slug']}/ ({item['steps']} steps)")
        else:
            print(f"  FAIL {item['file']} ({item.get('reason', 'desconhecido')})")

    if result["converted"] > 0:
        print()
        print(f"Output em: {output_dir}")
        print("Revise manualmente antes de copiar para output/deployed/")

    return 0 if result["failed"] == 0 else 1


# ─── cache-clear ───────────────────────────────────────────────────────

def cmd_cache_clear(args: argparse.Namespace) -> int:
    """Limpa o cache LLM em disco (.cache/)."""
    from src.cache import Cache

    cache = Cache()
    removidos = cache.clear()
    print(f"Cache limpo. {removidos} entrada(s) removida(s).")
    return 0


# ─── emit-llms-txt (Wave 10) ───────────────────────────────────────────

def cmd_emit_llms_txt(args: argparse.Namespace) -> int:
    """Gera llms.txt para 1 curso ou todos os cursos do cliente.

    Output: <output_dir>/<slug>/llms.txt
    """
    from src.agentic.llms_txt import write_llms_txt
    from src.converters.draft_to_course import convert_draft_to_course

    try:
        client = _resolve_client(args)
    except FileNotFoundError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1

    output_dir = Path(args.output_dir) if args.output_dir else client.output_dir / "llms-txt"
    output_dir.mkdir(parents=True, exist_ok=True)

    drafts_dir = Path(args.input) if args.input else client.output_dir / "drafts"
    if not drafts_dir.exists():
        print(f"Diretório de drafts não encontrado: {drafts_dir}", file=sys.stderr)
        return 1

    drafts = sorted(drafts_dir.glob("*.json"))
    drafts = [d for d in drafts if "checkpoint" not in d.name.lower()]
    if args.slug:
        drafts = [d for d in drafts if d.stem.startswith(args.slug)]
        if not drafts:
            print(f"Nenhum draft encontrado para slug '{args.slug}' em {drafts_dir}", file=sys.stderr)
            return 1

    gerados = 0
    falhas = 0
    for draft_path in drafts:
        course = convert_draft_to_course(draft_path, client=client)
        if not course:
            falhas += 1
            print(f"  FAIL {draft_path.name} (parse)")
            continue
        path = write_llms_txt(course, client, output_dir)
        gerados += 1
        print(f"  OK   {course.slug} -> {path.relative_to(output_dir.parent)}")

    print(f"\nGerados: {gerados} | Falhas: {falhas} | Output: {output_dir}")
    return 0 if falhas == 0 else 1


# ─── certify (Wave 9) ──────────────────────────────────────────────────

def cmd_certify(args: argparse.Namespace) -> int:
    """Gera certificado HTML verificável para um aluno."""
    import os
    from src.certification.certificate import generate_certificate, render_html
    from src.converters.draft_to_course import convert_draft_to_course

    try:
        client = _resolve_client(args)
    except FileNotFoundError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1

    drafts_dir = client.output_dir / "drafts"
    matching = sorted(drafts_dir.glob(f"{args.slug}_*.json"))
    matching = [d for d in matching if "checkpoint" not in d.name.lower()]
    if not matching:
        print(f"Nenhum draft encontrado para slug '{args.slug}' em {drafts_dir}", file=sys.stderr)
        return 1

    course = convert_draft_to_course(matching[-1], client=client)
    if not course:
        print(f"Falha ao parsear curso de {matching[-1]}", file=sys.stderr)
        return 1

    secret = args.secret or os.environ.get("CERTIFICATE_SECRET", "")
    if not secret:
        print("ERRO: --secret obrigatório (ou env CERTIFICATE_SECRET)", file=sys.stderr)
        return 1

    try:
        cert = generate_certificate(
            student_email=args.email,
            student_name=args.name,
            course=course,
            score=args.score,
            secret=secret,
            pass_threshold=args.pass_threshold,
        )
    except ValueError as exc:
        print(f"Reprovado: {exc}", file=sys.stderr)
        return 1

    output_dir = Path(args.output_dir) if args.output_dir else client.output_dir / "certificates"
    output_dir.mkdir(parents=True, exist_ok=True)

    html = render_html(cert, course)
    output_path = output_dir / f"{cert.id}.html"
    output_path.write_text(html, encoding="utf-8")

    print(f"Certificado gerado: {output_path}")
    print(f"Hash: {cert.hash}")
    print(f"Score: {cert.score:.2%}")
    return 0


# ─── parser ────────────────────────────────────────────────────────────

def _add_client_arg(sub: argparse.ArgumentParser) -> None:
    sub.add_argument(
        "--client",
        default=None,
        metavar="ID",
        help="ID do cliente em config/clients/<id>/ (default: 'default')",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="curso-factory",
        description="Fábrica de cursos educacionais com pipeline multi-LLM orquestrado.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("create", help="Cria um curso completo via pipeline")
    p.add_argument("nome", metavar="NOME", help="Nome do curso a ser criado")
    _add_client_arg(p)
    p.set_defaults(func=cmd_create)

    p = sub.add_parser("clients", help="Lista clientes configurados")
    p.set_defaults(func=cmd_clients)

    p = sub.add_parser("validate", help="Valida rascunhos via QualityGate")
    p.add_argument("path", metavar="PATH", help="Arquivo ou diretório com rascunhos")
    _add_client_arg(p)
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("cost-report", help="Relatório de custos por provider e por curso")
    p.set_defaults(func=cmd_cost_report)

    p = sub.add_parser("batch", help="Cria múltiplos cursos em lote via YAML")
    p.add_argument("config", metavar="CONFIG", help="Caminho para o arquivo YAML de lote")
    _add_client_arg(p)
    p.set_defaults(func=cmd_batch)

    p = sub.add_parser(
        "emit-catalog",
        help="Gera output/course_catalog.json (artefato consumido pela landing page via worker)",
    )
    p.add_argument(
        "--output-dir",
        dest="output_dir",
        default=None,
        metavar="DIR",
        help="Diretório de saída (padrão: output/ na raiz do projeto)",
    )
    p.set_defaults(func=cmd_emit_catalog)

    p = sub.add_parser(
        "drafts-to-tsx",
        help="Converte drafts JSON órfãos para TSX deployable",
    )
    p.add_argument(
        "--input",
        default="output/drafts",
        metavar="DIR",
        help="Diretório com drafts *.json (default: output/drafts)",
    )
    p.add_argument(
        "--output",
        default="output/converted_from_drafts",
        metavar="DIR",
        help="Diretório destino para os TSX (default: output/converted_from_drafts)",
    )
    _add_client_arg(p)
    p.set_defaults(func=cmd_drafts_to_tsx)

    p = sub.add_parser("cache-clear", help="Limpa o cache LLM em disco")
    p.set_defaults(func=cmd_cache_clear)

    # Wave 10 — emit-llms-txt
    p = sub.add_parser(
        "emit-llms-txt",
        help="Gera llms.txt por curso (agent legibility, Wave 10)",
    )
    p.add_argument("--slug", default=None, help="Slug específico (default: todos)")
    p.add_argument("--input", default=None, metavar="DIR", help="Diretório de drafts (default: <output_dir>/drafts)")
    p.add_argument("--output-dir", dest="output_dir", default=None, metavar="DIR", help="Saída (default: <output_dir>/llms-txt)")
    _add_client_arg(p)
    p.set_defaults(func=cmd_emit_llms_txt)

    # Wave 9 — certify
    p = sub.add_parser(
        "certify",
        help="Gera certificado verificável para um aluno (Wave 9)",
    )
    p.add_argument("--slug", required=True, help="Slug do curso")
    p.add_argument("--email", required=True, help="E-mail do aluno")
    p.add_argument("--name", required=True, help="Nome completo do aluno")
    p.add_argument("--score", type=float, required=True, help="Score (0.0 a 1.0)")
    p.add_argument("--secret", default=None, help="Secret HMAC (ou env CERTIFICATE_SECRET)")
    p.add_argument("--pass-threshold", dest="pass_threshold", type=float, default=0.7, help="Mínimo para aprovar (default 0.7)")
    p.add_argument("--output-dir", dest="output_dir", default=None, metavar="DIR", help="Saída (default: <output_dir>/certificates)")
    _add_client_arg(p)
    p.set_defaults(func=cmd_certify)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
