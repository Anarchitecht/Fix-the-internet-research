## [SHAPIRO-EATCS-11] Convergent and Commutative Replicated Data Types

**Citation:** Marc Shapiro, Nuno Preguiça, Carlos Baquero, Marek Zawirski. "Convergent and Commutative Replicated Data Types." Bulletin of the European Association for Theoretical Computer Science (EATCS), No. 104, 2011. Pages 67-88.
**Retrieved:** full text via https://drops.dagstuhl.de/opus/volltexte/2011/eatcs/2011_bulletin_104.pdf
**Source URL:** https://drops.dagstuhl.de/opus/volltexte/2011/eatcs/2011_bulletin_104.pdf
**Domain:** D

### What it does
A Conflict-free Replicated Data Type (CRDT) is a data type whose replicas converge to the same state after every replica has received the same set of updates, without any coordination protocol (locking, consensus, or synchronous agreement) between replicas during normal operation. This paper is the expository companion to the SSS 2011 conference paper (SHAPIRO-SSS-11), giving the same two sufficient conditions for convergence with longer worked examples (Registers, Sets, Graphs, a bookstore shopping cart) and a dedicated treatment of garbage collection that the conference paper omits.

Two update-propagation styles are defined, proved equivalent to each other (one can emulate the other), and each given one sufficient convergence condition:

- State-based (Convergent Replicated Data Type, CvRDT): every update executes locally against the full replica state, then the entire updated state (or a delta) is transmitted to other replicas, which fold it in with a merge function. If a replica's payload takes values in a join semilattice — a partially ordered set with a least-upper-bound (LUB) operation ⊔ for every pair of elements — and every update moves the payload strictly forward in that order (monotonic), and merge computes the LUB of the local and delivered states, then two replicas that each receive every update infinitely often converge to the same state. The LUB operation is commutative, idempotent, and associative, so the communication subsystem may lose messages, reorder them, or deliver them multiple times without breaking convergence, as long as every update eventually reaches every replica by some path.
- Operation-based (Commutative Replicated Data Type, CmRDT): the at-source phase of an update runs once at the initiating replica with no side effect other than producing the operation and its arguments to broadcast; the downstream phase, which mutates the payload, runs at every replica (including the source) once its precondition holds there. If every pair of concurrent operations (operations not ordered by happened-before) commutes, and the communication subsystem delivers every update to every replica in causal order (an update that happened-before another is delivered first everywhere), then replicas converge.

Worked examples given: Last-Writer-Wins Register (LWW-Register, state- and op-based), Multi-Value Register (MV-Register, keeps all concurrently-written values instead of picking one), two-phase Set (2P-Set, an add-set and a remove-set with add-wins-once semantics, i.e., an element once removed cannot be re-added), Observed-Remove Set (OR-Set, tags every added element with a unique identifier so a concurrent add and remove of the "same" logical element do not collide), and an Observed-Remove Map extending OR-Set for a shopping-cart application (ISBN to quantity).

### Measured results
This is a formal-methods and design paper with no implementation benchmark, simulation, or deployment measurement. It states no throughput, latency, message-count, or storage-overhead figures under stated experimental conditions. The paper's only quantitative content is the asymptotic and structural argument that op-based CmRDTs avoid the storage overhead of certain metadata (see Parameters, "tombstone" and "version vector" comparisons below), stated as a design-level claim rather than a measured one.

### Parameters
- Semilattice partial order ≤_v and LUB operator ⊔_v: object-type-specific, chosen so every update is monotonic (non-decreasing) in ≤_v; this is a design choice per CvRDT type, not a tunable runtime parameter.
- Causal-history tracking: state-based objects track C(x_i), the set of updates that have taken effect at replica i, used to prove convergence; the paper does not give a wire-format cost for this history but notes it as the formal device the convergence proof relies on.
- Stability detection (Section 4, garbage collection): an update f is "stable" at replica i when every update concurrent with f has already taken effect at i; liveness of stability detection requires that the set of replicas be known and that no replica crashes permanently and undetectably. This is a precondition, not a numeric tunable.
- Two garbage-collection classes are distinguished by their synchronization requirement: discarding metadata once an update is stable requires no synchronization beyond that already needed for delivery; resetting payload across all replicas (removing tombstones from a 2P-Set, trimming a version vector, rebalancing a replicated tree) requires a commitment protocol among a "core" stable subset of replicas, per Létia et al., cited as prior work applied to the Treedoc sequence CRDT.

