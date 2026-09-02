## [GUPTA-SIROCCO-20] Resource Burning for Permissionless Systems
**Citation:** Diksha Gupta, Jared Saia, Maxwell Young. "Resource Burning for Permissionless Systems." SIROCCO 2020 (invited paper). DOI 10.1007/978-3-030-54921-3_2.
**Retrieved:** full text via https://arxiv.org/abs/2006.04865 (arXiv:2006.04865v1)
**Source URL:** https://arxiv.org/abs/2006.04865
**Domain:** F

### What it does
This is a survey and position paper, not a paper reporting a new measured mechanism; it defines a
general framework, restates published cost bounds from four application domains, and states five
open problems. No number in this entry is a new result of this paper — each cited bound below
belongs to the paper it cites, and this entry records only what Gupta, Saia, and Young report
about it.

Resource burning is defined as verifiable consumption of a resource, where both the amount
consumed and the identifier (ID) that consumed it are computationally easy to check, done solely
to force an entity to prove distinct provenance before receiving an identity or performing an
action. The paper generalizes proof-of-work (the resource is computation) to any tunable
resource: CAPTCHAs (the resource is human effort spent solving a puzzle), proof-of-space (the
resource is storage), and resource testing (the resource is exclusive access to a wireless
channel, verified by demanding an echoed response on a randomly chosen channel that an
adversary controlling multiple identities on one radio cannot cover). The paper explicitly
excludes proof-of-stake from this category: proof-of-stake measures an already-held resource
(a cryptocurrency balance) rather than consuming one, and requires that stake be globally
knowable, which the paper states restricts its use mainly to cryptocurrency systems.

The paper's general model: identifiers are good (single real user, follows protocol) or bad
(adversary-controlled); a single adversary controls all bad identifiers and can schedule their
joins and departures adversarially, view good identifiers' messages before acting, but cannot
predict a good identifier's private random bits in advance. The adversary spends resources at
rate T (adversarial spending rate: total adversary cost over system lifetime divided by
lifetime); good identifiers collectively spend at algorithmic spending rate A. For churn
problems, JG denotes the join rate of good identifiers and PG the posting rate of good
identifiers (both defined the same way, as a count over system lifetime divided by lifetime).
The paper models resource-burning defense as a two-player zero-sum game between an attacking
adversary and a defending algorithm, and derives that at Nash equilibrium the algorithm's
expected utility is Θ(−f(0)) when the adversary sets T to its own advantage, for defense-cost
function f.

### Measured results
This paper contains no original experiments. It reports cost bounds proved or conjectured by
other cited work, organized by the domain in which the resource is burned.

| Domain | Resource burned | Cost bound reported | Source cited |
|---|---|---|---|
| Blockchain identifier generation (GenID: static set of identifiers, at most an O(α) fraction adversarial in the final set) | computation | latency 3 rounds, Õ(n²) bits sent per good identifier, O(1) burned cost per good identifier | Aspnes, Jackson, Krishnamurthy (cited [11]) |
| GenID, alternate construction | computation | latency Θ(n) rounds, Õ(n²) bits sent per good identifier, Õ(1) burned cost per good identifier | Andrychowicz, Dziembowski (cited [10]) |
| GenID, randomized leader election | computation | expected latency Θ(ln n / ln ln n) rounds, Õ(n) bits sent per good identifier, burned cost Θ(ln n / ln ln n) per good identifier | Hao et al. (cited [67]) |
| GenID, most recent | computation | expected O(1) latency, O(n) bits sent per good identifier, O(1) burned cost per good identifier | Aggarwal et al. (cited [4]) |
| DefID (GenID under churn: at most O(α)-fraction bad identifiers at any time) | computation | algorithmic spend rate O(JG + T), no additional assumptions | Gupta, Saia, Young (cited [58]) |
| DefID, improved | computation | algorithmic spend rate O(JG + √(T·JG)), subject to two assumptions on good-identifier join-rate stability across epochs (an epoch is defined as the time for the good-identifier fraction to change by 3/4), stated to be supported by real-world data | Gupta, Saia, Young (cited [59,60]); matching lower bound obtained for a large class of algorithms in [59] |
| Distributed hash table (DHT), conjectured | computation | Õ(√(T·JG) + JG), a conjectured extension of the DefID bound with a logarithmic-factor increase from group membership | This paper's own conjecture (Section 4.2), not proved |
| Application-layer distributed denial-of-service (DDoS) defense | bandwidth/computation | no conjectured closed-form bound; stated as an open problem | This paper (Open Problem 4) |
| Review spam | human classification time | conjectured Õ(T^(2/3) + PG) | This paper's own conjecture (Section 6.1), derived from a "preliminary analysis," not proved |

