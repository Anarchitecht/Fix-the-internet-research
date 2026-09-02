## [SOKOTO-USENIXSEC-24] Guardians of the Galaxy: Content Moderation in the InterPlanetary File System
**Citation:** Saidu Sokoto, Leonhard Balduf, Dennis Trautwein, Yiluo Wei, Gareth Tyson, Ignacio Castro, Onur Ascigil, George Pavlou, Maciej Korczyński, Björn Scheuermann, Michał Król. "Guardians of the Galaxy: Content Moderation in the InterPlanetary File System." 33rd USENIX Security Symposium, August 2024.
**Retrieved:** full text via https://www.usenix.org/conference/usenixsecurity24/presentation/sokoto
**Source URL:** https://www.usenix.org/conference/usenixsecurity24/presentation/sokoto
**Domain:** K

### What it does
This is a measurement study of how content moderation actually functions in the InterPlanetary File
System (IPFS), a content-addressed peer-to-peer storage network in which files are identified by
hash-based Content Identifiers (CIDs). IPFS itself has no built-in moderation; the paper studies the
moderation layer built on top of it by the network's principal maintaining organization, Protocol Labs,
called the "badbits" denylist: a list of hex-encoded SHA256 hashes of CIDs deemed problematic after a
takedown request, published for any IPFS Gateway operator (an HTTP-to-IPFS bridge server) to voluntarily
filter against. Because a CID's hash conceals the underlying content, the paper builds candidate-CID
sets from passive network observation (Bitswap broadcast traffic and Distributed Hash Table, DHT, request
logs) and reverse-maps their hashes against the badbits list to recover the actual CIDs the list refers
to, since the list itself only ever exposes a hash, not the CID. The paper measures four separate stages
of the moderation pipeline as they function on the live network: which content gets reported and how
fast; who hosts the flagged content and how replicated it is; which of the many independently operated
Gateways actually enforce the denylist; and whether a filtering Gateway's enforcement can be evaded by an
adversary who controls only how it names or wraps the same underlying bytes.

