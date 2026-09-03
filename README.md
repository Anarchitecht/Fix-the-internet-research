# Moved to Anarchitecht/konkin

This repository is empty. Its contents are in **Anarchitecht/konkin** under `research/`, with the
twenty-three commits that produced them, imported with `git subtree add --prefix=research` on
2026-09-03. `git log -- research/` in that repository reads as the research pass ran here.

Read the corpus there, not here. A copy left in place is a copy that goes stale, and the konkin
tree is where the corpus is being compared against a protocol.

## What moved

| Path in konkin | Contents |
|---|---|
| `research/BRIEF.md` | The governing document: what may enter the corpus and what may not |
| `research/evidence.md` | 392 entries, each extracted from a primary source's full text |
| `research/retrieval-log.md` | The outcome for all 417 targets; failures carry their DOI |
| `research/architecture.md` | One mechanism selected per component, against every rejected candidate |
| `research/conflicts.md` | 21 composition conflicts, and the one measurement disagreement in the corpus |
| `research/open-problems.md` | Eleven problems with no published solution |
| `research/registry/` | Per-paper entries, per-component selections, retrieval targets |
| `research/sources/text/` | The extracted full text the entries were built from |
| `research/tools/` | The retrieval and index-building scripts |

One file did not move: `scratch_zooko1.html`, whose entire content was the string
"Blocked by egress policy".

## Where the corpus stands in konkin

Nothing in `research/` is normative there. It selects mechanisms for a decentralized web
architecture in general, and no pass has yet compared one of its selections against a Konkin
choice. That pass is `D-CORPUS-01` in `docs/OPEN_DECISIONS_AND_DEFERRED_WORK.md`.

## The last commit here, and why the history is worth keeping

`6df7837` — "The claims audit finds this synthesis committing the error it was built to catch."
That commit is reachable in konkin. Deleting this repository outright would still lose nothing,
because every object in this history is now on konkin's remote.
