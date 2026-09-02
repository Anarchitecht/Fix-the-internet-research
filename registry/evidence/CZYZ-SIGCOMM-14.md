## [CZYZ-SIGCOMM-14] Measuring IPv6 Adoption
**Citation:** Jakub Czyz, Mark Allman, Jing Zhang, Scott Iekel-Johnson, Eric Osterweil, Michael Bailey. "Measuring IPv6 Adoption." ACM SIGCOMM, 2014. DOI 10.1145/2619239.2626295.
**Retrieved:** full text via faculty.cc.gatech.edu PDF mirror
**Source URL:** https://faculty.cc.gatech.edu/~mbailey/publications/sigcomm14_ipv6.pdf
**Domain:** L

### What it does
The paper measures how far the Internet had moved from IPv4 to IPv6 as of 2014, along twelve metrics grouped into three perspectives — address allocation and routing readiness, naming readiness, and end-host and traffic readiness — so that a single adoption number is never taken as representative of the whole transition. Each metric is computed from one of ten datasets: historical address-allocation records, BGP routing-table snapshots from Route Views and RIPE RIS, passive DNS query logs at the `.com`/`.net` authoritative nameservers, an active DNS/reachability probe of the Alexa top 10,000 web sites the authors ran themselves, Google's client-side IPv6-capability measurement (a JavaScript probe embedded in search results), and two Arbor Networks traffic-summary datasets built from customer network flow exports. A metric is computed by taking the ratio, or the raw count, of an IPv6-side observation to the equivalent IPv4-side observation, plotted over time, so that overall growth and the IPv6-to-IPv4 ratio's independent trend can both be read off the same figure.

### Measured results
| Metric | Result | Conditions |
|---|---|---|
| Prefix advertisement (A2, routing) | number of globally-seen IPv6 paths grew 110-fold, IPv4 paths grew 8-fold | Route Views + RIPE RIS BGP table snapshots, Jan. 2004 to Jan. 2014; IPv6-to-IPv4 path ratio reached 0.02 by Jan. 2014 |
| AS-level IPv6 support | 18-fold increase in IPv6-capable ASes vs. 2-fold for IPv4 over the same period; IPv6-to-IPv4 AS ratio reached 0.19 | same BGP dataset and window |
| Server-side readiness (R1) | 3.2 to 3.5% of the Alexa top 10,000 web sites reachable over IPv6 as of the most recent measurement | daily probes of AAAA records and IPv6 reachability (tunneled to Hurricane Electric) for the Alexa top 10K, April 2011 (AAAA) / June 2011 (reachability) through the paper's 2014 cutoff; World IPv6 Day 2011 produced a roughly 5-fold jump in AAAA records with a sustained 2-fold increase afterward; World IPv6 Launch 2012 produced a further sustained doubling |
| Client-side readiness (R2) | fraction of clients reaching Google over IPv6 grew 16-fold, from 0.15% (Sept. 2008) to 2.5% (Dec. 2013); annual growth 125% in 2012 and 175% in 2013 | Google's own client-side JavaScript probe, millions of trials per day, sampled users, 90% probed against dual-stacked hostnames and 10% against IPv4-only, resolving to 2-5 global data centers |
| Traffic volume (U1) | IPv6 was 0.6% of Internet traffic by volume at the end of the measurement window; IPv6-to-IPv4 traffic ratio rose from 0.0005 (March 2010) to 0.0064 (Dec. 2013), a 13-fold increase; year-over-year ratio growth was 71% in 2011, 469% in 2012, and 433% in 2013 | two Arbor Networks flow-summary datasets: dataset A, 12-customer sample, daily peak 5-minute volume, Q2 2010-Feb. 2013, covering >400 routers and 55K links; dataset B, ~260-provider sample (19 Tier-1, 92 Tier-2, plus >100 enterprise/content providers), daily average volume, 2013 only, methodology following Labovitz et al.; median daily traffic in dataset B was 58 Tbps in Q4 2013 |
| Application mix (U2) | HTTP/HTTPS share of IPv6 traffic rose from 6% (Dec. 2010) to 95% (2013), surpassing IPv4's 60-69% HTTP/HTTPS share in the same 2013 sample; DNS share of IPv6 traffic fell from a historical 80-90% (per cited prior studies) to IPv4-comparable levels only in the 2013 sample | same Arbor traffic datasets, classified by port number; IPv4 comparison data available only from 2012 onward |

