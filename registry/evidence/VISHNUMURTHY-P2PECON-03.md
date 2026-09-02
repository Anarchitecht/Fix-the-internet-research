## [VISHNUMURTHY-P2PECON-03] KARMA: A Secure Economic Framework for Peer-to-Peer Resource Sharing
**Citation:** Vivek Vishnumurthy, Sangeeth Chandrakumar, Emin Gün Sirer. "KARMA: A Secure Economic Framework for Peer-to-Peer Resource Sharing." Workshop on Economics of Peer-to-Peer Systems (P2PEcon), 2003.
**Retrieved:** full text via https://www.cs.cornell.edu/people/egs/papers/karma.pdf
**Source URL:** https://www.cs.cornell.edu/people/egs/papers/karma.pdf
**Domain:** I

### What it does
KARMA discourages participants in a peer-to-peer system from consuming more resources than they contribute, without a central accounting server. Each participant holds a single scalar balance, called karma, that rises when the participant contributes a resource (a file, a message, a computation result) and falls when the participant consumes one. A resource-consuming operation is refused if the consumer's karma balance is below the price of the operation.

The balance for a node A is not held by A itself. It is held redundantly by a bank-set: the k nodes whose node identifiers are closest, in a circular identifier space, to the hash of A's own identifier. A distributed hash table (the paper builds on Pastry) maps A's identifier to this set of k closest nodes, so the bank-set assignment is a deterministic function of A's identifier rather than a choice A or anyone else makes. Each bank-set member independently stores A's signed balance, the last transaction sequence number, and a recent transaction log.

A karma transfer from consumer A to provider B proceeds as follows. A sends B a message, signed with A's private key, stating the balance A would hold after the transfer and a sequence number that prevents replay. B forwards this to its own bank-set, whose members query BankA. BankA members check that the signed balance A supplied matches their stored balance; if so, they acknowledge, deduct the amount from A's account, and inform A. BankB members that receive a majority of positive acknowledgements from BankA credit B's account and inform B, at which point B transfers the resource to A. Bank-set members act independently and do not run a Byzantine agreement protocol among themselves: commutativity of addition guarantees that once a node stops issuing new transactions, the members of its bank-set converge on the same balance regardless of the order in which they observed credits and debits. A balance may dip transiently negative at one member if that member sees a debit before a credit that a majority of the bank-set saw in the opposite order; the balance is corrected once the credit propagates, so this transient underflow is contained to less than half the bank-set.

A new node obtains its identifier through a cryptographic puzzle: it selects a public/private key pair and a value x such that MD5(public key) matches MD5(x) in the low n digits, then sets its identifier to MD5(public key, x). This ties identifier assignment to a proof of computation the node cannot precompute for a chosen identifier, and n controls the difficulty of that computation. On joining, a node's prospective bank-set members exchange signed account records for it; if more than k/2 of them agree on a balance and sequence number, that balance is adopted, otherwise the node is initialized with a fixed system-wide starting balance and sequence number zero.

To bound long-run inflation or deflation of the total karma supply, the system recomputes a correction factor rho at the end of each epoch (a period the paper describes as typically spanning several months): rho equals (karma_total_at_epoch_start times nodes_active_now) divided by (karma_total_now times nodes_active_at_epoch_start). Each bank-set node broadcasts, at epoch end, the count and unused balances of nodes that went inactive and the count of nodes that joined; every node then computes the new totals and applies rho to the accounts for which it is a bank-set member.

For a file-sharing application built on KARMA, a file is hashed to a rendezvous node, which providers advertise to and seekers query; the seeker runs an auction over the karma bid providers submit and picks the lowest bidder. File delivery itself uses a Certified Mail scheme: the provider sends the file encrypted with a symmetric key, and the consumer receives the decryption key only in exchange for a signed receipt, so a karma transfer completes if and only if the file transfer completes, and vice versa.

### Measured results
The paper is a design paper with one analytic (not experimental) probability computation, no implementation or simulation is reported.

| Result | Conditions |
|---|---|
| Probability that an attacker who has compromised 10% of the nodes in a 1,000,000-node network controls a majority of some single 64-member bank-set is under 5.6 × 10^-12 | Closed-form calculation, not measured: attacker controls 10% of 1,000,000 nodes; expected attacker-controlled members of a given 64-member bank-set is 6.4 (10% of 64); bound derived via a Chernoff-style tail bound P(X > 32) = P(X > (1+4)·6.4) < (e^4/5^5)^6.4 |
| Probability that the attacker controls a majority in at least one bank-set across the whole network is under 5.6 × 10^-6 | Same setting, multiplied by the total number of bank-sets in a 1,000,000-node network at k=64 |
| Simply having peers announce their held content produces "less than a tenth of a percent" bandwidth overhead | This figure appears in the companion BitTorrent paper (COHEN-IPTPS-03), not in KARMA; do not attribute it to this paper |
| Currency-correction protocol requires O(N^2) messages per epoch, where N is the number of nodes in the system | Stated as an asymptotic message-count bound, not measured; the paper argues the cost is acceptable because an epoch spans several months, without stating what "several months" is derived from |

