## [SHI-WWW-25] Centralization in the Decentralized Web: Challenges and Opportunities in IPFS Data Management

**Citation:** Ruizhe Shi, Ruizhi Cheng, Yuqi Fu, Bo Han, Yue Cheng, Songqing Chen. "Centralization in the Decentralized Web: Challenges and Opportunities in IPFS Data Management." ACM Web Conference (WWW), 2025. Pages 4069-4075 (page numbers per running headers in text). DOI: 10.1145/3696410.3714627.
**Retrieved:** full text via https://dl.acm.org/doi/10.1145/3696410.3714627
**Source URL:** https://dl.acm.org/doi/10.1145/3696410.3714627
**Domain:** A

### What it does
This is a longitudinal measurement study of the InterPlanetary File System (IPFS), a decentralized, content-addressed peer-to-peer storage system. The paper measures three properties of IPFS over a three-year window and separately proposes a modified deduplication scheme; only the first two measurement results (replication and centralization) are within this entry's evidence scope.

Data collection: the authors ran a customized IPFS node that accepts unlimited peer connections to passively record all 1-hop Bitswap (IPFS's block-exchange protocol) broadcast traffic, and separately ran two modified Distributed Hash Table (DHT) server peers to log DHT Find_Node traffic, from March 1, 2021 to August 15, 2024. Each logged Bitswap and DHT request records timestamp, sender PeerID and network address, request type, receiver PeerID, and the targeted Content Identifier (CID, IPFS's hash-derived content address).

Replication measurement: a CID-provider mapping is built from the DHT and Bitswap logs, filtered to CIDs identified as complete files or directories by their request pattern (such a CID is typically requested first). Replication level per CID is verified by sending a WANT-HAVE Bitswap message to an assumed provider peer, retried every 4 hours for one week; a peer that never responds is not counted as a valid provider for that CID.