### Parameters
No tunable protocol parameters are set by this paper — it is a measurement study, not a mechanism design. The methodological constants used to build the reported figures are: Alexa top 10,000 sites as the server-side sample; Google's client probe splits traffic 90% dual-stack-hostname / 10% IPv4-only-hostname across 2-5 data centers; the routing-topology snapshot window is Jan. 2004-Jan. 2014.

### Stated limitations
The authors state that public BGP routing datasets (Route Views, RIPE RIS) carry geographic collection bias and miss many peer-to-peer links between smaller ISPs that never propagate to the volunteer collector networks, and argue the bias affects IPv4 and IPv6 data similarly so ratio trends remain informative even though absolute path/AS counts are lower bounds. The server-side and client-side readiness metrics both conflate host capability with the capability of the network path to the host, because neither can be measured independent of a path. The Arbor application-mix classification is by port number only and can misclassify traffic tunneled over port 80. Section 11 (Limitations and Future Work) states the framework omits social, behavioral, and economic factors, vendor support in specific software and hardware, and the prevalence of alternatives to IPv6 such as carrier-grade NAT.

### Requirements it places on the rest of the system
A design assuming IPv6-only or IPv6-preferred direct reachability between arbitrary peers, evaluated against this paper's 2014 endpoint, must assume only 3.2-3.5% of popular web servers and roughly 2.5% of client vantage points had working IPv6 at that time — a design that requires IPv6 transport for a majority of participants had no basis in this dataset's period and needs a more recent measurement (see DHAMDHERE-IMC-12 for an earlier point and any later measurement in this corpus for a current one) before that assumption is usable. The traffic-volume figures establish that even where IPv6 paths exist, aggregate IPv6 traffic share was two orders of magnitude below IPv4's in this dataset, so bandwidth-planning figures for an IPv6-first design cannot be drawn from IPv4-scale assumptions without adjustment. The application-mix finding that IPv6 traffic converged toward HTTP/HTTPS dominance by 2013 supports treating IPv6-carried traffic as ordinary web traffic for classification purposes in that period, not as still being dominated by tunneling or DNS overhead as it was pre-2012.

### Contradicts
None found within this corpus at time of writing. The paper itself flags no contradiction of its own headline claims.

### References worth retrieving
- **Foundational** — Dhamdhere, Luckie, Huffaker, Claffy, Elmokashfi, Aben. "Measuring the Deployment of IPv6: Topology, Routing and Performance." IMC 2012. (already in this batch, DHAMDHERE-IMC-12)
- **Competing** — Nikkhah, Guérin, Lee, Woundy. "Assessing IPv6 Through Web Access: A Measurement Study and Its Findings." CoNEXT 2011. — independent server-side/reachability methodology this paper says it corroborates.
- **Competing** — Zander, Andrew, Armitage, Huston, Michaelson. "Mitigating Sampling Error When Measuring Internet Client IPv6 Capabilities." IMC 2012. — reports 6% of a global client sample IPv6-capable but only 1-2% dual-stack-preferring IPv6, a divergent client-capability figure the paper itself flags as roughly consistent but methodologically different.
- **Competing** — Plonka, Barford. "Assessing Performance of Internet Services on IPv6." ISCC 2013. — independent passive-measurement methodology for IPv4/IPv6 performance comparison, found high variability in a campus traffic sample.
- **Foundational** — Colitti, Gunderson, Kline, Refice. "Evaluating IPv6 Adoption in the Internet." PAM 2010. — earlier IPv6 adoption baseline predating this paper's window.
- **Foundational** — Karpilovsky, Gerber, Pei, Rexford, Shaikh. "Quantifying the Extent of IPv6 Deployment." PAM 2009. — earlier traffic-profile study finding IPv6 traffic dominated by DNS (80-90%), the baseline this paper's application-mix result is measured against.
- **Attack or critique** — Sarrar, Maier, Ager, Sommer, Uhlig. "Investigating IPv6 Traffic - What Happened at the World IPv6 Day?" PAM 2012. — independent measurement of the same World IPv6 Day event this paper cites as producing a discontinuous jump in Figure 7.

### Verbatim extracts
"adoption, relative to IPv4, varies by two orders of magnitude depending on the measure examined"
"2.5% of clients use IPv6 ... most recent two-year annual growth rate averages 150%"
"IPv6 is 0.6% of traffic, and 2-year growth relative to IPv4 is 451% annually"
"only about 3.5% of the top most popular websites are IPv6-ready"
"the number of IPv6 paths has a 110-fold increase from January 2004 to January 2014"
