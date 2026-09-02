# Conflicts: transport family

Scope: hole-punching and connection-establishment success rates and the conditions each rate is
conditional on, address-translation type prevalence, relay-fallback rates, keepalive intervals and
measured mapping timeouts, browser peer-connection limits, and measurements of mobile-device
transport behavior.

Every entry opened for this family: `FORD-USENIX-05`, `DUARTE-ABAKOS-20`, `HALKES-NETWORKING-11`,
`KANARIS-ARXIV-23`, `TRAUTWEIN-ARXIV-26`, `KEIZER-MOBIHOC-20`, `KERANEN-RFC-18`,
`PETIT-HUGUENIN-RFC-18`, `ROSENBERG-RFC-03`, `REDDY-RFC-20`, `VYZOVITIS-SPECS-23`, `LIANG-ARXIV-24`,
`BUCHET-CCR-25`, `LANGLEY-SIGCOMM-17`, `KAKHKI-IMC-17`, `ENGELBART-ANRW-26`, `SINGH-ARXIV-26`,
`CHROMIUM-BLINK-SRC`, `WANG-SIGCOMM-11`, `RICHTER-IMC-16`, `LIVADARIU-INFOCOM-18`, `BOSWELL-ARXIV-24`,
`CZYZ-SIGCOMM-14`, `VALAPU-ARXIV-25`, `GUPTA-MOBICOM-24`, plus a pass over the full measurement and
requirements indexes for domain L and a check of the citation neighborhood for domains A and J
(`COSTA-DAIS-23`).

No entry in this family reports a mobile device's transport behavior specifically under OS-level
background suspension (an app moved off-screen and later throttled or killed by the operating
system, distinct from ordinary NAT-mapping expiry). `GUPTA-MOBICOM-24` measures per-radio power
draw while a phone is on-screen and in standby, not connection survival while backgrounded, and no
other entry in the corpus's domain-L population supplies that measurement. That is a blank cell in
this family's coverage, not a resolved question.

## Measurement disagreements

### Hole-punching / NAT-traversal connection-establishment success rate, across four different quantities

Four entries each report a headline "success rate" for hole punching, and none of the four measures
the same thing. `FORD-USENIX-05` (2005) reports that 82% of UDP NATs and 64% of TCP NATs, drawn from
a self-selected volunteer "NAT Check" dataset of 380 data points across 68 vendors, consistently
translate a client's private endpoint to the same public endpoint — a NAT-type compatibility check,
not a live two-peer connection attempt. `HALKES-NETWORKING-11` (2011) reports that 64% of peers in a
live Tribler BitTorrent field trial (907 and 1,531 peers, two trials) sit behind a NAT/firewall type
expected to permit hole punching, and that over 80% of attempts between such eligible peers succeed
— a real connection-attempt success rate, conditioned on NAT type. `KANARIS-ARXIV-23` (2023) reports
a single pass/fail outcome per carrier: 3 of 4 tested Dutch mobile carriers held a punched UDP
connection over live 5G, stated in the paper's own prose as "a 75% success rate," with no repeated
trials. `TRAUTWEIN-ARXIV-26` (2026) reports 70% ± 7.1% across 6.25 million real DCUtR hole-punch
attempts in the live IPFS/libp2p network, conditional on a Circuit-v2 relay reservation and address
discovery (Identify) already succeeding — themselves failing for roughly 29% of attempts before a
hole punch is even attempted.

Read side by side, these four figures span different populations (self-selected home routers;
BitTorrent users; four mobile carriers; IPFS/libp2p volunteers), different eras (2005 to 2026),
different sample sizes (four carriers against 6.25 million attempts), and different definitions of
"success" (NAT-type consistency; a real connection attempt; a single held session; a conditional
rate excluding prerequisite failures). None of the four contradicts another; a synthesis citing a
hole-punching success rate must state which of these four quantities it means and must not average
them.

### The commonly repeated "60% TCP / 80% UDP" hole-punching figure is a citation, not a measurement

