## [SHI-TRACERANK-25] Sybil-Resistant Service Discovery for Agent Economies
**Citation:** David Shi, Kevin Joo. "Sybil-Resistant Service Discovery for Agent Economies." arXiv:2510.27554v1 [cs.CR], Operator Labs, October 31, 2025.
**Retrieved:** full text via arXiv (no `targets-deduped.json` record for this key)
**Source URL:** https://arxiv.org/abs/2510.27554
**Domain:** F (Sybil resistance and reputation); secondarily I (incentives, since the mechanism ranks services paid through the x402 protocol)

### What it does
TraceRank ranks payment-gated web services by treating each cryptocurrency payment a client makes to a
service as an endorsement whose weight depends on the paying address's own precomputed reputation, rather
than on raw transaction count or transaction volume. The mechanism targets x402, a protocol (cited as
reference [1], a Coinbase Developer Platform whitepaper) that standardizes payment-gated Hypertext
Transfer Protocol (HTTP) endpoints: a client's first request to a paid endpoint receives an HTTP 402
(Payment Required) response describing terms, the client replays the request with a signed payment
payload, and the server (or an intermediary facilitator) verifies and settles the payment on a
blockchain, recording it as a directed edge from payer address to service address with an attached
value and timestamp. TraceRank first assigns every address i a seed reputation score s_i from external,
off-chain signals (the paper names trading performance, decentralized social-network signals such as
Farcaster, protocol-contribution history, labels for known entities such as decentralized autonomous
organizations or verified protocols, and agent-identity attestations from ERC-8004 registries); addresses
without any external signal receive s_i = 0. It then computes, for each observation window, an aggregated
flow F(j→i) into every address i by summing over every payment edge from j to i a term combining the
natural logarithm of the payment's US-dollar value (log(1 + value) dampens the effect of a single very
large payment) and an exponential decay in the payment's age in days (e^(-lambda*age), so older payments
count for less). It normalizes these flows into a column-stochastic matrix W (each column sums to 1,
except sink addresses with zero inbound flow, which stay at 0) and iterates r(t+1) = s + alpha*W^T*r(t)
for a damping parameter alpha in (0,1) — an update rule structurally identical to PageRank's, but seeded
with the external reputation vector s instead of a uniform prior — converging to the closed-form fixed
point r = (I - alpha*W^T)^-1 * s. The paper's stated Sybil-resistance property follows directly from this
construction: an address with a zero seed score propagates zero reputation regardless of how many payments
it sends, so a service that receives many payments only from zero-seed addresses (an adversary's control of
however many freshly created wallets) accumulates no propagated reputation from them, while a single
payment from a high-seed address propagates meaningfully. The paper additionally proposes fusing
TraceRank with semantic search over natural-language service descriptions: score(A, q) = cos(q, p_A) ×
TraceRank(A), a multiplicative combination of cosine similarity between a query embedding q and a
service's profile embedding p_A, and the service's precomputed TraceRank score.

### Measured results
This paper reports no experiment, no dataset, no live deployment measurement, and no benchmark of any
kind. Every quantity in the paper is either a symbolic definition (the Fj→i flow formula, the update rule,
the fixed-point equation) or a hypothetical illustrative example, explicitly introduced as a thought
experiment ("Consider two x402 services competing for discovery") rather than a measurement: Service A
(described as spam, an airdrop-farming lure) is stated to attract 10,000 fresh wallets, 10,000 payments,
and $10,000 total volume; Service B (described as a legitimate background-check service) is stated to have
50 payments from 50 sophisticated traders totaling $5,000 volume. The paper argues from this constructed
scenario, not from any run of TraceRank against real x402 payment-graph data, that raw count and volume
ranking would favor Service A while TraceRank favors Service B — no seed-score values, no computed
TraceRank output, and no comparison numbers are given even for this hypothetical pair. The paper's own
Section 5 states its comparison against three counterfactual ranking techniques (semantic-only,
TraceRank-only, and volume/count-oriented) is explicitly future work: "Future work will demonstrate how
the combined TraceRank and vector similarity technique excels at retrieving the highest quality services."
No parameter value for alpha (the damping factor) or lambda (the temporal-decay rate) is given anywhere in
the paper; both are left as free symbols in the formulas.

### Parameters
- Damping factor alpha in the TraceRank iteration r(t+1) = s + alpha*W^T*r(t): defined to lie in the open
  interval (0, 1); no specific value is chosen, tested, or recommended anywhere in the paper.
- Temporal decay rate lambda, with stated units of day^-1, in the flow-aggregation formula
  e^(-lambda*age_days(e)): no specific value is chosen, tested, or recommended.