### Measured results
Data collection: Bitswap broadcast traces collected mid-2021 to January 2024 via a modified IPFS node
accepting unlimited peer connections, observing roughly 300 billion requests covering roughly 1 billion
unique CIDs; DHT traffic collected September 2022 to January 2024 via 20 virtual peer identities running
a modified DHT server, observing 1.3 billion requests covering 120 million CIDs; a passive DNS dataset
covering all gateway-subdomain requests from mid-November 2023 to February 2024. From these logs, the
paper recovers 411,522 of the badbits list's hashed entries (approximately 99.98% of the list) as actual
CIDs, supplements them with 16,128 CIDs extracted from Web2 anti-phishing-service feeds, for a combined
denylist of 417,912 CIDs, of which 368,762 (approximately 86.60%) were successfully downloaded for
classification (all except those separately reported as CSAM, which were never downloaded by the
researchers' own node).

| Finding | Figure | Conditions |
|---|---|---|
| Content-type breakdown of the 368,762 downloaded denylist files | copyright-protected content ≈87.97%; phishing ≈5.81%; terrorist content ≈0.06%; potential CSAM <0.01% | Classified via MIME type, an open-source language model (Mistral) for document/text content, BLIP2 (an image-captioning model combining image encoders and large language models) for images, and SHA256 hashing against the Internet Watch Foundation's own CSAM database for the CSAM figure specifically |
| Classification accuracy checks | Domain-detection manual verification: 100% accurate on 100 files; BLIP2 image classification: 98% accurate on 1,000 files manually classified by Protocol Labs/anti-phishing-service partners | Small manually-checked samples, not the full dataset |
| Scanned-document share | ≈3.41% (12,574 of 368,762 files) are DjVu scanned-document files | Same downloaded-file set |
| Hosting concentration | over 60% of unique denylist content items hosted by just two peers; individual peers observed hosting between 19% and 63% of the entire badbits list | DHT provider-record crawl; the paper states this concentration is "misleading" because content is separately shown to be replicated at multiple locations, complicating any peer-targeted blocking strategy |
| Reporting-to-action latency | Protocol Labs typically actions takedown requests within 24 hours | Analysis of takedown request emails received at abuse@ipfs.tech between 2023-10-22 and 2024-01-11, obtained with permission from former Protocol Labs researchers, never directly accessed by the paper's authors |
| Content age before reporting | Problematic content can persist on the network "for years" before being reported | Same takedown-email and content-age analysis |
| Gateway HTTP-level filtering compliance (HTTP HEAD requests, daily sample of 10,000 CIDs — 5,000 badbits, 5,000 Web2-only-blocked — over January 2024, 431 total gateways observed) | Protocol Labs' own gateways block ~100% of badbits CIDs; CDN-operated gateways block only ~18% of badbits CIDs; other (public/GaaS) gateways show similarly low badbits enforcement; Protocol Labs' gateways block none of the Web2-sourced denylist CIDs, CDN gateways block up to 7% of them, other public gateways average ~18% | HTTP status 410 or 451 classified as "Blocked," 200 as "Available," other/timeout as "Failure" |
| Denylist share of gateway traffic vs. DHT traffic | one measured popular gateway shows 99% of its requests attributed to phishing content, versus ≈0.034% denylist traffic share observed at the DHT layer overall | Passive DNS dataset, top-10 gateways by request volume |
| CID-version normalization circumvention test | 0 of 100 sampled top-10%-blocked CIDs became accessible when requested by their alternate (v0 vs. v1) CID encoding | Tested 2024-02-04; the paper concludes all evaluated gateways correctly normalize CID versions before checking the denylist |
| Directory-wrapping circumvention test | 1 of the tested gateways was vulnerable: 67 of 68 blocked CIDs (≈98.5%) became retrievable when wrapped in an unblocked parent directory and requested by relative path | 100 sampled CIDs, non-NATed hosting node, malicious content never actually served by the researchers; an earlier preliminary run (2023-12-19) found four additional vulnerable Protocol Labs gateways, which the paper states were fixed after responsible disclosure |
| Alternative-hash-function circumvention test | 56 of 57 gateways that blocked any requested content became circumventable; evasion succeeded for 97.4% of usually-blocked CIDs in that group | 100 sampled phishing CIDs, re-uploaded under a different of the 72 hash functions the kubo IPFS implementation supports, then removed from the researchers' own node immediately after the test |
| Proposed-improvement measured gain | 227% increase in detected phishing content; 43% reduction in average time between a deceptive site's appearance and its filtering | The paper's own proposed tighter integration between Protocol Labs and existing Web2 anti-phishing services, evaluated by the paper's own methodology — described as requiring "minimal implementation effort," not deployed on the live network as of this paper |

### Parameters
- Gateway HTTP-request sampling: 10,000 CIDs per day (5,000 badbits, 5,000 Web2-only-blocked), sent as
  HTTP HEAD requests (not GET, to avoid downloading full content), over the full month of January 2024,
  against all 431 gateways in the paper's dataset.
- Gateway categorization used throughout the results: operated by Protocol Labs; operated by a large
  Content Delivery Network (CDN); public gateways listed on the official ipfs.tech tracker; ephemeral
  gateways (105 identified, all subdomains of a single Web3 Gateway-as-a-Service provider, Infura); an
  "others" catch-all for unlisted gateways discovered via threat-intelligence and passive-DNS sources.
- Circumvention test sample size: 100 CIDs per test (CID-version test, directory-wrapping test, and
  alternative-hash-function test each drawn independently).

### Stated limitations
The paper states the hosting-concentration finding (60%+ of content on two peers) is "misleading" taken
alone, because the same content is frequently replicated across additional locations not captured by a
single-peer takedown, meaning peer-targeted enforcement does not remove the content network-wide. The
paper states enforcement of the badbits list is highly uneven across independently operated gateways — a
decentralized moderation approach that depends on voluntary adoption of one shared denylist "facilitates
[the] spread" of problematic content precisely because no single operator's action is authoritative
network-wide, in the paper's own words from its abstract. The paper's directory-wrapping and
alternative-hash-function circumvention tests each identify a live, exploitable, and effective evasion
technique against real deployed gateways at the time of testing — the alternative-hash-function evasion
in particular is stated as "extremely effective," succeeding against 56 of 57 vulnerable gateways. The
paper explicitly limited its own downloading: CSAM-flagged content was never downloaded by the
researchers' own node at any point, and all other downloaded content was deleted immediately after
classification and never re-served to the network, a self-imposed ethical constraint stated directly in
the methodology, not a technical limitation of the moderation mechanism itself.

### Requirements it places on the rest of the system
The badbits denylist mechanism, as measured here, requires every independent gateway operator to
voluntarily fetch and enforce the same shared list — the paper's own measurement shows this requirement is
not met in practice (CDN and public gateways enforcing under 20% of the list), so any design relying on
this specific mechanism for network-wide content removal inherits this same voluntary-adoption gap unless
enforcement is made structurally rather than optionally binding. The mechanism's per-CID granularity means
moderation acts on exact-hash matches; the paper's own alternative-hash-function circumvention result
shows that any content-identification scheme allowing multiple valid identifiers for the same underlying
bytes (a stated property of IPFS's own 72-hash-function-supporting CID design) requires either a
canonicalization step before every moderation check or a content-based (not hash-based) detection layer to
resist this evasion — the paper's own tested gateways almost universally lacked such a layer. Recovering
which CIDs a hash-only denylist refers to requires passive observation of substantial live network traffic
(the paper's own Bitswap and DHT logs, spanning years and billions of requests) to build a large enough
candidate-CID set for reverse-mapping — a downstream system relying on a hash-only denylist for its own
moderation inherits this same operational cost to make the list actionable at all.

### Contradicts
None found against other corpus entries on a measured fact. This paper's own finding that individual
peers commonly host 19%–63% of the entire denylist bears directly on any design assuming content
replication alone is sufficient defense against targeted takedown — the paper's own data shows a small
number of peers can concentrate a large share of even a widely distributed corpus.

### References worth retrieving
- **Foundational** — IPFS specification for public HTTP gateways [52] (governs the HTTP 410/451 status-code
  convention this paper's Blocked/Available classification is built on) — bibliography detail not fully
  captured in this extraction pass; retrieve to confirm identity.
- **Attack/measurement** — cited as references [63, 67] in this paper's related-work discussion of IPFS
  security studies — bibliography detail not fully captured in this extraction pass; retrieve to confirm
  identity and check for overlapping or independent measurement of the same denylist mechanism.
- **Foundational** — cited as reference [68] in this paper, reporting a prior case of Google Safe Browsing
  triggering domain-wide blocking as a side effect of gateway subdomain structure — bibliography detail not
  fully captured in this extraction pass; retrieve to confirm identity.
- **Foundational** — cited as reference [72] in this paper's related-work discussion of IPFS performance
  studies — bibliography detail not fully captured in this extraction pass; retrieve to confirm identity
  and check for overlapping measurement infrastructure (Bitswap/DHT crawling methodology).

### Verbatim extracts
- "over 60% of unique denylist content items hosted by just two peers."
- "only the ones operated by Protocol Labs filter the entire badbits list."
- "the CDN-operated gateways block only around 18% of the requests for badbits CIDs."
- "we are able to access the blocked content on 56" of 57 vulnerable gateways, "evasion was possible for
  the majority (97.4%) of usually blocked CIDs."
- "increase the ratio of detected phishing content by 227%. Our approach reduces the average time between
  the appearance of deceptive websites and their filtering by 43%."
