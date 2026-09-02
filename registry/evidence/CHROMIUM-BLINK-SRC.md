## [CHROMIUM-BLINK-SRC] rtc_peer_connection.cc: kMaxPeerConnections limit enforced by RTCPeerConnection construction
**Citation:** Chromium project (Blink renderer, third_party/blink/renderer/modules/peerconnection). "rtc_peer_connection.cc." Chromium source repository, main branch, 2026.
**Retrieved:** full text via git.googlesource.com blob view
**Source URL:** https://chromium.googlesource.com/chromium/src/+/main/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc
**Domain:** L

### What it does
The function stops a browser tab from creating an unbounded number of WebRTC peer connections, so a page cannot exhaust the process by opening `RTCPeerConnection` objects without limit. The mechanism is a static counter and a compile-time constant. Blink defines a file-scope constant `kMaxPeerConnections` set to 500. `InstanceCounters` holds a running count of live `RTCPeerConnection` objects (`kRTCPeerConnectionCounter`), incremented by `InstanceCounters::IncrementCounter` at the start of `RTCPeerConnection` construction and decremented by `InstanceCounters::DecrementCounter` in the destructor. After incrementing, the constructor reads the counter with `InstanceCounters::CounterValue` and compares it against `kMaxPeerConnections`; when the value exceeds the constant, the constructor calls `exception_state.ThrowDOMException(DOMExceptionCode::kUnknownError, "Cannot create so many PeerConnections")` and returns, leaving the object unusable. `RTCPeerConnection::PeerConnectionCount()` and `RTCPeerConnection::PeerConnectionCountLimit()` expose the current count and the constant to other Blink code and to instrumentation.

### Measured results
None. This is a source-code artifact, not a paper reporting an experiment; it states a compile-time constant and the check that enforces it, not a measured outcome.

### Parameters
| Parameter | Value | Source |
|---|---|---|
| `kMaxPeerConnections` | 500, per browsing context (renderer process instance counter) | `const int64_t kMaxPeerConnections = 500;` |
| Counter checked | `InstanceCounters::kRTCPeerConnectionCounter`, incremented on construction, decremented on destruction | code read above |
| Failure mode on exceeding the limit | throws `DOMException` with `DOMExceptionCode::kUnknownError` and message "Cannot create so many PeerConnections"; the constructor returns early, the object is left closed | code read above |

### Stated limitations
None stated; the file is source code, not a paper, and carries no discussion or future-work section. No comment in the surrounding code explains why 500 was chosen; treat that number as an enforced ceiling with no documented derivation, not as evidence of a bandwidth or CPU justification.

### Requirements it places on the rest of the system
A browser-tab network participant that opens one `RTCPeerConnection` per remote peer is capped at 500 simultaneous peer connections in that tab, regardless of the application's own connection-management policy. Any overlay or mesh design that maps peers to `RTCPeerConnection` objects one-to-one must keep the per-tab active-peer count under 500 or handle the thrown exception when a new connection attempt exceeds it. The count is per browsing context in the Blink renderer process; the code read here does not state whether multiple tabs from the same origin, or Web Workers, share the counter or hold separate counters, so that boundary is unverified from this file alone.

### Contradicts
None found.

### References worth retrieving
None — a source file has no bibliography.

### Verbatim extracts
"The maximum number of PeerConnections that can exist simultaneously."
"const int64_t kMaxPeerConnections = 500;"
"Cannot create so many PeerConnections"
