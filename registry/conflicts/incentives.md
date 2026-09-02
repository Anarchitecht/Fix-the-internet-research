# Contradiction report — family I: incentives, free-riding, and rate limiting

Agent X. No retrieval performed. Every claim below traces to an entry in `registry/evidence/`,
cited by KEY, or to the primary-source text file under `sources/text/` when a citing paper's
exact wording had to be checked against its own bibliography target.

## 1. Measurement disagreement: does the Alwen-Blocki tradeoff attack threaten Argon2i-B at 1 GB

Two papers in this family analyze the identical attack — the depth-reducing-set tradeoff attack
against data-independent memory-hard functions, from Alwen and Blocki's CRYPTO 2016 construction —
against the identical target and memory scale, and reach opposite conclusions about whether it is
a practical threat.

`BIRYUKOV-EUROSP-16` (the Argon2 designers' own specification and security analysis) derives the
attack's time-area advantage analytically from the attack's own published closed-form formula and
concludes: "for M up to 2^20 (1 GB) the advantage is smaller than 1" — meaning no benefit to the
attacker — and that the advantage stays under 2 for memory up to 16 GB. The document states this
approach "is not better than the ranking attack" (Argon2's own analyzed tradeoff attack) at these
memory sizes, and concludes the Alwen-Blocki line of attack poses no practical threat in the
memory range Argon2 is deployed at.

`ALWEN-EUROSP-17` (Alwen and Blocki themselves, in a later paper) simulates the same attack against
randomly sampled Argon2i-B graphs and measures: "at tau = 6 passes over 1GB of memory the attack
already reduces costs by a factor of 2" — a factor-of-2 practical cost reduction inside the exact
parameter range (1 GB, up to 16 GB, the IRTF proposal's own recommended "paranoid" setting of 6
passes) that `BIRYUKOV-EUROSP-16` treats as safe.

**What differs in method, not in target or memory scale.** `BIRYUKOV-EUROSP-16` applies the
original 2016 attack's own published asymptotic time-area formula directly to Argon2's parameters
— a closed-form derivation, no simulation, no implementation of the attack itself.
`ALWEN-EUROSP-17` runs the attack computationally, adding two heuristics the 2016 formula does not
capture: a smaller depth-reducing-set construction than the original paper's, and an "XOR
compression" trick, together with an explicit analysis of how bounding attacker parallelism
affects cost. The second paper's own text states the purpose directly: prior observers, including
the Argon2 designers, "had argued the original Alwen-Blocki attack does not present a threat to
the real world security of Argon2-B" — this paper's stated purpose is to test, not assume, those
objections (`ALWEN-EUROSP-17`). The heuristic-improved, simulated attack instantiation beats what
the naive closed-form bound predicted; the disagreement is genuine and same-conditions, not an
artifact of different memory scales or different target constructions — both papers analyze
Argon2i-B specifically, at 1 GB and up to 16 GB. `BIRYUKOV-EUROSP-16` names `ALWEN-EUROSP-17`'s
predecessor result directly and reaches the opposite practical conclusion about it, and
`ALWEN-EUROSP-17` names `BIRYUKOV-EUROSP-16` as the document whose safety conclusion it disputes;
both sides of the disagreement cite each other in this corpus.

Because `ALWEN-EUROSP-17`'s figure is a demonstrated attack instantiation run directly against the
IRTF-recommended deployment parameter (not an asymptotic bound extrapolated from a different
attack family), it is the figure that fits assessing risk for an actual deployment at 1 GB,
6 passes — the parameter point the Argon2 designers themselves judged safe using the weaker
analytic method.

A third paper, `BONEH-ASIACRYPT-16` (the Balloon Hashing paper), reports a separate attack against
Argon2i v1.2.1 — a precomputation-based space-reduction attack on the algorithm's memory-reuse
rule, not the depth-reducing-set pebbling attack the two papers above analyze. It also contradicts
an Argon2 design-document claim (a stated 7.3x-16,384x computational penalty at reduced space,
which `BONEH-ASIACRYPT-16`'s attack achieves with no penalty), but this is a different attack
against a different version of the algorithm and belongs in the record as a separate, third
data point, not as confirmation of either side of the `BIRYUKOV-EUROSP-16` / `ALWEN-EUROSP-17`
disagreement.

## 2. Destroyed precondition: BitTorrent's optimistic-unchoke bootstrap assumes bounded exposure

`COHEN-IPTPS-03` (the original BitTorrent design) requires the tracker to hand out peer addresses
without a structured selection policy, and states this openness is what produces the random-graph
topology the paper credits with BitTorrent's churn robustness. The same openness underlies a second,
unstated assumption load-bearing for the choking algorithm's incentive property: a peer's exposure
to any other single peer's optimistic-unchoke slot — the deliberately unconditional grant of
upload bandwidth that lets a peer with nothing yet to reciprocate start downloading — stays small,
because a compliant client requests peer lists near the protocol's standard ~50-peer neighborhood
size and connects to a correspondingly small, roughly fixed number of peers.

`LOCHER-HOTNETS-06` (BitThief) and `SIRIVIANOS-IPTPS-07` (the Large View Exploit) both destroy this
bound using exactly the tracker mechanism `COHEN-IPTPS-03` relies on for its robustness argument.
`SIRIVIANOS-IPTPS-07` states its exploit "requires only the standard tracker announce protocol and
the standard practice... of accepting and merging additional peer lists from other peers" — no
protocol change, no credential. `LOCHER-HOTNETS-06` raises its client's simultaneous-connection
count from the reference default of 80 up to 500 and re-announces to the tracker far more
frequently, and measures that "opening more connections increases download speed linearly."
`SIRIVIANOS-IPTPS-07` separately measures its free-riding client reaching an average acquired view
of approximately 250 peers, five times the compliant client's ~50-peer standard, and completing
faster than a compliant client in 12 of 15 tested public swarms. Both papers state their own
requirement on any incentive mechanism that would resist this: `LOCHER-HOTNETS-06` states directly
that a defense "cannot rely solely on a reciprocity check triggered only by past upload behavior,"
because the optimistic-unchoke and seeder-round-robin paths are unconditional by design and scale
with connection count, not with reciprocation.

The requirement `COHEN-IPTPS-03` needs (bounded per-peer exposure to the unconditional bootstrap
slot) and the mechanism it needs from elsewhere (an open, unrestricted tracker that serves any
requester without limiting request size or frequency) are in direct tension: the same tracker
openness that gives the robustness-by-randomness property Cohen's paper claims is exactly what an
unrestricted connection count exploits to defeat the incentive property. A designer resolving this
either has the tracker rate-limit or cap peer-list size and connection count per requester (giving
up some of the claimed churn-robustness benefit of an unconstrained random graph), or accepts that
the choking algorithm's fairness property does not hold against a strategic client and must be
supplemented by a mechanism that prices or meters the bootstrap slot itself, as `LOCHER-HOTNETS-06`
recommends and as `PIATEK-NSDI-07` and `LEVIN-SIGCOMM-08` (BitTyrant, PropShare) independently
confirm by both stating they contradict the "TFT alone makes BitTorrent robust" claim `COHEN-IPTPS-03`
is read as making.

## 3. Unsupported attribution: two papers round Adar and Huberman's Gnutella figure past its own ceiling

`ADAR-FM-00` (Adar and Huberman, the primary source) states its own measured result as "almost 70%
of Gnutella users share no files" — 66% of 33,335 sampled peers, rising to approximately 69% once
NAT-blocked transactions are accounted for. The paper's own wording frames the figure as
approaching 70% from below, never reaching it.

`GOLLE-EC-01`, checked directly against its source text, states: "a recent study of the Gnutella
network found that more than 70% of its users contribute nothing to the system," citing Adar and
Huberman alone as its sole source for the figure. The retrieved primary source for that citation —
`ADAR-FM-00` — never reports a figure above roughly 69%. `GOLLE-EC-01`'s "more than 70%" crosses a
threshold its own cited source explicitly frames itself as falling short of.

`VISHNUMURTHY-P2PECON-03` (KARMA), checked directly against its source text, states: "20 to 40% of
Napster and almost 70% of Gnutella peers share little or no files," citing Adar and Huberman jointly
with `SAROIU-MMCN-02` (Saroiu, Gummadi, Gribble) for both figures together. The "almost 70%" wording
matches `ADAR-FM-00`'s own figure closely and is well supported by it. It is not supported by the
paper cited alongside it: `SAROIU-MMCN-02`'s own retrieved measured result states "25% of Gnutella
clients share zero files" — a figure less than half of "almost 70%," measured from a live Gnutella
crawl using the file-count field in pong messages. `VISHNUMURTHY-P2PECON-03` attributes the "almost
70%" claim to `SAROIU-MMCN-02` jointly with the paper that actually supports it, and `SAROIU-MMCN-02`'s
own text does not carry any figure close to 70% for Gnutella free-riding.

Both misattributions run in the same direction: a Gnutella free-riding figure drifts upward,
in one case past the 70% mark the original measurement explicitly avoided crossing, in the other
by attaching a second citation whose own reported figure is a different (and much lower) number
for the same claimed population.

## 4. What was checked and found not to be a conflict

- `PIATEK-NSDI-07` (BitTyrant, median 1.72x download-speed gain for a strategic client),
  `LOCHER-HOTNETS-06` (BitThief, relative multiples against a reference client),
  `SIRIVIANOS-IPTPS-07` (Large View Exploit, absolute completion times and a win-count metric),
  and `LEVIN-SIGCOMM-08` (PropShare, live-swarm completion times against both BitTorrent and
  BitTyrant) each report a different metric on different swarms. Each entry's own text already
  states this explicitly and warns against merging the figures; I confirm that caution rather than
  add a new one. None report the identical quantity under matched conditions, so there is no
  measurement disagreement to record among them, only independently confirmed instances of the
  same qualitative finding — a client contributing nothing to zero can match or beat a
  reciprocity-compliant client.
- `JANSEN-PAM-21` (honest-network bandwidth self-report underestimates true capacity by roughly
  53%) and `JOHNSON-POPETS-17` / `TRAUDT-ICDCS-21` (adversarial relays inflate self-reported
  bandwidth by up to 177x under TorFlow, bounded to 1.33x-4.52x under the two papers' proposed
  peer-measurement replacements) measure different quantities — passive estimation bias under
  honest reporting versus an adversary's achievable inflation under active manipulation — not a
  disagreement about the same figure.
- `TAHERIBOSHROOYEH-ARXIV-22` and `REVUELTA-DLT-24` both benchmark Rate-Limiting-Nullifier proof
  generation time, but at different Merkle-tree depths (representing group sizes of roughly 4
  billion against roughly 1 million) and on different hardware; the resulting times (approximately
  0.5 s against a range of 86 ms-767 ms across five platforms) are not measurements of the same
  configuration and are not a disagreement.
- No abstract-versus-conclusion inconsistency was found within any single domain-I entry.

## Family scope not covered by a finding

Storage-payment outcomes (`COX-SOSP-03`, `VISHNUMURTHY-P2PECON-03`, `GOLLE-EC-01`,
`NGAN-IPTPS-03`) and anonymous-token issuance/redemption cost (`DAVIDSON-POPETS-18`,
`KREUTER-CRYPTO-20`, `SILDE-FC-22`, `BENHAMOUDA-ASIACRYPT-23`, `TYAGI-EUROCRYPT-22`,
`EVERSPAUGH-USENIXSEC-15`) were checked; the entries compare non-identical constructions on
non-identical metrics (operation counts against wall-clock benchmarks, or different threat
models), and none disagree about a shared measured quantity under matched conditions.
