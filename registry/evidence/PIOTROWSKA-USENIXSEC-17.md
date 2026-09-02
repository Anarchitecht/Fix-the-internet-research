## [PIOTROWSKA-USENIXSEC-17] The Loopix Anonymity System
**Citation:** Ania M. Piotrowska, Jamie Hayes, Tariq Elahi, Sebastian Meiser, George Danezis. "The Loopix Anonymity System." 26th USENIX Security Symposium, 2017.
**Retrieved:** full text via https://www.usenix.org/system/files/conference/usenixsecurity17/sec17-piotrowska.pdf
**Source URL:** https://www.usenix.org/system/files/conference/usenixsecurity17/sec17-piotrowska.pdf
**Domain:** G

### What it does
Loopix provides bidirectional sender and receiver anonymity and unobservability for message-based communication against a global passive adversary (GPA), an adversary that observes all links between network nodes. It routes each message through a fixed number of mix nodes arranged in layers, so that intermediate nodes learn only routing metadata, using the Sphinx packet format (layered encryption plus a message authentication code (MAC) per hop that detects tagging and replay). Each hop applies an independent random delay drawn from an exponential distribution, so a mix node is a Poisson mix: the time a message spends inside it is memoryless, which prevents an observer from correlating arrival and departure times beyond the number of messages currently held. Every client and mix node also emits continuous cover traffic — self-addressed "loop" messages and destination-dropped "drop" messages — so that the volume and rate of traffic a network observer sees is independent of whether the client is sending genuine payload traffic. The network topology is stratified: nodes are organized into layers, each mix node connects only to nodes in the adjacent layer, so the number of links a message can take is bounded and cover traffic concentrates on those links rather than being diffused across an unstructured mesh. Providers form the first and last layer; each user registers with one provider, which injects that user's traffic into the mix network, stores messages for offline recipients in a per-client inbox, and serves pull requests, itself padded with dummy responses so an observer cannot infer inbox occupancy from provider traffic. A mix node under an (n-1) attack — an adversary that blocks all incoming messages except a target message, to link that message to its output deterministically — is caught because the mix's own self-addressed loop messages stop returning at the expected rate; the mix compares the observed return rate against a threshold to detect the attack.

### Measured results
| Result | Value | Conditions |
|---|---|---|
| Mix node bandwidth saturation point | traffic through a single mix node increases linearly with client sending rate up to approximately 225 messages/second, then flattens | AWS EC2 m4.4xlarge mix node instances (2.3 GHz, 64 GB RAM), m4.16xlarge providers (256 GB RAM); 6 mix nodes in 3 layers of 2 nodes; 4 providers, ~125 clients each; 500 total clients; fixed delay parameter mu=1000 (mean delay 1 ms); starting rates lambda_L=lambda_D=1, lambda_P=3 messages/min per client, mix loop rate lambda_M=1, each rate stepped up by 2 messages/min |
| Per-packet mix processing latency | approximately 0.6 ms per packet, dominated by one elliptic-curve scalar multiplication plus symmetric cryptographic operations | same EC2 deployment; measured via tcpdump traffic captures |
| Latency overhead vs. client count | increasing online clients from 50 to 500 raises latency overhead by only 0.37 ms | 6-mix-node network; all clients set lambda_P=lambda_L=lambda_D=10 messages/min, mix loop rate lambda_M=10 messages/min, zero added artificial per-hop delay (isolates processing overhead from mixing delay) |
| End-to-end latency distribution | Gamma-distributed, mean 1.93 s, standard deviation 0.87 s | 500 users, all rates (lambda_P=lambda_L=lambda_D=lambda_M) = 60 messages/min, per-hop delay drawn from Exp(mu=2), i.e. mean per-hop delay 0.5 s, measured by timing mix-node loop messages traversing the system |
| Anonymity metric (likelihood-difference epsilon) vs. delay | epsilon falls toward zero as lambda/mu increases; the paper states lambda/mu >= 2 as a good operating point | 100 senders, sending rate lambda=2, 3-layer topology with 3 nodes/layer, zero corrupt mix nodes, averaged over 100 repetitions with reported standard deviation |
| Anonymity metric vs. number of mix layers | epsilon falls toward zero as layer count rises; the paper states 3 or more layers as a good choice | lambda=2, mu=1, 3 nodes per layer, zero corrupt mix nodes, 100 repetitions |
| Anonymity metric vs. fraction of corrupt mix nodes | epsilon rises monotonically with the fraction of (passively) corrupted mix nodes | lambda=2, mu=1, 3-layer topology with 3 nodes/layer, corruption assigned uniformly at random, 100 repetitions |
| Entropy of a single mix's output distribution vs. incoming traffic rate | entropy rises with incoming traffic rate lambda, and rises further at higher mean delay 1/mu | single simulated Poisson mix node, entropy computed from the recorded traffic-flow distribution via the simpy Python discrete-event package, 50 simulations averaged per data point |

