## [JARECKI-ASIACRYPT-14] Round-Optimal Password-Protected Secret Sharing and T-PAKE in the Password-Only Model
**Citation:** Stanislaw Jarecki, Aggelos Kiayias, Hugo Krawczyk. "Round-Optimal Password-Protected Secret Sharing and T-PAKE in the Password-Only Model." ASIACRYPT, 2014. DOI 10.1007/978-3-662-45608-8_13.
**Retrieved:** full text via https://eprint.iacr.org/2014/650.pdf
**Source URL:** https://eprint.iacr.org/2014/650.pdf
**Domain:** I

### What it does
A password-protected secret sharing (PPSS) scheme with parameters `(t, n)` lets a user store a secret `s` split across `n` servers so the user can later reconstruct `s` using only a password, without any device holding a long-term key. The scheme provides a threshold guarantee: a user reconstructs `s` after contacting any `t+1` honest servers, while an attacker who compromises up to `t` servers learns nothing about `s` offline and gains only an online-guessing advantage proportional to the number of interactions attempted divided by the size of the password dictionary. The paper's core construction, 2HashDH-NIZK, realizes a verifiable oblivious pseudorandom function (V-OPRF): the client hashes and blinds its password as `a = H1(x)^r`, sends `a` to a server holding secret key `k`; the server returns `b = a^k` together with a non-interactive zero-knowledge (NIZK) proof of discrete-log equality between `(g, y, a, b)` where `y = g^k` is the server's public key; the client verifies the proof, unblinds by computing `b^(1/r)`, and applies a second hash `H2` to derive the pseudorandom output. Verifiability (the "V" in V-OPRF) means the client can detect a server deviating from the protocol using only the server's public key, without needing the secret key. The PPSS protocol built on this V-OPRF requires exactly one message from user to server and one message from server to user — the paper's stated round-optimality — in the password-only setting, meaning neither party holds an authenticated public key in advance (a common reference string suffices instead). The same PPSS construction composes generically with any key-exchange protocol to yield a single-round threshold password-authenticated key exchange (T-PAKE) for arbitrary `(t, n)`, with no public-key infrastructure requirement for clients or servers and no communication between servers.

### Measured results
The paper contains no empirical implementation, benchmark, or runtime measurement; all quantitative claims are protocol-structure facts derived by construction and proof, not measurements from a running system.

- Round complexity: the PPSS protocol requires one message from user to server and one message in reply — a single round trip — stated as the paper's central contribution ("round-optimal").
- Security bound (Theorem 1): for the 2HashDH-NIZK V-OPRF realizing functionality F_VOPRF under the `(N, Q)` One-More Gap Diffie-Hellman assumption, the simulator's distinguishing advantage is bounded by `q_S · ε_omdh,G(N, Q) + q_3/m² + 2·q_U/m + N²/m + ε_PRF(q_2)`, where `q_S` is the number of senders, `q_U` the number of users, `q_2` and `q_3` the number of queries to hash functions `H2` and `H3`, `m` the group order, and `N = Q + q_1` with `q_1` the number of `H1` queries and `Q` the number of V-OPRF executions.
- Online-guessing advantage: an attacker making `q` total interactions with users and servers gains advantage `q/|D|` (plus a negligible term) against a password drawn from dictionary `D` of size `|D|`.
- Robustness threshold: correct reconstruction despite up to `t` corrupted servers is achievable only when `2t + 1 ≤ n`; the paper states the other two security properties (secrecy, soundness) impose no such bound.
- Attack-cost reduction for the V-OPRF-based instantiation specifically: the number of rogue-send messages an online attacker needs to test one password against a target user is reduced by a factor of `t − t' + 1` relative to the generic T-PAKE composition bound, where `t'` is the number of servers already compromised.

### Parameters
- Threshold parameters `(t, n)`: `t` is the maximum number of corrupted servers tolerated for secrecy and soundness; `n` is the total number of servers; robustness additionally requires `2t + 1 ≤ n`. No specific numeric values are recommended; the construction is stated for arbitrary `(t, n)`.
- Group: cyclic group of prime order `m` with generator `g`; secret key `k` drawn uniformly from `Z_m`; public key `y = g^k`.
- Hash functions `H1` (range: the group `⟨g⟩`), `H2` (range `{0,1}^λ` for security parameter `λ`), `H3` (used inside the NIZK), modeled as random oracles.
- Dictionary size `|D|`: the space of passwords the attacker can guess from; online-attack advantage scales as `q/|D|` for `q` total interactions, no numeric value fixed by the paper.

