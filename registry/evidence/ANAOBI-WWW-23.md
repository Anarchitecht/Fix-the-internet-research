## [ANAOBI-WWW-23] Will Admins Cope? Decentralized Moderation in the Fediverse
**Citation:** Ishaku Hassan Anaobi, Aravindh Raman, Ignacio Castro, Haris Bin Zia, Dami Ibosiola, Gareth Tyson. "Will Admins Cope? Decentralized Moderation in the Fediverse." Proceedings of the ACM Web Conference (WWW), 2023.
**Retrieved:** full text
**Source URL:** target record (registry/targets-deduped.json)
**Domain:** K

### What it does
The paper measures the moderation workload carried by Pleroma instance administrators in the Fediverse (a federation of independently operated servers exchanging posts through ActivityPub-style federation) and builds WatchGen, a classifier that predicts which federated instances an administrator will later apply a moderation policy against. Pleroma exposes federation policies: administrator-configured rule-action pairs that act on incoming posts, users, or entire remote instances (for example, rejecting all posts from a given remote instance, or tagging posts above a certain age). WatchGen extracts per-instance features (post volume, hate-word counts, URL counts, mention counts, prior policy actions) from each instance's public API and its federated peers' data, trains a classifier on instances that later had a policy applied against them, and outputs a ranked watchlist an administrator can act on before applying a policy manually.

