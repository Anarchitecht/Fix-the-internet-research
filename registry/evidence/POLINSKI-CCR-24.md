## [POLINSKI-CCR-24] The Centralization of a Decentralized Video Platform: A First Characterization Of PeerTube
**Citation:** Michael Polinski, Richard Jo, Kevin McAfee, Fabián E. Bustamante. "The Centralization of a Decentralized Video Platform: A First Characterization Of PeerTube." ACM SIGCOMM Computer Communication Review, Volume 54 Issue 4, October 2024. Pages 26-34. DOI 10.1145/3717512.3717516.
**Retrieved:** full text via https://doi.org/10.1145/3717512.3717516
**Source URL:** https://doi.org/10.1145/3717512.3717516
**Domain:** K

### What it does
The paper measures deployed infrastructure and content distribution on PeerTube, an existing
federated video-hosting system built on ActivityPub, without modifying it. PeerTube lets a user
upload a video to one home server ("instance"), which becomes that video's origin instance and
retains authoritative control over the video, its comments, and its view count. Any other instance's
administrator may configure a "redundancy" policy naming source instances to mirror from and a
caching strategy (most-viewed, most-recently-added, or most-actively-trending videos) subject to a
storage quota; an instance following that strategy copies full video files from the origin instance
and serves them itself as a "caching instance," which is PeerTube's video redundancy mechanism.
Separately, one instance "following" another (a unidirectional relation reported to the origin
instance under ActivityPub) causes the followed instance's videos to be listed and discoverable
through the follower's search interface, without implying any file copy. Clients stream video over
HTTP Live Streaming (HLS), and the first-party client additionally forms a peer-to-peer swarm with
other simultaneous viewers of the same video over WebTorrent or peer-to-peer HLS; PeerTube v6
removed WebTorrent in favor of HLS over WebRTC.

The authors crawled the PeerTube instance graph starting from Framasoft's public instance tracker,
recursively following each instance's REST API-exposed "following"/"followed-by" lists, over roughly
30 hours in August 2024. They geolocated instance IP addresses using MaxMind GeoIP, ipinfo.io, and
RIPE IPmap, and resolved each instance's IPv4 addresses to an autonomous system (AS) number via
RIPEstat's API. From the per-instance video-metadata API responses, they built a UUID-keyed table of
unique videos, recording for each video its listing factor (the number of instances that list it,
counting both origin and mirrored listings) as an upper bound on its redundancy factor, and, for the
88% of instances that expose valid HLS streaming-source lists, a directly computed redundancy factor
(the count of unique streaming hosts, origin plus caching instances, for that video).

### Measured results

| Finding | Figure | Conditions |
|---|---|---|
| Live PeerTube instances discovered | ~1,200 | Crawl of the instance-follow graph starting from Framasoft's tracker (>1,000 listed instances), August 2024, ~30-hour crawl duration; excludes unreachable instances |
| Instances with open public registration | ~19% | Same crawl, from instance configuration objects |
| Instances running the latest major PeerTube version | 70% | Same crawl; only 14% were more than one major version behind, 42% ran the latest minor release |
| Top-3-country instance share (Germany, USA, France) | ~69.5% (24.5% + 23.2% + 21.8%) | Geolocation by ipinfo.io of all discovered instances (Table 1) |
| Country geolocation disagreement across the three geolocation sources | all three disagree on 1% of addresses; two of three disagree on 17% | MaxMind GeoIP, ipinfo.io, RIPE IPmap cross-compared over discovered instance IPs |
| Instance share on top 15 ASes | 62% | RIPEstat AS resolution of discovered instance IPv4 addresses; IPv6 excluded because fewer than half of instance hostnames carry an AAAA record |
| Instance share on top 7 ASes | over 50% | Same AS resolution |
| Instance share on top 5 ASes | 45% | Same AS resolution (Table 2) |
| Top single AS (Hetzner Online GmbH) instance share | 17.5% | Same AS resolution |
| Videos listed on 3 or fewer instances | 80% | Listing-factor computed from the UUID-keyed video dataset, August 2024 crawl |
| Videos listed on 6 or fewer instances | 95% | Same dataset |
| Videos stored with no inter-instance redundancy (single copy) | over 92% | Redundancy factor computed from HLS streaming-source lists, over the 88% of instances exposing valid streams |
| Unique videos discovered | 872,653 | Full crawl, August 2024 |
| Total views across all discovered videos | 124,172,763 | Same crawl; per-video view count taken as the highest value observed across repeated crawler visits to that video, because visits occur at different times during the ~30-hour crawl |
| Share of total views held by the 5 most-viewed videos | over 3% | Same view dataset |
| Videos with zero reported views | 305,282 | Same view dataset (out of 872,653) |
| Total likes / average likes per video | 264,393 / 0.30 | Same crawl |
| Total dislikes / average dislikes per video | 13,725 / 0.016 | Same crawl |
| Multihomed instance IP addresses (advertised by more than one AS) | 4 | Same AS resolution |
| Video publication growth trend | quadratic year-over-year, Jan 2018-Aug 2024 | Publication-date field of listed videos still present at crawl time; historical videos removed from all instances are excluded, so the trend understates true historical volume |

