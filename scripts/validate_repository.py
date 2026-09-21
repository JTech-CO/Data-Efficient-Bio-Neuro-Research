#!/usr/bin/env python3
"""Validate local links, reference IDs, bilingual chapter parity and JSON fixtures.
Does not test external URL availability or establish scientific validity.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit
from jsonschema import Draft202012Validator, FormatChecker
ROOT = Path(__file__).resolve().parents[1]


def validate() -> dict:
    errors: list[str] = []
    json_files = [p for p in ROOT.rglob("*.json") if ".venv" not in p.parts and "quality" not in p.parts]
    for p in json_files:
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except (ValueError, OSError) as e:
            errors.append(f"JSON {p.relative_to(ROOT)}: {e}")
    references = json.loads((ROOT / "references/references.json").read_text(encoding="utf-8"))
    ids = [r["id"] for r in references]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate reference IDs")
    known = set(ids)
    md_files = [p for p in ROOT.rglob("*.md") if ".venv" not in p.parts]
    local_links = 0
    for p in md_files:
        text = p.read_text(encoding="utf-8")
        if "" in text:
            errors.append(f"Nonportable chat citation in {p.relative_to(ROOT)}")
        unknown = set(re.findall(r"\[([RTD]\d{2})\]", text)) - known
        if unknown:
            errors.append(f"Unknown reference in {p.name}: {unknown}")
        outside_code = re.sub(r"```.*?```", "", text, flags=re.S)
        for href in re.findall(r"!?\[[^\]\n]*\]\(([^)\s]+)\)", outside_code):
            parts = urlsplit(href)
            if parts.scheme or href.startswith("#"):
                continue
            target = (p.parent / unquote(parts.path)).resolve()
            local_links += 1
            if not target.exists():
                errors.append(f"Broken local link: {p.relative_to(ROOT)} -> {href}")
            if target.name == "BIBLIOGRAPHY.md" and parts.fragment and parts.fragment.upper() not in known:
                errors.append(f"Unknown bibliography anchor: {href}")
    ko = {p.name for p in (ROOT / "docs/ko").glob("*.md")}
    en = {p.name for p in (ROOT / "docs/en").glob("*.md")}
    if ko != en:
        errors.append(f"Bilingual chapter mismatch: {ko ^ en}")
    validators = {}
    for stem in ("observation", "model_card"):
        schema = json.loads((ROOT / f"schemas/{stem}.schema.json").read_text())
        Draft202012Validator.check_schema(schema)
        validators[stem] = Draft202012Validator(schema, format_checker=FormatChecker())
        fixture = json.loads((ROOT / f"schemas/examples/{stem}.valid.json").read_text())
        for err in validators[stem].iter_errors(fixture):
            errors.append(f"Valid fixture failed: {stem}: {err.message}")
    negative = json.loads((ROOT / "schemas/examples/observation.invalid.json").read_text())
    if validators["observation"].is_valid(negative):
        errors.append("Negative provenance fixture was incorrectly accepted")
    runs = json.loads((ROOT / "examples/results/runs.json").read_text())
    for r in runs:
        if len(r["selected_indices"]) != r["n_queries"] or len(set(r["selected_indices"])) != r["n_queries"]:
            errors.append("Duplicate or inconsistent demo acquisition")
        if not 0 <= r["latent_pointwise_95_coverage"] <= 1:
            errors.append("Invalid demo coverage")
    report = {"status": "pass" if not errors else "fail", "errors": errors,
              "reference_records": len(ids), "paired_research_chapters": len(ko),
              "json_files_checked": len(json_files), "markdown_files_checked": len(md_files),
              "local_links_checked": local_links, "demo_budget_records": len(runs),
              "scope": "Internal structural validation only; not external-link, scientific, clinical or upstream-code validation."}
    return report


if __name__ == "__main__":
    report = validate()
    output = ROOT / "quality/validation_report.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["status"] == "pass" else 1)
