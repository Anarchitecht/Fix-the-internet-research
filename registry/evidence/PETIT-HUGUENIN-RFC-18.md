## [PETIT-HUGUENIN-RFC-18] Session Traversal Utilities for NAT (STUN)

**Citation:** Marc Petit-Huguenin, Gonzalo Salgueiro, Jonathan Rosenberg, Dan Wing, Rohan Mahy, Philip Matthews. "Session Traversal Utilities for NAT (STUN)." IETF RFC 8489 (obsoletes RFC 5389), February 2020. DOI 10.17487/RFC8489.
**Retrieved:** full text via https://www.rfc-editor.org/rfc/rfc8489
**Source URL:** https://www.rfc-editor.org/rfc/rfc8489
**Domain:** L

### What it does
STUN (Session Traversal Utilities for NAT) lets a client learn the public IP address and port a network address translator (NAT) has assigned to it, and lets two endpoints check that a path between them actually carries packets, without requiring any special behavior from the NAT itself. The client sends a Binding request to a STUN server over UDP, TCP, TLS, or DTLS. As the request passes through one or more NATs on the way to the server, each NAT rewrites the packet's source IP address and port; by the time the request reaches the server, its source transport address is the address and port assigned by the outermost NAT relative to the server, called the client's reflexive transport address. The server copies that observed source address into an XOR-MAPPED-ADDRESS attribute in its Binding response and returns it to the client. The value is XOR'd with a fixed 32-bit magic cookie (and, for IPv6, also with the 96-bit transaction ID) before encoding, specifically because deployment experience with RFC 3489's unencoded MAPPED-ADDRESS attribute found that some NATs rewrite any 32-bit payload matching the NAT's own public IP address, in a misguided attempt at generic address translation, which corrupted the attribute and broke STUN's message-integrity check; XOR encoding avoids producing a byte pattern the NAT would recognize as an address to rewrite. Every STUN message carries a fixed 20-byte header (message type, length, the magic cookie, and a 96-bit transaction ID) followed by zero or more Type-Length-Value attributes; the transaction ID lets a client match a response to its request. This document defines a single method, Binding, usable either as a request/response transaction or as a one-way indication (used to refresh a NAT binding without requesting a new address determination).

STUN by itself is stated explicitly not to be a complete NAT traversal solution; it is a tool other protocols (the RFC states Interactive Connectivity Establishment, ICE, and SIP outbound as examples) build traversal procedures on top of.

### Measured results
None. This document is a protocol specification defining message formats, attribute encodings, and normative client and server behavior; it contains no experimental measurement, deployment trial, or dataset of any kind. Any figure describing STUN success rates, latency, or NAT-type prevalence must come from a separate measurement paper, not from this document.

### Parameters
- RTO (Retransmission TimeOut) over UDP or DTLS-over-UDP: computed as an estimate of round-trip time per RFC 6298, with the initial value RECOMMENDED to be greater than or equal to 500 ms (500 ms specifically recommended for fixed-line access links); doubles after each retransmission; SHOULD be maintained at 1 ms accuracy rather than rounded to the nearest second.
- Rc (retransmission count over UDP/DTLS-over-UDP): SHOULD be configurable, default 7 total requests sent before giving up.
- Rm (final-wait multiplier): SHOULD be configurable, default 16; after the last (7th) retransmission, the client waits Rm times RTO for a response before declaring the transaction failed.
- Worked timeout example given in the spec, at the default RTO of 500 ms: retransmissions at 0 ms, 500 ms, 1500 ms, 3500 ms, 7500 ms, 15500 ms, 31500 ms, and a total transaction timeout at 39500 ms if no response arrives.
- Ti (TCP/TLS-over-TCP transaction timeout): SHOULD be configurable, default 39.5 s, stated to be chosen to equalize the TCP and UDP total-timeout values under their respective default parameters.
- Outstanding-transaction limit: absent another rate limit (such as one imposed by ICE connectivity checks or by running STUN over TCP), a client SHOULD limit itself to 10 outstanding transactions to the same server at once.
- RTO caching: the RTO value SHOULD be cached by the client per server (keyed by IP address) after a transaction completes and reused as the starting RTO for the next transaction to that server; SHOULD be considered stale and discarded if no transaction to that server has occurred in the last 10 minutes.
- Magic cookie: fixed 32-bit value 0x2112A442, present in every STUN message header.

