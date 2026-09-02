# Citation audit: storage-encoding.md, repair.md, application-data.md

Method: every claim carrying a citation key was traced to the cited entry in
`registry/evidence/`. Verdicts: supported, conditions-dropped, not-in-entry, wrong-key,
uncited-factual-claim.

## storage-encoding.md

Claims checked: approximately 55 (every bracketed figure in the candidate table, the
selection paragraphs, and the requirements/costs/open-problems sections).

Supported without qualification: the large majority. Spot-verified against source entries:
`WEATHERSPOON-IPTPS-02` (11x bandwidth/storage/seeks, 74 years vs 10^20 years MTTF),
`HUANG-ATC-12` (Azure MTTF table, 50% read reduction, 166/305/418/893 ms latencies, 13.2 µs
decode, pd=86%), `DIMAKIS-TIT-10` (73% OMMDS reduction at n-1=13 helpers, 84%/39% RC
reduction, 58x/100x PlanetLab result, "very slightly worse than Hybrid" on the Gnutella
trace, 14%/3.1% read overhead), `RASHMI-TIT-11` (d≥2k-2, field sizes ≥2n/≥n², the d≤2k-3
non-achievability result), `CHENG-TOS25-ECSURVEY` (1.18x-1.50x overhead table, n≤20, "more
than 98%" single-chunk figure), `DANEZIS-WALRUS-25` (25x/4.5x/3x overhead table, RaptorQ
replacement), `SATHIAMOORTHY-VLDB-13` (486.6 GB/369 blocks/26 min), `RODRIGUES-IPTPS-05`
(1x-3x savings range, Overnet unsustainability finding), `ANDERSON-CCGRID-06` (89.5-day host
lifetime), `LI-IWQOS-23-STORJ` (9.6% churn), `WILKINSON-STORJ-18` (separate per-piece hash
requirement).

### Findings

1. **not-in-entry** — the introductory paragraph attributes `a=0.38` and a
   "1-day-timeout permanent-failure rate 30%/day" to `BLAKE-HOTOS-03`'s own Gnutella crawl
   ("~33,000 Gnutella hosts (April 2003, mean availability a=0.38, 1-day-timeout
   permanent-failure rate 30%/day)"). `BLAKE-HOTOS-03`'s entry states no `a` value and no
   permanent-failure-rate value anywhere — its own crawl parameters are `Nτ`, `aτ`, `Tτ`,
   reported only as swept curves (Figures 2-4), never as the single numbers a=0.38 or
   30%/day. Those exact numbers (a=0.38, f=0.30/day) belong to a *different* Gnutella trace
   — the one used in `DIMAKIS-TIT-10` (1,846 nodes, May 2001, 2.5-day window), a separate
   dataset from BLAKE's own 33,000-host, April-2003, 8-day crawl. The selection has merged
   two distinct Gnutella measurements under one citation. A reader takes away a specific
   availability figure for BLAKE's population that BLAKE never measured.

2. **not-in-entry** — the same paragraph attributes `a=0.97` to `CHUN-NSDI-06`'s 632-host,
   one-year PlanetLab trace ("`CHUN-NSDI-06` (Carbonite) measures a 632-host, one-year
   PlanetLab trace (a=0.97, mean disk lifetime 2.23 years, sustainability ratio θ≈6.85)").
   The mean-disk-lifetime (2.23 years) and θ≈6.85 figures are genuinely CHUN's own derived
   values. `a=0.97` is not: CHUN's entry reports only `a=0.88` (used in a 5-year synthetic
   trace for the reintegration/batching comparison, not for the 632-host PlanetLab trace
   itself, which is not reported with a summary availability figure at all). `a=0.97` is
   `DIMAKIS-TIT-10`'s figure for its own, separate 303-node, 527-day PlanetLab trace — again
   a different dataset conflated with CHUN's. Both misattributions run in the same direction:
   pulling a DIMAKIS-TIT-10 parameter into a sentence that names BLAKE-HOTOS-03 or
   CHUN-NSDI-06 as the source, inside the passage that establishes which "regime" applies to
   the rest of the document's argument.