### Stated limitations
Robustness (correct reconstruction despite corrupted servers) holds only when `2t + 1 ≤ n`; the paper states this is "an intrinsic limitation" not shared by the secrecy and soundness properties. The pre-shared-key variant of the derived T-PAKE protocol requires each server to store a per-client secret key and requires a confidential channel to transmit that key during initialization; the paper states this as "its relative drawback." The public-key-based T-PAKE variant avoids the per-client-secret requirement but needs each client to generate and store a private/public key pair at initialization, adding key-management structure the pre-shared-key variant does not need. The paper's security-game count for "rogue send" messages only counts messages naming the target client as sender or recipient, which the authors state is a deliberate modeling restriction forcing the attacker to disclose which client it is attacking; they do not model an attacker probing without disclosing a target.

### Requirements it places on the rest of the system
The V-OPRF-based T-PAKE requires servers to use independent per-client V-OPRF keys — the paper states explicitly that adding the client identity as an input to a shared V-OPRF key would not achieve the same guessing-attempt-counting property, so key derivation per client, not per-request tagging, is required. The scheme assumes a common reference string (CRS) is available to all parties before any protocol run — the group parameters, generator, and hash functions must be fixed and agreed upon in advance; this is treated as outside the protocol's own message flow ("secure initialization phase" assumed). Servers must be able to detect and reject a client message `a` that is not a member of the group `⟨g⟩` (the protocol's check `a ∈ ⟨g⟩`); an omission here breaks the discrete-log-equality proof's soundness guarantee. Any system layering additional messages on top of the single-round PPSS exchange (for example, nonce exchange for a derived T-PAKE session key, or an explicit key-confirmation message) must piggyback those payloads onto the existing two messages to preserve round-optimality, or add exactly one further message if key confirmation is required — the paper states this explicitly as the mechanism for adding forward secrecy via an authenticated Diffie-Hellman exchange.

### Contradicts
None found.

### References worth retrieving
- **[2]** Bagherzandi, Jarecki, Saxena, Lu, "Password-protected secret sharing," CCS 2011 — foundational, defines the PPSS primitive this paper improves on for round complexity.
- **[37]** MacKenzie, Shrimpton, Jakobsson, "Threshold password-authenticated key exchange," Journal of Cryptology 19(1), 2006 — foundational, the T-PAKE security model this paper extends.
- **[24]/[25]** Freedman, Ishai, Pinkas, Reingold, "Keyword search and oblivious pseudorandom functions," TCC 2005 — foundational, an early oblivious-PRF construction predating 2HashDH.
- **[11]** Camenisch, Lysyanskaya, Neven, "Practical yet universally composable two-server password-authenticated secret sharing," CCS 2012 — competing two-server PPSS construction.
- **[10]** Camenisch, Lehmann, Lysyanskaya, Neven, "Memento: How to reconstruct your secrets from a single password in a hostile environment," CRYPTO 2014 — competing, contemporaneous secret-reconstruction-from-password scheme.
- **[8]** Brainard, Juels, Kaliski, Szydlo, "A new two-server approach for authentication with short secrets," USENIX Security 2003 — foundational, early two-server password-authentication approach.
- **[34]** Katz, Vaikuntanathan, "Round-optimal password-based authenticated key exchange," Journal of Cryptology 26(4), 2013 — competing, round-optimality result for plain (non-threshold) PAKE that this paper's T-PAKE construction is compared against implicitly by problem framing.
- **[32]** Katz, Mackenzie, Taban, Gligor, "Two-server password-only authenticated key exchange," ACNS 2005 — competing, prior two-server password-only construction.
- **[21]** Di Raimondo, Gennaro, "Provably secure threshold password-authenticated key exchange," J. Comput. Syst. Sci. 72(6), 2006 — competing, earlier threshold-PAKE construction.

### Verbatim extracts
- "We present the first round-optimal PPSS scheme, requiring just one message from user to server, and from server to user"
- "robustness can only be achieved if 2t + 1 ≤ n while the other properties do not impose such intrinsic limitation"
- "adding the client identity as an input to the V-OPRF would not solve this issue"
- "the term qrog(U) can be reduced by a factor of t − t′ + 1"
- "no PKI or secure channel requirements for clients or servers... with arbitrary (t, n) threshold parameters"
