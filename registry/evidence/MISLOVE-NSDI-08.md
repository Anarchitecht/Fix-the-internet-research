## [MISLOVE-NSDI-08] Ostra: Leveraging Trust to Thwart Unwanted Communication
**Citation:** Alan Mislove, Ansley Post, Peter Druschel, P. Krishna Gummadi. "Ostra: Leveraging Trust to Thwart Unwanted Communication." USENIX NSDI, 2008.
**Retrieved:** full text via https://www.usenix.org/legacy/event/nsdi08/tech/full_papers/mislove/mislove.pdf
**Source URL:** https://www.usenix.org/legacy/event/nsdi08/tech/full_papers/mislove/mislove.pdf
**Domain:** F

### What it does
Ostra bounds the rate at which a sender can push unwanted communication (spam, unsolicited
messages, unsolicited shared content) to other users, in proportion to that sender's number of
trust links, without classifying message content and without requiring a single strong identity
per user.

Ostra assigns a credit balance to each link of a trust network (a graph in which an edge
represents a relationship costly to form and maintain, such as a mutual social-network
connection), not to each user identity. Each link's balance B stays within a range [L, U] with L
≤ 0 ≤ U. To send a message, the sender obtains a signed token along the path from sender to
receiver in the trust network: obtaining the token raises the lower bound L on each link along
that path by one unit, reserving capacity. When the receiver classifies the message, if marked
unwanted, one credit transfers from sender to receiver along each link of the path, permanently
lowering the sender-side link's balance and raising the receiver side's; if marked wanted, the
reservation is undone and no credit moves. A link whose balance reaches L blocks further
sends across it until the balance recovers. Because the total credit summed over all links is
conserved at every operation (Table 1: join, wanted send, unwanted send, and decay each leave
total system credit at 0), colluding users cannot manufacture additional sending capacity by
creating more identities — they can only redistribute the fixed credit among themselves, and any
message that reaches a victim outside their group must still cross at least one real link into
the honest region of the trust graph.

Two auxiliary mechanisms prevent legitimate users from becoming permanently blocked. First,
credit balances decay toward 0 at a constant fractional rate d per unit time, absorbing the
natural imbalance between credit a well-behaved user earns (by receiving unwanted messages) and
loses (by occasionally sending a message someone else classifies as unwanted). Second, a
non-owned overflow account C with no upper bound lets a user who has accumulated too much
credit (from being targeted) deposit it, freeing her links to receive further messages; deposited
credit still decays, so system-wide credit does not grow. A timeout T resets an unclassified
message's reservation as though it had been marked wanted, preventing indefinite credit lock-up
from dropped messages or long receiver absence.

A decentralized variant (Section 7) removes the assumption of a trusted central site that holds
the full trust graph. Each user runs an agent holding her own link balances; route discovery
combines a Bloom filter (a probabilistic set-membership structure) advertising each user's
two-hop neighborhood for short paths with landmark routing (a small set of well-known reference
nodes with published hop-distances) for longer paths. Authorization and classification messages
propagate along the discovered path, and each forwarding node has an incentive to relay
correctly because a node that drops a message is penalized (has its own outgoing credit
lowered) by its predecessor after timeout T.

### Measured results

| Result | Conditions |
|---|---|
| At 1% of the network as attackers (4,096 of the network), each legitimate user receives 0.22 unwanted messages/week (≈12/year) | YouTube-derived trust network, 446,181 users, 1,728,938 symmetric links; L=-3, U=3, d=10%/day; attackers vary 1 to 4,096 (0.0002%–1% of network); each good user sends 2 messages, each attacker sends 500 |
| Unwanted messages received scales linearly with the proportion of attackers, matching the analytic bound d·L·D+S | Same YouTube-derived network and parameters; three traffic models compared: Random, Proximity (destination distribution matching the measured email trace), and YouTube (single high-degree, 1,376-link target account) |
| Increasing the maximum credit imbalance per link L increases unwanted messages received | Same network; L varied from 1 to 100 |
| At 30% false-positive rate for classifying legitimate messages as unwanted, only a small proportion of messages are blocked, in the messaging-system model (Random/Proximity) | Same network |
| At 64% false-classification rate, ~40% of messages cannot be sent, in the content-sharing model (YouTube, single shared target account) | Same network |
| Min-cut analysis: proportion of user pairs (out of 3,000 randomly sampled) whose min-cut is not adjacent to either endpoint decreases as the lower of the two users' degrees increases, meaning better-connected users are less exposed to link-exhaustion attacks | YouTube-derived trust network, uniform link weight of 1 |
| Email-trace destination selection: 93% of messages sent to a friend or friend-of-friend, versus an expected 14% under random destination selection | 100-day anonymized email trace, 2 institutes, ~200 researchers; extracted social network of 150 users linked by ≥3 emails exchanged, covering 13,978 emails |
| Message delay under credit-bound throttling with L=-3, U=3: send delayed 0.38% of the time (avg 2.2h) at 2h avg. classification delay; 0.57% of the time (avg 6.1h) at 6h avg. classification delay; receive delayed 1.3% of the time in both cases (avg 4.1h and 16.6h respectively) | Same email trace; 95% of the trace's 1,003,819 received messages were randomly discarded to simulate removing junk mail (administrators estimated ~95% of incoming mail was junk); >98% of delayed receive-messages concentrated on 3 users |
| Bloom-filter routing: >90% of users' Bloom filters smaller than 4 kilobytes; with 765 landmark users (0.16% of population), remaining users can route to >89% of the network | Preliminary analysis on the same YouTube-derived trust network; unrouteable users mostly single-link, weakly connected |
| Degree-distribution comparison: YouTube power-law coefficient 1.66 (Kolmogorov-Smirnov goodness-of-fit 0.12), LinkedIn coefficient 1.58 (goodness-of-fit 0.05) | Maximum-likelihood fit; used to argue YouTube's graph structure is comparable to a genuine trust network like LinkedIn's despite YouTube not itself meeting Ostra's link-cost requirement |

