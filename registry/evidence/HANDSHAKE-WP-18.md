## [HANDSHAKE-WP-18] Handshake: A Decentralized, Permissionless Naming Protocol Compatible with the Domain Name System
**Citation:** Handshake project (collective; whitepaper unattributed to named individuals in the retrieved copy). "Handshake: A Decentralized, Permissionless Naming Protocol Compatible with the Domain Name System." Project whitepaper (not peer-reviewed), 2018.
**Retrieved:** full text via https://handshake.org/files/handshake.txt
**Source URL:** https://handshake.org/files/handshake.txt
**Domain:** E

### What it does
Handshake replaces the trusted-Certificate-Authority root of web security by giving each fully-qualified top-level name (TLD) a blockchain-recorded owner and an associated certificate, so a client can check a name-to-certificate binding against chain state instead of trusting one of a fixed set of Certificate Authorities. The scope is narrower than Namecoin's whole-namespace ledger: Handshake secures only the root-zone level (the TLD), and delegates everything below a TLD to existing DNS infrastructure operated by that TLD's owner. A miner-run proof-of-work chain orders registration events, so a name claimed earlier is provably prior to a later, conflicting claim by a different party. Because an infinite number of short, desirable strings could otherwise be registered for free by one party, the chain requires the coin native to it as a scarcity input: a party places a coin-denominated bid to acquire a name, and the whitepaper states the bid amount is permanently destroyed from the circulating supply rather than transferred to a seller, so registering a name has a real resource cost enforced by supply reduction. Verification without running a full copy of the chain (Simplified Payment Verification, SPV) depends on an authenticated data structure the whitepaper calls the Flat-File Merkle Tree (FFMT): a base-2 Merkle trie stored directly in append-only flat files rather than layered on a general-purpose database, from which a full node emits compact Merkle inclusion or exclusion proofs for a given name. Existing TLD holders (Verisign for .com/.net, PIR for .org, Afilias, ICANN, Namecoin, Keybase, and others named in the text) are allocated a share of the initial coin supply redeemable by submitting a Domain Name System Security Extensions (DNSSEC) proof of control over the corresponding legacy TLD, and an SPV client falls back to a hardcoded or dynamically queried ICANN root zonefile for any TLD not yet claimed on the Handshake chain.

### Measured results
The whitepaper presents implementation benchmarks of its own authenticated data structure; because this document is a project whitepaper and not independently peer-reviewed, every figure below is recorded as project-stated design intent per the registry classification for this key, not as an independently verified measurement.

| Project-stated figure | Conditions given in the text |
|---|---|
| FFMT insertion over 50x faster than Ethereum's base-16 Patricia trie; over 500x faster than Google's Sparse Merkle Tree (used in Certificate Transparency) | Comparison is the project's own benchmark of its "initial FFMT implementation" against the two named alternative structures; no shared hardware, dataset, or run count stated for the two baselines |
| FFMT proof size comparable to a compressed Sparse Merkle Tree proof, and roughly 4x smaller than a base-16 trie proof | Same benchmark context as above; "comparable" and the 4x figure are not accompanied by absolute byte sizes |
| Sparse Merkle Tree insertion required at least 1.2 million rounds of hashing for a typical batch of 5,000 leaves | Stated as the project's own benchmark of the Google Sparse Merkle Tree baseline, without heavy caching |
| 500-leaf FFMT insertion batches averaged roughly 100-150 ms near peak capacity; committing (fsync) a batch of 44,000 accumulated leaf values averaged 400-600 ms | Benchmark run on one consumer laptop: Intel Core i7-7500U at 2.70 GHz with an NVMe PCIe SSD; total benchmark inserted 50,000,000 leaves of 300 bytes each in batches of 500, with periodic commits of 44,000 values; no run count or variance given |
| Alternative data structures examined and rejected: "many" unnamed structures had proof sizes "frequently exceeding 1-3 kilobytes" | No structures are individually cited for this figure beyond the two named comparisons (Ethereum trie, Google Sparse Merkle Tree) |

### Parameters
- Block interval: 5 minutes, stated as the target the FFMT's measured commit times (400-600 ms for 44,000 leaves) must fit inside.
- Per-block tree-update cap: a maximum of 600 tree updates per block, stated as an added fail-safe bound giving predictable worst-case insertion cost.
- Proof-of-work function: Hashcash-derived, combining SHA3 and BLAKE2b; the whitepaper states this combination is chosen because SHA3 is under-represented in existing proof-of-work hardware, to reduce the advantage of hardware built for other chains.
- Coin allocation to the free and open source software community: approximately 70% of total initial coin supply (stated once as "around 70%" and elsewhere itemized to 68.0%).
- Coin allocation to legacy naming-infrastructure stakeholders redeemable via DNSSEC proof: ICANN 24,480,000 coins; Namecoin 10,200,000 coins; PIR (.org) 3,400,000 coins; Afilias 3,400,000 coins; Verisign (.com/.net) 6,800,000 coins; Keybase, Inc. 0.25% of total supply; Handshake reserved-names pool (over 80,000 names) 2.5% of total supply; TLD holders generally 2.5% of total supply, distributed evenly.
- Initial coin valuation stated in the text: 7.5% of total supply valued at $136,000,000 in the initial distribution round described.

