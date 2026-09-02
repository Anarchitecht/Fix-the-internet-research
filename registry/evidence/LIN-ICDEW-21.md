## [LIN-ICDEW-21] Measuring Decentralization in Bitcoin and Ethereum using Multiple Metrics and Granularities

**Citation:** Qinwei Lin, Chao Li, Xifeng Zhao, Xianhai Chen. "Measuring Decentralization in Bitcoin and Ethereum using Multiple Metrics and Granularities." IEEE ICDE Workshops, 2021. DOI 10.1109/ICDEW53142.2021.00022.
**Retrieved:** full text via https://doi.org/10.1109/ICDEW53142.2021.00022 (also posted as arXiv:2101.10699)
**Source URL:** https://doi.org/10.1109/ICDEW53142.2021.00022
**Domain:** J

### What it does
The paper quantifies how concentrated block-production power is in Bitcoin and Ethereum over a full year, using three independent statistics computed at three time granularities, then adds a windowing method that avoids missing concentration spikes that fall across a fixed-interval boundary. Blocks are collected via Google BigQuery, a hosted service exposing an Application Programming Interface (a defined set of callable operations) over prebuilt blockchain datasets. The Gini coefficient (an inequality measure) is computed over the distribution of blocks produced by each distinct block producer within a window, giving a value from 0 (equal production) toward 1 (one producer dominates); the paper's own formula sums pairwise absolute differences in block counts across all producer pairs, divides by twice the number of producers times the total blocks produced. Shannon entropy (a measure of the unpredictability of a probability distribution) is computed over the same per-producer block-count distribution treated as a probability distribution, so a higher value means block production is spread more unpredictably across producers. The Nakamoto coefficient is the minimum number of distinct producers whose combined block share reaches 51% of all blocks in the window, so a higher value means more producers would need to combine to reach majority control. Two windowing methods are applied to each metric: fixed windows, which partition the year into non-overlapping day-, week-, or month-length intervals and compute one metric value per interval; and sliding windows, which use the same day/week/month length but advance the window by half its length each step, so consecutive windows overlap by half their length and a concentration event spanning a boundary between two fixed intervals appears fully within at least one sliding window instead of being split and diluted across two.

