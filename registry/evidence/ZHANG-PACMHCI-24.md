## [ZHANG-PACMHCI-24] Trouble in Paradise? Understanding Mastodon Admin's Motivations, Experiences, and Challenges Running Decentralised Social Media
**Citation:** Zhilin Zhang, Jun Zhao, Ge Wang, Samantha-Kaye Johnston, George Chalhoub, Tala Ross, Diyi Liu, Claudine Tinsman, Rui Zhao, Max Van Kleek, Nigel Shadbolt. "Trouble in Paradise? Understanding Mastodon Admin's Motivations, Experiences, and Challenges Running Decentralised Social Media." Proceedings of the ACM on Human-Computer Interaction (CSCW), Vol. 8, No. CSCW2, Article 520, 2024. DOI 10.1145/3687059.
**Retrieved:** full text via https://www.cs.ox.ac.uk/files/15025/Zhang_et_al_2024_Trouble_in_paradise.pdf
**Source URL:** https://www.cs.ox.ac.uk/files/15025/Zhang_et_al_2024_Trouble_in_paradise.pdf
**Domain:** K

### What it does
This is a qualitative interview study, not a system or mechanism; it records what a person who volunteers to run a Mastodon instance actually does and what that work costs. A preliminary 15-minute online survey (33 respondents) screened candidates for eligibility (18+, administers at least one Mastodon instance) and gathered background (tenure as admin, largest instance's user count, instance topic, motivations, challenges). Semi-structured, audio-recorded, remote (Zoom) interviews (16 participants, roughly 1 hour each) then asked administrators about their motivations for starting the instance, the challenges of running it, the strategies they use to address those challenges, and their views on the platform's future. Two authors independently coded a first half of the transcripts to build a shared codebook (Cohen's kappa 0.92), and the first author coded the remaining transcripts against that codebook (grounded thematic analysis). Participants were compensated a GBP 12 gift card. Recruitment used the Join Mastodon website's public instance directory plus social-media recruitment ads and snowball sampling from prior participants.

### Measured results
This is qualitative research; the "results" are themes, not effect sizes, and every quantitative figure below is a sample-composition or methodology count, not a measured system property.

| Figure | Conditions |
|---|---|
| 33 respondents completed the preliminary survey; 16 of those proceeded to interview | Recruitment window August 2023-January 2024; recruitment via Join Mastodon site invitations, social-media ads, and snowball sampling |
| 16 interviewed administrators spanned 7 countries (USA, Australia, Costa Rica, Germany, Netherlands, France, Canada) and instance topics General, LGBTQ+, Disability, Activism | Same interview sample; instance size per participant ranged from 0-9 users (one participant, an unlaunched/very new instance) to over 100,000 users (one participant); administrator tenure was either 6-12 months or more than 12 months for every participant (no participant had under 6 months of tenure) |
| Inter-coder reliability Cohen's kappa = 0.92 on the codebook built from the first half of the transcripts | Two authors coding independently, before reconciliation into the shared codebook |
| A dominant challenge, content moderation and community governance complexity, was mentioned by all 16 participants | Thematic coding across the full interview set |

The paper reports no latency, throughput, message-count, or other system-performance measurement; it is not that kind of study.

### Parameters
Not applicable in the sense of tunable system parameters — this is an interview study. Methodological parameters as run: interview count 16, interview length approximately 1 hour, preliminary survey length 15 minutes, coder count 2 (with kappa 0.92 before the first author coded the remainder), compensation GBP 12 per participant, geographic reporting granularity continent-level (deliberately coarsened from country-level for participant anonymity).

### Stated limitations
The authors state the study population's size and composition limit the findings: participants who agreed to take part may already have above-average awareness of and commitment to values like citizen empowerment, biasing the sample toward pro-decentralization views. All data is self-reported, so findings reflect what participants judged significant rather than an independent observation of their practice; the authors state this means the findings likely skew toward the perspectives of general and LGBTQ+-focused instance administrators specifically, not moderators or ordinary users. The authors state the choice of Mastodon as the example platform, made because of its prominence in the decentralized-platform space, may make some findings specific to Mastodon rather than to decentralized social media generally. The authors state future work should pursue direct ethnographic observation (rather than self-report) and co-design workshops to test content-moderation and governance designs.

### Requirements it places on the rest of the system
This paper is an empirical measurement of a human cost, not a mechanism proposal, so it does not impose implementable requirements on other components. What it supplies is a target that any design replacing per-instance human moderators must account for: participants reported that moderation is currently done largely manually, is described as tedious and stressful, and exposes moderators to traumatic content (one participant, P4, described exposure to child-abuse material during moderation). Participants reported cross-instance moderation policy incompatibility as an unresolved operational burden: instances differ in strictness, and administrators described negotiating directly with other instances' administrators to reconcile conflicting rules rather than relying on any automated or protocol-level reconciliation mechanism. Participants reported no built-in Mastodon tooling for moderation-team coordination and stated using separate third-party software (Discord was named) for that purpose. Participants reported legal uncertainty about what actions (e.g., identifying and blocking servers hosting illegal content) they are permitted to take under their jurisdiction, with no described institutional or protocol support for resolving that uncertainty. Any moderation-locus design that removes or automates the per-instance human administrator has to reproduce, or explicitly account for the loss of, the trust-based selection of moderators that participants described (moderators selected from known, personally-vetted community members) and the multi-timezone, multi-language moderator-team composition some participants described building deliberately.

### Contradicts
None found. This paper is commonly read as evidence that decentralized moderation "does not scale," but the paper's own findings do not make that a general claim — participants who deliberately kept their instances small reported this as a working strategy specifically because it kept community trust intact, not as evidence that decentralized moderation fails at all scales; the paper does not measure larger instances' moderation outcomes systematically enough to support a scaling claim either way.

### References worth retrieving
- foundational: Raman, A. et al. — cited in this paper's background section for prior fediverse/Mastodon measurement work characterizing the platform's growth and Fediverse-project popularity (full citation not resolvable from the excerpt read; bibliography entry number [94] in this paper).
- foundational: La Cava, L. et al. — cited for instance-level evolution and how Mastodon's design facilitates user connection (bibliography entry referenced near "La Cava et al." in section 2).
- competing: Nicholson et al. — cited by this paper for observations on rules against harassment/hate on Mastodon compared to Reddit; a direct point of comparison for moderation-policy prevalence across platform types (bibliography entry [84]).
- competing: Gilbert, [42] — cited for the finding that visible moderation is often perceived by users as censorship, studied on Reddit; relevant as a competing (centralized-platform) moderation-perception result.
- foundational: Dantec, C. and DiSalvo, C., [29] — cited for participatory design as a possible approach to the community-governance/power-centralization tension this paper documents.

### Verbatim extracts
"we conducted semi-structured interviews with 16 Mastodon instance administrators"
"a Cohen kappa of 0.92"
"A dominant challenge mentioned by all participants was the complexities of content moderation"
"I was exposed to the content of child abuse. And it was a hard day."
"the sample we reached out has provided a good range of themes relevant to the scope of our study"
"participants signed up for our study may already have heightened awareness about issues like citizen empowerment"
"all data collected is self-reported"
