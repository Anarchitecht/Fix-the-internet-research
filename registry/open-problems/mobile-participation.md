# Continuous participation from mobile devices

## Verdict: open

Apple and Google publish, in detail, which background mechanisms exist and what they permit; no
published paper measures a peer-to-peer (P2P) application accepting inbound requests, relaying for
another peer, or holding a Distributed Hash Table (DHT) routing-table slot while an iOS or Android
process sits in the state those mechanisms actually produce. Every "mobile P2P" measurement the
corpus holds or this search found either kept the app in the foreground (DTube), tested a mobile ad
hoc network rather than an OS-managed smartphone process (Kademlia-in-MANET), or is a project's own
engineering account (Berty) rather than a controlled measurement. The corpus's own note on this
domain — before this pass added anything — already stated this as a gap; the search below confirms
it and quantifies the platform mechanisms in place of the missing measurement.

## What iOS permits, read from the current vendor documentation

An iOS app that moves to the background is, by default, suspended shortly afterward: its process
stays resident in memory but executes no code and its open sockets close. Apple's current
documentation states the transition callback itself — `applicationDidEnterBackground` — "has five
seconds to perform any tasks and return," after which "the system puts your app into the suspended
state" (`developer.apple.com/documentation/uikit/extending-your-app-s-background-execution-time`,
fetched 2026-09-02). An app can ask for more time by calling `beginBackgroundTask`, but the
documentation no longer states a fixed number of seconds — it directs the developer to read the
system-supplied `backgroundTimeRemaining` property at run time instead, because the granted duration
is dynamic; third-party developer reports (not Apple's own documentation, so recorded here as
unverified) describe approximately 30 seconds when the extension is requested from an
already-backgrounded state and approximately 3 minutes when requested at the moment of
backgrounding.

