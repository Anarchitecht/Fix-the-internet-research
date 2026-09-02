## [CHASE-CRYPTO-20] Private Set Intersection in the Internet Setting From Lightweight Oblivious PRF

**Citation:** Melissa Chase, Peihan Miao. "Private Set Intersection in the Internet Setting From Lightweight Oblivious PRF." CRYPTO, 2020. DOI 10.1007/978-3-030-56877-1_2.
**Retrieved:** full text via https://eprint.iacr.org/2020/729.pdf
**Source URL:** https://eprint.iacr.org/2020/729.pdf
**Domain:** G

### What it does
Private set intersection (PSI) lets two parties, each holding a private set of elements, learn the intersection of both sets while revealing nothing else about either set. This paper's protocol targets a balance between computation time and communication volume that makes it the fastest of the compared protocols specifically on moderate-bandwidth networks (30-100 Mbps), the range the authors state matches typical U.S. fixed broadband as measured in 2018 (95.25 Mbps average download, 32.88 Mbps average upload).

The protocol builds a multi-point oblivious pseudorandom function (OPRF): a sender holds a PRF (pseudorandom function) key k, and a receiver evaluates that PRF obliviously (learning the outputs without learning k, while the sender learns nothing about the receiver's inputs) on all n of its own elements in one exchange, rather than the prior state-of-the-art protocol's single-point OPRF, which evaluates one input at a time. The receiver computes an m-row-by-w-column binary matrix D from its input set using oblivious transfer extension (OT extension: a method for producing many oblivious-transfer instances from few, using only symmetric-key operations after a small number of expensive public-key operations), then both parties derive PRF outputs from rows of this matrix using only hashing and bitwise operations. The sender separately computes the same PRF on its own set and sends the results to the receiver, who computes the intersection by matching PRF outputs. Fixing the matrix height m and set size n determines matrix width w through a collision-probability calculation (Section 3.3 of the paper); a larger m gives a smaller w and less computation, at the cost of a larger matrix to process, so the parameters are tunable to trade computation against communication.

The base protocol achieves semi-honest security (both parties follow the protocol but may try to infer extra information from the transcript) in the plain model. The authors additionally prove one-sided malicious security in the random oracle model: security holds even if the sender (the party that does not receive the intersection output) deviates from the protocol, at a stated 5-7% increase in communication over the semi-honest variant, with no additional computation cost. The receiver is not protected against acting maliciously; the paper states this asymmetric guarantee suits settings where a large organization (the sender) interacts with many individual consumers or small businesses (the receivers), because the large party has institutional reputation and controls to deter misbehavior, while consumer receivers as a class cannot all be trusted to be semi-honest.

### Measured results

Both parties hold equal-size sets of n elements throughout (n1 = n2 = n); this is not an unbalanced-set-size protocol. Benchmarks run on two Microsoft Azure virtual machines, Intel Xeon 2.40GHz CPU, 140 GB RAM, single thread per party. LAN network: 20 Gbps bandwidth, 0.1 ms round-trip time (RTT). WAN settings simulated via the Linux `tc` command at 80 ms RTT, bandwidth swept 150, 130, 100, 70, 50, 30, 10, 1 Mbps.

| Set size n | This protocol's total comm. (MB) | KKRT16 comm. (MB) | Comm. improvement | This protocol LAN time (s) | KKRT16 LAN time (s) |
|---|---|---|---|---|---|
| 2^16 | 5.34 | 8.77 | — | 0.63 | 0.34 |
| 2^20 | 87.6 | 137 | 1.56x smaller | 9.44 | 4.58 |
| 2^24 | 1,442 | 2,109 | — | 190 | 67.9 |

Communication is 1.46-1.69x smaller than KKRT16 (Kolesnikov, Kumaresan, Rosulek, Trieu, "Efficient batched oblivious PRF with applications to private set intersection," ACM CCS 2016) across the tested set sizes 2^16 to 2^24.

On the LAN network, where running time is dominated by computation rather than transfer, this protocol is 2.53-3.65x faster than SpOT-Light's speed-optimized variant (spot-fast) and 19.4-28.7x faster than SpOT-Light's communication-optimized variant (spot-low) (Pinkas, Rosulek, Trieu, Yanai, "SpOT-Light: Lightweight private set intersection from sparse OT extension," 2019). At n = 2^20: this protocol 9.44 s versus spot-fast 28.9 s (3.06x) and spot-low 271 s (28.7x). spot-low runs out of memory at n = 2^24 on this hardware and is excluded from that comparison.

At 50 Mbps bandwidth (80 ms RTT), n = 2^20: this protocol runs in 16.9 s, a 1.57x speedup over KKRT16 (26.5 s), a 1.96x speedup over spot-fast (33.1 s), and a 16.5x speedup over spot-low (279 s). Across the full 30-100 Mbps range swept, the authors state this protocol is faster than all three compared protocols, attributed to lower communication than KKRT16 combined with faster computation than both SpOT-Light variants.

Monetary cost (in currency, on Amazon Web Services EC2, using the same cost model as Pinkas et al. 2019) is reported as favorable relative to the compared protocols across the tested settings, including an AWS-cloud-sender asymmetric deployment scenario where this protocol achieves 5.01-6.48x lower monetary cost than spot-low.

### Parameters
- Computational security parameter λ = 128; statistical security parameter σ = 40.
- OT extension base parameter d = 128.
- Matrix height m: set equal to n (m = n) in all reported experiments, stated by the authors to achieve near-optimal communication and computation among all tested choices of m.
- Matrix width w: derived from n and m via the collision-probability calculation of Section 3.3; tabulated values at n = 2^16 through 2^24 range from w = 609 to w = 633 (and 349-717 when m is varied away from n at n = 2^24, tested at m = 0.9n, 1.1n, 2n).
- Hash output length l1 (collision resistance of H1) = 256 bits, set to 2*lambda.
- Hash output length l2 (collision probability of H2): semi-honest l2 = sigma + log(n1*n2), ranging 72-88 bits over the tested set sizes; malicious-security l2 = sigma + log(Q2*n2) where Q2 is the maximum adversary queries to H2, ranging 120-128 bits, with maximum adversary queries to H2 assumed at 2^64.
- Set sizes tested: n = 2^16, 2^18, 2^20, 2^22, 2^24.
- Network bandwidths tested: LAN (20 Gbps, 0.1 ms RTT) and WAN at 80 ms RTT, sweeping 150, 130, 100, 70, 50, 30, 10, 1 Mbps.

### Stated limitations
The one-sided malicious-security proof protects only against a malicious sender (the party not receiving the output); the paper does not claim or prove security against a malicious receiver. The authors state that reducing the communication cost of KKRT16 while keeping comparable computation cost was an open question that motivated this protocol; they do not claim optimality across all bandwidth regimes, only that their protocol is fastest specifically in the 30-100 Mbps moderate-bandwidth range they measured, and their own Table 2 shows KKRT16 remains faster at very low bandwidth (1 Mbps, where KKRT16's lower communication dominates) and at 150 Mbps (LAN-like, where KKRT16's lower computation dominates for the smallest set size tested). At n = 2^24, spot-low could not be benchmarked at all because it ran out of memory on the test machines, so no comparison exists at that scale.

### Requirements it places on the rest of the system
Both parties must already know the OPRF sender/receiver assignment and must both compute over sets of comparable, explicitly stated size — the measured results assume equal-size sets (n1 = n2 = n) and do not characterize behavior for a small client set against a large server set. A deployment giving this protocol's asymmetric malicious-security guarantee needs a trust assignment decision made in advance: the party accepting the semi-honest-only assumption must be the one designated sender, and the protocol supplies no mechanism to detect or recover from a malicious receiver. The OT-extension step needs a small number of base oblivious-transfer instances (a standard public-key primitive) to be generated once before the symmetric-key-only extension can run; the paper does not itself specify which base-OT construction to use for this. The matrix-height parameter m must be fixed to n (or otherwise chosen) before deployment; the paper does not describe an online mechanism for renegotiating m if set sizes change between runs.

### Contradicts
This paper's own experimental setting (n1 = n2 = n) directly contradicts the framing of it as addressing an unbalanced-set (large server set, small client set) scenario; the text explicitly states "we focus on the setting where n1 = n2 = n, i.e., the two parties have sets of equal size." Any claim describing this paper as measuring performance under set-size asymmetry is not supported by the paper as retrieved; an actual unbalanced-PSI comparison point is Resende and Aranha, "Unbalanced approximate private set intersection" (cited in this paper's own bibliography as [RA17], IACR ePrint 2017/677), not this paper. No other entry in this corpus disagrees with this paper's own measured figures.

