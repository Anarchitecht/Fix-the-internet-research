## [GOLLE-EC-01] Incentives for Sharing in Peer-to-Peer Networks

**Citation:** Philippe Golle, Kevin Leyton-Brown, Ilya Mironov. "Incentives for Sharing in Peer-to-Peer Networks." ACM Conference on Electronic Commerce (EC), 2001. DOI 10.1145/501158.501193.
**Retrieved:** full text via https://crypto.stanford.edu/~pgolle/papers/share.pdf
**Source URL:** https://crypto.stanford.edu/~pgolle/papers/share.pdf
**Domain:** I

### What it does

The paper predicts, for a set of candidate reward mechanisms, whether rational agents settle into an equilibrium in which files are shared or one in which nobody shares, by modeling file exchange as a repeated game and solving for Nash equilibria. Each agent, in each fixed-length time period, chooses a sharing level (none, moderate, or full) and a downloading level (none, moderate, or heavy). An agent's utility sums five components: value from downloaded volume, value from the variety of files available on the network, a negative term for disk space committed to shared files, a negative term for bandwidth consumed by uploads, and an optional altruism term. A mechanism assigns each agent, at the end of a period, a financial transfer that depends on that agent's observed sharing and downloading actions; the paper analyzes the equilibrium each transfer rule induces. Under the baseline case (no financial transfer, mapped to the actual unmodified Napster system), sharing nothing while downloading without limit is a strongly dominant strategy for a non-altruistic agent, so the unique equilibrium is zero sharing. Three transfer-rule families are then analyzed to break this equilibrium: a micro-payment mechanism that charges a fixed monetary amount per file downloaded and credits the same amount per file uploaded, a quantized variant of the same mechanism that bills downloads in fixed-size blocks rather than per file, and a point-based mechanism using an internal unit that an agent can acquire either with money or by uploading but cannot convert back into money. A further variant rewards agents in points proportional to the megabyte-time integral of the files they make available for download, rather than in proportion to completed uploads, to reward availability rather than completed transfers.

### Measured results

The paper's headline results are proofs of equilibria, not measurements; the entries below are the values proved to hold under each mechanism's assumptions, followed by the one empirical set of results, from a multi-agent Q-learning simulation.

| Mechanism | Equilibrium proved | Conditions |
|---|---|---|
| No financial transfer (baseline, models unmodified Napster) | Unique equilibrium is full downloading with zero sharing, for any non-altruistic agent | Assumes all agents share one utility function type; holds regardless of agent altruism level for altruism below the sharing cost |
| Per-file micro-payment, coefficient alpha per file | Unique strong equilibrium is full sharing and full downloading by every agent | Requires the per-file download utility to exceed alpha, and the per-file cost of uploading (disk plus bandwidth disutility) to be less than alpha; holds for any number of agents n |
| Points-based micro-payment (non-convertible internal unit) | Same equilibrium as monetary micro-payments when agents' desired download level exceeds the middle sharing tier; a different equilibrium, moderate sharing and moderate downloading by all agents, when agents have no desire to download above the middle tier | Same structural assumptions as the monetary case, substituted with point-denominated costs and rewards |

Simulation results (Q-learning agents, temporal-difference update with decay parameter and future-income discount both fixed strictly between 0 and 1; agent parameters for disk space, file-type preference, altruism, and money-utility scaling drawn from stated uniform ranges each run):

- Both the micro-payment and point-based mechanisms converge to a stable strategy distribution (measured as frequency of strategy change dropping toward zero) within roughly 4,000 to 5,000 simulated time periods (epochs); the unmodified-Napster baseline is plotted alongside for comparison in the same figure and converges to zero sharing.
- Agent utility for money was modeled as U(x) = A * ln(1 + x/A), with A the sole free parameter; as A increases the function approaches linear (risk-neutral) behavior, and lower A models stronger risk aversion. Under the micro-payment mechanism, lowering A (increasing risk aversion) reduces the number of files shared in the system, over an A range plotted from roughly 400 to 900.
- Enlarging each agent's action space from 9 to 35 available strategies changed the absolute payoffs agents achieved but did not change the qualitative equilibrium result, compared across two otherwise-identical simulation runs.
- In the point-based reward-for-availability mechanism, as the fraction of altruistic agents in the population rises from 0 to 1, non-altruistic agents increase both their downloading and, to compensate for the point cost, their sharing; measured as average files shared by non-altruistic agents against fraction of altruistic agents, for two settings of action-space size ("few choices" and "more choices").
- A further experiment (graph omitted from the paper for space) varied the monetary price of points agents must acquire to cover a negative point balance: at price zero agents behave as under unmodified Napster; as price rises agents share more; at higher price agents also reduce downloading, avoiding a large negative point balance.

