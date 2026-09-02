## [GYONGYI-VLDB-04] Combating Web Spam with TrustRank
**Citation:** Zoltán Gyöngyi, Hector Garcia-Molina, Jan Pedersen. "Combating Web Spam with TrustRank." VLDB, 2004. Pages 576-587. DOI 10.1016/B978-012088469-8.50052-8.
**Retrieved:** full text via http://www.vldb.org/conf/2004/RS15P3.PDF
**Source URL:** http://www.vldb.org/conf/2004/RS15P3.PDF
**Domain:** F

### What it does
TrustRank ranks web pages (or, at the granularity actually used in the evaluation, whole web sites) by an estimate of how unlikely each is to be spam, so a search engine can filter or demote spam without manually checking every page. A human evaluator (the oracle) checks a small set of pages directly and assigns a good/bad label. TrustRank then propagates trust from the labeled good pages along the outgoing hyperlinks of the web graph, using the same iterative computation as PageRank but restarted at each step toward the seed set instead of toward the whole graph. A page many hyperlink hops from every good seed page receives a low score even if it has high ordinary PageRank.

Mechanism, in the two steps a reader would implement: (1) seed selection — rank all sites by "inverse PageRank," a bias-free damped random walk run backward along inlinks so that sites with many outlinks to high-PageRank sites are ranked first, since such sites are efficient starting points for reaching much of the good web in a few hops; take the top-ranked few thousand sites, filter out sites absent from major web directories (this removes sites that mimic a directory's structure to inflate their own score), and have a human evaluator label a fixed budget of the highest-ranked remaining sites as good or bad; keep only the good ones as the seed set. (2) trust propagation — run the same power-iteration update as biased PageRank, t* = alpha_B * T * t* + (1 - alpha_B) * d, for M_B iterations, where T is the web's row-normalized link transition matrix and d is the seed set represented as a uniform probability vector over the labeled good sites (zero elsewhere). Two variant propagation rules were also defined but not implemented in the reported experiment: trust dampening (each hyperlink hop multiplies the passed trust score by a constant beta < 1) and trust splitting (a page with trust score T(p) and out-degree omega(p) passes T(p)/omega(p) along each outgoing link, so pages with many outgoing links pass less trust per link).

### Measured results
All experiments run on the site-level graph obtained by collapsing the full set of pages crawled and indexed by AltaVista as of August 2003 into 31,003,946 sites (individual pages sharing a fully qualified host name become one site); 13,197,046 of these sites (over one third) are unreferenced and receive the same minimal static score under every method tested.

| Experiment | Conditions | Result |
|---|---|---|
| Seed selection | Inverse PageRank with alpha_I = 0.85, M_I = 20 iterations, on the 31,003,946-site graph; top 25,000 by inverse-PageRank score, directory-filtered down to about 7,900, of which the top 1,250 were manually evaluated by the paper's first author acting as oracle | 178 sites selected as the good seed set S+ |
| Evaluation sample construction | 31,003,946 sites ranked by PageRank, split into 20 buckets each holding 5% of total PageRank mass (bucket 1 = 86 highest-PageRank sites, bucket 20 = 5,000,000+ lowest); 50 sites sampled at random per bucket | 1,000-site sample; oracle-usable subset of 748 sites: 563 reputable, 37 web-organization, 13 advertisement (all three counted "good," 613 total), 135 spam ("bad"); 252 sites dropped as unusable (22 personal-page hosts, 35 aliases, 56 empty, 96 non-existent, 43 unclassifiable) |
| TrustRank vs. PageRank, bucket-level spam concentration | TrustRank computed with M_B = 20 iterations, alpha_B = 0.85, the 178-site seed set; PageRank computed with M = 20, alpha = 0.85 on the same graph; buckets defined per method to hold equal counts | Top 5 TrustRank buckets contain almost no spam; PageRank's bad-site fraction peaks at 50% in buckets 9-10; PageRank bucket 2 already shows about 20% bad sites |
| Bucket-level demotion | Same TrustRank/PageRank run as above, on the 748-site evaluable sample | Spam sites starting in PageRank bucket 2 are demoted by 7 buckets on average (landing near TrustRank bucket 9); good sites in PageRank bucket 16 are promoted by about 1 bucket on average |
| Pairwise orderedness (fraction of sample pairs where the higher-trust page is not the worse one) | 748-site sample, pairs built cumulatively from the top 100 to all 748 top-PageRank sites; compared against Ignorant Trust (score 1/2 to all but the 5 seeds overlapping the sample) and against plain PageRank | TrustRank pairwise orderedness reaches about 0.95 at 500 sample sites and stays above both baselines across every sample size tested |
| Precision/recall at TrustRank-bucket thresholds | Threshold delta swept over the 17 TrustRank-bucket boundaries on the 748-site sample | At threshold = TrustRank buckets 1-10: precision 0.86, recall 0.55; over the full 748-site sample (threshold = 0): precision 0.82 (= 613/748), which is also the sample's baseline good fraction |
| M-step trust function (toy 7-page example, not the AltaVista graph) | Trust score = 1 if reachable from a random 3-page seed in <= M hops from Figure 2's 7-node example graph | M=1: pairwise orderedness 19/21, precision 1, recall 3/4. M=2: 1, 1, 1. M=3: 17/21, 4/5, 1 |
| Ignorant trust function (toy example) | Same 7-page example, random seed set of size L=3, score 1/2 for unlabeled pages | Pairwise orderedness 17/21 over 42 ordered pairs; precision 1, recall 1/2 at threshold 1/2 |

A separate synthetic-graph comparison of inverse PageRank against a second seed-selection scheme ("high PageRank") is reported only in a cited technical report (Gyöngyi and Garcia-Molina, "Seed selection in TrustRank," Stanford tech report 2004), not reproduced with numbers in this paper; the paper states only the qualitative conclusion that inverse PageRank was "slightly better."

### Parameters
| Parameter | Value used | Range tested |
|---|---|---|
| alpha_I (inverse PageRank decay factor, seed selection) | 0.85 | not varied; cited as the standard value from the original PageRank paper |
| M_I (inverse PageRank iterations) | 20 | not varied; stated as sufficient for convergence of relative site ordering |
| alpha_B (TrustRank decay factor) | 0.85 | not varied |
| M_B (TrustRank iterations) | 20 | not varied |
| L (oracle invocation budget / seed pool manually evaluated) | 1,250 sites examined, yielding 178 good seeds | not varied in the main experiment |
| Site-count reduction before oracle evaluation | 25,000 top inverse-PageRank sites -> ~7,900 after directory filtering -> 1,250 manually checked | not varied |
| Evaluation sample size | 1,000 sites (748 usable) | not varied |
| Number of PageRank/TrustRank buckets | 20, later merged to 17 (buckets 17-20 combined because they hold only the 13M+ zero-inlink sites) | not varied |
| Trust dampening factor beta | defined symbolically (beta < 1); no numeric value used in the reported AltaVista experiment | not tested numerically |

### Stated limitations
The paper works at site granularity, not page granularity, purely to reduce computation; the authors state the same methods apply equally at either granularity but do not report page-level results. Using the paper's first author as the sole oracle "raises the issue of bias in the results," which the authors acknowledge as their only practical option given the unavailability of a search-engine spam expert with time to spare. TrustRank "is unable to effectively separate low-scored good sites from bad ones," because a site with no inlinks (over 13 million of the 31 million sites) carries no information a link-propagation method can use. The authors state that trust dampening and trust splitting were proposed but their interplay was not explored experimentally and is left as future work, and that seed selection could be made iterative (reconsidering which pages to send to the oracle based on prior oracle answers) rather than done in one batch, also left to future work.

### Requirements it places on the rest of the system
Requires a directed link graph over the items to be ranked (the paper uses web hyperlinks; any analogous directed graph would substitute) and requires that "good" nodes point predominantly to other good nodes (the "approximate isolation" assumption) — TrustRank's demotion of spam depends on spam sites lying multiple hops from every seed, so a spam item with a direct or short-hop link from a seed page defeats the metric for that item. Requires a fixed, small, human-vetted seed set assembled before propagation runs; the paper's own seed-selection heuristic (inverse PageRank plus a directory-membership filter) is itself vulnerable to being gamed by any actor that can mimic a listed directory's link structure, which is exactly why the authors added the directory filter after observing spam pollution in their unfiltered candidate list. Requires re-running the human-oracle labeling step whenever the seed set needs to change, since nothing in the mechanism updates seed membership automatically. Does not require edge weights or any signal beyond the existence of a hyperlink.

### Contradicts
None found within this corpus. Not itself contradicted by any paper in this batch; it is cited by LAS-EPRINT-26 among related trust-propagation approaches only in a general list, without comparison figures.

### References worth retrieving
- foundational: L. Page, S. Brin, R. Motwani, T. Winograd, "The PageRank citation ranking: Bringing order to the web," Stanford tech report, 1998 — the base random-walk formulation TrustRank biases.
- foundational: T. Haveliwala, "Topic-sensitive PageRank," WWW 2002 — the custom static-score-distribution-vector technique TrustRank's biasing reuses.
- competing: S. Kamvar, M. Schlosser, H. Garcia-Molina, "The EigenTrust algorithm for reputation management in P2P networks," WWW 2003 — a PageRank-style algorithm for peer reputation in peer-to-peer networks, cited as the closest peer-to-peer analogue.
- competing (efficiency): S. Kamvar, T. Haveliwala, C. Manning, G. Golub, "Extrapolation methods for accelerating PageRank computations," WWW 2003.
- attack/critique-adjacent: J. M. Kleinberg, "Authoritative sources in a hyperlinked environment," Journal of the ACM 46(5), 1999 — the hub/authority framework the paper references when discussing directory-clone spam that inflates hub scores.

### Verbatim extracts
- "we can effectively filter out spam from a significant fraction of the web, based on a good seed set of less than 200 sites."
- "more than one third of the sites (13,197,046) were unreferenced."
- "we manually evaluated the top 1,250 (seed set S) and selected 178 sites."
- "for the 500 top-PageRank sample sites TrustRank receives a pairwise orderedness score of about 0.95."
- "if the threshold delta is set...precision is 0.86 and recall is 0.55."
- "the baseline precision score for the sample X is 613/(613+135) = 0.82."
- "there is virtually no spam in the top 5 TrustRank buckets."
- "spam sites in PageRank bucket 2 got demoted seven buckets on average."
