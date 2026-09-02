## [TANG-ARXIV-22] Stealthy Peers: Understanding Security Risks of WebRTC-Based Peer-Assisted Video Streaming
**Citation:** Siyuan Tang, Eihal Alowaisheq, Xianghang Mi, Yi Chen, XiaoFeng Wang, Yanzhi Dou. "Stealthy Peers: Understanding Security Risks of WebRTC-Based Peer-Assisted Video Streaming." arXiv preprint, 2022. DOI 10.48550/ARXIV.2212.02740.
**Retrieved:** full text via https://arxiv.org/abs/2212.02740
**Source URL:** https://arxiv.org/abs/2212.02740
**Domain:** K

### What it does
The paper measures deployed WebRTC-based peer-assisted delivery network (PDN) services — commercial
add-ons video-streaming websites and apps embed to offload video-segment delivery from their CDN
(content delivery network) onto viewers' own browsers, which form a peer-to-peer swarm over WebRTC
— and demonstrates four attacks against the observed deployments, without modifying WebRTC, ICE
(Interactive Connectivity Establishment), or any PDN provider's software.

Discovery pipeline: the authors identified 3 commercial PDN providers (Peer5, Streamroot, Viblast)
by observing their traffic patterns, then built a signature-based scanner (URL patterns, unique
namespaces, Android-manifest metadata) to detect customers automatically. The scanner crawled 68,757
candidate video-related domains (drawn from the top 300K Tranco-ranked domains, filtered by
VirusTotal category engines for "tv"/"media" labels, plus 44 domains found via source-code search
engines) using Selenium between January and February 2022, and separately unpacked a random 1.5
million-APK sample from Androzoo's Android-app corpus to detect mobile PDN customers by the same
signatures.

Attack 1, service free riding: a PDN customer authenticates to the provider with a static API-key
token embedded in client-side JavaScript or app code; an attacker extracts a legitimate customer's
token (by static analysis or from a colluding peer) and impersonates that customer to the PDN
service, generating billable traffic under the victim customer's account. The authors built a proxy
that redirects a whitelisted victim domain's traffic through an attacker-controlled test website,
tricking a viewer's client into sending an authenticated request that appears to originate from the
whitelisted domain, which defeats domain whitelisting as an authentication defense.

Attack 2, video segment pollution: PDN caches downloaded video content in browser memory (purged
after a short interval, protected by the browser same-origin policy) and PDN servers verify a peer's
membership in a swarm by consistency with the video's manifest file, not by verifying the content
itself. The authors ran an HTTPS proxy between a controlled peer and the real CDN that substitutes
altered video-segment files while leaving the manifest file untouched, then observed the altered
content propagate over the DTLS (Datagram Transport Layer Security) channel to other peers in the
swarm.

Attack 3, peer IP leak: to locate download sources, a PDN peer requests from the PDN server a list of
candidate peers watching the same stream, then exchanges WebRTC ICE binding requests directly with
each candidate to test connectivity; the binding-success response carries the peer's real public IP
address and port in plaintext, exposing it to every candidate peer regardless of mutual trust. The
authors instrumented a controlled peer to capture these STUN/ICE binding exchanges and recover peer
IP addresses from live traffic to two PDN customers.

Attack 4, resource squatting: the authors instrumented Docker containers running a browser web driver
against a PDN-integrated test page, and used the Docker Engine API to sample per-second CPU, memory,
and network I/O, comparing a peer participating in the PDN swarm against a peer receiving the same
video directly from CDN with PDN disabled.

### Measured results

