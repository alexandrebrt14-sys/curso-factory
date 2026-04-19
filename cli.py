"""
CLI principal do Curso Factory.

Uso:
    python cli.py create "Nome do Curso"
    python cli.py create "Nome do Curso" --client minha_empresa
    python cli.py validate PATH
    python cli.py cost-report
    python cli.py batch config/courses.yaml
    python cli.py clients                 # lista clientes configurados
    python cli.py cache-clear
"""

import argparse
import sys
from pathlib import Path


def _resolve_client(args: argparse.Namespace):
    """Carrega ClientContext a partir de --client ou env CURSO_FACTORY_CLIENT."""
    from src.clients import load_client
    client_id = getattr(args, "client", None) or "default"
    return load_client(client_id)


def cmd_create(args: argparse.Namespace) -> int:
    """Cria um curso completo via pipeline multi-LLM."""
    import logging
    from src.agents.pipeline import CourseFactory
    from src.config import load_courses

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    try:
        client = _resolve_client(args)
    except FileNotFoundError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1

    # Tenta encontrar config do curso no courses.yaml
    course_config = None
    for c in load_courses():
        if args.nome.lower() in c.get("nome", "").lower():
            modulos = []
            for m in c.get("estrutura_modulos", []):
                modulos.append({"titulo": m["titulo"], "descricao": m.get("descricao", "")})
            course_config = {
                "nivel": c.get("nivel", "intermediario"),
                "descricao": c.get("descricao", ""),
                "tags": c.get("tags", []),
                "pre_requisitos": c.get("prerequisitos", []),
                "modulos": modulos,
            }
            break

    factory = CourseFactory(client=client)
    print(f"Iniciando criação do curso: {args.nome}")
    print(f"Cliente: {client.id} ({client.author.name})")
    print("Pipeline: Perplexity > GPT-4o > Gemini > Groq > Claude")
    try:
        result = factory.run(args.nome, course_config=course_config)
        custo_total = sum(factory.cost_tracker.get_session_total().values())
        print(f"\nPipeline {'concluído com sucesso' if result.sucesso else 'interrompido com erros'}")
        print(f"Etapas executadas: {', '.join(result.etapas.keys())}")
        if result.erros:
            for e in result.erros:
                print(f"  ERRO: {e}")
        print(f"Custo total: ${custo_total:.4f}")
        print(factory.cost_tracker.report())
        return 0 if result.sucesso else 1
    except Exception as exc:
        print(f"Erro ao criar curso: {exc}", file=sys.stderr)
        return 1


def cmd_validate(args: argparse.Namespace) -> int:
    """Roda todos os validadores em rascunhos de um diretório ou arquivo."""
    from src.validators.quality import QualityValidator
    from src.validators.accents import AccentValidator

    path = Path(args.path)
    if not path.exists():
        print(f"Caminho não encontrado: {path}", file=sys.stderr)
        return 1

    quality_v = QualityValidator()
    accent_v = AccentValidator()

    files = list(path.rglob("*.md")) if path.is_dir() else [path]
    erros = 0

    for f in files:
        texto = f.read_text(encoding="utf-8")
        q_result = quality_v.validate(texto)
        a_result = accent_v.validate(texto)

        if not q_result.ok or not a_result.ok:
            print(f"\nArquivo: {f}")
            for issue in q_result.issues + a_result.issues:
                print(f"  - {issue}")
            erros += 1

    if erros == 0:
        print(f"Todos os {len(files)} arquivo(s) passaram na validação.")
    else:
        print(f"\n{erros} arquivo(s) com problemas de {len(files)} total.")
    return 0 if erros == 0 else 1


def cmd_cost_report(args: argparse.Namespace) -> int:
    """Exibe relatório detalhado de custos por provider e por curso."""
    from src.config import load_config
    from src.agents.cost_tracker import CostTracker

    config = load_config()
    tracker = CostTracker(config.cache_dir)
    report = tracker.generate_report()

    print("\n=== Relatório de Custos — Curso Factory ===\n")
    print(f"{'Provider':<20} {'Chamadas':>10} {'Tokens':>12} {'Custo (USD)':>14}")
    print("-" * 60)
    for row in report.by_provider:
        print(f"{row.provider:<20} {row.calls:>10} {row.tokens:>12} ${row.cost:>13.4f}")
    print("-" * 60)
    print(f"{'TOTAL':<20} {report.total_calls:>10} {report.total_tokens:>12} ${report.total_cost:>13.4f}")
    print(f"\nPeríodo: {report.period_start} a {report.period_end}")
    print(f"Cursos gerados: {report.courses_count}")
    return 0


def cmd_batch(args: argparse.Namespace) -> int:
    """Cria múltiplos cursos em lote a partir de um arquivo YAML de configuração."""
    import yaml
    from src.config import load_config
    from src.agents.pipeline import CourseFactory

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Arquivo de configuração não encontrado: {config_path}", file=sys.stderr)
        return 1

    with config_path.open(encoding="utf-8") as fh:
        batch_config = yaml.safe_load(fh)

    courses = batch_config.get("courses", [])
    if not courses:
        print("Nenhum curso definido no arquivo de configuração.", file=sys.stderr)
        return 1

    config = load_config()
    factory = CourseFactory(config)
    falhas = 0

    print(f"Processando {len(courses)} curso(s) em lote...\n")
    for i, course in enumerate(courses, 1):
        nome = course.get("name", f"Curso {i}")
        print(f"[{i}/{len(courses)}] {nome}")
        try:
            result = factory.run(nome, course_config=course)
            print(f"  Concluído: {result.output_path} — ${result.total_cost:.4f}")
        except Exception as exc:
            print(f"  Falha: {exc}", file=sys.stderr)
            falhas += 1

    print(f"\nLote concluído. Sucesso: {len(courses) - falhas} / Falhas: {falhas}")
    return 0 if falhas == 0 else 1


