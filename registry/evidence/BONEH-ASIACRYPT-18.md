## [BONEH-ASIACRYPT-18] Compact Multi-Signatures for Smaller Blockchains
**Citation:** Dan Boneh, Manu Drijvers, Gregory Neven. "Compact Multi-Signatures for Smaller Blockchains." ASIACRYPT, 2018. DOI 10.1007/978-3-030-03329-3_15.
**Retrieved:** full text via https://eprint.iacr.org/2018/483.pdf
**Source URL:** https://doi.org/10.1007/978-3-030-03329-3_15
**Domain:** E

### What it does
A multi-signature scheme lets n parties, each holding an independently generated key pair, jointly produce one short signature on one common message that a verifier accepts as proof all n parties signed. The paper gives three such schemes and one signature-aggregation scheme, each defending against the rogue-key attack (an attacker registers a public key computed from the honest parties' keys so a signature effectively covers a message the honest parties never saw).

MSP, the main pairing-based scheme, uses Boneh-Lynn-Shacham (BLS) signatures over a bilinear group (three prime-order groups G1, G2, Gt and an efficiently computable pairing e: G1 x G2 -> Gt). Each signer's secret key is a scalar in Zq; the public key is g2^sk in G2. To aggregate n public keys into one aggregate key apk, each key is raised to an exponent H1(pk_i, {pk_1,...,pk_n}) — a hash of that key together with the whole key set — and the results multiplied. To sign, each signer i computes a partial signature s_i = H0(m)^(a_i * sk_i), where a_i is the same per-key hash exponent used in key aggregation and H0 hashes the message into G2; a designated combiner (any signer, or an outside party) multiplies the partial signatures together into one final signature. Verification checks one pairing equation. This construction removes the interactive key-aggregation-commitment round that earlier BLS-based multi-signature schemes needed to block the rogue-key attack, without requiring signers to prove possession of their secret key.

AMSP extends MSP so that several multi-signatures on different messages can themselves be aggregated into one further-compressed signature. ASM (accountable-subgroup multi-signature) lets any subset S of n parties sign so the resulting signature discloses which subset signed, at O(security parameter) bits of signature and public-key size beyond the description of S itself, independent of n; earlier accountable-subgroup schemes needed O(n x security parameter) bits. MSDL is a Schnorr-based (discrete-log) alternative that repairs a security-proof gap the authors state exists in an earlier Schnorr-based scheme by Maxwell et al., adding one extra communication round to that scheme's signing protocol. Section 6 gives proof-of-possession (PoP) variants of every scheme: each signer additionally publishes a signature on its own public key at registration; this removes one layer of the security-proof's forking-lemma loss (see Parameters) and lets key aggregation use a plain product or hash instead of a multi-exponentiation, at the cost of a larger per-key public key.

### Measured results
| Scheme | Combined public-key size | Combined signature size | Total size for tx=1500, inp=3, n=3 (bytes) | Threshold support |
|---|---|---|---|---|
| Bitcoin (deployed, no aggregation) | tx*inp*n*\|G\| | tx*inp*n*2*\|Zq\| | 1296 | linear in n, t |
| MuSig (Maxwell et al.) | tx*inp*\|G\| | tx*(\|G\|+\|Zq\|) | 240 | small (n,t) only |
| MSDL (this paper, Section 5) | tx*inp*\|G\| | tx*(\|G\|+\|Zq\|) | 240 | small (n,t) only |
| MSP (this paper, Section 3.1) | tx*inp*\|G2\| | tx*\|G1\| | 360 | small (n,t) only |
| AMSP (this paper, Section 3.3) | tx*inp*\|G2\| | \|G1\| | 216 | small (n,t) only |
| ASM (this paper, Section 4) | tx*inp*\|G2\| | tx*inp*(\|G1\|+\|G2\|) | 864 | any polynomial t, n |

Conditions for the byte column: a Bitcoin block with tx=1500 transactions, each with inp=3 inputs, all spending from n-out-of-n multisig wallets with n=3. Bitcoin, MuSig, and MSDL use secp256k1 (|G|=32 bytes, |Zq|=32 bytes); MSP, AMSP, and ASM use the BLS381 pairing curve (|G1|=96 bytes, |G2|=48 bytes, |Zq|=32 bytes). The pairing-based MSP/AMSP scheme and the discrete-log MSDL scheme each use under 20% of the space the deployed Bitcoin solution uses, at these parameters. Separately, for a 50-out-of-100 multisig wallet, the deployed Bitcoin solution is stated to need 30 times more space than the ASM scheme; the paper does not show the arithmetic for this second figure, so it is reported here as stated, not derived.

The security proof for MSP is stated as a concrete reduction: MSP is (tau, q_S, q_H, epsilon)-unforgeable under the random-oracle model, given q > 8*q_H/epsilon and the co-computational-Diffie-Hellman (co-CDH) problem is hard with parameters (tau + q_H*tau_exp1 + q_S*(tau_exp2^l + tau_exp1) + tau_exp2^l) * 8*q_H^2/epsilon * ln(8*q_H/epsilon), epsilon/(8*q_H)), where q_H is the number of random-oracle queries, q_S the number of signing queries, l the maximum signers in one multi-signature, and tau_exp1/tau_exp2 the time to exponentiate in G1/G2. The 8*q_H^2/epsilon multiplicative loss comes from a two-layer application of the forking lemma; the PoP variant (MSP-pop) removes one layer, reducing the loss to epsilon/(q_H+q_S+1) with no q_H^2 factor, which the paper states yields a tighter reduction and, at fixed concrete security, shorter keys and signatures.