### Measured results
| Metric / chain | Fixed-window result | Sliding-window result |
|---|---|---|
| Gini coefficient, Bitcoin | Monthly values reach close to 0.90 in the first three months and are always higher than daily/weekly; daily values mostly 0.45-0.60, with extreme values near 0.25 in the first three months | Average of 0.523 (one-day windows), 0.667 (one-week), 0.760 (one-month) |
| Gini coefficient, Ethereum | Same ordering as Bitcoin (monthly > weekly > daily) but higher and more stable overall than Bitcoin's values | Average of 0.837 (one-day), 0.878 (one-week), 0.916 (one-month) |
| Shannon entropy, Bitcoin | Daily, weekly, monthly patterns are close to each other; daily entropy mostly in 3.5-4.0, with extreme values above 5.5, concentrated in the first two months | Average of 3.810 (one-day), 4.002 (one-week), 4.091 (one-month); more extreme values (>5.0) revealed than fixed-window results |
| Shannon entropy, Ethereum | Mostly within 3.3-3.5 across all granularities | Average of 3.420 (one-day), 3.433 (one-week), 3.445 (one-month) |
| Nakamoto coefficient, Bitcoin | Stable at 4 from day 100 to day 260; oscillates between 4 and 5 outside that range; daily values in the first 50 days reach above 35 at their highest | Mostly between 4 and 5; an abnormal spike at sliding-window position N=120 (approximately day 60) visible only in the sliding-window results, not the fixed-window results |
| Nakamoto coefficient, Ethereum | Fluctuates between 2 and 3 across all granularities | Majority of values between 2 and 3 |
| Data volume | 54,231 Bitcoin blocks collected, block numbers 556,459 to 610,690, all produced in 2019 | Sliding-window sizes: 144 blocks (approx. one day at Bitcoin's 10-minutes-per-block rate), 1,008 (one week), 4,320 (one month) |
| Data volume | 2,204,650 Ethereum blocks collected, block numbers 6,988,615 to 9,193,265, all produced in 2019 | Sliding-window sizes: 6,000 blocks (one day, at Ethereum's measured average of 6,000 blocks/day), 42,000 (one week), 180,000 (one month) |
| Named anomaly, Bitcoin day 14 (Jan. 14, 2019) | Daily Gini coefficient 0.34 and daily Shannon entropy 6.2, both extreme values, traced to two specific blocks (numbers 558,473 and 558,545) each containing more than 80-90 independent coinbase addresses, producing more than 80 distinct block producers on a day with only 148 total blocks | Not applicable to this entry (fixed-window observation) |

### Parameters
- Measurement year: 2019, for both chains
- Fixed-window granularities: day, week, month
- Sliding-window step length: half the window length, chosen "to simplify and clarify the main point of the sliding window based measurement approach" (the paper's own stated reason, not derived from any optimization)
- Bitcoin block production rate assumption: 10 minutes per block, used to derive the 144/1,008/4,320-block window sizes
- Ethereum block production rate: measured at 6,000 blocks/day average across the 2019 dataset, used to derive the 6,000/42,000/180,000-block window sizes
- Nakamoto-coefficient collusion threshold: 51% of overall mining power, cited from Srinivasan's original definition
- Formula for the number of sliding-window measurements: L = (S - N) / M + 1, where S is total blocks measured, N is window length, M is step length

### Stated limitations
The authors state that most prior decentralization measurement work used a single metric, a single granularity, or blocks from only one week, producing a snapshot rather than a continuous picture; this paper's stated contribution is multiple metrics, multiple granularities, and a full year of data, not a claim to have resolved every measurement question. The sliding-window approach is presented, by the authors' own description, as a response to a specific failure of short fixed windows: reducing fixed-window length to catch cross-interval events makes the metric overly sensitive to short-term fluctuations that do not reflect an actual change in mining-power distribution (their example: a miner with 10% of overall mining power that mines 30% of blocks within one particular day of an otherwise-normal week). The paper draws no causal conclusion about why Bitcoin is more decentralized than Ethereum in these measurements beyond noting the block-production-rate difference as a candidate explanation for part of the Gini-coefficient gap; the authors do not test that explanation directly. No admission-control, incentive, or attack analysis is offered; the paper measures only observed concentration, not why concentration arose or what would reduce it.

### Requirements it places on the rest of the system
This is a measurement study of two already-deployed Proof-of-Work blockchains and places no mechanical requirement on other system components; it is evidence about deployed decentralization outcomes, usable to compare against a design's own stated production-diversity target. A design that wants to reproduce or extend this measurement needs an equivalent block-producer identity signal; the paper computes its metrics over the distribution of blocks by producer address, so any comparable measurement of a different system requires a similarly reliable mapping from a produced block to the identity of its producer, which the paper obtains directly from each chain's own block-header data via Google BigQuery, not from a self-reported or inferred source.

### Contradicts
None found within this corpus. The paper itself cites Wu, Peng, Xie, Huang (ICEIEC 2019, ref. [20]) as concluding "Bitcoin is usually more decentralized than Ethereum" using Shannon entropy alone, a conclusion this paper's multi-metric, multi-granularity results are stated to agree with rather than contradict. The paper also cites Gencer, Basu, Eyal, Van Renesse, Sirer (Financial Cryptography and Data Security 2018, ref. [5]) as finding "Bitcoin and Ethereum have fairly centralized mining processes," which this paper's Nakamoto-coefficient results (4-5 for Bitcoin, 2-3 for Ethereum) are consistent with, not contrary to.

### References worth retrieving
- foundational: Srinivasan, "Quantifying decentralization," 2017 (informal publication, cited as ref. [16]) — origin of the Nakamoto coefficient this paper uses as its third metric
- foundational: Eyal, Sirer, "Majority is not enough: Bitcoin mining is vulnerable," Financial Cryptography and Data Security 2014, pp. 436-454 — introduces selfish mining, cited as lowering the practical threshold for a 51% attack to 33% of mining power
- foundational: Kwon, Liu, Kim, Song, Kim, "Impossibility of full decentralization in permissionless blockchains," ACM Advances in Financial Technologies 2019, pp. 110-123 — cited as the source of the Gini-coefficient application to mining-power distribution
- competing: Wu, Peng, Xie, Huang, "An information entropy method to quantify the degrees of decentralization for blockchain systems," IEEE ICEIEC 2019, pp. 1-6 — prior single-metric (Shannon entropy only) Bitcoin/Ethereum comparison whose conclusion this paper extends with two additional metrics and three granularities
- competing: Gencer, Basu, Eyal, Van Renesse, Sirer, "Decentralization in Bitcoin and Ethereum networks," Financial Cryptography and Data Security 2018, pp. 439-457 — application-layer/network-measurement comparison of the two chains, cited for finding Bitcoin has higher network capacity but more datacenter-clustered nodes than Ethereum
- competing: Li, Palanisamy, "Comparison of decentralization in DPoS and PoW blockchains," International Conference on Blockchain 2020, pp. 18-32 — prior work by an overlapping author comparing decentralization across a different consensus-mechanism boundary (Delegated Proof of Stake versus Proof of Work)
- foundational/attack: Eyal, "The miner's dilemma," IEEE S&P 2015, pp. 89-103 — game-theoretic analysis of mining-pool competition and block-withholding attacks, cited as motivation for why mining-power concentration matters for security
- independent-measurement: Wang, Chu, Yang, "Measurement and analysis of the Bitcoin networks: a view from mining pools," arXiv:1902.07549, 2019 — tracked over 1.56 million blocks and roughly 257 million historical transactions, cited as finding a few mining pools controlling and expected to keep controlling most Bitcoin computing resources
- attack/critique: Gervais, Karame, Capkun, Capkun, "Is Bitcoin a decentralized currency?", IEEE Security & Privacy 12(3), 2014, pp. 54-60 — analyzes Bitcoin centralization across web wallets, protocol maintenance, and blockchain forks

### Verbatim extracts
- "the degree of decentralization in Bitcoin is higher, while the degree of decentralization in Ethereum is more stable"
- "the use of sliding windows could reveal additional cross-interval information overlooked by the fixed window based measurements"
- "a lower Gini coefficient means that more miners need to collude to compromise a blockchain system"
- "Nakamoto coefficient is defined as the minimum number of entities required to collude for gathering over 51% of the overall mining power"
- "we found two abnormal blocks... containing more than 80 independent coinbase addresses"
- "Ethereum tends to be signiﬁcantly less decentralized in terms of the measurements of the Gini coefficient"
