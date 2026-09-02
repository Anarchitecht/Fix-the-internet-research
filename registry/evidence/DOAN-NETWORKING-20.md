## [DOAN-NETWORKING-20] Measuring Decentralized Video Streaming: A Case Study of DTube

**Citation:** Trinh Viet Doan, Tat Dat Pham, Markus Oberprieler, Vaibhav Bajpai. "Measuring Decentralized Video Streaming: A Case Study of DTube." IFIP Networking Conference, 2020. Pages 118-126. DOI: not recorded in registry (candidate URL carries no DOI; IEEE Xplore mirror at https://ieeexplore.ieee.org/document/9142739).
**Retrieved:** full text via https://dl.ifip.org/db/conf/networking/networking2020/1570619852.pdf
**Source URL:** https://dl.ifip.org/db/conf/networking/networking2020/1570619852.pdf
**Domain:** K

### What it does
The paper measures how DTube, a video-sharing platform, performs against YouTube from a mobile client's point of view. DTube stores video content on IPFS (the InterPlanetary File System), a peer-to-peer file system that splits each file into fingerprintable chunks organized as a Merkle tree and lets any peer retrieve a chunk by its content fingerprint rather than a server address. DTube records upload metadata and curation votes on the Steem blockchain rather than on an operator-controlled database. Because most users do not run an IPFS node, DTube operates its own IPFS gateway at video.dtube.top: a browser or app requests a video over ordinary HTTP from that gateway, and the gateway performs the underlying IPFS chunk retrieval on the requester's behalf. Videos uploaded through DTube's web interface enter a private, sandboxed IPFS network reachable only through that one gateway; DTube also lets a user embed videos already present on the public IPFS network by their IPFS hash. The authors built an Android application that streams a fixed sample of trending videos from both YouTube and DTube using the same playout logic (Google's ExoPlayer, one-minute playout, 480p resolution) so the two platforms are measured under one comparable methodology, then compare TCP connect time, startup delay, initial video buffer size, and the IP path length and round-trip time to the serving host.

### Measured results
All figures are 75th-percentile values over the collected sample, split by network type (WiFi or cellular over four ISPs: T-Mobile DE, Vodafone DE, o2 DE, SIMPLE Mobile US) and by platform (YouTube vs. DTube), collected February-November 2019 (10 months) from Germany, Czech Republic, and the United States, across four Android phones (two LG Nexus 5X, one Huawei P9, one Xiaomi Mi A1), on 8,551 total connectivity/performance measurements (2,814 DTube, 5,737 YouTube) and 7,073 successful traceroute measurements out of those.

| Metric | YouTube | DTube | Condition |
|---|---|---|---|
| TCP connect time (75th pct) | 22 ms | 45 ms | WiFi |
| TCP connect time (75th pct) | 44 ms | 107 ms | Cellular, all ISPs pooled |
| TCP connect time (75th pct) | ~30 ms | ~300 ms | Cellular via SIMPLE Mobile (US) only |
| Startup delay (75th pct) | 0.82 s | 3.2 s | WiFi |
| Startup delay (75th pct) | 1.35 s | 5.8 s | Cellular, all ISPs pooled |
| Startup delay (75th pct) | 1.6 s | 9.8 s | Cellular via SIMPLE Mobile (US) only |
| Startup delay (75th pct) | 1-1.8 s (all cellular ISPs) | 3.1-4.6 s (all cellular ISPs except SIMPLE Mobile) | Cellular, per-ISP range |
| Initial buffer size (75th pct) | 8.1 s | 3.7 s (WiFi), 3.0 s (cellular) | Both network types |
| IP path length | within 10 hops for 93.9% (WiFi) / 86.0% (cellular) of traces | within 10 hops for only 4.6% of traces (WiFi); lowest observed cellular path length is 11 hops (29.8% of traces) | traceroute after 1-minute playout |
| IP path length, US only | ~9-10 hops (via SIMPLE Mobile) | 15-20 hops (via SIMPLE Mobile) | US traces |
| Traceroute RTT (66th pct) | 28 ms (WiFi), 76 ms (cellular) | 108 ms (WiFi), 446 ms (cellular) | pooled across ISPs |
| Traceroute RTT (80th pct), cellular per-ISP | 80 ms (T-Mobile, SIMPLE Mobile), 100 ms (o2), 188 ms (Vodafone) | 348 ms (T-Mobile), 502 ms (o2), 1404 ms (Vodafone), 586 ms (SIMPLE Mobile) | per cellular ISP |
| Traceroute success rate | included in 82.7% overall success | included in 82.7% overall success | 7,073 of 8,551 total; T-Mobile 4.5% success, SIMPLE Mobile 59.6%, Vodafone and o2 both >90% |
| Median trending video content duration | 619 s | 323 s | across the full measured sample |

Every traceroute toward a DTube video terminated in autonomous system AS16276 (OVH, France); YouTube traces terminated in Google's AS15169 or in in-ISP caches. This single-location result is a property of DTube's gateway deployment as observed in 2019, not a general property of IPFS.

