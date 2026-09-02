## [BENET-FILECOIN-17] Filecoin: A Decentralized Storage Network

**Citation:** Juan Benet, Nicola Greco. "Filecoin: A Decentralized Storage Network." Protocol Labs technical report, 2017.
**Retrieved:** full text via https://filecoin.io/filecoin.pdf
**Source URL:** https://filecoin.io/filecoin.pdf
**Domain:** C

### What it does

Filecoin matches clients who want data stored durably against storage providers ("miners") who offer disk space, and lets any third party verify without downloading the data that a provider is still holding what it agreed to store. The paper defines a decentralized storage network (DSN) scheme as a tuple of three protocols — Put (store), Get (retrieve), Manage (verify and repair) — and states three properties a DSN must have: public verifiability (anyone holding only the key, not the data, can check a storage proof), auditability (a durable record shows a provider held data for the agreed duration), and incentive-compatibility (a provider's best strategy is to store the data honestly).

The verification mechanism is two composed proof types. Proof-of-Replication (PoRep) lets a prover convince a verifier it holds `n` independent physical replicas of data `D`, not `n` copies of a pointer to one shared copy. The prover runs a Seal operation that computes a pseudo-random permutation of `D` keyed to the prover's own public key, so each replica is bound to one identity and cannot be shared between provers. Sealing is deliberately expensive: the paper states a Seal built from a chained AES-256 construction, calibrated so sealing takes 10 to 100 times longer than the challenge-response proving step, which stops a prover from generating a replica on demand in response to a challenge rather than storing it continuously. The prover then builds a Merkle tree over the sealed replica and answers random-leaf challenges with a Merkle path, proved succinct and non-interactive with a zk-SNARK (zero-knowledge succinct non-interactive argument of knowledge).

Proof-of-Spacetime (PoSt) extends a single PoRep check into a check that storage persisted across an interval. Instead of one challenge-response round per time unit, the prover chains `t` PoRep proofs sequentially, feeding each proof's output into the next proof's input, and recursively composes the chain into one short proof. Because each step depends on the previous step's output, a prover cannot compute the chain in parallel and cannot outrun the sequential computation, which is what stops a provider from fabricating a spacetime proof by parallelizing across many machines. In deployment the interactive verifier is replaced by randomness drawn from the blockchain, so any network participant can issue and check challenges without an operator maintaining a live challenge session.

Storage assignment and payment run through two markets. The Storage Market matches a client's bid against a miner's ask off-chain by gossip; when a deal forms, both parties sign a deal order and post it on-chain, the client's data moves to the miner directly, and the miner later posts PoRep at seal time and PoSt every `Δproof` epochs (a system-defined interval, left symbolic in this paper) to keep the deal valid. The Retrieval Market pays for delivery in small increments: a miner splits requested data into parts and releases each part only after receiving a micropayment for it over a payment channel, so a client cannot receive the full file without paying and a miner cannot collect full payment without delivering. The paper's proof-of-storage consensus, Expected Consensus, elects block-producing leaders with probability proportional to each miner's currently-proved storage ("power"), verified through the same PoSt already posted for storage deals, so the chain's leader-election mechanism reuses the storage proof rather than requiring separate proof-of-work or staked capital.

### Measured results

None. This is a protocol design and specification document; it contains no implementation benchmark, no simulation, and no deployment measurement. Section 8.1 ("On-going Work") lists "detailed performance estimates and benchmarks for Filecoin and its components" as future work not yet done at the time of writing, and states a full implementable specification and formal proofs of the consensus and self-healing properties were also not yet complete. Any sealing time, proof size, epoch length, or repair-bandwidth figure attributed to Filecoin must be traced to a different, later source — this paper defines the mechanisms but reports no run of them.

### Parameters

| Parameter | Definition in this paper | Value given |
|---|---|---|
| Sealing slowdown factor | ratio of Seal-operation time to challenge-prove-verify time | stated as 10-100x, not a single number, not derived from a measurement in this paper |
| `Δproof` | epochs between required PoSt submissions to the blockchain | left symbolic, "a system parameter," no numeric value given |
| `Δfault` | epochs of missing/invalid proofs tolerated before a deal is declared failed and re-listed | left symbolic, no numeric value given |
| Replica count `n` (PoRep) | number of independent physical copies a client requests | client-selectable per deal, no default stated |
| PoSt chain length `t` | number of sequential PoRep proofs composed into one Proof-of-Spacetime | client/protocol-selectable, no default stated |

### Stated limitations

The Seal function used for PoRep is explicitly flagged as suboptimal by its own authors: Section 8.2 lists as an open question finding "a better primitive for the Proof-of-Replication Seal function, which ideally is O(n) on decode (not O(nm))," meaning the deployed construction's decoding cost scales worse than linearly in replica count. The Prove function likewise still requires a zk-SNARK, and the paper flags a publicly verifiable, transparent (non-SNARK) alternative as unsolved. The zk-SNARK construction requires a trusted setup ceremony to generate its proving and verification keys; the paper notes this trust assumption and cites, without adopting outright, prior "Scalable Computational Integrity and Privacy" work as a possible route to remove it. The leader election scheme (Expected Consensus) is stated to produce, in expectation, exactly one leader per epoch, but "some epochs may have zero or many leaders" — multi-leader and empty epochs are an accepted property, not a bug, and no bound on their frequency is given in this paper. No performance estimate, benchmark, or full protocol specification existed at the time of writing (Section 8.1). No proof of correctness existed yet for Expected Consensus, for the asynchronous impossibility side-step claimed for Power Fault Tolerance, or for the self-healing repair guarantees (Section 8.3).

### Requirements it places on the rest of the system

Filecoin's PoRep/PoSt layer requires an underlying content-addressed storage and transfer layer beneath it: the paper states Filecoin "works as an incentive layer on top of IPFS," and Get/Put move the actual bytes outside the proof protocol. The consensus mechanism (Expected Consensus) requires a source of public, unpredictable per-epoch randomness drawn from the blockchain itself to issue non-interactive PoSt challenges; without that randomness source a miner could choose favorable challenges. Power accounting requires every full node to replay the chain from genesis and maintain an `AllocTable` of storage assignments, or, for a light client, requires a trusted source that relays block headers and Merkle inclusion proofs for the entries a light client wants to check — the light-client path is a weaker trust assumption than full replay, and the paper offers it as an explicit alternative rather than the default. The retrieval micropayment mechanism requires a payment channel primitive between client and miner (the paper cites Lightning and Sprites as the channel constructions it is built from) capable of releasing funds per delivered part. The Sybil-attack resistance PoRep claims to provide depends on the Seal function actually binding a replica to one prover's key; if sealing can be computed cheaply relative to the challenge-response window, the 10-100x slowdown assumption is violated and the anti-outsourcing property does not hold.

### Contradicts

None found within this corpus batch. This paper is a design specification with no measured claim to contradict or be contradicted by. Note for later cross-paper checking: the storage-overhead and repair-bandwidth comparisons attributed to "Filecoin" in secondary literature are not supported by this source, since this paper reports no such figures — any such comparison must be traced to a different, later Filecoin measurement paper.

### References worth retrieving

- Ateniese, Burns, Curtmola, Herring, Kissner, Peterson, Song, "Provable data possession at untrusted stores," ACM CCS 2007 — foundational (the PDP scheme PoRep is built to improve on)
- Juels, Kaliski, "PORs: Proofs of retrievability for large files," ACM CCS 2007 — foundational
- Shacham, Waters, "Compact proofs of retrievability," ASIACRYPT 2008 — foundational
- Protocol Labs, "Technical Report: Proof-of-Replication," 2017 — foundational (the formal PoRep definition this paper only sketches)
- Protocol Labs, "Technical Report: Power Fault Tolerance," 2017 — foundational (the Byzantine-fault reformulation the consensus section depends on)
- Protocol Labs, "Technical Report: Expected Consensus," 2017 — foundational
- Bentov, Lee, Mizrahi, Rosenfeld, "Proof of Activity," ACM SIGMETRICS PER 42(3), 2014 — competing (alternative proof-of-stake/proof-of-work hybrid leader election)
- Bentov, Pass, Shi, "Snow White: Provably secure proofs of stake," 2016 — competing
- Micali, "Algorand: The efficient and democratic ledger," arXiv:1607.01341, 2016 — competing
- Poon, Dryja, "The Bitcoin Lightning Network," 2015 — foundational (payment-channel construction the retrieval market cites)
- Miller, Bentov, Kumaresan, McCorry, "Sprites: Payment channels that go faster than Lightning," arXiv:1702.05812, 2017 — foundational

### Verbatim extracts

- "storage providers must convince their clients that they stored the data they were paid to store"
- "requires provers to store a pseudo-random permutation of D unique to their public key"
- "takes 10-100x longer than the honest challenge-prove-verify sequence"
- "recursively compose the executions to generate a short proof"
- "the probability that the network elects a miner ... is proportional to their storage currently in use"
- "detailed performance estimates and benchmarks for Filecoin and its components" [listed under ongoing/future work]
- "none of them have to be solved before launch" [regarding the open questions in 8.2]
