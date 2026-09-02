## [COSTA-DAIS-23] Studying the Workload of a Fully Decentralized Web3 System: IPFS

**Citation:** Pedro Ákos Costa, João Leitão, Yiannis Psaras. "Studying the Workload of a Fully Decentralized Web3 System: IPFS." IFIP DAIS, 2023. DOI 10.1007/978-3-031-35260-7_2.
**Retrieved:** full text via https://arxiv.org/abs/2212.07375 (arXiv preprint, dated December 15, 2022; identical in scope and figures to the published DAIS proceedings paper this key cites)
**Source URL:** https://arxiv.org/abs/2212.07375
**Domain:** J

### What it does

The paper characterizes real request traffic and content-provider location for InterPlanetary File System (IPFS), a content-addressed peer-to-peer storage network, by passively collecting HTTP access logs from a public IPFS gateway and actively querying the IPFS Distributed Hash Table (DHT) for the peers holding each requested piece of content. IPFS identifies content by a content identifier (cId), a hash of the content's bytes. A gateway is an IPFS node that also runs a web server, letting a browser fetch IPFS content over ordinary HTTP without running an IPFS client. The authors extracted every valid GET request's cId from two weeks of gateway logs, then wrote a libp2p program (libp2p is the peer-to-peer networking library IPFS is built on) that issues a FindProviders DHT call for each distinct cId to discover which peers currently hold it. They joined the resulting request-frequency data and provider-location data, using the MaxMind GeoLite2 database to map IP addresses to geographic regions, to produce a combined view of where content is requested from and where it is served from.

### Measured results

