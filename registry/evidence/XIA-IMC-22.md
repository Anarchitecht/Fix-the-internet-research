## [XIA-IMC-22] Challenges in Decentralized Name Management: The Case of ENS
**Citation:** Pengcheng Xia, Haoyu Wang, Zhou Yu, Xinyu Liu, Xiapu Luo, Guoai Xu, Gareth Tyson. "Challenges in Decentralized Name Management: The Case of ENS." ACM Internet Measurement Conference (IMC), 2022. DOI 10.1145/3517745.3561469.
**Retrieved:** full text, but the file on disk is arXiv:2104.05185v1 (12 Apr 2021), titled "Ethereum Name Service: the Good, the Bad, and the Ugly," by six of the seven target authors (Pengcheng Xia, Haoyu Wang, Zhou Yu, Xinyu Liu, Xiapu Luo, Guoai Xu — Gareth Tyson absent). The dataset, research questions, methodology, and reported figures below are identical in kind to the published abstract's claims (a large-scale ENS event-log study reporting traditional-DNS-inherited issues plus ENS-specific smart-contract issues); this is the pre-publication version of the same study, not an unrelated paper. Numeric values below may differ from the camera-ready IMC 2022 text if the dataset window was extended before publication; treat the specific counts as sourced to the 2021-04-12 arXiv snapshot, cut off at Ethereum block 10,746,639 (2020-08-28 03:03:42 UTC).
**Source URL:** https://arxiv.org/abs/2104.05185
**Domain:** E

### What it does
Measures adoption, usage, and security of the Ethereum Name Service (ENS), a naming system built as Ethereum smart contracts that maps human-readable names to blockchain addresses and other records, so that a person can send funds to a name instead of a raw 40-hexadecimal-character address. ENS separates the naming function into three smart-contract roles: a registry (holds name-to-owner and name-to-resolver mappings, plus a per-name record cache time-to-live), a registrar (assigns names to owners under a registration rule — historically a Vickrey auction, later a fixed-fee permanent registrar), and a resolver (holds the name-to-record mapping, with eight defined record types: address, reverse-resolution name, content hash for IPFS/Swarm/Tor, key-value text, raw DNS wire-format record, ECDSA public key, contract ABI, and delegated authorization). ENS stores each name as a hash ("namehash," built by recursively hashing each label with keccak256) rather than as plaintext, so the paper's authors reconstruct plaintext names by matching candidate hashes against Dune Analytics' ENS name dictionary, a generated wordlist of 460,000-plus English words, and the Alexa top-100K domain list.

### Measured results
| Measurement | Value | Conditions |
|---|---|---|
| Dataset window | up to Ethereum block 10,746,639 | 2020-08-28 03:03:42 UTC cutoff |
| Registered ENS names found | 465,827 | decoded from registry event logs |
| Distinct Ethereum addresses that ever used ENS | 107,617 | same dataset |
| Names restored to plaintext | 373,950 total, 323,255 of them .eth (86.6% of all .eth names) | via namehash-dictionary matching against Dune Analytics data, a 460K-word list, and Alexa top-100K |
| Event logs collected | ~2 million registry logs, ~3.4 million registrar logs, ~200,000 resolver logs, plus over 3,000 decoded transactions for text-record values | from 14 manually labeled ENS core smart contracts plus 8 additional third-party resolvers |
| Explicit brand-squatting names | 15,179 .eth names, held by 1,532 addresses | heuristic: one address holds 2+ known-brand names (matched against Alexa top-100K 2LDs) whose real DNS domains belong to different owners; 42.7% of these names still active at study time |
| Typo-squatting names | 18,483 .eth names targeting 13,450 distinct Alexa domains | generated via dnstwist (12 variant methods: bitsquatting, omission, replacement, addition, vowel-swap, homoglyph, insertion, hyphenation, various, transposition, repetition) applied to Alexa top-100K, producing 755,908,096 candidate variants, then hash-matched against ENS; 52% of matched names still active |
| Total unique squatting names (explicit + typo) | 33,662 names, ever owned by 6,548 addresses | union of the two prior heuristics |
| Names with records among the 33,662 squatting names | 4,474 (3,775 still active); 85% of those set only a blockchain-address record | remaining records mostly point to sale listings (Opensea links, IPFS sale pages) |
| "Guilt-by-association" expanded suspicious names | 279,193 additional .eth names | all further names held by addresses already flagged as squatters; over 40% of these addresses hold more than 10 such names, accounting for over 96% of the 279,193 total |
| Top-10 squatter addresses' combined share | ~17% of all ENS names ever registered | same dataset |
| Malicious dWeb/onion/URL records found | 19 malicious content-hash-linked sites (17 distinct second-level names): 7 gambling, 5 adult, 7 scam | out of 5,879 unique dWeb hashes, 34 onion hashes, 620 URLs found in records; URLs scored via VirusTotal (flagged malicious if ≥2 of ~70 engines agree), screenshots via Eyewitness, content classified via Google Cloud Vision/Natural-Language APIs; no malicious traditional-DNS websites found among the 620 URLs |
| Scam blockchain addresses registered as ENS names | 3 | manual cross-check against scam-address sources; no comprehensive ground-truth dataset existed, so this is a lower bound |
| Expired names with records still attached ("record persistence") | 16,017 expired .eth names (plus 3,116 subdomains) retain resolvable records after expiry | ENS does not clear a name's records on expiry; example: thisisme.eth, expired 2020-05-04, still had 706 subdomains with live Ethereum-address records observed after re-registration by the authors for protection |
| Initial-auction (Vickrey) highest recorded bid | 201,709 ETH bid on ethfinex.eth, final auction price 0.01 ETH | Vickrey auction mechanics: highest bidder wins, pays the second-highest bid |
| Most valuable permanent-registrar name | darkmarket.eth, over 20,000 ETH paid by winner | separate from Vickrey auction period |