### Parameters
- L (lower credit bound per link): tested 1 to 100 in the sensitivity experiment (Figure 9); L=-3 used as the conservative operating point in the main evaluation.
- U (upper credit bound per link): U=3 used in the main evaluation; U=L in magnitude by symmetry in the examples given.
- d (daily credit decay rate): 10% per day used in the main evaluation; the paper states d must be "high enough to cover the expected imbalance but low enough to prevent considerable amounts of intentional unwanted communication," with no derivation of the 10% figure beyond the trace-based sensitivity result.
- T (classification timeout): stated only as "typically on the order of days," no specific value derived or tested.
- Attacker population: varied 1 to 4,096 nodes (0.0002% to 1% of a 446,181-node network) in the sensitivity experiment; 512 attackers (≈0.1%) used as the default elsewhere.

### Stated limitations
The paper states the YouTube social network used for evaluation does not strictly meet Ostra's
own requirement of non-trivial cost to form and maintain a link, because YouTube subscription
links cost nothing to create; the authors substitute it because genuine trust networks such as
LinkedIn cannot be crawled for privacy reasons, and justify the substitution only by a
degree-distribution similarity argument, not by directly measuring Ostra's performance on a real
trust network. The authors state this substitution may cause the YouTube-based results to
understate Ostra's real-world performance, because some YouTube accounts reach degree 20,000+ while real trust
networks are bounded by human relationship-maintenance capacity (cited as 150–200). No
communication trace at the same scale as the social network was available; traffic patterns are
inferred from a 200-person, 100-day internal email trace, not measured on the evaluation network
itself. The centralized design requires a trusted entity to hold the complete trust network and
credit state; systems without any trusted component, such as SMTP-based email, require the
decentralized design of Section 7, which the paper describes as a preliminary sketch validated
only by a bloom-filter/landmark routing feasibility measurement, not an end-to-end evaluation.
Ostra requires that joining be by invitation from an existing user, restricting deployment to
"invitation-only" social networks. Ostra depends on receivers actively classifying messages as
wanted or unwanted; the paper acknowledges this is a burden and only sketches (without measuring)
implicit-feedback alternatives such as inferring classification from delete/archive/reply
actions. A user whose account password is compromised can still be drained of credit by an
attacker sending through it, bounded by the account's own per-link limits, not prevented.

### Requirements it places on the rest of the system
Requires an underlying trust network in which link formation and maintenance carries a real,
non-zero cost to the participant, so that no user can cheaply create an unbounded number of
identities or links; the paper states this property explicitly does not hold for the YouTube
graph it evaluates against. Requires the trust network to be connected, so that a path exists
between any two user identities. Requires either a single trusted party holding the complete
trust network and credit state (centralized design), or — for the decentralized variant — a
route-discovery layer supplying Bloom-filter neighborhood advertisements and landmark-based
long-path routing, plus every forwarding node maintaining per-link balance state and honoring
signed authorization/classification/timeout messages from its neighbors. Requires receivers to
supply a wanted/unwanted classification for each received communication (or allow a timeout to
default it to wanted); the mechanism does not function without this feedback channel. Requires
new users to be introduced by an existing Ostra user at join time, which the rest of the system's
account-creation flow must supply. Does not require, and explicitly avoids requiring, a single
strong per-user identity — multiple identities per person are tolerated because sending capacity
is a property of trust links, not of identities.

### Contradicts
None found among the papers in this corpus.

### References worth retrieving
- H. Yu, M. Kaminsky, P. B. Gibbons, A. Flaxman. "SybilGuard: Defending against Sybil attacks via social networks." SIGCOMM 2006 — foundational (the random-route/attack-edge model Ostra's credit-conservation argument parallels)
- J. Douceur. "The Sybil Attack." IPTPS 2002 — foundational (defines the Sybil attack Ostra's multiple-identity analysis addresses)
- S. Garriss, M. Kaminsky, M. J. Freedman, B. Karp, D. Mazières, H. Yu. "RE: Reliable Email." NSDI 2006 — competing (a prior trust-based anti-spam system for email)
- M. Walfish, J. Zamfirescu, H. Balakrishnan, D. Karger, S. Shenker. "Distributed Quota Enforcement for Spam Control." NSDI 2006 — competing (quota-based rather than trust-link-based spam bound)
- A. Mislove, M. Marcon, K. P. Gummadi, P. Druschel, B. Bhattacharjee. "Measurement and Analysis of Online Social Networks." IMC 2007 — foundational (source of the structural claims about social-graph density used to argue link-attack resistance)
- P. F. Tsuchiya. "The Landmark Hierarchy: A New Hierarchy for Routing in Very Large Networks." SIGCOMM 1988 — foundational (landmark routing technique reused for decentralized path discovery)
- B. H. Bloom. "Space/time trade-offs in hash coding with allowable errors." CACM 1970 — foundational (Bloom filter used for local-neighborhood route discovery)
- M. Cha, H. Kwak, P. Rodriguez, Y.-Y. Ahn, S. Moon. "I Tube, You Tube, Everybody Tubes." IMC 2007 — foundational (source describing the YouTube dataset structure)

### Verbatim extracts
- "the sum of all credit balances is 0"
- "malicious, colluding users can pass credits only between themselves"
- "each user can produce unwanted communication at a rate of no more than d∗L+S"
- "the YouTube social network does not meet Ostra's requirements, because there is no significant cost"
- "each legitimate user receives only 0.22 unwanted messages per week"
- "more than 90% of users' bloom filters are smaller than 4 kilobytes"
