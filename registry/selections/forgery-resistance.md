## Forgery resistance: No social-graph defense bounds Sybil identity count on a real network; a write priced in memory-hard computation bounds an entity's write rate to compute it controls, independent of identity count

Forgery resistance is the property that lets a component elsewhere in the system (search ranking,
replication, a per-viewer aggregate over signed claims) treat one entity's influence as bounded by
the real resources that entity controls, so that splitting into many identities does not multiply
what that entity can do. Four candidate mechanisms attempt this: ranking or partitioning a social
graph to detect fabricated identities, certifying that one credential corresponds to one human,
charging computation for each write, and charging a forfeitable staked deposit for each write. The
first two try to bound the count of identities directly; the corpus shows both fail to reach that
goal on a real network. The last two do not try to count identities at all — they price each
write in a resource, so an entity's total achievable write rate is bounded by (resource it
controls) / (price per write), regardless of how many identities issue those writes.

### Candidates

| Mechanism | Measured cost (experimental conditions) | Security assumption required | Condition under which it fails | What it requires from other components |
|---|---|---|---|---|
| Social-graph community detection (SybilGuard/SybilLimit/SybilInfer/ACL/SybilRank family) | Exact max-flow underlying the credit-network variant of this family: 0.352 s (Renren, 1.4M links) to 220 s (Orkut, 234M links) per query on a dual-12-core Xeon X5650 `VISWANATH-EUROSYS-12`. SybilRank's power-iteration ranking processes a 160-million-node synthetic graph in under 33 hours on an 11-node Amazon EC2 cluster, and was deployed on the complete Tuenti graph (11,291,486 nodes, 1,421,367,504 edges) with roughly 100 nodes manually inspected to pick trust seeds `CAO-NSDI-12`. | The honest region of the graph forms one fast-mixing community reachable by a bounded number of attack edges from a trusted seed `YU-SIGCOMM-06`, `YU-SP-08`, `VISWANATH-SIGCOMM-10`. | On a real 21,297,772-node Twitter graph, the benign/Sybil partition has modularity 0.0042 — the paper's own cited threshold for detectable community structure is 0.3 — and restricting to the largest Sybil connected component raises modularity only to 0.0046 `GAO-CNS-18`. An adversary who places attack edges at the k nodes nearest the trusted seed, instead of uniformly at random, drives detection accuracy on a real Facebook graph first to random (0.5) and then below it, so Sybils outrank honest nodes `VISWANATH-SIGCOMM-10`. Under the isolated-Sybil attack pattern actually observed on RenRen, five tested schemes (SybilLimit, SybilGuard, Mislove's community detection, GateKeeper, ACL) score 0.34–0.49, all at or below random `ALVISI-SP-13`. Real graphs (correlation coefficient −0.81 between modularity and detection accuracy across 8 datasets) show weaker community structure than the synthetic graphs the schemes were validated on `VISWANATH-SIGCOMM-10`. | A designated trusted seed per verifying node, whose selection and refresh procedure neither `VISWANATH-SIGCOMM-10` nor `ALVISI-SP-13` specifies. A materialized or locally samplable social graph with mixing time varying by more than an order of magnitude across real networks (100–400 steps for Wiki-vote/Slashdot/DBLP/YouTube/Facebook versus 1,500–2,500 for LiveJournal, at ε=0.1) `MOHAISEN-IMC-10`, so the deploying system must measure its own graph's mixing time rather than assume it. Manual, out-of-band verification of trust-seed accounts — roughly 100 per deployment in `CAO-NSDI-12`'s own case. |
| Proof of personhood (biometric enrollment, government-document matching, or reverse-Turing-test / web-of-trust ceremonies certifying one credential per human) | The cryptographic wrapper alone, once a personhood proof is already available: 10.42 ms sign, 11.24 ms verify, threshold issuance 0.0651 s (t=5,n=10) to 72.6 s (t=150,n=300) `CRITES-CCS-25`. The personhood check itself is not measured: Idena's reverse-Turing test (FLIP) reaches 95% human accuracy against 60–76% for the best attacking AI teams, cited by the paper from a source it does not independently verify `SIDDARTH-FRONTIERS-20`. | An external, off-protocol channel correctly binds one credential to one human and refuses a second credential to the same human `CRITES-CCS-25`, `ADLER-ARXIV-24`. | `CRITES-CCS-25`'s own construction states plainly that it does not build this channel — it lists a signed government certificate, a biometric reading, or an OAuth token as possible instantiations and states security holds "only when at least t of the n issuers behave honestly," which is a claim about the cryptographic wrapper, not about whether the plugged-in personhood check itself resists forgery. Every web-of-trust instantiation (BrightID, Duniter, Kleros/Proof of Humanity) inherits the community-detection failure above: a person can obtain a second credential by enrolling through a second, non-intersecting vouching group, because vouching validates that a person exists without bounding how many distinct graphs will vouch for the same person `ADLER-ARXIV-24`, `SIDDARTH-FRONTIERS-20`. A reverse-Turing test alone "fails to address human-generated attacks, in which one individual passes the test multiple times and creates multiple different identities" `SIDDARTH-FRONTIERS-20`. Biometric enrollment depends on a TEE (trusted execution environment) deployment the corpus records as having already been discontinued after a disclosed DRAM-bus-interposition attack against the specific TEE product one such scheme names `LAS-EPRINT-26`. | An external personhood-verification channel this component cannot itself build or verify, per `CRITES-CCS-25`'s own stated scope. A functioning, sufficiently liquid financial-stake market and a dispute-resolution process for any vouching-with-stake variant `SIDDARTH-FRONTIERS-20`. |
| Computational work priced per write, verified locally by every relaying or storing peer | The base hash-based construction reports no usable minting figure — `BACK-HASHCASH-02` states only that it "describes initial experience from experiments" with no run count, hardware, or wall-clock time given. A memory-hard cost function does have measured figures, for the closely related password-hashing use: scrypt at N=2^20 (3.8 s per evaluation on a 2.5 GHz reference core) raises the estimated one-year brute-force hardware cost for an 8-character password to roughly $19 billion, against $18,000 for PBKDF2 at the same wall-clock target, both derived from 130 nm circuit die-area and manufacturing-cost data `PERCIVAL-BSDCAN-09`. Argon2d evaluates at 0.6 cycles/byte at 4 threads on a Haswell i7-4500U, filling 1 GB of memory in under a second `BIRYUKOV-EUROSP-16`. Verification of a Hashcash-style token is one hash evaluation `BACK-HASHCASH-02`; verification of a memory-hard token is one full evaluation of that function. | An entity's achievable write rate is bounded by (compute it controls) / (difficulty per write), independent of how many identities it presents: a faulty entity commanding resources ρ times a minimally capable entity's resources can obtain g = ρ times that entity's write rate, no more `DOUCEUR-IPTPS-02` (Lemma 1). | Bounded on both sides by the same free parameter, the required difficulty: set too low, the throttle enforces nothing; set too high, honest participants on constrained hardware (mobile, embedded) cannot sustain any write rate at all. Plain hash-based work lets specialized hardware mint at a cost per hash orders of magnitude below a commodity CPU's, breaking the assumption that compute controlled tracks resources controlled evenly across participants; a memory-hard cost function narrows this but does not close it — `ALWEN-EUROSP-17` measured a 2x cost reduction against Argon2i-B at 1 GB memory and 6 passes, inside the parameter region the function's own designers' analysis (`BIRYUKOV-EUROSP-16`) had called safe. A non-interactively minted token can be produced in advance from idle compute and spent in a burst later, unless bound to an unpredictable, frequently changing value — a mitigation `BACK-HASHCASH-02` proposes but does not implement or measure. | Local verification of the attached proof by every peer that relays or stores the write, at the cost of one hash or one memory-hard evaluation per write. A spent-token or nullifier store, retained at least as long as the token's validity window, at every verifying peer, plus loosely synchronized clocks across peers to bound that window without either rejecting valid recent tokens or letting the store grow unboundedly `BACK-HASHCASH-02`. A canonical, per-write target string bound into the proof (the write's own content address or destination), so a solved token cannot be replayed against a different write `BACK-HASHCASH-02`. |
| Resource-based admission: a forfeitable staked deposit priced per write, recovered by cryptographic slashing on detected double-use (Rate-Limiting Nullifier construction) | Membership-proof generation ≈0.5 s on an iPhone 8 at a group size of 2^32; proof verification ≈30 ms, constant regardless of group size; per-peer identity-commitment-tree storage 67 MB at depth 20 (up to ≈1,048,576 members); on-chain registration or deletion costs 40,000 gas, stated to exceed 20 USD "at the time of writing" `TAHERIBOSHROOYEH-ARXIV-22`. | A globally consistent, slashable ledger of deposits exists and is itself resistant to the same forgery this mechanism defends against, and at least one honest routing peer observes any double-signal within the retained epoch window `TAHERIBOSHROOYEH-ARXIV-22`. | The paper's own authors state the bound is not eliminated, only priced: an entity that registers k identities and pays k times the deposit obtains k writes per epoch rather than one, a limitation they say "can only be raised in cost, not eliminated, by increasing the membership fee." A spammer can withdraw its deposit before a routing peer catches and reports a double-signal, forfeiting only the registration cost rather than the full stake a slasher would otherwise claim `TAHERIBOSHROOYEH-ARXIV-22`. | A smart-contract-capable, globally ordered ledger the deployed instance builds on Ethereum specifically; every verifying peer independently reconstructing the identity-commitment tree from that ledger's event stream, since the contract itself stores only the ordered public-key list, not the tree; a zkSNARK verifier for the specific proof system used (Groth16), and, if a single-party trusted setup is unacceptable, a multi-party setup ceremony trusted by every verifier; loosely synchronized clocks to define the shared epoch boundary `TAHERIBOSHROOYEH-ARXIV-22`. |

