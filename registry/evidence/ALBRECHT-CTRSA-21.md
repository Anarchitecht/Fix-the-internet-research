## [ALBRECHT-CTRSA-21] Mesh Messaging in Large-Scale Protests: Breaking Bridgefy
**Citation:** Martin R. Albrecht, Jorge Blasco, Rikke Bjerg Jensen, Lenka Mareková. "Mesh Messaging in Large-scale Protests: Breaking Bridgefy." Cryptographers' Track at RSA Conference (CT-RSA), 2021. DOI 10.1007/978-3-030-75539-3_16.
**Retrieved:** full text via https://eprint.iacr.org/2021/214.pdf
**Source URL:** https://eprint.iacr.org/2021/214.pdf
**Domain:** H

### What it does
This paper is a security analysis, not a mechanism proposal: it reverse-engineers and attacks Bridgefy, a deployed Bluetooth-mesh messaging application (Android apk version 2.1.28, dated January 2020, with Bridgefy SDK version 1.0.6) that was promoted for and used during large-scale protests (Hong Kong, India, Iran, United States, Zimbabwe, Belarus). Bridgefy routes one-to-one messages over the internet when both parties are online, directly over Bluetooth Low Energy (BLE) when parties are in physical range, or over a Bluetooth mesh network of forwarding peers otherwise; it also supports plaintext broadcast messages readable by anyone in a "Broadcast mode" room. The authors decompiled the apk with Jadx and instrumented the running application with Frida, a dynamic-instrumentation toolkit that injects scripts into a running process to trace and modify method calls, to recover the wire protocol and demonstrate attacks against it in practice, on real Android devices.

Tracking mechanism exploited: every Bridgefy client continuously transmits, in its BLE advertising packets, the CRC32 checksum of its own user ID, encoded as 10 decimal-digit bytes; this identifier does not change unless the application is reinstalled, so passive observation of BLE advertisements alone tracks a given device indefinitely.

Impersonation mechanism exploited: the handshake protocol that establishes user identity and exchanges public keys is stateless and unauthenticated. An attacker who has observed a target's user ID (learnable by passively monitoring the network) sends a forged handshake response asserting that user ID and its own public key; the receiving client overwrites its stored association for that user ID with the attacker's key, causing subsequent messages from the attacker to display as if from the impersonated user.

