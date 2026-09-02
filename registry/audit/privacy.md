# Audit: privacy-tiers.md and group-encryption.md

## privacy-tiers.md

Checked claims: Tor page-fetch latency and 60MB-download figures, CAI-CCS-14 Tamaraw/BuFLO/Tor
percentages, ZHOU-SP-24 Piano latency/communication/preprocessing figures at 1GB and 100GB,
HENZINGER-SOSP-23 Tiptoe latency/communication/rank figures, the CASH-CCS-15 and GRUBBS-SP-19
searchable-encryption exclusion figures. All of these match their cited entries, including the
matched conditions (relay count, dataset, thread count, network setup).

One unsupported claim found:

- Table 1, row "3-hop onion circuit, no padding (Tor-class)": "roughly four orders of magnitude
  smaller than a present-day relay population" is attached to [DINGLEDINE-USENIXSEC-04] but the
  entry states only the 2004 network's own size (32 relays) and carries no present-day relay count
  to compare against. The claim also fails its own arithmetic: a present-day Tor network runs on
  the order of 7,000-8,000 relays, a factor of roughly 250, not four orders of magnitude (10,000x).
  This is an uncited factual claim with no traceable source and an internally implausible figure.

## group-encryption.md

Checked claims: BeeKEM best-case and partition-recovery figures (group sizes, welcome-message
growth, benchmark hardware, plateau behavior), AUERBACH-CRYPTO-25's exponent table and "over √N"
figure, BIENSTOCK-TCC-22's Ω(n) black-box-PKE bound and its stated relation to TreeKEM, ALWEN-SCN-24
(DeCAF)'s cost table for CoCoA (centralized and decentralized), and DeCAF's own O(n log n log t)
figure and confirmation-depth gap. All of these match their cited entries with conditions preserved.

One unsupported claim found, restated twice in the document:

- Table row "Weidner, Kleppmann, Hugenroth, Beresford DCGKA ('WKHB')" states: "Highest measured CPU
  time of three systems compared, sender and recipient, at every tested group size 8 to 512
  ... [YEN-EPRINT-26]." The entry states only that BeeKEM has the lowest measured CPU time of the
  three systems (BeeKEM, OpenMLS, WKHB) at every tested group size — it never states which of the
  remaining two, OpenMLS or WKHB, ranks highest. "WKHB highest" does not follow from "BeeKEM lowest"
  without a third data point the entry does not supply.
  - The same unsupported ranking is repeated in the "Against Weidner et al.'s DCGKA" paragraph of
    the Selection section: "WKHB has the highest measured CPU time of the three systems compared,
    for both sender and recipient roles, at every tested group size from 8 to 512 (YEN-EPRINT-26
    Fig. 4)." Same defect, same fix needed: either cite a source that ranks OpenMLS against WKHB
    directly, or narrow the claim to what the entry supports (BeeKEM lowest; WKHB's O(n) sender-side
    asymptotic cost against BeeKEM's O(log n), which the entry does support).

## Count

Claims checked: 24. Supported: 22. Unsupported: 2 (one distinct defect, cited in two places within
group-encryption.md, plus one distinct defect in privacy-tiers.md).
