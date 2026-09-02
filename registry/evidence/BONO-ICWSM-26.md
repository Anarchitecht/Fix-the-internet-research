## [BONO-ICWSM-26] Self-Moderation in the Decentralized Era: Decoding Blocking Behavior on Bluesky
**Citation:** Carlo Alberto Bono, Nick Liu, Giuseppe Russo, Francesco Pierri. "Self-moderation in the Decentralized Era: Decoding Blocking Behavior on Bluesky." Proceedings of the International AAAI Conference on Web and Social Media (ICWSM), 2026.
**Retrieved:** full text
**Source URL:** target record (registry/targets-deduped.json)
**Domain:** K

### What it does
The paper measures whether a Bluesky user's likelihood of being blocked by other users can be predicted from that user's own in-platform behavior, without access to the block target's own account or any moderation label. Bluesky (a social network built on the AT Protocol) exposes a public Firehose feed that streams every user action, including block events, because blocking on Bluesky is public rather than private, unlike on most centralized platforms. The authors build one behavioral profile per user from 86 numerical features grouped into five categories: Action (counts of like, post, repost, and follow create/delete events), Derived (counts of actions received by the user, such as being liked or followed), Post-derived (character, digit, emoji, and language statistics of the user's posts, plus Detoxify toxicity scores), Domain-derived (Media Bias/Fact Check ratings and a domain-quality score for URLs the user shared), and Graph-based (coreness, degree, and PageRank centrality of the user in the follow, like, reply, and repost networks). They define two target variables, the raw count of blocks a user received and that count normalized by the user's post count, and train an XGBoost Random Forest classifier (binary: is the user in the blocked class above a given quantile threshold) and two regressors (XGBRFRegressor and AutoGluon TabularPredictor) to predict them, with SHAP (SHapley Additive exPlanations) used to attribute predictions to individual features.

### Measured results
| Metric | Value | Conditions |
|---|---|---|
| Dataset scale | 3,278,406 blocks; 33,942,018 follow actions; 292,388,501 likes; 79,737,148 posts; 30,284,394 reposts; 1,979,713 unique users | June 1 - August 28, 2024 (about three months), collected continuously via Bluesky's public Firehose endpoint (com.atproto.sync.subscribeRepos) |
| Users analyzed | 427,118 | Subset of the 1,979,713 unique users with at least 10 posts during the observation period and posts predominantly in English |
| Daily action medians | Likes 3,240,712; posts 873,760; reposts 338,544; follows 248,255; blocks 31,934 (several orders of magnitude below the other action types) | Same three-month window |
| Per-user action medians | Blocks issued = 2; follows = 2; likes = 8; posts = 6; reposts = 4 | Same window, per-user distributions, all heavy-tailed |
| Extreme per-user outliers | Up to 74,000 blocks issued, 517,000 likes, 145,000 follows, 316,000 original posts, 82,000 reposts by single users | Same window |
| Distribution of blocks received | 90% of the 427,118 analyzed users received fewer than 10 blocks; approximately 0.6% received over 100 blocks | Same window, users with >=10 posts only |
| Correlation of total user activity with blocks received | Pearson R=0.55, Spearman R=0.53 (log10 blocks vs. total actions) | Same 427,118-user set, binned into 100 bins with bootstrapped 95% confidence intervals |
| Correlation of average post toxicity (Detoxify) with blocks received | Pearson R=0.20, Spearman R=0.23 | Same analysis; no clear relationship found between low-credibility URL sharing and blocks received |
| Binary classification, all 86 features, XGBoost Random Forest with 500 estimators, 10 runs of 10-fold cross-validation, class-balanced by undersampling | Max ROC AUC 0.892 (raw block count target) and 0.875 (activity-normalized block count target) | Reported at the best-performing quantile threshold; label thresholds swept across percentiles from 0.1 to 0.9995 of the two target distributions |
| Single-feature-group classifiers (Action, Derived, or Graph groups alone) | Up to AUC 0.856 (raw) and 0.846 (normalized) | Same setup, isolating one feature group at a time; Domain and Posts groups alone perform worse, with normalized-setting AUC below 0.7 |
| Feature-group ablation (all features except one group) | Removing Action or Post features causes the largest AUC decline, approximately -5 percentage points; other single-group removals are comparable to the full model | Same 10-run, 10-fold cross-validation setup |
| Feature-count ablation (best-n vs. worst-n features by SHAP rank) | At higher thresholds, 4 of the best-ranked features reach near-maximum AUC; matching that AUC using worst-ranked features requires at least 64 features | Same classification setup, both raw and normalized settings |
| Regression, raw block count | AutoGluon TabularPredictor R^2 = 0.55; XGBRFRegressor R^2 = 0.15 | 80:20 random train-test split, three-month dataset |
| Regression, activity-normalized block count | AutoGluon TabularPredictor R^2 = 0.50; XGBRFRegressor R^2 = 0.22 | Same split; AutoGluon training took about one hour vs. under one minute for XGBRFRegressor |
| Regression practical accuracy | Approximately 84% of users with zero raw blocks were correctly predicted to receive fewer than one block | Same regression setup |

