## [GRUBBS-SP-19] Learning to Reconstruct: Statistical Learning Theory and Encrypted Database Attacks
**Citation:** Paul Grubbs, Marie-Sarah Lacharite, Brice Minaud, Kenneth G. Paterson. "Learning to Reconstruct: Statistical Learning Theory and Encrypted Database Attacks." IEEE Symposium on Security and Privacy, 2019. DOI 10.1109/SP.2019.00030.
**Retrieved:** full text via https://eprint.iacr.org/2019/011.pdf
**Source URL:** https://eprint.iacr.org/2019/011.pdf
**Domain:** G

### What it does
The paper reconstructs the plaintext values or plaintext order of records in an encrypted database
from access-pattern leakage alone — the record identifiers a server returns for each query, without
seeing plaintext query or record content — by treating reconstruction as a statistical learning
problem. This reframing produces attacks whose query count depends only on the desired error
tolerance, not on the number of records or the number of possible plaintext values, which the
authors state as the first attacks with that scale-free property.

Mechanism (approximate order reconstruction, ApproxOrder, the paper's central result): the attacker
observes range queries against the database and, for each query, the encrypted database returns
which stored records fall inside the range. From the sequence of returned record sets the attacker
builds a PQ-tree, a data structure originally used for testing the consecutive-ones property, that
compactly records every ordering constraint the observed queries impose on the records. Reading
maximal-order-preserving groups ("buckets") out of the finished PQ-tree yields the records' order up
to a sacrifice: any two records whose true values differ by at most a fraction epsilon of the value
domain N may be merged into an ungrouped bucket, and records within epsilon N of the domain's two
extremes may be left ungrouped ("sacrificial epsilon-approximate order reconstruction",
epsilon-AOR). The attack requires no assumption about the query distribution — not independence,
not identical distribution, not uniformity — to run; a uniform-distribution assumption is used only
in the paper's own analysis of query count, not in the attack.

Mechanism (approximate value reconstruction, epsilon-ADR, extending order to value): given the
epsilon-AOR bucket structure and an auxiliary model of the database's value distribution (a
probability distribution over N approximating, but not necessarily equal to, the true one), the
attack in three steps: (1) record-rank estimation orients the ordered buckets left-to-right by
comparing the proportion of records estimated above versus below the domain midpoint against the
same proportion computed from the auxiliary distribution, and estimates how many sacrificed records
precede the first bucket; (2) partition estimation converts the estimated rank range of each bucket
into an estimated value-range boundary using order statistics of the auxiliary distribution; (3)
database estimation assigns every record in a bucket the median of the auxiliary distribution
restricted to that bucket's estimated value range.

Mechanism (approximate value reconstruction without order, ApproxValue, an independent attack
requiring i.i.d. uniformly random queries): assumes the database holds at least one record with
value in the range [0.2N, 0.3N] (or its reflection [0.7N, 0.8N]) and uses that anchor record's
observed query-match pattern as a reference to place other records by comparing their match patterns
against it.

### Measured results

