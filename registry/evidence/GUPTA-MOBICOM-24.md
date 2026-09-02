## [GUPTA-MOBICOM-24] 3 W's of smartphone power consumption: Who, Where and How much is draining my battery?
**Citation:** Agrim Gupta, Adel Heidari, Avyakta Kalipattapu, Ish Kumar Jain, Dinesh Bharadia. "3 W's of smartphone power consumption: Who, Where and How much is draining my battery?" ACM MobiCom, 2024. DOI 10.1145/3636534.3695905.
**Retrieved:** full text via https://wcsng.ucsd.edu/ue-power/
**Source URL:** https://dl.acm.org/doi/10.1145/3636534.3695905
**Domain:** L

### What it does
This paper attributes a phone's battery discharge to individual hardware subsystems (cellular modem, Wi-Fi radio, display, compute, camera, memory) rather than to whole applications, using a per-rail power measurement path that does not depend on subtracting one whole-device power reading from another. On Google Pixel phones the paper reads Google's On-Device Power Rails Monitor (ODPM), a hardware facility that reports power draw separately per subsystem rail, captured over a background system trace using the open-source Perfetto tool while a person uses the phone normally. Because ODPM exists only on Pixel 6 and later, the paper also validates a second, portable measurement path for phones without ODPM: net battery discharge is read from the phone's standard battery counter, and a baseline power reading is taken in a state where the target subsystem is off (airplane mode for the modem, screen off for the display), so that subtracting the baseline from an active-use reading isolates that subsystem's power. This baseline-subtraction path was used before this paper (cited to Xu et al., 2020) without validation against a direct measurement; this paper is the first to check it against ODPM as ground truth on the same device.

### Measured results
Every number below is read from bar-chart figures in the paper; the source figures give axis ranges and legend categories in text, not per-bar numeric labels, so no exact milliwatt value can be extracted for an individual bar. Reported figures are axis-scale ranges and the qualitative orderings the paper states in prose.

| Result | Condition | Figure |
|---|---|---|
| Cellular and display are the two largest power-consuming components, exceeding compute, memory, camera, and Wi-Fi, for every activity tested | Google Pixel 7A, ODPM measurement, five 1-minute sessions: standby, Instagram, YouTube (720p), Clash-of-Clans, Google Meet video call; axis range 0-4000 mW | Fig. 2 |
| Baseline-subtraction (battery counter) modem-power estimates agree with ODPM ground truth for standby and downlink transfer, but do not agree for uplink transfer | Google Pixel 7A, iPerf-generated traffic at 1, 5, and 10 Mbps in each of uplink and downlink, over a 5G base-station setup; axis range 250-2000 mW | Fig. 3 |
| 5G standby power consumption is about two times 4G standby power consumption | Google Pixel 7A and Samsung Galaxy S23+, both on the same commercial SIM, same wireless band, same physical location relative to the base station; battery-discharge method; axis range 0-800 mW | Fig. 4 |
| Samsung S23+ (Qualcomm X70 modem) draws less standby power than Google Pixel 7A (Samsung Exynos 5300 modem); S23+ display power exceeds Pixel 7A display power | Same standby-mode setup as above | Fig. 4 |
| S23+ (Wi-Fi and cellular chipsets) draws less connectivity power than Pixel 7A during 720p YouTube streaming, across Wi-Fi, 4G, and 5G | Both phones, 720p YouTube streaming, same nominal display brightness; axis range 0-1400 mW | Fig. 5 |
| Wi-Fi power draw is lower than cellular power draw for transferring the same amount of data | Stated in prose (Section 2.3 discussion), consistent with Fig. 5 | Fig. 5, Section 3(c) |

The paper states the uplink disagreement between the two modem-power measurement methods may result from power-amplifier current draws during uplink transmission that are large and brief enough not to be captured by a total-battery-discharge reading.

