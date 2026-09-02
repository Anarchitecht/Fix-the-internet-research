## [LUBY-RFC-11] RaptorQ Forward Error Correction Scheme for Object Delivery

**Citation:** Michael Luby, Amin Shokrollahi, Mark Watson, Thomas Stockhammer, Lorenz Minder. "RaptorQ Forward Error Correction Scheme for Object Delivery." IETF RFC 6330, August 2011. DOI 10.17487/RFC6330.
**Retrieved:** full text via https://www.rfc-editor.org/rfc/rfc6330
**Source URL:** https://www.rfc-editor.org/rfc/rfc6330
**Domain:** C

### What it does
RaptorQ recovers a block of data from any sufficiently large set of received encoding symbols, so a sender can produce as many redundant symbols as needed on the fly and a receiver can reconstruct the original data after losing an arbitrary subset of transmitted symbols, without a retransmission round trip. The sender divides a source object of length F octets into Z source blocks, each source block into K source symbols of T octets each. An encoder run once per source block builds an intermediate block from the K source symbols using a fixed pseudo-random generator (1024 shared random numbers, specified in the RFC) and produces encoding symbols, each identified by an Encoding Symbol ID (ESI): ESI values 0 through K-1 reproduce the original source symbols unchanged (the code is systematic), and ESI values K and above are repair symbols computed from the intermediate block. The receiver collects encoding symbols carrying (Source Block Number, ESI) pairs from any mix of source and repair symbols and, once it holds a mathematically sufficient set, recovers the intermediate block by solving a linear system over octets (Gaussian-elimination-style rank reduction), then reconstructs any still-missing source symbols. Large source blocks are additionally split into N sub-blocks of sub-symbols to bound working-set memory during encoding and decoding; the sub-symbols of a symbol's position across all N sub-blocks concatenate to form that symbol.

### Measured results
| Result | Conditions |
|---|---|
| Decoder fails to recover the source block on average at most 1 in 100 times | Receiver holds exactly K' encoding symbols (K' = extended source symbol count), ESIs chosen independently and uniformly at random from the possible range, for every K' value in the RFC's systematic-index table |
| Decoder fails on average at most 1 in 10,000 times | Receiver holds K'+1 encoding symbols, same random-ESI condition, same K' range |
| Decoder fails on average at most 1 in 1,000,000 times | Receiver holds K'+2 encoding symbols, same random-ESI condition, same K' range |

These three figures are mandatory conformance requirements the RFC places on any compliant decoder (Section 5.8), not a measurement of one specific implementation; the RFC states its own reference decoder (Section 5.4) meets them.

### Parameters
- K'_max (maximum source symbols per source block): fixed at 56403 (Section 5.1.2); source blocks otherwise range from 1 to 56403 source symbols.
- T (symbol size): 16-bit unsigned integer, must be less than 2^16 octets, and must be a multiple of the symbol alignment parameter Al.
- Z (number of source blocks): 8-bit unsigned integer, so at most 256 per object.
- F (transfer length of the object): 40-bit unsigned integer, at most 946,270,874,880 octets; the RFC states this ceiling follows arithmetically from the T, K'_max, and Z limits above (symbol-size ceiling times per-block symbol ceiling times block-count ceiling).
- N (number of sub-blocks per source block): 16-bit unsigned integer, chosen so sub-symbol size stays at or above a target lower bound SS while remaining a multiple of Al.
- Encoding and decoding parameters (K, K', T, Z, N, Al) must be identical between encoder and receiver; construction rules for deriving them from F and T are given in Section 4.4.1.2, not left to implementation choice.

### Stated limitations
The RFC states RaptorQ provides no source authentication or corrupted-packet detection on its own: a single corrupted repair-data packet accepted as legitimate can cause the decoder to reconstruct an object that is entirely corrupted and unusable, and the RFC recommends (not requires) an appended SHA-256 hash checked post-decode, a digital signature over that hash, and a packet-authentication protocol (TESLA, RFC 4082) to detect and discard corrupted packets on arrival. The RFC also flags that FEC parameters obtained out-of-band in a session description are a separate attack surface: a forged or corrupted session description causes receivers to apply the wrong decoding parameters, and the RFC recommends source-authenticated session descriptions as the mitigation.

### Requirements it places on the rest of the system
The transport must deliver each encoding symbol tagged with its Source Block Number and Encoding Symbol ID, since decoding depends on knowing which ESI each received symbol carries. Encoder and decoder must share the object-level Common FEC Object Transmission Information (F, T) and the scheme-specific parameters (Z, N, Al) before decoding starts; these are derived once from F and T by the fixed construction rules in Section 4.4.1.2 and are not negotiated per packet. The scheme assumes symbols may arrive out of order, be duplicated, or be lost, but places no requirement on delivering symbols in ESI order. It supplies no confidentiality, integrity, or authenticity: a system built on RaptorQ must supply corruption detection (for example a hash check) and source authentication itself if a single forged repair symbol must not be able to corrupt the whole decoded object.

### Contradicts
None found.

### References worth retrieving
- Shokrollahi, Luby. "Raptor Codes." Foundations and Trends in Communications and Information Theory, Vol. 6, No. 3-4, 2011 — foundational (fuller theory treatment of the code family RaptorQ extends).
- Luby, Shokrollahi, Watson, Stockhammer. "Raptor Forward Error Correction Scheme for Object Delivery." RFC 5053, October 2007 — foundational (RaptorQ's direct predecessor, RFC 6330 states RaptorQ supports larger source blocks and better coding efficiency than this).
- Luby. "LT codes." Annual IEEE Symposium on Foundations of Computer Science, pp. 271-280, November 2002 — foundational (the original rateless/fountain code construction RaptorQ descends from).
- Luby, Vicisano, Gemmell, Rizzo, Handley, Crowcroft. "The Use of Forward Error Correction (FEC) in Reliable Multicast." RFC 3453, December 2002 — foundational (context for why FEC is used for object delivery rather than retransmission).

### Verbatim extracts
"on average the decoder will fail to recover the entire source block at most 1 out of 100 times"
"K'_max denotes the maximum number of source symbols that can be in a single source block"
"the RaptorQ code supports source blocks with between 1 and 56403 source symbols"
"The use of even one corrupted packet... may result in the decoding of an object that is completely corrupted and unusable"
