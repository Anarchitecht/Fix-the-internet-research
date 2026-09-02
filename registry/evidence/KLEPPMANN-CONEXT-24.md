## [KLEPPMANN-CONEXT-24] Bluesky and the AT Protocol: Usable Decentralized Social Media

**Citation:** Martin Kleppmann, Paul Frazee, Jake Gold, Jay Graber, Daniel Holmgren, Devin Ivy, Jeromy Johnson, Bryan Newbold, Jaz Volpert. "Bluesky and the AT Protocol: Usable Decentralized Social Media." ACM DIN Workshop, CoNEXT, 2024. 9 pages. DOI 10.1145/3694809.3700740.
**Retrieved:** full text via https://arxiv.org/abs/2402.03239 (candidate URL list target; text on disk matches the DIN '24 extended version)
**Source URL:** https://doi.org/10.1145/3694809.3700740
**Domain:** J+K

### What it does
The AT Protocol (Authenticated Transfer Protocol) separates social-media hosting into independently replaceable roles so a user can move between providers without losing their username, posts, or social graph. Each user account holds one repository: a signed, append-only collection of records (posts, likes, follows) encoded in DAG-CBOR (a restricted, compact form of the Concise Binary Object Representation). A Personal Data Server (PDS) hosts a set of repositories, exposes them over an HTTP API, and pushes a WebSocket stream of new and deleted records. A Relay crawls known PDSes, verifies the cryptographic proofs on each update, holds its own replica of every repository, and merges the per-PDS streams into one public stream called the firehose. An App View consumes the firehose and computes derived views specific to one social mode (like counts, reply threads, follower sets, timelines) that a client queries indirectly through the user's own PDS. Labelers and feed generators consume the firehose independently and produce, respectively, content-judgment labels and ranked post-ID lists that a client or App View applies as opt-in filters, so ranking and moderation policy are not fixed inside the App View. A repository's records form a Merkle Search Tree (a Merkle tree structure that stays balanced under arbitrary insertion and deletion order); the tree's root hash is signed after every change, which lets any party prove a record is or is not present in a given repository without holding the whole repository. Identity is a Decentralized Identifier (DID), an immutable URI that resolves to a DID document stating the user's current handle, PDS URL, and signing public key; a human-readable handle is a DNS name and is proved to correspond to a DID by a bidirectional link (a DNS TXT record or a `/.well-known/` HTTPS response naming the DID, plus the DID document naming the handle back). The paper defines two DID methods: `did:web`, which resolves via HTTPS to a domain the identity is permanently tied to, and `did:plc`, the protocol's own method, in which the DID is the truncated SHA-256 hash of the initial DID document and later versions are valid only if signed by the key authorized in the immediately preceding version, verified through a chain returned by a directory server.

### Measured results
| Figure | Conditions |
|---|---|
| Over 10 million registered users | Growth from invite-only launch in February 2023 to the paper's writing, roughly 20 months, counted by Bluesky Social PBC's own registration records |
| Real-time single-server mirror of every user repository cost US$153/month | Measured in July 2024, when Bluesky had 6 million users; figure covers repository storage and inbound bandwidth for fetching records from PDSes; excludes compute for building and serving summary indexes; cited to a third-party operator's own report (Newbold, ref. [43]), not an experiment run by this paper's authors |
| "Tens of thousands" of custom feeds created | No date or measurement method given beyond this count; not usable as a precise figure |
| Farcaster per-user storage cost approximately $5 USD/year in Ethereum-equivalent currency | Stated as a comparison figure from Farcaster's own fee schedule (ref. [30]), at the time of writing, not independently measured by this paper |

No latency, throughput, or failure-rate experiment is run by the authors themselves; the paper is an architecture description with one third-party cost citation, not an evaluation study.

### Parameters
- Post length limit: 300 characters of text, up to four images, plus short-form video (Bluesky app-level lexicon parameter, not an AT Protocol parameter)
- DID hash truncation for `did:plc`: SHA-256 hash of the initial DID document, truncated to 120 bits, base32-encoded
- Scuttlebutt comparison parameter cited from related work: default follow-graph crawl depth of three hops

