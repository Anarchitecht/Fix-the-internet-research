## [MERKLE-CRYPTO-87] A Digital Signature Based on a Conventional Encryption Function
**Citation:** Ralph C. Merkle. "A Digital Signature Based on a Conventional Encryption Function." Advances in Cryptology — CRYPTO '87, LNCS 293, pp. 369–378, 1988. DOI 10.1007/3-540-48184-2_32.
**Retrieved:** full text via https://doi.org/10.1007/3-540-48184-2_32 (registry candidate URL, matched against `targets-deduped.json`)
**Source URL:** https://www.merkle.com/papers/Certified1979.pdf (registry alternate candidate URL) / https://doi.org/10.1007/3-540-48184-2_32
**Domain:** C

### What it does
The mechanism turns a one-time signature scheme — a signature primitive that can sign only a single
message per key pair before the signing key is exposed — into a signature system that signs an unlimited
number of messages, using only a conventional one-way hash function (the paper uses a conventional block
cipher such as the Data Encryption Standard, DES, keyed on a constant plaintext, to build the one-way
function), with no reliance on the computational hardness of integer factoring. The paper places an
infinite binary tree of one-time-signature key pairs, numbering nodes so the root is node 1, node i's left
child is node 2i and its right child is 2i+1. Every node performs three functions using three independent
one-time signatures: a "left" signature authenticating its left child, a "right" signature authenticating
its right child, and a "message" signature available to sign one user message. Each node's authenticity
is bound into a single value, HASH(i), computed by hashing the concatenation of the one-way hash of the
node's left-signature public values, the hash of its right-signature public values, and the hash of its
message-signature public values — the value this repository's project-instructions document calls a
Merkle-linked structure, generalized to non-binary branching later in the paper. Only the root's HASH(1)
value is published (in a "public file"), authenticating the entire infinite tree. To sign message M, the
signer picks an unused node i, signs M with node i's message-signature key pair, then walks up the tree
from i to the root: at each step, it reveals the parent node's public one-time-signature values for the
child branch just traversed and signs the child's HASH value with the parent's corresponding one-time
signature. A verifier who receives this chain of log(i)-many one-time signatures — one per tree level —
recomputes each HASH value bottom-up and checks it against the next level, terminating at the publicly
known HASH(1). This lets a verifier check any one signed message against a small, fixed, public root
value without needing every other message the tree can ever sign, which is the general property later
content-addressed and Merkle-linked data structures reuse: verify one leaf against a path of hash values
rather than the whole structure.

### Measured results
This is a 1987 analytical design paper with no implementation, benchmark, or experimental run reported;
every quantity below is a designer's own analytical estimate stated in the text, not a measured figure,
and the paper gives no dataset, hardware, or run count because none was executed.

- Stated design-range estimate: "Signature size in a 'typical' system might range from a few hundred
  bytes to a few kilobytes," with signature generation costing "a few hundred to a few thousand"
  invocations of the underlying conventional encryption function — the paper's own words, offered as an
  illustrative range, not a measurement.
- Worked numeric example (Lamport-Diffie base scheme, 128 x-values per one-time signature): signing 1,000
  messages under the naive one-time-signature scheme (no tree) requires roughly 10,000 published y-values
  per user; at 1,000 users each signing 1,000 messages, the public-file storage requirement reaches
  "hundreds of megabytes" — stated by the paper as the motivating problem the tree construction removes,
  not a measurement of any built system.
- Per-signer runtime storage: the paper states that if computations are correctly ordered, a full
  signature can be generated using "128 bytes of RAM," calling this "more than enough" for
  resource-constrained devices such as smart cards of the era — again an analytical estimate, not a
  measured footprint of an implementation.
- Per-signer persistent secret state: one secret key sufficient for a conventional cipher (56 bits, if
  instantiated with DES) plus a simple integer counter (the paper estimates 20 to 30 bits) tracking the
  next unused tree node — the paper shows every leaf's random-looking secret x-values can be regenerated
  deterministically from this one key by encrypting the node/branch/index coordinates, so no per-node
  secret storage is needed.

### Parameters
- Tree branching factor K: the paper analyzes both the binary case (K = 2, requiring log2(i) one-time
  signatures per proof) and the general K-ary case (requiring logK(i) signatures per proof, trading a
  smaller proof for more computation and memory per node, since a K-ary node's HASH value requires
  hashing K+1 sub-values instead of 3). No specific K is recommended as a default; the paper states the
  optimal K "can't be too large" without quantifying a bound, and proposes combining the K-ary tree with
  the author's separate prior "tree-signature" method (cited as reference [3]) to keep the
  per-node authentication cost at O(log K) instead of growing linearly in K, again without a numeric
  recommendation.
