## [BHAGWAN-IPTPS-03] Understanding Availability

**Citation:** Ranjita Bhagwan, Stefan Savage, Geoffrey M. Voelker. "Understanding Availability." International Workshop on Peer-to-Peer Systems (IPTPS), 2003.
**Retrieved:** full text via https://doi.org/10.1007/978-3-540-45172-3_24
**Source URL:** https://doi.org/10.1007/978-3-540-45172-3_24
**Domain:** C

### What it does

The paper measures host availability in a deployed peer-to-peer file-sharing network so that a designer of a storage system built from these hosts can pick a replication policy from a measured distribution rather than from a single assumed mean availability figure. It builds two measurement tools against Overnet, a distributed hash table (DHT) file-sharing network built on Kademlia in which every host generates and keeps a persistent random identifier (ID) independent of its network address. A crawler discovers active host IDs by recursively querying for 50 randomly generated IDs, so each new host it contacts is itself queried for the same 50 IDs, producing a widening snapshot of active hosts. A prober separately selects a random subset of IDs the crawler found and performs a DHT lookup against each one every 20 minutes; a returned lookup response counts the host as available at that instant. Because probes are ordinary Overnet lookup traffic rather than raw TCP SYN packets used in prior studies, hosts are identified by their persistent ID rather than by IP address, which the paper shows removes an aliasing effect: a single host reappears under many different IP addresses over time (residential DHCP reassignment, network address translation, and multiple users sharing one machine all produce this), so IP-address-based probing undercounts a host's true uptime and overcounts the number of distinct hosts in the system.

### Measured results

| Result | Conditions |
|---|---|
| Crawler discovers ~40,000 host IDs per pass, 70,000-90,000 distinct IDs seen per day (6 passes) | crawler run every 4 hours, 15 days, January 14-28, 2003, on Overnet; one 24-hour crawler outage on January 21 |
| ~85,000 hosts active per day, network size roughly constant over the trace | same 15-day crawler trace |
| Unique host-ID-to-IP-address ratio approximately 1:4 (1,468 unique host IDs responded, mapping to 5,867 unique IP addresses) | 2,400 host IDs selected at random from day-1 crawler output, probed every 20 minutes for 7 days, January 15-21, 2003; 1,468 of 2,400 responded at least once |
| 40% of probed hosts used more than one IP address within 1 day of probing; 50% within 4 days; 32% used 5 or more IP addresses; 12% used 10 or more, over the 7-day trace | same 7-day, 2,400-host prober trace |
| Median host availability (fraction of probes answered) was 0.3 using host-ID-based identification, versus 0.07 using first-seen-IP-address identification over the same 7 days — a 4x understatement | same 7-day, 2,400-host prober trace, availability = successful probes / total probes per host |
| Citing a separate replication model (reference [2], their own prior technical report), replica count needed for 99% file availability at mean host availability 0.07 is 5x the replica count needed at mean host availability 0.3 | applied to the two availability figures immediately above; this multiplier is from the cited replication model, not measured in this paper |
| Availability-distribution curve shape changes with the measurement window: slightly concave over 10 hours, convex over 4 days, more convex over 7 days | same prober trace, availability recomputed over three different window lengths on the same 2,400 hosts |
| Diurnal (daily) swing of roughly 100 hosts between the daily maximum and minimum number of simultaneously available hosts | 7-day prober trace, hosts' local time computed by mapping IP-geolocated longitude (CAIDA Netgeo) to time zone |
| 9,413 host joins-and-leaves per day on average across the probed set, i.e., 6.4 joins/leaves per host per day, against a base of 1,468 responding hosts | same 7-day, 2,400-host prober trace |
| Decay of roughly 32 hosts per day in the number of hosts still responding at all, over the trace | same 7-day prober trace; the paper flags the trace as too short to confirm this trend |
| Pairwise availability independence: for more than 30% of all host pairs, the difference between P(host Y available given host X available) and P(host Y available unconditionally) was 0; 80% of pairs fell between -0.2 and +0.2 | computed per-hour across the full 7-day, 2,400-host prober trace, over all pairs among the 1,468 responding hosts |
| 20%+ of the roughly 85,000 daily active hosts are first-time arrivals each day (about 17,000 hosts/day); departures occur at approximately the same rate | 15-day crawler trace; arrival = first appearance of a host ID in the trace, departure = last appearance |

### Parameters

| Parameter | Value used |
|---|---|
| Crawler query fan-out | 50 randomly generated IDs per query round |
| Crawler interval | every 4 hours |
| Crawler trace duration | 15 days (January 14-28, 2003), with one 24-hour outage |
| Prober sample size | 2,400 host IDs, drawn at random from ~84,000 IDs the crawler found on day 1 |
| Prober interval | every 20 minutes |
| Prober trace duration | 7 days (January 15-21, 2003) |
| CFS replication subset size (cited, not measured here) | 6 |
| Kademlia replication subset size (cited, not measured here) | 20 |