| Attack | Result | Conditions |
|---|---|---|
| GeneralizedKKNO (sacrificial epsilon-ADR, generalizing Kellaris et al. to sparse databases) | O(epsilon^-4 log epsilon^-1) queries; generic lower bound Omega(epsilon^-4) | Analytical result; any data density, uniformly random range queries |
| ApproxValue (sacrificial epsilon-ADR, requires a record near the 0.2N-0.3N anchor point) | O(epsilon^-2 log epsilon^-1) queries; generic lower bound Omega(epsilon^-2) | Analytical result; any density given the anchor-record requirement, uniformly random range queries |
| ApproxValue, empirical query count at N = 10^6 with the anchor condition met | 500 queries recover almost all records to within 5% error, versus approximately 10^26 queries the KKNO exact-reconstruction attack would need for the same N | Synthetic data, uniformly random range queries |
| ApproxOrder (sacrificial epsilon-AOR, no query-distribution assumption needed to run) | O(epsilon^-1 log epsilon^-1) queries under a uniform-query assumption used only for the analysis; generic lower bound Omega(epsilon^-1 log epsilon^-1) | Analytical result; any density |
| ApproxOrder, empirical, uniform random range queries | At N = 10^6, after 500 queries the attack fully orders records except those differing by less than 2% of the domain size | Synthetic data, results averaged over 500 databases with 500 randomly sampled queries each |
| ApproxOrder, empirical, fixed-width range queries (width in {100, 250, 500, 1000, 2000, 5000}) | Behaves as predicted by the epsilon^-1 log epsilon^-1 bound after an initial period bottlenecked by sacrificed-record symmetric values, not bucket diameter | R = 1,000 records, N = 10,000 possible values, results averaged over 500 databases per range-query width |
| ADR from AOR plus auxiliary distribution (Algorithm 4), ZIP code dataset | Percent of records recovered to within 25%/50%/75% of N error: 10 queries → 4%/7%/11%; 25 queries → 2%/4%/7%; 50 queries → 1%/3%/6%; 100 queries → 1%/2%/5%. Baseline (guess the median): 15%/27%/37% | US FAA registered-pilot database, over 61,000 records, N = 9,999 (5-digit ZIP codes); auxiliary model = US Census ZIP-code population data (statistical distance from true distribution approximately 0.51); results averaged over 20 randomly generated query transcripts; run on Ubuntu 16.04, Intel Core i7-6700 at 3.4 GHz, Python 2.7, PQ-tree via a C++ library called through SWIG |
| ADR from AOR plus auxiliary distribution (Algorithm 4), salary dataset | Percent of records recovered to within 25%/50%/75% of N error: 10 queries → 2%/4%/7%; 25 queries → 1%/2%/4%; 50 queries → 1%/2%/3%; 100 queries → 1%/2%/3%. Baseline: 2%/5%/9% | California state public-employee salaries from 2016 (over 248,000 records, values 0-762,000 USD, outliers above 500,000 USD truncated), N = 500,000; subsampled to random 10,000-salary databases per trial; auxiliary model = New York state public-employee salaries from the same year (approximately 120,000 records; statistical distance from CA distribution approximately 0.19); results averaged over 10 subsampled databases x 10 query transcripts each |
| ADR headline figures quoted in the abstract | 50 queries recover the first two ZIP-code digits (often identifying a city) for a majority of records; 100 queries on salaries predict a majority to within 10,000 USD | Same ZIP-code and salary datasets and setup as above |
| Prefix-query reconstruction attack, last-name dataset | With approximately 500 prefix queries (mean 315 to reach the grouping condition in 9 of 10 trials): recovers the first character for over 70% of records. With 40,000 queries: recovers first two characters for over 55%. With 3,000,000 queries: recovers first three characters for over 40%, exactly recovering roughly 1,500 three-character last names | Fraternal Order of Police (FOP) database dump (2016), over 600,000 US law-enforcement personnel records; auxiliary data = US Census last-name frequency statistics; theoretical (epsilon-net) sample-complexity predictions for the same three targets were 1,491 / 120,000 / 6,000,000 queries, substantially higher than what the experiment needed |
| Prefix-query attack applied to the FAA ZIP-code dataset instead of last names | Performed poorly | Same ZIP-code dataset as the range-query experiment; degradation attributed by the authors to the auxiliary Census data poorly modeling the ZIP-code distribution |

### Parameters
Sacrificial-order/sacrificial-value error tolerance epsilon: swept as the independent variable in
every experiment (queries-vs-epsilon plots), not fixed to one value. Domain size N: 10,000 in the
fixed-width synthetic experiment, 9,999 for FAA ZIP codes, 500,000 for CA salaries, 10^6 in the
ApproxValue synthetic test. Record count R: 1,000 in the fixed-width synthetic experiment; over
61,000 for FAA ZIP codes; subsampled to 10,000 per trial for CA salaries; over 600,000 for the
last-name dataset. Range-query widths tested for fixed-width queries: 100, 250, 500, 1000, 2000,
5000. Number of query transcripts averaged: 500 databases x 500 queries for the AOR synthetic tests;
20 transcripts for ZIP codes; 10 subsampled databases x 10 transcripts for salaries; 10 trials for
the prefix-query experiment. ApproxValue's anchor-record requirement: at least one record with value
in [0.2N, 0.3N] or its reflection [0.7N, 0.8N]. Hardware for Algorithm 4 and prefix experiments:
Ubuntu 16.04 desktop, Intel Core i7-6700 CPU at 3.4 GHz, Python 2.7, PQ-tree implementation in C++
called via SWIG.

### Stated limitations
The attacks assume the adversary knows the domain size N and the full set of possible queries, but
not the set of records in the database, their count, or that every value in [N] is populated (no
density assumption is required for the general attacks). ApproxValue additionally requires a record
with a value in a specific sub-range of the domain; the authors state this as a mild but real
precondition. The uniform-query-distribution assumption used to state ApproxOrder's O(epsilon^-1 log
epsilon^-1) query bound is used only for the paper's own complexity analysis; running the attack
itself needs no assumption about the query distribution, but the authors note this distinction only
holds cleanly for ApproxOrder, not for ApproxValue or GeneralizedKKNO, which require the queries to
be drawn i.i.d. and uniformly at random to run at all, and the authors state this requirement makes
those two attacks values "as important indicators of what is possible in principle" rather than
"practical, ready-for-use attacks" against a real deployment whose query distribution is unknown and
non-uniform. The heuristic that orients the sorted bucket list (OrientSubsets) chose the wrong
orientation in approximately half of the ZIP-code trials, because the ZIP-code value distribution is
close to flat around the domain midpoint, though the authors note an incorrect choice between only
two possible orientations is "mostly inconsequential" to the eventual error. A fraction of trials
produced a PQ-tree with no Q-node at its first level and were excluded from the reported statistics:
this happened rarely for ZIP codes, in about one-quarter of salary trials at 10 queries, and in about
one-tenth of salary trials at 100 queries; the authors state the attacker can detect this condition
and query further before running the attack. The prefix-query attack performed poorly on the
ZIP-code dataset because the available auxiliary distribution (Census population data) was a poor
model of the true distribution, illustrating that ADR-style attacks needing an auxiliary distribution
degrade when that distribution diverges from the truth. The paper's stated future work: extend the
approach to other query types of practical importance (edit distance, wildcard, substring queries)
and apply further learning-theory results (active or online learning) to access-pattern leakage
attacks and defenses; neither extension is carried out in this paper.