`KEIZER-MOBIHOC-20` states "hole punching to be successful 60% for TCP and 80% for UDP," explicitly
attributed to RFC 5128 (Srisuresh, Ford, Kegel, 2008) and explicitly marked in that paper's own text
as an external citation, not a result of its own experiment. RFC 5128 is not itself retrieved in
this corpus, so its own sourcing cannot be checked here, but the only entry in this corpus that
measures a directly comparable quantity — NAT compatibility with hole punching, from the same
research lineage (Ford is a co-author of both the 2005 USENIX paper and RFC 5128) — is
`FORD-USENIX-05`, which measures 82% UDP / 64% TCP, not 60%/80%. The cited figure and the measured
figure disagree even in which transport comes out ahead by how much (Ford's own gap is 18 points;
the cited figure's gap is 20 points, and the absolute values do not match either transport). A
synthesis repeating "60% TCP / 80% UDP" as an empirical hole-punching success rate is repeating a
specification-document citation whose own measured basis, if any, is not in this corpus; it should
cite `FORD-USENIX-05`'s own 82%/64% figures instead when a measured NAT-compatibility rate is
needed.

### Carrier-Grade NAT deployment prevalence across Autonomous Systems

`RICHTER-IMC-16` reports 13.3% of roughly 52,000 non-cellular routed Autonomous Systems (609
CGN-positive ASes after the authors' own later update) deploy Carrier-Grade NAT, from a one-week
BitTorrent DHT crawl (March 2016) combined with voluntary Netalyzr sessions, requiring direct
evidence of a leaked internal address alongside the external address as its detection signal.
`LIVADARIU-INFOCOM-18` reports 23.9% of 17,400 Transit/Access ASes (4,191 ASes), roughly six times
Richter's AS count, from passive Internet Background Radiation and Measurement Lab repeat-address
analysis over a longer window (July 2014-September 2016). `LIVADARIU-INFOCOM-18`'s own text
attributes the gap to its lower evidentiary bar (a traffic-volume and behavioral score crossing an
empirically set threshold) against Richter's stricter per-AS signal, not to either paper's figure
being wrong, and states both figures should be read as different-methodology estimates rather than
reconciled measurements. A synthesis wanting current CGN prevalence should state which detection
method a cited figure used rather than treating "13.3%" and "23.9%" as competing measurements of one
number.

### Fraction of IPFS peers unreachable without a relay

`KEIZER-MOBIHOC-20` cites, from Henningsen et al. 2020 (not itself retrieved in this corpus), that
52.2% of IPFS nodes sit behind a NAT — a figure drawn from a Distributed Hash Table crawl of the
entire discoverable peer population. `COSTA-DAIS-23` separately reports that of 55,830 providers
observed actually serving `ipfs.io` gateway traffic over a two-week log window, 2,473 (4.4%) have no
public address and are relay-only. The two figures measure different populations: a DHT crawl counts
every discoverable peer, including many that never successfully serve a request, while the gateway
log counts only peers that already succeeded in serving one — a set structurally biased toward
peers that are, by definition, reachable. This is a difference in what was counted, not a
disagreement about IPFS's NAT exposure.

### Safe UDP keepalive interval and measured NAT mapping timeout, by NAT population

`HALKES-NETWORKING-11` recommends sending a keepalive at least every 55 seconds, derived from a 2011
field trial in which most single-packet-exchange NAT/firewall timeouts fell around 60 seconds or
less, over a population drawn largely from home routers and P2P client software.
`RICHTER-IMC-16` separately measures Carrier-Grade NAT UDP mapping timeouts specifically — devices
operated by an ISP inside its own network, not at the customer's premises — ranging 10 to 200
seconds, with a median of 35 seconds for non-cellular CGNs and 65 seconds for cellular CGNs, and 74%
of detected CGNs expiring idle UDP state within 60 seconds. `RICHTER-IMC-16`'s own text states CGN
mapping is frequently more restrictive than customer-premises-equipment mapping. Halkes's
recommended 55-second floor was derived from, and is safe for, the population Halkes measured; it is
not safe against Richter's measured minimum of 10 seconds. See the destroyed-precondition finding
below for what this does to ICE's own specified keepalive floor.

### Relative hole-punch difficulty of TCP against UDP/QUIC

`FORD-USENIX-05` finds UDP NAT-type compatibility (82%) substantially exceeds TCP (64%), an 18-point
gap, from unsynchronized volunteer NAT-type testing in 2005. `TRAUTWEIN-ARXIV-26` finds TCP and
QUIC (over UDP) hole-punch success rates statistically indistinguishable, both near 70%, when
transport is restricted to one protocol by a server-assigned filter in its 2026 field campaign. The
paper's own text states this result "contradicts the commonly stated belief... that UDP hole
punching is easier than TCP," and attributes the reversal to DCUtR's round-trip-time-based
synchronized dial removing the timing unpredictability that ordinarily disadvantages TCP's
simultaneous-open. The two results measure different conditions — unsynchronized dialing against
deliberately RTT-synchronized dialing — not a contradiction once the synchronization mechanism is
accounted for; a synthesis should not treat Ford's 2005 UDP-over-TCP gap as still holding once a
synchronized-dial mechanism like DCUtR is in use.

## Destroyed preconditions

### QUIC connection migration as a hole-punch restoration path, against measured migration support

`LIANG-ARXIV-24` proposes restoring a hole-punched connection after an address change by using QUIC
connection migration instead of re-punching, and derives that migration saves 2 to 3 round trips
over a fresh punch — a closed-form derivation from protocol step counts, not a measurement against
real, diverse QUIC endpoints. The mechanism requires both peers' QUIC stacks to support and permit
migration: to offer a spare Connection ID and to answer a `PATH_CHALLENGE` from the new address with
a valid `PATH_RESPONSE`.

`BUCHET-CCR-25` scans the real, deployed QUIC-speaking population (May 2024) and measures that this
requirement fails for most endpoints. Among targets that already completed a full handshake with
Server Name Indication supplied — the condition closest to a normal client connecting to a named
service — migration succeeded for 52% of IPv4 targets and 78% of IPv6 targets; without SNI, migration
succeeded for only 7.7% (IPv4) and 1.2% (IPv6) of handshake-succeeding targets. Of the IPv6 targets
that did support migration, 94% belong to a single hosting organization (Hostinger), and the paper
states Cloudflare and Google — two of the largest QUIC-speaking operators — do not support
connection migration at all. A design that adopts `LIANG-ARXIV-24`'s migration-based restoration
path as its primary mechanism, rather than as an opportunistic shortcut behind a full re-punch
fallback, loses the restoration path for roughly half of IPv4 peers and the large majority of IPv6
peers outside one hosting provider.

### ICE's mandatory keepalive floor, against measured Carrier-Grade NAT mapping timeouts

`KERANEN-RFC-18` (ICE, RFC 8445) specifies that an agent's keepalive interval Tr "MUST NOT" fall
below 15 seconds, a fixed lower bound chosen to keep background STUN traffic small, while requiring
(also as a MUST) that every endpoint send periodic keepalives on every active candidate pair to hold
the underlying NAT/firewall UDP binding open for the life of the session.

`RICHTER-IMC-16` measures real Carrier-Grade NAT UDP mapping timeouts as short as 10 seconds (full
range 10-200 seconds, the low end below the RFC's own mandatory floor). An ICE agent following the
specification's floor exactly — sending no more often than every 15 seconds — cannot refresh a
mapping that expires at 10 seconds; the mapping closes, and the punched session with it, before the
next permitted keepalive is due. `HALKES-NETWORKING-11`'s own field-measured recommendation of a
55-second interval, drawn from a home-router/P2P-client population rather than carrier-operated CGN
devices, fails against the same 10-second minimum for the same reason. Neither the RFC's specified
floor nor Halkes's measured recommendation is a safe interval against the shortest Carrier-Grade NAT
timeout this corpus measures.

A design cannot treat 15 seconds or 55 seconds as a universal safe keepalive interval. It needs
either to measure the actual mapping timeout per path — the way `RICHTER-IMC-16`'s own TTL-driven
probing technique does — or to keepalive at whatever interval its deployment's worst-case
Carrier-Grade NAT population requires, accepting the additional background traffic ICE's floor was
chosen to bound.

## Unsupported attributions

None found that can be checked within this corpus. The one candidate — `KEIZER-MOBIHOC-20`'s "60%
TCP / 80% UDP" figure, attributed to RFC 5128 — cannot be verified as unsupported because RFC 5128
is not itself retrieved as a corpus entry; its treatment as a citation rather than a measurement is
recorded above under measurement disagreements instead.

## Internal inconsistencies

None found in this family. No domain-L entry's own abstract states a claim its own body or
conclusion contradicts.
