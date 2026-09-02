# Audit: forgery-resistance.md, reputation.md, incentives.md

## Method

Extracted every cited factual claim carrying a number, measured result, or stated property from
the three assigned selection files and traced each against the entry it cites. Checked 27 distinct
citation instances directly against evidence-entry text: GAO-CNS-18, VISWANATH-SIGCOMM-10,
ALVISI-SP-13, CRITES-CCS-25, PERCIVAL-BSDCAN-09, KAMVAR-WWW-03, GYONGYI-VLDB-04,
TAHERIBOSHROOYEH-ARXIV-22, SHACHAM-ASIACRYPT-08, VORICK-SIA-14, ADAR-FM-00, PIATEK-NSDI-07,
LEVIN-SIGCOMM-08, MISLOVE-NSDI-08, POST-NSDI-11, TRAN-NSDI-09, VISHNUMURTHY-P2PECON-03,
SIRIVIANOS-USENIXATC-07, LEVIEN-USS-98. Also scanned all three files for factual claims with no
citation key attached.

26 of 27 checked claims restate the cited entry's figures and conditions correctly, including
several with many chained numbers (Gao's 0.0042/0.3/0.0046 modularity chain, Viswanath's -0.81
correlation and below-0.5 targeted-attack result, Taheriboshrooyeh's proof-generation and
gas-cost figures, Levin's PropShare 30%-deviation/under-1%-gain pair). One finding survives.

## Finding

**File:** registry/selections/forgery-resistance.md, lines 20 and 114 (candidate table and "What
it costs and where it fails" section)

**Claim:** "scrypt at N=2^20 (3.8 s per evaluation on a 2.5 GHz reference core) raises the
estimated one-year brute-force hardware cost for an 8-character password to roughly $19 billion,
against $18,000 for PBKDF2 at the same wall-clock target, both derived from 130 nm circuit
die-area and manufacturing-cost data `PERCIVAL-BSDCAN-09`."

**What the entry states:** PERCIVAL-BSDCAN-09 reports two separate parameter sets. At the
5-second, file-encryption wall-clock target for an 8-character password from a 95-symbol
alphabet: PBKDF2 (5.0 s per guess) costs an estimated $920,000, scrypt (3.8 s per guess) costs an
estimated $19 billion. The $18,000 figure belongs to a different table entirely: PBKDF2 at the
100 ms, interactive-login wall-clock target for the same 8-character password.

**Verdict:** not-in-entry (misattributed figure — the two numbers paired in the selection come
from different experimental conditions in the cited entry, not the same one). The selection's own
phrase "at the same wall-clock target" is the error: PBKDF2's cost at scrypt's 3.8-second target
is $920,000, roughly 51 times the $18,000 figure actually used. A reader comparing "$19 billion
vs. $18,000" believes scrypt beats PBKDF2 by six orders of magnitude at one fixed latency; the
entry's own same-latency comparison is closer to four orders of magnitude ($19 billion vs.
$920,000).

**Why it matters:** the selection uses this pair to argue memory-hard functions substantially
outperform a non-memory-hard KDF at equal attacker latency, inside the "What it costs and where it
fails" discussion of computational work priced per write — the mechanism the document ultimately
selects for forgery resistance. The $920,000 figure still supports that qualitative point ($19
billion still dwarfs it); the specific $18,000 number does not belong to the comparison the
sentence claims to be making, and repeating it at both occurrences compounds the error rather than
being a one-off slip.

## Uncited claims checked

No claim in the three files carrying a factual number, measured result, or stated property was
found without a citation key attached nearby. The "What this selection requires from the rest of
the system" and "What the corpus does not settle" sections in all three files state reasoning and
scope gaps rather than new factual claims, consistent with what the brief allows uncited.

## Summary

27 claims checked, 26 supported with conditions preserved, 1 not-in-entry (a misattributed figure
pairing two different experimental conditions from the same source as though they were the same
condition, appearing twice in forgery-resistance.md).
