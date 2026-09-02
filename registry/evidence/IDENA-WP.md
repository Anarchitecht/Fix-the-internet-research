## [IDENA-WP] Idena: Proof-of-Person Blockchain Technology Overview
**Citation:** Idena project (collective; not peer-reviewed). "Idena Whitepaper - Technology." Project documentation (not peer-reviewed), 2019 (page cites a 2023-06-22 timezone example, indicating the retrieved page has been updated after initial publication).
**Retrieved:** full text via https://docs.idena.io/docs/wp/technology
**Source URL:** https://docs.idena.io/docs/wp/technology
**Domain:** E

### What it does
Idena's Proof-of-Person (PoP) protocol certifies that a network participant is a distinct human, without collecting personal data or using a third-party identification service, by making every participant solve the same test at the same moment worldwide. Uniqueness follows from timing rather than from biometric or document data: a synchronous validation session decrypts a shared set of puzzles ("flips") to every candidate at once, at a fixed global time (15:00 UTC), so one person holding two identities cannot complete two separate sessions inside the single narrow answer-submission window. A flip presents four images and asks the participant to choose which of two orderings of those images tells a coherent story; the network defines this as a common-sense test that is stated to be easy for a human and difficult for an automated solver ("AI-hard"), because flips carry narrative rather than semantic structure and are authored by other validated participants rather than generated algorithmically. Each validation session has two phases: a short session under two minutes with six flips, each shown to only 1-4 participants, functioning as a pairwise Turing test; and a long qualification session of 30 minutes with 25-30 flips shown to a larger group, whose purpose is for the network to reach consensus on the correct answer to each flip and thereby validate the flip itself (a flip lacking network consensus on its answer is discarded and its submitted answers do not count). A validated participant holds one "cryptoidentity" with one vote, valid only for the current epoch (a fixed period, capped at 28 days), and must revalidate at every subsequent session to keep that status; failing or missing a session moves the identity down a status ladder (Candidate, Newbie, Verified, Human, Suspended, Zombie, Killed) that gates invitation rights, block-mining rights, and a stake-slashing penalty. New identities enter only via an invitation code issued by an already-validated participant, and the total invitation supply issued per epoch is capped at 50% of current network size, which the document states is intended to bound the rate of network growth and thereby limit Sybil-attack feasibility.

### Measured results
The source is project documentation describing a live, deployed protocol's own rule parameters rather than an independent experiment; the figures below are the protocol's stated design constants and thresholds, not results of an external study, so they are recorded here as project-stated operating parameters.

| Parameter | Stated value |
|---|---|
| Validation session frequency by network size | 17+ identities: every 3 days; 45+: every 4 days; 96+: every 5 days; 176+: every 6 days; 291+: every 14 days (adjusted to Saturdays, 13 or 15 days otherwise); 5,845+: every 21 days; 16,203+: every 28 days |
| Epoch duration cap | 28 days maximum |
| Short session duration and structure | under 2 minutes; 6 flips; each flip shown to 1-4 participants |
| Long session duration and structure | 30 minutes; 25-30 flips; each flip shown to a larger participant group scaled to network size |
| Validation pass thresholds | current short-session score >=60%; rolling total score over the last 10 short validations >=75%; current long-session score >=75%; the first 6 flips must be solved in under 2 minutes |
| Stake share of rewards | 20% of mining and validation rewards accumulate in a locked stake account; 80% go to the spendable wallet |
| Newbie reward split | 20% of earned coins to the spendable wallet; 80% (of which 60% is described as "temporarily locked") held in stake until the Newbie status is upgraded to Verified |
| Invitation supply target | 50% of network size, recalculated after each validation session; core-team invitation allowance capped at max(500, network_size * 0.1) |
| Flip report cap | at most one-third of received flips may be reported by a participant per session |
| Transaction fee formula | transactionFee = currFeeRate x transactionSize, where currFeeRate = max(1e-16, 0.1/networkSize, prevFeeRate x (1 + 0.25 x (prevBlockSize/300Kb - 0.5))), targeting 50% average block utilization; 90% of collected fees are removed from circulation (burnt), 10% go to the block proposer |
| Smart-contract minimum gas price | GasPrice = 0.01/networkSize |
| AI-attack research incentive | a stated $55,000 prize pool offered for an open AI tool to detect adversarially generated flip patterns, to be integrated into the client |

