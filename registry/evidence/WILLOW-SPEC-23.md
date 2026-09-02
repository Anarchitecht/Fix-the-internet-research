## [WILLOW-SPEC-23] Willow: 3d Range-Based Set Reconciliation (protocol specification)
**Citation:** Sam Gwilym, Aljoscha Meyer, and the Earthstar/Willow project contributors. "Willow: 3d Range-Based Set Reconciliation (protocol specification)." willowprotocol.org, protocol specification (not a peer-reviewed paper), funded in part by NLnet, 2023.
**Retrieved:** full text via https://willowprotocol.org/specs/rbsr/index.html
**Source URL:** https://willowprotocol.org/specs/rbsr/index.html
**Domain:** D

### What it does
The mechanism lets two peers holding entries in a three-dimensional coordinate space (a namespace subspace, a path, and a timestamp) identify which entries the other peer lacks, without either peer transmitting its whole entry set. Each Willow entry is wrapped into a `LengthyAuthorisedEntry`: the entry plus a count of how many consecutive bytes of its payload, from the start, the peer already holds. This wrapping merges two separate synchronization problems (missing entries, and entries whose payload is only partly held) into one problem: a peer either holds a `LengthyAuthorisedEntry` or does not.

Reconciliation proceeds recursively over a `3dRange`, a three-dimensional range that bounds a set of entries by subspace, path, and time. A peer that wants to compare a `3dRange` against another peer's holdings computes a `Fingerprint`, a hash over every `LengthyAuthorisedEntry` it holds inside that range, and sends a `3dRangeFingerprint` message naming the range and the fingerprint. The receiving peer computes its own fingerprint over the same range. If the fingerprints match, the peer replies with an empty `3dRangeEntrySet` for that range, signaling that reconciliation of the range is complete and no data needs to change hands. If the fingerprints differ, the receiving peer takes one of two actions: it splits the range into multiple sub-ranges and sends a `3dRangeFingerprint` for each, so the mismatch localizes recursively; or, once the range holds few enough entries, it replies with a `3dRangeEntrySet` containing every entry it holds in that range and sets a `want_response` flag, prompting the other peer to reply with its own entries (omitting anything just received) and complete the exchange for that range. A peer splitting a range must divide it so each sub-range holds close to the same number of entries the peer locally has, not so each sub-range spans equal numeric width of subspace, path, or time; splitting by numeric width defeats the recursion's efficiency because a peer cannot know in advance how its holdings are distributed across the coordinate space.

Fingerprint computation supports incremental assembly: a range's fingerprint is computable by combining the fingerprints of its sub-ranges, avoiding a full rescan on every split. Each `LengthyAuthorisedEntry` is mapped to a `PreFingerprint` by a `fingerprint_singleton` function sensitive to every field of the entry (namespace, subspace, path, timestamp, payload digest, payload length, and bytes held). `PreFingerprint`s combine pairwise through an associative and commutative `fingerprint_combine` function with a neutral element `fingerprint_neutral`, so a range's combined `PreFingerprint` can be computed in any grouping or order — commutativity is required here because the specification does not prescribe a linear order over three-dimensional coordinates, unlike the one-dimensional range-based set reconciliation this generalizes. A final `fingerprint_finalise` function maps the accumulated `PreFingerprint` to the transmitted `Fingerprint`, and the specification recommends this be a standard cryptographic hash so the wire-transmitted value stays small even if the `PreFingerprint` representation is large.

Because a peer cannot cheaply determine, from the set of ranges it has received so far, whether their union covers a range it originally asked about, the specification has the splitting peer attach metadata to the final sub-range in a split batch, stating which of the other peer's original ranges is now fully covered by the sub-ranges sent. Both peers rely on this metadata being accurate to track reconciliation progress without maintaining coverage-tracking data structures; a peer supplying inaccurate metadata degrades reconciliation, but the specification treats this as tolerable because a malicious peer already has other ways to disrupt reconciliation.

### Measured results
None. The document is a protocol specification with no reported experiment, benchmark, node count, or dataset. It states an asymptotic property only: reconciliation "collaboratively drill[s] down to the differences... in a logarithmic number of communication rounds," inherited by construction from the recursive halving, without measuring round count, message count, or bandwidth on any concrete topology.

