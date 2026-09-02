# Removing illegal material from content-addressed storage

## Verdict: open

No published construction makes a peer cryptographically unable to serve a specified piece of
already-published content in a permissionless, content-addressed network. Every mechanism found,
deployed or proposed, is one of two kinds: a voluntary identifier denylist that a node operator may
or may not consult, or a key-destruction scheme that presupposes a cooperating uploader and a
pre-established custody committee — a condition an adversary who deliberately publishes illegal
material will never supply. Deny-list compliance in a real deployed network, IPFS, has been measured
directly, repeatedly, and as recently as 2026: compliance is high only at the one operator that
maintains the list, falls to under a fifth of requests at independent gateways, and is defeated
outright, at zero cost, by re-encoding the same bytes under a different hash.

## What the deployed mechanism is, and how it is measured

Sokoto, Balduf, Trautwein, Wei, Tyson, Castro, Ascigil, Pavlou, Korczyński, Scheuermann, and Król
("Guardians of the Galaxy: Content Moderation in the InterPlanetary File System," USENIX Security
2024) ran the first full measurement of IPFS's only deployed moderation mechanism, Protocol Labs'
"badbits" denylist. A Content Identifier (CID) in IPFS is a hash of the data itself, so any peer can
verify what it serves against the identifier requested; the denylist stores, for each blocked item,
the hex-encoded SHA-256 of the base32-encoded CID rather than the CID itself, so an operator can test
membership without holding a plaintext list of blocked material — a privacy technique for checking
membership, not an enforcement mechanism, since nothing compels a node to run the check or to act on
a match. Protocol Labs applies the list only to gateways it operates itself.

The paper's dataset: 411,522 of the list's then-410,000+ entries recovered by hash-matching against
CIDs collected from roughly 300 billion Bitswap requests (mid-2021 to January 2024, covering about 1
billion unique CIDs) and 1.3 billion DHT requests (September 2022 to January 2024, 120 million CIDs);
368,762 of the resulting 417,912-CID denylist (badbits plus phishing URLs mined from four Web2
anti-phishing feeds) successfully downloaded and classified. By content type: 87.97% copyright
material (mostly PDF/ePub academic texts migrated from shadow libraries such as Anna's Archive and
the Nexus project), 5.81% phishing, 0.06% terrorist material (255 CIDs), and under 0.01% content the
authors' automated classifier flagged as explicit, of which a subsequent check against the Internet
Watch Foundation's hash database matched three images, all classified as hentai (Japanese
pornographic anime/manga) rather than genuine CSAM; content the takedown senders themselves labeled
CSAM was excluded from download entirely and handled through separate coordination with the IWF, so
the paper reports no independent verification of how much CSAM the badbits list holds.

Gateway compliance, measured by sending HTTP HEAD requests for a daily sample of 5,000 badbits and
5,000 Web2-denylist CIDs across 431 gateways through January 2024: gateways operated by Protocol Labs
itself block essentially all badbits content; gateways run by large CDNs block about 18%; other
public gateways cluster similarly low. Content persists a mean of 713 days between first observation
on the network and inclusion on the denylist, against under a day for the Web2 anti-phishing feeds the
same paper compares against. Within the IPFS peer-to-peer layer itself — Bitswap and the DHT, as
opposed to the HTTP gateways — the paper finds no evidence of enforcement at all; filtering is a
gateway-side, not a protocol-side, phenomenon.