### Stated limitations
The protocol currently supports only public content; the authors state they are investigating mechanisms for private blocking actions but have not built them. Direct messages are handled by a centralized service operated by Bluesky Social PBC, with decentralization stated as a future plan, not a current property. The PLC directory server is a single point that can omit valid DID document versions or fail to respond, and can choose which fork to serve if two correctly signed successor DID documents exist for the same DID; the authors state a future version will use an append-only transparency log to mitigate this, which does not exist yet. Signing keys are held custodially by the PDS operator for ordinary users, so a compromised or malicious PDS operator holds the keys needed to forge repository updates on that user's behalf; the protocol places no requirement on how a PDS authenticates its users. `did:web` identity security depends on trusting the domain's web hosting provider and the certificate authorities that authenticate its HTTPS endpoint. The authors state that most of the indexing infrastructure is currently run by one company, though they argue this does not make the system centralized because repositories are public and re-indexable by anyone.

### Requirements it places on the rest of the system
A Relay requires every PDS to serve a WebSocket stream of signed repository updates and to accept periodic re-crawl requests as a fallback when the stream is interrupted; without a re-crawl fallback, deletions and additions made during a network interruption are missed. An App View requires a Relay's firehose as its only input and does not itself crawl PDSes; a new social mode built on the protocol needs a new App View but can reuse the same PDSes and Relay. Handle verification requires DNS or HTTPS control over a domain and requires the App View performing verification to defend against DNS cache poisoning, optionally with DNSSEC (Domain Name System Security Extensions); the paper states this defense as a should, not as implemented. `did:plc` requires a directory server that returns the full version history for a DID so that clients can verify the unbroken signature chain themselves; the directory's honesty is not required for basic integrity, only for availability and fork-choice, per the paper's own analysis. Blocking enforcement requires block records to be public, because every App View must be able to read who blocks whom in order to drop disallowed interactions; a design that keeps blocks private would remove the App View's ability to enforce them under the mechanism this paper describes.

### Contradicts
None found within this corpus at the time of writing. Note for cross-paper checking: SECKIN-ARXIV-25 measures Bluesky's user and network growth through February 2025 and should be checked for growth-rate figures against this paper's "10 million users in 20 months" figure, since the two papers cover different measurement windows (this paper: through October 2024; SECKIN-ARXIV-25: through February 2025).

### References worth retrieving
- foundational: Auvolat, Taïani, "Merkle Search Trees: Efficient State-Based CRDTs in Open Networks," SRDS 2019, DOI 10.1109/srds47363.2019.00032 — defines the Merkle Search Tree structure the repository uses
- foundational: Sporny, Longley, Sabadello, Reed, Steele, Allen, "Decentralized Identifiers (DIDs) v1.0," W3C Recommendation, 2022 — the DID standard atproto's identity layer implements
- foundational: Laurie, "Certificate Transparency," ACM Queue 12(8), 2014, DOI 10.1145/2668152.2668154 — the append-only log design the authors cite as the intended future mitigation for PLC directory fork attacks
- competing: Henshaw-Plath (fiatjaf), "Pivoting Protocols, from SSB to Nostr," 2023 — Nostr's relay-based architecture, directly contrasted in this paper's related work
- competing: Srinivasan, "Farcaster: A Decentralized Social Network," 2023, and Farcaster Team, "Farcaster Architecture," 2024 — blockchain-anchored identity and storage-fee comparison system
- competing: Lemmer-Webber, Tallon, Shepherd, Guy, Prodromou, "ActivityPub," W3C Recommendation, 2018 — the Mastodon federation protocol this paper compares against on server lock-in and reply-thread consistency
- competing: "Scuttlebutt Protocol Guide," 2023, and Karlsson, "Launch of the PZP protocol and the future of Manyverse," 2024 — the peer-to-peer, key-on-device predecessor and its stated successor protocol addressing multi-device key loss
- attack/critique: Erin, "queer.af domain suspended without warning," 2024 — cited as a real instance of Mastodon-style server-loss risk to a user's social graph

### Verbatim extracts
- "the AT Protocol is designed to support multiple social modes, not just Bluesky"
- "it was possible to maintain a real-time copy of all user repositories on a single server for US$153 per month"
- "Any new version of the DID document is only valid if it has been signed by the key in the previous version"
- "there are no guarantees of anything [...] to use Nostr one must embrace the inherent chaos"
- "Fees are currently collected centrally by the Farcaster team"