### References worth retrieving
- foundational: Vladimir Kolesnikov, Ranjit Kumaresan, Mike Rosulek, Ni Trieu. "Efficient batched oblivious PRF with applications to private set intersection." ACM CCS, 2016. (KKRT16, the computation-optimized baseline this paper directly compares against and improves communication over)
- competing: Benny Pinkas, Mike Rosulek, Ni Trieu, Avishay Yanai. "SpOT-light: Lightweight private set intersection from sparse OT extension." 2019. (spot-fast and spot-low variants, the communication-optimized baseline)
- competing: Benny Pinkas, Mike Rosulek, Ni Trieu, Avishay Yanai. "PSI from Paxos: Fast, malicious private set intersection." EUROCRYPT, 2020.
- competing: Amanda C. Davi Resende, Diego F. Aranha. "Unbalanced approximate private set intersection." IACR ePrint 2017/677. (the actual unbalanced-set-size PSI line, misattributed to this paper by the registry's characterization)
- competing: Peter Rindal, Mike Rosulek. "Malicious-secure private set intersection via dual execution." ACM CCS, 2017.
- competing: Peter Rindal, Mike Rosulek. "Improved private set intersection against malicious adversaries." EUROCRYPT, 2017.
- foundational: Benny Pinkas, Thomas Schneider, Michael Zohner. "Faster private set intersection based on OT extension." USENIX Security, 2014.
- competing: Daniel Kales, Christian Rechberger, Thomas Schneider, Matthias Senker, Christian Weinert. "Mobile private contact discovery at scale." USENIX Security, 2019.

### Verbatim extracts
- "our protocol is the fastest in networks with moderate bandwidth (e.g., 30-100 Mbps)"
- "we focus on the setting where n1 = n2 = n, i.e., the two parties have sets of equal size"
- "our protocol also achieves security in the random oracle model when one of the parties is malicious"
- "the total communication cost of our protocol is 1.46-1.69x smaller than that of KKRT"
- "our protocol achieves a 2.53-3.65x speedup comparing to spot-fast"
- "achieving 5.01-6.48x lower monetary cost than spot-low"