### Parameters
- Malicious-URL threshold: a URL is marked malicious if flagged by 2 or more of VirusTotal's ~70 anti-virus engines (following prior studies' methodology, cited but not re-derived here).
- Squatting heuristic threshold: one address controlling 2 or more known-brand-matched 2LDs whose real DNS owners differ triggers explicit-squatting classification.
- Alexa-name filtering: names of Alexa top-100K entries and typo variants shorter than 4 characters are excluded (119,764 Alexa names and 15,701 typo-squatting variants removed) to reduce false positives from short, generic strings.
- dnstwist variant generation: 12 method classes applied to the Alexa top-100K domain list, no stated cap on variants per domain (google.com alone produced 1,982 variants).

### Stated limitations
The authors restored only 86.6% of .eth names to plaintext, which they say limits detection of combosquatting variants (names that embed a brand plus extra tokens) among the unrestored 13.4%, though they state this restoration gap does not affect the explicit- and typo-squatting counts, which are computed on hash values directly rather than on restored plaintext. Distributed-denial-of-service and other traditional DNS attack classes are stated as not studied, due to time and cost, and left as future work. The malicious-dWeb count (19) is stated as a lower bound, because IPFS and Swarm content is not required to be persistently pinned online, so some content-hash targets could not be reached during the analysis window. The scam-address count (3) is stated as limited by the absence of any comprehensive ground-truth list of scam blockchain addresses at the time of the study.

### Requirements it places on the rest of the system
A ledger-based naming system that stores names as hashes (to bound identifier length and block enumeration during auction periods) requires an external plaintext-name dictionary — built from a wordlist, a domain list, or a data dump the naming project itself publishes — for any downstream service, moderation tool, or measurement pipeline to resolve a hash back to a human-readable string; absent that dictionary, a name is opaque even to the chain that stores it. A design that never clears a name's resolver records on expiry requires whichever wallet or client resolves that name to independently check the name's registration status (active vs. expired) before trusting any resolved address, because the mapping itself gives no signal that ownership has lapsed. A design permitting unrestricted third-party resolver deployment (the paper finds and decodes 8 additional resolvers beyond ENS's own two) requires any measurement or moderation system to enumerate resolver contracts dynamically rather than assume a fixed, closed set.

### Contradicts
None found. No other entry in this batch measures ENS or any blockchain naming system.

### References worth retrieving
- Foundational: Hari, Lakshman, "The Internet Blockchain: A Distributed, Tamper-Resistant Transaction Framework for the Internet," ACM HotNets 2016 — early proposal for blockchain-based DNS replacement.
- Foundational: Kalodner, Carlsten, Ellenbogen, Bonneau, Narayanan, "An Empirical Study of Namecoin and Lessons for Decentralized Namespace Design," WEIS 2015 — first empirical measurement of a blockchain naming system (Namecoin), which the paper cites as the precedent for its own methodology.
- Competing: Guan, Garba, Li, Chen, Kaaniche, "AuthLedger: A Novel Blockchain-Based Domain Name Authentication Scheme," ICISSP 2019 — alternative design reducing certificate-authority trust rather than replacing DNS resolution outright.
- Competing: He, Su, Gao, Yue, "TD-Root: A Trustworthy Decentralized DNS Root Management Architecture Based on Permissioned Blockchain," Future Generation Computer Systems 102, 2020 — permissioned-blockchain alternative to ENS's fully public-chain design.
- Attack/critique: Szurdi, Kocso, Cseh, Spring, Felegyhazi, Kanich, "The Long 'Taile' of Typosquatting Domain Names," USENIX Security 2014 — the typo-squatting methodology (dnstwist-style variant generation) this paper's ENS analysis is adapted from.
- Attack/critique: Kintis, Miramirkhani, Lever, Chen, Romero-Gómez, Pitropakis, Nikiforakis, Antonakakis, "Hiding in Plain Sight: A Longitudinal Study of Combosquatting Abuse," ACM CCS 2017 — the combosquatting class this paper states its restoration gap may miss.
- Competing: Patsakis, Casino, Lykousas, Katos, "Unravelling Ariadne's Thread: Exploring the Threats of Decentralised DNS," IEEE Access 8, 2020 — survey of blockchain-DNS threats (malware, registrar mechanisms, phishing) covering multiple systems, a broader-scope comparison point to this paper's ENS-only measurement.

### Verbatim extracts
- "the same names with names of Alexa list in total" — squatting-match criterion (paraphrased context above).
- "465, 827 registered names and 107, 617 Ethereum addresses that ever used ENS."
- "16, 017 expired .eth names have records within them or their subdomains."
- "we get 19 (17 second-level ENS names) malicious dWeb URLs."
- "these top-10 addresses have ever held around 17% of all names."
- "DNS and the aforementioned solutions still cannot achieve human-readability, security and decentralization simultaneously."
