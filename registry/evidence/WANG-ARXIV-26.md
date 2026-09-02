## [WANG-ARXIV-26] Whose Posts Get Ranked: Identical-Text Exposure Gaps in Bluesky Custom Feeds
**Citation:** Yipeng Wang, Mohit Singhal. "Whose Posts Get Ranked: Identical-Text Exposure Gaps in Bluesky Custom Feeds." 20th ACM Conference on Recommender Systems (RecSys '26), September 27-October 02, 2026, Minneapolis, MN, USA. 3 pages. DOI 10.1145/3773078.3841250.
**Retrieved:** full text via https://arxiv.org/abs/2608.13879
**Source URL:** https://arxiv.org/abs/2608.13879
**Domain:** K

### What it does
The paper measures whether Bluesky's user-published custom feeds — independently operated
recommendation services the platform distributes alongside each other, roughly 40,000 of them from
18,000 creators at the time of writing — return byte-identical post text at equal rates across
different authors, using only naturally occurring duplicate posts already in the feeds' ranked
output, without creating test accounts or injecting content.

Data collection: the authors polled the public Top-50 output of Bluesky custom feeds roughly every
10 minutes through the `app.bsky.feed.getFeed` API endpoint, keeping only "complete" snapshots — one
poll of one feed that returned exactly 50 distinct ranks mapped to 50 distinct posts after
deduplication. From this stream they formed "matched sets": groups of posts sharing byte-identical
text but different authors, all present in the candidate pool for the same feed at the same snapshot
time, each post published no more than 7 days before that snapshot, with the group's creation-time
span and age span both capped at 120 minutes (with 60- and 30-minute caps used as robustness checks),
and each group required to contain at least two distinct authors. Byte-exact text matching removes
text content itself as an explanation for any exposure difference within a set.

Exposure was scored per copy by two rank-based weighting functions: reciprocal rank (1/r, the paper's
primary metric) and discounted cumulative gain weight (1/log2(r+1)); a copy absent from the returned
Top-50 list receives zero exposure under both. The authors regressed each copy's reciprocal-rank
exposure on author-history, profile, media, and post-type feature blocks, using matched-set fixed
effects (which absorb every factor common to all copies in a set — the feed, the snapshot time, the
text itself), with standard errors clustered by text group (the set of all posts across all snapshots
sharing that byte-identical text), and controlled the false discovery rate across tests with the
Benjamini-Hochberg procedure, reporting both within-block (q_blk) and across-all-tests (q_all)
corrected significance.

### Measured results

| Finding | Figure | Conditions |
|---|---|---|
| Raw Top-50 posts observed before filtering | 7.3 million distinct posts | Full snapshot stream, unfiltered |
| Complete snapshots retained | 297,093, covering 1,366 distinct feeds | February-April 2026 collection window |
| Matched sets in the main sample | 64,853 | 120-minute creation/age-span cap, byte-exact text matching, at least 2 distinct authors per set |
| Matched sets span | 250 feeds | Same sample |
| Sets where one copy is returned and another is missing | 33% | Main 64,853-set sample |
| Sets where one copy reaches Top-10 and another does not appear at all | 6.8% | Same sample |
| Two-post matched sets with at least one returned copy | 58,318 (89.9% of all 64,853 sets) | Used for Figure 1's rank-pair visualization, same 120-minute cap |
| Average DCG-weight gap between paired copies | 0.102 (mean); up to 0.25 in the most unequal decile | Same two-post-set sample; a 0.25 gap is stated as equivalent to a post's entire DCG weight at rank 15 |
| Better-ranked copy's share of total exposure in its matched set | 66% on average | Same sample |
| Exposure-gap robustness to tighter time-span caps | 0.095 at 60-minute cap, 0.085 at 30-minute cap (versus 0.102 at 120-minute cap) | Same DCG-gap metric, same sample re-filtered at each cap |
| "New author on feed" reciprocal-rank penalty | -0.061 RR (SE 0.020), p=0.003, q_blk=0.023, q_all=0.047, permutation p=0.007 | Fixed-effects regression on the 64,853-set sample; "new" = feed had returned none of that author's posts in the collection logs before this snapshot |
| Prior-exposure effect on current RR | +0.032 RR per natural-log unit of prior same-feed exposure (SE 0.012), p=0.007, q_all=0.078, permutation p=0.012 | Same regression |
| Return-probability penalty for first-time authors under strictest cap | -27 percentage points, q_blk=0.007 | 30-minute time-span cap specification |
| New-author penalty after controlling for copy arrival order | -0.049 RR, p=0.016 | Robustness check adding arrival-order as a control |
| Leave-one-feed-out robustness | all 250 per-feed refits remain negative; 99.6% satisfy p<0.05 | Each of the 250 feeds dropped one at a time and the regression rerun |
| Robustness to excluding the single most-duplicating author | -0.063 RR, p=0.003 (versus -0.061 baseline) | Same regression, that author's posts removed |
| New-vs-previously-returned author head-to-head win rate | new author's copy ranks better only 16% of the time | 6,768 matched sets pairing a new author against a previously returned author |
| New author with more followers, head-to-head loss rate | new author's copy still ranks lower 74% of the time | Subset of 746 matchups where the new author has strictly more followers than the competing author |
| Content/media feature significance | 0 of 304 tested media and post-type features (e.g. has_image, is_reply, hashtag count) pass FDR correction | Same fixed-effects framework, feature-block tests |
| Multiway-cluster p-values for the new-author estimate | exact text: 0.003; +author: 0.007; +feed: 0.028; text+author+feed: 0.024 | Robustness across four clustering specifications |
| Family-wise max-T permutation p-value | 0.017 | Robustness check |
| Frequency concentration within the matched-set sample | most frequent single text: 0.5% of all matched sets; largest single contributing feed: 11% of all matched sets | Descriptive check that no single duplicate text or feed dominates the sample |

### Parameters
| Parameter | Value used | Range tested |
|---|---|---|
| Snapshot polling interval | ~10 minutes | Not varied |
| Snapshot completeness requirement | exactly 50 distinct ranks mapped to 50 distinct posts | Fixed |
| Matched-set text-matching rule | byte-exact match | An unspecified alternate "text-matching rule" is mentioned as one of the robustness checks the two headline estimates were tested against, without the alternate rule's definition given in this 3-page paper |
| Matched-set creation/age-span cap | 120 minutes (main) | 60 and 30 minutes as robustness checks |
| Maximum post age at snapshot time | 7 days | Not varied |
| Minimum distinct authors per matched set | 2 | Not varied |
| Exposure weighting functions | reciprocal rank (main), DCG weight (secondary) | Both reported; RR used for the regression |
| Multiple-comparison correction | Benjamini-Hochberg FDR, both within-block (q_blk) and across all tests (q_all) | Applied to all reported feature-block tests |
| Collection window | February-April 2026 | Not varied |

### Stated limitations
The authors state that most of the custom feeds in their dataset run algorithms that are black boxes
to the observer, so confounding variables affecting exposure cannot be ruled out. They state author
history is left-censored: it is observed only within the collection window, so an author's true prior
history on a given feed before the study began is unknown and any author's measured "new" status may
undercount actual prior exposure that occurred before data collection started. They state that,
although byte-identical text rules out the text itself as an explanation for exposure differences,
copies within a matched set may still differ in media attachments, thread position, or moderation
status, and that the paper examines only observable media factors, finding none of the 304 tested
features statistically significant after correction — leaving unobserved factors (thread position,
moderation status) as an acknowledged possible confound the paper does not measure.

### Requirements it places on the rest of the system
The measurement method requires nothing from Bluesky's protocol beyond the already-public
`app.bsky.feed.getFeed` endpoint returning a feed's current ranked Top-50 list; it requires no
platform cooperation, no test-account creation, and no injected content, because it relies entirely
on duplicate posts that already occur naturally on the platform. The fixed-effects fair-exposure
audit method depends on identical text recurring across multiple authors at comparable ages within
the same feed's candidate pool — a system with no duplicate-post traffic at all (e.g., one enforcing
canonicalization or global deduplication at the protocol layer) would supply this method with no
matched sets to compare, so the technique's applicability is conditional on the target system
tolerating duplicate content. Any component of a "ranking without a global index" architecture that
uses per-author history — return counts, prior appearances on a specific feed — as an input signal
inherits the finding's failure mode directly: this paper shows that signal produces persistent,
statistically robust exposure inequality for otherwise-identical content, independent of follower
count, and independent of the specific feed (the effect holds across all 250 feeds tested
individually).