Experimental setup is capped at 500 simultaneous clients by hardware port and memory limits of the test deployment (one m4.16xlarge instance hosting all clients); the paper states a production deployment would scale to a larger client base but reports no measurement beyond 500.

### Parameters
| Parameter | Symbol | Value(s) used | Range tested |
|---|---|---|---|
| Loop cover-traffic rate (per client) | lambda_L | starts at 1 msg/min, stepped by 2 msg/min in the bandwidth experiment; 10 msg/min and 60 msg/min in other experiments | 1 to 60+ msg/min across experiments |
| Drop cover-traffic rate (per client) | lambda_D | same schedule as lambda_L | 1 to 60+ msg/min |
| Payload traffic rate (per client) | lambda_P | starts at 3 msg/min | 3 to 60 msg/min |
| Mix loop cover-traffic rate | lambda_M | starts at 1 msg/min | 1 to 60 msg/min |
| Mean per-hop mix delay parameter | mu | 1000 (mean delay 1 ms) in the bandwidth experiment; mu=2 (mean 0.5 s) in the latency-distribution experiment; mu=1 in the anonymity-vs-layers and anonymity-vs-corruption experiments | mu=1 to mu=1000 across experiments |
| Number of mix layers | l | 3 (default anonymity experiments); varied for the layer-count experiment | 1 to roughly 9 layers tested for the layer-count experiment |
| Mix nodes per layer | -- | 2 in the performance evaluation; 3 in the anonymity evaluation | -- |
| Recommended ratio of sending rate to delay | lambda/mu | -- | authors state lambda/mu >= 2 as "a good choice" for anonymity, based on the epsilon-vs-mu experiment |
| Number of providers | -- | 4, each serving approximately 125 of the 500 clients | -- |
| Cryptographic curve | -- | NIST/SECG P-224, modified into the Sphinx packet format | -- |

### Stated limitations
The paper explicitly leaves reliable message delivery, session management, and flow control unaddressed, citing statistical disclosure attacks as an open risk for future flow-control designs. It leaves quantitative analysis of reply mechanisms (attaching a sender address to the payload, or single-use anonymous reply blocks) as future work. Receiver unobservability is not perfect when the recipient's egress provider is corrupt: an egress provider can tell whether a client is receiving any messages at all, though it cannot determine whether a given received message is genuine payload or a self-addressed loop; the paper states that quantifying the exact information leakage under this threat is left for future work. The paper explicitly excludes Sybil attacks from its threat model, assuming honest providers hold the fraction of adversary-controlled users to a small known bound. It assumes a privacy-preserving lookup or introduction system already exists to let a sender learn a receiver's provider address and identifier; building that system is out of scope. Anonymous blacklisting, payment-gated access, and privacy-preserving network measurement are described as benefits the provider architecture could support, but none are designed or evaluated in the paper.

