## [HASHIMOTO-CCS-22] How to Hide MetaData in MLS-Like Secure Group Messaging: Simple, Modular, and Post-Quantum
**Citation:** Keitaro Hashimoto, Shuichi Katsumata, Thomas Prest. "How to Hide MetaData in MLS-Like Secure Group Messaging: Simple, Modular, and Post-Quantum." ACM SIGSAC Conference on Computer and Communications Security (CCS), 2022. DOI 10.1145/3548606.3560679.
**Retrieved:** full text via https://doi.org/10.1145/3548606.3560679
**Source URL:** https://doi.org/10.1145/3548606.3560679
**Domain:** H

### What it does
The wrapper protocol W^mh upgrades a continuous group key agreement (CGKA) protocol that already hides message contents into one that additionally hides group membership metadata from the delivery server, without changing the underlying CGKA's mechanism for forward secrecy (FS) or post-compromise security (PCS). CGKA is the abstraction underlying MLS's TreeKEM (Messaging Layer Security's tree-structured key encapsulation mechanism): group members exchange proposal messages (add, remove, or update a member) and periodically issue a commit message that ratifies a set of pending proposals and advances the group to a new epoch with a fresh shared secret.

The paper separates what a delivery server can learn into three layers: layer 1 (group secret keys and message contents, already protected by standard CGKA), layer 2 (static, explicit metadata such as a sender's identity appearing in the clear inside a proposal or commit), and layer 3 (dynamic, implicit metadata inferable from which server-side records a party uploads or downloads, even over an anonymous transport). A CGKA is metadata-hiding, in this paper's terms, only when it hides all three layers.

W^mh's mechanism: every member of a CGKA group already holds a single group secret key that evolves each epoch. W^mh uses this shared, continuously-evolving secret to run a lightweight membership-authentication step: a member proves knowledge of the current epoch's group secret to the server via a standard digital signature, convincing the server the uploader or downloader is a legitimate current group member without revealing which member. This requires only a standard signature scheme (classical or post-quantum), not a specialized anonymous-credential construction. To keep server-side record indices from linking back to a member's identity across epochs, the wrapper additionally applies a per-epoch random permutation (via a pseudorandom permutation, generated either by an oblivious shuffle such as Fisher-Yates or a Thorp shuffle, or by hashing each member's identity and sorting) to the party-indexed positions a member's selective-download commit messages occupy on the server.

The paper proves, in the universal composability (UC) framework, that W^mh composed with any CGKA realizing a restricted ideal functionality F^ctxt_CGKA (capturing layer 1 and layer 2 security) realizes a new ideal functionality F^mh_CGKA (capturing all three layers), against a server modeled as honest-but-curious — the first CGKA security model to formalize a non-malicious server, needed to state that the server correctly rejects an outsider's upload or download while remaining unable to learn membership identity from a legitimate one. The paper instantiates the underlying CGKA with a ciphertext variant of Chained CmPKE (a prior CGKA construction using multi-recipient public-key encryption, from the same authors' earlier work), which supports selective downloading (also called filtered CGKA): a member downloads only the update material addressed to it rather than the whole commit.

### Measured results
This paper reports analytical bandwidth-overhead figures derived from cryptographic-object sizes, not runtime or wall-clock benchmarks; no simulation, testbed, or timing measurement is present. The overhead is computed symbolically (Table 3, in terms of group size N and per-epoch proposal counts U/A/R for update/add/remove) and then instantiated concretely (Table 4) for a group of N=256 members, assuming no proposal was issued during the prior epoch (which the authors state makes the Commit and Process percentage overheads reported here an upper bound; in practice, with proposals present, both figures are lower).

General bound (Section 1.2 and Section 6.2, applying to any CGKA realizing F^ctxt_CGKA composed with W^mh): the wrapper never increases the bandwidth cost of update, add, remove, commit, process, or application messages by more than a factor of two (100%), because the added elements are one signature and one verification key per relevant message.

Concrete instantiation, four multi-recipient-public-key-encryption(mPKE)+signature pairings at NIST security level I (128-bit-equivalent), N=256 members, sizes in bytes, nominal cost then wrapper overhead added:
| Procedure | ElGamal+ECDSA (classical) | SIKEp434+Falcon | Ilum512+Dilithium | Bilbo640+SPHINCS+ |
|---|---|---|---|---|
| Propose-'upd' | 160 +64 | 1,662 +666 | 5,608 +2,420 | 44,416 +17,088 |
| Propose-'add' | 128 +64 | 1,893 +666 | 4,500 +2,420 | 27,360 +17,088 |
| Propose-'rem' | 64 +64 | 666 +666 | 2,420 +2,420 | 17,088 +17,088 |
| Commit | 8,384 +160 | 6,088 +2,229 | 18,600 +6,152 | 60,800 +34,208 |
| Process | 224 +64 | 2,008 +666 | 6,360 +2,420 | 54,680 +17,088 |
| Application message | 64 +64 | 666 +666 | 2,420 +2,420 | 17,088 +17,088 |