### Contradicts
None found within this corpus. The paper does not claim its measured penalty reflects intentional
discrimination by feed operators; it presents the correlation between prior exposure and current
exposure as the finding, explicitly comparable in the authors' own words to "popularity-bias feedback
loops observed in centralized recommendation systems," attributed as the authors' own interpretive
framing rather than a separately established causal mechanism in this paper.

### References worth retrieving
- **Balduf, Sokoto, Ascigil, Tyson, Scheuermann, Korczyński, Castro, Król, "Looking AT the Blue Skies of Bluesky," IMC 2024** — foundational/competing measurement of the Bluesky network and feed ecosystem, cited [1]; the paper states this prior work maps the platform and feed ecosystem but does not measure exposure allocation, which is the gap this paper fills.
- **Kleppmann, Frazee, Gold, Graber, Holmgren, Ivy, Johnson, Newbold, Volpert, "Bluesky and the AT Protocol: Usable Decentralized Social Media," DIN 2024** — foundational protocol description, cited [7]; the source for the custom-feed-generator mechanism this paper audits, already flagged from QUELLE-PLOSONE-25's bibliography.
- **Huszár, Ktena, O'Brien, Belli, Schlaikjer, Hardt, "Algorithmic amplification of politics on Twitter," PNAS 2022** — competing/foundational algorithm-audit methodology on a centralized platform, cited [6]; directly comparable amplification-measurement methodology from a non-decentralized system.
- **Singh, Joachims, "Fairness of Exposure in Rankings," KDD 2018** — foundational fair-ranking framework this paper's exposure metric derives from, cited [12].
- **Biega, Gummadi, Weikum, "Equity of Attention: Amortizing Individual Fairness in Rankings," SIGIR 2018** — foundational fair-ranking framework, cited [3].
- **Diaz, Mitra, Ekstrand, Biega, Carterette, "Evaluating Stochastic Rankings with Expected Exposure," CIKM 2020** — foundational exposure-metric methodology, cited [5].
- **Sandvig, Hamilton, Karahalios, Langbort, "Auditing Algorithms: Research Methods for Detecting Discrimination on Internet Platforms," ICA 2014** — foundational algorithm-audit methodology this paper extends to social feeds, cited [11].
- **Singhal, Ling, Paudel, Thota, Kumarswamy, Stringhini, Nilizadeh, "SoK: Content Moderation in Social Media," EuroS&P 2023** — foundational, cited [13] for moderation-status as an unmeasured potential confound; co-authored by this paper's second author.

### Verbatim extracts
"in 33% of sets, one copy appears on the list while another does not" (abstract).
"A new author with more followers than the competing author still loses 74% of head-to-head comparisons" (abstract).
"none are statistically significant" (Section 3, Content features).
"Author history is observed only within our collection window (left-censored)" (Section 3, Limitations).
"resembles the popularity-bias feedback loops observed in centralized recommendation systems" (Section 4, Conclusion).
"feed operators can also apply this method to their own logs to monitor such gaps" (Section 4, Conclusion).