Man-in-the-middle (MITM) mechanism exploited: an extension of the impersonation attack in which the attacker forces a client to request an "updated" public key for a target user (by presenting a public-key CRC that does not match the client's cached value) and then supplies its own key, which the client then associates with the target's user ID; all further messages the victim sends to that user ID are encrypted under the attacker's key.

Confidentiality break exploited: Bridgefy's one-to-one message encryption is RSA under the PKCS#1 v1.5 padding standard, applied to MessagePack-serialized, Gzip-compressed payloads, with no message authentication. Because there is no authentication, an attacker can construct arbitrary valid-looking ciphertexts and use Bridgefy's own protocol-level delivery-receipt behavior (a receipt is sent only if decryption, decompression, and parsing all succeed; no receipt and no error signal is sent otherwise) as a Bleichenbacher-style padding oracle: whether a chosen ciphertext produces a delivery receipt reveals whether it satisfies PKCS#1 v1.5 padding. The authors' variant abuses the Gzip file format's optional FLG.FCOMMENT field, whose comment bytes are excluded from the payload's CRC32 checksum, to smuggle a chosen-ciphertext block between two honestly-generated ciphertext blocks that make the joint payload decompress and parse successfully whenever the smuggled padding-oracle probe happens not to contain a zero byte.

Denial-of-service (DoS) mechanism exploited: Bridgefy mesh clients forward a received message to other peers before attempting to parse or display it. Because message payloads are Gzip-compressed before transmission, a single small compressed "zip bomb" message (a highly compressible payload that expands enormously on decompression) that is sent to the broadcast room is forwarded by every receiving client before any of them attempt to decompress and display it, and each client then hangs while trying to process the oversized decompressed content, requiring reinstallation to recover.

### Measured results
- Local user tracking: passive observation of BLE advertisement packets suffices to track a device indefinitely, because the transmitted CRC32-of-user-ID identifier is static until reinstallation; this is a structural/protocol-level finding, not a numeric measurement of tracking range or duration.
- IND-CPA confidentiality break: the encryption scheme (RSA PKCS#1 v1.5 with 245-byte messages) offers only 2^64 security in a standard indistinguishability-under-chosen-plaintext-attack game — an adversary distinguishing between two chosen messages m0, m1 by trying all 255^8 possible padding-random-byte values for the challenge ciphertext.
- Impersonation and MITM attacks: verified in a physical setup of four Android devices; the attacker used two devices running Frida scripts to hotpatch and modify handshake messages, one impersonating each side of the conversation to instantiate a full attacker-in-the-middle.
- Bleichenbacher-style padding-oracle simulation: the authors adapted existing Bleichenbacher-simulation code and ran the attack 4,096 times on 80 CPU cores, about 12 hours total compute time, recording the number of oracle queries needed per run. Median: 2^16.75 oracle queries; mean: 2^17.36 oracle queries.
- The probability that a randomly chosen padding-oracle probe avoids a zero byte in its 245-byte comment field (required for the Gzip-comment smuggling trick to succeed) is (1 − 1/256)^245 ≈ 0.383, derived analytically and confirmed by observed receipt frequency matching this figure in live device tests.
- End-to-end oracle-query throughput measured in the authors' proof-of-concept (using Frida to hotpatch the live application, not an optimized implementation): one chosen ciphertext sent every 450ms, giving an estimated 50% probability of a complete attack finishing in under 14 hours; the authors state a purpose-built (non-hotpatched) implementation could likely achieve higher throughput, but do not measure one.
- Timing side-channel variant (an alternative 2-ciphertext-block padding oracle, sketched but not carried to a full end-to-end attack): execution time of the message-extraction method (`ChunkUtils.stitchChunksToEntity`), measured directly on-device with Frida/Java timers, for two classes of malformed input — bad-padding errors: N=1,360 samples, mean 33.88ms, standard deviation 3.14ms, standard error 0.085ms; Gzip-parse errors: N=1,508 samples, mean 42.56ms, standard deviation 4.27ms, standard error 0.110ms. The authors state they leave demonstrating this side-channel as a practical end-to-end attack to future work, noting that an attacker would likely need more precise packet-timing control than stock Android devices provide.
- Broad denial-of-service (zip bomb): a 10MB message consisting of a single repeated character compresses to a 10KB payload, small enough to transmit over the BLE mesh; the authors implemented and tested this attack on a number of Android devices (count not stated) and report the receiving application becomes unresponsive, requiring reinstallation.

### Parameters
- Target software version: Bridgefy apk 2.1.28 (dated January 2020, from Google Play), Bridgefy SDK 1.0.6.
- RSA key/message parameters for the IND-CPA attack: 245-byte messages, PKCS#1 v1.5 padding.
- Zip-bomb parameters: 10MB single-character input compresses to a 10KB transmitted payload.
- Bleichenbacher-simulation parameters: 4,096 independent simulated attack runs, 80 cores, about 12 hours total wall/CPU time (paper does not distinguish).
- Live padding-oracle throughput: one probe ciphertext sent per 450ms (a proof-of-concept figure from Frida hotpatching, not a claimed protocol limit).
- Application-imposed message-size limit relevant to the two-block timing-oracle variant: the shipped Bridgefy application caps message text at 256 bytes, which the paper states keeps ciphertexts to at most two blocks in normal use.

### Stated limitations
The authors state their analysis applies to the specific apk/SDK versions studied (2.1.28 / 1.0.6) and explicitly does not apply as-is to the versions Bridgefy released afterward in response to this work — in October 2020 the developers switched to the Signal protocol, and the authors state they have not reviewed that update and recommend an independent security audit of it rather than asserting it is secure or that their attacks still apply. The timing side-channel padding oracle is presented only as a sketch: the authors state they leave demonstrating it as a working end-to-end attack to future work, and note it would likely require finer packet-timing control than standard Android devices offer. The paper does not attempt to fix Bridgefy or propose a replacement protocol; it states that designing communication tools that meet the actual needs of protesters facing internet shutdowns is a topic for future work, citing separate prior interview-based research on high-risk user needs.

### Requirements it places on the rest of the system
- A mesh-messaging deployment that wants to prevent this class of attack needs, at minimum, an authenticated key-establishment/handshake mechanism (the handshake here is unauthenticated and stateless, which is what enables both the impersonation and MITM attacks) and message authentication on ciphertexts (there is none here, which is what enables the chosen-ciphertext padding-oracle attack).
- Any protocol-level delivery/read receipt (or any other signal that leaks whether decryption plus decompression plus parsing succeeded) must not be observable by, or distinguishable to, an entity that also controls or can inject ciphertexts, or it functions as a padding oracle; the receipt-based oracle here required no compromise of any node, only network presence and the ability to send messages.
- A store-and-forward mesh design in which nodes forward a message before parsing or displaying it needs the forwarding step to not depend on trusting message well-formedness, or a single adversarial message can propagate before it disables every downstream node that eventually tries to process it — the observed failure mode here is forward-then-parse ordering combined with unbounded decompression.
- Any identifier transmitted in link-layer advertisement or broadcast packets (here, a checksum of the user ID) must rotate or be otherwise unlinkable across sessions, or passive physical-layer observation alone provides persistent device tracking regardless of what protections exist at higher protocol layers.
- A server-mediated public-key directory (used here to resolve online one-to-one messaging) is a single point of trust: the paper states that compromising it would trivially enable an attacker-in-the-middle attack against any two users, including users who intend to communicate only offline, because the server can serve incorrect keys during registration.

### Contradicts
None found — no other entry in this batch addresses Bridgefy, BLE mesh messaging, or Bleichenbacher-style padding oracles.

### References worth retrieving
- foundational: Bleichenbacher, "Chosen Ciphertext Attacks Against Protocols Based on the RSA Encryption Standard PKCS #1" [12] — the original attack this paper's confidentiality break instantiates.
- foundational: Bardou, Focardi, Kawamoto, Simionato, Steel, Tsay, "Efficient Padding Oracle Attacks on Cryptographic Hardware," CRYPTO 2012 [7] — source of the "FFT" query-classification terminology and simulation methodology the authors adapt for their Bleichenbacher-variant query count.
- competing/attack: Ryan, "Bluetooth: With Low Energy Comes Low Security" [57] — shows BLE device addresses can be spoofed, cited as a further avenue for impersonation beyond what this paper exploits.
- competing: Bluetooth SIG, "Mesh Profile Specification 1.0.1" [59] — the standard BLE mesh alternative, discussed and contrasted (message size capped at 384 bytes, nodes advised against more than 100 messages per 10-second window, assumes benign participating nodes, so a malicious member can still impersonate and deny service).
- competing: HypeLabs Hype SDK [37],[38] — an alternative mesh-messaging SDK for similar use cases, no independent security evaluation found by the authors.
- competing: Briar [56] — described as secure messaging but not a mesh network (only single-hop point-to-point Bluetooth Classic sockets unless a user manually forwards).
- competing: Serval Mesh [30] — Wi-Fi-based mesh application for areas without infrastructure, not deployment-ready at scale per the authors.
- competing: Subnodes [66] — Raspberry-Pi-based local mesh access points using the BATMAN routing protocol, requires carrying dedicated hardware.
- foundational (cryptography/side channel): Kelsey, "Compression and Information Leakage of Plaintext" [44] — origin of compression side-channel attacks that this paper's Gzip-based oracle descends from; also CRIME [25] and BREACH [32] as the well-known instances in TLS/HTTP.
- attack: Alwen, Coretti, Dodis, Tselekounis, "Security Analysis and Improvements for the IETF MLS Standard for Group Messaging," ePrint 2019/1189 [5] — cited as related secure-messaging formal-analysis work (this is the same paper as ALWEN-CRYPTO-20 in this corpus).

### Verbatim extracts
- "permitted its users to be tracked, offered no authenticity, no effective confidentiality protections"
- "an adversary could produce social graphs about them, read their messages, impersonate anyone to anyone and shut down the entire network"
- "passive observation of the network is enough to enable tracking all users"
- "Bridgefy does not utilise cryptographic authentication mechanisms"
- "a passive adversary can decide whether a message m0 or m1... was encrypted"
- "we ran a Bleichenbacher-style attack 4,096 times (on 80 cores, taking about 12h in total)"
- "The median is 2^16.75, the mean 2^17.36"
- "a single adversarially generated message can take down the entire network"
- "we have not reviewed these changes and we recommend an independent security audit"