### Parameters
- Security parameter kappa: sets group and hash-output sizes; no concrete value is fixed by the scheme itself.
- Bilinear group choice: BLS381 curve used in the worked size example (|G1|=96B, |G2|=48B, |Zq|=32B); secp256k1 used for the discrete-log schemes (|G|=32B, |Zq|=32B).
- l: maximum number of signers combined into a single multi-signature; appears directly in the security-loss term for MSP and in the running time for MSP-pop.
- Worked block-size example parameters: tx=1500 transactions, inp=3 inputs per transaction, n=3 signers per multisig wallet (n-of-n). Not measured from a deployed network; chosen by the authors as illustrative.
- Random-oracle query bound q_H and signing-query bound q_S: enter the security-loss formula; no fixed values are given, only the algebraic form.

### Stated limitations
Compressing signatures alone, without also aggregating the public keys, is stated to save little space, because all n public keys still have to be written to the blockchain. The Schnorr-based scheme by Maxwell et al. that this paper builds on and repairs is stated to have a gap in its published security proof; whether it can be proven secure under a different assumption or in the generic group model is stated as an open problem. The plain-public-key-model defense against rogue-key attacks (no proof of possession required) is stated to require a multi-round or hash-heavy key-aggregation step, whereas the PoP variants avoid that at the cost of larger public keys and a per-key proof-of-possession check at registration. The paper leaves open which of the two pairing groups (G1 or G2) has the more compact representation, stating the choice depends on the application. Proof-of-possession requires a static or infrequently-changing signer set, or the possession proofs have to be re-verified whenever new keys enter the aggregation.

### Requirements it places on the rest of the system
Every signer must have generated its key pair before any aggregation or signing occurs, and the aggregation step (or, for PoP variants, the possession-proof verification) must run over the full identical set of participating public keys that later signers use, since the per-key aggregation exponent is itself a hash of that whole set. A pairing-friendly elliptic curve (an asymmetric bilinear group with an efficient pairing) must be available in the underlying cryptographic library for the MSP, AMSP, and ASM schemes; the MSDL scheme instead needs only ordinary discrete-log groups such as secp256k1. Signing for MSP requires either a single designated combiner to receive every partial signature and multiply them, or every verifier to be able to perform that same multiplication; no total ordering or synchrony among signers beyond that combination step is required. Non-PoP schemes rely on the plain-public-key model holding, meaning the system must not assume any signer proved possession of its secret key at registration; PoP variants instead require the registration process to check the possession proof e(H1(y_i), y_i) = e(pi_i, g2) for every key before accepting it into any aggregate.

### Contradicts
None found.

### References worth retrieving
- Maxwell, Poelstra, Seurin, Wuille, "Simple Schnorr multi-signatures with applications to Bitcoin," ePrint 2018/068 — competing (the Schnorr-based scheme this paper's MSDL repairs and compares against).
- Drijvers, EdalatNejad, Ford, Neven, "Okamoto beats Schnorr: On the provable security of multi-signatures," ePrint 2018/417 — attack (identifies the security-proof gap in Maxwell et al.'s scheme).
- Ristenpart, Yilek, (proof-of-possession defense against rogue-key attacks) — foundational (source of the PoP technique this paper's Section 6 builds on).
- Bellare, Neven — foundational (the plain-public-key-model rogue-key defense this paper's key-aggregation approach builds on).
- Micali, Ohta, Reyzin, "Accountable-subgroup multisignatures," ACM CCS 2001 — foundational (defines the ASM primitive this paper's Section 4 gives a compact construction for).
- Boldyreva, (threshold BLS multi-signature) — competing (an earlier pairing-based multi-signature scheme cited as the trivial-size baseline).

### Verbatim extracts
"An eﬃciently computable non-degenerate pairing e : G1× G2→ Gt in groups"
"there is a gap in the security proof, and that security cannot be proven under this assumption"
"Whether their scheme can be proved secure under a different assumption... is currently an open problem."
"tighter security reductions, and therefore shorter key and signature sizes if concrete security is taken into account"