### Stated limitations

The paper states its 15-day crawler trace and 7-day prober trace are both too short to characterize long-term host turnover and says the authors were continuing the trace to validate the availability-distribution-widens-with-window-length trend and to capture longer-term arrival and departure behavior — these results are stated as preliminary. The target system, Overnet, is not open-source, so the measurement infrastructure required reverse-engineering the protocol rather than instrumenting a reference implementation; the paper does not claim its probe behavior is bit-identical to a real client's. Local time for the diurnal-pattern measurement is inferred from IP-address geolocation (CAIDA Netgeo) applied at the moment of each probe, which is an approximation of the host's true time zone, not a direct observation. The independence measurement (pairwise conditional probability) is computed per hour across the trace and characterizes only the population probed, not a proof that any specific small subset chosen by a real deployed system is independent.

### Requirements it places on the rest of the system

A replication-strategy calculation that consumes this paper's availability numbers must use a time-window-matched availability figure, not a single global mean, because the measured distribution's shape changes with the window length over which availability is computed (10 hours vs. 4 days vs. 7 days produce different curves from the same host population). A system that identifies hosts by IP address rather than a persistent host identifier will undercount true per-host availability by roughly a factor of four, per the measured 0.3-vs-0.07 median gap, so any redundancy calculation driven by IP-address-based measurement will over-provision replicas. A system such as Consistent File System (CFS) that eagerly re-replicates on every observed join or leave should expect roughly 6.4 join/leave events per host per day to drive that re-replication trigger, at the measured churn rate on this network. A system relying on availability independence across a replica set (so that correlated simultaneous failure of all replica holders is unlikely) is supported for randomly chosen small subsets by the pairwise measurement, but the paper measures this only for the population it probed and does not measure whether Kademlia's or CFS's specific selection procedure for a replica subset preserves that independence property.

### Contradicts

None found. The paper's central claim is methodological (that IP-address-based probing undercounts availability, contradicting prior IP-address-based peer-to-peer measurement studies such as the Gnutella study it cites [Saroiu, Gummadi, Gribble, MMCN 2002]), but this batch holds no other paper measuring Overnet or the same network to compare against.

### References worth retrieving

- Bhagwan, Savage, Voelker, "Replication strategies for highly available peer-to-peer systems," UCSD Technical Report CS2002-0726, Nov 2002 — foundational (source of the 5x replica-count-at-99%-availability figure this paper cites but does not derive)
- Maymounkov, Mazières, "Kademlia: A peer-to-peer information system based on the XOR metric," IPTPS 2002 — foundational (already in corpus per BRIEF.md §7)
- Dabek, Kaashoek, Karger, Morris, Stoica, "Wide-area cooperative storage with CFS," SOSP 2001 — foundational (CFS's join/leave-triggered replication is the system this paper's churn numbers are framed against)
- Kubiatowicz et al., "OceanStore: An architecture for global-scale persistent storage," ASPLOS 2000 — foundational (OceanStore's periodic-refresh design is cited as needing the decay-rate finding)
- Saroiu, Gummadi, Gribble, "A measurement study of peer-to-peer file sharing systems," MMCN 2002 — competing (the prior IP-address-based availability study whose curve this paper's IP-address curve is said to resemble and whose methodology this paper argues against)
- Chu, Labonte, Levine, "Availability and locality measurements of peer-to-peer file systems," ITCom 2002 — competing (prior availability measurement study)
- Weatherspoon, Kubiatowicz, "Erasure coding v/s replication: a quantitative approach," IPTPS 2002 — competing/foundational for the repair-economics question
- Weatherspoon, Moscovitz, Kubiatowicz, "Introspective failure analysis: Avoiding correlated failures in peer-to-peer systems," Workshop on Reliable P2P Distributed Systems, 2002 — competing (directly addresses the correlated-failure question this paper measures independence for)
- Long, Muir, Golding, "A longitudinal study of internet host reliability," SRDS 1995 — foundational (pre-P2P host-reliability measurement precedent)

### Verbatim extracts

- "the crawler uses a recursive algorithm to discover the IDs of hosts in the network"
- "a successful lookup implies an available host running an Overnet peer"
- "host IP address aliasing is a signiﬁcant issue in deployed peer-to-peer systems"
- "50% of hosts have availability 0.3 or less" [host-ID method, 7 days]
- "50% of all hosts have availability 0.07 or less" [IP-address method, 7 days]
- "each host joined and left the system 6.4 times a day on average"
- "over 20% of the hosts in system arrive and depart every day"
- "80% of all host pairs lie between +0.2 and -0.2"
