## [GADUREK-SEA-26] Breaking 2-Cores for Invertible Bloom Lookup Tables by Structure Prediction

**Citation:** Vojtěch Gaďurek, Pavel Veselý. "Breaking 2-Cores for Invertible Bloom Lookup Tables by Structure Prediction." 24th International Symposium on Experimental Algorithms (SEA 2026), LIPIcs Volume 371, pp. 19:1-19:24. DOI 10.4230/LIPIcs.SEA.2026.19.
**Retrieved:** ABSTRACT ONLY — NOT USABLE AS EVIDENCE. The file at sources/text/GADUREK-SEA-26.txt is the DROPS (Dagstuhl Research Online Publication Server) landing page for the paper — page metadata, the abstract, the BibTeX citation, author affiliations, funding statement, supplementary-material links, and the full reference list — not the 24-page paper body. Title and authors match the registry record exactly, so this is not a wrong-document mismatch; the full text simply was not fetched. The PDF (LIPIcs.SEA.2026.19.pdf, stated filesize 0.99 MB, 24 pages) exists at the same DOI and was not retrieved into this file.
**Source URL:** https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SEA.2026.19
**Domain:** D

### What it does
Per the abstract only (unverified against the full text): the paper addresses the case where an Invertible Bloom Lookup Table (IBLT) is too small relative to the set it encodes for the standard peeling decode to complete — a failure the paper calls a "2-core" occurring in the hypergraph formed by the encoding's hash assignments. Rather than treating this as a hard failure, the method the abstract describes adds a structure-aware predictor that is invoked whenever peeling decode gets stuck, to guess a missing element and let peeling continue, while leaving the IBLT's own encoding unchanged (only the decode procedure is modified). The abstract states this is demonstrated on k-mers (fixed-length substrings of a genome sequence, of length k) drawn from the symmetric difference of two closely related genomes, and separately describes a variant for large k that combines subsampling with a fingerprinting-based predictor.

### Measured results
None usable. The abstract states several figures — recovery of "27% more elements than the nominal IBLT size" from a proven weak matching-based predictor, an IBLT of "66% of the encoded set size" sufficing for k=31 with the genomic predictors, and an "O(M log M) bits" scaling result for large k versus "Theta(k*M) bits" for the standard IBLT — but the abstract does not state the dataset, genome pairs, set sizes, number of trials, or hardware behind any of these figures. Per this extraction's governing rule, a figure without its experimental conditions is not usable, so none of these numbers are recorded as evidence.

### Parameters
Not extractable from the landing page. The full text (not retrieved) would hold the IBLT cell-count and hash-count parameters used in the experiments, the predictor construction, and the genomic datasets used.

### Stated limitations
Not extractable from the landing page.

### Requirements it places on the rest of the system
Not extractable from the landing page. The abstract's claim that decoding is modified while "leaving the IBLT data structure unchanged" suggests the predictor-based decode is meant to be a drop-in replacement for standard IBLT peeling decode on the receiving side only, requiring no change to the sender's encoding — but this is a claim from the abstract, not a verified mechanism, and the specifics of what the predictor needs to observe (for example, access to a reference genome or a fingerprint table) are not stated in the retrieved text.

### Contradicts
Cannot be assessed without the full text. Note for the synthesis step: the registry's `why_needed` field for this key describes it as an attack that forces a "measured decode-failure rate" at set sizes and load factors "otherwise considered safe" — but the retrieved abstract describes the opposite framing: a technique for recovering more of the symmetric difference than the standard IBLT decode threshold allows, not an attack that induces failure below that threshold. Whether the full paper also contains an adversarial-input analysis, as the registry entry implies, cannot be confirmed from this landing page and must be checked against the actual PDF before this paper is cited as an attack paper in the synthesis.

### References worth retrieving
From the landing page's reference list (paper's own bibliography, not independently classified without the body text to see how each is used):
- Belazzougui, Kucherov, Walzer, "Better space-time-robustness trade-offs for set reconciliation," ICALP 2024, LIPIcs — competing, a set-reconciliation scheme with a stated space-time-robustness trade-off, directly relevant to the same problem this paper addresses.
- Molloy, "Cores in random hypergraphs and boolean formulas," Random Structures & Algorithms 27(1), 2005 — foundational, the random-hypergraph 2-core theory this paper's title and mechanism directly build on.
- Rink, "On thresholds for the appearance of 2-cores in mixed hypergraphs," arXiv abs/1204.2131, 2012 — foundational, threshold analysis for the same 2-core phenomenon.
- Walzer, "Peeling close to the orientability threshold: spatial coupling in hashing-based data structures," ACM Trans. Algorithms 21(3), 2025 — competing, an alternative technique for improving peeling-based decode success near the theoretical threshold.
- Mizrahi, Bar-Lev, Yaakobi, Rottenstreich, "Invertible bloom lookup tables with listing guarantees," Proc. ACM Meas. Anal. Comput. Syst. 7(3), 2023 — competing, a variant IBLT construction with correctness guarantees on listing recovered elements.
- Bar-Lev, Mizrahi, Etzion, Rottenstreich, Yaakobi, "Coding for IBLTs with listing guarantees," ISIT 2023 — competing, related coding-theoretic guarantees for IBLT listing.
- Ozisik, Andresen, Levine, Tapp, Bissias, Katkuri, "Graphene: efficient interactive set reconciliation applied to blockchain propagation," SIGCOMM 2019 — competing, an applied set-reconciliation system for peer-to-peer blockchain propagation, a direct deployment-relevant comparison.
- Yang, Gilad, Alizadeh, "Practical rateless set reconciliation," ACM SIGCOMM 2024 — competing, a rateless-coding approach to set reconciliation, relevant to the rateless family GOMES-ARXIV-25 (this corpus) also addresses.
- Shibuya, Belazzougui, Kucherov, "Efficient reconciliation of genomic datasets of high similarity," WABI 2022, LIPIcs — foundational, prior work on the same genomic k-mer reconciliation application this paper targets.
- Pontarelli, Reviriego, Mitzenmacher, "Improving the performance of invertible bloom lookup tables," Inf. Process. Lett. 114(4), 2014 — foundational, an earlier IBLT performance-improvement technique to compare this paper's predictor-based approach against.

### Verbatim extracts
- "the set recovery process succeeds if the IBLT size is at least 1.22 times the size of the encoded set"
- "this approach modifies only the decoding procedure, leaving the IBLT data structure unchanged"
- "recovery of 27% more elements than the nominal IBLT size"
- "an IBLT of size only 66% of the encoded set size for k = 31"
