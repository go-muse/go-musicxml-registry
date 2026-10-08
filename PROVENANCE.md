# Provenance and integrity

## Initial curated import

The complete 28-file `docs/validation/` tree was copied from
[go-muse/go-musicxml commit a7927e591e817ec8fddaab2ee4d33ccf80c37bd0](https://github.com/go-muse/go-musicxml/tree/a7927e591e817ec8fddaab2ee4d33ccf80c37bd0/docs/validation),
the research revision in [PR #11](https://github.com/go-muse/go-musicxml/pull/11).
The copied files total 16,040,633 bytes.

Each imported file was checked against the Git blob SHA-1 and size returned by
the source commit's complete, non-truncated recursive Git tree. The local import
does not alter any research record, English addition, source locator, hash,
classification, question, or historical guide. No files from the product-code
tree, product tests, corpora, or dependencies are imported.

[initial-import.json](provenance/initial-import.json) records those source blob
IDs and local SHA-256 values. The source project's LICENSE is also preserved
verbatim, with its source blob ID recorded separately. New top-level guides,
notices, and integrity tooling describe this standalone packaging.

## Upstream evidence

The research sources are the dated
[MusicXML 4.0 publication](https://www.w3.org/2021/06/musicxml40/) and
[release commit 799e2defb2ece0ae7bafe08dcbcac25b2c631d53](https://github.com/w3c-cg/musicxml/tree/799e2defb2ece0ae7bafe08dcbcac25b2c631d53),
plus the external standards identified in individual records. The release is a
Final Community Group Report, not a W3C Recommendation.

The schema provenance, archive provenance, coverage dispositions, and their
verification limits are preserved in the registry. Import verification proves
that this package matches its curated source; it does not retroactively upgrade
earlier research checks to fresh raw-source downloads or full normative closure.

See [sources and coverage](docs/validation/sources-and-coverage.md),
[XSD source provenance](docs/validation/registry/xsd/source-provenance.json),
[archive provenance](docs/validation/registry/prose/github-archive-provenance.json),
and [original packaging provenance](docs/validation/registry/packaging-provenance.json).

## Three distinct integrity layers

1. Upstream-source fingerprints identify the schema, HTML, archive, or annotated
   source representation reviewed by the research run.
2. The preserved [registry manifest](docs/validation/registry/manifest.json)
   fingerprints the curated registry publication. Its paths are relative to
   `docs/validation/registry/`; it excludes itself.
3. [MANIFEST.json](MANIFEST.json) fingerprints this standalone repository,
   including all imported guides, the preserved registry manifest, license
   notices, and validation tooling. Its paths are relative to the repository
   root; it excludes itself and Git/local cache metadata.

Git blob identities in the initial-import record provide an additional direct
comparison with the pinned source repository. None of these checksums is a
digital signature or a proof that an interpretation is correct.

## Publication and later changes

Creating this separate repository does not modify the original library, branch,
or PR. The source pin remains historical even if that PR later changes or merges.
There is no automatic synchronization. Any future re-import must name an exact
source commit, verify every imported file, and describe scope and semantic
changes. Keep original evidence and third-party attribution when adding derived
views or interpretations.