The paper additionally cites two real-world resource-consumption figures, without deriving them:
Bitcoin's May 2020 annual energy consumption at 57.92 terawatt-hours (compared to Bangladesh's
annual electricity consumption), Ethereum's at 7.9 terawatt-hours (compared to Angola's), and an
estimated 150,000 human-hours per day spent solving CAPTCHAs in 2012 (citing separate prior
sources [39], [114], [137]).

### Parameters
- α: the fraction of a burnable resource the adversary is assumed to control. The paper states α must be a small constant (often below 1/3 or 1/4) in settings requiring correctness guarantees, and may be any constant bounded away from 1 in settings requiring only performance guarantees. The permissionless-DHT open problem (Problem 3) is stated to assume α < 1/3.
- T (adversarial spending rate), A (algorithmic spending rate), JG (good-identifier join rate), PG (good-identifier posting rate): all defined as a total cost or count over the system lifetime, divided by that lifetime; no numeric value is given for any of them, they are the free variables the cited cost bounds are stated in terms of.
- Puzzle/challenge difficulty x: the model assumes an identifier can be issued a challenge of any difficulty x requiring consumption of x units of the chosen resource; no specific tuning rule for x is given as settled, and several cited works (Mankins et al., Wang and Reiter, Noureddine et al.) are described as offering different, unresolved approaches to setting it.