| Finding | Figure | Conditions |
|---|---|---|
| PDN customers detected | 134 websites, 38 Android apps (627 distinct APK versions) | Signature scan of 68,757 candidate domains (Selenium, Jan-Feb 2022) plus 1.5 million randomly sampled APKs from Androzoo's ~8 million-app June 2022 corpus |
| PDN customer breakdown by provider | Peer5: 60 websites / 31 apps; Streamroot: 53 websites / 6 apps; Viblast: 21 websites / 1 app | Same scan |
| PDN customer popularity | 92 of 105 websites with obtained traffic data (69%) exceed 1 million monthly visits; 19 exceed 10 million monthly visits; 25 of 35 apps with obtained data (66%) exceed 1 million downloads; 9 exceed 10 million downloads; 1 app exceeds 100 million downloads | SimilarWeb (websites) and Google Play (apps) lookups on the 134/38 detected customers, of which 105 websites and 35 apps had available data |
| API keys extracted from detected customers | 44 total (36 Peer5, 7 Viblast, 1 Streamroot); 40 confirmed valid | Static/dynamic extraction against the 134-website/38-app customer set |
| Customers vulnerable to service free riding | 11 of 40 valid API keys (18 customers, all belonging to Peer5) | Free-riding feasibility test performed on the extracted keys; free trial obtained from Peer5 and Viblast (Streamroot declined the request), both found vulnerable to domain-whitelist spoofing when tested with the trial account |
| Video segment pollution test outcome | both Peer5 and Viblast failed to detect substituted video segments when the manifest file was left unmodified | Two-peer test on the authors' own PDN-integrated test website with free-trial SDK access; Streamroot and private PDN services were not tested for this attack |
| Peer IPs recovered | 7,740 unique peer IP addresses total: 7,055 from Huya TV, 685 from RT News | Two-hour daily traffic capture from a controlled peer in a live channel, for 7 consecutive days, against two customers (Huya TV, a private-PDN website; RT News/com.rt.mobile.english, a Streamroot-integrated app) |
| Recovered-IP validity breakdown | 7,159 public IPs, 581 bogon IPs (543 private-network, 33 NAT, 5 reserved) | Same capture, IPInfo geolocation lookup |
| Geographic concentration of recovered IPs | 98% of Huya TV's public IPs are in China; RT News's public IPs span 259 cities in 56 countries, top 3 being United States (35%), Britain (17%), Canada (13%) | Same capture |
| Resource overhead from PDN participation (Peer5) | +15% CPU, +10% memory versus no-peer (direct CDN) baseline | Docker-container resource sampling, two peers (Peer A, Peer B) simultaneously watching the same stream via the authors' PDN-integrated test website, over a ~600-second window |
| Upload traffic growth with peer count | up to 200% of download traffic at 3 peers (versus 0 peers) | Same test setup, varying the number of additional peers from 0 to 3, Peer5 SDK; CPU, memory, and download traffic show no significant change across this range, attributed by the authors to WebRTC's connection scalability; Viblast tests reported similar results without separate figures given |
| Peer5 customer configuration audit | of 47 detected Peer5 customers (36 extracted API keys), 33 enable PDN for all viewers, 14 disable it (deployment=0); of the 33 enabled, 3 Android apps allow cellular data for both upload and download ("full" mode), the remaining 30 restrict cellular to download only ("leech" mode) | Extracted from an unprotected client-side configuration variable Peer5 exposes in its JavaScript, cross-referenced against the 47 customers whose keys were recoverable |
| Consent disclosure to viewers | 0 of 134 websites, 38 apps, and 9 private PDN cases provide a consent pop-up or documented notice of P2P participation | Manual inspection of all detected customers' services and public documentation |
| JWT (JSON Web Token) mitigation-token overhead | 283-byte encoded token including an HMAC-SHA256 signature; extra latency under 80 ms | Authors' own proposed disposable, video-bound authentication token, tested in the authors' PDN analyzer under a simulated environment (peer-assisted integrity-checking overhead detailed in the paper's Appendix 9.3) |
| PDN traffic offload claimed by providers | at least 50% of video traffic offloaded from origin infrastructure to PDN peers, per provider marketing materials | Provider-stated figures (Peer5, Streamroot, Viblast documentation), not independently measured by the authors in this paper |
| Passive-DNS popularity proxy (average daily resolutions to each provider's backend domain, 2018-2021) | Peer5: 48,124 (2018) -> 22,153 (2021); Streamroot: 32,824 (2018) -> 36,806 (2021); Viblast: 231 (2018) -> 391 (2021) | Farsight Security passive-DNS query volume against each provider's backend server domain, four-year window |

### Parameters
| Parameter | Value used |
|---|---|
| Candidate domain pool | 68,757 (68,713 from Tranco top 300K filtered by VirusTotal category engines to "tv"/"media" labels, plus 44 from NerdyData/PublicWWW source-code search) |
| Website crawl tool / rate / depth / timeout | Selenium; 1 webpage per 3 seconds; subpage crawl depth 3; 10-minute timeout per domain |
| Website scan window | January-February 2022 |
| Android APK sample size / source | 1.5 million randomly sampled from Androzoo's ~8 million distinct apps (19,661,675 APKs as of June 2022) |
| IP-leak capture duration | 2 hours per day, 7 consecutive days, per customer, against 2 customers (Huya TV, RT News) |
| Resource-squatting test window | ~600 seconds per run, sampled once per second via Docker Engine API |
| Peer count varied in upload-traffic test | 0, 1, 2, 3 additional peers |
| Proposed defense token fields | customer_id, pdn_peer_id, video_ids, timestamp, ttl, usage_limit; example instance signed with HMAC-SHA256 |
| Prior baseline cited for content-pollution propagation speed in P2P live streaming | 47% of viewers reached in the initial propagation stage even with few initial polluters (cited from Wang, Chen, Wang, Chan, IET Communications 2018 [71], not independently reproduced in this paper) |
| Prior baseline cited for P2P video opt-in rate | ~30% of video viewers opt in to P2P participation when asked (cited from a prior large-scale study [77], not independently reproduced in this paper) |

### Stated limitations
The authors state their PDN-provider detection may miss providers that are proprietary or of low
public visibility, and that this limitation also applies to their signature-based customer detector,
which they state is not robust against code obfuscation; they state some domains matching their
signatures may not actually have PDN enabled at runtime. They state they were unable to evaluate the
free-riding and video-segment-pollution attacks against Streamroot (which declined their free-trial
request) or against the private PDN services they identified, so it remains unconfirmed whether those
two attacks succeed against those deployments. They state that, without access to PDN provider
servers, it is impossible to determine whether these risks have already been exploited by attackers
against real-world PDN traffic. The authors state their proposed mitigations were evaluated only in a
simulated environment within their own PDN analyzer framework, not against production PDN
infrastructure. For the peer IP-leak mitigation (restricting candidate peers to the same country or
ISP), the authors state this is only a heuristic that an attacker can bypass using a proxy peer, and
that it may degrade the quality of service a legitimate peer-assisted delivery achieves.

### Requirements it places on the rest of the system
The demonstrated attacks depend on specific, named properties of the PDN designs studied, not on
peer-assisted delivery generically: (1) service free riding requires the provider to authenticate
customers with a long-lived, statically embedded API key rather than a short-lived, stream-bound
token — the authors' proposed fix requires each token to carry a customer ID, peer ID, a specific
video-ID list, an issuance timestamp, a time-to-live, and a usage-limit field, cryptographically
signed, which in turn requires the video website's server and the PDN server to share a key in
advance; (2) video segment pollution requires the PDN server to validate a peer's swarm membership
by manifest-file consistency without independently validating segment content — the authors'
proposed fix requires a trusted PDN server to resolve integrity-metadata conflicts among peers by
downloading the disputed segment from the origin CDN and re-verifying it, which requires the PDN
server to retain CDN read access and to assign and track a per-peer identifier bound to IP and port
for blacklisting; (3) peer IP leak follows directly from WebRTC ICE's requirement that two peers
exchange real, routable IP/port pairs to establish a direct connection — any component built on
direct-WebRTC peer connection therefore exposes each participant's IP to every other participant it
is matched with, unless traffic is relayed through a TURN (Traversal Using Relays around NAT) server,
which the authors note two of the observed customers did use but state does not scale to PDN's
volume of peer-to-peer video traffic without incurring "huge overhead" on the relay infrastructure.
None of the four attacks require breaking TLS/DTLS encryption of the transport channels themselves;
all four exploit protocol-level trust assumptions (static tokens, unverified manifest-only content
checks, direct IP exchange, and unbounded per-viewer resource consumption) that sit above the
encrypted transport.

### Contradicts
None found within this corpus. The paper's claim that PDN services are "as secure as traditional CDN
services" is explicitly attributed to provider marketing material (cited to Peer5's own security
documentation) and is the claim the paper's own attacks refute, not a claim the paper itself makes.

### References worth retrieving
- **Wang, Chen, Wang, Chan, "Content pollution propagation in the overlay network of peer-to-peer live streaming systems: modelling and analysis," IET Communications 12(17), 2018** — foundational, cited [71]; source of the cited 47%-of-viewers pollution-propagation figure this paper references but does not itself reproduce.
- **Zhao, Aditya, Chen, Lin, Haeberlen, Druschel, Maggs, Wishon, Ponec, "Peer-assisted content distribution in akamai netsession," IMC 2013** — competing measurement of a different production peer-assisted CDN, cited [77]; source of the cited ~30% P2P opt-in figure.
- **Zhang, Zhou, Mislove, Sundaram, "Maygh: Building a cdn from client web browsers," EuroSys 2013** — foundational/competing browser-based CDN system, cited [76].
- **Heilman, Kendler, Zohar, Goldberg, "Eclipse attacks on bitcoin's peer-to-peer network," USENIX Security 2015** — attack paper on a different P2P system's peer-discovery mechanism, cited [48]; relevant as a comparison for peer-list-based attacks.
- **Ziwich, Duarte, Silveira, "Distributed mitigation of content pollution in peer-to-peer video streaming"** — foundational for the peer-assisted integrity-checking mitigation this paper adapts, cited [78].
- **Fakis, Karopoulos, Kambourakis, "Neither denied nor exposed: Fixing webrtc privacy leaks," Future Internet 12(5), 2020** — competing/foundational WebRTC IP-leak mitigation work, cited [42].
- **Al-Fannah, "One leak will sink a ship: Webrtc..."** — foundational prior work on WebRTC IP leaks in a non-PDN context, cited [32].
- **Hazhirpasand, Ghafari, "One leak..."** — foundational prior work on WebRTC IP leaks, cited [47].

### Verbatim extracts
"reported to offload up to 95% of bandwidth consumption for video streaming" (abstract).
"claim that their services can offload at least 50% traffic" (Section 3.2).
"11 API keys have been integrated by 18 PDN customers" (Section 4.2).
"both Peer5 and Viblast failed to pass our video segment pollution test" (Section 4.3).
"the binding success response...containing the real public IP address and port is transmitted in plain text" (Section 4.4).
"at a cost of an additional 15% CPU and 10% memory" (Section 4.5).
"none of them provide any pop-up windows to ask for viewers' consent" (Section 4.5).
"our detection for PDN providers...may miss ones that are either proprietary or of low public visibility" (Section 6).
