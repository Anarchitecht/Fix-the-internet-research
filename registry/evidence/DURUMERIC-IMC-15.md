## [DURUMERIC-IMC-15] Neither Snow Nor Rain Nor MITM...: An Empirical Analysis of Email Delivery Security

**Citation:** Zakir Durumeric, David Adrian, Ariana Mirian, James Kasten, Elie Bursztein, Nicolas Lidzborski, Kurt Thomas, Vijay Eranti, Michael D. Bailey, J. Alex Halderman. "Neither Snow Nor Rain Nor MITM...: An Empirical Analysis of Email Delivery Security." ACM Internet Measurement Conference (IMC), 2015. DOI 10.1145/2815675.2815695.
**Retrieved:** full text via https://conferences2.sigcomm.org/imc/2015/papers/p27.pdf
**Source URL:** https://conferences2.sigcomm.org/imc/2015/papers/p27.pdf
**Domain:** J

### What it does
The paper measures how completely deployed mail-transport encryption and authentication protocols are, by scanning the mail-server configurations of the Alexa Top Million domains and by analyzing a year of Gmail's own SMTP (Simple Mail Transfer Protocol, the protocol that relays messages between mail servers) handshake logs. It also measures two live network attacks against mail confidentiality: an on-path attacker corrupting the STARTTLS command during an SMTP handshake to force the connection to fall back to unencrypted transport (a downgrade attack, possible because STARTTLS fails open to cleartext on any error), and an attacker returning falsified DNS MX (mail exchange) records to redirect a sender's connection to an attacker-controlled server. The authors detect STARTTLS downgrading by sending a deliberately malformed STARTTLS command to servers across the public IPv4 address space and checking whether the server echoes back the exact bytes sent or a corrupted variant, which reveals a middlebox that rewrote the command in transit.

### Measured results
| Result | Conditions |
|---|---|
| Gmail: 80% of outgoing messages and 60% of incoming connections used STARTTLS | Snapshot as of 26 April 2015, Google's own SMTP handshake logs excluding spam |
| Gmail STARTTLS growth: outbound 52% to 80%, inbound 33% to 60% | January 2014 to April 2015, same dataset |
| 792,494 of the Alexa Top Million domains (79.25%) have operational mail servers; of those, 648,030 (81.8%) support STARTTLS | MX-record lookup and SMTP/STARTTLS handshake scan of the Alexa Top Million domains, 26 April 2015, using ZMap |
| Five third-party mail providers transport mail for 25% of the Top Million domains: Gmail 15.9%, GoDaddy 4.6%, Yandex 1.6%, QQ 1.4%, OVH 1.1% | Same Alexa Top Million domain scan; all five support inbound STARTTLS |
| 414,374 domains (52% of domains with SMTP servers, 64% of STARTTLS-supporting domains) present certificates that validate against the Mozilla NSS root store, but only 0.6% present a certificate matching the recipient's own domain name | Same scan |
| Five SMTP server implementations account for 97% of identifiable Top Million mail servers: exim 34% (Top Million) / 24% (public IPv4), Postfix 18%/21%, qmail 6%/1%, sendmail 5%/4%, Exchange 4%/12% | Installed each implementation's latest version on Ubuntu 14.04.1 LTS (Exchange documentation used instead of installation) and tested default STARTTLS behavior |
| 14.1 million IPv4 hosts had TCP port 25 open, 8.85 million responded as SMTP servers, 4.62 million (52% of responsive SMTP servers) completed a STARTTLS handshake | Public IPv4 TCP SYN scan on port 25, 20 April 2015, from the University of Michigan, using ZMap |
| 41,405 SMTP servers across 4,714 autonomous systems (ASes) and 191 countries show evidence of STARTTLS command corruption, transiting mail for 2,563 Top Million domains | Same IPv4 scan; detected via 623,635 hosts (14% of hosts that failed the TLS handshake) that echoed back the received command, of which 5,756 showed corrupted bytes, plus 35,649 more found via corrupted STARTTLS advertisement in the EHLO response |
| 96.13% of mail transiting from Tunisia to Gmail affected by STARTTLS stripping; 8 more countries above 10%, 16 more above 5% | Fraction of inbound Gmail messages originating from IPs identified as stripping TLS, measured 20-27 April 2015 |
| 178,439 of 8,860,639 responsive public DNS servers (2.01%) returned an invalid or falsified MX or A record for one of gmail.com, yahoo.com, outlook.com, qq.com, or mail.ru | Ten repeated IPv4-wide ZMap scans querying MX and A records for the five domains, 25 April 2015, from the University of Michigan |
| DKIM (DomainKeys Identified Mail) validation failure rate for inbound Gmail messages: 10.65% in November 2013, 6.14% in April 2015 | Gmail's own validation logs, two snapshots |

