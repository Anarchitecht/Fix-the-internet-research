## [ENGELBART-ANRW-26] QUIC as Multiplexing Layer in WebRTC
**Citation:** Mathis Engelbart, Fabian Willi Fromwald, Jörg Ott. "QUIC as Multiplexing Layer in WebRTC." Applied Networking Research Workshop (ANRW), 2026. DOI 10.1145/3822163.3827919.
**Retrieved:** full text via conference slide deck (talk slides, presented July 19, 2026)
**Source URL:** https://doi.org/10.1145/3822163.3827919
**Domain:** L

### Note on source form
The retrieved text is an OCR transcript of the presentation slide deck, not the paper's typeset body text — each slide's bullet text repeats across consecutive extracted "pages" as the deck was captured frame-by-frame. Two of the deck's graphs (a bandwidth/latency time series on slide 3, and a four-panel delay/rate comparison on slide 10 spanning 5 Mbit/s at 10, 25, and 50 ms one-way delay) present numeric results only as plotted curves; the OCR text carries axis labels and scenario parameters but not the plotted data values themselves, so no specific latency or throughput number from those two figures can be recorded under Rule 1 of this extraction. Everything below is restricted to what the slide text states outright.

### What it does
The paper proposes replacing WebRTC's two separate transport stacks — (S)RTP (Secure Real-time Transport Protocol, for media) over UDP with SRTP's own congestion control, and SCTP (Stream Control Transmission Protocol, for data channels) over UDP with SCTP's own congestion control — with a single QUIC connection that carries both. RTP packets are carried using RoQ (RTP over QUIC, IETF draft-ietf-avtcore-rtp-over-quic), which encapsulates an RTP packet inside a QUIC datagram frame behind a flow identifier used to multiplex multiple RTP flows on one QUIC connection. Data-channel traffic is carried by a new protocol the authors propose, "Data Channels over QUIC" (draft-engelbart-quic-data-channels), and a further draft (draft-engelbart-multiplex-roq-qdc) defines how RTP and Data Channel traffic multiplex onto one QUIC connection, using flow identifiers or QUIC stream types to distinguish them. Because both traffic classes now share one QUIC connection, they share one congestion controller and one bandwidth estimate instead of running two independent ones that the deck states must otherwise be coordinated through "Coupled Congestion Control." The deck states congestion control can be implemented at the QUIC layer using an existing real-time algorithm (GCC, SCReAM, or NADA), and that using such a controller for real-time media over QUIC requires a QUIC packet-receive-timestamp extension (draft-ietf-quic-receive-ts) so the sender can compute one-way delay the way RTCP feedback does today. Scheduling policy is stated as: media encoders are configured to produce data at their allocated rate and are prioritized on the QUIC connection so they are delivered at low latency without consuming the full available bandwidth, while data-channel traffic (not necessarily rate-based, e.g. a file transfer) dynamically yields bandwidth to media when media is under its target rate and consumes the remainder when media is at or under target.

### Measured results
The authors built two implementations for comparison: a baseline WebRTC application (Pion WebRTC for the peer connection, Gstreamer for media) streaming video while sending data over a data channel, and an alternative using the same bandwidth-estimation algorithm implementation over a QUIC transport (quic-go). Both were evaluated across a matrix of bandwidth and delay scenarios using Linux network namespaces and `tc-netem` for traffic shaping, including a stated point of 5 Mbit/s at 10 ms, 25 ms, and 50 ms one-way delay. No numeric latency, throughput, or fairness value from these runs is stated as text in the retrieved slides — the results appear only as time-series and delay/rate plots, so none is usable as a recorded figure under Rule 1. The deck's stated qualitative conclusions, attributed to the authors and not independently verified here, are: RTP and Data Channels can be multiplexed over one QUIC connection; a real-time congestion controller such as GCC can be integrated into QUIC using the receive-timestamp extension; and multiplexing can resolve the bandwidth-unfairness problem that arises when RTP and Data Channel traffic run independent congestion controllers over separate UDP flows.

### Parameters
| Parameter | Value | Source |
|---|---|---|
| Test bandwidth points (deck slide 10) | 5 Mbit/s, at 10 ms / 25 ms / 50 ms one-way delay | scenario labels on the delay/rate comparison figure |
| Congestion-control algorithms named as QUIC-layer options | GCC, SCReAM, NADA | slide 6 |
| Implementation components | Pion WebRTC, Gstreamer, quic-go; Linux network namespaces + `tc-netem` for bandwidth/delay shaping | slide 8 |

No numeric parameter values (target bitrate, buffer size, pacing rate) beyond the bandwidth/delay test points above are stated in the retrieved text.

### Stated limitations
The retrieved slide text carries no discussion, limitations, or future-work section distinct from the three-line conclusion; a slide deck of this form typically omits the caveats a full paper states in prose, so any limitation not listed among the three conclusion bullets above is unverified from this source and would need the accompanying ANRW 2026 paper text, not just the talk slides, to check.

### Requirements it places on the rest of the system
A WebRTC peer wishing to use this multiplexing scheme needs both peers' QUIC stacks to support the packet-receive-timestamp extension (draft-ietf-quic-receive-ts) before a real-time congestion controller such as GCC can run at the QUIC layer, because that extension is what lets the sender compute one-way delay the way RTCP receiver reports do in today's separate-stack WebRTC. The scheme also needs an agreed multiplexing protocol on both peers (draft-engelbart-multiplex-roq-qdc, itself an unpublished Internet-Draft the paper states as still in progress) before RTP and Data Channel flows can share one QUIC connection; a peer implementing only RoQ or only Data Channels over QUIC, without the multiplexing draft, cannot use this scheme. Because media and data now share one congestion-controlled connection, the scheduling policy described (prioritize media, let data channels yield or consume the remainder) must be implemented by whatever component multiplexes the two traffic classes onto QUIC streams or datagrams — an implementation that does not prioritize media traffic on the shared connection loses the low-latency delivery property the paper states this design is meant to provide.

### Contradicts
None found.

### References worth retrieving
- **Foundational** — IETF draft-ietf-avtcore-rtp-over-quic (RoQ). — the RTP-in-QUIC encapsulation this design is built on.
- **Foundational** — IETF draft-ietf-quic-receive-ts. — the packet-receive-timestamp extension the design states is required for real-time congestion control over QUIC.
- **Competing** — the coupled-congestion-control approach to the same RTP/Data-Channel unfairness problem, referred to on slide 3 as the alternative the field has otherwise pursued instead of QUIC multiplexing; the specific citation for this alternative is not given in the retrieved slide text and needs the full paper to identify.
- **Foundational** — Google Congestion Control (GCC), SCReAM, NADA — the three named real-time congestion-control algorithms the deck states can run at the QUIC layer; none is cited with a specific reference in the retrieved slide text.

### Verbatim extracts
"Multiplex RTP and Data Channels over QUIC"
"congestion control for real-time media requires packet receive timestamp extension for QUIC"
"Data Channels dynamically yield or consume bandwidth when media over- or undershoots target"
"RTP and Data Channels can be multiplexed over QUIC"
"Multiplexing can solve unfairness issue between RTP and Data Channels"
