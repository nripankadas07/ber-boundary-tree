# Research — 22 October 2026

Demand is **inferred** from this workflow: A nested length can escape its parent even when the overall byte stream looks plausible in a hex dump.

[Exact stars-desc GitHub query](https://github.com/search?q=BER%20TLV%20sort%3Astars-desc&type=repositories), observed 2026-10-22T06:18:36.315Z. Highest-star relevant comparable found in the inspected pool: `wbond/asn1crypto`. Keywords are narrow; established comparables were supplemented directly. The difference-constraints keyword results were mostly unrelated and do not establish market coverage.

| Comparable | Stars | Last push | GitHub license metadata | Workflow and setup |
| --- | ---: | --- | --- | --- |
| [wbond/asn1crypto](https://github.com/wbond/asn1crypto) | 363 | 2026-07-18T16:57:21Z | MIT | Pure Python BER/DER parsing and serialization with schemas for common cryptographic structures. |
| [evsinev/ber-tlv](https://github.com/evsinev/ber-tlv) | 140 | 2021-12-11T02:25:14Z | Apache-2.0 | Java/Maven TLV parser and builder, including payment-oriented value types; tag semantics differ from strict ASN.1. |
| [pyasn1/pyasn1](https://github.com/pyasn1/pyasn1) | 53 | 2026-08-10T20:31:34Z | BSD-2-Clause | Python ASN.1 types and BER/CER/DER codecs, pip package and protocol/schema workflows. |

## Choice and tradeoffs

Emit exact BER parent/header/value boundaries and byte-offset errors without decoding application values. Existing byte dumps and image/chunk tools do not parse ASN.1 tag/length nesting. This preserves structural offsets and ASN.1 tag classes.

The established alternatives are broader and may be the right choice for their supported ecosystem. Our small CLI offers one dependency-free runtime and an inspectable JSON report for the stated subset. It sacrifices generality and may reject valid real-world input outside that subset. READMEs/current docs/source and sampled issues were inspected for workflow context; this does not prove competitor feature absence. ATL explicitly supports WAV CUE/LIST, NetworkX explicitly returns negative cycles, and RLEMaskLib performs mask operations without full raster expansion. Our example proves only our behavior.

Installability and first-result instructions are documented above and in upstream READMEs. Competitor clean installs, time to first useful result, reliability, support response and performance were **not measured**. No superiority, adoption or global ranking claim. Stars are research context only. [Exact provenance and sampled issues/PRs](RESEARCH_PROVENANCE.json). Inconclusive GitHub license metadata is not a legal conclusion; NetworkX README states BSD3, Z3 README MIT, and Knossos README EPL. No implementation is reused.

Primary references:
- https://www.itu.int/rec/dologin_pub.asp?id=T-REC-X.690-202102-I%21%21PDF-E&lang=e&type=items
