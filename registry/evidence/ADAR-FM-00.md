## [ADAR-FM-00] Free Riding on Gnutella

**Citation:** Eytan Adar, Bernardo A. Huberman. "Free Riding on Gnutella." First Monday, 2000. DOI 10.5210/fm.v5i10.792.
**Retrieved:** full text via https://firstmonday.org/ojs/index.php/fm/article/view/792/701
**Source URL:** https://firstmonday.org/ojs/index.php/fm/article/view/792/701
**Domain:** I

### What it does

The paper measures the distribution of file-sharing and query-answering effort across participants of the Gnutella network, by passively logging protocol messages that pass through one modified client. The authors instrumented the Furi Gnutella client to log every ping, pong, query, and query-response message it observed. A ping message asks other hosts "are you there"; a pong message replies and states how many files the replying host shares. A query message asks the network "who has X"; a query-response message states that a specific host holds a match. Because query-response messages are relayed back along the same path the query traveled, the logging host observed responses from hosts well beyond its direct neighbors, giving a wider sample than direct connections alone would allow.

### Measured results

| Measurement | Figure | Conditions |
|---|---|---|
| Hosts sharing zero files | 66% (22,084 of 33,335 peers); rises to ~69% once NAT-blocked transactions are accounted for | 24-hour capture, Saturday 1pm to Sunday 1pm, August 2000, Furi client logging pong messages |
| Hosts sharing 10 or fewer files | 73% (24,347 of 33,335) | Same capture |
| Share of files held by top 1% of hosts | 37% (333 hosts holding 1,142,645 of the shared files) | Same capture, ranked by files shared |
| Share of files held by top 20% of hosts | 98% (6,667 hosts) | Same capture |
| Hosts issuing pings, before NAT filtering | 35,352 hosts sharing 3,304,046 files | 24-hour capture |
| Hosts and files after NAT-address hosts removed | 33,335 hosts sharing 3,100,464 files | NAT hosts identified by duplicate reported address; 2,017 of ping-reporting hosts (about 5%) and 937 of 5,699 query-response hosts (16%) reported NAT addresses |
| Query-response messages captured | 87,668 | Same 24-hour period, sampled by repeatedly reattaching to different points in the network to widen coverage |
| Hosts never returning a query response | 63% (7,349 of 11,585 hosts that had files to offer) | Sample restricted to hosts with a downloadable file, using the 5% lower-bound NAT estimate |
| Share of query responses from top 1% of responding hosts | 47% | Same 11,585-host sample |
| Share of query responses from top 25% of responding hosts | 98% | Same 11,585-host sample |
| Correlation between peer count and files shared, by domain | r-squared 0.927 | 2,538 unique domains, peer counts from 1 to 2,951 |
| Correlation between peer count and query responses, by domain | r-squared 0.922 | 1,276 domains |
| Correlation between peer count and files shared, by top-level domain | r-squared 0.953 | 77 top-level domains |
| Correlation between peer count and query responses, by top-level domain | r-squared 0.958 | 61 top-level domains |
| Correlation between files shared and query responses received per host (quantity vs. quality of files) | r-squared 0.00105 (no relationship) | 10,510 peers |
| Queries concentrated on few distinct search terms | Top 1% of distinct queries account for 37% of total query volume; top 25% account for over 75% | Separate capture of 202,509 Gnutella queries |
| Weekday consistency check | 72% of a sample of over 300 hosts shared no files | Smaller weekday trace, cited as consistent with the 24-hour weekend result |

### Parameters

No tunable system parameter is introduced; this is a passive measurement study. The only methodological choice stated is the NAT-detection threshold: a host is classified as behind NAT when its reported address in a ping or query-response message is shared by another host, giving the two bounds of 5% (ping-based) and 16% (query-response-based) NAT prevalence used to bound the free-riding estimate.

### Stated limitations

The authors state that Gnutella's search horizon, the farthest set of hosts a query can reach given the message time-to-live, means files held beyond that horizon are unreachable regardless of whether the holding host would answer, so the measured non-response rate is a lower bound on total unreachability, not a full accounting of it. They state the measurement cannot capture all query-response messages, only a sample obtained by repeatedly reattaching to different points in the network. They state that host connectivity duration during the 24-hour window is unknown, so the query-response sample's coverage per host cannot be corrected for how long each host was actually online. The paper offers no experimental test of proposed countermeasures (FreeNet-style forced replication, Napster-style automatic sharing, or a market for resources); these are discussed only as unevaluated alternatives.

### Requirements it places on the rest of the system

None as a positive mechanism — this paper reports a measurement, not a protocol. Any component that assumes participants will act as content or bandwidth providers by default must budget for a request-serving population concentrated in a small fraction of participants: this trace shows the top 1% of hosts answering roughly half of query traffic and the top 20% holding roughly all shared file volume, so those hosts are a measured single point of exposure and a load concentration risk, not a diffuse one.

### Contradicts

None found within this corpus. The paper is frequently summarized elsewhere with rounded figures ("70% free ride," "50% of files from 1% of peers"); this entry's exact figures (66% base rate rising to ~69%, 37% of files from the top 1%, 47% of query responses from the top 1%) should be used instead of the rounded secondary versions.

### References worth retrieving

- Chaum, "Security without identification: Transaction systems to make big brother obsolete," CACM 28(10), 1985 — foundational (pseudonymity/anonymity in transaction systems, not p2p-specific)
- Hardin, "The Tragedy of the Commons," Science 162, 1968 — foundational (the social-dilemma framing the paper applies)
- Waldspurger, Hogg, Huberman, Kephart, Stornetta, "Spawn: A Distributed Computational Economy," IEEE Trans. Software Engineering 18(2), 1992 — competing (market-based resource-allocation alternative to voluntary sharing, cited as an incentive-design comparison)
- Huberman, Lukose, "Social Dilemmas and Internet Congestion," Science 277, 1997 — foundational (companion empirical work by an author, on congestion as a social dilemma)

### Verbatim extracts

- "almost 70% of Gnutella users share no files, and nearly 50% of all responses are returned by the top 1% of sharing hosts"
- "free riding is distributed evenly between domains"
- "peers that volunteer to share files are not necessarily those who have desirable ones"
- "These few providers act as a rather centralized server"
