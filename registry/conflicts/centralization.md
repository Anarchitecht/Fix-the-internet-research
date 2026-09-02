# Centralization family: conflicts and disagreements

Scope: share of nodes on cloud providers, share of users on the largest instances
or relays, share of requests served by one party, gateway concentration, and
instance or relay population distributions, for nominally decentralized systems.
Entries covered: `BALDUF-IMC-23`, `BALDUF-IMC-24`, `WEI-NSDI-24`, `SHI-WWW-25`,
`TRAUTWEIN-SIGCOMM-22`, `COSTA-DAIS-23`, `SOKOTO-USENIXSEC-24`, `RAMAN-IMC-19`,
`LACAVA-ANS-21`, `XAVIER-ARXIV-24`, `BONO-WEBSCI-24`, `DICURSI-BIGDATA-24`,
`WEI-PACMNET-25`, `QU-TOMCCAP-26`, `KLEPPMANN-CONEXT-24`, `QUELLE-PLOSONE-25`,
`SECKIN-ARXIV-25`, `JACOB-MIDDLEWARE-19`, `MARTINS-JCC-26`, `LIN-ICDEW-21`,
`OVEZIK-ACNS-25`, `OVEZIK-FC-24`, `LUO-ARXIV-25`, `STEINER-IMC-07`,
`ADAR-FM-00`, `ELAHI-WPES-12`, `DURUMERIC-IMC-15`, `POLINSKI-CCR-24`.

## 1. IPFS: share of nodes hosted in the cloud

Three papers measure what fraction of the IPFS peer population runs on
commercial cloud infrastructure rather than volunteer-operated machines, and
report figures from under 3% to above 87%.

`TRAUTWEIN-SIGCOMM-22` crawls the IPFS Kademlia DHT every 30 minutes from a
single server in Germany, July 2021 to 2022, discovering 198,964 unique
PeerIDs and 464,303 unique IP addresses. Classifying each address against
1,525 curated cloud-provider IP ranges (the Udger database), the paper states
fewer than 2.3% of IPFS nodes run on a major cloud platform, with the largest
single provider (Contabo GmbH) at 0.44%.

`BALDUF-IMC-23` crawls the same DHT 101 times, twice daily, April 18 to May
26, 2023, using the same Udger classification database. Counting the average
number of unique nodes present per individual crawl, the paper reports 79.6%
cloud-hosted. Recomputing with a global-unique-IP-across-the-whole-window
method — built specifically to match `TRAUTWEIN-SIGCOMM-22`'s own counting
method — the same crawl data gives 39.9% cloud-hosted, still roughly 17 times
`TRAUTWEIN-SIGCOMM-22`'s figure. `BALDUF-IMC-23`'s own text attributes the
full gap to counting methodology and crawl frequency, not to a change in the
network between the two measurement windows, but a methodology-matched
recomputation that still differs by an order of magnitude means the
attribution is not fully demonstrated by the numbers given: the residual gap
between 2.3% and 39.9% is stated as due to method, not shown to be due to
method.

`SHI-WWW-25` does not crawl the DHT topology at all; it observes Bitswap
block-exchange and DHT `Find_Node` traffic directly, from one node accepting
unlimited peer connections plus two virtual DHT peer IDs, March 2021 to
August 2024. Classifying each address as a data-center or public-gateway
node, the cloud share of the observed peer population rises from 50.02% at
the start of the window to 87.33% by the end, and the cloud share of hosted
files rises from 52.32% to 97.43% over the same period. `SHI-WWW-25`'s own
text states its estimate is higher than `BALDUF-IMC-23`'s, attributing the
difference to measurement channel — direct traffic observation captures
NAT-ed clients invisible to a DHT crawl, and folds public gateways into
"cloud" — not to disagreement about the underlying network state.