### Parameters
- Observation window: June 1, 2024 to August 28, 2024 (about three months).
- User inclusion threshold: at least 10 posts during the window, posts predominantly in a supported language (Detoxify covers 'en', 'pt', 'ru', 'es', 'fr', 'tr', 'it'), and predominantly English for the toxicity-feature computation.
- Feature count: 86 total, in 5 groups (18 Action, 27 Post-derived including 14 toxicity-related, 27 Domain/URL-derived, 14 Graph-based; exact per-group counts per the paper's Table 2 sum to 86).
- Classifier: XGBoost Random Forest, 500 estimators; evaluated as the average of 10 independent runs of 10-fold cross-validation; majority class randomly undersampled to balance labels.
- Classification thresholds tested: percentile cuts at 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 0.995, 0.999, 0.9995 of the raw and normalized block-count distributions.
- Regression models: XGBRFRegressor and AutoGluon TabularPredictor ("high quality" setting), 80:20 train-test split, evaluated with R^2 and Mean Absolute Error.
- Feature importance: SHAP, model-agnostic local attribution.

### Stated limitations
The authors state the three-month observation window may not capture long-term trends or seasonal variation, and that behavior is aggregated statically over the whole period rather than analyzed as a time series. They state the feature set, while large, is "simple," omitting text embeddings or graph embeddings that could raise predictive power, and that alternative toxicity-assessment approaches distinguishing content types (replies vs. reposts) and covering more languages were not explored. The study identifies behavioral correlates of being blocked but does not investigate the motivations behind blocking, such as harassment or misinformation. The analysis is restricted to users who interact predominantly in English, which the authors state may not represent global user behavior, and the Bluesky user base itself is not necessarily representative of other platforms. The models are retrospective: they classify and estimate existing block counts and do not predict future blocking events; the authors state this prospective-prediction task is left for future work. Features are not normalized by account age, so users who joined during the observation window have shorter behavioral histories that are not corrected for. Both regression models underperform for the most heavily blocked users, a comparatively rare group, though the authors note this is a minor practical concern because median block counts are low.

### Requirements it places on the rest of the system
The mechanism requires a data source that streams every block action publicly and in real time, the way Bluesky's Firehose does; the authors state explicitly that this data is typically inaccessible on other platforms, including on another decentralized platform, Mastodon, where blocks are not similarly exposed. The feature set requires access to each user's full action history (likes, posts, reposts, follows, blocks, both created and received) and to derived social-graph structure (centrality in four separate interaction networks), so a system that only logs the block event itself, without the blocking and blocked users' surrounding activity, cannot reproduce the classifier's inputs. The toxicity features require running a pretrained text classifier (Detoxify) over each user's post history, and the domain features require access to an external URL-reputation source (Media Bias/Fact Check ratings and a separately cited domain-quality score). The classifier is trained and evaluated retrospectively against blocks that have already occurred, so it presupposes an existing, functioning blocking mechanism as ground truth and does not itself generate a moderation decision.

### Contradicts
None found.

### References worth retrieving
- Ali, Saeed, Aldreabi, Blackburn, De Cristofaro, Zannettou, Stringhini. "Understanding the Effect of Deplatforming on Social Networks." WebSci 2021. — competing (deplatforming measurement on a different, centralized-adjacent target).
- Balduf, Sokoto, Ascigil, Tyson, Scheuermann, Korczynski, Castro, Krol. "Looking AT the Blue Skies of Bluesky." ACM Internet Measurement Conference (IMC), 2024. — foundational (independent large-scale Bluesky measurement, infrastructure and user-base characterization).
- Failla, Rossetti. "'I'm in the Bluesky Tonight': Insights from a year worth of social data." PLOS One, 2024. — foundational (competing/complementary Bluesky-scale dataset, 4 million users and 235 million posts cited directly in this paper's related work).
- Balduf, Sokoto, Baronchelli, Castro, Krol, Tyson, Pavlou, Scheuermann, Ascigil. "Bootstrapping Social Networks: Lessons from Bluesky Starter Packs." ICWSM 2025. — foundational (Bluesky network-formation measurement).
- Bono, La Cava, Luceri, Pierri. "An Exploration of Decentralized Moderation on Mastodon." WebSci 2024. — already in this corpus (BONO-WEBSCI-24), same lead author.
- Zia, He, Raman, Castro, Sastry, Tyson. "Flocking to Mastodon: Tracking the great Twitter migration." arXiv:2302.14294. — foundational (Fediverse migration measurement, comparison decentralized platform).
- Chandrasekharan, Pavalanathan, Srinivasan, Glynn, Eisenstein, Gilbert. "You can't stay here: The efficacy of Reddit's 2015 ban examined through hate speech." Proc. ACM Hum.-Comput. Interact. (CSCW), 2017. — competing (centralized-platform ban-effectiveness measurement, comparison case for a different self/instance-moderation mechanism).
- Jhaver, Boylston, Yang, Bruckman. "Evaluating the effectiveness of deplatforming as a moderation strategy on Twitter." Proc. ACM Hum.-Comput. Interact. (CSCW), 2021. — competing.
- Horta Ribeiro, Jhaver, Zannettou, Blackburn, Stringhini, De Cristofaro, West. "Do platform migrations compromise content moderation? Evidence from r/the_donald and r/incels." Proc. ACM Hum.-Comput. Interact. (CSCW), 2021. — attack/critique (evidence that migration undermines a moderation intervention's effect).

### Verbatim extracts
- "analyzing more than 100M actions by nearly 2M users over three months"
- "we achieve high accuracy in binary classification (AUROC>0.85)"
- "block actions are significantly less common, with a daily median of 31 934"
- "approximately 84% of users with zero raw_blocked blocks are correctly predicted"
- "blocks on Bluesky are public"