### Parameters
- Validation time: fixed at 15:00 UTC for every session worldwide, stated as chosen to fall within waking hours for most of the world's population.
- Discrimination threshold on stake weight in consensus: an identity's stake below 0.5% x median_top100 (the median stake among the top 100 accounts) is excluded from having its vote counted in Byzantine Fault Tolerant (BFT) consensus, oracle votes, and governance votes.
- Stake-burn schedule on validation failure or a missed session: varies by identity age and status, ranging from 100% of stake burnt (Candidate or Newbie failing or missing, or any Verified identity failing) down to a schedule that decays from 5% at age 5 to 0% at age 10+ for Suspended/Zombie identities that fail, and an entirely separate 0%-at-Verified/Human-status schedule for a first missed (not failed) session.
- Newbie discrimination: Newbie-status votes are cast but not counted in block consensus, oracle votes, or hard-fork governance votes.

### Stated limitations
The document states that selling or buying a cryptoidentity or an invitation is technically possible but is deliberately made economically irrational by protocol-level incentives: a seller retains a copy of the private key after transfer and can unilaterally kill the identity (or double-spend an invitation) at any time, so the document states the buyer "would not have an economic reason" to complete such a purchase — this is the document's own economic argument, not an independent proof, and it is recorded here as the document's stated design intent rather than as a verified security guarantee. Oracle-voting mechanisms depend on a trusted-enough threshold of honest oracle behavior; the document states a high consensus threshold is required for fact-certifying oracle votes "to prevent a possible attack on voting," without stating what quantitative Sybil or collusion resistance that threshold provides. The AI-resistance analysis is presented as an ongoing arms race rather than a settled property: the document describes adversarial-perturbation and adversarial-nonsense-image attacks on flip images and states a bespoke detection tool is under a funded contest rather than already deployed and proven effective.

### Requirements it places on the rest of the system
Global time synchronization across all participants is a precondition the whole mechanism depends on: the document states uniqueness follows specifically from every participant decrypting flips "at the same time worldwide," so any client or network layer that lets a subset of participants receive or answer flips outside the shared narrow window (through relayed decryption, replay, or clock skew) removes the property the scheme is built on. Flip authorship requires an existing pool of validated participants willing to generate new flips every epoch, since flips are stated to be human-generated specifically to remain AI-hard and to avoid needing a trusted third party to author them, so a bootstrapping network with too few validated identities has no flip supply to run a validation session against. Network-wide BFT consensus on both the correct answer to each flip and on which identities validated depends on a committee-selection and block-production layer external to this document's description, which the document assumes exists (referred to only as "committee-based consensus with fast finality") without specifying committee-selection security parameters here. The invitation-graph growth cap (50% of network size per epoch) requires that invitation issuance actually is restricted to already-validated identities, so any pathway that mints invitations outside that gate (a bug, an unaudited smart contract, or a bridge to another identity system) defeats the growth-rate control the document states is what "minimizes the probability of a Sybil attack."

### Contradicts
None found within this corpus batch.

### References worth retrieving
- competing: BrightID documentation — a social-graph proof-of-personhood approach the target registry's "why_needed" note explicitly contrasts against Idena's synchronous-ceremony approach; not cited by name inside this document's retrieved text, so classified here as competing rather than as an in-text reference.
- competing: Worldcoin / World ID documentation — a biometric proof-of-personhood approach in the same category, likewise not cited by name in the retrieved text but named in the target registry's rationale as the comparison this key exists to support.
- foundational: Idena Improvement Proposal IIP-4 (referenced in-text as the source of the "stake protection" rules) — governs the stake-burn schedule cited above; not separately retrieved in this batch.

### Verbatim extracts
- "Flips are decrypted at the same time worldwide."
- "A single person is not able to validate herself multiple times because of the limited timeframe"
- "the validation date is adjusted to Saturdays once the network reaches 291 identities"
- "The total epoch duration is limited to 28 days."
- "the buyer would not have an economic reason to buy identity."
- "90% of paid fees are burnt. The rest 10% are paid to the block proposer."
- "announced a contest for AI researchers ... with a $55,000 reward cascade"
