## [SINGH-ARXIV-26] Lightweight Call Signaling and Peer-to-Peer Control of WebRTC Video Conferencing

**Citation:** Kundan Singh. "Lightweight Call Signaling and Peer-to-Peer Control of WebRTC Video Conferencing." arXiv preprint (CoRR), 2026. DOI 10.48550/ARXIV.2602.08975.
**Retrieved:** full text via https://arxiv.org/pdf/2602.08975
**Source URL:** https://arxiv.org/abs/2602.08975
**Domain:** L

### What it does
The system, named Ezcall, runs a multiparty WebRTC (Web Real-Time Communication) video conference with no media server in the data path for either signaling or data storage. Call signaling — the initial exchange needed to open a WebRTC data channel between two browser endpoints — piggybacks on Google Firebase Cloud Messaging (FCM) push notifications routed through a lightweight notification server (under 300 lines of PHP), or, to remove that server dependency entirely, on manually copy-pasted email or instant-message bodies. Once the first data channel is open between two endpoints, every later signaling step (session description protocol offer-answer, ICE candidate exchange for additional media, control messages) travels over that data channel instead of the push/email channel. As more participants are invited, the endpoints form an unstructured peer-to-peer network among the browser tabs themselves: the network topology mirrors the invitation graph (who invited whom), not a designed overlay. Two independent overlays exist per call: a control-path network of WebRTC data channels carrying conference state (roster, text chat, call state) via a component named PeerStorageImpl, and a media-path network carrying audio/video, defaulting to full mesh (every pair of participants exchanges its own encoder/decoder streams directly) but able to reconfigure into a browser-hosted multipoint control unit (MCU, an endpoint that decodes and mixes every other participant's stream into one outbound stream) or selective forwarding unit (SFU, an endpoint that forwards received streams to other participants without decoding) chosen by an unspecified distributed decision process based on endpoint CPU/network capacity.

### Measured results
No experiment with stated node counts, message counts, bandwidth, or latency figures is reported. The paper reports only implementation scale and a local functional test, not a network-scale measurement.

| Observation | Conditions |
|---|---|
| A local test application forms a peer-to-peer network of connection paths and exercises data synchronization and media paths among the emulated participants | Up to 30 emulated participants running as independent web apps on a single machine, each using real WebRTC connection, data-channel, and media-stream APIs |
| A six-user text-chat conference partitions when one link between two participants is broken, and resynchronizes (with duplicate messages suppressed by message identifier) when the link is restored | Demonstrated in the same local test application; no participant count beyond six stated for this specific demonstration, no timing figures given |
| Total new implementation size | Under 3,000 lines of JavaScript for the endpoint components plus under 300 lines of PHP for the optional notification server |

### Parameters
- Push-notification expiry: 1 minute (the FCM push used for call signaling is discarded by the notification server after this interval, since it is only used for real-time signaling)
- Serverless (email) signaling message validity: 2 minutes (an invite or accept message received after this interval is not used by the app)
- Flooding time-to-live (TTL) for data-synchronization messages: described as "a small number" by default; no numeric value is stated
- Router/NAT inactive-port timeout bounding serverless SDP offer/answer validity: 30 seconds to 5 minutes, described by the authors as typical router behavior, not as a value they measured themselves

### Stated limitations
The system does not support merging two separate calls that use different conference identifiers, even when the same users are on both. Only the full-mesh media-path topology is implemented in the media-chat component; MCU and SFU operation are described conceptually but not built into the endpoint. After a network partition and merge, the flooding synchronization deduplicates messages by random message identifier but does not preserve a consistent message order across participants; the authors state that message timestamps could add ordering in future work. The shared-storage component that PeerStorageImpl reuses has little or no access control: any participant can alter a data object another participant created. A participant's display name can be impersonated when a third-party conference app is used or when serverless (email) signaling is used, because no mechanism ties the display name to the signaling identity. The auth token used for initial user lookup is a bearer secret equivalent in risk to a leaked password; the authors describe, but do not implement, a client-certificate binding that would remove this risk. Exposing a user's FCM push token through a public directory or a peer-to-peer network (an alternative to the built-in notification server that the authors discuss but do not build) lets any holder send an arbitrary push notification, including one carrying a malicious link, to that user's devices. A proposed drag-and-drop workaround for passing the serverless signaling message between the app and an email or messaging client, using an image or QR code as the carrier, is untested by the authors. The authors describe the software as "still in its early stage."

### Requirements it places on the rest of the system
The first signaling round-trip needs an asynchronous, out-of-band channel the browser tab did not open itself, because a browser tab cannot accept an unsolicited inbound connection; the implementation supplies this with Firebase Cloud Messaging push or with a human relaying an email/instant-message body, and states that a minimum of two messages (one per direction) is required for the offer-answer exchange even without ICE trickling. The flooding-based control-path synchronization assumes every relaying node cooperates: each node forwards every received change to every data-channel neighbor bounded only by a hop-count TTL, with no signature or integrity check performed by default (the paper only proposes, without implementing, that a message resource could be signed by the sender's private key). Point-to-point message delivery (used for session negotiation and private text) depends on a per-node routing table that each node builds and synchronizes only with its immediate data-channel neighbors, so a node's ability to reach a distant peer depends on every intermediate node in the invitation-graph topology continuing to relay and to keep its table current. Cycle avoidance in the control-path topology depends on every node holding a full local copy of the shared conference topology (through the shared-storage component), which the paper states each node has, so a scheme built on partial or eventually-consistent topology knowledge would not get the same duplicate-link suppression. Building a structured peer-to-peer network or a distributed hash table for call-signaling lookup (an alternative the paper raises but does not build) would need an external socket gateway, browser plugin, or existing peer-to-peer network, because the paper states that web apps cannot open listening sockets in JavaScript.

### Contradicts
None found. No other paper in this corpus reports a measurement of this specific serverless-WebRTC-conferencing mechanism.

### References worth retrieving
- Husøy, T.K. "Topology in WebRTC services." Master's thesis, Department of Telematics, Norwegian University of Science and Technology, 2015. — foundational (media-path topology comparison this paper cites for MCU/SFU/full-mesh tradeoffs)
- Sandholm, T. "SnoW: Serverless n-Party calls over WebRTC." arXiv:2206.12762, 2022. — competing (another serverless multiparty WebRTC system)
- Singh, K., Schulzrinne, H. "Peer-to-peer Internet Telephony using SIP." NOSSDAV, 2005. — foundational (prior peer-to-peer call-signaling network by the same author)
- Singh, K., Schulzrinne, H. "SIPpeer: a SIP-based P2P Internet telephony client adaptor." Columbia University report, 2004. — foundational
- Jones, P., et al. "WebFinger." IETF RFC 7033, 2013. — foundational (proposed mechanism for publishing reachability/contact tokens)
- Rosenberg, J., et al. "SIP: Session Initiation Protocol." IETF RFC 3261, 2002. — foundational (baseline call-signaling protocol contrasted with this system's approach)

### Verbatim extracts
"It does not use a media server."
"We use flooding for data synchronization in the peer-to-peer network."
"can emulate up to 30 nodes for testing on a local machine"
"no new link is created in the network"
"it currently has little or no access control"
"We have not tested if this actually works."
"web apps cannot create listening sockets in JavaScript"