def cmd_emit_catalog(args: argparse.Namespace) -> int:
    """Gera o artefato course_catalog.json em output/.

    O artefato é consumido pela landing-page-geo via worker externo.
    O curso-factory nunca escreve diretamente na estrutura da landing page.
    """
    import logging
    from pathlib import Path
    from src.generators.metadata_sync import MetadataSync

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    output_dir = Path(args.output_dir) if args.output_dir else None
    syncer = MetadataSync(output_dir=output_dir)
    result = syncer.sync()

    if result["ok"]:
        print(f"Catálogo gerado: {result['catalog_path']}")
        print(f"Cursos incluídos: {result['course_count']}")
        return 0
    else:
        for err in result["errors"]:
            print(f"ERRO: {err}", file=sys.stderr)
        return 1


def cmd_drafts_to_tsx(args: argparse.Namespace) -> int:
    """Converte drafts JSON em output/drafts/ para TSX deployable.

    Achado F12 da auditoria 2026-04-08: 13 drafts com investimento LLM ja
    gasto (15-17k palavras cada) ficaram orfaos sem nunca ser convertidos.
    Este comando faz best-effort de conversao, recuperando o investimento.

    Drafts que falharem parsing sao logados como warnings e o batch
    continua. Operador revisa o output em output/converted_from_drafts/
    e copia manualmente para output/deployed/ os que aprovou.
    """
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

    print()
    if result["converted"] > 0:
        print(f"Output em: {output_dir}")
        print("Revise manualmente antes de copiar para output/deployed/")

    return 0 if result["failed"] == 0 else 0  # nao falhar batch por individuais


def cmd_clients(args: argparse.Namespace) -> int:
    """Lista clientes configurados em config/clients/."""
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
            print(f"  {'':<20} voice_guard={vg} min_score={c.voice_guard.min_score} style={c.editorial.style}")
        except Exception as exc:
            print(f"  {cid:<20} ERRO ao carregar: {exc}")
    return 0


def cmd_cache_clear(args: argparse.Namespace) -> int:
    """Limpa o cache de resultados de chamadas aos LLMs."""
    import shutil
    from src.config import load_config

    config = load_config()
    cache_dir = Path(config.cache_dir)

    if not cache_dir.exists():
        print("Cache já está vazio.")
        return 0

    tamanho = sum(f.stat().st_size for f in cache_dir.rglob("*") if f.is_file())
    shutil.rmtree(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)

    print(f"Cache limpo. Espaço liberado: {tamanho / 1024:.1f} KB")
    return 0


def _add_client_arg(sub: argparse.ArgumentParser) -> None:
    """Adiciona o argumento --client em subcomandos que precisam de ClientContext."""
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
    subparsers = parser.add_subparsers(dest="command", required=True)

    # create
    p_create = subparsers.add_parser("create", help="Cria um curso completo via pipeline")
    p_create.add_argument("nome", metavar="NOME", help="Nome do curso a ser criado")
    _add_client_arg(p_create)
    p_create.set_defaults(func=cmd_create)

    # clients
    p_clients = subparsers.add_parser("clients", help="Lista clientes configurados")
    p_clients.set_defaults(func=cmd_clients)

    # validate
    p_validate = subparsers.add_parser("validate", help="Valida rascunhos de um caminho")
    p_validate.add_argument("path", metavar="PATH", help="Arquivo ou diretório com rascunhos")
    p_validate.set_defaults(func=cmd_validate)

    # cost-report
    p_cost = subparsers.add_parser("cost-report", help="Exibe relatório de custos por provider")
    p_cost.set_defaults(func=cmd_cost_report)

    # batch
    p_batch = subparsers.add_parser("batch", help="Cria múltiplos cursos em lote via YAML")
    p_batch.add_argument("config", metavar="CONFIG", help="Caminho para o arquivo YAML de lote")
    _add_client_arg(p_batch)
    p_batch.set_defaults(func=cmd_batch)

    # emit-catalog
    p_catalog = subparsers.add_parser(
        "emit-catalog",
        help="Gera output/course_catalog.json (artefato consumido pela landing page via worker)",
    )
    p_catalog.add_argument(
        "--output-dir",
        dest="output_dir",
        default=None,
        metavar="DIR",
        help="Diretório de saída (padrão: output/ na raiz do projeto)",
    )
    p_catalog.set_defaults(func=cmd_emit_catalog)

    # cache-clear
    p_cache = subparsers.add_parser("cache-clear", help="Limpa o cache de resultados dos LLMs")
    p_cache.set_defaults(func=cmd_cache_clear)

    # drafts-to-tsx (achado F12 da auditoria 2026-04-08)
    p_d2t = subparsers.add_parser(
        "drafts-to-tsx",
        help="Converte drafts JSON orfaos para TSX deployable (F12)",
    )
    p_d2t.add_argument(
        "--input",
        default="output/drafts",
        metavar="DIR",
        help="Diretorio com drafts *.json (default: output/drafts)",
    )
    p_d2t.add_argument(
        "--output",
        default="output/converted_from_drafts",
        metavar="DIR",
        help="Diretorio destino para os TSX (default: output/converted_from_drafts)",
    )
    _add_client_arg(p_d2t)
    p_d2t.set_defaults(func=cmd_drafts_to_tsx)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
