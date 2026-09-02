## [FRIEDMAN-JEMS-01] The Social Cost of Cheap Pseudonyms

**Citation:** Eric J. Friedman, Paul Resnick. "The Social Cost of Cheap Pseudonyms." Journal of Economics & Management Strategy, 2001. DOI 10.1162/105864001300122476.
**Retrieved:** full text
**Source URL:** https://sites.google.com/site/econfriedman/cheap-pseudonyms
**Domain:** F

### What it does
The paper proves that in a system where identity changes are free, no equilibrium strategy for a repeated cooperation game sustains substantially more cooperation than a strategy that distrusts every newcomer, once a small non-vanishing rate of mistaken or malicious defection exists. It models the game as an infinite sequence of periods in which M active players are matched uniformly at random into pairs to play a prisoner's dilemma; a fraction alpha of players exit at the end of each period and are replaced by new entrants; every player observes the complete public history of past pairings and actions before choosing an action; and any player may discard its identifier and re-enter as an indistinguishable newcomer at zero cost. The paper compares four strategy classes: a localized punishment strategy usable only when identities are fixed, a public grim trigger strategy that punishes the whole population after any single defection, a public forgiving trigger strategy that punishes for a finite number of periods, and a paying-your-dues (PYD) strategy in which an entrant unconditionally cooperates while a compliant veteran defects against the entrant with a computed probability. It then defines two further mechanisms outside the base game: a monetary entry fee paid on each identity change, and a once-in-a-lifetime identifier issued through a blind-signature protocol with a trusted intermediary, which lets a player commit to non-persistent identity without revealing it to anyone, including the intermediary.

### Measured results
The paper reports no simulation or empirical data; every result below is a proven bound on the equilibrium payoff function V(s), the average per-player, per-period expected payoff under strategy vector s, under the stated parameter conditions.