### Stated limitations
STUN is stated explicitly not to be a NAT traversal solution by itself, only a tool used within one. The document states that protecting the reflexive address against modification using a message-integrity check is impossible in the common case of STUN run directly over UDP, because an on-path attacker can alter the packet's source IP address before it reaches the server and no message-integrity value can cover the source address field, since the NAT itself must be able to modify it; the document states the client must instead verify the learned reflexive address by other means, citing ICE as one usage that does this. The bid-down defense against forcing weaker password-hashing algorithms cannot detect the attack until the server receives the second (post-authentication) request, and SHA-256, the new default password hash, is stated to do little to deter brute-force search of a weak password because it is a comparatively fast algorithm; a stronger algorithm such as Argon2 is cited as unadopted-by-default here. STUN's HMAC-based authentication is stated to be subject to offline dictionary attack when a weak password is used and the channel is unprotected by TLS or DTLS. A rogue client can use a STUN server as a reflector by spoofing its source address so the server's response is delivered elsewhere; the document states this produces no packet-count amplification (one response per request) but a modest increase in bytes, and that ingress source-address filtering mitigates it — a network-layer countermeasure external to the protocol itself.

### Requirements it places on the rest of the system
A STUN Binding transaction requires a STUN server reachable by the client over the chosen transport (UDP, TCP, TLS, or DTLS) and requires that at least one NAT between client and server perform address/port translation on the outbound packet for the mechanism to produce a useful reflexive address; on a path with no NAT, the server simply returns the client's own address. Any usage that needs to trust the returned reflexive address against an on-path attacker must supply its own verification step, since STUN's own message-integrity mechanism cannot protect the source-address field; the document names ICE connectivity checks as the verification mechanism it expects usages to rely on, but that verification is out of scope for this document itself. A usage multiplexing STUN traffic with other protocol traffic on the same port must supply its own demultiplexing, using the fixed magic-cookie value, the two top bits of the message-type field, and optionally the FINGERPRINT attribute, none of which this document itself performs. Long-term credential authentication requires a server-side password database (or equivalent per-user secret) shared out of band between client and server, following the recommendations in RFC 7616 for the digest mechanism this document adapts.

### Contradicts
None found.

### References worth retrieving
- Rosenberg, Weinberger, Huitema, Mahy, "STUN - Simple Traversal of User Datagram Protocol (UDP) Through Network Address Translators (NATs)," RFC 3489, 2003 — superseded-by (this document, via RFC 5389, obsoletes it); already in this batch as ROSENBERG-RFC-03.
- Rosenberg, Mahy, Matthews, Wing, "Session Traversal Utilities for NAT (STUN)," RFC 5389, 2008 — superseded-by (this document obsoletes it directly); introduced XOR-MAPPED-ADDRESS and the current STUN message format this document extends.
- Mahy, Matthews, Rosenberg, "Traversal Using Relays around NAT (TURN)," RFC 5766, 2010 — foundational/companion, the relay mechanism STUN's binding discovery is combined with when direct traversal fails; superseded within this corpus by REDDY-RFC-20 (RFC 8656).
- Keranen, Holmberg, Rosenberg, "Interactive Connectivity Establishment (ICE): A Protocol for Network Address Translator (NAT) Traversal," RFC 8445 — foundational, the NAT-traversal procedure this document states actually verifies the reflexive address STUN discovers and defends against the outside-attack class this document describes but does not itself solve.
- Paxson, Allman, Chu, Sargent, "Computing TCP's Retransmission Timer," RFC 6298 — foundational, source of the RTO computation this document's UDP retransmission timing is aligned to.
- Turner, Chen, "Updated Security Considerations for the MD5 Message-Digest and the HMAC-MD5 Algorithms," RFC 6151 — foundational, cited in the security discussion of hash algorithm weakness underlying the bid-down attack analysis.

### Verbatim extracts
- "STUN is not a NAT traversal solution by itself"
- "the source transport address of the request received by the server will be" the reflexive address
- "some NATs rewrite the 32-bit binary payloads containing the NAT's public IP address"
- "a client SHOULD limit itself to ten outstanding transactions to the same server"
- "Rc SHOULD be configurable and SHOULD have a default of 7"
- "protecting against this attack by using a message-integrity check is impossible"
- "ingress source address filtering" mitigates the reflector attack