### Stated limitations
The whitepaper's own Disclaimers section states no guarantee is provided for the naming and auction system's functionality, including renewal availability, fees, or block availability in general, and no guarantee of coin supply, coin value, or name value. It states that transaction formats are not guaranteed to remain valid past one year, and that pre-signed transactions should not be presumed permanently valid. Trademark holders, not the protocol, are stated to be responsible for managing their own renewals and registrations. The chain's own root-zone security is stated to depend on the proof-of-work function, and the document states the resulting protocol is "not usable in practice without proper SPV proofs," meaning the raw consensus construction alone is stated as insufficient without the compact-proof mechanism described. The text states that specialized proof-of-work hardware can produce hardware monopolies, calling this "an acceptable risk" without a quantified bound. It states that no known proof-of-stake system was, at time of writing, sufficiently decentralized and resilient to fraudulent SPV proofs to serve as a substitute for proof-of-work in this design. The document opens by stating it is "not a prescriptive document" describing "the approach," rather than a specification.

### Requirements it places on the rest of the system
A client that wants root-zone security without a full copy of the chain needs an SPV resolver capable of verifying FFMT inclusion and exclusion proofs; the whitepaper states the protocol is unusable without this. For every TLD not yet claimed by its legacy holder, an SPV client is stated to require either a hardcoded ICANN root zonefile snapshot or a live query path to ICANN's own root servers as fallback, so a Handshake-only client cannot resolve unclaimed legacy TLDs without also trusting one of those two ICANN-derived sources. Legacy TLD holders reclaiming a name on Handshake are stated to need a valid DNSSEC proof chain rooted in the two IANA-controlled root Key Signing Keys, so the mechanism inherits a dependency on IANA's DNSSEC root operations for that one-time claim step, even though ordinary Handshake-chain operation afterward does not require it. Sybil resistance for name registration depends on the native coin's bid-and-destroy auction, so any component that lets a party register a name without a coin-denominated, destroyed bid removes the scarcity mechanism the whitepaper states is necessary to prevent single-party namespace monopolization.

### Contradicts
None found within this corpus batch. Retrieved via the project's own site rather than an independent archive; the retrieval note in the target registry classifies every number in this entry as project-stated, not independently measured, and this entry preserves that qualifier throughout.

### References worth retrieving
- foundational: Satoshi Nakamoto, "Bitcoin: A peer-to-peer electronic cash system" — underlying UTXO and proof-of-work construction Handshake extends.
- competing: Blockstack whitepaper (blockstack.org/whitepaper.pdf) — a full-namespace blockchain-secured naming system the text discusses and contrasts on SPV name verification (the "SNV" protocol).
- competing: Ethereum Yellow Paper (ethereum.github.io/yellowpaper) and Ethereum Name Service documentation (ens.domains) — the base-16 Merkle Patricia trie the FFMT benchmark is compared against, and a competing name-binding system on a general-purpose chain.
- competing: Google Trillian / Certificate Transparency Sparse Merkle Tree (github.com/google/trillian; IACR ePrint 2016/683) — the second data structure the FFMT benchmark is compared against.
- attack/critique: OpenNIC FAQ (wiki.opennic.org) — cited as prior work on an alternative DNS root zone, contrasted for its reliance on a still-centralized root operator.
- foundational: William Vickrey, auction-theory paper cited as [vickrey] (jstor.org/stable/2977633) — theoretical basis for the auction mechanism's incentive design.
- foundational: MES16 covenants paper, Financial Cryptography 2016 (fc16.ifca.ai/bitcoin/papers/MES16.pdf) — the covenant construction the naming-transaction state machine is built on.
- attack/critique: "Shattered" SHA-1 collision demonstration (shattered.io) — cited in the context of choosing hash functions for the proof-of-work and Merkle structure.

### Verbatim extracts
- "Users use the native token (coin) to register TLDs which are pinned to a specific certificate as the identity."
- "When a name is auction and sold, the coins are permanently destroyed from the system."
- "A Hashcash proof-of-work function using SHA3 and blake2b is used."
- "resulted in over a 50x speedup over Ethereum's Base-16 Trie and over a 500x speedup"
- "A typical insertion of 5,000 leaves required at least 1.2 million rounds of hashing"
- "the 500-value insertions themselves averaged roughly 100-150ms"
- "No guarantees are provided for transaction formats past one year."
- "no guarantees are provided with regards to functionality of the naming and auction system"