### Stated limitations
The system model assumes non-Byzantine processes that may crash and recover with memory intact; Byzantine-tolerant replication is out of scope. State-based objects require only that the communication subsystem eventually deliver every update to every replica, arbitrarily many times, out of order, or with loss tolerated as long as delivery eventually happens; op-based objects additionally require causal-order delivery, a stronger requirement supplied by the communication layer, not by the CRDT logic itself. The 2P-Set and derived types (Containers, Maps, Graphs, Sequences built on Sets) that use a tombstone-based remove cannot re-add an element once removed under the plain 2P-Set semantics; the OR-Set removes that restriction but a removed-then-readded element is tracked as a logically new element via a unique identifier, not as the same element restored. Version-vector-based approaches (cited via comparison to Dynamo's MV-Register) impose a cost the OR-Set-based shopping cart design explicitly avoids, but the paper does not quantify that cost. The paper states its future work includes evaluating CRDT performance "analytically and experimentally," meaning no such evaluation exists in this paper. It also identifies as open the question of adding infrequent strongly-consistent (linearizable) operations to an otherwise eventually-consistent CRDT design, citing Serafini et al.'s result that the ◇S failure detector is insufficient to solve that problem under a requirement that all operations terminate.

### Requirements it places on the rest of the system
- CvRDT convergence requires the communication subsystem to deliver every update to every replica infinitely often (eventually, possibly with loss, reordering, or duplication tolerated); it does not require causal or any other ordering guarantee. A component selecting the state-based style needs only a best-effort anti-entropy or gossip transport, not a causal broadcast layer.
- CmRDT convergence requires the communication subsystem to deliver updates in causal order to every replica: for any two updates f and g where f happened-before g, f must be delivered before g at every replica. A component selecting the operation-based style must supply causal broadcast, which itself requires the network to track and enforce a happened-before relation (e.g., via vector clocks or an equivalent mechanism) — this is a stronger requirement than the state-based style needs.
- Both styles assume objects are independent and do not consider cross-object transactions; a system composing multiple CRDT-typed objects with a cross-object invariant is explicitly outside this paper's model.
- Garbage collection that discards stability-tracked metadata requires that the full set of replicas be known and that no replica crash permanently without being detected as such; a system with unbounded or unknown replica membership (an open peer-to-peer network without a fixed replica set) cannot use this class of garbage collection without first supplying replica-membership knowledge.
- Garbage collection that resets payload globally (tombstone removal, version-vector trimming) requires a commitment protocol among a designated stable "core" subset of replicas; a fully decentralized system without a distinguished core needs to construct that subset itself before this class of garbage collection is available.

### Contradicts
None found within this corpus. This paper and SHAPIRO-SSS-11 present the same two sufficient conditions; no numeric disagreement exists between them because neither states a measured figure.

### References worth retrieving
- foundational: Baquero, Moura. "Specification of convergent abstract data types for autonomous mobile computing." Technical report, Universidade do Minho, 1997. (Origin of the CvRDT formalization this paper extends.)
- foundational: Baquero, Moura. "Using structural characteristics for autonomous operation." Operating Systems Review 33(4), 1999.
- competing: Ellis, Gibbs. Operational Transformation (OT) for shared editing, cited as the alternative op-based Sequence approach that transforms operations against concurrent history rather than designing for commutativity; the paper cites Oster et al. showing most decentralized OT algorithms are incorrect.
- competing: Roh et al. "Replicated Abstract Data Type," independently developed, generalizes Last-Writer-Wins to a partial order of updates.
- competing: Alvaro et al., the Bloom programming language, enforces eventual consistency via logical monotonicity but does not support remove without synchronization.
- attack/critique: Oster et al., cited as demonstrating that most Operational Transformation algorithms for decentralized architectures are incorrect (specific venue not given in this excerpt).
- foundational: Preguiça, Shapiro et al., Treedoc, a Sequence CRDT for collaborative text editing based on approximating a continuum as a binary tree.
- foundational: Serafini et al., result that the ◇S failure detector is insufficient to guarantee termination when mixing strong (linearizable) and weak operations; motivates this paper's stated future work.
- foundational: Létia et al., core-replica commitment protocol for CRDT garbage collection, applied to Treedoc.

### Verbatim extracts
- "successive states of an object should form a monotonic semilattice"
- "concurrent operations should commute"
- "Assuming only that the communication subsystem eventually delivers"
- "Causal delivery... is sufficient to ensure that the downstream precondition is true"
- "reliable causal delivery does not require agreement"
- "does not have the cost of the version vectors needed by Dynamo's MV-Register"
- "the ◇S failure detector is insufficient for solving this problem"