3. **conditions-dropped** (minor) — the candidate table's "Measured cost" column header
   applies to whole-copy replication's `WEATHERSPOON-IPTPS-02` row, but that entry's own
   Measured Results section states explicitly: "All results are analytical, from the paper's
   closed-form cost model, not from a simulation or a deployed system; no node count,
   topology, dataset, or runtime is reported anywhere in the paper." The selection's
   candidate-table cells for this row (11x, 74 years vs 10^20 years, 28x, 12-month repair
   epoch) are stated as flatly as the deployment-measured Azure and Facebook figures two rows
   down, with no flag that they come from a closed-form model rather than a measurement. A
   reader comparing rows across the table has no way to tell these apart without opening the
   source entry.

Everything else checked in this selection — the requirements section, the "what it costs and
where it fails" section, and the "what the corpus does not settle" section — traces cleanly
to its cited entries.

## repair.md

Claims checked: approximately 35.

Supported without qualification, spot-verified: `SATHIAMOORTHY-VLDB-13` (11.5 blocks/repair,
41-52% bytes, 25-45% faster, 0.58 GB vs 1.318 GB), `HUANG-ATC-12` (3 vs 6 fragments, 1.33x vs
1.5x, latency table), `LI-IWQOS-23-STORJ` (k=29 of n=80, o=110, reputation-manipulation
finding), `VAJHA-FAST-18` (C3=(20,16,19), 2.9x traffic / 3.4x disk-read reduction, d=19 = all
19 surviving nodes in a 20-node stripe), `RASHMI-TIT-11` (cutset-bound equality, field sizes),
`PATRA-TIT-25` (limited-power adversary corrupts stored data, not computation — matches the
selection's characterization exactly), `DANEZIS-WALRUS-25` (epoch 17/20 shard-recovery
durations, committee hardware, per-sliver vector commitments), `CHUN-NSDI-06` (44% overhead,
~2x for Total Recall/Cates), `BHAGWAN-NSDI-04` (eager vs. lazy repair mechanism description).

### Findings

1. **uncited-factual-claim** (minor) — "the resulting ~100 kbps/node average maintenance
   bandwidth" attributed to `RODRIGUES-IPTPS-05` in the Hybrid row is supported (the entry's
   verbatim extract states "around 100 kbps on average"), but the same sentence's redundancy
   comparison — "coding cuts the required redundancy factor to under half pure replication's
   factor of 20" — compresses `RODRIGUES-IPTPS-05`'s own qualitative statement ("reduced by
   coding to less than half its replication-factor requirement") correctly; no issue found on
   closer reading. Downgraded from a finding — supported.

2. **conditions-dropped** — the "what this selection requires" section states: "against
   roughly 2x oracle overhead for a threshold policy that discards and re-replicates on every
   disconnection (`BHAGWAN-NSDI-04`'s eager repair, and the 'Cates' comparison point in
   `CHUN-NSDI-06`)." The 2x figure is `CHUN-NSDI-06`'s own measurement of Total Recall and a
   "Cates"-style system in CHUN's simulation, not a figure `BHAGWAN-NSDI-04` reports for its
   own eager-repair policy — `BHAGWAN-NSDI-04`'s entry reports no oracle-relative overhead
   ratio for eager repair at all, only that eager repair "produces the highest per-host
   bandwidth of the five policies tested" in its own trace-driven simulation, an unrelated
   metric. Citing `BHAGWAN-NSDI-04` alongside the 2x number invites a reader to believe
   BHAGWAN-NSDI-04 measured that ratio for its own eager-repair design; it did not — CHUN
   measured a same-shaped policy inside its own comparison. The two mechanisms are
   structurally similar (both discard-and-recount on disconnection) but the citation implies
   a shared measurement that does not exist.

Everything else checked in this selection, including the security-assumption column, the
"what the corpus does not settle" section, and the cross-reference to the storage-encoding
selection's disagreement, traces cleanly.

