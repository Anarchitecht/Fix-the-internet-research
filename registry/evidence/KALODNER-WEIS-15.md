## [KALODNER-WEIS-15] An Empirical Study of Namecoin and Lessons for Decentralized Namespace Design
**Citation:** Harry A. Kalodner, Miles Carlsten, Paul Ellenbogen, Joseph Bonneau, Arvind Narayanan. "An Empirical Study of Namecoin and Lessons for Decentralized Namespace Design." Workshop on the Economics of Information Security (WEIS), 2015.
**Retrieved:** full text via https://www.econinfosec.org/archive/weis2015/papers/WEIS_2015_kalodner.pdf
**Source URL:** https://www.econinfosec.org/archive/weis2015/papers/WEIS_2015_kalodner.pdf
**Domain:** E

### What it does
Namecoin gives a blockchain-secured directory that maps arbitrary user-chosen names to values, satisfying decentralization, security, and human-readable names at once (the three properties jointly conjectured impossible before Bitcoin, called Zooko's triangle). A miner majority weighted by computing power runs the same consensus protocol as Bitcoin over a forked chain, so every participant reads the same name-to-value mapping without a central directory operator. Registration uses three chain-recorded operations. NAME_NEW posts a hash commitment of the desired name from a controlled address, hiding the plaintext name so no other party can observe and register it first. After 12 or more confirmed blocks, NAME_FIRSTUPDATE reveals the name and nonce and attaches the first value; a block-chain validator checks the nonce and name hash against the earlier commitment. NAME_UPDATE, taking a prior NAME_FIRSTUPDATE or NAME_UPDATE output as input, serves three purposes depending only on where the transaction sends its output: sending to the same address with an unchanged value renews the name, sending to the same address with a new value updates the record, and sending to a different address transfers control. Ownership of a name is bound to control of the private key of a special coin (0.01 NMC in this design), so transferring the name and transferring a payment can be combined in one atomic transaction with three outputs: name plus payment to the seller, and change back to the buyer, so that either both legs settle or neither does. Names lapse if not renewed within a fixed window; a lapsed name returns to the pool available to any new NAME_NEW claim.

### Measured results
| Measurement | Value | Conditions |
|---|---|---|
| Registered .bit names, snapshot | ~120,000 (196,023 active names counted separately in the value-uniqueness pass; 119,624 counted in the resolution pass) | Namecoin block chain as crawled at time of writing (2015); two separate counting passes in the paper use slightly different name-activity filters |
| Fraction squatted | at least 76% of .bit domains | Names whose value string occurs 10 or more times across the chain are classified as squatted; 34,361 unique values found among 196,023 active names |
| Domains resolving to any IP/hostname | 9,354 of 119,624 .bit domains | Only names carrying a JSON value with a DNS-style record are counted as resolving |
| Domains serving real, non-duplicate, non-squatter content | 745 -> 455 (dedup) -> 278 (non-error) -> 222 (>=15 words) -> 28 (unique, not mirroring an ICANN-TLD site) | Funnel from the 9,354 resolving domains: HTTP GET on port 80 to the front page only, 5,374 responsive; 4,629 of the 5,374 owned by 3 squatters and removed first |
| Lower bound on secondary-market transfers (atomic) | 14 transactions total (6 detected by the three-output heuristic, of which 5 overlapped with an independent implementation-quirk heuristic that separately found the same 14) | Full transaction history of the Namecoin chain to date of writing; atomic transfer defined as a single transaction moving both a name and its associated payment |
| Upper bound on squatter-to-regular-user transfers | approximately 250 transactions, stable across the tested range | Squatter threshold n swept from 5 to 25 (a value counted as squatted if it recurs n or more times); transfer counted only where a name's value moves from a squatter-associated value to a non-squatter value and an info/email field does not merely persist unchanged |
| Registration availability by name length | 1-character: 100% taken; 2-character: 100% taken; 3-character: 58.61% taken; 4-character: 1.00% taken; 5-character: 0.02% taken | Combinatorial universe of all possible names of each length computed from the Namecoin domain-name specification (bibliography entry [7]); percentage is share of that combinatorial universe already registered |
| Expiration window | 12,000 blocks originally, raised by hard fork in March 2012 to 36,000 blocks (~250 days) | Applies chain-wide; a name unmentioned in any NAME_FIRSTUPDATE/NAME_UPDATE for 36,000 blocks returns to the available pool |
| Merged-mining hash power | Namecoin holds approximately one-third of Bitcoin's hash rate, including merge-miners | Measured against Bitcoin's contemporaneous hash rate at time of writing; stated as providing resilience to a 51% attack while noting a sufficiently large Bitcoin mining pool could still carry it out |

### Parameters
- NAME_NEW confirmation wait before NAME_FIRSTUPDATE: 12 or more blocks, to let the commitment reach chain consensus before reveal.
- Special name-holding coin value: 0.01 NMC, unspendable as ordinary currency while attached to a name.
- Per-transaction fee (at time of writing): 0.005 NMC, set in client software.
- Historical network fee on NAME_FIRSTUPDATE: nonzero originally, decayed to a value that rounds to 0 by block 85,585; the paper states this was designed to deter early bulk registration while making later registration cheap.
- Expiration window: 12,000 blocks (original) then 36,000 blocks (~250 days) after a March 2012 hard fork.
- Squatting-detection threshold used for the headline figure: value recurs 10 or more times (paper states no definitive threshold exists and sweeps 5-25 for the transfer-upper-bound figure).
- Content-inclusion threshold for "real content": page carries 15 or more words, after removing duplicate mirrors and error/default pages.

### Stated limitations
The domain-content survey queried only the front page of each domain over port 80/HTTP; sites resolving only on subdomains or only over HTTPS are excluded, and content reachable only through in-page links is not counted, so the 28-domain figure is a lower bound on non-trivial unique content by the authors' own statement. Detecting non-atomic name transfers in general is stated as not possible with the available chain data, because Namecoin's client sends updated names to a new address by default, making an ordinary value update indistinguishable on-chain from a change of owner; only the squatter-to-non-squatter subclass is detectable, and that bound is explicitly conservative (an upper bound, not a count). The paper states its economic-mechanism analysis assumes a "decentralized algorithmic agent" capable of running pricing and buy-back logic without addressing the practical feasibility of implementing such an agent. Losing the private key controlling a name loses that name irrecoverably; the paper treats this as a structural cost of any ownership-based (non-expiring) naming scheme, distinct from Namecoin's actual fixed-expiration design.

### Requirements it places on the rest of the system
A consuming application needs continuous access to a synchronized copy of the Namecoin block chain to resolve a name, because the mapping lives only in chain state, not on any server the application can query directly. Renewal is a proof obligation on the holder: a name goes back to the available pool automatically after 36,000 blocks (~250 days) without an on-chain NAME_UPDATE citing a still-valid prior UPDATE/FIRSTUPDATE, so any naming layer building on this mechanism needs its own reminder or automated-renewal process external to the chain protocol, since the protocol supplies none. Front-running resistance during registration depends specifically on the two-phase commit-then-reveal design (NAME_NEW then NAME_FIRSTUPDATE): a system that lets a value be observed and copied before commitment is confirmed reopens front-running, which the paper states is exploitable by any node observing the peer-to-peer network before a commitment is bound to a signing address. Atomic name-for-payment exchange depends on both the name and the payment being representable as inputs/outputs of the same underlying transaction format (as Namecoin's Bitcoin-derived script does); a naming system whose payment rail is a separate ledger cannot reproduce this specific mechanism without a cross-chain atomic-exchange protocol.

### Contradicts
None found within this corpus batch.

### References worth retrieving
- foundational: Satoshi Nakamoto, "Bitcoin: A peer-to-peer electronic cash system" (bitcoin.org/bitcoin.pdf) — underlying consensus and transaction-script mechanism Namecoin forks.
- foundational: "Domain name specification," Namecoin wiki, 2015 — defines the combinatorial name universe used for the length-availability table.
- competing: J. Bonneau, J. Clark, E. Felten, J. Kroll, A. Miller, A. Narayanan, "On decentralizing prediction markets and order books," WEIS 2014 — cited as prior evidence that decentralized algorithmic agents can implement complex market logic; relevant comparison for any algorithmic-pricing primary market.
- attack/critique: Wikipedia, "Domain name front running" — cited as evidence front-running is already a live problem in conventional DNS registrar services, motivating the commit-reveal design.
- foundational: Roger Dingledine, Nick Mathewson, Paul Syverson, "Tor: The second-generation onion router," 2004 — cited for the .onion resolution target type observed in .bit domain records.

### Verbatim extracts
- "among Namecoin's roughly 120,000 registered domain names, a mere 28 are not squatted and have non-trivial content."
- "Of the 196023 currently active names, there are only 34361 unique values."
- "it appears safe to say that at least 76% of .bit domains are held by squatters."
- "we found 6 transactions fitting this form. However 5 of the 6 were also detected"
- "the total number of squatter→ non-squatter transactions detected holds at approximately 250 transactions."
- "the expiration period was increased to 36,000 blocks (which comes out to about 250 days)."
- "Namecoin has approximately one third the hash rate of Bitcoin."