Across these four instantiations, the paper states the wrapper's percentage overhead peaks at 44% for Propose-'upd', 63% for Propose-'add', 100% for Propose-'rem', 57% for Commit, 39% for Process, and 100% for application messages (Section 6.2). The underlying mPKE building blocks (Table 2, sizes in bytes for encryption key |ek|, base ciphertext |ct0|, per-recipient ciphertext |bctid|): ElGamal-based 32/32/32; SIKEp434-based 330/330/16; Ilum512 768/704/48; Bilbo640 10,240/10,240/24.

### Parameters
| Parameter | Value(s) used |
|---|---|
| Target security level | NIST Level I (~128-bit, no easier than key recovery on AES-128) |
| Group size for concrete Table 4 figures | N = 256 members |
| Proposal counts for Commit/Process figures | 0 (idealized, no proposals in the prior epoch — a stated upper bound on percentage overhead) |
| Multi-recipient PKE (classical) | ElGamal-based, via Kurosawa's multi-recipient variant with a decomposability transform |
| Multi-recipient PKE (post-quantum) | SIKEp434-based, Ilum512, Bilbo640 (all from the authors' own prior Chained CmPKE paper) |
| Signature schemes | ECDSA (classical), Falcon, Dilithium, SPHINCS+ (all NIST PQC candidates/finalists) |
| Pseudorandom permutation construction | Fisher-Yates shuffle (O(N-1) swaps) or Thorp shuffle (O(log N) per member) if cache-timing attacks are a concern; alternatively a hash-and-sort construction using Batcher sorting networks, O(N log^2 N) |

### Stated limitations
The security model and protocol cover only the CGKA layer of secure group messaging; extending the proof to the full message-exchange layer of a complete secure-group-messaging protocol is left unaddressed, citing one contemporaneous paper as the first to model the full protocol at layer 1. The protocol does not prevent an adversary from anonymously registering many fake groups on the server; it only prevents an outsider from accessing an existing group's contents, and the authors state this gap is efficiently solvable with standard anonymous credentials, left as future work. Metadata outside the paper's three-layer model, specifically access-timing side channels and device fingerprinting, can defeat the privacy guarantee the wrapper provides, because the model does not represent either channel. The formal model excludes adversary-controlled randomness (an adversary forcing a corrupted member to reuse or bias its randomness); this attack class is left as future work, consistent with the authors' note that recent related models make the same exclusion. Message size itself is not hidden by the wrapper: an observer can still infer the CGKA protocol's internal structure and group activity from the sizes of proposal, commit, and welcome messages, because size correlates with proposal type, group size, or (for tree-based CGKAs such as TreeKEM) the sender's position in the ratchet tree and the tree's topology; the paper works through concrete leakage examples for Chained CmPKE, TreeKEM, and Tainted TreeKEM and states the extent of the leakage is protocol- and topology-dependent, without giving a general fix beyond noting that padding could remove the proposal-type signal. Welcome messages leak the receiving member's identity (it must remain in the clear so the server can route delivery) and, if the uploading member's identity is not separately hidden, allow the server to link the uploader and the new member as co-members of the same group. Formalizing the wrapper's non-interactive fetch/download step required weakening the ideal functionality to let the server return database contents to any requester without a membership check on download (only upload is authenticated); the authors state that whether this weakening has practical impact is an open question, left as future work. The paper's efficiency comparison against Signal's Private Groups is asymptotic (O(log N) upload cost for the wrapper's construction versus O(N) for Private Groups) and is not benchmarked against a Private Groups implementation in this paper.

