## [BIRYUKOV-SP-13] Trawling for Tor Hidden Services: Detection, Measurement, Deanonymization

**Citation:** Alex Biryukov, Ivan Pustogarov, Ralf-Philipp Weinmann. "Trawling for Tor Hidden Services: Detection, Measurement, Deanonymization." IEEE Symposium on Security and Privacy, 2013. DOI 10.1109/SP.2013.15.
**Retrieved:** full text via https://www.cryptolux.org/images/2/25/Tor-HS-deanonymization.pdf
**Source URL:** https://www.cryptolux.org/images/2/25/Tor-HS-deanonymization.pdf
**Domain:** J

### What it does
The paper demonstrates three attacks against Tor hidden services (a Tor hidden service publishes a rendezvous descriptor to a small set of relays instead of a public IP address, so a client reaches it only through the Tor network). First, an attacker computes future rendezvous-descriptor identifiers and precomputes relay key pairs whose fingerprints land immediately after those identifiers on the fingerprint ring Tor uses to assign descriptor storage, then runs relays with those keys so the attacker's own relays become the hidden service's descriptor-storage points (hidden service directories, HSDirs). Injecting the relays into every second gap of the ring lets the attacker capture every descriptor published network-wide. Second, controlling a hidden service's rendezvous descriptor storage or its guard node lets the attacker count descriptor fetch requests, which the paper uses as a proxy for the number of distinct clients that used the hidden service in the counted period. Third, an attacker who additionally controls a Tor relay acting as a hidden service's entry guard (the fixed first hop of every circuit the hidden service builds) forces the hidden service to open a rendezvous circuit to an attacker-controlled rendezvous point; the rendezvous point sends a distinctive count of relay cells (50 padding cells) back down the circuit, and the guard node recognizes the resulting cell-count and timing signature on any circuit passing through it, which identifies the immediately preceding relay as the hidden service's own entry point and, when the guard is one hop from the hidden service's own machine, reveals its IP address directly.

### Measured results
| Result | Conditions |
|---|---|
| 59,130 descriptor publication requests, 58,389 descriptors fetched, 24,703 with unique public keys, ~1.5% encrypted | 50 Amazon EC2 instances running 1,200 Tor relay processes (24 relays per instance) for 25 hours, November 2012 |
| ~3% of hidden descriptors estimated missed | Verified against a 120-hidden-service sample from public sources; 4 relays from the sample were absent from the harvested set |
| 39,824 unique onion addresses collected, cost reduced to USD 57 | Second harvesting run, 58 EC2 micro instances, relays set to 0-1 Bytes/sec reported bandwidth to avoid attracting client traffic unrelated to the attack |
| Estimated botnet size 12,000-30,000 infected machines | Derived from descriptor-fetch counts of 1,408-4,977 requests/day for one hidden service (command-and-control channel), 13-29 July, capped at one fetch per 24 hours per machine because Tor caches descriptors for 24 hours |
| Silk Road: 15,185-19,284 descriptor requests/day; DuckDuckGo: 502-549 requests/day | Four consecutive days, 9-12 November 2012, measured by controlling one of each service's three responsible HSDir relays |
| Average gap between consecutive HSDir fingerprints on the ring: 10^44.8, minimum 10^42.16 | One randomly selected Tor consensus document, November 2012; finding a key fingerprint that falls in such a gap took a few minutes on a multi-core computer |
| Guard-identification attack: 8, 6, 5 correct identifications from ~36,000 rendezvous cells over 1h20m; second run: 5, 2, 1 correct identifications from ~16,000 rendezvous cells over 40 minutes | Two hidden services operated by the authors, attacker running one guard-adjacent (middle) relay and one rendezvous point |
| Cell-count traffic signature (3 cells up / 53 cells down) observed on 0 of 748,846 circuits examined | Circuits passing through one guard node the authors operated, used to establish the signature's false-positive rate |
| 90% probability of deanonymizing a long-running hidden service within 8 months, for EUR 8,280 (~USD 11,000) | Renting 23 relays of the EUR 45/month "EcoServer Large X5" class, each independently having ~0.6% average monthly probability of being chosen as one of a hidden service's three guards; combined chance per hidden service of 13.8% per guard-rotation attempt |