| Result | Conditions (from the paper's propositions) |
|---|---|
| Full cooperation is sustainable, V(LPS) = 1 | Identities fixed (cannot be changed); exit rate alpha <= 1/2; localized punishment strategy (LPS): cooperate with a newcomer or a veteran who complied last period, defect against a veteran who deviated last period |
| Full cooperation is sustainable with free identity changes, V(PGTS) = 1 | Free identity changes allowed; alpha <= 1/2; no trembles or malicious players (probability of error epsilon = 0); public grim trigger strategy (PGTS): defect forever once any defection has ever occurred |
| PGTS collapses to zero cooperation, V(PGTS) = 0 | Free identity changes; any epsilon > 0 (trembles or malicious players present) |
| Fixed-identity cooperation is near-total, V(LPS) >= 1 - 2*epsilon | alpha < 0.3, M > 1, epsilon < 0.1; player identifiers cannot change |
| Paying-your-dues equilibrium payoff, V(PYD) = 1 - alpha/(2-alpha) - O(epsilon) - O(1/M) | alpha < 0.3, epsilon < 0.1, M > 11, and the computed dues-probability q-hat(alpha, epsilon, M) <= 1 (automatically satisfied when alpha < 0.24 or epsilon < 0.05) |
| Stable value (population M to infinity, then epsilon to 0) lower bound, SV >= 1 - alpha/(2-alpha) | Free identity changes; impersistent identities; PYD strategy |
| No equilibrium exceeds the PYD stable value | alpha < 0.3; a threshold beta > 0 exists such that for any target value v > 1 - alpha/(2-alpha) - beta, there is an epsilon-bar such that for all epsilon < epsilon-bar and M > beta/epsilon, no equilibrium reaches v (Proposition 3) |
| Once-in-a-lifetime identifiers restore full cooperation even with heterogeneous player payoffs, SV = 1 | Trusted (or blind-signature-mediated) intermediary issues at most one committed identifier per player per arena; LPS extended to treat regular (non-committed) identifiers as untrustworthy |

At alpha near zero, the PYD equilibrium's per-player net loss (relative to full cooperation) is between 0.5 and 1 unnormalized utility unit, computed from the payoff matrix in which mutual cooperation pays 1 and mutual defection pays 0 to each player.

### Parameters
- alpha: fraction of the M active players who exit (and are replaced by entrants) at the end of each period; propositions require alpha < 0.3, and full cooperation under fixed or free identifiers with epsilon = 0 further requires alpha <= 1/2.
- M: number of active players per period; propositions require M > 1 (Proposition 1), M > 11 (Proposition 2), and M > beta/epsilon for a threshold beta (Proposition 3, no numeric value for beta given).
- epsilon: probability a player trembles (plays the opposite of its intended action) or, equivalently, the fraction of malicious players; propositions require epsilon < 0.1; the paper takes the limit epsilon to 0 after M to infinity when defining the stable value SV.
- q-hat(alpha, epsilon, M): the PYD veteran's computed probability of defecting against a compliant entrant, given in closed form in the text; required to satisfy q-hat <= 1, automatically true for alpha < 0.24 or epsilon < 0.05.
- Entry fee F: no numeric value derived or recommended; the paper states only that F must be large enough to deter the wealthiest player type from deviating, which then excludes some lower-value players from participating, and that standard price-discrimination remedies do not apply to this setting.

### Stated limitations
The paper states its model does not determine the reliability of player-reported feedback (whether players report negative outcomes honestly), citing this as a separate, unaddressed problem beyond the scope of the analysis. It states that redistributing collected entry fees back to players breaks the model's assumption that player exit is exogenous, and that redistribution also fails when player expected lifetimes are heterogeneous, since some players know in advance they will not remain long enough to recoup a fee. It states that when players have heterogeneous valuations of money or heterogeneous game payoffs, any fixed entry fee or PYD dues level that deters the highest-value deviator simultaneously excludes some lower-value players from participating, and that this exclusion problem has no standard solution in the entry-fee literature the authors are aware of. It states that the once-in-a-lifetime identifier protocol remains vulnerable to a timing attack in which the intermediary correlates the appearance of a new committed identifier in the game with the most recent identifier request, unless players hold an acquired identifier for a randomized delay before using it. It states that a person can still acquire multiple once-in-a-lifetime identifiers for one arena by using other people's true identities to request them, and that this is deterred, not prevented, once a robust cryptographic infrastructure exists.

### Requirements it places on the rest of the system
The equilibrium results require a public history mechanism that every player can observe before acting: each pairing and each action taken must become common knowledge, either through direct interaction monitoring or explicit feedback collection: the model equates this to the environment's ability to publish a complete play history. The once-in-a-lifetime identifier mechanism requires a system-wide or per-arena intermediary — trusted not to reveal identity mappings, or cryptographically prevented from learning them via blind signatures — that enforces a strict one-committed-identifier-per-player-per-arena limit, and requires each player to hold a pre-existing private key tied to a true identity, usable to sign the blinded certificate request. The PYD mechanism requires an exogenous source of variability in the entrant count each period (the paper assumes each player independently loses its identifier with probability epsilon) to prevent strategies that condition punishment on the literal count of new identifiers appearing; a deploying system must supply this randomness or an equivalent.

### Contradicts
None found. No other paper in this batch measures or restates this paper's specific equilibrium bounds.

### References worth retrieving
- Ellison. "Cooperation in the prisoner's dilemma with anonymous random matching." Review of Economic Studies, 1994 — foundational (source of the public forgiving trigger strategy this paper builds on and reverses the limit order against)
- Kandori. "Social norms and community enforcement." Review of Economic Studies, 1992 — foundational (prior work on reputation transfer this paper contrasts with, since here reputation transfer is a player-controlled strategic variable)
- Milgrom, North, Weingast. "The role of institutions in the revival of trade: the law merchant, private judges, and the champaign fairs." Economics and Politics, 1990 — foundational (prior reputation-transfer model without player control)
- Tadelis. "What's in a name? Reputation as a tradeable asset." American Economic Review, 1999 — competing (models reputation as a tradeable name where skill, not performance, is the underlying signal)
- Watson. "Starting small and renegotiation." Journal of Economic Theory, 1999 — competing (alternative slow-start equilibrium approach to newcomer trust)
- Nowak, Sigmund. "A strategy of win-stay, lose-shift that outperforms tit-for-tat in the prisoner's dilemma game." Nature, 1993 — foundational (evolutionary behavior of the prisoner's dilemma under trembles, cited to motivate modeling errors)
- Kreps, Milgrom, Roberts, Wilson. "Rational cooperation in the finitely repeated prisoner's dilemma." Econometrica, 1982 — foundational (shows small numbers of atypical players can dramatically change the equilibrium set)

### Verbatim extracts
"there is an inherent social cost in making the spread of reputations optional"
"no equilibrium can sustain significantly more cooperation than the dues-paying equilibrium"
"A single tremble or malicious player causes mass defection in future periods"
"the intermediary never learns what identifier A is using"
"this remains an equilibrium with full participation and full cooperation, unlike entry fees"