| Measurement | Figure | Conditions |
|---|---|---|
| Request volume processed | 123,959,912 total log entries; 58,869,788 (47.49%) classified as valid GET requests with a resolvable cId, after removing 0.001% out-of-format entries, 19.60% non-GET requests, and a further 41% of GET requests that either failed (17%, HTTP 400) or carried no cId (24%) | Gateway ipfs.io, two weeks of logs, March 7 to March 21, 2022 |
| Distinct content requested | 4,009,575 distinct cIds requested, drawn from the 58,869,788 valid GET requests | Same trace |
| Provider discovery success rate | Providers located for 45.74% of requested cIds (1,833,967 of 4,009,575); no provider found for the remaining 54.26% | DHT queries performed some months after the requests were logged; the paper attributes non-location partly to content no longer being available |
| Providers discovered and addressed | 55,830 distinct provider peer IDs found; 59% initially had no address information (the peer that holds the provider record had received no traffic from that provider in a 30-minute window and treated the address as stale); a follow-up DHT query for the missing addresses recovered 4,024 more (a 7% increase over the initial address count) | Same DHT-query process |
| Geo-location coverage | All requester IP addresses resolved to a location; 88% of addressed providers resolved to a location via MaxMind GeoLite2 | Same dataset |
| DHT provider-record query latency | Average latency about 6 seconds; maximum latency up to 1.5 hours | Measured while resolving all 4,009,575 distinct cIds through parallelized DHT queries; full resolution took around 40 hours; a batch of 100 parallel provider-finding queries produced almost 10,000 network packets per minute |
| Gateway request rate | Average over 150,000 requests per hour; peak near 275,000 requests per hour; a roughly 9-hour outage observed on 2022-03-14 | Two-week trace, hourly aggregation |
| Request origin by region | North America and Asia each average more than 75,000 requests per hour; Oceania averages about 2,500/hour; Europe about 85/hour; Africa about 57/hour; South America about 3/hour | Same two-week trace, aggregated by continent of requester IP |
| Request concentration across content (Zipf-shaped) | Almost 50% of distinct cIds requested exactly once; about 90% requested at most 10 times; about 99% requested at most 100 times | ECDF over all 4,009,575 distinct cIds and their request counts |
| Top single cId request count | 482,620 requests to the single most-requested cId | Top-10 table; the paper states most of the top 10 most-requested cIds carry Non-Fungible Token (NFT) related data |
| Content replication | About 70% of all cIds are held by at most 2 provider peers (replication factor of at most 2); the top-10 most-replicated cIds are mostly IPFS documentation pages, not the top-10 most-requested cIds, and the most-replicated of the top-10 requested cIds has only 29 providers, the second-most has 28 | Same joined request/provider dataset |
| Provider concentration | 60% of providers serve only a single distinct cId; fewer than 10% of providers serve at least 10 distinct cIds; a small proportion serve at least 1,000 distinct cIds; the top single provider serves 869,734 distinct cIds | Same dataset; the paper attributes the largest providers to pinning services such as nft.storage, identified from DNS-resolved multiaddresses |
| Provider geo-distribution | North America: 10,983 providers; Europe: 5,789; Asia: 4,959; Oceania: 431; South America: 104; Africa: 40; Antarctica: 1; relay-only (no public address, behind NAT): 2,473; location unknown: 689 | Table of all 55,830 addressed and unaddressed providers by continent |
| Request-to-provider region correlation | Requests from every region are served predominantly by North American providers (roughly 48-54% of that region's requests) and European providers (roughly 25-30%); requests originating from Africa and South America matched to zero identified providers in every destination region in the reported heatmap | Normalized per-origin-region percentages, computed by joining request-origin and provider-location data |

### Parameters

- Trace window: two weeks, March 7 to March 21, 2022, from a single gateway (ipfs.io) located in North America.
- Provider-record staleness window used by the IPFS DHT (not set by the authors, but observed and reported): 30 minutes of no traffic from a provider before the peer holding its provider record drops the address.
- Parallel DHT query batch size used by the authors' measurement tool: 100 queries in parallel, chosen empirically to keep resolution time tractable, generating close to 10,000 packets per minute at that setting.

### Stated limitations

The authors state their provider-discovery step ran some months after the requests were logged, so the 54.26% of cIds for which no provider was found may reflect content that was available at request time but has since left the network, not necessarily unavailability at the time of the original request. They state MaxMind GeoLite2 is an incomplete database, leaving 12% of addressed providers without a resolvable location. They state a provider observed at multiple locations, plausibly through VPN use, is assigned only its last-observed location, and note this affects a small enough number of cases to not materially change the results. They state their study observes only traffic passing through the public IPFS gateway used for the trace and does not include Bitswap traffic (the peer-to-peer content-exchange protocol operating inside the IPFS network, as opposed to the gateway's external HTTP interface), and mark integrating Bitswap-level observation as future work. They state the observed low replication (about 70% of content held by at most two providers) follows from IPFS requiring an explicit re-provide action by a node after it fetches a copy, so replication does not happen automatically as a side effect of being served, and they state this design produces limited high availability through replication. They state that because IPFS provider records are stored on the DHT at peers determined by the content identifier's hash rather than by which peers hold copies of the content, adding more providers for popular content does not spread the DHT lookup load for that content's provider records across more DHT peers, since the same responsible peers keep serving the lookups.

### Requirements it places on the rest of the system

None as a positive mechanism — this paper is a measurement study of a system it does not modify. What it establishes as required background for interpreting these figures: the measurements assume the IPFS DHT correctly resolves FindProviders queries to the peers currently advertising a cId, and that gateway logs faithfully record every client-facing HTTP request; a provider count or replication figure is only as accurate as those two channels. The paper's own critique of IPFS is relevant to any design considering DHT-based provider records for popular content: because a content identifier's hash fixes which DHT peers store its provider record regardless of how many nodes replicate the content itself, a content-location index built this way needs a separate mechanism to spread load for popular items' metadata, since replicating the content does not by itself replicate the metadata's lookup path.

### Contradicts

None found within this corpus. This entry supersedes any earlier citation of this paper's average and maximum DHT-lookup-latency figures that did not carry the two-week gateway-trace and 4,009,575-cId-resolution conditions stated above; those figures (about 6 seconds average, up to 1.5 hours maximum) are reproduced here with their conditions attached.

### References worth retrieving

- Trautwein, Raman, Tyson, Castro, Scott, Schubotz, Gipp, Psaras, "Design and evaluation of IPFS: A storage layer for the decentralized web," ACM SIGCOMM 2022 — foundational (the primary IPFS system-design and evaluation paper this workload study builds on).
- Balduf, Henningsen, Florian, Rust, Scheuermann, "Monitoring data requests in decentralized data storage systems: A case study of IPFS," IEEE ICDCS 2022 — competing/independent-measurement (an independent IPFS traffic study the paper cites as corroborating its North America provider-concentration finding).
- Henningsen, Florian, Rust, Scheuermann, "Mapping the interplanetary filesystem," IFIP Networking 2020 — foundational/independent-measurement; the paper states its own findings confirm this earlier peer-location mapping study.
- Pouwelse, Garbacki, Epema, Sips, "The BitTorrent P2P file-sharing system: Measurements and analysis," IPTPS 2005 — competing (the paper cites this as reference [23] once, correctly, for active measurement of BitTorrent upload/download speeds; the paper's related-work section later reuses the same [23] marker to describe a different, unnamed study of Bitswap traffic and its effect on privacy — this second use does not match the bibliography entry for [23], an internal citation error in the source text; retrieve the actual Bitswap-privacy study under its own title rather than relying on this paper's citation number).
- Sen, Wang, "Analyzing peer-to-peer traffic across large networks," ACM SIGCOMM IMW 2002 — foundational/independent-measurement (ISP-level measurement of FastTrack, Gnutella, and DirectConnect traffic; the paper states this earlier study found the same small-fraction-of-hosts-dominates-traffic pattern it reports for IPFS).
- Maymounkov, Mazières, "Kademlia: A peer-to-peer information system based on the XOR metric," IPTPS 2002 — foundational (the DHT design IPFS's provider-record storage is built on; already noted as a verified seed in the brief).
- Benet, "IPFS - Content Addressed, Versioned, P2P File System," Technical Report Draft 3, 2014 — foundational (the original IPFS design document).
- de la Rocha, Dias, Psaras, "Accelerating content routing with Bitswap: A multi-path file transfer protocol in IPFS and Filecoin," technical report, 2021 — foundational (Bitswap, the in-network content-exchange protocol this paper explicitly leaves unmeasured).

### Verbatim extracts

- "the average latency was about 6 seconds, with the maximum latency reaching up to 1.5 hours"
- "almost half of all cIds are only requested once"
- "almost 70% of all cIds in the system are replicated at most twice"
- "60% of providers only provide a single cId"
- "there needs to be an explicit (re)provide action by the user"
- "the records will still be stored in the same peers of the DHT"
