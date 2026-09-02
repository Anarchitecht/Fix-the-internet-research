## [HASHIMOTO-CCS-21] A Concrete Treatment of Efficient Continuous Group Key Agreement via Multi-Recipient PKEs
**Citation:** Keitaro Hashimoto, Shuichi Katsumata, Eamonn Postlethwaite, Thomas Prest, Bas Westerbaan. "A Concrete Treatment of Efficient Continuous Group Key Agreement via Multi-Recipient PKEs." ACM SIGSAC Conference on Computer and Communications Security (CCS), 2021, 1441–1462. DOI 10.1145/3460120.3484817.
**Retrieved:** full text via https://eprint.iacr.org/2021/300.pdf (registry candidate URL; DOI 10.1145/3460120.3484817 confirmed against `targets-deduped.json`)
**Source URL:** https://eprint.iacr.org/2021/300.pdf
**Domain:** H

### What it does
Chained CmPKE reduces the download and total network cost of a Continuous Group Key Agreement (CGKA)
protocol's commit message — the message a group member sends to refresh cryptographic key material and
give every other member Post-Compromise Forward Security (PCFS), the guarantee that a device compromise
at one point in time does not expose past or future messages — by giving the group's untrusted delivery
server one narrow function: strip a multi-recipient ciphertext down to only the one sub-ciphertext each
downloading member needs, rather than delivering the same full commit message to everyone. The
construction starts from Chained mKEM (a prior scheme organizing the group as a single-level, N-wide
tree rather than TreeKEM's binary tree of depth log N) and adds a Committing Multi-recipient Public-Key
Encryption (CmPKE) primitive: a multi-recipient PKE (a ciphertext under which many different recipients,
each with an independent public key, can decrypt the same or different sub-messages) extended with one
commitment value that every recipient can check against a single signature, so the server can hand out
individual sub-ciphertexts without any recipient needing a separate authentication proof (avoiding the
O(log N)-sized Merkle membership proof a naive per-recipient commitment scheme would need). The paper
also derives three new post-quantum multi-recipient PKE constructions — Bilbo640, Ilum512, LPRime757 —
each a multi-recipient variant of an existing single-recipient post-quantum key-encapsulation mechanism
(Frodo, Kyber, LPRime respectively), built to keep the marginal bandwidth cost of each additional
recipient in a multi-recipient ciphertext lower than sending N independent single-recipient ciphertexts.

### Measured results
The bandwidth-versus-group-size comparison (Table 1, Figures 6–7) is a closed-form asymptotic and
concrete-parameter calculation, not an implementation measurement: TreeKEM costs Ω(log N) per direction
and Ω(N log N) total; Chained CmPKE costs O(N) upload, O(1) download, O(N) total. The paper's own
concrete instantiations show uploaded commit messages of less than 50 KiB for groups of at most 1,024
users, and Chained CmPKE's uploaded commit messages compare favorably to post-quantum TreeKEM
instantiations for groups of "less than 200 users" — beyond that group size the paper's own asymptotics
favor TreeKEM's O(log N) upload growth over Chained CmPKE's O(N).

Computational-efficiency figures are measured from an implementation (Go, with C bindings for the
underlying mechanisms, i.e. multi-recipient key-encapsulation constructions, implemented in C), on a
single-threaded Apple M1 central processing unit (CPU) at 3.2 GHz:

| Operation | Instantiation | Group size N | Measured time |
|---|---|---|---|
| Multi-recipient encryption (CmEnc) | Lattice-based (Bilbo640, Ilum512, or LPRime757) | 2^10 = 1,024 | under 100 ms |
| Multi-recipient encryption (CmEnc) | SIKEp434 (isogeny-based) | 2^10 = 1,024 | about 7.5 s |
| Multi-recipient encryption, amortized speedup over N independent single-recipient encryptions | Bilbo640 | 1,024 | ~29× faster |
| Multi-recipient encryption, amortized speedup | Ilum512 | 1,024 | ~4× faster |
| Multi-recipient encryption, amortized speedup | LPRime757 | 1,024 | ~3× faster |
| Multi-recipient encryption, amortized speedup | SIKEp434 | 1,024 | ~2× faster |

The paper states its own bandwidth cost model treats one uploaded byte as equal in cost to one downloaded
byte, and justifies this by noting all its instantiations keep uploaded commit messages under 50 KiB for
groups up to 1,024 users, uploadable in under 0.2 seconds "even in countries with low uploading speed" —
citing 2.90 Mbps as the slowest measured national average as of July 2021 (Afghanistan), from a
third-party survey the paper cites, not a measurement of its own.

### Parameters
- Symmetric-key size κ = 128 bits, used for the one-time authenticated symmetric encryption (SKE)
  component wrapping the shared message.
- Signature scheme: Dilithium, chosen for balanced performance and standard-lattice-assumption security.
- Three lattice-based multi-recipient PKE parameter sets derived by the paper: Bilbo640 (from Frodo640),
  Ilum512 (from Kyber512), LPRime757 (from LPRime653); plus a fourth, isogeny-based, SIKEp434.
- Reported asymptotic-to-concrete improvement of the derived multi-recipient PKEs over naively combining
  N independent single-recipient PKEs: a factor of 16 (Kyber512 versus Ilum512) to 71 (Frodo640 versus
  Bilbo640) reduction in commit-message size.
- Group sizes tested in the bandwidth comparison: swept up to N = 1,024 (2^10) in the concrete figures.

### Stated limitations
The paper explicitly leaves as future work assessing whether TreeKEM's download cost could similarly be
lowered using the same sanitizing-server idea, stating this "would entail more server-side bookkeeping of
the tree structure ... which would likely add complexity to the protocol description and security
proof." Two further open items appear in the appendix bibliographic trail: an interesting-future-research
note on the mKEM security-reduction tightness, and a note that a Gröbner-basis cryptanalytic question for
one of the derived post-quantum constructions is left as future work. The construction's asymptotic
upload cost, O(N), is worse than TreeKEM's Ω(log N); the paper's own crossover point, stated directly, is
"groups of less than 200 users" for favorable concrete comparison, meaning the mechanism's advantage is
an empirical, parameter-dependent claim bounded to a stated group-size range, not an asymptotic win.

### Requirements it places on the rest of the system
The delivery server must perform an active sanitizing step — extracting and delivering only the
sub-ciphertext addressed to each recipient — rather than acting as a pure bulletin board; the paper's
security proof holds regardless of server behavior, but bandwidth savings and correct delivery depend on
the server actually doing this. Every recipient must be able to verify the single shared commitment T
against the group's shared signature before trusting its individually delivered sub-ciphertext,
requiring the signature and commitment to be transmitted to every member independent of the server's
sanitization. The construction assumes members are organized as a flat, depth-1 structure of arity N (not
TreeKEM's binary tree), so any component built on TreeKEM's per-node public-key structure (proposals
targeting individual tree nodes, node-level blanking) is not directly compatible without translation.

### Contradicts
None found against other corpus entries on measured facts. ALWEN-CCS-22 (Server-Aided Continuous Group
Key Agreement) cites this construction as "CmPKE" and re-benchmarks it, substituting this paper's
post-quantum multi-recipient PKE instantiation with a Diffie-Hellman-based one for a fair-assumption
comparison against its own SAIK protocol — a difference in instantiation choice for comparison purposes,
not a disagreement over either paper's own reported figures.

### References worth retrieving
- **Foundational** — Joël Alwen, Daniel Jost, Marta Mularczyk. "On The Insider Security of MLS."
  Cryptology ePrint Archive, Report 2020/1327. (Defines Insider-Secure TreeKEM, the baseline this paper
  benchmarks against.)
- **Foundational** — Karthikeyan Bhargavan, Richard Barnes, Eric Rescorla. "TreeKEM: Asynchronous
  Decentralized Key Management for Large Dynamic Groups." 2018. (Origin of the TreeKEM ratchet-tree
  construction.)
- **Foundational** — Shuichi Katsumata, Kris Kwiatkowski, Federico Pintore, Thomas Prest. "Scalable
  Ciphertext Compression Techniques for Post-quantum KEMs and Their Applications." ASIACRYPT 2020.
  (Source of the isogeny-based multi-recipient PKE this paper adapts as SIKEp434.)
- **Foundational** — R. Barnes, B. Beurdouche, J. Millican, E. Omara, K. Cohn-Gordon. "The Messaging
  Layer Security (MLS) Protocol." IETF draft. (The deployed standard TreeKEM underlies and this paper's
  bandwidth comparison targets.)
- **Competing** — Joël Alwen, Dominik Hartmann, Eike Kiltz, Marta Mularczyk. "Server-Aided Continuous
  Group Key Agreement." ACM CCS 2022. (Already retrieved in this batch as ALWEN-CCS-22; benchmarks
  directly against this paper's CmPKE construction under a shared cost model.)

### Verbatim extracts
- "downloading one byte costs as much as uploading one byte."
- "our instantiations of our protocol achieve uploaded commit messages of less than 50KiB for groups of
  at most 1024 users."
- "Even for group of 2^10 members, lattice-based CmPKEs perform a multi-recipient encryption in less than
  100 ms."
- "compared to TreeKEM-based equivalents ... have consistently better upload costs for groups of less
  than 200 users."
- "All measurements were obtained on an Apple M1 CPU @3.2 GHz (single-threaded)."
