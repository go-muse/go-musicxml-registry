# Editing and validating the registry

This repository begins with a byte-for-byte curated research snapshot. The
research records are evidence for review, not approved executable rules.

## Changes to research evidence

- Preserve stable record IDs and original source locators. Do not silently reuse
  an ID for a different obligation or interpretation.
- Keep original bilingual fields. Add translations explicitly rather than
  overwriting the evidence or silently changing the classification.
- Distinguish source facts, interpretation, open decisions, implementation
  mappings, and test results. Do not equate reviewed-source counts with runtime
  coverage or count overlapping clauses as independent failures.
- Cite exact source versions. Document changed semantics, provenance limits,
  exclusions, and uncertainty alongside the affected records.
- Update relevant issue, reconciliation, and coverage records together. Keep
  third-party notices and the scope of their licenses intact.

The initial-import record is historical evidence. Do not rewrite its source
commit or checksums to make a later edit appear to be part of the original
snapshot. After intentional imported-file changes, `--check-import` will report
the differences; record a new versioned provenance record and update the
validation policy in the same reviewed change.

## Local validation

Python 3.10+ and the standard library are sufficient:

```sh
python3 scripts/validate_registry.py --check-import
```

The command parses all JSON with duplicate-key detection; checks initial research
counts, unique IDs, source-occurrence and property links, XSD/prose
reconciliation, coverage-record uniqueness, local Markdown link targets, and
the two manifests; and optionally verifies all initial import bytes against the
pinned Git blobs. It is an integrity check, not validation of MusicXML scores or
an independent re-audit of the specification. It does not fetch external links.

After an intentional edit, regenerate the applicable manifest only after
reviewing the diff. `--write-manifest` updates only the repository-wide manifest;
the preserved registry manifest must be deliberately updated if registry bytes
change. Run validation without `--check-import` to assess the changed working
tree, and retain the initial-import record as historical provenance.

```sh
python3 scripts/validate_registry.py --write-manifest
python3 scripts/validate_registry.py
git diff --check
```

Current counts are explicit initial-snapshot invariants in the validator. A
reviewed extension must update them and explain the new coverage boundaries;
loosening an invariant simply to make a failing check pass is not sufficient.

This repository contains no product code. Go library tests, runtime rule
implementation, API changes, source migration, and synchronization with
go-musicxml require separate changes in the appropriate repository.