### Selection

Computational work priced per write, verified locally by every peer that relays or stores the
write, with no identity system consulted at all. An entity's total achievable write rate across
every identity it holds is bounded by the compute it controls divided by the difficulty set per
write — Douceur's Lemma 1 states this bound formally for any resource-demanding challenge `DOUCEUR-IPTPS-02`
— and identity count plays no part in the bound, because minting a fresh identity costs nothing
while producing a fresh write still does.

Against social-graph community detection: rejected because the corpus establishes the mechanism
does not reach its stated goal on a real network, not merely that it costs more than an
alternative. `GAO-CNS-18` measures modularity 0.0042 on a 21,297,772-node Twitter graph, against
the 0.3 threshold the field itself uses for detectable community structure — the graph property
every scheme in this family assumes is, on this measured real network, absent by two orders of
magnitude. `ALVISI-SP-13` and `VISWANATH-SIGCOMM-10` are two independent analyses that reduce every
published social-graph scheme to the same underlying operation, local community detection around a
trusted seed, and both measure that an adversary who chooses which honest nodes to attach Sybils
to, rather than attaching uniformly at random, defeats it: accuracy at or below random guessing
(0.34–0.49 across five schemes in `ALVISI-SP-13`; below 0.5, meaning Sybils outrank honest nodes, in
`VISWANATH-SIGCOMM-10`'s Facebook experiment). A mechanism whose own literature shows it degrading to
worse than a coin flip under the attack it exists to resist is not a workable candidate, regardless
of what it costs to run.

Against proof of personhood: rejected because no entry in this corpus builds the mechanism the
approach depends on. `CRITES-CCS-25`'s own construction states it does not supply the personhood
relation — the check that a claimed identity string corresponds to one real, previously-unenrolled
human — and lists a government certificate, a biometric reading, or an OAuth token as external
instantiations whose own forgery resistance the paper does not evaluate. Every instantiation this
corpus does evaluate that avoids depending on an external, centrally-operated issuer instead
depends on a social graph of vouches, which `ADLER-ARXIV-24` and `SIDDARTH-FRONTIERS-20` both state
fails on exactly the axis social-graph community detection fails on: a person obtains a second
credential by enrolling through a second, non-intersecting vouching group, since vouching
establishes that a person exists without bounding how many distinct groups will vouch for the same
person. A reverse-Turing test (Idena's FLIP, 95% human accuracy against 60–76% for the best
attacking AI team, `SIDDARTH-FRONTIERS-20`) distinguishes a human from a machine, which is a
different claim from distinguishing one human from many humans, and does not bound identity count
by itself.

Against resource-based admission (staked deposit with slashing): not rejected as broken — measured,
deployed-scale figures exist for it (`TAHERIBOSHROOYEH-ARXIV-22`: 0.5 s proof generation, 30 ms
verification, 67 MB tree storage at 2^20 members) and its own authors state the same
resources-not-identity-count property this selection is chosen for: k identities cost k deposits
for k writes, a bound that is priced rather than eliminated, matching what per-write compute cost
also delivers. The two mechanisms are preferred on what each requires from the rest of the system,
not on what either costs to run. Staked-deposit admission requires a globally ordered,
smart-contract-capable ledger recording and slashing balances — in the measured deployment,
Ethereum specifically — plus every verifying peer holding a live view of that one ledger's state
`TAHERIBOSHROOYEH-ARXIV-22`. That ledger's own forgery resistance (why an attacker cannot mint
arbitrary balances to stake) is a second, unstated instance of the same problem this component
exists to solve, pushed onto whichever component secures the ledger rather than solved locally.
Per-write compute cost needs no ledger, no consensus over balances, and no external asset: any peer
independently checks one hash or one memory-hard function evaluation against the write's own
content. Where the architecture already includes a global consensus ledger for an unrelated reason,
staked-deposit admission becomes attractive on its measured constant-time, sub-second-latency
verification (`TAHERIBOSHROOYEH-ARXIV-22`); absent one, requiring it here to solve forgery resistance
adds exactly the centralized dependency the rest of the design exists to avoid.