Beyond that short extension, iOS supplies five mechanisms for code to run later, each with a
distinct trigger and a distinct scope of what it is for, catalogued in Apple's "Configuring
background execution modes" page (`developer.apple.com/documentation/xcode/configuring-background-
execution-modes`, fetched 2026-09-02):

- **Background fetch** and **`BGAppRefreshTaskRequest`** — the system wakes the app "at regular
  intervals" it chooses, for a task Apple's own reference describes only as "a short refresh task"
  (`developer.apple.com/tutorials/data/documentation/backgroundtasks/bgapprefreshtaskrequest.json`);
  no fixed interval or duration is published, and the system can skip a scheduled refresh entirely
  based on the device's charge state, network conditions, and the app's own history of how the user
  actually opens it.
- **`BGProcessingTaskRequest`** — a longer task, Apple's own description stating it "can take minutes
  to complete," typically scheduled by the system for a period when the device is plugged in and idle
  (the same source as above); this is a maintenance window, not a standing execution grant.
- **Remote notifications with `content-available`** ("silent push") — a push arrives over the Apple
  Push Notification service (APNs) and wakes the app briefly to fetch new content before it is
  displayed; Apple's own background-execution-modes catalog states this mode exists so "the app uses
  push notifications as a signal that new content is available to download," which makes every
  invocation of this mechanism conditional on APNs itself having delivered the triggering push — a
  channel with its own reliability limits, covered below.
- **PushKit VoIP pushes** — the one mechanism Apple documents as reliably launching a suspended app
  regardless of the background-fetch scheduling algorithm, but restricted by policy to actual
  incoming calls: since iOS 13, the app must report the call to `CallKit` "in the same run loop" as
  receiving the push, and Apple's own developer forum states that failing to do so repeatedly causes
  the system to stop delivering further VoIP pushes to that app
  (`developer.apple.com/forums/thread/124134`, `developer.apple.com/forums/thread/128370`). A
  non-call use of this channel is a policy violation, not merely a missed opportunity.
- **`URLSession` background transfer** — a download or upload configured with a background session
  identifier is handed to a separate system daemon (`nsurlsessiond`) that continues the transfer
  after the app suspends or is even terminated by the system for memory pressure, relaunching the app
  in the background to deliver the completed transfer to its delegate. This is the one mechanism that
  survives suspension for an operation already in flight; it does not let the app accept a new
  inbound request while suspended; it moves one bounded file, not a standing bidirectional channel.

None of these five mechanisms opens a listening socket. An inbound TCP or UDP listener an app held
before backgrounding is closed with the rest of its sockets at suspension, and no publicly documented
API reopens one without the app first being woken by one of the five triggers above. A suspended iOS
app cannot be dialed; it can only be told, through one of these channels, that something is waiting
for it once the channel itself succeeds in reaching it.

## What Android permits, read from the current vendor documentation

Android's restriction path is graduated rather than binary. Two independent mechanisms narrow what a
background process can do: Doze mode, triggered when the device is stationary, unplugged, and
screen-off for a system-determined interval, and App Standby Buckets, which classify every installed
app by recent-use pattern independently of Doze.

Doze suspends network access and ignores wake locks outside periodic maintenance windows; deferred
alarms scheduled through `setAndAllowWhileIdle` or `setExactAndAllowWhileIdle` are throttled to at
most once every 9 minutes per app while idle, and app standby's own network access for an app with no
other exemption is granted "approximately once per day" during prolonged inactivity
(`developer.android.com/training/monitoring-device-state/doze-standby`, fetched 2026-09-02).

The standby buckets carry their own numeric job-execution quotas, published on Android's power-
management reference page (`developer.android.com/topic/performance/power/power-details`, fetched
2026-09-02):

| Standby bucket | Regular job quota | Expedited job quota | Alarm rate |
|---|---|---|---|
| Active | up to 20 min per rolling 60 min | up to 30 min per rolling 24 h | unlimited |
| Working set | up to 10 min per rolling 4 h | up to 15 min per rolling 24 h | 10/hour |
| Frequent | up to 10 min per rolling 12 h | up to 10 min per rolling 24 h | 2/hour |
| Rare | up to 10 min per rolling 24 h | up to 10 min per rolling 24 h | 1/hour |
| Restricted | once per day, up to 10 min | up to 5 min per rolling 24 h | 1/day |

An app enters the Restricted bucket automatically after 8 days of no use on Android 13 and later (45
days on Android 12), independent of any Doze state
(`developer.android.com/topic/performance/appstandby`, fetched 2026-09-02). A **foreground service**
— a background component the user can see, through a persistent notification, and that the user can
therefore choose to end — is the one Android mechanism exempt from these quotas and from Doze's
network suspension, and it is how a small number of production messaging apps hold a standing
connection open on Android today; Android 12 and later restrict which app states are allowed to
start one, and Android 14 requires the service to declare which of a fixed set of use-case types
(`connectedDevice`, `dataSync`, and others) it is claiming, each with its own eligibility rule.

Firebase Cloud Messaging (FCM), the delivery channel most Android apps use to trigger a wake, offers
a **high-priority** message class that Google's own documentation states FCM "attempts to deliver
... immediately even if the device is in Doze mode," granting the woken app "very limited" network
access and a partial wake lock for the duration of the callback
(`firebase.google.com/docs/cloud-messaging/concept-options`, search-cache fetched 2026-09-02); the
same documentation states the system will silently downgrade an app's high-priority messages to
normal priority if the app does not consistently show the user a visible result from them, at which
point Doze deferral applies again.

## The wake channel is itself a capacity-bounded, best-effort relay

Both platforms implement their push-wake channel as a store-and-forward relay with a stated,
non-negotiable capacity, not as a queue that grows to match demand. Apple's current documentation
states APNs "stores only one notification per bundle ID" per device — a second notification arriving
before the device reconnects replaces, rather than queues behind, the first — for at most 30 days by
default, adjustable per notification via the `apns-expiration` header, delivered "as a best-effort
service" with no delivery guarantee and explicit permission to reorder, throttle, batch, or drop
notifications depending on "the power state of the device"
(`developer.apple.com/tutorials/data/documentation/usernotifications/sending-notification-requests-
to-apns.json`, fetched 2026-09-02). Google's FCM documentation states the equivalent bound in more
granular form: the server holds at most four distinct **collapsible** messages per device
simultaneously, one per declared collapse key, replacing the oldest under a given key when a new one
with the same key arrives; a separate pool of up to 100 **non-collapsible** messages queues per
device, and once that pool fills, FCM discards every queued message and replaces them all with one
"limit exceeded" signal that tells the app only that it must perform a full resynchronization against
its own server, not what it missed (`firebase.google.com/docs/cloud-messaging/customize-messages/
collapsible-message-types`, search-cache fetched 2026-09-02); the default and maximum time-to-live
for any FCM message is four weeks, after which an undelivered message is discarded outright.

Neither platform vendor's own infrastructure — built with a managed server fleet, unlimited storage
budget by any single application's standard, and no adversarial peer to defend against — chose to
build unbounded, guaranteed-delivery message storage for a device that might stay unreachable. Both
capped the queue at a small fixed size, and both fell back to "tell the client to resynchronize" once
that cap is exceeded rather than attempting to preserve every individual item.

## No published paper measures a P2P application under these conditions

Corpus search and external search converge on the same result: the corpus's Domain L (transport and
reachability) holds NAT-traversal and QUIC-migration measurements, and separately a smartphone
power-consumption paper and a push-notification-latency citation, but no entry measures a P2P
application's server-side behavior — accepting an inbound stream, forwarding for another peer,
answering a DHT lookup — while the requesting process sits in the suspended or Doze-restricted state
the sections above describe.

**DBLP** (`dblp.org/search/publ/api`) returns zero hits for `mobile background execution`,
`background app refresh`, `iOS background execution measurement`, `push notification wake latency`,
`smartphone DHT participation`, `decentralized messaging mobile survey`, and `smartphone always-on
connectivity`. It returns results only for the adjacent, and distinct, literature on mobile ad hoc
networks (MANET) — multi-hop wireless routing among moving devices, a different problem from an
OS-managed smartphone process reaching the ordinary Internet — including Kademlia-in-MANET
(`ICUFN 2018`) and hierarchical-DHT churn mitigation for mobile networks (`Comput. Commun. 2016`),
neither of which tests OS-level suspension because a MANET simulation or testbed does not run the
routing code inside a sandboxed app process subject to iOS or Android's background policy. The two
DBLP hits that do concern an OS-managed phone and P2P networking — "Battery life of mobile peers with
UMTS and WLAN in a Kademlia-based P2P overlay" (PIMRC 2009) and "Silent Battery Draining Attack
against Android Systems by Subverting Doze Mode" (GLOBECOM 2016) — were found but not retrieved in
full for this pass; both predate, respectively by seven and by two years, the App Standby Bucket
system in the table above (introduced in Android 9, 2018), so neither can be read as a measurement
of the current restriction regime even once retrieved.

**arXiv** full-text abstract search for `"background execution" AND "peer-to-peer"`, `"background app
refresh"`, and `"Doze mode"` each return zero results.