## application-data.md

Claims checked: approximately 60.

Supported without qualification, spot-verified: `AUVOLAT-SRDS-19` (66%/34% bandwidth/entropy
reduction at light load; loses on entropy and delay at heavy load; MPT non-termination at
2000 nodes), `KLEPPMANN-TPDS-22` (5,700 vs 22,000 ops/sec, 4x-23x throughput gap, 100,000x
latency gap), `ATTIYA-PODC-16`'s core bound (O(D log k) for RGA against a proved Ω(D) floor),
`KLEPPMANN-ARXIV-20` (96.7%/3.2%/0.04% round-trip distribution, ~1 kB overhead, I-confluence
theorem, the cryptocurrency-balance counterexample), `KLEPPMANN-PAPOC-22` (equivocation attack
on version vectors, sub-100-byte frontier summary, the conjectured-not-proved extension of
convergence to type-specific validity), `DOUCEUR-IPTPS-02` (Lemma 2's unbounded-identity
result, cited correctly as the reason quorum-based BFT has no basis in an open network),
`BENET-ARXIV-14` (no persistence layer beyond transient caching, IPNS as a signed pointer),
`KERMARREC-DICG-20` (no benchmark methodology / anecdotal figures, per-store memory scaling
with total activity, follower-graph leakage), `RAWAT-DLT-24` (24%-45% / ~3x), `AMPARORE-
ARXIV-26` (4.69x-13.98x), `MEYER-TR-24` (prolly trees proved not clamping-invariant),
`GRUBBS-SP-19` (500 queries / 2%, 100 queries / majority of 248,000 records).

### Findings

1. **conditions-dropped** — the Byzantine-tolerance section states: "`ATTIYA-PODC-16` proves
   any protocol in the 'push-based' class — which the paper states explicitly includes
   deployed eventually-consistent write-propagating protocols generally, OT included — carries
   Ω(D) metadata overhead in the number of deletions." `ATTIYA-PODC-16`'s own text supports
   "deployed eventually-consistent write-propagating protocols generally" as inside the formal
   push-based class (its own definition is stated to contain both operation-based and
   state-based protocols, and "to contain deployed eventually-consistent write-propagating
   protocols generally"). It does not state that operational transformation is inside that
   *formal, proved* class. What the entry actually contains is a separate, related-work-level
   remark: "operational-transformation protocols storing a full update log have metadata
   overhead at least linear in the number of updates for the same reason" — an informal
   observation by analogy, not an instance of the Ω(D) theorem being proved to cover OT. The
   selection's parenthetical "OT included" reads as though the paper's proof scope names OT
   specifically; the paper's own text keeps that claim in its discussion, not its theorem
   statement. This matters because §22 of the selection uses exactly this claim to argue OT
   has no metadata-cost advantage over CRDTs, treating an informal aside as though it carried
   the same proof strength as the Ω(D) theorem itself.

2. Everything else checked — the requirements section, the "what it costs and where it
   fails" section, the "what the corpus does not settle" section, and the secondary-index
   discussion — traces cleanly to its cited entries with conditions preserved (in particular,
   the Willow/prolly-tree/clamping-invariance incompatibility argument correctly represents
   all three source entries' own stated scope limits).

## Summary

- storage-encoding.md: 3 findings — two conflate figures from a different paper's Gnutella or
  PlanetLab trace with the paper actually cited (BLAKE-HOTOS-03 and CHUN-NSDI-06 respectively,
  both pulling numbers that belong to DIMAKIS-TIT-10's traces), one minor unflagged
  analytical-vs-measured distinction in a table header.
- repair.md: 1 finding — a citation implying BHAGWAN-NSDI-04 measured the same 2x
  oracle-overhead ratio CHUN-NSDI-06 measured for a structurally similar policy.
- application-data.md: 1 finding — an informal related-work aside about OT's metadata cost is
  presented as covered by the paper's proved theorem scope.

All five findings change what a reader takes away about a cited paper's own measurement, not
about the selection's reasoning or mechanism choice.
