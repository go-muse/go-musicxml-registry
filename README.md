# go-musicxml-registry

A standalone research registry for MusicXML 4.0 validation requirements,
source coverage, unresolved questions, and a proposed validation architecture.
It is intended for reviewing requirements and planning implementations.
It is not a runtime validator, an executable rule catalog, or a certification
of MusicXML conformance.

Repository: [go-muse/go-musicxml-registry](https://github.com/go-muse/go-musicxml-registry).

## Contents

The complete curated research snapshot is available as ordinary, unpacked files
under [docs/validation](docs/validation/README.md):

- [Catalog](docs/validation/registry/catalog.json): 2,560 records, comprising
  2,218 XSD contracts and 342 prose records, with original IDs and fields retained.
- [XSD evidence](docs/validation/registry/xsd/): 2,939 operative occurrences,
  3,958 explicit properties, and 1,515 QName reference tokens across six schemas.
- [Prose coverage](docs/validation/registry/prose/coverage-ledger.json): all 974
  scoped page records and 642 schema-annotation records with their dispositions.
- [Reconciliation](docs/validation/registry/reconciliation.json): links between
  XSD and prose evidence, with overlap and deduplication cautions.
- [Open questions](docs/validation/open-questions.md): 28 ambiguity, editorial,
  and dependency records with proposed dispositions.
- [Architecture proposal](docs/validation/architecture.md) and six
  [illustrative rule declarations](docs/validation/registry/rule-definition-examples.json).

Start with the [reading guide](docs/validation/README.md), then read
[sources and coverage](docs/validation/sources-and-coverage.md) before relying on
the counts. Catalog records are not independent mandatory executable predicates.

## Source and version pins

- MusicXML publication: [MusicXML 4.0, 1 June 2021](https://www.w3.org/2021/06/musicxml40/).
- Official release source: [w3c-cg/musicxml at
  799e2defb2ece0ae7bafe08dcbcac25b2c631d53](https://github.com/w3c-cg/musicxml/tree/799e2defb2ece0ae7bafe08dcbcac25b2c631d53).
- Curated research source: [go-muse/go-musicxml PR #11](https://github.com/go-muse/go-musicxml/pull/11),
  pinned to [a7927e591e817ec8fddaab2ee4d33ccf80c37bd0](https://github.com/go-muse/go-musicxml/tree/a7927e591e817ec8fddaab2ee4d33ccf80c37bd0/docs/validation).
- Research snapshot: 8 October 2026. The [existing-code map](docs/validation/existing-code-map.md)
  assesses go-musicxml product commit
  [e486735cd6e4537e839ff67704b7768a9df3bdb3](https://github.com/go-muse/go-musicxml/tree/e486735cd6e4537e839ff67704b7768a9df3bdb3).

The initial import preserves all 28 files in the source `docs/validation/` tree
byte for byte. [Import provenance](provenance/initial-import.json) records the
source paths, Git blob IDs, sizes, and SHA-256 checksums.

## Relationship to go-musicxml

[go-musicxml](https://github.com/go-muse/go-musicxml) is the separate Go library.
This repository holds its extracted research snapshot and review material.
There is no runtime, module, submodule, or automatic synchronization dependency.
The initial publication does not merge, remove, or modify the original PR.

The historical architecture and code-map documents are retained unchanged;
references to the "current library" refer to their pinned product commit, not
the moving head of go-musicxml. Future consumers should pin an exact registry
commit and record which requirements they implement. The proposed architecture,
API sketches, severity choices, and issue dispositions are not final decisions.

## Limits and open work

- The snapshot covers the scoped publication and schemas. It does not establish
  complete transitive closure over external normative standards.
- Source coverage is distinct from resolved semantics, executable predicates,
  model mapping, and implementation/test coverage. Those latter axes remain open.
- Original bilingual research fields are preserved. Additive English fields cover
  51 prose constraints, all 28 issues, and six examples; 291 other prose records
  still lack English descriptions or conditions.
- The original packaging intentionally omitted duplicate export views, raw HTML
  caches, downloaded archives, and the individual 14,569-block HTML hash index.
  Its checksum and aggregate counts remain; the omitted block evidence cannot be
  reconstructed from page summaries. This is the full curated registry, not the
  full raw research workspace.
- Schema-byte verification has documented limits, including the recorded
  `sounds.xsd` verification method and upstream/vendored `opus.xsd` differences.
  See [source coverage](docs/validation/sources-and-coverage.md) and
  [packaging provenance](docs/validation/registry/packaging-provenance.json).

## Validate and edit

Use Python 3.10 or newer. No third-party packages or network access are needed.

```sh
python3 scripts/validate_registry.py --check-import
```

This checks JSON parsing, IDs and counts, source-occurrence/property mappings,
cross-record links, local Markdown targets, both manifests, and byte-for-byte
identity with the initial pinned import. It does not run a MusicXML validator,
fetch upstream sources, or prove normative completeness.

For a change, preserve stable IDs and original evidence, record the source and
reason, distinguish translations from changed interpretations, and update the
relevant coverage and issue records. Read [CONTRIBUTING.md](CONTRIBUTING.md) before
changing imported data. To regenerate the repository manifest after a deliberate
change to repository-owned files, then verify it:

```sh
python3 scripts/validate_registry.py --write-manifest
python3 scripts/validate_registry.py
```

[MANIFEST.json](MANIFEST.json) covers every repository file except itself and
Git/local cache metadata. The separate, preserved
[registry manifest](docs/validation/registry/manifest.json) covers the curated
registry files. [PROVENANCE.md](PROVENANCE.md) explains the three checksum layers.

## Licensing

Original project contributions retain the source project's [MIT license](LICENSE).
Upstream MusicXML and other third-party source material retain their own terms
and attribution; they are not relicensed as project-owned MIT material.
See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for source-specific notices.