### What this selection requires from the rest of the system

- Every peer that relays or stores a write verifies the attached proof before consuming further
  bandwidth or storage on that write — one hash evaluation for a plain construction, one full
  memory-hard function evaluation for the hardened variant `BACK-HASHCASH-02`, `BIRYUKOV-EUROSP-16`.
- The proof is bound into a canonical, per-write target string — the write's own content address or
  destination — derived by the canonical-encoding / content-addressing component, so a solved proof
  cannot be replayed against a different write; `BACK-HASHCASH-02` states a token not bound this way
  can be replayed against a resource other than the one it was minted for.
- Every verifying peer holds a spent-token or nullifier store, keyed by the proof's own value, and
  loosely synchronized clocks across peers to bound how long that store must retain an entry before
  the token's own validity window expires; too short a window and legitimate recent writes are
  rejected, too long a window and the store grows unboundedly `BACK-HASHCASH-02`.
- No identity, key-transparency, or admission component is consulted by this mechanism at all —
  this is the resources-not-identity-count property itself. Any per-identity quota or rate limit
  elsewhere in the architecture is a separate mechanism this component neither supplies nor
  interferes with; the composition between the two (whether a per-identity quota and a per-write
  price compound or substitute) is not addressed by anything in this corpus.
- The deploying system independently estimates or bounds ρ, the ratio between the most and least
  capable participant's compute it intends to admit, since `DOUCEUR-IPTPS-02`'s Lemma 1 ties the
  resulting write-rate advantage directly to that ratio and supplies no method for measuring or
  enforcing it.