Kastantin, Balduf, Ascigil, Sokoto, Scheuermann, Duda, Król, and Korczyński ("Netting Phish in the
IPFS Ocean," ACM Web Conference 2026), overlapping in authorship with the 2024 paper, ran an
eleven-month follow-up (September 2024–July 2025) focused on phishing specifically, sampling under 1%
of daily Bitswap traffic (a stated lower bound) and 3.3 million CID-bearing passive-DNS requests. It
found 10,489 phishing CIDs, twice the number carried by the combined public anti-phishing feeds
(APWG, OpenPhish, PhishTank) for the same period, and reports that the badbits denylist "adds no
additional CIDs beyond the union of APS and our detections" — the central curated list contributed no
coverage the independent web-facing feeds and the authors' own pipeline had not already found,
nineteen months after the 2024 paper documented the same list's coverage gaps. During the measurement
window 196 gateways updated their blocking policies, moving 569 CIDs from allowed to blocked; the
paper frames this as a lower bound on active moderation activity across the gateway population, not
as evidence the list itself is comprehensive.

## Circumvention: alternative-hash re-encoding, not a partial gap

Both the 2024 and 2026 papers, and an independent third paper, converge on the same finding by three
different methods, which raises it from an isolated result to a structural property of hash-derived
content addressing.

Sokoto et al. re-added 100 already-blocked phishing files to the network using a different hash
function for the CID (Kubo, the reference IPFS implementation, supports 72), then re-requested them
through the gateways that had been blocking the originals. Of 57 gateways blocking any of the sampled
content, 56 served the re-hashed copy, and content-level evasion succeeded for 97.4% of individually
tested CIDs; the single resistant gateway also proved to be the one gateway vulnerable to the paper's
separate directory-wrapping evasion (requesting blocked content by a relative path inside an
unblocked parent directory succeeded for 67 of 68 tested CIDs, 98.5%, on that gateway; the authors
disclosed both findings, and cite an earlier private test that found and fixed four more vulnerable
Protocol-Labs-operated gateways before publication).

Karapapas, Pittaras, Polyzos, and Patsakis ("Hello, won't you tell me your name?: Investigating
Anonymity Abuse in IPFS," arXiv 2506.04307, June 2025) independently confirmed the same class of
evasion by choosing a different chunk size when re-adding content, which likewise yields an unrelated
CID, and states plainly that "a malicious actor can circumvent it by simply choosing an alternative
chunking size when adding the file to IPFS," citing the Sokoto paper's own hash-function-substitution
result as the precedent. The same paper measured pinning-service Know-Your-Customer practices
directly: Pinata and Fleek accepted the first disposable email address the authors generated;
Filebase accepted one after four attempts; 4EVERLAND required only a cryptocurrency wallet, itself
creatable with no identifying information; all three email-gated services worked over Tor. Uploading
a functioning, VirusTotal-flagged WannaCry sample and a synthetic malware stub to five pinning
services succeeded on every one, with no service performing content inspection before accepting or
serving the file.

Kastantin et al.'s 2026 measurement documents the same defeat occurring in deployed attacker
behavior, not as an experiment the researchers ran themselves: clustering 10,489 collected phishing
pages by content similarity, the paper finds that in the two largest clusters (1,459 and 256
instances) attackers vary only HTML comments or whitespace between successive uploads, which is
sufficient to generate a fresh, unlisted CID each time while leaving the rendered page identical, and
states the general mechanism directly — "any modification, no matter how small, yields a new CID."
The same paper ran a controlled test of a second, independent circumvention path: it published a
file through its own IPFS node, fetched it once through each gateway, then withdrew the only copy
from its node. Every gateway that had returned the file in the first round still returned it in the
second, because fetching through the gateway had caused the gateway's own backend IPFS node to
announce itself as a new content provider — nineteen such new providers appeared after a single round
of gateway fetches, entirely independent of whether the original publisher remained online. A voluntary
denylist enforced only at the point of retrieval cannot outrun a protocol property in which the act of
retrieval itself creates a new, unlisted, independently persistent copy.

## Why key-destruction cryptography does not reach this problem

The corpus and a broader search turned up one 2026 systematization of the general technique closest
to "make serving cryptographically impossible": Aikebaier, "SoK: Cryptographic Erasure on Public
Ledgers" (IACR ePrint 2026/1109), which classifies application-layer schemes that leave a ledger or
store untouched and instead destroy the decryption key needed to read data already committed to it —
crypto-shredding. It organizes the field into a twelve-cell grid crossing data locus (ciphertext
on-chain, an off-chain store such as IPFS anchored by an on-chain commitment, or a hybrid) against key
custody (single custodian, (t, n)-threshold committee, time-lock, or witness encryption), and proves
a formal equivalence between a "Destruction-IND" security notion and the EU's GDPR Article 17 "render
unrecoverable" erasure criterion for a cooperating data controller.

The scheme does not solve, or claim to solve, the problem this pass asked about, for two reasons the
paper's own definitions make explicit rather than requiring inference.

First, every one of the paper's seven evaluated reference architectures assumes a single controller
who both creates the data and either holds or empanels the committee that later destroys the key —
the paper's worked example throughout is a UK law firm's audit-trail records under a compliance
mandate, and its equivalence theorem is a tool for that controller to document a defensible erasure
claim to a regulator. Nothing in the taxonomy addresses who selects a custody committee, or under what
process, in a permissionless network with anonymous, adversarial uploaders who have every incentive
not to cooperate. A committee empanelled to revoke content over an open network's objection is a
trusted party by another name, and the paper never proposes how one would be selected without
reintroducing exactly that trust.

Second, and structurally decisive independent of the first point: the paper's own security game
(Definition 2, "Destruction-IND") is explicitly voided once an adversarial party has reconstructed the
plaintext before the destruction event — the paper states this as Remark 1, "if k ≥ t, the adversary
reconstructs Dec from the coerced shares before Destroy is ever invoked and wins trivially," and
frames its whole model around measuring security only for an adversary who has not yet crossed that
threshold. For illegal material on a real content-addressed network, that threshold has already been
crossed by the time anyone requests removal: Sokoto et al. measured a 713-day mean gap between first
appearance and denylist inclusion, during which any number of independent nodes may already have
retrieved, decoded, and independently re-published the plaintext, exactly as Kastantin et al.
demonstrated gateways do automatically on ordinary retrieval. A key-destruction scheme secures a
single ciphertext behind a committee; it has no mechanism for, and its own formal model does not even
define security against, a party who already holds the plaintext and re-inserts it under a CID the
committee never touched.

A separate, earlier proposal specific to IPFS — Politou, Alepis, Patsakis, Casino, and Alazab,
"Delegated content erasure in IPFS" (Future Generation Computer Systems 112, 2020) — could not be
retrieved in full text (the publisher copy is paywalled; the institutional-repository copy at Charles
Darwin University sits behind a Cloudflare challenge that blocked automated retrieval). Its mechanism,
as described consistently across the publisher abstract and independent third-party summaries, is a
protocol for propagating a signed erasure request across IPFS nodes, restricted so that "only the
original content provider or delegates" may issue one. That restriction is reported here as an
unverified, secondary-source characterization rather than a measured fact, per this pass's own
sourcing standard, and it is enough on its own to place the scheme outside the scope of this problem:
a mechanism gated on the uploader's own request cannot remove content an uploader deliberately
published and has no interest in withdrawing. Independent evidence that the scheme was never adopted
comes from its own co-author: Patsakis is also a co-author of the 2025 Karapapas et al. paper, which
states without qualification, five years after the erasure proposal, that "there is no official
deletion mechanism for IPFS," citing the 2020 paper only as the source for that absence, not as a
deployed remedy.

## The one structural property that does resist a classical peer-to-peer countermeasure

Content poisoning — flooding a network with corrupted copies of a targeted item so that a downloader
is likely to retrieve a broken file, deployed historically by copyright holders against BitTorrent and
earlier file-sharing networks — is defeated by the same property that makes deny-list circumvention
trivial. A content identifier is the hash of the exact bytes requested, so IPFS's Bitswap protocol
(and BitTorrent's own per-chunk hashing, for the same reason) lets a downloader verify each block it
receives against the CID it asked for, per Benet's original IPFS design description already in this
corpus (`BENET-ARXIV-14`) and per Trautwein et al.'s deployed-system description cited throughout the
papers above. A poisoned block simply fails verification and is discarded, so it is the identical
mechanism that makes removal-by-denylist gameable (any single-byte change produces an unlisted,
independently valid identifier) that makes removal-by-poisoning impossible (any corrupted block is
independently checkable and discarded). No source in this pass measures content poisoning against
IPFS specifically; the point is structural, not a separate measured result, and is recorded here only
to close off a mechanism family a synthesis step might otherwise propose.

## Assumption doing the work

Every mechanism examined supplies its guarantee only because some party is assumed to cooperate
voluntarily: a gateway operator choosing to consult a hash-based denylist it has no protocol-level
obligation to honor; a custody committee that must be empanelled, and trusted, before an adversarial
upload ever occurs; an uploader who must be the one requesting their own content's erasure. A
decentralized deployment, by definition, has no operator positioned to compel any of these — no party
can force an independent gateway operator to adopt a denylist, empanel a committee an anonymous
adversary will accept in advance, or compel a malicious uploader to request deletion of the material
they deliberately published. The measured deployed reality is a voluntary honor system with
partial, heterogeneous, and empirically falling-further-behind compliance (the central curated list
added zero unique coverage over independent detection fully nineteen months after its own gaps were
published), defeated at the protocol layer by the same hash-derived addressing that gives
content-addressed storage its integrity guarantee in the first place: change one byte, and the
"same" content is a different, unlisted object.

## What was searched

Corpus: `registry/index-measurements.md` and `registry/index-requirements.md` were read in full and
grepped for `deny.?list`, `removal`, `illegal`, `csam`, `takedown`, `moderat`, `redact`, `censor`,
`content.address`, `chameleon`, `mutable`, `forget`, `gdpr`, `badbits`, `blocklist`, `poison`, and
`unlinkab`. Full evidence entries opened: `BALDUF-IMC-23`, `BALDUF-IMC-24`, `BENET-ARXIV-14`,
`BENET-FILECOIN-17`, `DANEZIS-WALRUS-25`, `KEIZER-CSUR-24`, `WEI-NSDI-24`, `ZHANG-ARXIV-25`,
`ZHANG-PACMHCI-24`, `WOLCHOK-WOOT-10`. `KEIZER-CSUR-24` (2024 survey) supplied the pointer that
motivated the rest of this pass: it states the badbits process was, at the time of that survey,
undocumented ("little is known about the moderation process involved in preparing the bad bits
list") and its adoption unmeasured.

Beyond the corpus: DBLP's publication-search API for `IPFS content moderation`, `IPFS illegal
content`, `denylist IPFS`, `redactable blockchain` (30 hits, all chain-rewriting constructions
explicitly out of scope per the SoK's own §1.1 and therefore not pursued further), `NeuralHash
attack`, `content addressable network censorship`, and `InterPlanetary File System security`, the
last of which surfaced both `SOKOTO-USENIXSEC-24` and the 2022 IPFS eclipse-attack paper (Prünster,
Marsalek, Zefferer, USENIX Security 2022 — disrupts availability network-wide, not a moderation
mechanism, not pursued further). Web searches covered `IPFS content-addressed storage illegal content
removal survey 2025 systematization of knowledge`, `threshold decryption revocable access
content-addressed storage cryptographic erasure 2024 2025` (surfaced the crypto-erasure SoK),
`content poisoning copyright enforcement peer-to-peer measurement effectiveness`, `IPFS content
moderation 2026 badbits denylist measurement follow-up study` (surfaced the 2026 WWW phishing
paper), and `decentralized storage CSAM detection cryptographic 2026 arxiv` (no relevant result).

Full text retrieved with `tools/fetch-paper.py` and read in full: `SOKOTO-USENIXSEC-24` (Guardians of
the Galaxy, USENIX Security 2024, 92,483 characters via the USENIX-hosted PDF after the DBLP `ee`
link resolved only to a landing page), `POLITOU-ARXIV-25` (Karapapas et al., arXiv 2506.04307, June
2025, 53,162 characters), `SOK-CRYPTOERASURE-EPRINT-26` (Aikebaier, IACR ePrint 2026/1109, 79,714
characters), and `KROL-WWW-26` (Kastantin et al., ACM Web Conference 2026, 60,193 characters, via the
KOR Labs-hosted author copy). `POLITOU-FGCS-20` (Politou et al., Future Generation Computer Systems
112, 2020) could not be retrieved: the Elsevier/ScienceDirect page and the ResearchGate page both
returned HTTP 403, and the Charles Darwin University institutional-repository PDF returned a
Cloudflare interstitial rather than the document; its mechanism above is therefore reported only from
secondary description and flagged as such, per this pass's rule against citing measurements from
unretrieved sources. The most recent directly relevant full-text retrieval is `KROL-WWW-26`
(April 2026 conference date, retrieved September 2026).