### Parameters
- ODPM trace duration: 1 minute per application/use case (standby, Instagram, YouTube, Clash-of-Clans, Google Meet).
- iPerf traffic rates tested for modem-power validation: 1 Mbps, 5 Mbps, 10 Mbps, in both uplink and downlink, over a 5G connection.
- Video streaming resolution used throughout: 720p.
- Devices: Google Pixel 7A (Samsung Exynos 5300 modem, OLED display) and Samsung Galaxy S23+ (Qualcomm X70 modem, AMOLED display).
- Cross-device comparison controls held constant: identical commercial SIM card, identical wireless band, identical physical location (same base-station link quality), identical nominal display brightness.

### Stated limitations
ODPM power rails are available only on Google Pixel phones from generation 6 onward, so the paper's direct per-rail measurement cannot be applied to other manufacturers' devices without the battery-discharge substitute method. The battery-discharge substitute method for modem power is stated to work well for downlink and standby power but not for uplink power. The paper states no measurement or model of compute energy for on-device AI inference workloads exists in this study, and identifies this as future work needed before communication-versus-computation energy tradeoffs for edge inference can be evaluated. The paper offers no measurement of energy under mobility (moving between cell towers, handoff, or varying signal strength) — every reported measurement holds the physical location fixed.

### Requirements it places on the rest of the system
A design that wants to cite this paper's cellular-versus-Wi-Fi or standby power figures for a continuous-participation cost estimate must use the axis-range figures above, not a fabricated per-bar milliwatt number, because the source figures in the retrieved text do not carry numeric data labels. Any claim about 5G standby cost relative to 4G is conditioned on both radios connecting to the same base station in the same location; the paper does not report results across varying signal strength or handoff. A protocol design that assumes uplink transmission energy can be estimated from total battery discharge, on a phone without a direct per-rail power measurement facility (ODPM or equivalent), inherits the same inaccuracy the paper reports for uplink and should not treat that estimate as reliable in the way its downlink estimate is.

### Contradicts
None found.

### References worth retrieving
- Dongzhu Xu, Anfu Zhou, Xinyu Zhang, Guixian Wang, Xi Liu, Congkai An, Yiming Shi, Liang Liu, Huadong Ma, "Understanding operational 5G: A first measurement study on its coverage, performance and energy consumption," ACM SIGCOMM (applications, technologies, architectures workshop), 2020 — foundational (source of the baseline-suppression modem-power estimation method this paper validates against ODPM).
- Matteo Varvello, Kleomenis Katevas, Mihai Plesa, Hamed Haddadi, Benjamin Livshits, "Batterylab, a distributed power monitoring platform for mobile devices," ACM HotNets, 2019 — competing (a distributed power-monitoring platform for mobile devices, an alternative measurement approach).
- David Patterson, Jeffrey M. Gilbert, Marco Gruteser, Efren Robles, Krishna Sekar, Yong Wei, Tenghui Zhu, "Energy and emissions of machine learning on smartphones vs. the cloud," Communications of the ACM 67(2), 2024 — competing (assumes Wi-Fi communication to cloud for on-device vs. cloud inference energy comparison, cited in this paper's future-work discussion as needing a more careful cellular-power treatment).
- Jennifer Switzer, Gabriel Marcano, Ryan Kastner, Pat Pannuto, "Junkyard computing: Repurposing discarded smartphones to minimize carbon," ASPLOS, 2023 — foundational (cited for smartphone e-waste and embodied-carbon context motivating the study).

### Verbatim extracts
- "connectivity (Wi-Fi, 4G/5G) and screen display are the primary power consumers" (Abstract).
- "we observe that cellular and display stand out as the two largest power consuming components" (Section 2.1).
- "The two methods agree well for downlink... The two methods don't agree on uplink" (Fig. 3 caption text).
- "5G does consume a higher (about two times) standby power consumption than 4G" (Section 2.3).
- "Wi-Fi still consumes lesser power than cellular networks while they transfer same amount of data" (Section 3(c)).
