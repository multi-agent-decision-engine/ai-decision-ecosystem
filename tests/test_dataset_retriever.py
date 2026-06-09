"""Unit tests for DatasetRetriever (inference-time retrieval).

Bu testler gercek COMBINED_DATASET.json'a deginmez; gecici dosya ile
deterministik kanit uretir.
"""
import json
from pathlib import Path

import pytest

from app.domain.learning.dataset_retriever import DatasetRetriever, _load_records


@pytest.fixture
def tiny_dataset(tmp_path: Path) -> Path:
    data = [
        {"source": "Test", "budget": 5.0, "risk": 5, "readiness": 7, "decision": "APPROVE"},
        {"source": "Test", "budget": 6.0, "risk": 5, "readiness": 7, "decision": "REJECT"},
        {"source": "Test", "budget": 30.0, "risk": 4, "readiness": 4, "decision": "APPROVE"},
        {"source": "Test", "budget": 40.0, "risk": 5, "readiness": 3, "decision": "REJECT"},
    ]
    path = tmp_path / "tiny.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    # lru_cache hot key olabilir; her test icin path yeni oldugundan cakisma yok
    return path


def test_is_available_true_when_file_exists(tiny_dataset: Path):
    r = DatasetRetriever(dataset_path=str(tiny_dataset))
    assert r.is_available is True


def test_is_available_false_when_missing(tmp_path: Path):
    r = DatasetRetriever(dataset_path=str(tmp_path / "nope.json"))
    assert r.is_available is False


def test_find_similar_orders_by_distance(tiny_dataset: Path):
    r = DatasetRetriever(dataset_path=str(tiny_dataset))
    top, stats = r.find_similar(budget=5.5, risk=5, readiness=7, k=2)
    assert len(top) == 2
    # ilk iki kayit (budget 5/6) bizim sorguya en yakin olmali
    budgets = sorted(rec["budget"] for rec in top)
    assert budgets == [5.0, 6.0]
    assert stats["k"] == 2
    assert stats["decisions"] == {"APPROVE": 1, "REJECT": 1}


def test_format_for_prompt_includes_key_lines(tiny_dataset: Path):
    r = DatasetRetriever(dataset_path=str(tiny_dataset))
    block = r.format_for_prompt(budget=5.5, risk=5, readiness=7, k=2)
    assert "## Tarihsel Veri (benzer vakalar)" in block
    assert "Veriseti: 4 kayit" in block
    assert "Senaryona en benzer 2 vaka" in block
    assert "APPROVE: 1" in block and "REJECT: 1" in block
    assert "Butce araligi: $5M - $6M" in block
    assert "Risk araligi: 5 - 5" in block
    assert "REVISE yok" in block  # akademik durustluk notu


def test_format_for_prompt_empty_when_unavailable(tmp_path: Path):
    r = DatasetRetriever(dataset_path=str(tmp_path / "nope.json"))
    assert r.format_for_prompt(budget=5.0, risk=5, readiness=7) == ""


def test_load_records_is_cached(tiny_dataset: Path):
    # lru_cache hit oldugunu dolayli olarak teyit et — ikinci cagri ayni objeyi dondurmeli
    rec1 = _load_records(str(tiny_dataset))
    rec2 = _load_records(str(tiny_dataset))
    assert rec1 is rec2
