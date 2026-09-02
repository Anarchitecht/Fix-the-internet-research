## [ZHANG-ARXIV-25] Understanding Community-Level Blocklists in Decentralized Social Media
**Citation:** Owen Xingjian Zhang, Sohyeon Hwang, Yuhan Liu, Manoel Horta Ribeiro, Andrés Monroy-Hernández. "Understanding Community-Level Blocklists in Decentralized Social Media." arXiv preprint, 2025 (24 pages).
**Retrieved:** full text via https://arxiv.org/abs/2506.05522
**Source URL:** https://arxiv.org/abs/2506.05522
**Domain:** K

### What it does
The paper measures how Mastodon instance administrators (moderators) use and share "community-level
blocklists" — a list an instance administrator maintains naming other instances (domains) their own
instance refuses to federate with — and separately interviews moderators about how they select,
apply, and want to improve such lists. It runs two studies against the deployed, unmodified Mastodon
federation mechanism (an instance blocking another domain is a unilateral, locally enforced policy
choice; nothing in the ActivityPub protocol requires a target instance's cooperation).

Study one, content analysis: the authors queried the `instances.social` API for all Mastodon
instances with at least 10 active users, then used an automated scraper (Octoparse) to extract each
instance's publicly visible "About" page for any listed blocked domains and stated blocking reasons.
They manually categorized the free-text blocking rationales into thematic groups (spam, harassment,
hate speech, and others) through open coding. Separately, from community-curated resource lists, they
selected five widely referenced shared blocklists (Seirdy Tier-0, FediNuke, Garden Fence, CARIAD,
IFTAS-DNI) and four blocklist-related tools (FediCheck, FediBlockHole, Fediseer, The Bad Space) and
coded each against a fixed set of dimensions (purpose, inclusion/exclusion criteria, transparency of
review process, distribution method, self-reported limitations, and cross-references to other
resources) derived through iterative open coding by the first author with feedback from co-authors.

Study two, interviews: the authors recruited 12 Mastodon instance moderators (ages 26-55, from seven
countries) via direct Mastodon messages and email to instance owners identified through the same
`instances.social` filter, supplemented by snowball sampling from initial respondents. Each
participant completed a pre-interview demographic survey and a semi-structured Zoom interview; a
subset of the interview walked participants through a demo prototype implementing category filters
for blocklist entries, to elicit reactions to a proposed design.

### Measured results

| Finding | Figure | Conditions |
|---|---|---|
| Mastodon instances with >=10 active users identified | 1,807 (out of approximately 8,700 total Mastodon instances, per the Mastodon software organization's own server list) | Instance list from `instances.social` API, cross-referenced against joinmastodon.org's server list |
| Instances that publicly share their blocklist | 364 of 1,807 (20.1%) | Automated scrape of each instance's public "About" page |
| Instances (of those sharing) that give explicit blocking reasons | 169 of 364 (46.4%) | Same scrape |
| Public blocklist sharing rate by instance size | 10-24 users: 13.9% (89/638); 25-49: 17.7% (62/350); 50-99: 21.3% (51/239); 100-199: 25.3% (50/198); 200-499: 25.9% (42/162); 500-999: 40.8% (20/49); 1000+ users: 45.3% (34/75) | Table 3a, same 1,807-instance dataset, binned by self-reported active-user count |
| Top blocking-reason categories among the 169 instances with stated reasons | Spam 69.8% (118); Harassment/Troll 50.3% (85); Bots 47.3% (80); Hate Speech 37.9% (64); CSAM/Child Abuse 33.7% (57); Misinformation 29.6% (50); Facebook/Meta 23.7% (40); Transphobia 21.9% (37); Adult/NSFW 21.9% (37); Racism 17.8% (30) | Table 3b, thematic coding of free-text blocking rationales; percentages are of the 169 instances with a stated reason and are not mutually exclusive (an instance can cite multiple reasons) |
| Interview sample | 12 Mastodon moderators, ages 26-55, seven countries (USA, France, New Zealand, Netherlands, and others not fully enumerated in the excerpt read) | Semi-structured Zoom interviews plus a demo-prototype walkthrough |
| Demo category-filter feature rated useful | 7 of 12 participants (P1, P5, P6, P8, P9, P11, P12) | Reactions elicited during the demo-prototype portion of the interview |

The paper does not measure, for any of the five named shared blocklists (Seirdy Tier-0, FediNuke,
Garden Fence, CARIAD, IFTAS-DNI), how many instances have adopted that specific list, nor does it
compute a network-reach or isolation metric (e.g., what fraction of the federation graph a given
blocklist's adoption would disconnect). Those five lists are analyzed only qualitatively, by coding
their stated purpose, criteria, transparency, and distribution method (Table 4), not by measuring
their deployment. The claim that Fediverse blocking "can effectively isolate entire communities" is
attributed in the paper's Discussion to an external source (Spencer-Smith, 2025, cited [91]), not
established as a measurement this paper itself performs.

### Parameters
| Parameter | Value used |
|---|---|
| Instance inclusion threshold for content analysis | >=10 active users |
| Instance source | `instances.social` API, cross-checked against joinmastodon.org/servers |
| Scraping tool | Octoparse |
| Shared-blocklist selection count | 5 (Seirdy Tier-0, FediNuke, Garden Fence, CARIAD, IFTAS-DNI), selected for public accessibility, community-driven maintenance, documentation, and adoption |
| Blocklist-tool selection count | 4 (FediCheck, FediBlockHole, Fediseer, The Bad Space) |
| Interview sample size | 12 |
| Interview participant age range | 26-55 |
| Interview participant countries | 7 (USA, France, New Zealand, Netherlands, plus others named in the paper's Table 2, not reproduced here in full) |

### Stated limitations
The authors state the small sample size of 12 Mastodon moderators limits the generalizability of
interview findings across the broader moderator population, and beyond Mastodon to other decentralized
platforms. They state their content analysis's focus on a curated selection of publicly visible,
widely referenced blocklists and tools may introduce selection bias and overlook less prominent
resources, explicitly including non-English-language resources; they note decentralized social media
sees use in non-English-speaking communities operating under different cultural and legal standards
and state that future work should address how the findings translate to those contexts. They state
that moderation practices in decentralized networks are dynamic, making a complete and stable picture
hard to capture, so specific practices and perceptions documented here may shift over time. Within the
content analysis itself, they state that all five analyzed shared blocklists carry limitations tied to
manual curation: Garden Fence acknowledges bias toward English-language sources and subjective
administrative judgment calls; CARIAD notes bias toward Global North perspectives, which the paper
states may disadvantage marginalized communities; IFTAS-DNI does not disclose its internal
decision-making process, limiting transparency; and Seirdy Tier-0 requires intensive ongoing manual
labor to maintain. These are the blocklist creators' own stated limitations as coded by the authors,
not independently verified by the authors against the lists' actual domain contents.

### Requirements it places on the rest of the system
Community-level blocking in Mastodon requires no protocol-level mechanism beyond each instance
administrator maintaining a local, unilateral list of domains to refuse; the paper's data shows this
is enforced entirely at the instance level with no shared-state coordination required to block. Shared
blocklist distribution requires either a synchronization tool (the paper names FediCheck and
FediBlockHole as examples) that periodically pulls updates from a maintainer-controlled source into an
instance's local block configuration, or manual application of a publicly hosted CSV file (the
distribution method the paper reports for Seirdy Tier-0 and FediNuke); either path requires the
receiving instance's administrator to trust the maintaining party's inclusion criteria, since the
paper finds none of the five analyzed shared blocklists discloses its full underlying evidence for
each blocked domain, and some (Garden Fence) incorporate additional external blocklists that are
themselves not publicly disclosed. Any moderation architecture that assumes blocklist adoption
produces uniform network-wide effects should not rely on this paper for a coverage or isolation
figure — the paper's own measurement stops at the 20.1% public-sharing rate and the per-category
breakdown of stated reasons, and does not quantify adoption of any specific named shared list nor its
resulting network-isolation effect.

### Contradicts
None found within this corpus. The paper's own Discussion is careful to attribute the claim that
Fediverse blocking "can effectively isolate entire communities" to an external source (Spencer-Smith,
2025) rather than presenting it as a result of the content analysis or interviews reported here — a
reader treating that sentence as this paper's own measured finding would be incorrect; the paper
supports only the blocklist-sharing-rate and category-breakdown figures in Table 3 as its own
measurements.

### References worth retrieving
- **Spencer-Smith, "Labour pains: Content moderation challenges in Mastodon growth," Internet Policy Review 14(1), 2025** — cited [91] as the source for the "blocking can isolate entire communities" claim; also appears as [92], an alternate-format citation of what may be the same work (Spencer-Smith and Tomaz) — worth retrieving to resolve whether these are one paper or two, and to check for the network-isolation measurement this paper's Discussion attributes to it.
- **Colglazier, TeBlunthuis, Shaw, "The effects of group sanctions on participation and toxicity: Quasi-experimental evidence from the fediverse," ICWSM 2024** — competing/foundational quasi-experimental measurement of Fediverse defederation effects, cited [15]; directly relevant to any claim about blocking's effect on participation and toxicity, with a quasi-experimental design distinct from this paper's content analysis.
- **Lai, Roth, DiResta, Klonick, Knodel, Prodromou, Rodericks, "New Paradigms in Trust and Safety: Navigating Defederation on Decentralized Social Media Platforms," Carnegie Endowment for International Peace, March 2025** — cited [59]; a policy-oriented report on defederation, worth checking for adoption or reach figures not in this paper.
- **Seering, Kaufman, Chancellor, "Metaphors in Moderation," New Media & Society 24(3), 2022** — foundational framework for moderator roles cited [88], underlying this paper's discussion of moderator power.
- **Kumar, Hamilton, Leskovec, Jurafsky, "Community interaction and conflict on the web," WWW 2018** — foundational, cited [58], on cross-community conflict dynamics relevant to blocklist motivations.
- **Crawford, Gillespie, "What is a flag for? Social media reporting tools and the vocabulary of complaint," 2016** — foundational, cited [16], on centralized-platform reporting/flagging as the individual-level analogue to this paper's community-level blocklists.

### Verbatim extracts
"only 364 (20.1%) publicly shared their blocklists" (Section 4.1.1).
"fewer than half (169, or 46.4%) provided explicit reasons for blocking" (Section 4.1.1).
"the largest instances (1,000+ users) shared their blocklists at the highest rate (45.3%)" (Section 4.1.1).
"Blocking on the Fediverse can effectively isolate entire communities [91]" (Section 5.2).
"The small sample size of 12 Mastodon moderators limits the generalizability" (Section 6).
"these external sources and their blocklists are typically not publicly shared" (Section 4.1.2).
