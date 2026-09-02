## [JANSEN-HOTPETS-14] From Onions to Shallots: Rewarding Tor Relays with TEARS
**Citation:** Rob Jansen, Andrew Miller, Paul Syverson, Bryan Ford. "From Onions to Shallots: Rewarding Tor Relays with TEARS." Workshop on Hot Topics in Privacy Enhancing Technologies (HotPETs), 2014. DOI: not recorded in registry.
**Retrieved:** full text via https://www.robgjansen.com/publications/tears-hotpets2014.pdf
**Source URL:** https://www.robgjansen.com/publications/tears-hotpets2014.pdf
**Domain:** I

### What it does
TEARS (the paper does not expand this as an acronym; the name plays on "onions") rewards relay operators in the Tor anonymous-communication network with traffic priority in exchange for contributed bandwidth, without a central bank holding user balances. A distributed audit process measures each relay's bandwidth contribution and reports it to a bank; the bank mints tokens called Shallots and deposits them to the relay's account in proportion to the measured contribution. A user (relay or ordinary client who acquired Shallots) redeems Shallots at the bank for a relay-specific PriorityPass, using a blind-signature construction so the bank cannot learn which relay the pass is bound to. The user presents the PriorityPass directly to that relay, in a single onion-wrapped private message, to obtain temporary priority in the relay's traffic scheduler. Because each PriorityPass is bound to one relay identity and is marked spent immediately, the relay checks and rejects double-spending locally, with no further bank communication after the pass is issued — this is what prevents the withdrawal/deposit timing pattern from leaking which relay a client is using. Shallots themselves are transferable between user accounts, letting a market form independent of the bandwidth-audit process. The bank is a quorum of semi-trusted servers (envisioned as the existing Tor directory servers) running a Byzantine Paxos-family agreement protocol to order transactions and a publicly verifiable e-cash protocol (drawing on Sander-Ta-Shma auditable e-cash and Zerocoin) so that any minority-server misbehavior is prevented and any majority-server misbehavior is at least publicly detectable from the published transaction transcript. Traffic prioritization uses a Proportionally Differentiated Services circuit scheduler, the same scheduling approach used in the BRAIDS and LIRA schemes the paper compares against.

### Measured results
None. The paper is a design proposal with no implementation and no experimental evaluation. It explicitly lists building an implementation, a scalability analysis as relay count and banking-authority count grow, and Shadow-simulator experiments as future work, none of which the paper itself performs.

### Parameters
No numeric parameters are fixed by the paper. The paper states these are open policy choices, deferred to a deployment decision: the fraction of each minted Shallot allocated to Tor Project administrators as a transaction fee, whether Shallots expire after a fixed interval, and the schedule for periodic publication of received PriorityPasses (the paper suggests "for example, once a month" as an illustrative interval, not a chosen value).

### Stated limitations
The paper states that securely auditing relay bandwidth contributions is an open research problem, and that it does not believe any existing bandwidth-measurement design (citing EigenSpeed) is suitable for TEARS. The bandwidth-audit mechanism itself is out of scope for the paper. Proving that a relay actually granted priority to a presented PriorityPass, and that it did not alter network-set scheduling parameters, is stated as an unsolved problem. The cryptographic construction of the blind-signature PriorityPass is stated as out of scope. The paper states that no system or efficiency analysis has been performed to confirm the claimed properties hold as the number of relays and banking authorities scales. The paper states a general social risk, attributed to Benkler's argument about paid versus volunteer participation, that introducing an explicit incentive can reduce intrinsically motivated volunteer contribution — presented as a risk the authors flag, not a measured effect.

### Requirements it places on the rest of the system
Requires a separate, unspecified secure bandwidth-auditing subsystem that reports per-relay contribution to the bank; the paper does not supply this component. Requires a Byzantine-fault-tolerant agreement protocol (the paper cites Fast Paxos) among a quorum of semi-trusted bank servers to order transactions, plus a threshold-signature scheme (cited: Pedersen; Boldyreva) so a majority of servers can jointly sign a batch. Requires an auditable/publicly-verifiable e-cash primitive (cited: Sander-Ta-Shma; Zerocoin) supporting non-interactive zero-knowledge proofs of unspent-coin possession. Requires that users communicate with the bank only through an anonymizing relay (Tor itself), so that withdrawal and redemption traffic does not itself deanonymize the requester. Requires a circuit scheduler at each relay capable of proportional differentiated service between PriorityPass and ordinary traffic. Requires that PriorityPass presentation happen in a single message with no subsequent bank round trip, which in turn requires the blind-signature construction to bind a pass to one relay identity before it leaves the bank.

### Contradicts
None found. No other paper in this batch measures TEARS or Shallots.

### References worth retrieving
- Ghosh, Richardson, Ford, Jansen, "A TorPath to TorCoin: Proof-of-bandwidth altcoins for compensating relays," HotPETs 2014 — competing: peer-measured circuit-goodput currency, the direct trust-model contrast to TEARS's audited/bank model.
- Jansen, Hopper, Kim, "Recruiting new Tor relays with BRAIDS," CCS 2010 — foundational/competing: prior ticket-based incentive scheme TEARS compares its double-spend and overhead properties against.
- Jansen, Johnson, Syverson, "LIRA: Lightweight Incentivized Routing for Anonymity," NDSS 2013 — competing: prior lottery-based incentive scheme, direct efficiency comparison target.
- Miers, Garman, Green, Rubin, "Zerocoin: Anonymous distributed e-cash from bitcoin," IEEE S&P 2013 — foundational: the anonymous e-cash construction TEARS's bank protocol draws on.
- Snader, Borisov, "EigenSpeed: secure peer-to-peer bandwidth evaluation," IPTPS 2009 — attack/critique target: TEARS's own text lists EigenSpeed's failure modes (ignores asymmetric bandwidth, opportunistic-measurement underestimation, unclear Sybil handling) as reasons it is unsuitable.
- Johnson, Jansen, Syverson, "Onions for sale: Putting privacy on the market," FC 2013 — competing: direct-payment-for-Tor-service proposal, an alternative incentive philosophy TEARS's Appendix E discusses.
- Chen, Sion, Carbunar, "XPay: Practical anonymous payments for Tor routing and other networked services," WPES 2009 — competing: an earlier payment-for-relay scheme TEARS's introduction cites among trade-offs on double-spend detection speed versus information leakage.

### Verbatim extracts
"rewards relays for providing useful service to the network"
"PriorityPasses are locally verifiable, have non-transferable value"
"measuring relay bandwidth securely is an open research problem"
"It is unclear how to handle sybil attacks by malicious collectives" (re: EigenSpeed)
"an efficiency analysis should be done to determine the scalability"