### Parameters

- Sharing levels per agent per period: three discrete levels, no sharing / moderate / full.
- Downloading levels per agent per period: three discrete levels, no downloading / moderate / heavy.
- Micro-payment coefficient alpha: a monetary cost/reward per file, given as an example value of $0.05 per file; the formal analysis leaves alpha as a free parameter subject to the two inequality constraints stated above.
- Quantization block size b (quantized micro-payment mechanism): a fixed parameter; b = 1 reduces to the unquantized micro-payment mechanism, and the mechanism approaches flat-rate pricing as b grows, with no specific numeric value tested beyond the two limiting cases.
- Availability-reward coefficient c: number of hours a newly downloaded file must be shared for the download's point cost to be offset; set to c = 1 in the equilibrium analysis and the simulation.
- Simulation agent parameters: disk space drawn uniformly from a stated interval [DSmin, DSmax]; altruism utility-per-file drawn uniformly from [ALmin, ALmax]; a download-utility scaling factor drawn uniformly from [MAmin, MAmax]; file-type preference drawn from a predefined set of weighted type combinations. The paper states these are drawn from intervals but does not give the numeric interval endpoints used in the reported runs.
- Q-learning decay parameter and future-income discount: both held fixed in (0, 1); no numeric value stated.

### Stated limitations

The authors state they do not formally analyze the behavior of risk-averse agents under the micro-payment mechanism, because it depends heavily on each agent's specific utility function, and defer that case to the simulation. They state the quantized micro-payment mechanism is vulnerable to a coalition attack: after one file in a block is downloaded, the remaining files in that block carry zero marginal cost, so a coalition of agents can direct their zero-cost downloads to each other to generate credited uploads for their own benefit; the paper proposes obfuscating which server list entries correspond to the requester's collaborators as a partial mitigation, and states this mitigation reduces but does not eliminate the attack's effectiveness. They state the availability-reward mechanism creates an incentive for agents to make files available at low-demand times or to offer only unpopular files, to minimize the bandwidth cost of being downloaded from, and propose without formal analysis a demand-weighted reward function as an unproven remedy. They state they do not model price discrimination across agents. They state a mechanism to reward point accumulation with faster downloads or early access is not pursued because its effect depends on details of agent utility functions and the file-sharing system not specified in the paper.

### Requirements it places on the rest of the system

The micro-payment and point-based mechanisms require a server, or an equivalent trusted component, that observes every download and upload transaction and can attribute each to a specific agent identity; the paper states the server tracks per-agent download and upload counts directly because it processes every download request. The mechanisms require agents to hold a persistent identity across time periods, since points and monetary balances must carry over and rewards must attach to the correct identity retroactively, including the deferred-credit scheme for files that start rare and later become popular. The file-identification requirement is explicit: the paper states that rewarding upload behavior requires the system to verify what file an agent actually shared, and that without a reliable file-fingerprinting mechanism the fallback is to penalize agents accused of falsely claiming to share files, which the paper states is more costly because it requires human investigation of complaints. The fair-exchange step (crediting an upload and debiting a download only for a transfer both parties agree completed) requires a two-party protocol run at each transaction, cited to a specific fairness-in-commerce construction rather than specified in this paper.

### Contradicts

None found within this corpus.

### References worth retrieving

- Adar, Huberman, "Free Riding on Gnutella," First Monday 5(10), 2000 — foundational; already held in this corpus as ADAR-FM-00, and is the sole empirical citation this paper's introduction rests its free-rider premise on.
- Asokan, "Fairness in Electronic Commerce," PhD thesis, University of Waterloo, 1998 — foundational (the fair-exchange protocol the micro-payment mechanism depends on for verified transfer completion).
- Marwell, Ames, "Experiments in the provision of public goods: I. Resources, interest, group size, and the free-rider problem," American Journal of Sociology 84, 1979 — foundational (economics literature on the general free-rider problem, not p2p-specific).
- Sweeny, "An experimental investigation of the free-rider problem," Social Science Research 2, 1973 — foundational (same category).
- Thorn, Connolly, "Discretionary data bases," Communication Research 14(5), 1987 — foundational (pre-p2p study of voluntary information contribution to a shared database).

### Verbatim extracts

- "more than 70% of its users contribute nothing to the system"
- "the dominant strategy leads to an equilibrium in which nothing gets shared"
- "users strongly dislike micro-payments"
- "agents get no credit for serving rare files"
- "our simulations confirm the existence of equilibria for the micro-payment and point-based mechanisms"
