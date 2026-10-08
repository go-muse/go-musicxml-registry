#!/usr/bin/env python3
"""Offline integrity checks for the curated MusicXML 4.0 research snapshot."""

import argparse
import collections
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/validation/registry"
MANIFEST = ROOT / "MANIFEST.json"
SKIP_PARTS = {".git", "__pycache__"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)


def included_files(base):
    result = []
    for path in base.rglob("*"):
        relative = path.relative_to(base)
        if any(part in SKIP_PARTS for part in relative.parts):
            continue
        if path.name == ".DS_Store" or path.suffix in {".pyc", ".pyo"}:
            continue
        require(not path.is_symlink(), f"Unexpected symlink: {relative}")
        if path.is_file():
            result.append(path)
    return sorted(result)


def digest_entry(path, base):
    raw = path.read_bytes()
    return {
        "path": path.relative_to(base).as_posix(),
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def check_manifest(path, base):
    data = read_json(path)
    entries = data["files"]
    paths = [entry["path"] for entry in entries]
    require(len(paths) == len(set(paths)), f"Duplicate paths in {path.name}")
    actual = {p.relative_to(base).as_posix(): p for p in included_files(base) if p != path}
    require(set(paths) == set(actual), f"Manifest file coverage mismatch: {path}")
    for entry in entries:
        require(entry == digest_entry(actual[entry["path"]], base),
                f"Manifest digest/size mismatch: {entry['path']}")
    return len(entries)


def write_manifest():
    entries = [digest_entry(p, ROOT) for p in included_files(ROOT) if p != MANIFEST]
    data = {
        "format": "go-musicxml-registry-manifest-1",
        "snapshot_date": "2026-10-08",
        "scope": "All repository files except this manifest, .git, Python bytecode/cache, and .DS_Store. Paths are relative to the repository root.",
        "files": entries,
    }
    MANIFEST.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def check_unique(records, key, count, label):
    require(len(records) == count, f"Unexpected {label} count: {len(records)} != {count}")
    values = [record[key] for record in records]
    require(len(set(values)) == count, f"Duplicate {label} {key}")
    return set(values)


def check_research():
    catalog = read_json(REGISTRY / "catalog.json")["records"]
    ids = check_unique(catalog, "id", 2560, "catalog")
    require(collections.Counter(r["registry_origin"] for r in catalog) == {"XSD": 2218, "prose": 342},
            "Catalog origin counts differ")
    for record in catalog:
        require(record["id"] == record["record"]["id"], f"Wrapper ID mismatch: {record['id']}")
    xsd_ids = {r["id"] for r in catalog if r["registry_origin"] == "XSD"}
    prose_ids = ids - xsd_ids
    occurrences = read_json(REGISTRY / "xsd/occurrence-registry.json")["occurrences"]
    occurrence_ids = check_unique(occurrences, "id", 2939, "XSD occurrence")
    property_ids = {o["id"] + "@" + name for o in occurrences for name in o["attributes"]}
    require(len(property_ids) == 3958, "Explicit-property count differs")
    mapped_properties = set()
    inverse = collections.defaultdict(set)
    for entry in catalog:
        if entry["registry_origin"] != "XSD":
            continue
        record = entry["record"]
        require(set(record.get("source_occurrence_ids", [])) <= occurrence_ids,
                f"Unknown source occurrence in {entry['id']}")
        properties = set(record.get("source_property_ids", []))
        require(properties <= property_ids, f"Unknown property in {entry['id']}")
        mapped_properties.update(properties)
        if record.get("category") not in {"language_semantics", "builtin_datatype"}:
            for occurrence_id in record.get("source_occurrence_ids", []):
                inverse[occurrence_id].add(entry["id"])
    require(mapped_properties == property_ids, "Unmapped explicit properties")
    mapping = read_json(REGISTRY / "xsd/occurrence-requirement-map.json")["mapping"]
    require(check_unique(mapping, "occurrence_id", 2939, "occurrence mapping") == occurrence_ids,
            "Occurrence mapping coverage differs")
    actual_mapping = {r["occurrence_id"]: set(r["requirement_ids"]) for r in mapping}
    require(actual_mapping == dict(inverse), "Occurrence-to-contract map differs from catalog inverse")
    references = read_json(REGISTRY / "xsd/reference-graph.json")["references"]
    check_unique(references, "id", 1515, "QName reference")
    semantics = read_json(REGISTRY / "xsd/language-semantics.json")
    builtin_ids = {entry["id"] for entry in semantics["builtin_types"]}
    for reference in references:
        require(reference["source_occurrence_id"] in occurrence_ids, "Unknown QName source")
        require(reference["target"].get("id") in occurrence_ids | builtin_ids,
                f"Unknown QName target: {reference['target']}")
    issues = read_json(REGISTRY / "issues.json")["issues"]
    issue_ids = check_unique(issues, "id", 28, "issue")
    relations = read_json(REGISTRY / "reconciliation.json")["relations"]
    require(check_unique(relations, "prose_id", 342, "prose reconciliation") == prose_ids,
            "Prose reconciliation coverage differs")
    for relation in relations:
        require(set(relation["related_xsd_contract_ids"]) <= xsd_ids, "Unknown related XSD contract")
    ledger = read_json(REGISTRY / "prose/coverage-ledger.json")
    check_unique(ledger["page_coverage"], "source_id", 974, "page coverage")
    check_unique(ledger["annotation_coverage"], "id", 642, "annotation coverage")
    for annotation in ledger["annotation_coverage"]:
        require(set(annotation["rule_ids"]) <= ids, "Unknown annotation rule reference")
        require(set(annotation["issue_ids"]) <= issue_ids, "Unknown annotation issue reference")
    examples = read_json(REGISTRY / "rule-definition-examples.json")["examples"]
    check_unique(examples, "id", 6, "illustrative rule")
    for example in examples:
        require(set(example["requirement_ids"]) <= ids, "Unknown illustrative requirement reference")


def check_local_links():
    checked = 0
    for path in included_files(ROOT):
        if path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        references = {m[1].strip().casefold(): m[2] for m in
                      re.finditer(r"(?m)^\s*\[([^\]]+)\]:\s*<?([^\s>]+)>?", text)}
        targets = [m[1] for m in re.finditer(r"\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)", text)]
        for match in re.finditer(r"\[([^\]]+)\]\[([^\]]*)\]", text):
            key = (match[2] or match[1]).strip().casefold()
            require(key in references, f"Undefined Markdown reference in {path}: {key}")
            targets.append(references[key])
        targets.extend(references.values())
        for target in targets:
            parts = urlsplit(target)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            resolved = (path.parent / unquote(parts.path)).resolve()
            require(resolved.is_relative_to(ROOT), f"Local link leaves repository: {path}: {target}")
            require(resolved.exists(), f"Broken local Markdown link: {path}: {target}")
            checked += 1
    return checked


def check_initial_import():
    provenance = read_json(ROOT / "provenance/initial-import.json")
    expected_paths = {entry["path"] for entry in provenance["files"]}
    actual_paths = {p.relative_to(ROOT).as_posix() for p in included_files(ROOT / "docs/validation")}
    require(expected_paths == actual_paths and len(expected_paths) == 28, "Initial-import tree differs")
    for entry in provenance["files"]:
        path = ROOT / entry["path"]
        raw = path.read_bytes()
        sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        require(sha == entry["git_blob_sha1"], f"Imported Git blob differs: {entry['path']}")
        require(len(raw) == entry["bytes"] and hashlib.sha256(raw).hexdigest() == entry["sha256"],
                f"Imported SHA-256/size differs: {entry['path']}")
    raw = (ROOT / "LICENSE").read_bytes()
    sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    require(sha == provenance["license_source"]["git_blob_sha1"], "Source MIT license differs")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-import", action="store_true", help="Also verify every byte of the initial pinned import")
    parser.add_argument("--write-manifest", action="store_true", help="Regenerate only the repository-wide MANIFEST.json")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest()
        print("Updated MANIFEST.json; run validation separately.")
        return 0
    json_files = [p for p in included_files(ROOT) if p.suffix == ".json"]
    for path in json_files:
        read_json(path)
    check_research()
    local_links = check_local_links()
    registry_files = check_manifest(REGISTRY / "manifest.json", REGISTRY)
    repository_files = check_manifest(MANIFEST, ROOT)
    if args.check_import:
        check_initial_import()
    print(f"PASS: {len(json_files)} JSON files; 2,560 catalog records; 28 issues; 2,939 XSD occurrences; "
          f"3,958 properties; 1,515 QName references; 974 pages; 642 annotations; six examples; "
          f"{local_links} local Markdown targets; {registry_files} registry manifest entries; "
          f"{repository_files} repository manifest entries.")
    if args.check_import:
        print("PASS: all 28 imported files and source LICENSE match the pinned Git blob identities.")
    print("Integrity checks only; no runtime conformance or fresh upstream-source audit claimed.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, KeyError, OSError, TypeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