- Underlying one-time signature scheme: the paper's chain-of-signatures method is stated to work with any
  one-time signature scheme as a subcomponent; it walks through three specific choices with different
  signature-size costs — plain Lamport-Diffie (2n x-values to sign an n-bit message), the paper's own
  earlier one-time-signature improvement (n + log2(n) x-values, using a released count-of-zero-bits field
  to prevent a forger from claiming fewer 1-bits than were actually signed), and Winternitz's scheme
  (further size reduction by having each x-value represent multiple message bits through repeated
  hash-function application, with the tradeoff of more hash computations per signature).
- Underlying one-way function: the paper assumes availability of a secure one-way hash function F,
  and shows one way to build it from a conventional encryption function (DES) by encrypting a fixed
  constant plaintext under the secret as key; it explicitly warns that the naive way to shrink a wider
  input to a narrower hash output (splitting the input into blocks and double-encrypting) is vulnerable
  to a meet-in-the-middle ("square root") attack requiring roughly 2^28 operations in its own 112-bit-to-
  64-bit worked example, and that a secure design must guard against this class of attack.

### Stated limitations
The paper states its own signature construction is a "meta-system" whose performance depends entirely on
whichever one-time signature scheme is plugged into each tree node, and states plainly that "there is no
particular reason to believe that current one-time signature systems have reached a plateau of
perfection" — the paper does not claim its own choice of underlying one-time scheme is optimal. The
K-ary generalization is described but not resolved: the paper states the problem of minimizing the
per-node authentication information as K grows "is actually interesting in its own right" and proposes,
without evaluating, combining it with a separate hybrid technique. No security proof or formal security
definition is given for the tree construction itself in this text; the paper's security argument is
informal, resting on the assumed security of the one-way function F and of whichever one-time signature
scheme is chosen.

### Requirements it places on the rest of the system
A verifier must already possess (or independently trust) exactly one small public value, HASH(1), the
root of the signer's tree — every other trust decision reduces to checking a hash chain against this one
value, so the mechanism supplies no way to obtain or authenticate that root value itself; that is
assumed to come from outside the mechanism ("placed in the public file," in the paper's own words). The
signer must track, and never reuse, which tree node index was used for each signed message — reusing a
one-time signature node breaks the one-time signature's own security guarantee, a requirement the paper
states is met by keeping a simple incrementing counter. Verification of one signed message requires
receiving and checking a chain of log_K(i) one-time signatures (i the node index used), so the
communication and verification cost of one proof grows with the depth of the node signing it, which
grows with the total number of messages ever signed under that root, unlike a scheme with a fixed-size
proof independent of history.

### Contradicts
None found. No other entry in this corpus disagrees with a measured figure here, because this paper
reports no measured figures — only analytical design estimates, explicitly labeled as such in this entry.

### References worth retrieving
- **Foundational** — Whitfield Diffie, Martin Hellman. "New Directions in Cryptography." IEEE
  Transactions on Information Theory IT-22, 6 (Nov. 1976), 644–654. (Cited as reference [1]; origin of
  the public-key cryptography context this paper's DES-based alternative responds to.)
- **Foundational** — R. Rivest, A. Shamir, L. Adleman. "A method for obtaining digital signatures and
  public-key cryptosystems." Communications of the ACM 21, 2 (Feb. 1978), 120–126. (Cited as reference
  [2]; the factoring-based RSA signature scheme this paper's construction is offered as an alternative
  to.)
- **Foundational** — Ralph C. Merkle. "Secrecy, Authentication, and Public Key Systems." UMI Research
  Press, 1982. (Cited as reference [3]; the author's own earlier "tree-signature" method proposed for
  hybridization with the K-ary construction in this paper.)
- **Competing** — Shafi Goldwasser, Silvio Micali, Ronald L. Rivest. "A 'Paradoxical' solution to the
  Signature Problem." FOCS 1984, 441–448; and "A Digital Signature Scheme Secure Against Adaptive Chosen
  Message Attack," 1986. (Cited as references [8], [9]; an alternative tree-structured signature scheme
  the paper explicitly contrasts, built on claw-free trapdoor permutations from large-prime multiplication
  rather than a conventional one-way function.)

### Verbatim extracts
- "the security does not depend on the difficulty of factoring."
- "the signature size increases logarithmically as a function of the number of messages signed."
- "128 bytes of RAM is more than enough" for generating a signature.
- "there is no particular reason to believe that current one-time signature systems have reached a
  plateau of perfection."
- "the use of a binary tree is arbitrary -- it could just as easily be a K-ary tree."
