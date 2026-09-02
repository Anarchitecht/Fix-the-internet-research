## [JACOB-MIDDLEWARE-19] A Glimpse of the Matrix: Scalability Issues of a New Message-Oriented Data Synchronization Middleware

**Citation:** Florian Jacob, Jan Grashöfer, Hannes Hartenstein. "A Glimpse of the Matrix: Scalability Issues of a New Message-Oriented Data Synchronization Middleware." ACM Middleware Demos/Posters (extended version), 2019. DOI 10.1145/3366627.3368106.
**Retrieved:** full text via https://arxiv.org/abs/1910.06295
**Source URL:** https://arxiv.org/abs/1910.06295
**Domain:** J

### What it does
The paper measures the deployed public Matrix federation and derives a formula that predicts the number of inter-server transactions each homeserver must send and receive from the measured network structure. Matrix is a federated publish-subscribe middleware: a topic in Matrix is called a room, each user connects only to their own homeserver, and for each room every participating homeserver holds a replicated, eventually-consistent copy of the room's message history plus derived state. A homeserver that originates an event sends one separate transaction to every other homeserver participating in the room, so the transmission side of the protocol is asymmetric with the reception side. The authors built a crawler bot, DSN Traveller, that joins public rooms known to it through the Matrix Voyager room list and records which users and homeservers appear in each room, producing a snapshot of the public federation's tripartite user-room-server graph. They then derive closed-form expressions for the outgoing transaction count tx_s and incoming transaction count rx_s of a homeserver s, as a function of the assumed fixed average per-user message rate lambda, the rooms a homeserver's users participate in, and the count of foreign homeservers Fr in each of those rooms. Applying these expressions to the crawled network structure produces a per-server load distribution the authors compare against server rank by user count.

### Measured results

| Quantity | Value | Conditions |
|---|---|---|
| Rooms joined by crawler | 798 | Snapshot taken 2018-07-25, public Matrix federation only |
| Users observed | 131,463 | Same snapshot |
| Homeservers observed | 2,003 | Same snapshot; crawler saw about two-thirds of the servers known to Matrix Voyager at that time |
| Homeservers with more than 100 users | 15 of 2,003 | Same snapshot |
| Largest homeserver user count | 76,271 | Same snapshot |
| Second-largest homeserver user count | 37,751 | Same snapshot |
| Share of all 131,463 users held by the top 1% of homeservers | 87% | Same snapshot |
| Largest room, server count | 581 servers (76% of all known servers) | Same snapshot |
| Rooms with fewer than 10 servers | 83% of all 798 rooms | Same snapshot |
| Rooms with 100 users or fewer | 71% of all 798 rooms | Same snapshot; largest room had 24,729 users |
| Rooms in the rightmost server-count histogram bin (most servers) | maximum 7,756 users, median 1,542 users | Same snapshot |
| Users seen in three or fewer rooms | 94% of all discovered users | Same snapshot |
| Most rooms a single user appeared in | 207 rooms (27% of all rooms crawled) | Same snapshot |
| Single largest homeserver's share of all inter-server messages | 44.5% of all messages, 88.4% of all sent messages, 0.6% of all received messages | Derived by applying the transaction-count formula (their Equation 2 and 3) to the measured 2003-server network structure; formulas cross-checked against a Monte-Carlo simulation |
| Bottom-ranked ~3 servers by user count (of the 2003) | receive almost 100% of all received messages combined but send only about 10% of all sent messages, comprising just above 50% of all traffic | Same derivation, same snapshot |
| Remaining top-ranked servers (of the 2003) | send about 90% of all sent messages while receiving almost none, comprising just below 50% of all traffic | Same derivation, same snapshot |

### Parameters
Average per-user message rate lambda: held fixed and uniform across users in the analytical model; no measured value is given because per-transaction timing was not recorded, for privacy reasons. Room selection: modeled as uniform, meaning a user sends to any room they participate in with equal probability. No batching of events into transactions is modeled, which the authors state causes the model to overestimate the transaction count relative to the deployed Synapse homeserver implementation, which does batch.

