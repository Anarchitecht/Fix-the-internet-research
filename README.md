# Decentralized research

Research corpus and integrated design for peer-to-peer search, storage, identity, privacy, and
moderation. Independent of any implementation repository.

## What is here

`research/00-corpus-p2p-search-storage-identity.md` — the source corpus, in three passes. Each
section surveys the published mechanisms for one component, quotes measurements from primary
sources where the paper was read in full, and states one selection with the assumption that
selection requires and the condition under which it fails. The third pass supersedes two earlier
selections (BeeKEM replaces DCGKA; disjoint-path lookups operate at d=8, not d=3).

## Reading order

The corpus states its own dependency order in "Design sequence and thresholds": storage and naming
first, because those components have the most primary-source measurement behind them.

Three constraints in the corpus govern how every other section is read:

- Under a 4,096-byte padded onion cell, a round trip is the scarce resource and a byte is not.
  Space-efficiency results that shrink a structure without removing a cell change nothing.
- A search channel that returns only match or no-match destroys the feedback signal square-root
  replication requires, because a forwarding peer never learns which object matched.
- Twelve problems in the corpus have no published solution. They are listed in the open-problems
  table and must not be described as solved.

## Provenance of numbers

Every figure in the corpus carries its source. Where a paper could not be retrieved, the corpus
says so and strikes the claims that rested on it. A number without a stated derivation, a
measurement, or a `NOT DERIVED` label does not belong in this repository.