### Measured results
| Metric | Value | Conditions |
|---|---|---|
| Instances discovered by crawling distsn.org and the-federation.info, then federation-peer enumeration | 9,981 total instances found (2,407 Pleroma, remainder non-Pleroma such as Mastodon) | 16 Dec 2020 - 19 Oct 2021, metadata polled every 4 hours via each instance's public API |
| Instances with retrievable metadata | 1,740 of 2,407 Pleroma instances (72.28%) | Failure causes for the remaining 667: 65.1% non-existent domain, 17.9% HTTP 404, 6.4% HTTP 403 (private timeline), 4.5% HTTP 502, 1.3% HTTP 503, under 1% HTTP 410 |
| Instances exposing policy information | 93.2% of the 1,740, covering 94.2% of users and 94.5% of posts | Same dataset |
| Unique policy types observed | 49 | Same dataset |
| Instances still on default (unconfigured) policy set | 66.9% | Same dataset, end of measurement period |
| Instances managed by exactly one administrator | 71.6% of 1,633 instances that expose administrator information (93.8% of 1,740) | Total of 2,111 unique administrators observed |
| Post-to-administrator ratio for multi-administrator instances vs. single-administrator instances | 6:1 (more posts per added administrator on average) | Driven by a small number of instances, notably poa.st |
| Correlation of post growth to administrator-count growth | Spearman coefficient 0.19 (weak) | Growth measured per instance over the 10-month period; only 6.9% of instances added any administrator during the period |
| Aggregate post growth vs. administrator growth | 60.3% increase in posts, 35.6% growth in administrators | Same 10-month period, aggregate across all 1,740 instances |
| Policy volume difference tied to administrator growth | Instances that added administrators applied 1.5x more policies overall, 1.8x more `reject` policy actions, and received 4x more policies applied against them by other instances | Comparison is instances with administrator growth vs. instances without, same dataset |
| Average delay from federation to first policy application against a newly federated instance | 82.3 days | Computed from time between an instance's federation date and the date a `SimplePolicy` action was first applied against it; 55% of federations that predate the measurement window are excluded because their federation timestamp is unknown |
| Delay for "top 10" most-targeted instances vs. "bottom 10" least-targeted instances | 59.5 days (top 10) vs. 74.7 days (bottom 10) | Same delay metric, subset by number of policies received |
| Delay for specific controversial instances | gab.com: 19 days average; neckbeard.xyz: up to 98.4 days average | Same delay metric; neckbeard.xyz grew by 789.4k posts and kiwifarms.cc by 469.2k posts during the measurement window |
| Instances that delegate moderation to an account distinct from the administrator | 3.5% of the 1,740 instances (29 of 819 instances that expose moderator role information; a further 72 assign the moderator role to an account that is also an administrator) | Same dataset |
| Effect of having a dedicated (non-administrator) moderator | Instances with a dedicated moderator take 103 days on average to apply a `SimplePolicy` action after federation, vs. 111 days without one; 38% of instances with a dedicated moderator apply zero `SimplePolicy` actions, vs. 70% without one | Same dataset |
| WatchGen, global training pool, full 38-feature set (16 retained as most determinant), 80:20 train/test split, 5-fold cross-validated grid search over hyperparameters, sklearn | Random Forest: accuracy 0.92, precision 0.88, recall 0.68, F1 0.77 (best of 4 models tested); Logistic Regression F1 0.49; Multi-Layer Perceptron F1 0.53; Gradient Boosted Trees F1 0.71 | Predicting whether any policy will later be applied against a given instance by any other instance |
| WatchGen, global pool, excluding the two post-volume features (posts, transformed posts) | Random Forest F1 drops from 0.77 to 0.62 | Same task, isolating the contribution of post-volume features |
| WatchGen, time-windowed training (1 to 9 months of data, remainder held out as test) | Best F1 reached at month 5 for Gradient Boosted Trees and month 7 for Random Forest | Month 10 excluded for insufficient remaining test data |
| WatchGen, per-instance local model (each instance trains only on its own federated peers' data, first 8 months train / last 2 months test) | Mean F1 0.55 across instances; 42.6% of instances reach F1 >= 0.6; 8.3% of instances fall below F1 0.4 | Decentralized training variant, one independent model per instance, using Random Forest (the best global-model algorithm) |
| Relationship between local training-set size and local model performance | 65.4% of instances with F1 >= 0.6 have over 50,000 local posts; only 4.4% of instances with F1 < 0.6 have over 50,000 local posts | Same decentralized-training experiment |

### Parameters
- Data-collection window: 16 December 2020 to 19 October 2021 (10 months), metadata polled every 4 hours per instance.
- Logistic Regression: regularization parameter C tuned over {0.001, 0.01, 0.1, 1, 10, 100, 1000}.
- Multilayer Perceptron: single hidden layer, hidden-layer size in {10, 50, 100}; activation function in {relu, tanh, logistic}; learning-rate schedule in {constant, invscaling, adaptive}.
- Random Forest: n_estimators in {5, 50, 250}; max_depth in {2, 4, 8, 16, 32, None}.
- Gradient Boosted Trees: n_estimators in {5, 50, 250, 500}; max_depth in {1, 3, 5, 7, 9}; learning rate in {0.01, 0.1, 1, 10, 100}.
- Feature set: 38 extracted features distilled by manual experimentation to 16 retained as most determinant (full list in the paper's Table 5, including post count, hate-word count from hatebase.org, URL count, mention count, hashtag count, and per-policy action counts).
- Global-model split: 80:20 train/test.
- Local-model split: first 8 months train, last 2 months test, per instance, using only that instance's federated peers as training data.

### Stated limitations
The authors state their delay metric is "a rudimentary proxy" for how long it takes an administrator to identify a problem, and that many unmeasured factors could explain the observed delay. WatchGen's global-pool variant assumes a central broker aggregating training data from all instances, which the authors state may be infeasible given the decentralized nature of the Fediverse; the local variant they test as an alternative shows a mean F1 of 0.55, a measured drop from the global model's 0.77, attributed to the reduced per-instance training-set size. The paper covers Pleroma instances only; the authors state as future work that they intend to extend the study to other Fediverse platforms, specifically Mastodon and PeerTube. The dataset excludes federations that predate the measurement window (55% of observed federations) from the delay analysis because their federation timestamp cannot be determined. The study observes only the policies administrators set and does not examine other administrator behavior, such as individual posts they author.

### Requirements it places on the rest of the system
WatchGen's global (central-broker) variant requires a component that can aggregate per-instance moderation-relevant metadata (post counts, hate-word counts, prior policy actions, user counts) across all participating instances into one training pool; this conflicts with a design in which no party holds a global view of instance activity. The local (decentralized) variant instead requires each instance to observe federation-relevant metadata only from its own federated peers, and produces materially worse prediction accuracy (F1 0.55 vs. 0.77) as a measured consequence of the smaller per-instance training set. Any system reusing the feature set needs instances to expose post content signals (hate-word matches via a wordlist such as hatebase.org, URL counts, mention counts) and prior policy-action history through a public API, the way Pleroma instances do. The predicted signal (whether an instance will later have a policy applied against it) is trained against administrators' actual historical policy decisions, so the mechanism reproduces existing administrator judgment rather than an independent measure of harm.

### Contradicts
None found.

### References worth retrieving
- Zia, Raman, Castro, Anaobi, De Cristofaro, Sastry, Tyson. "Toxicity in the decentralized web and the potential for model sharing." ACM SIGMETRICS, 2022. — foundational (same author group's prior study of toxicity in Pleroma, and of federation policies).
- Raman et al. "Challenges in the Decentralised Web: The Mastodon Case" (cited as ref [39] for Mastodon infrastructure and resilience). — foundational.
- Zignani, Gaito, Rossi. "Follow the 'Mastodon': Structure and Evolution of a Decentralized Online Social Network." ICWSM, 2018. — foundational (Mastodon social-graph structure, comparison point for a non-Pleroma Fediverse platform).
- Bielenberg et al. on Diaspora growth, topology, and server reliability (cited as ref [4]). — competing/comparison (a different decentralized social network's measured reliability and topology).
- Trautwein et al. on IPFS (InterPlanetary File System). — foundational (decentralized storage measurement, cited as a comparison decentralized-system study).
- Cheng et al. (ref [25]), cited for using random forest and logistic regression to predict whether a user will be banned, reducing moderator load. — competing (a centralized-platform ban-prediction classifier, directly comparable to WatchGen's task).

### Verbatim extracts
- "It takes administrators an average of 82.3 days to apply any form of policy against other instances."
- "only 3.5% of instances have dedicated account(s) assigned the role of moderator."
- "Random Forest being the best performing model (f1=0.77)."
- "instances with multiple administrators have more posts, with a ratio of 6:1."
