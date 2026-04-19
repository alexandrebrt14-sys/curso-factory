"""Converte draft do curso 'Introdução às Semijoias' em TSX sob cliente herreira.

Pega o draft mais recente gerado pelo pipeline e roda: Quality Gate →
Schema Builder → TSX Generator → escreve em output/clients/herreira/approved/.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.clients import load_client
from src.generators.schema_builder import SchemaBuilder
from src.generators.tsx_generator import TsxGenerator
from src.validators.quality_gate import QualityGate


def banner(title: str) -> None:
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


SLUG = "introducao-as-semijoias"
client = load_client("herreira")

banner(f"1. Cliente carregado: {client.id}")
print(f"  Autor:    {client.author.name}")
print(f"  Empresa:  {client.company.name}")
print(f"  Domínio:  {client.domain.canonical_url}")
print(f"  Path:     {client.domain.educacao_path}")

banner("2. Localizar draft mais recente")
drafts = sorted(
    (ROOT / "output" / "drafts").glob(f"{SLUG}_*.json"),
    reverse=True,
)
if not drafts:
    print("Nenhum draft encontrado para", SLUG)
    sys.exit(1)
draft_path = drafts[0]
print(f"  {draft_path.name}")

with draft_path.open("r", encoding="utf-8") as f:
    draft_json = json.load(f)

etapas = draft_json.get("etapas", {})
# Usar draft do GPT-4o (maior e mais completo) ao invés do review (bug do
# Orchestrator envia metadata em vez de draft — já reportado)
md_bruto = etapas.get("draft", "")
print(f"  Etapas: {list(etapas.keys())}")
print(f"  Draft:  {len(md_bruto)} chars")

banner("3. Normalizar headings")
lines = []
seen = set()
for line in md_bruto.splitlines():
    m = re.match(r"^#\s+(Módulo\s+\d+[:\s].*)$", line)
    if m:
        title = m.group(1).strip()
        if title.lower() in seen:
            lines.append("")
            continue
        seen.add(title.lower())
        lines.append(f"## {title}")
    else:
        m2 = re.match(r"^##\s+(.+)$", line)
        if m2:
            lines.append(f"### {m2.group(1)}")
        else:
            lines.append(line)
md = "\n".join(lines)
print(f"  {len(seen)} módulos únicos extraídos")

banner("4. Quality Gate (voice_guard Herreira)")
gate = QualityGate(client=client, auto_fix=True)
result = gate.check_text(md, curso_id=SLUG)
print(f"  voice_guard score:     {result.voice_guard_score}/100")
print(f"  voice_guard aprovou:   {result.voice_guard_ok}")
print(f"  acentos corrigidos:    {result.acentos_corrigidos}")
print(f"  erros bloqueantes:     {len(result.erros)}")
if result.erros:
    print("  Primeiros erros:")
    for e in result.erros[:5]:
        print(f"    - {e[:140]}")

md_limpo = result.texto_corrigido or md

banner("5. Schema Builder")
yaml_def = {
    "titulo": "Introdução às Semijoias: Materiais, Banhos e Pedras",
    "descricao": (
        "Base técnica para quem está começando na revenda: como são feitas as "
        "semijoias, diferença entre banho de ouro 18K e ródio, tipos de pedras, "
        "padrões de qualidade e como falar sobre produto com segurança."
    ),
    "tags": ["semijoias", "banho-ouro-18k", "produto", "iniciante", "herreira"],
    "keywords_seo": [
        "curso para revendedora de semijoias",
        "banho de ouro 18K",
        "semijoias finas",
        "como vender semijoias",
        "curso Herreira Joias",
    ],
    "nivel": "iniciante",
}

classify_stub = {
    "nivel": "iniciante",
    "tags": yaml_def["tags"],
    "keywords_seo": yaml_def["keywords_seo"],
    "prerequisitos": [],
    "faq": [
        {
            "pergunta": "Preciso ter experiência prévia em vendas para fazer esse curso?",
            "resposta": (
                "Não. O curso foi desenhado para quem está começando como revendedora da "
                "rede Herreira. Tudo parte do zero, com exemplos de como apresentar o produto "
                "para clientes reais do dia a dia."
            ),
        },
        {
            "pergunta": "Em quanto tempo consigo concluir?",
            "resposta": (
                "Cerca de duas horas divididas em seis módulos curtos. A maioria das "
                "revendedoras conclui em uma semana fazendo um módulo por dia, no intervalo "
                "entre atendimentos."
            ),
        },
        {
            "pergunta": "O conteúdo vale para revenda de Aulore e Vitesse também?",
            "resposta": (
                "Sim. Os fundamentos técnicos de semijoia (matéria-prima, banho de ouro 18K, "
                "ródio, pedras) são os mesmos para as três marcas do Grupo HAV — Herreira, "
                "Aulore e Vitesse."
            ),
        },
    ],
}

sb = SchemaBuilder()
course = sb.build(SLUG, yaml_def, md_limpo, classify_stub, client=client)
print(f"  CourseDefinition válido: slug={course.slug}, steps={len(course.steps)}, min={course.duracao_total_minutos}")
print(f"  Autor: {course.autor_nome}")
print(f"  Domínio: {course.dominio}")
print(f"  Company: {course.company_name}")
print(f"  URL canônica: {course.canonical_url}")

banner("6. Renderizar TSX")
gen = TsxGenerator()
page_tsx = gen.render_page(course)
layout_tsx = gen.render_layout(course)

# Sentinela: zero vazamento do cliente default
forbidden = ["alexandrecaramaschi.com", "Alexandre Caramaschi", "Brasil GEO"]
leaks = [t for t in forbidden if t in page_tsx or t in layout_tsx]
assert not leaks, f"VAZAMENTO do default no TSX Herreira: {leaks}"
print(f"  page.tsx:   {len(page_tsx)} chars, sem vazamento do default")
print(f"  layout.tsx: {len(layout_tsx)} chars, sem vazamento do default")

# Presença
assert "Patrícia Caramaschi" in page_tsx
assert "Herreira Joias" in page_tsx
assert "herreirasemijoias.com.br" in page_tsx
print(f"  Autor Patrícia presente: OK")
print(f"  Company Herreira presente: OK")
print(f"  Domínio Herreira presente: OK")

banner("7. Escrita em output/clients/herreira/approved/")
out_dir = ROOT / "output" / "clients" / "herreira" / "approved"
out_dir.mkdir(parents=True, exist_ok=True)
page_path, layout_path = gen.write(course, out_dir)
print(f"  {page_path}")
print(f"  {layout_path}")

banner("8. Resumo")
print(f"  Curso:     {course.titulo}")
print(f"  Slug:      {course.slug}")
print(f"  Módulos:   {len(course.steps)}")
print(f"  Duração:   {course.duracao_total_minutos} min ({course.duracao_display})")
print(f"  Nível:     {course.nivel.value}")
print(f"  VG score:  {result.voice_guard_score}/100 (threshold {client.voice_guard.min_score})")
print()
print("Próximo passo: na pasta herreira, rode")
print("  bash scripts/sync-cursos.sh introducao-as-semijoias")
