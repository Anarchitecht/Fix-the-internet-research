## [STEINER-CCR-07] Exploiting KAD: Possible Uses and Misuses

**Citation:** Moritz Steiner, Taoufik En-Najjary, Ernst W. Biersack. "Exploiting KAD: Possible Uses and Misuses." ACM SIGCOMM Computer Communication Review, 2007. DOI 10.1145/1290168.1290176.
**Retrieved:** full text via http://www.moritzsteiner.de/papers/ExploitingKAD.pdf
**Source URL:** http://www.moritzsteiner.de/papers/ExploitingKAD.pdf
**Domain:** A+J

### What it does
The paper states and measures three attacks executed against the live, deployed KAD network — the Kademlia-based distributed hash table (DHT) protocol used by eMule, aMule, and formerly Overnet, with several million simultaneous users at the time of writing — each built from the same underlying Sybil attack (introducing many peer identities controlled by one entity, following Douceur's original definition of the Sybil attack as "the forging of multiple identities").

KAD identifies each node by a 128-bit Kad ID and routes by prefix matching: node A forwards a query for node B to whichever routing-table entry has the smallest bitwise exclusive-or (XOR) distance to B, iteratively, with three parallel routing lookups per query for churn robustness. A key is published redundantly on ten peers whose Kad ID agrees with the key in its first 8 bits (the "tolerance zone"), republished every 5 or 24 hours depending on content type; a search launches three parallel routing lookups toward the key.

Spying attack (Section 3.1): the authors' "spy" tool creates thousands of stateless Sybil identities on a single physical machine, crawls a target 8-bit zone of the Kad ID space to discover currently active peers, sends "hello" messages to those peers so the peers insert the Sybil identities into their own routing-table buckets ("poisoning" the tables), then answers subsequent route requests destined for that zone with further Sybil identities so the requester's routing lookup is steered entirely through Sybils; the follow-up publish or search request from the victim then also lands on a Sybil, and its content is logged.

Eclipsing attack (Section 3.2): to make a specific keyword K unfindable by anyone using KAD's search algorithm (though the underlying content remains stored, unreachable, on the original regular peers), the authors position a small number of Sybil identities with Kad IDs closer to K's hash than any real peer's, then poison regular peers' routing tables the same way as the spying attack, so every search request for K terminates on a Sybil, which simply drops it instead of answering.

DDOS-enlistment attack (Section 3.3): identical Sybil placement to the eclipse attack, except each Sybil, instead of dropping the intercepted search request, replies with the IP address of a third-party "target" host, causing the querying peer to contact that target — enlisting ordinary KAD peers as an amplification/reflection mechanism against a machine they were never trying to reach.

### Measured results

| Attack | Conditions | Result |
|---|---|---|
| Full-network crawl speed | Authors' own breadth-first crawler, issuing route requests, run over "the last 18 months" of study | Full Kad-ID-space crawl completed in about 8 minutes; found between 3 and 4.3 million distinct peers per full crawl, of which 1.5 to 2 million were directly reachable (not behind NAT/firewall) |
| Zone crawl speed | 8-bit zone (1/256th of the full Kad ID space) | Under 2.5 seconds per zone crawl; the same zone was crawled every 5 minutes for slightly less than 6 months |
| Spying attack, traffic volume | Spy tool running 2^16 (65,536) Sybil identities in one 8-bit zone, on a single physical machine, for one day | Observed 1.4 million distinct files published, 42,000 distinct keyword hashes, 1.5 million distinct users; approximately 1,000 search requests, 10,000 publish requests, and 25,000 route requests per minute reaching the Sybils; approximately 400 KB/sec incoming and 200 KB/sec outgoing traffic load on the spying machine |
| Publish vs. search traffic ratio | Same spying-attack measurement | Publish traffic exceeds search traffic by one order of magnitude in message count and two orders of magnitude in total bytes transmitted |
| Eclipsing attack, minimum Sybil count | Live KAD network | As few as 8 Sybil identities positioned around a keyword's hash were sufficient to make all search requests for that keyword terminate on a Sybil |
| Eclipsing attack, resource cost by keyword popularity | 32 Sybils running on one physical machine, eclipsing two specific keywords, "the" (popular) and "dreirad" (German for "tricycle," less popular) | For "the": 41,801 route messages/min, 1,091 hello messages/min, 12,360 publish messages/min, 704 search messages/min, 186 KB/sec total incoming bandwidth. For "dreirad": 818 route messages/min, 433 hello messages/min, 290 publish messages/min, 49 search messages/min, 32 KB/sec total incoming bandwidth |
| DDOS-enlistment attack | Attack directed by the authors against their own machines, using KAD peers redirected by Sybils | Incoming traffic on the order of several Mbit/sec observed on the targeted machines; no fixed Sybil count or duration stated for this specific run |
| Independently reported real-world DDOS scale | Cited third-party report (Prolexic, May 2007), not measured by the authors | More than 300,000 peers observed participating in a peer-to-peer-based DDOS attack in the wild |

### Parameters
- Kad ID length: 128 bits.
- Publish redundancy: 10 peers per key, selected by 8-bit prefix agreement with the key (the "tolerance zone"), not by strict numeric closeness.
- Republish interval: 5 or 24 hours, depending on content type.
- Parallel routing lookups per query: 3 (both publish and search use this).
- Spying-attack zone size used in the reported measurement: 8-bit zone (yielding 2^16 = 65,536 Sybil identities placed).
- Eclipsing-attack Sybil count: as low as 8 sufficient in principle; 32 used in the reported resource-consumption measurement (Table 1).
- Crawl frequency for the 6-month zone study: every 5 minutes.

### Stated limitations
The paper states its proposed defense — a centralized agent binding each Kad ID to a cell-phone number via SMS verification, or alternatively a CAPTCHA-based Reverse Turing Test — cannot prevent a peer from giving away or having stolen a validly obtained Kad ID, and requires re-issuing a new Kad ID whenever the peer's IP address changes, since IP address is bound into the encrypted ID. It states the scheme cannot prevent a well-resourced attacker from obtaining multiple valid Kad IDs by controlling multiple phone numbers or solving multiple CAPTCHAs, and states plainly that it will never be possible to prevent an attacker with sufficient resources from obtaining multiple Kad IDs. It states that, given KAD's scale (several million simultaneous peers), a disruptive attack would probably require an attacker to introduce thousands of Sybils, without deriving that count from a model or measurement, so this is a bound of the authors' judgment, not a derived figure. The paper explicitly states the article is an editorial note submitted to Computer Communication Review (CCR) and was not peer-reviewed.

### Requirements it places on the rest of the system
- The spying and eclipsing attacks both require the ability to have Sybil identities' presence inserted into victim peers' routing tables (via unsolicited "hello" messages accepted by KAD's own protocol); a routing-table admission policy that verifies a peer's identifier through means other than the peer's self-reported claim would remove this precondition.
- The eclipsing attack requires the victim's routing lookup to be steerable entirely through attacker-controlled nodes before it reaches any honest node; a lookup mechanism guaranteeing at least one disjoint, attacker-independent path (the property S/Kademlia's disjoint-path lookup targets, per the already-verified S/Kademlia entry) would change this precondition, though this paper does not measure disjoint-path lookup itself.
- The DDOS-enlistment attack requires ordinary KAD peers to accept and act on a search response's supplied IP address without independently verifying that the responding node is authoritative for the requested content; a verification step at the requesting peer (e.g., confirming the response against a second independent path) would remove the precondition this attack exploits.
- The paper's own proposed centralized-identity defense requires a trusted central agent (CA) to hold the CA's private key securely and to keep a list of (phone number, expiration) and (IP address, expiration) pairs, and requires every participating peer to know the CA's public key to verify Kad ID validity — reintroducing a single point of trust into an otherwise decentralized system, a value tradeoff the paper states but does not resolve.

### Contradicts
None found within this batch against other current entries. This paper's Table 1 and Section 3 findings are themselves a directly measured cost figure that BRIEF.md's registry `why_needed` field frames as a check against Sybil/eclipse cost claims made only in simulation elsewhere (e.g., Pitch Black, already verified per BRIEF.md section 7, which used a simulated/testbed adversary rather than a live-network Sybil deployment); no simulated figure from another entry in this batch directly measures the same live-network cost, so no direct numeric contradiction is recorded.

### References worth retrieving
- Attack/critique: N. Naoumov, K. Ross, "Exploiting p2p systems for ddos attacks," International Workshop on Peer-to-Peer Information Management, May 2006 — index-poisoning and routing-poisoning attack taxonomy for the related Overnet system, cited as directly relevant to KAD given their similar routing.
- Competing (Sybil defense): H. Rowaihy, W. Enck, P. McDaniel, T. La Porta, "Limiting sybil attacks in structured p2p networks," IEEE INFOCOM 2007 — hierarchical hash-puzzle admission-control defense, critiqued by this paper as still vulnerable to a resourceful attacker.
- Competing (Sybil defense): H. Yu, M. Kaminsky, P. B. Gibbons, A. Flaxman, "Sybilguard: Defending against sybil attacks via social networks," ACM SIGCOMM 2006 — social-graph-based Sybil defense, critiqued here as requiring a well-connected social network not present in deployed DHT-based p2p systems.
- Competing (eclipse defense): M. Castro, P. Druschel, A. Ganesh, A. Rowstron, D. Wallach, "Secure routing for structured peer-to-peer overlay networks," OSDI 2002 — Constrained Routing Tables defense, critiqued here as preventing proximity neighbor selection because it leaves no flexibility in neighbor choice.
- Attack/critique: A. Singh, M. Castro, P. Druschel, A. Rowstron, "Defending against eclipse attacks on overlay networks," ACM SIGOPS 2004 — the workshop-length predecessor paper; note this is the paper mistakenly retrieved under key SINGH-INFOCOM-06 in this batch (see that key's mismatch record).
- Foundational: A. Singh et al., "Eclipse attacks on overlay networks: Threats and defenses," Proc. INFOCOM 2006 — cited here by exact venue/year, confirming the correct citation for the SINGH-INFOCOM-06 target that this batch's retrieval fetched the wrong document for.
- Foundational: J. R. Douceur, "The Sybil attack," IPTPS 2002 — origin of the Sybil-attack concept this entire paper builds on.
- Foundational (measurement): D. Stutzbach, R. Rejaie, "Improving lookup performance over a widely-deployed DHT," INFOCOM 2006 — cited for KAD implementation detail; a churn/lookup-performance measurement paper on the same live network.
- Companion measurement paper: M. Steiner, T. En-Najjary, E. W. Biersack, "A Global View of KAD," IMC 2007 — cited as [26], the companion crawl-measurement paper sharing this paper's crawl infrastructure (this is the STEINER-IMC-07 key noted adjacent to this one in the registry).
- Competing (load reduction): M. Steiner, W. Effelsberg, T. En-Najjary, E. W. Biersack, "Load reduction in the kad peer-to-peer system," DBISP2P 2007 — cited as the source of the improved publish scheme reducing publish traffic by one order of magnitude, referenced but not itself measured in this paper.

### Verbatim extracts
- "the sybils allow to gain control over a fraction of the peer-to-peer network or even over the whole network"
- "as few as eight sybil peers are sufficient to make sure that all search requests for K will terminate on one of the sybils"
- "publish traffic... is one order of magnitude larger... and two orders of magnitude larger... in terms of the total number of bytes"
- "we found between 3 and 4.3 million different peers"
- "it will never possible to prevent an attacker with a lot of resources from obtaining multiple (random) Kad IDs"
- "an attacker will probably need to introduce thousands of sybils in order to disturb the system"