### Parameters
- SPF (Sender Policy Framework), DKIM, and DMARC (Domain-based Message Authentication, Reporting, and Conformance) are the three authentication extensions measured; no numeric threshold parameter is set by the authors themselves — all figures are observed deployment states, not configured experimental variables.
- Scan dates: Alexa Top Million domain scan 26 April 2015; IPv4 STARTTLS-stripping scan 20 April 2015; IPv4 DNS-falsification scan 25 April 2015; provider-encryption spot check against 19 webmail/ISP providers, date given only as "as of" the study's April 2015 window.
- Gmail transparency-report and paired cipher/authentication dataset window: January 2014 to April 2015.

### Stated limitations
The authors state their STARTTLS-corruption scanning methodology "does not comprehensively find all servers where STARTTLS is blocked," because it depends on a server echoing back the received command (only 14% did), cannot detect stripping that applies only to outgoing messages, and cannot detect a middlebox that removes the STARTTLS advertisement entirely rather than corrupting it in place — so the reported 41,405-server figure is stated as an underestimate. The Gmail-log dataset is stated to be "noticeably skewed towards a handful of large web mail providers" (Yahoo, Outlook, and large ISPs relaying bulk personal mail), so its aggregate percentages do not represent the long tail of small mail operators uniformly. The authors state end-to-end encryption (PGP, S/MIME) "does not address many of the challenges" they measure, because it leaves sender, recipient, and subject metadata exposed at the SMTP transport layer regardless of message-body encryption. The paper identifies as an open problem how to authenticate mail sent through mailing lists, because in-transit message modification invalidates DKIM signatures and blocks large providers from publishing a DMARC reject policy.

### Requirements it places on the rest of the system
A store-and-forward relay protocol that fails open to cleartext on any handshake error (STARTTLS's behavior, as measured here) requires every relay hop, not just the endpoints, to correctly negotiate encryption, because a single corrupting hop anywhere on the path suffices to force cleartext delivery for that message, and the sender has no protocol-level signal that this occurred. Certificate-based server authentication for a mail relay requires either DNSSEC-protected MX records or an equivalent authenticated-name-resolution mechanism, because a certificate that matches only the MX hostname (the common deployment pattern measured here, 34.2% of trusted certificates) provides no protection if the attacker can also falsify the DNS response that supplies that hostname. A provider-concentration mitigation such as third-party mail hosting requires the hosting provider to hold a certificate valid for its client's domain, which the authors state creates an impersonation risk if the hosting provider's systems are separately compromised.

### Contradicts
The paper's own comparison notes that Foster et al. (2015, concurrent, comparing Top Million domains from the 2013 Adobe breach data) found higher adoption rates (89% STARTTLS, 85% SPF, 68% DMARC among popular providers) than this paper's Alexa Top Million figures (81.8% STARTTLS among domains with mail servers); the authors attribute the difference to Foster et al. sampling popular providers rather than the general domain population, not to a measurement disagreement. No other paper in this batch measures SMTP transport-security deployment or DNS-record falsification for mail, so no cross-paper numeric contradiction exists in this batch.

### References worth retrieving
- foundational: Klensin. "Simple mail transfer protocol." RFC 5321, 2008.
- foundational: Hoffman. "SMTP service extension for secure SMTP over transport layer security." RFC 3207, 2002.
- competing/independent-measurement: Foster, Larson, Masich, Snoeren, Savage, Levchenko. "Security by any other name: On the effectiveness of provider based email security." ACM CCS 2015.
- independent-measurement: Rijs, van der Meer. "The state of StartTLS." June 2014 (116 Dutch organizations).
- competing methodology: Holz, Braun, Kammenhuber, Carle. "The SSL landscape: A thorough analysis of the X.509 PKI using active and passive measurements." IMC 2011.
- foundational (scanning tool): Durumeric, Wustrow, Halderman. "ZMap: Fast Internet-wide scanning and its security applications." USENIX Security 2013.
- attack/related: Duan, Weaver, Zhao, Hu, Liang, Jiang, Li, Paxson. "Hold-on: Protecting against on-path DNS poisoning." Workshop on Securing and Trusting Internet Names, 2012.

### Verbatim extracts
- "only 35% successfully conﬁgure encryption, and 1.1% specify a DMARC authentication policy"
- "highlighting seven countries where more than 20% of inbound Gmail messages arrive in cleartext"
- "Five providers are used for mail transport by 25% of the Top Million domains"
- "only 0.6% are valid for the recipient domain"
- "our scanning methodology does not comprehensively ﬁnd all servers where STARTTLS is blocked"
- "end-to-end mail encryption... does not address many of the challenges we discuss"
