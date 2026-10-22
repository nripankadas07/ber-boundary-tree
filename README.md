# ber-boundary-tree

Emit exact BER parent/header/value boundaries and byte-offset errors without decoding application values.

For aSN.1 protocol developers locating a malformed definite-length BER boundary.

## Quickstart

Python3.10+; no runtime dependencies or external service. The wheel build needs setuptools and wheel from the normal Python registry. Linux shell:

```sh
git clone https://github.com/nripankadas07/ber-boundary-tree.git
cd ber-boundary-tree
python -m venv .venv
. .venv/bin/activate
python -m pip install .
ber-boundary-tree example.hex
```

The invented nested sequence reports four nodes with exact parent boundaries and preserves the octet-string value. [Expected report](example-output.json).

## Input and interpretation

Start from [example.hex](example.hex). Inputs are read only. Hex input accepts ASCII whitespace.

ASCII hex file<=1MiB decodes to<=128KiB. Definite lengths only,<=4 subsequent high-tag octets and4 long-length octets,depth<=32,<=5000 nodes. Multiple top-level siblings and empty input allowed. Reject truncation,parent overflow,indefinite length,EOC and nonminimal high tags. Nonminimal definite length forms remain accepted and explicitly flagged (BER permits them). Primitive bytes opaque,preview<=32 bytes. No ASN.1 schema/type/value checks, DER/CER validator, EMV-specific nonminimal tags such as9F02, padding, decryption,certificate verification or encoder.

Exit0 means analysis completed, including any infeasibility, NOT_LINEARIZABLE, UNKNOWN or reference finding. Inspect the report fields; exit0 is not a health assertion. Exit2 means malformed/unsupported input or I/O failure, with JSON error on stderr and no partial report. No live-system operations, network requests or credential reads occur. Reports may expose supplied identifiers and bytes; review before sharing.

## Verification

```sh
python -m unittest -v
python -m compileall -q ber_boundary_tree.py
python -m pip wheel --no-deps . -w dist
```

Nested/class/high-tag and nonminimal length cases, every truncation prefix, malformed parent boundaries, EOC/indefinite rejection and size/depth/node caps. [Validation record](VALIDATION.md). CI runs Python3.10/3.12/3.14 on Linux and the installed console outside checkout. Windows/macOS, production workloads and competitor performance remain untested.

## Scope and provenance

Alpha utility. Original AI-assisted code and invented fixtures; standard algorithms independently reimplemented. No third-party implementation/prose copied. MIT. [Candidate brief](BRIEF.json), [research](RESEARCH.md), [support](SUPPORT.md), [contributing](CONTRIBUTING.md), [security](SECURITY.md).

Existing byte dumps and image/chunk tools do not parse ASN.1 tag/length nesting. This preserves structural offsets and ASN.1 tag classes.