### Parameters
Video resolution fixed at 480p on both platforms (DTube's default; no adaptive bitrate streaming, since DTube did not support it). Playout duration fixed at 60 seconds per video (a lower bound chosen to cut resource consumption; the cited methodology work recommends at least one minute, preferably three). Initial buffer readiness threshold set to at least 2 seconds of buffered content before playback starts (ExoPlayer STATE_READY). Traceroute timeout: 5 seconds; a traceroute that fails to reach the destination within that window is excluded from the path-length and RTT figures. Sample size per platform: n user-specified trending videos per measurement cycle, drawn from each platform's trending list; total measurements 8,551 (2,814 DTube, 5,737 YouTube).

### Stated limitations
The authors state the DTube figures reflect one specific 2019 deployment, not a property of decentralized video streaming in general: all DTube traffic terminated at one gateway operator (OVH, France), so the measured latency and path-length penalty is a deployment-geography effect, not an IPFS protocol effect. The paper states, as an unverified conjecture rather than a measured claim, that a larger population of participating IPFS peers could improve DTube's lack of geographic distribution, while adding overhead that could raise scalability concerns requiring separate study. The study measured DTube's private, sandboxed IPFS network reachable only through DTube's own gateway, not the public IPFS network; the authors state that file retrieval behavior on the public network might differ. The authors explicitly excluded DTube's blockchain-based incentive mechanism from analysis, restricting the study to connectivity metrics. Cellular data collection stopped in July 2019, so 10-month coverage applies fully only to the WiFi measurements after that point. DTube's IPFS-hosted videos frequently failed to load in the study period, which is why roughly twice as many YouTube videos as DTube videos were successfully measured — a nonrandom subset of DTube content is reflected in the results. The authors state as future work that they did not collect TCP packet traces and did not measure PeerTube or public-network IPFS videos.

### Requirements it places on the rest of the system
A gateway-based content-addressed retrieval design requires the gateway operator to be reachable at low network-path length from the client, or startup delay and RTT degrade severely for clients geographically far from that operator (measured here as a 4x startup-delay penalty and 7-8 additional IP hops when the only gateway sits on another continent from the client). A system that isolates its object namespace behind one private network segment (DTube's sandboxed IPFS instance) forfeits the retrieval-diversity benefit that a content-addressed, multi-peer-source design is meant to provide, because every request still resolves to the single operator's own IPFS peers rather than to any holder of the content. For a content-addressed video system to avoid this failure mode, it needs either multiple independently operated gateways at diverse network locations, or a client capable of resolving content hashes directly against the public swarm rather than through one fixed HTTP gateway.

### Contradicts
None found within this corpus. This paper's finding that DTube's decentralized architecture produced a de facto single point of geographic centralization is consistent with, and cited by later, the independent finding for Mastodon in Raman et al. (cited in this paper's own bibliography as reference 33) that decentralized platforms concentrate around a small number of operators.

### References worth retrieving
- Benet, "IPFS - Content Addressed, Versioned, P2P File System," CoRR, 2014, arXiv:1407.3561 — foundational (defines the content-addressing and chunk-Merkle-tree mechanism DTube is built on)
- Raman, Joglekar, De Cristofaro, Sastry, Tyson, "Challenges in the Decentralised Web: The Mastodon Case," ACM IMC 2019, DOI 10.1145/3355369.3355572 — competing/parallel (independent measurement of centralization emerging inside a different decentralized platform)
- Ascigil, Reñé, Król, Pavlou, Zhang, Hasegawa, Koizumi, Kita, "Towards Peer-to-Peer Content Retrieval Markets: Enhancing IPFS with ICN," ACM ICN 2019, DOI 10.1145/3357150.3357403 — competing (proposes an alternative IPFS retrieval mechanism)
- Li, Lin, Akodjenou, Xie, Kaafar, Jin, Peng, "Watching Videos From Everywhere: A Study of the PPTV Mobile VoD System," ACM IMC 2012, DOI 10.1145/2398776.2398797 — foundational (prior peer-assisted VoD measurement methodology)
- Zou, Wang, Ge, Tian, "Peer-Assisted Video Streaming With RTMFP Flash Player: A Measurement Study on PPTV," IEEE TCSVT 2018, DOI 10.1109/TCSVT.2016.2601962 — competing (measured peer-assisted, not content-addressed, video delivery)

### Verbatim extracts
"DTube aims to prevent having a single point of control by using the aforementioned decentralized solutions instead."
"all traceroute measurements toward DTube end in AS16276, managed by OVH (FR)"
"75th percentile for WiFi measurements to YouTube is at 22 ms (cellular 44 ms)... 45 ms for DTube (cellular 107 ms)"
"75% of the measured YouTube videos require up to 0.82 seconds to start, whereas 75% of the DTube videos require up to 3.2 seconds"
"only around 7.1k traceroute measurements out of the 8.5k measurements overall are successful, i.e., a failure rate of 17.3%"
"DTube lacked the distribution and accessibility of reliable content servers globally, indicating geographical centralization"