### Parameters
- Split factor: unspecified as a fixed number. The specification states a peer "can actually split sets into arbitrarily many subsets in each step," and that splitting into more subsets per step decreases the number of communication rounds, but gives no recommended value or tested range.
- Threshold for switching from further splitting to direct entry transmission ("if the set is sufficiently small"): unspecified — no numeric threshold given.
- Fingerprint size (`Fingerprint` type): unspecified — left to the implementation, with the sole constraint that `fingerprint_finalise` must not map distinct inputs to equal outputs.

### Stated limitations
The specification states that fingerprinting is "not mandatory for Willow, but it probably is a good idea," marking the entire fingerprinting construction as optional rather than a requirement of the reconciliation protocol itself.

The metadata mechanism used to track which ranges have been fully covered has a stated failure mode: "a malicious peer could provide wildly inadequate metadata," which corrupts a peer's own view of reconciliation progress. The specification does not describe a countermeasure beyond noting that a malicious peer already has other means to disrupt reconciliation, so this is treated as an accepted exposure rather than a solved problem.

The specification defers commutativity of `fingerprint_combine` as an extra requirement not present in the one-dimensional predecessor, because it declines to prescribe a linearization of the three-dimensional coordinate space; this is stated as a design choice rather than a defended proof that no acceptable order exists.

### Requirements it places on the rest of the system
Reconciliation operates over `AuthorisedEntry` objects that already carry a `namespace_id`, `subspace_id`, `path`, `timestamp`, `payload_digest`, and `payload_length` — the rest of the system must supply and authenticate these fields before reconciliation can run, since the fingerprint function is defined over exactly this tuple.

The protocol assumes each peer can enumerate, for an arbitrary `3dRange`, the `LengthyAuthorisedEntry` set it holds inside that range, and can split that range into sub-ranges holding an approximately equal share of its local entries. This requires a local index over entries keyed by the three coordinates (subspace, path, timestamp) that supports efficient range queries and range splitting by entry count, not by coordinate-space width.

The protocol assumes each peer can determine how many consecutive bytes from the start of a given entry's payload it holds locally (the `available` field of `LengthyAuthorisedEntry`), which requires a storage layer that tracks partial payload receipt per entry rather than only complete/absent status.

Correctness of the whole scheme depends on `fingerprint_singleton` sensitivity to every entry field, together with a `fingerprint_finalise` function that maps distinct `PreFingerprint` values to distinct `Fingerprint` values with high probability even against maliciously crafted input. This is a requirement placed on whichever concrete hash function an implementation selects, not something the specification proves generically.

The `want_response` protocol state depends on message delivery and ordering being reliable enough that both peers agree on which range a given `3dRangeEntrySet` answers; the specification does not state a transport-layer requirement (e.g., ordered or reliable delivery) explicitly, leaving this implicit in the message-exchange description.

### Contradicts
None found.

### References worth retrieving
- Meyer, Aljoscha: "Range-Based Set Reconciliation." 2023 42nd International Symposium on Reliable Distributed Systems (SRDS), IEEE, 2023, pp. 59–69. — foundational (already in this corpus; this document is the direct generalization of Meyer's one-dimensional range-based set reconciliation to three dimensions).
- Minsky, Yaron; Trachtenberg, Ari; Zippel, Richard: "Set reconciliation with nearly optimal communication complexity." IEEE Transactions on Information Theory, vol. 49, Nr. 9, 2003, pp. 2213–2218. — foundational (states the general set reconciliation problem this protocol solves).

### Verbatim extracts
- "In the scientific literature, this problem is known as set reconciliation (Minsky et al., 2003)."
- "peers collaboratively drill down to the differences between their two sets in a logarithmic number of communication rounds"
- "it is crucial for overall efficiency to not split based on volume... but to split into subranges in which the peer holds roughly the same number of AuthorisedEntries"
- "a malicious peer could provide wildly inadequate metadata, but in general this is tolerable"
- "What we describe now is not mandatory for Willow, but it probably is a good idea."
