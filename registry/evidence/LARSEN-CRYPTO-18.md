## [LARSEN-CRYPTO-18] Yes, There is an Oblivious RAM Lower Bound!
**Citation:** Kasper Green Larsen, Jesper Buus Nielsen. "Yes, There is an Oblivious RAM Lower Bound!" CRYPTO, 2018. DOI 10.1007/978-3-319-96881-0_18.
**Retrieved:** full text via https://eprint.iacr.org/2018/955.pdf
**Source URL:** https://eprint.iacr.org/2018/955.pdf
**Domain:** G

### What it does
An Oblivious RAM (ORAM) lets a client store data on an untrusted server so that the sequence of server-side memory accesses the server observes reveals nothing about which read or write operations the client performed. The paper proves a lower bound on the bandwidth overhead any such construction must pay: the multiplicative factor of extra memory blocks accessed per operation compared to reading the data itself. The proof recasts the online ORAM problem as an oblivious data structure solving an array-maintenance problem (read/write to an n-entry array), then proves the bound in a new model the authors call the oblivious cell probe model, an extension of Yao's cell probe model that additionally accounts for client memory. The proof method is the information-transfer method of Patrascu and Demaine: a binary tree is built over a random sequence of M operations, each server memory access is attributed to a tree node, and the amount of information that must flow into each node's subtree bounds the number of accesses that subtree requires.

### Measured results
This is a theory paper; it contains no experiments. The results are proved bounds, not measurements, and each is stated with the class of construction it binds.

| Result | Applies to | Statement |
|---|---|---|
| Main theorem (informal Theorem 1) | Any online ORAM, n blocks of r >= 1 bits each, random oracle model | Expected amortized bandwidth overhead is Omega(lg(nr/m)) on sequences of Theta(n) operations, where m is client memory in bits; holds under only computational indistinguishability, for any server cell size w, and for arbitrary data representations |
| Simplified form | Natural parameter range r <= m <= n^(1-eps) for arbitrarily small constant eps > 0 | The bound simplifies to Omega(lg n) |
| Comparison to prior bound | Goldreich-Ostrovsky 1996 | That bound required statistical security and restricted the ORAM to "balls in bins" algorithms (block-shuffling only, no re-encoding); this paper's bound removes both restrictions |
| Matching upper bound | Path ORAM (Stefanov et al., CCS 2013) | Path ORAM achieves amortized Theta(lg n) memory-cell accesses per operation for blocks of size Omega(lg^2 n) bits, computed in the paper as Theta(lg^3 n) bits moved, a Theta(lg n) multiplicative overhead relative to the r = Theta(lg^2 n)-bit block; the paper states its own bound "asymptotically matches the known upper bounds when r = Omega(lg^2 n)" |

### Parameters
- n: number of memory blocks maintained by the ORAM.
- r: bits per block (data argument size), r >= 1.
- w: bits per server-side memory cell; the bound is stated to hold "regardless of the memory cell size w."
- m: client-side memory, in bits.
- M: number of operations in the sequence the bound is proved over, set to Theta(n).
- Failure probability: the proof in Section 3 (Theorem 2) is carried out assuming the data structure has failure probability at most 1/32, stated as a proof-convenience choice, with the paper noting the bound extends to the more standard error probability of 1/3.

### Stated limitations
The lower bound applies only to "online" ORAMs, meaning constructions that must remain secure when operations arrive one at a time without knowledge of future operations; the paper argues most ORAM constructions and most ORAM applications are of this kind, following Boyle and Naor's online-ORAM definition. The bound explicitly does not apply to "passive" ORAM's complement: constructions in which the server performs untrusted computation on the client's behalf rather than acting as passive storage, citing Onion ORAM and a 2016 proposal by Abraham et al. as examples, and the paper states most such schemes achieve sub-logarithmic overhead. The authors could not extend the stronger cell-probe lower-bound techniques of Larsen (STOC 2012) and Larsen-Weinstein-Yu (STOC 2018), which prove bounds of order lg^2 n and lg^1.5 n respectively for other problems, to the ORAM setting, and label pushing past lg n on ORAM worst-case overhead an open problem for future work. The paper also notes its security definition is slightly stricter than Boyle and Naor's: it lets the adversary observe which server accesses belong to which operation, a choice the authors justify but flag as a definitional divergence from the paper the result answers.

### Requirements it places on the rest of the system
Any component in the target architecture that stores client data on an untrusted peer or server and wants access-pattern privacy through ORAM inherits a floor: retrieving one r-bit block from an n-block online ORAM under bounded client memory costs at least a constant times lg(nr/m) times as much server-side traffic as an access-pattern-revealing read would, and this floor holds even for computationally secure constructions and even for constructions that re-encode data rather than merely shuffle blocks. The floor holds only for passive-storage ORAM; a design that instead lets the storage node compute obliviously on the client's behalf (Onion-ORAM-style) is not bound by this result and can be sub-logarithmic, so a component wanting to beat lg n overhead must place computation, not merely storage, at the peer holding the data. The bound assumes the online-operation-arrival model; a design that can batch and reorder its full operation sequence in advance falls outside this bound's stated scope (the paper distinguishes this as the "offline" setting, which is where the original Goldreich-Ostrovsky statistically-secure bound already applied).

### Contradicts
None found against other entries in this corpus. Against attribution in general: the bound is frequently summarized as applying to "statistically secure ORAM" (matching the original Goldreich-Ostrovsky statement); this paper's own contribution is that the Omega(lg n) bandwidth floor holds even for computationally secure, arbitrarily-encoding constructions, which is a strictly stronger claim than the statistically-secure-only version.

### References worth retrieving
- foundational: Goldreich, Ostrovsky. "Software protection and simulation on oblivious RAMs." J. ACM 43(3), 1996.
- foundational: Boyle, Naor. "Is there an oblivious RAM lower bound?" ITCS 2016.
- foundational: Patrascu, Demaine. "Logarithmic lower bounds in the cell-probe model." SIAM J. Comput. 35(4), 2006.
- competing: Stefanov, van Dijk, Shi, Fletcher, Ren, Yu, Devadas. "Path ORAM: an extremely simple oblivious RAM protocol." CCS 2013.
- competing: Devadas, van Dijk, Fletcher, Ren, Shi, Wichs. "Onion ORAM: A constant bandwidth blowup oblivious RAM." TCC 2016.
- competing: Abraham, Fletcher, Nayak, Pinkas, Ren. "Asymptotically tight bounds for composing ORAM with PIR." ePrint 2016/849.
- competing: Chung, Liu, Pass. "Statistically-secure ORAM with o~(log^2 n) overhead." ASIACRYPT 2014.
- foundational: Wang, Nayak, Liu, Chan, Shi, Stefanov, Huang. "Oblivious data structures." CCS 2014.
- foundational: Larsen. "The cell probe complexity of dynamic range counting." STOC 2012.
- foundational: Larsen, Weinstein, Yu. "Crossing the logarithmic barrier for dynamic boolean data structure lower bounds." STOC 2018.
- competing: Stefanov, Shi. "Oblivistore: High performance oblivious distributed cloud data store." NDSS 2013.

### Verbatim extracts
"expected amortized bandwidth overhead of Ω(lg(nr/m))"
"holds regardless of the memory cell size w"
"most of these schemes achieves sub-logarithmic overhead"
"eliminating both restrictions of the Goldreich-Ostrovsky lower bound"