None of the three pairs is a same-conditions contradiction: the three
measurements differ in channel (DHT-topology crawl for two of them, direct
Bitswap/DHT traffic logging for the third), in classification scope (a fixed
cloud-provider IP-range list versus "cloud or public gateway"), and in window
length (a single multi-week crawl versus a 3.5-year trace). `SHI-WWW-25`'s own
longitudinal curve is consistent with `BALDUF-IMC-23`'s 79.6% 2023 figure
sitting roughly where the trend line would place it, and both are consistent
with cloud concentration having risen substantially since
`TRAUTWEIN-SIGCOMM-22`'s 2021-22 crawl. The one point these three papers do
not resolve is the residual 17x gap between `TRAUTWEIN-SIGCOMM-22` and
`BALDUF-IMC-23`'s own methodology-matched recomputation on data collected
less than a year apart; a synthesis step citing an IPFS cloud-hosting share
should use `BALDUF-IMC-23`'s A-N method (79.6%, closest to `SHI-WWW-25`'s
independently-derived contemporaneous estimate) rather than
`TRAUTWEIN-SIGCOMM-22`'s figure, and should state which channel (topology
crawl versus traffic log) the number came from.

`BALDUF-IMC-24`'s Bluesky measurement adds one more cloud-hosting figure to
this family from a different system: of 62 Bluesky Labeler accounts
identified, 65% (40) run on cloud-hosting infrastructure or behind a reverse
proxy, versus 10% on ISP-assigned residential addresses. This is not
comparable in magnitude to the IPFS figures above — a population of 62
accounts performing one specific moderation role, not a peer population
performing content routing or storage — and is recorded here only as a
same-family, different-system data point.

## 2. IPFS: which channel is "decentralized" — topology, traffic, providers, or entry points

`BALDUF-IMC-23`, `WEI-NSDI-24`, and `COSTA-DAIS-23` each measure a different
part of IPFS and each finds a different concentration figure, because "IPFS
centralization" is not one quantity.

`BALDUF-IMC-23` finds DHT peer-ID traffic concentration separate from node
population: the top 5% of peer IDs generate approximately 97% of DHT and
Bitswap traffic combined, and cloud nodes generate approximately 85% of DHT
traffic against approximately 15% for non-cloud nodes — a traffic-share
figure, not the 79.6%/39.9% node-population figure discussed in Section 1.

`WEI-NSDI-24`, written by IPFS's own maintainers, measures a purpose-built
centralized fast path rather than the DHT itself: a single Protocol-Labs-
operated Indexer service holds 173,998,039,712 provider records, over 100
times the DHT's own count, but from only 604 distinct publishers, against
roughly 56,000 publishers still using the DHT directly. The paper's own text
states the Indexer "does not replace the DHT," since the DHT still holds the
larger publisher count and a larger share of query volume even though the
Indexer holds the numerical majority of records — collapsing this into one
"IPFS is centralized" headline would drop that distinction.

`COSTA-DAIS-23` measures the content-provider population from a single
gateway's request logs rather than from the DHT or the Indexer: 60% of
providers serve only a single distinct content identifier, and the single
largest provider (a pinning service) serves 869,734 distinct identifiers, a
concentration measured over which peers hold retrievable content, not over
which peers participate in DHT routing.

These are not disagreements — DHT-node-population share (Section 1), DHT/
Bitswap traffic share, Indexer-versus-DHT provider-record count, and content-
provider population are four different quantities, each measured over a
different data source and a different sampling window. A synthesis citing
"IPFS centralization" against one number risks conflating any two of these;
`WEI-NSDI-24`'s own entry states this explicitly as a requirement on how a
downstream accounting must be scoped.

A fifth, narrower quantity comes from `SOKOTO-USENIXSEC-24`: hosting
concentration measured only over the badbits denylist, a moderated subset of
IPFS content, not the general population any of the four papers above
measure. Individual peers each host between 19% and 63% of the entire
denylist, and more than 60% of unique denylisted items sit on just two
peers, found from a DHT provider-record crawl of the 417,912-CID denylist
`SOKOTO-USENIXSEC-24` reconstructs. `SOKOTO-USENIXSEC-24`'s own text calls
this figure "misleading" taken alone, because the same denylisted content is
separately shown to be replicated at other locations the two-peer figure
does not capture — a peer-count concentration figure and a content-
availability figure answer different questions even within one paper. This
is consistent in direction with, but not the same measurement as, the
whole-network content-provider concentration `BALDUF-IMC-23` reports in
Section 1 (roughly 1% of peers appear as a provider in about 90% of DHT
provider records): both find that content-hosting responsibility sits with a
small peer count, over different content populations (all DHT-advertised
content versus a curated 417,912-item denylist).