### Requirements it places on the rest of the system
Requires every group member to hold and continuously evolve a single shared group secret key, as in MLS-style CGKA (not per-pairwise secrets, as in Signal); the wrapper's server-authentication mechanism is built directly on proving knowledge of this key each epoch. Requires the underlying CGKA to already realize the paper's F^ctxt_CGKA functionality (hiding layers 1 and 2); the wrapper adds only layer-3 (access-pattern) hiding and provides no guarantee if composed with a CGKA that leaks sender identity in the clear. Requires an honest-but-curious server: the paper's own security model states that a malicious, actively adversarial server can always choose to accept or reject the wrapper's authentication step arbitrarily, at which point the wrapper "does not provide any meaningful functionality" and the composed protocol degrades to the underlying CGKA's layer-1/layer-2-only guarantee — so any deployment that cannot assume server-side honesty on the accept/reject decision gets no metadata protection from this mechanism against that server. Requires each member to compute a per-epoch pseudorandom permutation over the full set of N member indices before locating its own position, an O(N) or worse per-epoch cost (O(N-1) swaps for Fisher-Yates, O(N log^2 N) for the sorting-network alternative) that every member — not just the committer — must perform. Requires a delivery layer that lets the server maintain two per-group, per-epoch lists (proposal database and commit database) and serve fetches from them without a per-fetch membership check, per the weakened non-interactive functionality; a system requiring download-side authentication as well as upload-side authentication is not what this construction proves secure. Bandwidth overhead is additive only on the upload direction (the added signature and verification key), so a deployment bandwidth-constrained specifically on the download side gains no benefit from that constraint being addressed by this mechanism.

### Contradicts
None found.

### References worth retrieving
- K. Bhargavan, R. Barnes, E. Rescorla, "TreeKEM: Asynchronous Decentralized Key Management for Large Dynamic Groups," 2018 — foundational (defines TreeKEM, the CGKA construction underlying MLS that this paper's leakage analysis directly examines)
- R. Barnes, B. Beurdouche, J. Millican, E. Omara, K. Cohn-Gordon, R. Robert, "The Messaging Layer Security (MLS) Protocol," IETF standard — foundational
- J. Alwen, S. Coretti, Y. Dodis, Y. Tselekounis, "Security Analysis and Improvements for the IETF MLS Standard for Group Messaging," CRYPTO 2020 — foundational (UC security model for CGKA layer 1 that this paper's F^ctxt_CGKA model extends)
- J. Alwen, S. Coretti, D. Jost, M. Mularczyk, "Continuous Group Key Agreement with Active Security," TCC 2020 — foundational
- K. Hashimoto, S. Katsumata, E. Postlethwaite, T. Prest, B. Westerbaan, "A Concrete Treatment of Efficient Continuous Group Key Agreement via Multi-Recipient PKEs," CCS 2021 — foundational (defines Chained CmPKE, the underlying CGKA this paper's wrapper is instantiated over; note this is the target paper found MISMATCHED under key HASHIMOTO-CCS-21 in this corpus and needs re-retrieval)
- M. Chase, T. Perrin, G. Zaverucha, "The Signal Private Group System and Anonymous Credentials Supporting Efficient Verifiable Encryption," CCS 2020 — competing (analyzes Signal's Private Groups, the KVAC-based metadata-hiding SGM this paper compares against and improves on in asymptotic upload cost)
- M. Chase, S. Meiklejohn, G. Zaverucha, "Algebraic MACs and Keyed-Verification Anonymous Credentials," CCS 2014 — competing (the KVAC building block underlying Signal's Private Groups, which this paper's construction avoids)
- K. Klein, G. Pascual-Perez, M. Walter, C. Kamath, M. Capretto, M. Cueto, I. Markov, M. Yeo, J. Alwen, K. Pietrzak, "Keep the Dirt: Tainted TreeKEM," IEEE S&P 2021 — competing (Tainted TreeKEM variant, whose commit-message-size leakage this paper analyzes as a limitation example)
- M. Weidner, M. Kleppmann, D. Hugenroth, A. R. Beresford, "Decentralized Asynchronous Continuous Group Key Agreement" (DCGKA) — foundational (already in this corpus's verified seed list; superseded by BeeKEM per the brief)
- J. Alwen, D. Hartmann, E. Kiltz, M. Mularczyk, "Server-Aided Continuous Group Key Agreement," CCS 2021 — competing (an alternative approach to reducing CGKA cost via server assistance, a different mechanism from this paper's server-agnostic wrapper)

### Verbatim extracts
"increases the bandwidth cost of the underlying CGKA operations by at most a factor of two"
"the bandwidth overhead is added only in the upload direction"
"by at most 44%, 63%, 100%, 57%, 39% and 100%, respectively"
"a server that honestly follows the protocol but tries to learn as much metadata as possible"
"does not provide any meaningful functionality" when the server is malicious
"we do not consider adversary-controlled randomness in the current model"
"metadata outside the scope of our models, such as access timing... may circumvent the privacy guarantees"
"the size of an uploaded commit message is affine in the group size N"
