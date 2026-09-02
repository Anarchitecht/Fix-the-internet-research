## [QU-TOMCCAP-26] Understanding User-Generated Content and Communities in Decentralized Web3 Networks: An Empirical Study on Nostr
**Citation:** Shutong Qu, Chunyang Li, Hongzhou Chen, Wei Cai. "Understanding User-Generated Content and Communities in Decentralized Web3 Networks: An Empirical Study on Nostr." ACM Transactions on Multimedia Computing, Communications, and Applications (TOMCCAP), 2026. DOI 10.1145/3828666.
**Retrieved:** full text via https://doi.org/10.1145/3828666 (matched title and authors in first 2000 characters)
**Source URL:** https://doi.org/10.1145/3828666
**Domain:** J

### What it does
Characterizes, by direct measurement rather than protocol specification, how content production, social structure, and monetary reward behave on a live deployment of Nostr (Notes and Other Stuff Transmitted by Relays) — a decentralized social-networking protocol in which a lightweight cryptographic event format and signature-verification rule are specified centrally, while storage and dissemination of events are delegated to independently operated relay servers, and clients read from and publish to whichever relays they choose.

Data collection: continuous crawling of four major publicly reachable relays (wss://relay.damus.io, wss://relay.nostr.band, wss://relay.primal.net, wss://nos.lol) from August 30, 2024 to September 14, 2025, retrieving five Nostr event kinds — Kind-0 (user metadata), Kind-1 (text notes), Kind-3 (contact/follow lists), Kind-7 (reactions), and Kind-9735 (Lightning "Zap" tipping receipts) — while excluding encrypted, auxiliary, or non-analyzable kinds (relay recommendations, direct messages, deletions, custom kinds). Each stored record carries event ID, timestamp, author public key, relay source, and raw content, which the authors state supports reconstructing both the discourse layer (text) and the network layer (follow/engagement graph). Deduplication of events mirrored by multiple relays retained the latest copy within a relay and the earliest copy across relays (to approximate cross-relay propagation timing); messages with empty content were dropped, but no other spam/bot filtering was applied, so automated accounts remain in the dataset by design.

Semantic clustering: Kind-1 post text was embedded with SBERT (specifically the all-MiniLM-L6-v2 distilled-BERT sentence-transformer model, producing 384-dimensional vectors) and partitioned into k=10 clusters via MiniBatch K-means, with k chosen by the elbow method combined with silhouette analysis. PCA-then-UMAP (50 principal components, then 2D) was used only for visualization, never for cluster assignment.

Network structure: Kind-3 follow relations among users who both post and participate in the follow graph were modeled as a directed graph, and the Louvain community-detection algorithm (which greedily maximizes modularity, grouping nodes more densely connected to each other than to the rest of the network) partitioned it into communities. A relative-density metric D_r = E / (V * log V) was defined per community (E = intra-community edge count, V = node count) to compare internal cohesion across communities of different sizes without the small-community bias that a V^2 denominator would produce.

Economic-feedback analysis: Kind-9735 Zap events (a Lightning Network micropayment receipt format) were mapped onto the ten semantic clusters to measure how monetary tipping activity distributes across content types.

### Measured results

| Measurement | Value | Conditions |
|---|---|---|
| Total deduplicated events collected | 22,317,426 | across Kind-0, Kind-1, Kind-3, Kind-7, Kind-9735; four relays; Aug 30, 2024 - Sep 14, 2025 |
| Kind-1 posts used for semantic modeling | 6,696,205 | posts with valid textual content entries in the JSONL records; this is a different (smaller) scope than the total event count, explicitly flagged by the authors as not numerically comparable to it |
| Kind-1 posts used for multimedia/URL analysis | 4,749,879 | stricter subset requiring unique, parsable, non-empty text content, after URL parsing and validity checks |
| Distinct Kind-1 authors | 91,311 | unique public keys authoring text notes over the full period |
| Distinct public keys observed overall (posting or interaction) | 378,599 | representing the "observable active population"; this is also the node count of the follow graph used for community detection |
| Point-in-time relay-layer coverage estimate | 72.26% | event-ID overlap check on Kind-1 messages from a single day (Sep 13, 2025 UTC): 109,374 unique Kind-1 messages in an independent same-day relay-universe sample versus 79,037 also observed at the four collection relays; explicitly reported as a one-day relay-layer estimate, not a full-network coverage claim |
| Per-relay unique (deduplicated) event totals | relay.nostr.band 6.48M, nos.lol 5.98M, relay.primal.net 5.44M, relay.damus.io 4.42M | full Aug 30, 2024 - Sep 14, 2025 window; one deduplicated instance counted per event via the default Python Nostr relay manager's relay-selection rule |
| Relay-level growth pattern | relay.damus.io roughly an order of magnitude below the other three before May 2025, then rapid growth toward parity; relay.nostr.band and relay.primal.net show multiple surges after May 2025 and become the most active; nos.lol stays stable and moderate throughout | same period |
| Louvain community count | 1,385 total communities, 108 with at least 10 users | follow graph of 378,599 nodes, 12,068,537 directed following edges |
| User-follow-participation breakdown | of 684,394 total observed users: 296,445 isolated (no follow interaction), 136,907 only-following, 135,066 only-followed, 115,976 both; 378,599 (following and/or followed, with posting activity) form the analyzed follow graph | same collection window |
| Top 8 community sizes | C1 113,580; C2 98,988; C3 40,647; C4 34,843; C5 22,601; C6 21,836; C7 20,062; C8 9,045; remaining communities 16,997 combined | of the 378,599-node follow graph |
| Community 51 internal cohesion example | 35 core users, 274 directed edges, average degree 15.7 | one worked example of a medium-sized, tightly reciprocal community from the D_r metric analysis |
| Inter-community follow ties | 1,408,315 of 12,068,537 total follow edges (about 12%) are inter-community; these span 721 inter-community links across 403 clusters; two communities (IDs 1 and 4) account for more than 80% (1,145,427 edges) of all inter-community ties | follow graph, same window |
| Multimedia (URL) prevalence | 50.4% of posts contain at least one URL; mean 0.72 URLs per post; 15.5% of posts contain 2+ URLs | 4,749,879-post multimedia-analysis subset |
| Zap activity by post type | 1.8% of multimedia posts (>=1 URL) received a Zap vs. 2.4% of text-only posts; mean Zap count 0.093 for multimedia posts vs. 0.080 for text-only posts | same subset |
| Embedding dimensionality and scale | 384-dimensional SBERT vectors (all-MiniLM-L6-v2), embedding matrix shape (6,696,205, 384) | full Kind-1 semantic-modeling subset |
| Cluster validity check | random-sample cosine-similarity check found semantically related messages (e.g., technical updates, decentralization discussion) typically score above 0.8 similarity | qualitative validation, not a formal benchmark |
| UMAP visualization parameters | n_neighbors=15, min_dist=0.1, metric=cosine, applied after PCA reduction to 50 components; 100,000 points randomly sampled for plotting | visualization only, not used for cluster assignment |
| Clustering-quality Silhouette Coefficient | 0.083 (cosine distance) | over the full 10-cluster MiniBatch K-means solution on 6,696,205 posts; authors characterize this as low in absolute terms but consistent with continuous, overlapping high-dimensional text semantic space rather than indicating invalid clustering |
| Cluster sizes, content type, and multimedia rate (Table 1) | see table below | 10 clusters, k selected via elbow method plus silhouette analysis |
| Total observed Zap volume | 0.656 BTC | full Kind-9735 Zap set over the entire observation window (not restricted to the text-clustering subset) |
| Zap concentration by cluster | Clusters 1, 2, 5, and 8 (lifestyle/knowledge/identity content) account for more than 80% of observed Zap activity; Clusters 6 and 9 (automated on-chain/financial broadcasts) receive only a small fraction | full Zap dataset mapped onto the 10 semantic clusters |
| Zap share detail by cluster (message share % / BTC share %) | Cluster 0: 5.12% msgs / 4.30% BTC; Cluster 1: 19.90% msgs / 30.15% BTC; Cluster 2: 7.63% / 19.59%; Cluster 3: 5.83% / 0.80%; Cluster 4: 10.95% / 0.77%; Cluster 5: 13.97% / 23.73%; Cluster 6: 4.13% / 0.01%; Cluster 7: 11.44% / 5.53%; Cluster 8: 11.34% / 13.33%; Cluster 9: 9.69% / 1.79% | message-share denominator is 6,696,205 posts; BTC-share denominator is the 0.656 BTC total Zap volume |

Table 1 (cluster themes, message counts, multimedia rate — full reproduction):

| Cluster | Language | Main content type | Interpretation | n_posts | Multimedia rate |
|---|---|---|---|---|---|
| 0 | Japanese + emoji | Greetings, reactions | Casual affective exchange | 342,692 | 2.0% |
| 1 | English | Nostr / Bitcoin posts | Web3 community broadcasting | 1,332,879 | 25.4% |
| 2 | Mixed | Profile cards, images | Visual identity sharing | 510,652 | 36.0% |
| 3 | English | Sports / fantasy football | Informational analysis | 390,630 | 54.1% |
| 4 | Japanese | Daily life expressions | Localized social interaction | 733,232 | 25.7% |
| 5 | English | External articles (Substack/Medium) | Knowledge curation | 935,664 | 65.9% |
| 6 | English | On-chain OP_RETURN posts | Technical broadcast | 276,323 | 99.8% |
| 7 | English | Global political comments | Opinion and news discussion | 766,106 | 65.2% |
| 8 | English | Motivational short texts | Community solidarity | 759,236 | 40.3% |
| 9 | English | Daily Bitcoin reports | Automated financial content | 648,791 | 69.4% |

### Parameters
- Collection window: August 30, 2024 to September 14, 2025 (over one year).
- Relays crawled: relay.damus.io, relay.nostr.band, relay.primal.net, nos.lol (four major publicly accessible relays; no authoritative relay registry exists for Nostr, so this is a sample, not a census).
- Event kinds retained: Kind-0, Kind-1, Kind-3, Kind-7, Kind-9735.
- Deduplication rule: within a relay, keep the latest-seen copy of a duplicate event; across relays, keep the earliest-seen copy.
- SBERT model: all-MiniLM-L6-v2, 384-dimensional output.
- Cluster count k = 10, selected via elbow method plus silhouette analysis (range of k tested is not stated in the retrieved text).
- MiniBatch K-means used for cluster assignment; UMAP used only for 2D visualization, with n_neighbors=15, min_dist=0.1, metric=cosine, after PCA reduction from 384 to 50 dimensions.
- Louvain community detection applied to the 378,599-node, 12,068,537-edge directed follow graph.
- Relative density metric: D_r = E / (V log V), with baseline reference D_r = 1.0 used to distinguish high-cohesion from low-cohesion communities in Fig. 6a.

### Stated limitations
The authors state their collection reflects "the historically observable relay layer during the collection window" rather than the entire global Nostr ecosystem, because Nostr has no global state and no authoritative relay registry, and their one-day overlap check found only 72.26% coverage against an independent same-day relay-universe sample — so an unknown fraction of network activity on other relays is absent from every reported figure. The one-year observation window is stated as insufficient to capture longer-term structural and behavioral evolution. Clustering and visualization outcomes are stated to depend on model and parameter choices (embedding model, k, UMAP parameters); the reported Silhouette Coefficient of 0.083 is explicitly called low in absolute terms, attributed by the authors to the continuous and overlapping nature of high-dimensional text semantic space rather than to invalid clustering, but no alternative validation (e.g., held-out labeled data) is reported to substantiate this interpretation. Multimedia analysis is stated to be descriptive and URL-presence-based only, not a structured or multimodal analysis of the media objects themselves, because Kind-1 events lack a uniform structured media field. Zap-engagement differences are interpreted only at the cluster level; the authors explicitly state they do not model post-level sentiment or emotional intensity and therefore do not infer affective mechanisms from the engagement patterns. The paper explicitly declines causal attribution: the two observed 2025 activity surges are only temporally associated with (not causally linked to) publicly documented governance controversies, and the authors state directly that their dataset "does not establish causal attribution." No spam or bot filtering beyond removing empty-content messages was applied, so all reported activity figures include automation-driven signal by design, which the authors state explicitly rather than treating as a defect.

### Requirements it places on the rest of the system
- A measurement or indexing component built on top of Nostr's relay layer needs to query multiple relays and deduplicate by event ID, because the same event is commonly mirrored across relays and no single relay is authoritative; this paper's own pipeline required exactly this deduplication step (latest-within-relay, earliest-across-relay) before any downstream analysis.
- A component inferring "the observable network" from relay data must treat relay selection as a sampling decision with a measurable, non-total coverage rate: this paper's 72.26% one-day overlap figure, on four major relays, is the only quantified figure in this corpus for how much of the live event stream a fixed relay set misses; a coverage claim about a Nostr-based system cannot assume any fixed relay subset sees all events.
- Any component performing social-graph analysis (community detection, trust inference, ranking) over Nostr's follow graph (Kind-3) needs to first separate posting-active users from purely passive or purely-followed accounts, since this paper found 43.31% of the observed 684,394-user population had no follow interaction at all (neither following nor being followed) and had to be excluded from the 378,599-node graph actually analyzed.
- A cross-relay content-discovery or ranking mechanism needs a way to bridge community boundaries deliberately, because this paper's Louvain analysis found only about 12% of follow edges are inter-community and over 80% of those inter-community edges concentrate in just two of 1,385 communities — a design relying on organic inter-community diffusion, without added mechanism, will inherit this near-absence of cross-community connectivity.
- An engagement-weighted ranking or moderation signal built on Zap (Lightning tipping) data needs to account for extreme content-type skew before treating Zap volume as a general quality proxy: this paper found automated/technical content (Clusters 6 and 9) attracted under 2% of total Zap value despite representing over 13% of posts, while affective/identity content attracted a disproportionate share — so raw Zap totals reward social/affective content structurally, independent of informational value.
- A component relying on Nostr's Lightning-Zap layer as an economic signal must accommodate its stated skew toward a small number of high-value transfers ("whale" users); the paper reports this qualitatively (strong skewness in per-transaction Zap value) without a quantified Gini coefficient or percentile breakdown in the retrieved text.

### Contradicts
None found within this corpus against another paper's specific measured figures. The paper is explicitly positioned (per its own bibliography, reference [34]) as an independent check against Wei and Tyson's prior Nostr measurement (arXiv:2402.05709, "An Empirical Analysis of the Nostr Social Network: Decentralization, Availability, and Replication Overhead") on relay concentration and availability; the retrieved text of this paper cites that work only once, in a general statement that "Nostr traffic is concentrated in a small set of relays," without reproducing Wei and Tyson's specific figures for direct numeric comparison — so no side-by-side contradiction or confirmation between the two papers' numbers can be extracted from this text alone. Retrieve WEI-TYSON (arXiv:2402.05709) directly to perform that comparison.

### References worth retrieving
- Competing / independent measurement: Yiluo Wei, Gareth Tyson, "An Empirical Analysis of the Nostr Social Network: Decentralization, Availability, and Replication Overhead," arXiv:2402.05709, 2025 — the prior Nostr relay-concentration and availability measurement this paper is meant to check against; cited once here but not quantitatively compared in the retrieved text.
- Competing: Matteo Zignani, Christian Quadri, Sabrina Gaito, Hocine Cherifi, Gian Paolo Rossi, "The Footprints of a 'Mastodon': How a Decentralized Architecture Influences Online Social Relationships," IEEE INFOCOM Workshops, 2019 — a measurement study of a different decentralized/federated social network (Mastodon) with directly comparable structural-fragmentation findings.
- Competing: G. La Cava, R. Zagaria, M. Stella, "Understanding the growth of the Fediverse through the lens of Mastodon," Applied Network Science 6(1), 2021 — growth-and-structure measurement of another federated social network, useful for cross-protocol comparison of relay/instance concentration.
- Competing: Carlo Alberto Bono, Lucio La Cava, Luca Luceri, Francesco Pierri, "An Exploration of Decentralized Moderation on Mastodon," ACM WebSci 2024 — direct comparison point for the moderation-design discussion in Section 6.2 of this paper.
- Foundational (method): Nils Reimers, Iryna Gurevych, "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks," EMNLP-IJCNLP 2019 — source of the SBERT embedding technique used for all semantic clustering in this paper.
- Foundational (method): Leland McInnes, John Healy, James Melville, "UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction," arXiv:1802.03426, 2018 — the dimensionality-reduction technique used for this paper's cluster visualization.
- Foundational: Nostr Protocol Community, "Nostr: Notes and Other Stuff Transmitted by Relays," GitHub, 2023 — the protocol specification itself.
- Related: Philipp Zabka, Klaus-T. Foerster, Christian Decker, Stefan Schmid, "A centrality analysis of the Lightning Network," Telecommunications Policy 48(2), 2024 — direct source for understanding the Lightning Network structure underlying Nostr's Zap micropayment mechanism.
- Related: Andrea De Salve, Paolo Mori, Laura Ricci, "A Survey on Privacy in Decentralized Online Social Networks," Computer Science Review 27, 2023 — survey covering privacy properties of decentralized social platforms generally, useful for the identity/privacy component of this corpus.

### Verbatim extracts
- "22.3 million user events collected from four major publicly accessible relays"
- "the interaction network remains highly modular and loosely connected"
- "we report this as a relay-layer overlap estimate, not as a full-network coverage claim"
- "Nostr traffic is concentrated in a small set of relays"
- "only 1,408,315 (about 12%) are inter-community ties"
- "the total observed Zap volume is 0.656 BTC"
- "clusters... account for more than 80% of observed Zap activity"
- "our dataset does not establish causal attribution"
- "we do not model post-level sentiment or emotional intensity"