### Requirements it places on the rest of the system
A server or peer implementing an encrypted database that returns record identifiers per query — the
minimal access-pattern leakage this paper attacks — must not treat that leakage as safe merely
because the ciphertext and query content are hidden: the epsilon-AOR attack requires only the
sequence of which stored items matched which range query, nothing about query content or plaintext
values, and no assumption that queries are independent or uniformly distributed. A design offering
range queries over encrypted or access-pattern-observable content should assume an observer with
query-response visibility can recover approximate record order using only O(epsilon^-1 log
epsilon^-1) observed queries, scale-free in both record count and domain size. Converting that order
recovery into approximate value recovery (epsilon-ADR) additionally requires the observer to hold, or
construct, an auxiliary distribution over the value domain that approximates the true one; a system
wanting to bound this specific escalation would need to prevent an observer's access to any such
distribution, which is generally infeasible for public distributions (Census data, published salary
tables). The prefix-query result establishes the same requires-only-access-pattern property extends
to prefix queries under an analogous auxiliary last-name-frequency distribution, so a design using
either range or prefix predicates over leakage-observable stored content faces both attack classes.

### Contradicts
The paper does not contradict a claim of its own predecessors' results; it explicitly generalizes and
extends Kellaris, Kollios, Nissim, O'Neill (KKNO16, CCS 2016) and Lacharite, Minaud, Paterson (LMP18,
IEEE S&P 2018), reproducing LMP's O(N log N) dense-database result as a special case at epsilon =
1/N. No claim commonly attributed to this paper needs correction from the text retrieved. Cross-paper
in this corpus: None found.

### References worth retrieving
- Kellaris, Kollios, Nissim, O'Neill, "Generic attacks on secure outsourced databases," CCS 2016 — foundational (KKNO, first exact range-query reconstruction attack; this paper's generalized version and comparison baseline).
- Lacharite, Minaud, Paterson, "Improved reconstruction attacks on encrypted data using range query leakage," IEEE S&P 2018 — foundational/competing (LMP, direct predecessor whose dense-database O(N log N) result this paper reproduces as a special case and whose auxiliary-distribution attack this paper's epsilon-ADR construction is compared against).
- Kornaropoulos, Papamanthou, Tamassia, "Data recovery on encrypted databases with k-nearest neighbor query leakage," ePrint 2018/719 — competing (approximate reconstruction from a different query class, k-nearest-neighbor).
- Naveed, Kamara, Wright, "Inference attacks on property-preserving encrypted databases," CCS 2015 — attack (auxiliary-distribution inference attack cited as prior use of the auxiliary-distribution technique this paper also relies on).
- Grubbs, Sekniqi, Bindschaedler, Naveed, Ristenpart, "Leakage-abuse attacks against order-revealing encryption," IEEE S&P 2017 — attack (order-leakage attack on a different encryption scheme, order-revealing encryption, cited on the severity of order leakage).
- Cash, Grubbs, Perry, Ristenpart, "Leakage-abuse attacks against searchable encryption," CCS 2015 — foundational (coins the "leakage-abuse attack" category this paper belongs to).
- Zhang, Katz, Papamanthou, "All your queries are belong to us: The power of file-injection attacks on searchable encryption," USENIX Security 2016 — attack (a distinct, file-injection-based attack family on searchable encryption).
- Dautrich Jr., Ravishankar, "Compromising privacy in precise query protocols," EDBT 2013 — foundational (first use of PQ-trees for order-leakage reconstruction, direct predecessor of this paper's PQ-tree method).
- Fuller, Varia, Yerukhimovich, Shen, Hamlin, Gadepally, Shay, Mitchell, Cunningham, "SoK: Cryptographically protected database search," IEEE S&P 2017 — foundational (systematization-of-knowledge survey of the encrypted-database-search field this paper's attacks target).
- Grubbs, McPherson, Naveed, Ristenpart, Shmatikov, "Breaking web applications built on top of encrypted data," CCS 2016 — competing (an applied leakage attack on deployed encrypted-database-backed web applications).
- Bindschaedler, Grubbs, Cash, Ristenpart, Shmatikov, "The tao of inference in privacy-protected databases," VLDB 2018 — competing (inference attack on privacy-protected, not only encrypted, databases).

### Verbatim extracts
"the attack does not use any knowledge on the query distribution."
"50 queries, we can learn the first two digits of a ZIP code."
"only 500 queries (or 24 orders of magnitude fewer than KKNO) are needed."
"FAA ZIP codes are not well-modeled by the census data - their statistical distance is about 0.51."
"important indicators of what is possible in principle... but not as practical, ready-for-use attacks."