### Parameters
| Parameter | Value used |
|---|---|
| Crawl seed | Framasoft's public PeerTube instance tracker |
| Crawl duration | ~30 hours, August 2024 |
| Geolocation sources | MaxMind GeoIP, ipinfo.io, RIPE IPmap (result reported from ipinfo.io) |
| AS resolution source | RIPEstat API, queried on DNS-resolved IPv4 addresses only |
| Redundancy-factor computation scope | 88% of instances (those exposing valid HLS streaming-source lists with redundancy URLs) |
| Per-video view/like count aggregation | maximum value observed across repeated crawler visits within the crawl window |
| Caching strategies PeerTube exposes to administrators | most-viewed, most-recently-added, most-actively-trending (administrator picks one or more, each under its own storage quota) |

### Stated limitations
The authors state their crawl, which follows the instance-follow graph recursively from the tracker's
seed list, discovers only the "main" connected component of the instance graph and may miss smaller
connected components not reachable from it; they argue such components are better analyzed as
private video-sharing servers or forums rather than as part of the PeerTube federated network proper.
They state it is impossible to give an exact instance count at any moment because of nonzero churn
and because some instances are misconfigured or temporarily unresponsive. They state the listing
factor is only an upper bound on the true redundancy factor, because listing another instance's video
does not by itself imply a local copy exists; they compute a directly measured redundancy factor only
for the 88% subset with usable HLS stream data. They state they lack historical crawl data, so the
video-production growth trend excludes any video that was published and later removed from every
instance, which understates true historical publication volume. They state some crawled videos may
be spoofed listings returned by instances (metadata for nonexistent videos), which they did not
inspect for. They attribute the cause of the observed AS concentration — cloud hyperscalers such as
AWS and GCP being nearly absent — to a lack of competitive outbound-bandwidth pricing relative to
providers like OVHCloud and Scaleway, stated as the authors' inference rather than as a measured fact.

### Requirements it places on the rest of the system
PeerTube's redundancy mechanism requires a per-instance administrator to opt in explicitly by
configuring a redundancy strategy and a storage quota; no redundancy occurs by default. It requires
the origin instance to remain the sole authoritative holder of a video's mutable state — comments,
view count — even after other instances hold full copies of the video bytes, so any consumer of view
or comment data must query the origin instance rather than a caching instance for correctness. The
listing mechanism (instance-follow) is independent of the redundancy mechanism: a follower instance
can list and make discoverable a video it holds no copy of, so any component using listing count as a
proxy for availability or fault tolerance will overstate both, as the paper's own listing-factor/
redundancy-factor gap demonstrates. The instance-follow relation is unidirectional and each follow
and mirror event is reported back to the origin instance under the ActivityPub protocol, so any
external measurement of the federation graph depends on cooperating instances correctly implementing
that reporting. AS-level geolocation and hosting-concentration measurement of this kind depends on
DNS resolution succeeding for IPv4 (this study excluded IPv6 because fewer than half of instance
hostnames carried an AAAA record) and on the accuracy of third-party geolocation databases, which the
paper shows disagree with each other on a nontrivial fraction of addresses (17% two-source
disagreement).

### Contradicts
None found within this corpus. The paper's own conclusion states this is "the first characterization
of PeerTube," a claim the paper supports directly rather than one to check against another source.

### References worth retrieving
- **Raman, Joglekar, De Cristofaro, Sastry, Tyson, "Challenges in the decentralized web: The mastodon case," 2019** — foundational/competing measurement of the sibling Fediverse platform Mastodon, cited [34]; already in this corpus family (cited by LIU-PACMHCI-25 as well).
- **Trautwein, Raman, Tyson, Castro, Scott, Shubotz, Gipp, Psaras, "Design and evaluation of IPFS: a storage layer for the decentralized Web," 2022** — foundational, cited [39]; describes the storage system PeerTube's authors propose as a future redundancy backend.
- **Balduf et al., large-scale measurement study of IPFS** — competing measurement, cited via [10]; reports ~80% of IPFS DHT servers hosted in the cloud with the top three cloud providers holding nearly 52% of all servers, a directly comparable centralization figure for a different content-addressed decentralized storage system.
- **Viet Doan, Pham, Oberprieler, Bajpai, "Measuring decentralized video streaming: a case study of dtube," IFIP Networking 2020** — competing measurement of DTube, an IPFS/Steem-blockchain-backed video platform, cited [19]; measures end-user streaming performance and reports the IPFS-HTTP-gateway "CDN" caching model as potentially competitive with centralized services.
- **He, Bin Zia, Castro, Raman, Sastry, Tyson, "Flocking to mastodon: Tracking the great twitter migration," 2023** — foundational/competing Fediverse-migration measurement, cited [27].
- **La Cava, Greco, Tagarelli, "Understanding the growth of the Fediverse through the lens of Mastodon," Applied Network Science 6(64), 2021** — foundational, cited [18]; already flagged from LIU-PACMHCI-25's bibliography as well.
- **Rhea, Geels, Roscoe, Kubiatowicz, "Handling churn in a DHT," 2004** — foundational churn-measurement methodology, cited [35].
- **Stutzbach, Rejaie, "Understanding churn in peer-to-peer networks," 2006** — foundational churn-measurement methodology, cited [36].

### Verbatim extracts
"over 92% of videos are stored without any inter-instance redundancy" (abstract).
"most videos (80%) are listed across 3 or fewer instances" (Section 5.1).
"over 50% of instances are hosted by the 7 most popular ASes" (Section 4.2).
"70% of instances...were running the latest major version" (Section 4.1).
"it is virtually impossible to state an exact total count of PeerTube instances" (Section 4.1).
"our listing factor is an upper bound on the redundancy factor" (Section 3, Video Metadata).