**A 2013 clinical-engineering measurement**, Rothman, Dexter, and Epstein, "Communication Latencies
of Apple Push Notification Messages Relevant for Delivery of Time-Critical Information to Anesthesia
Providers" (*Anesthesia & Analgesia* 117(2), 2013), sent one probe push per minute to fixed iOS
devices in high-signal-strength locations for four months and reports, in its published structured
abstract (full text paywalled, not retrieved — this figure is recorded as **abstract-only** under
this corpus's evidentiary rule, not as verified full-text evidence): mean latency under 4 seconds for
iPhone over cellular, under 1 second for iPad/iPod over WLAN, with a 95% upper confidence bound of 42%
of days containing at least one delivery exceeding 100 seconds on iPhone. This is the closest
retrievable figure to a measured reliability bound on the push-wake channel itself, and it still does
not measure a P2P application, does not test a device actually left backgrounded by a user under
Doze- or App-Standby-equivalent restriction (no such restriction existed on iOS in 2013), and predates
the current APNs single-slot coalescing behavior's documentation by over a decade.

**Berty**, a deployed libp2p-and-IPFS-based mobile messenger, is the one project account found that
directly engages this problem on a real mobile P2P stack, in an engineering blog post rather than a
peer-reviewed measurement: "computing resources (CPU, battery, network) are relatively limited on
mobile devices," and holding several hundred simultaneous peer connections has, in the team's own
words, "a huge impact on a smartphone" even a high-end one
(`berty.tech/blog/bluetooth-low-energy`, fetched 2026-09-02). This is a project's own qualitative
account, not a controlled measurement with stated conditions, and is recorded here only as evidence
that the gap is recognized by at least one production team, not as a quantified result.

**DTube on Android** (`DOAN-NETWORKING-20`, already in the corpus) measured a mobile P2P-adjacent
video app for ten months across four physical Android phones, but every measurement session ran the
app in the foreground for exactly the duration of one video's playout; the paper does not report the
app moving to the background during measurement and does not test IPFS retrieval, gateway
connectivity, or DHT participation continuing once the app is backgrounded.

**TRAUTWEIN-ARXIV-26** (DCUtR hole-punching on IPFS, already in the corpus), the largest field
measurement in the corpus's transport domain, ran its 212 volunteer clients as ordinary libp2p/IPFS
peers; the paper records client mobility only as a network-identity artifact ("one highly mobile
client from 28 distinct networks," consistent with a laptop changing Wi-Fi networks) and states
nothing about client operating system or app-lifecycle state, so it cannot be read either way on
whether any client ran as a backgrounded phone app.

**GUPTA-MOBICOM-24** (already in the corpus, Domain L) measures cellular- and Wi-Fi-radio power draw
on stock Android phones with per-rail hardware instrumentation, including a standby-power figure — the
closest corpus entry to a cost measurement for holding a device reachable. It measures power only, not
whether or for how long the process delivering or receiving that traffic is permitted to run; it does
not bear on the scheduling question this open problem concerns and is not a candidate solution.

## What a store-and-forward relay must supply as a consequence

The requirement follows from combining the platform mechanisms above with one mechanism already in
the corpus: libp2p's Circuit Relay v2 (`VYZOVITIS-SPECS-23`), the P2P relay protocol the field
already uses to make a NAT-behind peer reachable. Circuit v2's own specification states the private
peer's reservation "becomes invalid if [it] disconnects," and requires that peer to "keep its
connection to R alive and refresh the reservation before it expires." A backgrounded, suspended iOS
process — sockets closed, no code executing — cannot hold that connection open, and cannot refresh a
reservation it has no running code to refresh. The same failure applies to Keizer et al.'s relay-
incentive mechanism (`KEIZER-MOBIHOC-20`), whose Proof-of-Timely-Relay verification "requires the
client to have simultaneous, independent contact with two separate relay-capable nodes" for the
duration of every relay session, and whose smart-contract settlement "requires constant blockchain
monitoring by both parties" as a design assumption the paper states outright. Both mechanisms assume
what a suspended mobile process cannot supply: a live, continuously monitorable connection held by
the reachable-but-behind-NAT device itself.

A relay a mobile client depends on for reachability, therefore, cannot be one that treats the client's
own liveness as the thing keeping its address valid. It must hold state on the client's behalf across
the client's own process suspension, and it must resume normal peer-to-peer operation once the client
process wakes rather than requiring the client to re-establish standing infrastructure state (a
reservation, a synchronous verification session) from scratch. Concretely, three properties are
required of it, each following directly from a mechanism documented above:

1. **A finite, disclosed queue capacity with an explicit overflow signal, not silent unbounded
   growth.** Both platform vendors' own push infrastructure — APNs with one slot per app per device,
   FCM with four collapsible slots plus a 100-message non-collapsible pool — cap at a small fixed size
   and, once exceeded, discard the backlog and tell the client only to resynchronize. A relay serving
   a mobile client should adopt the same discipline explicitly (a stated, bounded queue depth and a
   defined resynchronization signal once it is exceeded) rather than attempting unbounded storage that
   either exhausts the relay's own resources or silently drops data with no signal to the client at
   all.

2. **A wake path that does not depend on the relay dialing the client directly.** Because no
   documented mechanism on either platform reopens a listening socket on a suspended process, a relay
   cannot itself wake the client; it can only hold data ready for a request the client's OS-level
   background-fetch or push-wake mechanism will eventually issue. This makes the relay's freshness
   guarantee only as good as the platform's own wake scheduling — opportunistic and vendor-scheduled on
   iOS background fetch, quota-limited by standby bucket on Android jobs, or dependent on a push
   provider (APNs or FCM) the relay does not control and whose own delivery is stated by both vendors
   as best-effort, not guaranteed.

3. **Reservation and verification state that survives the client's absence rather than expiring with
   it.** Where Circuit v2 invalidates a relay reservation on client disconnect and Keizer et al.'s
   incentive scheme requires the client's synchronous participation in every settlement round, a relay
   built for mobile participation needs the inverse property: a reservation, subscription, or
   verification credential that remains valid across an interval of client absence bounded by a stated
   policy (an expiry the client renews on its own schedule when next reachable, not one that lapses at
   the first suspension) — with the tradeoff, not evaluated by any measurement this search found, that
   a longer-lived credential is also a longer-lived target for replay or impersonation if the relay
   does not separately verify the client is still the legitimate holder each time it becomes reachable
   again.

No published measurement establishes what queue depth, wake latency, or credential lifetime these
three properties should actually use for a P2P relay under real mobile deployment; the figures in
this section are read from platform vendor specifications, which state what the platforms permit, not
from any experiment that ran a P2P relay against them.

## What was searched

Corpus: `registry/index-measurements.md` and `registry/index-requirements.md` grepped for `mobile`,
`background`, `push`, and `APNs`/`FCM`/`GCM`; every Domain L entry read from `registry/targets-
L.json`; evidence files opened in full for `GUPTA-MOBICOM-24`, `DOAN-NETWORKING-20`,
`TRAUTWEIN-ARXIV-26`, `KEIZER-MOBIHOC-20`, `VYZOVITIS-SPECS-23`, and `SINGH-ARXIV-26`; confirmed
`EPSTEIN-ANESTHANALG-13` was a listed target with no evidence file (unretrieved) before attempting
retrieval.

Retrieval attempt: `tools/fetch-paper.py` against the DOI and journal URL for
`EPSTEIN-ANESTHANALG-13` returned a 2,774-character paywall stub, below the corpus's 6,000-character
full-text threshold; the paper's structured medical-journal abstract (which reports its key figures
directly, unlike a typical computer-science abstract) is used above and labeled abstract-only rather
than treated as full-text evidence.

External: DBLP publication-search API for `mobile background execution`, `background app refresh`,
`iOS background execution measurement`, `Android Doze`, `push notification wake latency`, `P2P mobile
battery`, `Briar mobile messaging`, `background transfer service`, `Kademlia mobile`, `mobile DHT
churn`, `smartphone DHT participation`, `P2P messaging smartphone measurement`, `decentralized
messaging mobile survey`, `peer discovery mobile network`, `gossip protocol mobile devices`, and
`mobile ad hoc P2P energy`. arXiv full-text search for `"background execution" AND "peer-to-peer"`,
`"background app refresh"`, and `"Doze mode"` (each zero results). Semantic Scholar's search API was
rate-limited (HTTP 429) throughout this pass and returned no results. General web search for Apple
and Google's own current developer documentation (fetched directly from `developer.apple.com` and
`developer.android.com`, with Apple's JSON documentation API used where the rendered HTML page is a
client-side application shell with no server-rendered text), for academic measurement of push
notification reliability in 2023-2026 (industry benchmarking reports and user-experience diary studies
found; no controlled reliability measurement more recent than the 2013 clinical study above), and for
mobile-deployed decentralized messengers with a published measurement of background behavior (Berty,
Scuttlebutt/Manyverse, Session/Oxen, Signal — engineering documentation and blog posts found for
Berty and Scuttlebutt; no peer-reviewed measurement of background-execution behavior for any of the
four). The most recent directly relevant publication found and retrieved is `TRAUTWEIN-ARXIV-26`
(2026), which does not itself address mobile OS background state; the most recent publication found
whose own subject is mobile background execution is Rothman, Dexter, and Epstein (2013),
abstract-only.