Centralization measurement: two statistical measures are computed weekly across the 3-year trace. Shannon entropy H = −Σp_i·log2(p_i), where p_i is the fraction of all file accesses directed at file i, measures the unpredictability of file-access patterns (lower entropy means access is concentrated on fewer files). The Gini coefficient G = (ΣᵢΣⱼ|xᵢ−xⱼ|)/(2n²x̄), where n is the number of nodes, xᵢ is the amount of data node i stores, and x̄ is the mean stored per node, measures storage-distribution inequality across peers. Both are computed under three stated assumptions: each CID represents one 256 KB storage block (IPFS's default block size); a peer hosting a CID remains active and continues serving it without leaving the network; and a peer announcing multiple IP addresses due to churn is counted as one entity.

### Measured results

| Measurement | Value | Conditions |
|---|---|---|
| Bitswap trace volume | ~21 million requests/day, 1.8 billion unique CIDs total | March 1, 2021 - August 15, 2024, from a single custom-crawler node with unlimited peer connections |
| DHT trace volume | ~1 million requests/day, 120 million unique CIDs total | Same period, 2 virtual DHT peer IDs |
| CID replication (all versions detected) | 214 million CIDs total: 147 million version0, 67 million version1 | Filtered to CIDs identified as complete files/directories |
| CIDs replicated more than once | 29.20% | Same dataset |
| CIDs replicated more than 5 times | 2.71% | Same dataset |
| "Replication wastage" from CID versioning | 18.24 million files hold both a version0 and a version1 CID for the same content | Inflates the apparent count of unique content |
| Average lookup time vs. replication level | 1,817 ms at replication level 1, falling to 397 ms at replication level 20 | IPFS client on a t2.medium AWS EC2 instance (2 vCPUs, 4 GB memory) in central Europe, fetching 1,000 files of 10 MB each at every replication level from 1 to 20 |
| Bitswap success ratio vs. replication level | 73.21% at level 1, rising to 95.09% at level 20 | Same client setup |
| Download throughput vs. replication level | peaks at 14.54 MB/s at replication level 2, then declines as replication level rises further | Same client setup; decline attributed to a rising rate of "request-peer switching" during download |
| Gini coefficient of storage distribution | 0.53 in early 2021, rising to 0.78 by mid-2024 | Weekly measurement across the 3-year trace |
| Share of peers hosting 80% of content | 21.38% of peers at start of measurement period, versus 5% of peers hosting 80.55% of content by the last measured week | Same 3-year trace |
| Cloud-node share of peer population and hosted files | 50.02% of peers / 52.32% of files at start of period, rising to 87.33% of peers / 97.43% of files by end of period | Cloud peers identified by IP address as located in data centers or operating as public gateway nodes |

The paper states its cloud-node share estimate is higher than the estimate in a prior study (Balduf et al., cited as reference [6]), which the authors attribute to that prior study estimating cloud-node share by crawling the DHT and reconstructing network topology, versus this paper's direct measurement from internal Bitswap and DHT traffic.

CID-download load for the (out-of-scope-here) deduplication analysis: spread over a three-week period, generating an average of 55 GB of daily traffic, characterized by the authors as negligible against an estimated over 100 TB of daily traffic on the IPFS network as a whole (that 100 TB estimate is attributed to a cited source [33], not independently measured by this paper).

### Parameters
- CID-provider WANT-HAVE retry interval: every 4 hours, for up to one week, before a non-responding peer is excluded as an invalid provider.
- Storage-block size assumption for centralization analysis: 256 KB per CID, stated as IPFS's default block size.
- Centralization-analysis granularity: weekly aggregation across the 3-year trace.
- Client-side replication-performance test: file size 10 MB, 1,000 files fetched per replication level, replication levels 1 through 20, single client instance type (t2.medium, 2 vCPUs, 4 GB memory), located in central Europe.
- IRB approval obtained for the data collection; IP addresses in the traces anonymized and mapped only to country level.

### Stated limitations
The paper states three of its own centralization-analysis assumptions as simplifications rather than measured facts: that peers hosting a given CID remain continuously active without leaving the network, that every CID maps to exactly one 256 KB block, and that a peer using multiple IP addresses due to churn is treated as a single entity — each assumption, if violated in the underlying network, would bias the Gini-coefficient and entropy figures in an unstated direction. The authors distinguish their study from four prior IPFS-centralization studies (references [6], [10], [27], [38]) by stating those studies are "limited to snapshots of centralization at specific moments," implying (as a claim about those other papers, not independently verified here) that only this paper's three-year trace captures a centralization trend rather than a point estimate. The paper does not attempt any content analysis of downloaded CIDs and deletes all downloaded CIDs immediately after the (out-of-scope) deduplication analysis, so the study does not characterize what content is being centralized, only how many peers host it and how often it is accessed. No hardware, geographic, or network-condition variation is reported for the crawler and DHT-logging nodes themselves (a single crawler node and two virtual DHT peer IDs), so the measured request and CID volumes reflect what one vantage point observed, a scope the paper does not explicitly flag as a limitation but that bears on how the 21-million-requests/day and 1-million-requests/day figures should be read.

### Requirements it places on the rest of the system
This is a measurement paper about an existing deployed system, not a mechanism proposal; it places no design requirement on a system being built. Its results place a requirement on how a design should reason about IPFS-as-a-component: a design that intends to rely on IPFS's DHT- and Bitswap-based content discovery for availability should not assume replication is high by default — the measured 29.20% of CIDs replicated more than once (and only 2.71% more than five times) means a design must either accept this baseline low-availability profile for content addressed only by CID, or add an explicit replication-enforcement mechanism, since IPFS itself does not enforce or reward replication. A design intending to use IPFS as a genuinely decentralized storage layer should account for the measured trend toward peer-population concentration (Gini coefficient 0.53 to 0.78 over three years, cloud-node peer share 50.02% to 87.33%) as a property of the deployed network today, not an assumption to be waived by protocol design alone.

### Contradicts
No numeric conflict with another entry in this corpus is confirmed; SHI-WWW-25 is one measurement in a sequence the brief also asks to compare against Balduf et al. (2023, ACM IMC) and Wei et al. (2024, NSDI), neither of which has a matching entry key in this batch — a comparison entry for either paper is not yet available to check against directly. This paper states its own cloud-node-share estimate is higher than the estimate reported by Balduf et al. [6], attributed by the authors to a difference in measurement method (direct internal-traffic observation here versus DHT-crawl-based topology reconstruction there) rather than to disagreement about the underlying network state.

### References worth retrieving
- competing/independent-measurement: Leonhard Balduf, Maciej Korczyński, Onur Ascigil, Navin V Keizer, George Pavlou, Björn Scheuermann, Michał Król. "The cloud strikes back: Investigating the decentralization of IPFS." ACM Internet Measurement Conference, 2023. (Prior centralization estimate this paper's own figure is directly compared against and found higher.)
- competing/independent-measurement: Yiluo Wei, Dennis Trautwein, Yiannis Psaras, Ignacio Castro, Will Scott, Aravindh Raman, Gareth Tyson. "The Eternal Tussle: Exploring the Role of Centralization in IPFS." USENIX NSDI, 2024.
- foundational (same authors, prior work): Ruizhe Shi, Ruizhi Cheng, Bo Han, Yue Cheng, Songqing Chen. "A Closer Look into IPFS: Accessibility, Content, and Performance." Proceedings of the ACM on Measurement and Analysis of Computing Systems 8(2), 2024.
- foundational: Leonhard Balduf, Sebastian Henningsen, Martin Florian, Sebastian Rust, Björn Scheuermann. "Monitoring data requests in decentralized data storage systems: A case study of IPFS." IEEE ICDCS, 2022. (Source of the crawler methodology this paper's Bitswap logging approach is built on.)
- foundational: Juan Benet. "IPFS - content addressed, versioned, P2P file system." arXiv, 2014. (Original IPFS design.)
- foundational: Petar Maymounkov, David Mazières. "Kademlia: A Peer-to-Peer Information System Based on the XOR Metric." IPTPS, 2002. (Underlies IPFS's DHT.)
- competing: Dennis Trautwein, Yiluo Wei, Yiannis Psaras, Moritz Schubotz, Ignacio Castro, Bela Gipp, Gareth Tyson. "IPFS in the Fast Lane: Accelerating Record Storage with Optimistic Provide." IEEE INFOCOM, 2024. (Content-publication optimization cited as related IPFS-optimization work.)
- foundational: Alfonso De la Rocha, David Dias, Yiannis Psaras. "Accelerating content routing with bitswap: a multi-path file transfer protocol in ipfs and filecoin," cited for the claim that Bitswap now outperforms DHT-based discovery in efficiency.
- attack/critique: Srivatsan Sridhar, Onur Ascigil, Navin Keizer, François Genon, Sébastien Pierre. Content censorship attack exploiting IPFS's decentralized nature, with a proposed detection technique.
- attack/critique: Bernd Prünster, Alexander Marsalek, Thomas Zefferer. "Total Eclipse..." (Eclipse-attack vulnerability of IPFS, cited under IPFS security and privacy.)
- foundational: Erik Daniel, Florian Tschorsch. "Exploring the design space of privacy-..." 2024. (Bitswap-message-traceability privacy work cited as related.)

### Verbatim extracts
- "29.20% of CIDs are replicated more than once, and 2.71% ... more than five times"
- "average lookup time decreases from 1817 ms at a replication level of 1 to 397 ms at a replication level of 20"
- "Gini Coefficient starts at 0.53 ... reaching 0.78 by mid-2024"
- "only 5% of the peers are responsible for hosting 80.55% of the content"
- "cloud nodes comprised 50.02% of the peer set and hosted 52.32% of the files"
- "these figures dramatically increased to 87.33% of the peer set and 97.43% of the total files"
- "limited to snapshots of centralization at specific moments"