### Stated limitations
The paper states it is not known whether the GenID costs it cites can be reduced further for the
general problem or for an "almost-everywhere" variant (where an o(1) fraction of identifiers need
not learn the final set), and that no lower bound exists yet for the general GenID problem. It
states that extending the DefID matching lower bound (currently proved only for "a large class of
algorithms") to all algorithms is an open problem. Current DefID solutions depend on a
committee — a small identifier set with a good majority — coordinating resource burning, and the
paper states that "additional work is required" to decentralize this coordination for use in a
DHT (distributed hash table). It states DefID's majority-of-good-identifiers guarantee at the
network level is insufficient by itself for group-based DHT constructions, which additionally
require a minority of bad identifiers inside every individual group, and that maintaining this
per-group property under continual identifier shuffling "incurs large bandwidth costs" not yet
minimized jointly with resource-burning cost — stated as an explicit open problem (Open Problem 3).
It states no conjectured cost bound exists yet for application-layer DDoS defense (Open Problem 4)
because request cost heterogeneity breaks the direct analogy to DefID's uniform join/departure
events, leaving "a tight upper bound... an interesting direction for future work." The review-spam
conjecture is stated to follow only from "a preliminary analysis," not a proof. Proof-of-stake is
stated to require that each identifier's stake be globally knowable, restricting its applicability
mainly to cryptocurrency systems even setting aside other unresolved concerns the paper reports as
an attributed quote from a named researcher.

### Requirements it places on the rest of the system
A resource-burning defense requires a means to verify both that the claimed resource was consumed
and which identifier consumed it — the paper's own definition makes this a hard requirement, not
an implementation detail. Requires the resource's cost to be arbitrarily tunable per identifier
(a challenge of difficulty x consumes x units), which the paper states holds naturally for
computation, memory, and bandwidth, and requires an explicit adjustment scheme (puzzle difficulty
or challenge probability) for CAPTCHAs. The DefID and DHT bounds require an assumption of
bounded, epoch-to-epoch-stable good-identifier join-rate behavior to reach the improved
O(JG + √(T·JG)) bound; absent that assumption, only the weaker O(JG + T) bound applies. Applying
DefID-style bounds to a DHT requires a committee mechanism — a small identifier group with a
built-in good majority — to issue and validate resource-burning challenges, and the paper states
this committee functionality itself still needs to be decentralized for a permissionless DHT.
The review-spam conjecture requires an available classifier that labels each post as spam or
legitimate with a fixed, known error probability, supplied by a component outside this paper's
scope (the paper cites classification accuracy near 90% from a separate work, [110], as existing
infrastructure this conjecture assumes).

### Contradicts
None found among the papers in this corpus. This paper explicitly distinguishes itself from
proof-of-stake mechanisms, which it classifies as not resource burning because they measure
rather than consume a resource — a definitional statement, not a disagreement with a measured
result elsewhere in this corpus.

### References worth retrieving
- J. Douceur. "The Sybil Attack." IPTPS 2002 (cited [41]) — foundational
- C. Dwork, M. Naor. Computational puzzles for spam (1993) (cited [43]) — foundational (origin of resource burning as a defense concept)
- J. Aspnes, C. Jackson, A. Krishnamurthy. GenID original solution (cited [11]) — foundational
- M. Andrychowicz, S. Dziembowski. GenID algorithm (cited [10]) — competing (alternative GenID cost tradeoff)
- J. Katz, A. Miller, E. Shi. GenID concurrent solution (cited [81]) — competing
- S. Hao et al. Randomized leader election for GenID (cited [67]) — competing
- D. Gupta, J. Saia, M. Young. DefID original and improved algorithms (cited [58], [59], [60]) — foundational (this paper's own authors' prior work, the direct basis of the DHT conjecture)
- F. Li, P. Mittal, M. Caesar, N. Borisov. "SybilControl: Practical Sybil defense with computational puzzles." (cited [88]) — competing (the paper's own "arguably best-known" DHT-specific resource-burning Sybil defense, evaluated on Chord)
- G. Danezis et al. Bootstrapping heuristic for limiting bad-identifier impact in DHTs (cited [37]) — competing (explicitly noted to provide "no formal guarantees")
- N. Borisov. "Computational puzzles as Sybil defenses." (cited [31]) — competing
- H. Rowaihy et al. Computational puzzles throttling identifier addition rate in structured P2P (cited [116]) — competing (explicitly noted to throttle rate but not limit total count)
- M. Walfish et al. "Speak-up" bandwidth-based DDoS defense (cited [138]) — competing
- A. Alvisi, A. Clement, A. Epasto, S. Lattanzi, A. Panconesi. "SoK: The Evolution of Sybil Defense via Social Networks." IEEE S&P 2013 (cited [7]) — foundational/survey (already in corpus per BRIEF §4.4)
- C. Lesniewski-Laas, M. F. Kaashoek. "Whanau: A Sybil-proof DHT." (cited [86]) — competing (already in this batch, LESNIEWSKI-LAAS-NSDI-10)
- H. Yu, M. Kaminsky, P. Gibbons, A. Flaxman. "SybilGuard." (cited [154]) — foundational
- H. Yu, P. Gibbons, M. Kaminsky, F. Xiao. "SybilLimit." (cited [153]) — foundational

### Verbatim extracts
- "verifiable consumption of a resource"
- "it is computationally easy to verify both the consumption of the resource, and also the ID"
- "PoS involves a measurement, rather than a consumption of, a resource"
- "additional work is required to limit the fraction of bad IDs in the permissionless setting"
- "a tight upper bound is an interesting direction for future work"
- "there are no current lower-bounds on the problem"