- If tokens are minted non-interactively (no live challenge from the verifying peer), the
  per-write target string should incorporate a value that changes unpredictably and frequently — a
  public beacon — to prevent an entity from banking tokens from idle compute today and spending
  them in a burst later; `BACK-HASHCASH-02` proposes this without implementing or measuring it.

### What it costs and where it fails

No entry in this corpus measures a deployed wall-clock or dollar cost for a hash-based per-write
proof in this exact use — `BACK-HASHCASH-02` states explicitly that its own reported experience
carries no usable run count, hardware, or timing figure. The closest measured figures are for a
different use of a memory-hard cost function, password-hashing rather than a write-rate throttle:
`PERCIVAL-BSDCAN-09` derives that scrypt at a 3.8-second-per-evaluation setting (N=2^20) raises
estimated one-year brute-force attacker hardware cost to roughly $19 billion, against $18,000 for
PBKDF2 at the same wall-clock target, both figures derived from circa-2002, 130 nm circuit
die-area data the authors themselves call "very approximate." Argon2d evaluates at 0.6 cycles per
byte at four threads on a Haswell-generation commodity CPU, filling 1 GB of memory in under a
second `BIRYUKOV-EUROSP-16` — the cost an honest participant pays per unit of difficulty, on
hardware from that period.