### Stated limitations
The model assumes all participants are honest, sending only message events, so it excludes the State Resolution Algorithm Matrix uses to reconcile conflicting state changes. Servers in the model are always reachable, process an unbounded number of events in parallel with no delay, and put transactions on the wire instantly with no acknowledgement wait, which the authors state overestimates the transaction count because no batching is modeled. Private, invite-only rooms are absent from the crawl entirely, because the crawler can only join rooms it can discover as public; the authors state they expect this absence explains an otherwise-unexplained peak in their room-size histogram. No adversarial or Byzantine servers are modeled. The paper states the routing algorithm evaluated is already problematic for the measured (party centralized) network structure, and separately derives that a transition toward a less centralized federation, before reaching full decentralization, worsens the peak per-server load rather than improving it, because a server whose user leaves for a new homeserver still has to send that user's data to every other server in every room, while the new homeserver only has to receive it. The paper offers only a room-structure-adaptive routing concept as future work, not an implemented or evaluated solution.

### Requirements it places on the rest of the system
Homeserver-to-homeserver load balancing by relocating users cannot be used as a mitigation, because Matrix homeservers hold only limited mutual trust and a receiving server cannot compel a sending server's user population to redistribute. Any group communication mechanism substituted for Matrix's current per-room full broadcast needs, at minimum, per-room visibility into which servers participate and how many users each holds, since the paper's own proposed room-structure-adaptive mechanism depends on servers exchanging exactly that information before agreeing on a per-room communication mode. A system adopting Matrix-style full-history replication per room for group communication should expect send load to concentrate on whichever server holds the largest active user population in a room, independent of how many total servers or users that room has, so any component depending on that server's send capacity needs a load bound stated for the single largest participant, not an average across participants.

### Contradicts
None found.

### References worth retrieving
- Werner Vogels, "Eventually consistent," Communications of the ACM 52.1 (2009), pp. 40-44 — foundational (eventual consistency, the model Matrix's replicated room history relies on).
- Elias Koutsoupias, Christos Papadimitriou, "Worst-case equilibria," Annual Symposium on Theoretical Aspects of Computer Science, Springer, 1999, pp. 404-413 — foundational (Price of Anarchy concept the paper invokes for the proposed optimization framing).
- Avinash Lakshman, Prashant Malik, "Cassandra: a decentralized structured storage system," ACM SIGOPS Operating Systems Review 44.2 (2010), pp. 35-40 — competing (a decentralized structured-storage system cited as related replication architecture).
- Ksenia Ermoshina, Francesca Musiani, Harry Halpin, "End-to-end encrypted messaging protocols: An overview," International Conference on Internet Science, Springer, 2016, pp. 244-254 — foundational (survey of the messaging-protocol space Matrix sits in).
- Alex Balducci, Jake Meredith, "Olm cryptographic review," NCC Group PLC technical report, 2016 — foundational (security review of Matrix's own end-to-end encryption layer, Olm).
- Maciej Rostanski, Krzysztof Grochla, Aleksander Seman, "Evaluation of highly available and fault-tolerant middleware clustered architectures using RabbitMQ," 2014 Federated Conference on Computer Science and Information Systems, IEEE, 2014, pp. 879-884 — competing (measured evaluation of a different message-oriented middleware's clustered architecture).

### Verbatim extracts
- "the sending server does n − 1 individual transmissions to each receiving server."
- "the single, largest server is involved in 44.5% of all messages, sends 88.4%, but receives only 0.6%"
- "moving from a centralized network to a more decentralized one will not improve the load distribution, but can actually make it worse"
- "load balancing can not be achieved by moving users away from busy servers as with non-federated middlewares"
- "all private, invite-only rooms are missing in the data"