### Requirements it places on the rest of the system
Loopix requires an external mechanism, not built in this paper, that lets a sender learn a receiver's provider IP address, per-provider client identifier, and public encryption key before a message can be sent — the paper names DP5 and MP3 as candidate "presence" systems but does not integrate one. It requires each user to register with exactly one provider, which must be honest for receiver unobservability to hold, and requires that providers respond to pull requests with dummy-padded traffic regardless of actual inbox occupancy. It requires clients to run a continuous, independent Poisson-process sender for loop and drop cover traffic even while idle, which composes on the client's total bandwidth cost with any application-layer traffic and cannot be suspended without collapsing the unobservability guarantee. It requires the network to remain online continuously — there is no batching-round synchronization — so clients need transport connectivity to their provider at loop-cover-traffic rate at all times, not only when sending genuine traffic. It assumes the fraction of adversary-corrupted mix nodes and providers stays below the levels the epsilon-vs.-corruption measurement covers, and provides no defense against a Sybil attack that inflates the adversary-controlled user fraction beyond what a provider can screen out at registration.

### Contradicts
None found within this batch. The paper's own comparison table (Table 3) states that Loopix, unlike Vuvuzela and Stadium, needs no synchronized rounds and provides offline storage, so any claim that Loopix requires round synchronization would misattribute a property of the round-based systems it is compared against.

### References worth retrieving
- Foundational: G. Danezis, R. Dingledine, "Sphinx" packet format (cited as [16], underlying packet construction).
- Foundational: A. Serjantov, G. Danezis, "Towards an information theoretic metric for anonymity," PETS 2002 (cited as [40], the Shannon-entropy anonymity metric used in Section 4.1.3).
- Foundational: A. Serjantov, R. Dingledine, P. Syverson, "From a trickle to a flood: Active attacks on several mix types," Information Hiding 2002 (cited as [41], defines the (n-1) attack Loopix defends against).
- Competing: J. Van den Hooff, D. Lazar, M. Zaharia, N. Zeldovich, "Vuvuzela: Scalable private messaging resistant to traffic analysis," SOSP 2015 (cited as [46]; two-server design compared directly in Table 3).
- Competing: N. Tyagi, Y. Gilad, M. Zaharia, N. Zeldovich, "Stadium: A Distributed Metadata-Private Messaging System," eprint 2016/943, later SOSP 2017 (cited as [45]; also in this batch as TYAGI-SOSP-17).
- Competing: D. I. Wolinsky, H. Corrigan-Gibbs, B. Ford, A. Johnson, "Dissent in numbers," OSDI 2012 (cited as [47]).
- Competing: A. Kwon, H. Corrigan-Gibbs, S. Devadas, B. Ford, "Atom: Scalable Anonymity Resistant to Traffic Analysis," CoRR abs/1612.07841 (cited as [30]).
- Competing: Y. H. Kwon, "Riffle: An efficient communication system with strong anonymity," MIT PhD thesis, 2015 (cited as [31]).
- Attack/critique: A. Serjantov, R. E. Newman, "On the anonymity of timed pool mixes," 2003 (cited as [42]).
- Attack/critique: V. Shmatikov, M.-H. Wang, "Timing analysis in low-latency mix networks: Attacks and defenses," ESORICS 2006 (cited as [44]).
- Attack/critique: Y. Zhu, X. Fu, R. Bettati, W. Zhao, "Anonymity analysis of mix networks against flow-correlation attacks," GLOBECOM 2005 (cited as [48]).
- Foundational: D. Lazar, N. Zeldovich, "Alpenhorn: Bootstrapping secure communication without leaking metadata," OSDI 2016 (cited as [32]; candidate presence/lookup system).
- Foundational: R. Parhi, M. Schliep, N. Hopper, "MP3: A More Efficient Private Presence Protocol," arXiv:1609.02987, 2016 (cited as [37]; candidate presence system).

### Verbatim extracts
- "mix nodes in Loopix can handle upwards of 300 messages per second, at a small delay overhead"
- "we observe that the bandwidth of the mix node increases linearly until it reaches around 225 messages per second"
- "increasing the number of online clients, from 50 to 500, raises the latency overhead by only 0.37 ms"
- "the end-to-end latency ... fits the Gamma distribution with mean 1.93 and standard deviation 0.87"
- "we do not expect a large fraction of mix nodes to be corrupt"
- "Loopix does not guarantee perfect receiver unobservability in the presence of a corrupted egress provider"
- "effectively excluding Sybil attacks ... from the Loopix threat model"
