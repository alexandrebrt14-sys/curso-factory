"""Indexador de cursos: gera chunks semânticos e embeddings para busca vetorial.

Lê os dados de cursos do page.tsx da landing-page-geo, gera chunks
(course, course_decision, module, faq), cria embeddings via OpenAI
text-embedding-3-small e faz upsert no Supabase edu_documents.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

# ───────────────────── Configuração ─────────────────────

# Carrega chaves do geo-orchestrator/.env (fonte de verdade)
_ENV_PATH = Path("C:/Sandyboxclaude/geo-orchestrator/.env")
load_dotenv(_ENV_PATH)

import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
SUPABASE_URL = os.environ.get("NEXT_PUBLIC_SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")

LANDING_PAGE_DIR = Path("C:/Sandyboxclaude/landing-page-geo")
COURSES_FILE = LANDING_PAGE_DIR / "src" / "app" / "educacao" / "page.tsx"

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMS = 1536
OPENAI_EMBED_URL = "https://api.openai.com/v1/embeddings"
BATCH_SIZE = 20  # Chunks por chamada de embedding (limite da API: 2048)
RATE_LIMIT_PAUSE = 1.0  # Segundos entre batches para respeitar rate limits

console = Console()


# ───────────────────── Tipos auxiliares ─────────────────────

class CourseData:
    """Dados de um curso extraídos do TypeScript."""

    def __init__(
        self,
        id: str,
        title: str,
        description: str,
        href: str,
        modules: int,
        duration: str,
        level: str,
        tags: list[str],
    ):
        self.id = id
        self.title = title
        self.description = description
        self.href = href
        self.modules = modules
        self.duration = duration
        self.level = level
        self.tags = tags

    def __repr__(self) -> str:
        return f"CourseData(id={self.id!r}, title={self.title!r})"


class Chunk:
    """Um chunk semântico pronto para embedding e upsert."""

    def __init__(self, kind: str, course_id: str, title: str, body: str, metadata: dict[str, Any]):
        self.kind = kind
        self.course_id = course_id
        self.title = title
        self.body = body
        self.metadata = metadata
        self.embedding: list[float] | None = None
        # ID determinístico baseado no conteúdo
        self.doc_id = hashlib.sha256(
            f"{kind}:{course_id}:{title}:{body[:200]}".encode()
        ).hexdigest()[:24]


# ───────────────────── Parser do TypeScript ─────────────────────

def parse_courses_from_tsx(file_path: Path) -> list[CourseData]:
    """Extrai dados de cursos do page.tsx usando regex.

    Faz parsing simplificado do array TypeScript `const courses: CourseData[]`.
    Não tenta interpretar JSX ou imports, apenas os objetos literais.
    """
    content = file_path.read_text(encoding="utf-8")

    # Localiza o array de cursos
    match = re.search(r"const courses:\s*CourseData\[\]\s*=\s*\[", content)
    if not match:
        console.print("[red]Erro: array de cursos não encontrado no arquivo.[/red]")
        return []

    start = match.end()

    # Encontra o fechamento do array (contando colchetes)
    depth = 1
    pos = start
    while pos < len(content) and depth > 0:
        if content[pos] == "[":
            depth += 1
        elif content[pos] == "]":
            depth -= 1
        pos += 1

    array_body = content[start : pos - 1]

    # Extrai cada objeto { ... } do array
    courses: list[CourseData] = []
    # Usa regex para encontrar cada bloco de curso
    obj_pattern = re.compile(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", re.DOTALL)

    for obj_match in obj_pattern.finditer(array_body):
        obj_text = obj_match.group()

        # Extrai campos individuais
        def extract_str(field: str) -> str:
            m = re.search(rf'{field}:\s*["\'](.+?)["\']', obj_text)
            if m:
                return m.group(1)
            # Tenta string multilinha com template literal ou concatenação
            m = re.search(rf"{field}:\s*\n?\s*\"(.+?)\"", obj_text, re.DOTALL)
            if m:
                return m.group(1).strip()
            return ""

        def extract_int(field: str) -> int:
            m = re.search(rf"{field}:\s*(\d+)", obj_text)
            return int(m.group(1)) if m else 0

        def extract_tags(field: str) -> list[str]:
            m = re.search(rf"{field}:\s*\[([^\]]*)\]", obj_text)
            if not m:
                return []
            raw = m.group(1)
            return [t.strip().strip("\"'") for t in raw.split(",") if t.strip().strip("\"'")]

        course_id = extract_str("id")
        if not course_id:
            continue

        # Descrição pode estar em linha seguinte (padrão multilinha do TS)
        desc_match = re.search(
            r'description:\s*\n?\s*"((?:[^"\\]|\\.)*)"|description:\s*"((?:[^"\\]|\\.)*)"',
            obj_text,
            re.DOTALL,
        )
        description = ""
        if desc_match:
            description = (desc_match.group(1) or desc_match.group(2) or "").strip()

        courses.append(
            CourseData(
                id=course_id,
                title=extract_str("title"),
                description=description,
                href=extract_str("href"),
                modules=extract_int("modules"),
                duration=extract_str("duration"),
                level=extract_str("level"),
                tags=extract_tags("tags"),
            )
        )

    console.print(f"[green]{len(courses)} cursos extraidos do TypeScript.[/green]")
    return courses


def parse_faqs_from_tsx(file_path: Path) -> list[dict[str, str]]:
    """Extrai itens de FAQ do page.tsx."""
    content = file_path.read_text(encoding="utf-8")

    match = re.search(r"const faqItems\s*=\s*\[", content)
    if not match:
        return []

    start = match.end()
    depth = 1
    pos = start
    while pos < len(content) and depth > 0:
        if content[pos] == "[":
            depth += 1
        elif content[pos] == "]":
            depth -= 1
        pos += 1

    array_body = content[start : pos - 1]

    faqs: list[dict[str, str]] = []
    # Extrai pares q/a
    faq_pattern = re.compile(
        r'q:\s*"((?:[^"\\]|\\.)*)"\s*,\s*a:\s*(?:"((?:[^"\\]|\\.)*)"|`((?:[^`\\]|\\.)*)`)',
        re.DOTALL,
    )
    for m in faq_pattern.finditer(array_body):
        q = m.group(1).strip()
        a = (m.group(2) or m.group(3) or "").strip()
        if q and a:
            faqs.append({"q": q, "a": a})

    console.print(f"[green]{len(faqs)} FAQs extraidas.[/green]")
    return faqs


# ───────────────────── Geração de chunks ─────────────────────

def _prerequisites_for_level(level: str) -> str:
    """Gera texto de pré-requisitos baseado no nível do curso."""
    level_lower = level.lower()
    if "iniciante" in level_lower:
        return "Nenhum pré-requisito. Ideal para quem está começando do zero."
    elif "intermediário" in level_lower or "intermediario" in level_lower:
        return "Conhecimento básico de tecnologia e familiaridade com ferramentas digitais."
    elif "avançado" in level_lower or "avancado" in level_lower:
        return "Experiência prévia na área. Recomendável ter completado cursos de nível intermediário."
    else:
        return "Consulte a descrição do curso para pré-requisitos específicos."


def _derive_skills(tags: list[str], description: str) -> str:
    """Deriva skills de saída a partir das tags e descrição."""
    skills = []
    for tag in tags[:4]:
        skills.append(f"domínio de {tag}")
    # Adiciona skills derivadas de palavras-chave na descrição
    keywords_map = {
        "automação": "automação de processos",
        "API": "integração via API",
        "dashboard": "criação de dashboards",
        "deploy": "deploy de aplicações",
        "Schema": "implementação de Schema.org",
        "estratégia": "planejamento estratégico",
    }
    for keyword, skill in keywords_map.items():
        if keyword.lower() in description.lower() and skill not in skills:
            skills.append(skill)
            break
    return ", ".join(skills) if skills else "competências técnicas na área"


def _derive_when(description: str, level: str) -> str:
    """Deriva contexto de 'quando faz sentido' a partir da descrição."""
    level_lower = level.lower()
    if "iniciante" in level_lower:
        return "Quando você está começando na área e precisa de uma base sólida."
    elif "avançado" in level_lower or "avancado" in level_lower:
        return "Quando você já tem experiência e quer se aprofundar com técnicas avançadas."
    else:
        return "Quando você quer expandir suas competências e aplicar técnicas profissionais."


def generate_chunks(courses: list[CourseData], faqs: list[dict[str, str]]) -> list[Chunk]:
    """Gera todos os chunks semânticos a partir dos cursos e FAQs."""
    chunks: list[Chunk] = []

    for course in courses:
        # 1. Chunk de visão geral do curso (kind='course')
        course_body = f"{course.title}. {course.description}"
        chunks.append(
            Chunk(
                kind="course",
                course_id=course.id,
                title=course.title,
                body=course_body,
                metadata={
                    "level": course.level,
                    "duration": course.duration,
                    "modules": course.modules,
                    "tags": course.tags,
                    "href": course.href,
                },
            )
        )

        # 2. Chunk sintético de decisão (kind='course_decision')
        tags_str = ", ".join(course.tags)
        prerequisites = _prerequisites_for_level(course.level)
        skills = _derive_skills(course.tags, course.description)
        when = _derive_when(course.description, course.level)

        decision_body = (
            f"Para quem é: profissionais que buscam {tags_str}. "
            f"Nível: {course.level}. "
            f"Duração: {course.duration}. "
            f"{course.modules} módulos. "
            f"Pré-requisitos: {prerequisites} "
            f"Skills de saída: {skills}. "
            f"Quando faz sentido: {when}"
        )

        chunks.append(
            Chunk(
                kind="course_decision",
                course_id=course.id,
                title=f"Decisão: {course.title}",
                body=decision_body,
                metadata={
                    "level": course.level,
                    "duration": course.duration,
                    "modules": course.modules,
                    "tags": course.tags,
                    "href": course.href,
                },
            )
        )

        # 3. Chunks de módulos (kind='module')
        # Como ainda não parseamos conteúdo individual de módulos,
        # geramos um chunk por módulo usando o contexto do curso
        for i in range(1, course.modules + 1):
            module_body = (
                f"Módulo {i} de {course.modules} do curso {course.title}. "
                f"{course.description} "
                f"Nível: {course.level}. Tags: {tags_str}."
            )
            chunks.append(
                Chunk(
                    kind="module",
                    course_id=course.id,
                    title=f"{course.title} - Módulo {i}",
                    body=module_body,
                    metadata={
                        "level": course.level,
                        "module_number": i,
                        "total_modules": course.modules,
                        "href": course.href,
                    },
                )
            )

    # 4. Chunks de FAQ (kind='faq')
    for i, faq in enumerate(faqs):
        faq_body = f"Pergunta: {faq['q']} Resposta: {faq['a']}"
        chunks.append(
            Chunk(
                kind="faq",
                course_id="global",
                title=faq["q"],
                body=faq_body,
                metadata={"faq_index": i},
            )
        )

    console.print(f"[green]{len(chunks)} chunks gerados no total.[/green]")
    return chunks


# ───────────────────── Embeddings via OpenAI ─────────────────────

def embed_chunks(chunks: list[Chunk], client: httpx.Client) -> list[Chunk]:
    """Gera embeddings para todos os chunks em batches.

    Usa text-embedding-3-small (1536 dimensões).
    Respeita rate limits com pausa entre batches.
    """
    total = len(chunks)
    embedded = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        console=console,
    ) as progress:
        task = progress.add_task("Gerando embeddings...", total=total)

        for i in range(0, total, BATCH_SIZE):
            batch = chunks[i : i + BATCH_SIZE]
            texts = [c.body for c in batch]

            retries = 0
            max_retries = 3
            while retries < max_retries:
                try:
                    resp = client.post(
                        OPENAI_EMBED_URL,
                        headers={
                            "Authorization": f"Bearer {OPENAI_API_KEY}",
                            "Content-Type": "application/json",
                        },
                        json={
                            "model": EMBEDDING_MODEL,
                            "input": texts,
                            "dimensions": EMBEDDING_DIMS,
                        },
                        timeout=30.0,
                    )

                    if resp.status_code == 429:
                        # Rate limit: espera e tenta novamente
                        retry_after = float(resp.headers.get("retry-after", "5"))
                        console.print(
                            f"[yellow]Rate limit atingido. Aguardando {retry_after}s...[/yellow]"
                        )
                        time.sleep(retry_after)
                        retries += 1
                        continue

                    resp.raise_for_status()
                    data = resp.json()

                    for item in data["data"]:
                        idx = item["index"]
                        batch[idx].embedding = item["embedding"]

                    embedded += len(batch)
                    progress.update(task, completed=embedded)
                    break

                except httpx.HTTPStatusError as e:
                    console.print(f"[red]Erro HTTP {e.response.status_code}: {e.response.text}[/red]")
                    retries += 1
                    if retries >= max_retries:
                        console.print("[red]Maximo de tentativas atingido. Abortando batch.[/red]")
                        break
                    time.sleep(2 ** retries)

                except httpx.RequestError as e:
                    console.print(f"[red]Erro de conexão: {e}[/red]")
                    retries += 1
                    if retries >= max_retries:
                        break
                    time.sleep(2 ** retries)

            # Pausa entre batches para respeitar rate limits
            if i + BATCH_SIZE < total:
                time.sleep(RATE_LIMIT_PAUSE)

    successful = sum(1 for c in chunks if c.embedding is not None)
    console.print(f"[green]{successful}/{total} chunks com embedding gerado.[/green]")
    return chunks


# ───────────────────── Upsert no Supabase ─────────────────────

def upsert_to_supabase(chunks: list[Chunk], client: httpx.Client) -> int:
    """Faz upsert dos chunks na tabela edu_documents do Supabase.

    Usa a REST API do Supabase com header Prefer: resolution=merge-duplicates
    para upsert baseado na coluna id.
    """
    url = f"{SUPABASE_URL}/rest/v1/edu_documents"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates",
    }

    # Filtra chunks sem embedding
    valid_chunks = [c for c in chunks if c.embedding is not None]
    if not valid_chunks:
        console.print("[red]Nenhum chunk com embedding para inserir.[/red]")
        return 0

    inserted = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        console=console,
    ) as progress:
        task = progress.add_task("Upsert no Supabase...", total=len(valid_chunks))

        for i in range(0, len(valid_chunks), BATCH_SIZE):
            batch = valid_chunks[i : i + BATCH_SIZE]
            rows = []

            for chunk in batch:
                rows.append(
                    {
                        "id": chunk.doc_id,
                        "kind": chunk.kind,
                        "course_id": chunk.course_id,
                        "title": chunk.title,
                        "body": chunk.body,
                        "embedding": chunk.embedding,
                        "metadata": json.dumps(chunk.metadata, ensure_ascii=False),
                    }
                )

            retries = 0
            max_retries = 3
            while retries < max_retries:
                try:
                    resp = client.post(
                        url,
                        headers=headers,
                        json=rows,
                        timeout=30.0,
                    )

                    if resp.status_code == 429:
                        retry_after = float(resp.headers.get("retry-after", "5"))
                        console.print(
                            f"[yellow]Rate limit Supabase. Aguardando {retry_after}s...[/yellow]"
                        )
                        time.sleep(retry_after)
                        retries += 1
                        continue

                    if resp.status_code in (200, 201):
                        inserted += len(batch)
                        progress.update(task, completed=inserted)
                        break
                    else:
                        console.print(
                            f"[red]Erro Supabase {resp.status_code}: {resp.text}[/red]"
                        )
                        retries += 1
                        if retries >= max_retries:
                            console.print(
                                f"[red]Falha no batch {i // BATCH_SIZE + 1}. "
                                f"{len(batch)} chunks não inseridos.[/red]"
                            )
                            break
                        time.sleep(2 ** retries)

                except httpx.RequestError as e:
                    console.print(f"[red]Erro de conexão com Supabase: {e}[/red]")
                    retries += 1
                    if retries >= max_retries:
                        break
                    time.sleep(2 ** retries)

    console.print(f"[green]{inserted}/{len(valid_chunks)} chunks inseridos no Supabase.[/green]")
    return inserted


# ───────────────────── Validação de configuração ─────────────────────

def validate_config() -> bool:
    """Valida que todas as variáveis de ambiente necessárias estão configuradas."""
    missing = []
    if not OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")
    if not SUPABASE_URL:
        missing.append("NEXT_PUBLIC_SUPABASE_URL")
    if not SUPABASE_KEY:
        missing.append("SUPABASE_SERVICE_ROLE_KEY")

    if missing:
        console.print(f"[red]Variáveis de ambiente ausentes: {', '.join(missing)}[/red]")
        console.print(f"[dim]Verifique o arquivo: {_ENV_PATH}[/dim]")
        return False

    if not COURSES_FILE.exists():
        console.print(f"[red]Arquivo de cursos não encontrado: {COURSES_FILE}[/red]")
        return False

    return True


# ───────────────────── Main ─────────────────────

def main() -> None:
    """Pipeline principal: parse -> chunks -> embed -> upsert."""
    console.rule("[bold blue]Course Indexer - Brasil GEO Educação[/bold blue]")

    # Validação
    if not validate_config():
        sys.exit(1)

    console.print(f"[dim]Fonte: {COURSES_FILE}[/dim]")
    console.print(f"[dim]Destino: {SUPABASE_URL}/rest/v1/edu_documents[/dim]")
    console.print()

    # 1. Extrai cursos e FAQs do TypeScript
    console.rule("1. Parsing do TypeScript")
    courses = parse_courses_from_tsx(COURSES_FILE)
    faqs = parse_faqs_from_tsx(COURSES_FILE)

    if not courses:
        console.print("[red]Nenhum curso encontrado. Abortando.[/red]")
        sys.exit(1)

    # 2. Gera chunks semânticos
    console.rule("2. Geração de chunks")
    chunks = generate_chunks(courses, faqs)

    # 3. Gera embeddings
    console.rule("3. Embeddings via OpenAI")
    with httpx.Client() as client:
        chunks = embed_chunks(chunks, client)

        # 4. Upsert no Supabase
        console.rule("4. Upsert no Supabase")
        inserted = upsert_to_supabase(chunks, client)

    # Resumo final
    console.rule("[bold green]Resumo[/bold green]")
    console.print(f"  Cursos processados: {len(courses)}")
    console.print(f"  FAQs processadas:   {len(faqs)}")
    console.print(f"  Chunks gerados:     {len(chunks)}")
    console.print(f"  Chunks inseridos:   {inserted}")
    console.print()


if __name__ == "__main__":
    main()