### Parameters
- Hidden service directory (HSDir) set size: 3 relays per descriptor replica, 2 replicas published, so 6 HSDirs total per hidden service.
- HSDir flag acquisition delay: 25 hours of consensus presence required before a relay is trusted as an HSDir.
- Consensus validity window: published hourly, fresh for 1 hour, valid for 3 hours total; clients fetch the next consensus in the interval (fresh-until + 45 min, valid-until − 10 min).
- Guard set size: 3 guards chosen initially; replaced only when fewer than 2 remain reachable; each guard's tenure is a random duration between 30 and 60 days.
- Maximum Tor relays per IP address admitted to the consensus: 2 (enforced by directory authorities; used in the attack by running additional "shadow" relays on the same IP that do not appear in the consensus until an active relay drops out).
- Attacker resource used for full-network descriptor harvesting: R = N / (12 × 2) IP addresses, where N is the number of HSDirs in the network (derived from the need to cover every second gap on the fingerprint ring, in two ring passes per day, with 2 relays per IP).

### Stated limitations
The paper's descriptor-count-based population estimates are approximate: multiple power cycles of one machine in a day overcount that machine, and the 24-hour descriptor cache means a machine that stays on for multiple days is undercounted. The authors state the guard-identification method proposed for encrypted introduction points cannot distinguish between hidden services once the full descriptor set for comparison is unavailable to the attacker. The authors state their proposed fixes are "nothing more than stop-gap measures" and that hidden services need a more complete redesign. The paper does not measure detection resistance of the attacker's own relays against countermeasures the Tor directory authorities might apply beyond the flag-assignment change already made in response to this work.

### Requirements it places on the rest of the system
Any rendezvous/directory design that assigns responsibility for storing a lookup record deterministically from a public identifier (a fingerprint ring keyed by a hash of the identifier, here) gives an adversary who can compute future identifiers the ability to precompute keys that land adjacent to that identifier and, by running relays with those keys, capture the storage role before the legitimate publisher does. Any capacity- or reputation-gated onboarding delay (the 25-hour HSDir-flag wait, here) bounds only the attacker's setup latency, not the number of identities the attacker can eventually operate, when the identity-creation cost itself is close to free (running a Tor relay process). A guard-node or fixed-entry-hop mechanism that keeps the same relay as a client's or service's first hop for weeks concentrates all of that period's deanonymization risk onto whichever party operates that one relay; the risk is proportional to the probability of an adversary being selected in the guard-selection weighting, which this paper measures directly for one bandwidth class.

### Contradicts
None found. No other paper in this batch measures Tor hidden-service directory assignment or guard-selection probability directly; JOHNSON-CCS-13 and SUN-USENIXSEC-15 measure Tor circuit compromise from different adversary positions (autonomous-system-level and relay-operator-level traffic correlation, and BGP-level routing manipulation) and do not overlap with this paper's descriptor-harvesting or guard-identification figures.

### References worth retrieving
- foundational: Dingledine, Mathewson, Syverson. "Tor: The second-generation onion router." USENIX Security Symposium, 2004.
- foundational: Øverlier, Syverson. "Locating hidden servers." IEEE S&P, 2006.
- competing/related: Elahi, Bauer, AlSabah, Dingledine, Goldberg. "Changing of the Guards: A framework for understanding and improving entry guard selection in Tor." WPES 2012. (already a target in this batch: ELAHI-WPES-12)
- attack: Bauer, McCoy, Grunwald, Kohno, Sicker. "Low-resource routing attacks against Tor." WPES 2007.
- attack: Murdoch. "Hot or not: Revealing hidden services by their clock skew." ACM CCS 2006.
- attack: Zander, Murdoch. "An improved clock-skew measurement technique for revealing hidden services." USENIX Security Symposium 2008.
- foundational: Douceur. "The Sybil attack." IPTPS 2002.

### Verbatim extracts
- "she can gain control over all the responsible HS directories... by injecting 6 Tor relays with precomputed public keys"
- "we could have lost about 3% of hidden descriptors"
- "None of the circuit exhibited the trafﬁc pattern of 3 cells up the circuit and 53 cells down the circuit"
- "the probability to deanonymize a long-running hidden service... is more than 90%, for a cost of... USD 11,000"
- "the above suggestions are nothing more than stop-gap measures"