- Seed score s_i: defined only by its source category (external signals — trading performance, social-
  graph signals, protocol-contribution history, entity labels, ERC-8004 agent attestations) and its
  default (0 for any address with no external signal); the paper states TraceRank is "agnostic to seed
  provenance" and does not specify or evaluate any particular seed-scoring function.
- Fusion weighting in score(A, q) = cos(q, p_A) × TraceRank(A): a fixed, unweighted multiplicative
  combination — no tunable weighting parameter is introduced or evaluated between the semantic-similarity
  term and the TraceRank term.

### Stated limitations
The paper itself frames its own contribution as a design and worked-example argument, not a validated
system: the counterfactual evaluation against semantic-only, TraceRank-only, and volume-based ranking is
stated explicitly as future work, not completed in this paper. No mechanism is specified for how seed
reputation scores are actually computed, verified, updated, or kept resistant to manipulation at the
source (for example, gaming a Farcaster social-graph score or an ERC-8004 attestation to obtain artificial
seed reputation) — the paper states seeds may combine several named external signal categories but treats
each as an opaque external input, not something this paper's own mechanism secures. The paper's own
worked example demonstrates the mechanism's intended qualitative behavior only for the specific case where
an adversary's Sybil addresses have exactly zero seed score; the paper states no bound, formula, or
worked case for how much reputation an adversary with some nonzero but low seed scores (rather than
literally zero) could accumulate through many payments, an intermediate case its own "immediate
consequence" argument (an address with a zero seed score propagates zero reputation "regardless of N")
does not directly address.

### Requirements it places on the rest of the system
TraceRank requires a source of externally derived seed reputation scores for at least some addresses in
the payment graph — the mechanism's own stated Sybil resistance depends entirely on genuine Sybil
addresses actually receiving a seed score of (or close to) zero, which requires whatever external
signal source assigns those scores to itself resist the same Sybil attack TraceRank is meant to prevent;
the paper does not analyze or bound this dependency. It requires the underlying payment protocol to record
every payment as a public, attributable, directed edge with a value and timestamp — the mechanism cannot
compute its flow aggregation Fj→i without this data being observable, so it is inherently incompatible,
without modification, with any privacy-preserving payment layer that hides sender identity, payment value,
or timing from the party computing TraceRank scores. It requires periodic or continuous recomputation of
the fixed-point vector r over a chosen observation window, since the paper's construction is explicitly
time-decayed (the exponential age term) and windowed, so a deployment must decide and the paper does not
specify how frequently to recompute scores and over what window length, a free parameter left unresolved
in the presented design.

### Contradicts
None found against other corpus entries on a measured fact — this paper reports no measurement to compare
against any other source in this corpus.

### References worth retrieving
- **Foundational** — E. Reppel, R. Caspers, K. Leffew, D. Organ, D. Kim, N. Dalal. "x402: An open standard
  for internet-native payments." Coinbase Developer Platform whitepaper, May 6, 2025. (Cited as reference
  [1]; the payment protocol TraceRank's entire mechanism is built on top of.)
- **Foundational** — S. Brin, L. Page. "The Anatomy of a Large-Scale Hypertextual Web Search Engine."
  Computer Networks and ISDN Systems 30(1-7), 1998, 107-117. (Cited as reference [3]; origin of PageRank,
  the algorithm TraceRank's update rule structurally generalizes by replacing a uniform prior with a
  seeded external reputation vector.)
- **Foundational** — Z. Gyöngyi, H. Garcia-Molina, J. Pedersen. "Combating Web Spam with TrustRank." VLDB
  2004. (Cited as reference [4]; the manual-seed-list precedent this paper states "does not generalize in
  pseudonymous settings" — worth retrieving to check what TrustRank's own seed-list construction and
  evaluation methodology was, for comparison against TraceRank's unspecified seed-scoring function.)
- **Foundational** — M. De Rossi, D. Crapis, J. Ellis, E. Reppel. "ERC-8004: Trustless Agents [DRAFT]."
  Ethereum Improvement Proposal 8004, August 2025. (Cited as reference [5]; one of the named external
  seed-score sources — an on-chain agent identity/reputation/validation registry — whose own guarantees
  this paper's Sybil-resistance claim indirectly depends on.)

### Verbatim extracts
- "if a service receives payments from N addresses with zero seed scores, it accumulates zero propagated
  reputation regardless of N."
- "TraceRank is agnostic to seed provenance."
- "Future work will demonstrate how the combined TraceRank and vector similarity technique excels at
  retrieving the highest quality services."
- "Quality emerges from who pays, not just how much."
- "enabling agents to bootstrap trust in decentralized marketplaces without privileged curators or
  identity systems."
