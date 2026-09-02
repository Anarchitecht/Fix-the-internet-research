# Audit: transport.md, nat-traversal.md, capacity-ordering.md, content-location.md

## Method

Every citation-carrying claim in the four assigned selection files was traced to its cited
evidence entry under `registry/evidence/`. Entries checked in full: LANGLEY-SIGCOMM-17,
KAKHKI-IMC-17, BUCHET-CCR-25, DINGLEDINE-USENIXSEC-04, TANG-ARXIV-22, HALKES-NETWORKING-11,
CHROMIUM-BLINK-SRC, FORD-USENIX-05, LIANG-ARXIV-24, DUARTE-ABAKOS-20, REDDY-RFC-20,
KERANEN-RFC-18, PETIT-HUGUENIN-RFC-18, SINGH-ARXIV-26, TRAUTWEIN-ARXIV-26, YANG-ICDE-03,
LOO-IPTPS-04, STEINER-CCR-07, CASTRO-OSDI-02, CORTESGOICOECHEA-ARXIV-24.

## Finding

**transport.md, WebRTC data channels row, "Measured cost" column** — the selection states:

> +15% CPU / +10% memory per additional simultaneous peer in a production peer-assisted-delivery
> deployment [TANG-ARXIV-22]

TANG-ARXIV-22 states the +15% CPU / +10% memory figure as the fixed overhead of PDN
(peer-assisted-delivery-network) participation against a no-peer, direct-CDN baseline — a single
measurement from two peers watching one stream, not a per-peer rate. The same entry separately
varies peer count from 0 to 3 and states directly that "CPU, memory, and download traffic show no
significant change across this range." The entry attributes this flatness to WebRTC's own
connection scalability. The selection's phrase "per additional simultaneous peer" asserts a
scaling relationship the cited entry states does not hold — a reader would conclude CPU and memory
cost rise with each added peer, when the entry's own measurement shows the opposite: a fixed
one-peer-versus-none overhead that stays flat as peer count grows to 3.

Verdict: conditions-dropped (the entry's own no-significant-change-with-peer-count finding is the
condition that was dropped).

## What was checked and held up

Across the four files, the following load-bearing figures were traced to their cited entries and
found to match figure, condition, and framing:

- transport.md: LANGLEY-SIGCOMM-17's 8.0%/3.6% search-latency and 18.0%/15.3% rebuffer-rate
  reductions, 88%/65-68% 0-RTT rates, ~2x server CPU; KAKHKI-IMC-17's 2x/2.8/2.75 Mbps
  bandwidth-share figures, 58%/7% Application-Limited state, 9% Verizon-3G reordering and the
  NACK-threshold-3 mechanism; BUCHET-CCR-25's 52%/78% migration-success and 94%
  single-organization concentration; DINGLEDINE-USENIXSEC-04's 2.8s/5.3s/0.3s page-fetch and
  300s/210s download figures, the stated non-goal against a global passive adversary; FORD-USENIX-05's
  82%/64% UDP/TCP hole-punch compatibility; LIANG-ARXIV-24's ~55ms/~56ms punch times and the
  paper's own Endpoint-Independent-Mapping-versus-real-NAT caveat, correctly carried into the
  selection's "does not settle" section; CHROMIUM-BLINK-SRC's 500-connection cap; DUARTE-ABAKOS-20's
  88.49/9.28 Mbps relay-collapse figures; SINGH-ARXIV-26's "cannot create listening sockets"
  quotation; KERANEN-RFC-18's 15-second keepalive minimum, correctly distinguished from
  HALKES-NETWORKING-11's measured 55-second recommendation.
- nat-traversal.md: TRAUTWEIN-ARXIV-26's 70%±7.1% conditional success rate, 29% precondition
  failure, 500-byte/two-round-trip coordination cost, 97.6% first-attempt completion, 70%-RTT
  reduction for half of peers, 859 networks/39 countries — all confirmed verbatim against the
  entry; FORD-USENIX-05 and HALKES-NETWORKING-11 figures reused correctly from the transport.md
  check above; LIANG-ARXIV-24's 55/56ms figures reused correctly.
- capacity-ordering.md: YANG-ICDE-03's 79% bandwidth/processing reduction, the 303%/14% first-mover
  figures, the k=2 redundancy 48%/2.5%/17% figures — all confirmed exact; LOO-IPTPS-04's
  58-minute/93-minute connection-lifetime figures and the 30-or-75-leaf-node ultrapeer fan-out
  finding — confirmed exact, including the "1.5x" framing used correctly in the selection's
  "costs and fails" section rather than overstated as an order of magnitude.
- content-location.md: STEINER-CCR-07's 8-Sybil eclipse figure, confirmed exact including the
  live-network condition; CASTRO-OSDI-02's 42%-success Chord figure at f=20%, N=100,000, confirmed
  exact; CORTESGOICOECHEA-ARXIV-24's 10-14-minute/12-second provide() figures and the
  routing-table-bottleneck mechanism, confirmed exact. The document's own repeated flagging of the
  S/Kademlia 99%-success figure as sourced only to a BRIEF.md summary, not a full evidence-file
  entry, is accurate as stated — this is the document doing exactly what this audit exists to
  check for, and it is already disclosed rather than presented as settled.

No instance of a figure attributed to the wrong key (wrong-key) was found in these four files. No
uncited numeric claim presented as settled fact was found; the few uncited factual statements
present are either restatements of a mechanism's structural property already established earlier
in the same row, or explicitly labeled as unverified by the selection's own "does not settle"
section.