The mechanism fails on the same axis on both sides of one bounded range: below some difficulty
setting the throttle imposes no real cost, so an entity with even modest excess compute floods
writes unopposed; above some difficulty setting, a legitimate participant on constrained hardware
(a mobile device, an embedded node) cannot sustain any write rate the mechanism will accept. No
entry in this corpus derives or measures where that boundary falls for a decentralized write-rate
throttle specifically — every cost figure available is for a different application (password
hashing) at a different latency target (0.1–5 seconds per single evaluation, chosen for
interactive login or file-encryption use, not for a sustained per-write rate) `PERCIVAL-BSDCAN-09`,
`BIRYUKOV-EUROSP-16`.

It also fails when the difficulty function's own hardness assumption is wrong: `ALWEN-EUROSP-17`
measured a concrete 2x cost reduction against Argon2i-B at 1 GB memory and 6 passes, a parameter
region its own designers' published security analysis (`BIRYUKOV-EUROSP-16`) had concluded was
safe, using heuristics that analysis did not consider. A memory-hard cost function narrows the gap
between commodity and specialized attacker hardware relative to a plain hash function; it does not
close that gap to zero, and the corpus records at least one case of the designers' own safety
margin being wrong in practice.

### What the corpus does not settle

1. No entry measures a deployed wall-clock or dollar cost for computational work priced per write
   in a peer-to-peer network specifically — every cost figure available in this corpus for a
   compute-cost mechanism is either a symbolic bound with no numeric value (`DOUCEUR-IPTPS-02`) or a
   measurement for password-hashing at a different latency target (`PERCIVAL-BSDCAN-09`,
   `BIRYUKOV-EUROSP-16`). A solution needs a measured figure for minting and verification cost at a
   difficulty calibrated specifically to a sustained per-write throttle, on hardware ranging from a
   commodity mobile device to purpose-built attacker hardware.
2. No entry measures what write rate a legitimate participant on the least capable hardware this
   architecture intends to admit can sustain at any given difficulty setting, so the corpus supplies
   no way to place the operating point within the bounded range stated above.
3. No entry measures the real-world ratio ρ between the most and least capable participant's
   compute in a deployed, heterogeneous peer-to-peer network — the one number `DOUCEUR-IPTPS-02`'s
   Lemma 1 needs to state what write-rate advantage the resulting bound actually permits.
4. No entry composes a per-write computational cost with a replication mechanism elsewhere in this
   architecture that itself depends on write or query rate (for instance, a search-feedback-driven
   replication scheme). Whether a per-write cost throttle changes the write pattern such a mechanism
   observes is not addressed by anything in this corpus.
5. No entry measures the effect of the public-beacon mitigation against a precomputation attack —
   `BACK-HASHCASH-02` proposes it without implementing or measuring it, so its actual cost and
   effectiveness against a well-resourced adversary banking tokens over time is unmeasured.
6. Whether a memory-hard cost function's hardware-heterogeneity advantage (commodity CPU against
   specialized attacker hardware) is adequately bounded for this specific threat model — an
   adversary that controls a botnet of ordinary consumer devices rather than purpose-built hardware
   — is not measured anywhere in this corpus; every measured hardware-cost figure available concerns
   dedicated attacker hardware built to crack passwords, not a botnet of commodity devices already
   under an adversary's control.