Gateway concentration, the family's fourth named quantity, has one measured
figure in this corpus: `BALDUF-IMC-23` finds 50% of the gateway IP addresses
referenced by DNSLink records (a naming layer that maps human-readable
domains to IPFS content) belong to a single provider, Cloudflare, from one
month of passive DNS data, and that only 20% of DNSLink gateway IPs are
non-cloud at all. `SOKOTO-USENIXSEC-24` separately enumerates 431 gateways
by operator category (Protocol Labs' own; a large CDN; public gateways
listed on ipfs.tech; 105 ephemeral subdomains of one Web3 Gateway-as-a-
Service provider, Infura; an unlisted-others catch-all) without reporting
what fraction of total gateway traffic or IP count each category holds, so
the two papers' gateway figures are not directly combinable into one
concentration number — one gives a hosting-provider share of DNSLink-
referenced gateways, the other gives an operator-category count of a
differently-assembled gateway population.

## 3. Mastodon: instance concentration measured at different granularities and times

`RAMAN-IMC-19` (April 2017-July 2018 crawl of 4,328 instances) and
`XAVIER-ARXIV-24` (August 2024 snapshot of 21,146 instances from
fediverse.observer) both report Mastodon instance concentration, six years
apart, using different metrics: `RAMAN-IMC-19` reports hosting-provider
concentration (top 3 autonomous systems host 62% of all users; Amazon alone
hosts over 30% of users while being used by only 6% of instances) and content-
generation concentration (78% of instances produce under 10% of their own
timeline's content). `XAVIER-ARXIV-24` reports user-population concentration
directly (50% of active Fediverse users on the top 20 of 21,146 instances; 82%
of instances have fewer than 5 active users). Neither figure contradicts the
other; they measure different things (hosting-provider share and content-
origination share versus active-user share by instance) at different times,
and both show persistent, large concentration under their own metric.

`LACAVA-ANS-21` crawled the Mastodon instance-to-instance follow graph
(November-December 2020, 6,960 instances) and explicitly states it does not
measure user-population-per-instance at all — its own entry warns that
"conflating the two would misattribute a user-population-concentration claim
to this paper's evidence." Its own retrieval rationale, stated in the
target registry, was to check whether `RAMAN-IMC-19`'s instance-concentration
figures held up as the network grew; its own text states it never performs
that comparison, citing `RAMAN-IMC-19` only once in a list of prior studies.
A claim that `LACAVA-ANS-21` confirms, updates, or refutes `RAMAN-IMC-19`'s
concentration figures is not supported by `LACAVA-ANS-21`'s own text.

## 4. Nostr: relay concentration measured over different relay populations

`WEI-PACMNET-25` (crawl of all 911 relays discoverable via the nostr.watch
index, July-December 2023) finds 73% of all collected posts present on the
single top-ranked relay, though the paper's own text cautions this overstates
concentration because a post commonly exists on more than one relay at once
(mean replication 34.6 relays per post). `QU-TOMCCAP-26` (a fixed set of four
pre-selected major relays — relay.damus.io, relay.nostr.band,
relay.primal.net, nos.lol — August 2024 to September 2025) finds a
comparatively even split among those four: per-relay deduplicated event
totals range from 4.42 million to 6.48 million, none dominating.

These figures are not a contradiction: `WEI-PACMNET-25` ranks a "top relay"
against the full discovered population, including a long tail of small
relays, while `QU-TOMCCAP-26` measures distribution only among four relays
that were all already large by construction. A single relay dominating the
full population is compatible with an even split among the four largest
relays in that population. `QU-TOMCCAP-26`'s own text cites `WEI-PACMNET-25`'s
finding once, in the general form "Nostr traffic is concentrated in a small
set of relays," without reproducing `WEI-PACMNET-25`'s specific figures for a
side-by-side check, and its own entry states directly that no such comparison
can be extracted from its retrieved text. Whether the specific relay
`WEI-PACMNET-25` found dominant in 2023 is one of `QU-TOMCCAP-26`'s four
2024-25 relays is not stated in either paper's retrieved text and is not
established here.

`WEI-PACMNET-25` separately runs the same top-10-hosting-provider removal
simulation `RAMAN-IMC-19` ran for Mastodon, over its own Nostr dataset, and
cites `RAMAN-IMC-19` by name as the comparison baseline: after removing the
top 10 autonomous systems by relay count, over 80% of Nostr posts stay
available (reachable on at least one surviving relay), against `RAMAN-IMC-19`'s
finding that the same removal makes 90.1% of Mastodon toots unavailable
under Mastodon's no-replication baseline — under 10% of toots survive. Both
figures come from an identical removal methodology (top-10 autonomous
systems, ranked by hosting count, availability defined as at least one
surviving copy) applied by each paper to its own live network, so this is a
directly comparable pair, not a same-word-different-quantity case. It is not
a contradiction either: the two papers measure two different systems, and
`WEI-PACMNET-25` attributes the more-than-70-percentage-point gap to a
measured structural difference between the networks — 64% of the autonomous
systems hosting a Nostr relay host exactly one relay each, against
`RAMAN-IMC-19`'s finding that the top 3 autonomous systems host 62% of all
Mastodon users. A flatter hosting distribution across autonomous systems
produces measurably higher resilience to hosting-provider removal under an
identical knockout test; this is the corpus's clearest same-methodology,
cross-system comparison in this family.

## 5. Bitcoin: block-production concentration and token-wealth concentration are different quantities

`LIN-ICDEW-21` (2019 block data, one calendar year, block producer identified
by coinbase address) reports a Nakamoto coefficient — the minimum number of
producers whose combined share exceeds 50% of blocks — stable at 4 to 5 for
Bitcoin, and a sliding-window Gini coefficient over per-producer block counts
averaging 0.523 (one-day windows) to 0.760 (one-month windows).

`OVEZIK-FC-24` (figures compiled from third-party sources as of 2022) reports
a different Gini coefficient over a different resource: token wealth by
address, not blocks by producer — 0.5145 restricted to the 10,000 wealthiest
addresses, 0.956 over all addresses — alongside a separately sourced claim
that four mining pools control more than 75% of Bitcoin's mining power as of
2022.

These are not comparable figures despite both being called "Bitcoin's Gini
coefficient": one is computed over block-production share, the other over
token-holding share, and the two resources have no reason to be distributed
alike. `OVEZIK-ACNS-25` (the later companion paper by an overlapping author
set, its own pipeline run 2018-2024) demonstrates the point directly rather
than by cross-paper comparison: computing Gini and the Herfindahl-Hirschman
index on the identical Bitcoin chain data, entity-clustering addresses into
real-world parties versus leaving them unclustered produces materially
different HHI values starting in 2016, and computing Gini under an "all
entities that ever produced a block" population window versus a "only
entities active in this specific week" window produces visibly different Gini
trajectories on the same underlying blocks. `OVEZIK-ACNS-25`'s own text states
plainly that a Gini or HHI figure "must therefore also know, and state, which
population definition produced it," because two values computed on the same
chain under different population or clustering choices are not directly
comparable. This is the family's clearest documented case of the same
counting-method sensitivity the brief's calibration examples describe: the
number moves by method, not by a change in the underlying network, and the
paper that shows this is explicit about it.

## 6. Matrix: a single 2018 concentration figure with no independent check in this corpus

`JACOB-MIDDLEWARE-19` crawled the public Matrix federation on 2018-07-25:
2,003 homeservers, 131,463 users. The top 1% of homeservers held 87% of all
users; the single largest homeserver held 76,271 of the 131,463 users (58%);
applying the paper's own transaction-count formula to the crawled structure,
that single largest homeserver was projected to be involved in 44.5% of all
inter-server messages, sending 88.4% of all sent messages while receiving
0.6% of all received messages.

No other entry in this family independently measures Matrix homeserver
concentration. `MARTINS-JCC-26` is a systematic literature-mapping study, not
a measurement of the protocol: its own text states plainly that "no
throughput, latency, or scalability figures for the Matrix protocol itself
are reported as the mapping study's own measurements." It lists
`JACOB-MIDDLEWARE-19` as one of 21 primary studies surveyed but does not
restate or check its concentration figures. A synthesis citing Matrix
homeserver concentration has exactly one measured data point in this corpus,
from a single day in 2018, with no later snapshot to check it against.

## 7. Bluesky and Fediverse account growth across time — consistent, not disagreeing

`KLEPPMANN-CONEXT-24` (the AT Protocol authors' own paper, written through
October 2024) states over 10 million registered Bluesky users, about 20
months after the February 2023 launch. `BALDUF-IMC-24` (crawl March-April
2024) counts 5,591,824 user DIDs. `QUELLE-PLOSONE-25` (crawl through May
2024) analyzes 5,000,000 users from a 5.28-million-ID seed list.
`SECKIN-ARXIV-25` (through February 2025) reports 30 million total accounts,
26 million with at least one follower, as of early 2025. Read in date order —
5.0-5.6 million (April 2024), over 10 million (October 2024), 30 million
(January 2025) — these track one system's growth curve rather than
disagreeing about its size at one point in time; `SECKIN-ARXIV-25`'s own data
attributes a large share of the late-2024 jump to two dated events (Brazil's
August 30, 2024 blocking of X, and the November 4, 2024 US election), both of
which fall after `BALDUF-IMC-24`'s and `QUELLE-PLOSONE-25`'s April-May 2024
collection windows and before `KLEPPMANN-CONEXT-24`'s October 2024 and
`SECKIN-ARXIV-25`'s own January 2025 cutoffs. No entry in this corpus reports
two different user counts for Bluesky at the same date.

## 8. PeerTube: hosting-provider concentration at a similar scale to IPFS, among different providers

`POLINSKI-CCR-24` crawls the PeerTube federation (a federated video-hosting
system, the closest population in this corpus to IPFS's content-addressed
storage in scale of finding, if not in mechanism) starting from Framasoft's
public instance tracker, August 2024, reaching about 1,200 instances. The
top 15 autonomous systems host 62% of discovered instances; the top 7 host
over 50%; the single largest, Hetzner Online GmbH, hosts 17.5%. `POLINSKI-CCR-24`'s
own bibliography note draws the comparison directly: it states `BALDUF-IMC-23`'s
IPFS figure (top 3 cloud providers hosting 51.9% of DHT servers) is "a
directly comparable centralization figure for a different content-addressed
decentralized storage system."

The two networks share the same shape of finding — a small number of
hosting providers holding roughly half of the population — but not the same
providers. `POLINSKI-CCR-24` states explicitly that cloud hyperscalers (AWS,
Google Cloud Platform) are "nearly absent" from PeerTube's hosting AS list,
attributing this (as an inference, not a measured fact) to those providers'
outbound-bandwidth pricing being uncompetitive against the specialized,
lower-cost European hosts (OVHCloud, Scaleway, Hetzner) that dominate
instead. This is the opposite hosting-provider profile from IPFS's, where
`BALDUF-IMC-23` finds Amazon AWS alone responsible for 68% of DHT cloud
traffic volume. A "top-N-hosting-provider share" figure for a decentralized
system therefore does not by itself say which kind of provider is
concentrating the population — PeerTube's ~50-62% and IPFS's ~52-80%
(Section 1) are comparable in magnitude, not in composition.

`POLINSKI-CCR-24` also reports a low-replication finding structurally
parallel to `COSTA-DAIS-23`'s IPFS result (Section 2): over 92% of PeerTube
videos are stored with no inter-instance redundancy at all (a single copy),
against `COSTA-DAIS-23`'s finding that about 70% of IPFS content identifiers
are held by at most two providers. Both figures describe low replication by
default in a content-addressed or federated storage system with no built-in
replication incentive, but over different content populations (video files
under PeerTube's opt-in per-instance redundancy policy, versus arbitrary
IPFS content identifiers under IPFS's explicit re-provide requirement), so
the two percentages are not one statistic measured twice.

## 9. Bluesky: component-level hosting concentration is a different measurement from account growth

Section 7 tracks how many Bluesky accounts exist over time. `BALDUF-IMC-24`
measures a different quantity entirely at one point in that timeline
(March-April 2024, 5,591,824 DIDs): which single operator or platform each
architectural component concentrates around. Of 5,077,159 downloaded DID
Documents, 98.9% carry a handle that is a subdomain of bsky.social, the
platform operator's own free custodial domain; only 1.1% of users manage
their own signing keys and domain. Among the roughly 43,000 Feed Generators
(user-created feed-ranking services) discovered, the top three hosting-as-a-
service platforms hold 95.8% of them between them, with one platform,
Skyfeed, alone hosting 85.86%.

`BALDUF-IMC-24`'s own text states these per-component figures do not reduce
to one number: identity-handle concentration (98.9%), Feed-Generator-hosting
concentration (85.86%), and domain-registrar concentration among the small
fraction of users who do self-manage a domain (the top four registrars hold
50%, the least concentrated of the three) move independently, and the paper
states directly that a synthesis step treating "Bluesky's decomposition
produces diversity" as one true-or-false claim "would need to average or
otherwise combine these disparate per-component figures," which the paper
itself does not do. No other entry in this corpus independently measures
Bluesky's identity-handle or Feed-Generator-hosting concentration at a
different date to check `BALDUF-IMC-24`'s figures against; as with the
Matrix figure in Section 6, this is a single measured snapshot with no
second measurement in this family to compare it to.

## 10. Unsupported attribution: a Mastodon concentration figure not present in its cited source

`DICURSI-BIGDATA-24`'s own related-work section attributes to `RAMAN-IMC-19`
the figures "5% of instances hold 90% of users and 94% of toots" and
"outages in 10 instances could remove 60% of global toot volume."
`RAMAN-IMC-19`'s own retrieved measured-results contain no "5% of instances /
90% of users / 94% of toots" figure in any form; its actual reported
concentration figures are shaped differently — hosting-provider share (top 3
autonomous systems host 62% of users), content-generation share (78% of
instances produce under 10% of their own timeline content), and a simulated-
removal figure (removing the top 10 instances by toot count, with no
replication, makes 62.69% of toots unavailable — close to, but not identical
to, `DICURSI-BIGDATA-24`'s stated "60% from outages of 10 instances," and
describing a different event: simulated permanent removal from a graph
model, not an outage). `DICURSI-BIGDATA-24`'s own entry already flags both
figures as unverified and states they must be checked against `RAMAN-IMC-19`'s
full text before use, which is the correct caution — but the specific
"5%/90%/94%" figure remains unconfirmed against `RAMAN-IMC-19`'s retrieved
text as it stands in this evidence file, and a synthesis step must not carry
it forward as `RAMAN-IMC-19`'s finding.

A second, smaller cross-system comparison is worth flagging without being a
misattribution: `TRAUTWEIN-SIGCOMM-22` contrasts its own IPFS figure ("fewer
than 2.3% of IPFS nodes run in major cloud platforms") against "a stated 6%
Amazon-only share for Mastodon," citing `RAMAN-IMC-19`. `RAMAN-IMC-19`'s own
text does state Amazon is "used by only 6% of instances" — the figure is
correctly sourced — but the two percentages have different denominators and
different scope: `RAMAN-IMC-19`'s 6% counts Mastodon instances using one
named provider (Amazon), while `TRAUTWEIN-SIGCOMM-22`'s 2.3% counts IPFS
nodes across 1,525 provider IP ranges combined. The comparison as stated
invites reading the two numbers as directly comparable cloud-dependence
figures; they are not, without adjusting for the provider-count and unit
mismatch.

## 11. What this family does not contain

No destroyed-precondition finding was found within this family in the sense
the brief defines it — one selected mechanism's requirement removed by
another selected mechanism's effect. The papers gathered under this family
are measurement studies of already-deployed systems, not mechanism proposals
with requirements another mechanism in this corpus could remove; the
requirement statements their own entries carry (for example,
`WEI-PACMNET-25`'s AS-diversity replication cap needing prior knowledge of
each relay's hosting AS, or `JACOB-MIDDLEWARE-19`'s finding that
redistributing users away from a centralized Matrix homeserver structure
worsens rather than improves peak per-server load) are internal to a single
paper's own analysis, not a requirement one paper's selected mechanism places
on a second paper's separately selected mechanism. No abstract-versus-
conclusion inconsistency was found within any single entry in this family.
