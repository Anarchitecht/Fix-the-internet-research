# Audit: indexing.md, ranking.md, moderation.md

## Method
Extracted every cited factual claim in the three assigned selection files and traced each to
its cited entry under registry/evidence/. Checked figures, percentages, and stated conditions
against the entry's own measured-results tables and verbatim extracts.

## Findings

### indexing.md — RICHARDSON-SIGIR-14 rank figures attached to the wrong malicious-fraction condition

Selection text (Candidates table, PAC row, "Condition under which it fails" column):
"At z=2,000 nodes queried and 10% malicious peers, with no defense, a censorship attack moves a
target document's rank from 5 to 582 and a promotion attack moves an unrelated document from rank
20,778 into the top 10 (`RICHARDSON-SIGIR-14`)."

RICHARDSON-SIGIR-14's own measured-results table states the censorship-attack rank sequence as
5 -> 9 -> 582 -> 2166 as the malicious fraction f rises 0% -> 10% -> 20% -> 30%. Rank 582 occurs
at f=20%, not f=10%; the rank at f=10% is 9. The promotion-attack sequence is
20,778 -> 84 -> 11 -> 9 across the same f values: at f=10% the rank is 84, well outside the top
10; the document reaches the top 10 only at f=20% (rank 11) or f=30% (rank 9).

The selection states both figures as occurring "at 10% malicious peers." Neither does in the
cited entry — both are the entry's f=20%-30% figures relabeled to the f=10% condition. This
overstates how little adversarial control the described attack needs: a reader takes away that
10% malicious peers alone is sufficient to move a document from rank 5 to rank 582 and from rank
20,778 into the top 10, when the entry's own numbers show 10% malicious peers produces a far
smaller effect (rank 5->9, rank 20,778->84) and the stated failures require double or triple that
adversarial share. Verdict: conditions-dropped (the specific malicious-fraction condition is
wrong for the cited figures).

This is the only figure discrepancy found in indexing.md; every other cited number checked
(LI-IPTPS-03's 6 MB/530 MB/75x/7x figures and budget derivation, ASTHANA-ICTIR-11's 1.0-3.6 MB
and 90%-accuracy node counts, COX-ICTIR-09's 63% figure at 340,000 nodes, WEI-NSDI-24's provider-
record and cache-hit figures, RICHARDSON-SIGIR-14's Brahms-20%/skewness-40% bound, TRAUTWEIN-
SIGCOMM-22's 1-second Bitswap timeout) matches the cited entry's own stated conditions.

## ranking.md

Checked: QUELLE-PLOSONE-25's 139,033/5,000,000 (2.8%) alternative-feed-adoption figure,
BALDUF-IMC-24's generator/hosting-concentration figures, WANG-ARXIV-26's -0.061 reciprocal-rank
new-author penalty (SE 0.020, p=0.003, robust across all 250 feeds, independent of follower
count), KAMVAR-WWW-03's EigenTrust convergence and 40%-collusion figures, GYONGYI-VLDB-04's
178-seed/1,250-candidate TrustRank figures and the 7-bucket average demotion, GOLD-ARXIV-23's
75-of-100-peer collapse and 600-byte/600-kilobyte figures, HEGEDUS-ECMLPKDD-19's message-size
figures. All match their cited entry's own stated figures and conditions. No unsupported or
misattributed claim found in this selection beyond what the document already labels as an
unmeasured guess (the gossip-computed-default-inside-a-marketplace pairing, stated explicitly as
"a guess, stated as one" in the Selection section) — that self-labeling satisfies the audit
standard rather than violating it.

One borderline item, not counted as a finding: the combined "roughly 40,000-43,000 generators
created by 18,000-18,352 distinct accounts by 2024" figure cites both BALDUF-IMC-24 and
QUELLE-PLOSONE-25 together. QUELLE-PLOSONE-25 states 39,639 feeds by 18,352 users on its own
dataset window; the range given in the selection is wide enough to cover both papers' individual
counts without asserting a single precise figure from either, so this is a fair range citation,
not a wrong-key error.

## moderation.md

Checked: BALDUF-IMC-24's labeler-count, object-count, and 30 GB/day figures; the 3.2% cross-
labeler-overlap figure; BONO-WEBSCI-24's in-degree and connected-component claims; ANAOBI-WWW-23's
82.3-day average and 19/98.4-day range; ZHANG-ARXIV-25's 364/1,807 (20.1%) and 169/364 (46.4%)
disclosure figures; ZIA-ARXIV-25's 12.69% macro-F1 gain and 50%-inverted-label collapse;
AGARWAL-ICWSM-24's 0.60-to-0.8826 macro-F1 figures; SOKOTO-USENIXSEC-24's denylist-entry counts,
reporting latency, content-type breakdown, gateway-compliance percentages (100% / 18%), and the
two circumvention figures (56 of 57 gateways / 97.4% of usually-blocked identifiers via hash
substitution; 67 of 68 / 98.5% via directory wrapping). All match their cited entry's own stated
figures and conditions, including the "71 supported hash functions" figure, which is consistent
with the entry's stated 72 total hash functions (71 remaining once the content's original hash is
excluded).

No uncited factual claim was found in any of the three files: every number, measured result, or
stated mechanism property carries a citation key, and the few sentences without one (the framing
paragraphs, the Selection section's comparative reasoning) are reasoning from cited figures
already introduced elsewhere in the same file, not new unsourced facts.

## Summary

Claims checked: 3 selection files, approximately 90 distinct cited figures across the three.
Supported: all but one.
Unsupported: 1 — the RICHARDSON-SIGIR-14 rank-manipulation figures in indexing.md, misattributed
to the 10% malicious-peer condition when the entry's own table places them at 20% and 30%.
