# Decentralized research

A verified evidence corpus and a Pareto-optimal component selection for a decentralized web
architecture. `BRIEF.md` is the governing document; where this README and the brief disagree, the
brief holds.

## What is being designed

A decentralized internet whose identity, indexing, and storage components cannot be captured by any
company, and whose client reproduces the functional patterns of the most-visited websites. Privacy
mechanisms are user-selectable tiers, each stating the adversary it defeats and the measured latency
and bandwidth it adds.

The target is Pareto optimality across the whole system. A component that is optimal alone and
destroys a precondition the component beside it requires is worse than two components that compose.
Finding those destroyed preconditions is a deliverable, not a remark.

## The rule that governs every entry

Three categories, never merged:

| Category | Definition | Where it goes |
|---|---|---|
| Measured fact | A number an experiment produced, with its conditions stated | `evidence.md`, cited to the paper |
| Structural consequence | A property that follows by reasoning from a measured fact or a proof | `architecture.md`, with the derivation shown |
| Value judgment | A decision that a cost is or is not worth paying | Excluded, or attributed to whoever made it |

A number, a parameter, or a mechanism description enters `evidence.md` only from the full text of the
primary source. An abstract establishes that a paper exists and what it claims to cover. An abstract
establishes no measurement.

## Deliverables

| File | Contents |
|---|---|
| `evidence.md` | Every retrieved paper in the brief's §6 schema. The artifact of record. |
| `retrieval-log.md` | Every paper attempted, the escalation steps tried, the outcome. Failures carry their exact DOI. |
| `architecture.md` | The synthesis: one selection per component, each justified against every rejected candidate. |
| `conflicts.md` | Measurement disagreements between sources, destroyed preconditions between selected components, and any claim in `architecture.md` no `evidence.md` entry supports. |
| `open-problems.md` | Problems with no published solution, each stating what was tried and where it falls short. |

## Why `sources/prior-pass-corpus.md` is quarantined

That document is a prior research pass. It is retained as a source of citations and of measured facts
that can be re-verified against primary sources. It is not a source of constraints, conclusions,
terminology, or architecture, for two reasons the brief states in §2.

It carried figures from abstracts and secondary summaries. One example it corrects itself: a
distributed search system's recall was stated as 1.2 million documents across 750 peers with 45 to
130 peers contacted; the paper says 50 overlapping collections, and plots recall against 1 to 20
queried peers.

It also absorbed one implementation project's refusals as though those refusals were properties of
the mechanisms. Five mechanism families appear there as rejected: gossiped inventory filters,
network-wide popularity aggregation, published per-identity behavior scores, content-derived
similarity signatures, and epidemic push. Each of the five works. That project decided the costs were
not worth paying for its own deployment. The cost, the exposure, and the failure condition are facts
and are extracted. The refusal belongs to whoever wrote it and is not carried.

The same applies to that project's parameters. Its transport frame is 4,096 bytes, from which it
concluded that space-efficiency results produce no benefit. The general form transfers — under a
fixed padded transport frame of size F, a size reduction that stays within one frame reduces
transmitted size by nothing — and F is a design variable, recorded as that project's setting rather
than as a constant.

## Design posture

The possibility space is open. A mechanism is excluded when a measurement or a proof excludes it,
not because a prior document declined it and not because a deployed system chose otherwise. Where an
existing architecture is suboptimal and a different decomposition of the problem removes the
limitation, the different decomposition is the one to state.
