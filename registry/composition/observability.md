# Composition check: observability

Scope: for every pair of selected components in `registry/selections/`, does one component's
stated requirement to observe something collide with another component's stated or structural
property of hiding that same thing. Method: every selection file's "What this selection requires
from the rest of the system" section was read against every other selection file's stated hiding
property, concentrated in `privacy-tiers.md`'s three tables and in any other selection that states
it withholds a value by design (single-server PIR's index-blindness, a mix network's sender
concealment, an onion circuit's identity concealment from the serving peer).

Three findings survive verification against the full selection text. A fourth candidate pairing —
the ranking component's gossip-based default writing a querying peer's node ID into the payload a
mix network exists to hide — is already reported in `registry/conflicts/composition.md`, finding 3,
and is not repeated here.

## 1. The illegal-content deny list needs to read the identifier a query privacy tier is built to hide from the answering peer

`moderation.md` selects an identifier deny list, honored at the point of serving, as the sole
mechanism in the corpus for illegal content: the retrieval-serving node "performs the deny-list
check at the moment of serving, before returning bytes," because the underlying content-addressed
store has no deletion primitive at the identifier layer (`SOKOTO-USENIXSEC-24`). The selection
states this check is mandatory independent of any viewer's choices — its "entire value is that it
does not depend on any viewer's subscription choice." The check can run only if the node answering
a request reads the requested content identifier and tests it against the list.

`privacy-tiers.md` selects single-server computational Private Information Retrieval (PIR) as the
default Query tier (Piano, `ZHOU-SP-24`) for querying a shared index, and states the tier "defends
which record is requested, hidden even from the single peer answering." The selection states this
tier applies beyond keyword search — a client "already has an object's content hash" and can
"supply that as the PIR index" — so it is stated to cover retrieving a specific already-known
object by its content hash, not keyword search alone. The security property PIR supplies is
precisely that the answering peer cannot determine which index — which content identifier — the
client queried; a server that cannot determine the requested identifier cannot compare it to a deny
list.

A person who selects the Query privacy tier for a fetch, and a deny-list-enforcing node answering
that fetch, cannot both get what their respective selections promise. Moderation's own bootstrap
method for the list depends on the same observability: `SOKOTO-USENIXSEC-24`'s own dataset was
built by passively watching Bitswap and DHT traffic to map hash-only list entries back to
identifiers, a step that `privacy-tiers.md`'s Fetch-ladder onion circuit (Table 1) is separately
built to defeat by hiding the fetched identifier's connection pattern from a network-position
observer — so the same privacy selection that blocks live enforcement also removes the traffic
visibility the list's own construction method used.

This is the same structural conflict the brief's own worked example states for search-driven
replication and blinded search — one selection's input is the other's deliberate secret — applied
here to illegal-content interdiction and query privacy rather than to replication.

**Resolution.** No published construction in this corpus lets an answering peer test a query's
requested identifier against a blocklist without learning the identifier, so this is recorded as an
open problem: record it explicitly, next to `registry/open-problems/illegal-content-removal.md`,
that the deny-list mechanism this corpus selects has no defined behavior once the Query privacy
tier is in effect. Absent a solution, the corpus supports one operational degradation: state to the
user, at the point they select the Query privacy tier for a fetch, that illegal-content
interdiction is not covered for that fetch — the identical pattern `registry/conflicts/composition.md`
finding 3 uses for G-Rank's clicklog traffic under a mix network. Changing the selection instead
would mean either dropping single-server PIR as the default Query tier (giving up its measured
73 ms–2.64 s query cost against multi-gigabyte databases, `ZHOU-SP-24`, `MENON-USENIXSEC-24`) or
restricting the deny-list check to a class of content the Query tier is not offered for, neither of
which any entry in this corpus evaluates.

## 2. The reputation flow computation needs to observe the linkage graph a Message-tier mix network is built to hide from the party computing it

`reputation.md` selects a capacity-bounded network-flow computation (SumUp, Bazaar, Ostra,
accelerated by Canal) over a graph whose edges each represent one linkage "that cost something real
to form" — a real transaction, a real vouch. The selection states its own composition requirement
directly: no privacy tier "may hide a participant's linkage graph from whichever party executes the
flow computation," calling this "a composition conflict to resolve explicitly," not an open
question to leave unresolved. The mechanism requires either a central party (Bazaar's own design)
or a route-discovery layer (Ostra's Bloom-filter scheme) or a precomputed index (Canal) to hold
enough of the graph to compute a flow between the assessor and a stranger.

`privacy-tiers.md` selects a cover-traffic mix network under a proven differential-privacy bound
(Karaoke, `LAZAR-OSDI-18`) as the default Message tier for point-to-point communication where
who-talks-to-whom "is itself sensitive," stating it "defends who talks to whom against an adversary
controlling the network and some servers." The tier's proven bound holds "provided at least one
server on the message's path is honest" — the guarantee is stated against exactly the kind of
server role a flow-computing party (Bazaar's centralized instance, or a party assembling Canal's
landmark index) occupies with respect to two transacting participants' own communication.

Where a linkage this architecture's reputation component depends on is formed through a real,
point-to-point interaction that the two participants themselves have routed through the Message
privacy tier — a vouch, a negotiated transaction — the mix network hides from any observing server,
including the flow-computing party, precisely the who-talked-to-whom fact reputation's own edge
needs to be recorded at all. Neither `reputation.md` nor `privacy-tiers.md` states a mechanism for
the flow-computing party to learn that a linkage exists without one of the two forming participants
disclosing it directly, outside the tier's own guarantee.

**Resolution.** This is recorded as a degradation, stated precisely, because it is the reading both
selection files' own text supports without inventing a mechanism neither states: a linkage formed
through a Message-tier-protected interaction contributes nothing to either participant's flow-based
reputation value, so the computed reputation value undercounts real linkages in proportion to how
many participants route their vouches and transactions through that tier, and a stranger who has
transacted honestly but privately is scored identically to one who has never transacted at all. The
alternative of changing a selection — requiring every linkage-forming interaction to disclose its
two endpoints to the flow-computing party regardless of the sender's chosen Message tier — is the
option `reputation.md`'s own text argues against by naming this a conflict to resolve rather than
accepting silently, but no entry in either selection file specifies how a participant would signal
"this specific message forms a reputation-relevant linkage; disclose its endpoints" without
otherwise defeating the tier for that message.

## 3. Per-neighbor bandwidth reciprocation needs a stable, mutually observed peer identity that a Fetch-tier onion circuit hides from the peer serving content

`incentives.md` selects a proportional-share reciprocation rule (PropShare, `LEVIN-SIGCOMM-08`) for
bandwidth, requiring each peer to observe "how much bandwidth a given neighbor sent it in the prior
round or rounds" so it can return upload bandwidth to that same neighbor in the following round.
`capacity-ordering.md` selects the identical rule for the same reason at its transit tier,
consuming "an observable per-round received-bandwidth signal per neighbor." Both selections depend
on two peers recognizing each other as the same counterparty across successive rounds; PropShare's
own proof of Sybil-proofness (`LEVIN-SIGCOMM-08`, §6.3) is stated over one identity splitting into
several, which presupposes that an honest counterparty's single identity is otherwise stable and
visible to the peer reciprocating with it.

`privacy-tiers.md` selects a 3-hop onion circuit as the default Fetch tier for "retrieving one
object from one peer," listing among the adversaries a direct connection fails against — and the
onion tier therefore defeats — "the serving peer" itself, alongside an on-path router and a passive
metadata collector. The tier hides the requester's identity from the very peer serving the content,
not only from a third-party observer, and the requester's own directly observed counterparty is one
hop of the circuit — an entry relay — not the peer actually serving the requested bytes.

Under the Fetch privacy tier, the peer serving content cannot attribute the request to a stable,
recognizable neighbor across rounds, and the requester's own bandwidth observation attaches to a
relay rather than to whichever peer served the object it fetched. Reciprocation credit accrues to
the wrong party, or to no party either side can carry forward, for every transfer routed through
this tier — a different failure than PropShare's own documented Sybil-splitting resistance, since
here the identity being made unstable is the counterparty's, not the reciprocating peer's own.

**Resolution.** The corpus supports treating this as a degradation rather than a selection change:
per-neighbor bandwidth reciprocation applies, and functions as `LEVIN-SIGCOMM-08` measures it, only
to transfers made under a direct connection or a Fetch-tier padding defense that still exposes a
stable serving-peer identity to the requester (WTF-PAD and Tamaraw, which pad an existing connection
rather than route it through an intermediary that hides the endpoint); a transfer routed through the
onion-circuit tier contributes nothing to either side's reciprocation ledger, and should be
disclosed to the user as outside the incentive mechanism's coverage, matching the pattern applied to
findings 1 and 2 above. Changing the selection instead — settling bandwidth using the storage
component's own retrievability-proof-and-ledger payment instead of peer-observed reciprocity for
anonymized transfers specifically — is not evaluated by any entry in this corpus, since
`incentives.md`'s own comparison of the two payment families is written for storage capacity and
bandwidth as a whole, not for the anonymized-transfer case alone. No entry in either selection file
proposes or measures a third mechanism.

## Checked and found not to compose into a conflict

- `indexing.md`'s local-index-first-with-PAC-fallback default against `privacy-tiers.md`'s strong
  privacy tier: no residual conflict, because `privacy-tiers.md` states it substitutes an entirely
  different mechanism (Tiptoe or Pacmann) for the private tier rather than routing PAC's own
  peer-sampled search through an anonymizing layer — the observability PAC needs (per-peer response
  and local statistics, `RICHARDSON-SIGIR-14`) is never asked of the privacy tier at all.
- `moderation.md`'s labeler subscriptions against `privacy-tiers.md`'s Fetch tier: no conflict — a
  client applies labels it has already fetched and holds locally; the Fetch tier's concealment of
  the client's identity from a serving peer does not prevent the client from reading a label it
  possesses.
- `key-transparency.md`'s witness auditing against every privacy tier: no conflict — Parakeet's
  witnesses are stated to observe ordinary DID-document update rounds, which are public by
  construction in `identity.md`'s own selection; no privacy tier in this corpus is selected to
  conceal an identity's own key-rotation history from a witness whose job is to detect exactly that.
- `content-location.md`'s S/Kademlia lookup against the Query-tier PIR: no conflict — `privacy-tiers.md`
  states the client must already hold the numeric index (and, by extension, already know which peer
  to query) before the PIR exchange begins; PIR hides which record was requested from that
  already-identified peer, not which peer holds it.
- `group-encryption.md`'s BeeKEM, which requires sender-authenticated delivery among group members,
  against the Message-tier mix network: no conflict on the authentication axis specifically — the
  mix network is selected to hide communication metadata from an outside network or server
  adversary, not from the group's own already-known members, and BeeKEM's authentication requirement
  is a signature check between members who already hold each other's keys.

## What this pass did not settle

Whether a private set-intersection or committed-blocklist construction could let an answering peer
test a PIR-protected query against a deny list without learning the query is not addressed by any
entry in this corpus; finding 1 records the gap rather than closing it. Whether reputation's
flow-computing party could accept a zero-knowledge proof of linkage existence, rather than the
linkage's endpoints, from two Message-tier-protected participants is not proposed or measured by
any entry in this corpus; finding 2 records the gap in the same way. No entry in this corpus
measures what fraction of bandwidth reciprocation traffic in a deployed system would actually route
through an anonymizing Fetch tier, so the practical severity of finding 3's degradation — as opposed
to its structural existence — is unmeasured here.
