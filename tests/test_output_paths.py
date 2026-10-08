"""Destinos intermediários do portal não recebem rascunhos nem catálogo."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.generators.metadata_sync import MetadataSync
from src.output_paths import validate_intermediate_output


@pytest.fixture
def portal(tmp_path, monkeypatch):
    root = tmp_path / "checkout-com-nome-livre"
    (root / "src/app/educacao").mkdir(parents=True)
    (root / "package.json").write_text(
        json.dumps({"name": "alexandrecaramaschi-com"}), encoding="utf-8"
    )
    (root / "next.config.ts").touch()
    monkeypatch.setattr("src.config.LANDING_PAGE_DIR", root)
    return root


@pytest.mark.parametrize("relative", ["public", "public/educacao/drafts", "src/generated"])
def test_rejects_reserved_directory_and_descendants(portal, relative):
    with pytest.raises(ValueError, match="Destino intermediário reservado"):
        validate_intermediate_output(portal / relative)
    assert not (portal / relative).exists()


def test_resolves_parent_segments(portal):
    with pytest.raises(ValueError):
        validate_intermediate_output(portal / "output/../public/drafts")


def test_allows_local_output_unrelated_public_and_tsx_destination(portal, tmp_path):
    for target in (tmp_path / "output", tmp_path / "outro/public", portal / "src/app/educacao"):
        validate_intermediate_output(target)


@pytest.mark.parametrize("missing", ["package.json", "next.config.ts", "src/app/educacao"])
def test_requires_every_identity_marker(portal, missing):
    marker = portal / missing
    marker.rmdir() if marker.is_dir() else marker.unlink()
    validate_intermediate_output(portal / "public")


@pytest.mark.parametrize("package", [{"name": "outro-portal"}, [], "inválido"])
def test_does_not_identify_other_or_invalid_package(portal, package):
    (portal / "package.json").write_text(
        json.dumps(package) if not isinstance(package, str) else package, encoding="utf-8"
    )
    validate_intermediate_output(portal / "public")


def test_catalog_fails_before_creating_reserved_target(portal, monkeypatch):
    target = portal / "src/generated/catalogo"
    sync = MetadataSync(output_dir=target)
    collect = Mock(side_effect=AssertionError("Não deveria coletar cursos"))
    monkeypatch.setattr(sync, "_collect_courses", collect)
    result = sync.sync()
    assert not result["ok"]
    assert "Destino intermediário reservado" in result["errors"][0]
    assert not target.exists()
    collect.assert_not_called()


def test_catalog_still_emits_local_artifact(portal, tmp_path, monkeypatch):
    sync = MetadataSync(output_dir=tmp_path / "output")
    monkeypatch.setattr(sync, "_collect_courses", lambda: [{"slug": "curso"}])
    assert sync.sync()["ok"]
    assert json.loads(sync.catalog_path.read_text(encoding="utf-8"))["course_count"] == 1


@pytest.mark.parametrize("explicit", [True, False])
def test_drafts_fail_before_llm_initialization(portal, monkeypatch, explicit):
    from src.orchestrator import Orchestrator

    factory = Mock(side_effect=AssertionError("Não deveria inicializar LLM"))
    monkeypatch.setattr("src.llm_client.make_llm_client", factory)
    client = SimpleNamespace(output_dir=portal / "public")
    with pytest.raises(ValueError, match="Destino intermediário reservado"):
        Orchestrator(
            cost_tracker=object(),
            client_context=client,
            drafts_dir=portal / "src/generated/drafts" if explicit else None,
        )
    assert not (portal / "public").exists()
    assert not (portal / "src/generated").exists()
    factory.assert_not_called()