### Parameters
| Parameter | Value used in the paper | Tested range |
|---|---|---|
| Bank-set size k | Used symbolically throughout; the one worked numeric example uses k=64 | No range tested; the paper states only that the system needs "at least k nodes in the system at all times" |
| Node-identifier puzzle difficulty n | Left as "a parameter that can be used to limit the difficulty of the puzzle" | Not specified numerically |
| Epoch length | Described as "typically several months" | Not derived or measured; stated as a design assumption used to argue the O(N^2) correction cost is acceptable |
| Fraction of malicious nodes tolerated by the underlying secure-routing layer | Cited from Castro et al.'s secure routing for structured peer-to-peer overlays as tolerating up to 25% of nodes not adhering to the routing protocol | This bound is imported from the cited secure-routing paper, not derived within KARMA |
| Adversarial fraction in the worked bank-set-corruption example | 10% of a 1,000,000-node network | Single point example, not a range |
| Compensation dampening threshold for bank-node service karma | Example given: award extra karma only after a bank node has performed 10^4 transactions on behalf of others | Presented as an example fix, not a derived or tested value |

### Stated limitations
The paper states that KARMA relies on the identifier-to-bank-set mapping remaining secure, and its own tamper-resilience bound is conditioned entirely on the security of that underlying DHT routing layer: the authors write that "the limiting factor to KARMA's tamper-resilience lies in the p2p routing substrate, and not in the higher level protocols." It leaves the resource-pricing mechanism (how many units of karma a given resource in a given application costs) entirely to the application built on top of KARMA. It states that KARMA cannot prevent Sybil attacks in a peer-to-peer setting without external identifiers, and only limits the rate at which new identifiers can be manufactured through the cryptographic-puzzle join procedure; the authors write they "permit Sybil attacks but limit the rate at which they can be launched." The paper also identifies, without resolving beyond a sketch, a second-order incentive problem: bank-set members themselves have no built-in incentive to perform bank-node work honestly and consistently for other nodes, and the paper's proposed compensation (awarding karma for bank-node service) is presented with the caveat that it risks a runaway chain reaction of compensatory transactions unless a dampening rule is added, and risks violating the zero-sum property of the currency, which the paper says a taxation-based alternative might address instead, without specifying the tax mechanism.

### Requirements it places on the rest of the system
KARMA requires an underlying secure-routing DHT (the paper builds on Pastry with the Castro et al. secure-routing extension) that tolerates a bounded fraction of adversarial nodes and can map a node's hashed identifier to the k nodes closest to that hash; KARMA's own security bound against bank-set corruption holds only conditional on that routing layer's own bound holding. It requires every participant to hold a persistent public/private key pair, established once at join time through the identifier-generation puzzle, and requires all subsequent balance and transaction messages to be signed by that key. It requires the DHT to notify a newly joined or newly failed bank-set member of which accounts now fall under its responsibility, so that node can retrieve those accounts' balances by majority vote from the account's other current bank-set members. It requires an application layer to supply the actual exchange semantics (what resource a transaction concerns, and how many karma units it costs); KARMA supplies only the balance-transfer and file-delivery-atomicity primitives, not pricing. It requires that the fraction of malicious members within any single node's bank-set stay below one-half at the moment of a transaction decision, since the transfer protocol resolves consumer-side and provider-side approval by majority vote within each bank-set. It requires application-level periodic delivery of epoch-boundary join/leave counts and balances between all bank-set members to keep the inflation-correction factor consistent, and tolerates temporary inconsistency between nodes in different epochs only by rescaling in-flight payments with the correction factor.

### Contradicts
None found. No other entry in this batch measures or discusses the karma/bank-set credit-scheme mechanism.

### References worth retrieving
- foundational: A. Rowstron, P. Druschel, "Pastry: Scalable, distributed object location and routing for large-scale peer-to-peer systems," IFIP/ACM Middleware 2001 — the DHT KARMA layers its bank-set assignment on top of.
- foundational: M. Castro, P. Druschel, A. Ganesh, A. Rowstron, D. Wallach, "Secure routing for structured peer-to-peer overlay networks," OSDI 2002 — supplies the 25%-adversarial-node routing-resilience bound KARMA's own security argument depends on.
- attack: J. Douceur, "The Sybil attack," IPTPS 2002 — the attack KARMA states it does not prevent, only rate-limits.
- competing: T. Ngan, D. S. Wallach, P. Druschel, "Enforcing Fair Sharing of Peer-to-Peer Resources," IPTPS 2003 — a fairness mechanism for spatial (storage) resources verified by random audit, which the KARMA authors argue does not extend to temporal resources like bandwidth.
- competing: J. Shneidman, D. Parkes, "Rationality and Self-Interest in Peer to Peer Networks," IPTPS 2003 — mechanism-design framing for incentivizing globally beneficial peer behavior, cited as a parallel approach to KARMA's accounting approach.
- foundational: S. Saroiu, P. K. Gummadi, S. D. Gribble, "A measurement study of peer-to-peer file sharing systems," MMCN 2002 — source of the cited 20-40% Napster / ~70% Gnutella freeloading figures that motivate KARMA.
- foundational: E. Adar, B. Huberman, "Free riding on Gnutella," First Monday 5(10), 2000 — the other cited source for the freeloading motivation, also cited directly by COHEN-IPTPS-03 in this batch.

### Verbatim extracts
- "the limiting factor to KARMA's tamper-resilience lies in the p2p routing substrate, and not in the higher level protocols."
- "We permit Sybil attacks but limit the rate at which they can be launched through our secure entry algorithm"
- "Commutativity of addition guarantees that ... bank members will agree on the same bank account balance."
- "This scheme needs O(N^2) messages to be transmitted at the end of each epoch"
- "P(X > 32) = P(X > (1+4)6.4) < (e^4/5^5)^6.4 = 5.6 × 10^-12"
