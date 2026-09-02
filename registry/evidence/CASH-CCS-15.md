## [CASH-CCS-15] Leakage-Abuse Attacks Against Searchable Encryption

**Citation:** David Cash, Paul Grubbs, Jason Perry, Thomas Ristenpart. "Leakage-Abuse Attacks Against Searchable Encryption." ACM CCS, 2015. DOI 10.1145/2810103.2813700.
**Retrieved:** full text via https://eprint.iacr.org/2016/718.pdf
**Source URL:** https://eprint.iacr.org/2016/718.pdf
**Domain:** G

### What it does
Searchable encryption (SE) lets a client store encrypted documents at a server and query them by keyword without revealing plaintext, at the cost of a defined leakage profile: information the server sees during upload and search even under the scheme's security proof. This paper builds attacks that recover a client's query keywords or plaintext content from that leakage alone, given a stated amount of auxiliary knowledge, without breaking any cryptographic primitive.

The paper defines four leakage profiles ordered by amount of information revealed, L1 (least) to L4 (most). L1 (query-revealed occurrence pattern) leaks, for each queried keyword, the set of document identifiers containing it (the access pattern), revealed only for queried terms. L2 (fully-revealed occurrence pattern) leaks the same occurrence sets for every term in the corpus, not only queried ones, but not the order of terms within a document. L3 adds the within-document order of first keyword occurrence. L4 leaks the full plaintext under a deterministic word-substitution cipher (every occurrence, not just first, visible).

The count attack (query recovery, targets L1) assumes the adversarial server additionally knows, for every keyword in a fixed vocabulary, the number of documents in the true corpus containing that keyword (`count(w)`). A keyword with a document-count value not shared by any other keyword is recovered immediately by matching the observed query's result-set size to that unique count. Remaining queries are recovered by iteratively comparing observed co-occurrence counts between pairs of queries against the co-occurrence counts computable from the known document set, eliminating candidate keywords whose co-occurrence count does not match; the process repeats until no further query is disambiguated. The attack needs no known queries and no numerical optimization, unlike the prior IKK attack (Islam, Kuzu, Kantarcioglu, NDSS 2012), which uses simulated annealing to match an observed co-occurrence matrix to a known one and requires some fraction of queries to be known in advance.

The generalized count attack extends this to two adversary-knowledge deficits. First, index padding (the client pads each keyword's document-count entry up to a multiple of an integer n, so multiple keywords may share a padded count): the attack tolerates false co-occurrences up to a bounded window and bootstraps candidate queries by brute-force guessing rather than requiring an initial unique-count match. Second, partial document knowledge (the server holds only a fraction of the true document set): the adversary estimates each keyword's true document count with a Hoeffding-inequality confidence interval computed from the known subset, and prunes candidate keywords whose interval excludes the observed query result size.

The plaintext recovery attacks (target L2 and L3) exploit a server that knows the plaintext of a small number of stored documents (known-document attack) or can insert chosen documents into the client's store (chosen-document, active attack). Under L3 (keyword order preserved), the server reads keyword hashes directly off the known plaintext's position-ordered ciphertext. Under L2 (keyword order randomized per document), a known document only narrows a keyword hash to the set of hashes appearing in that document; the chosen-document variant plants documents whose keywords are drawn to have maximally separated frequency ranks (computed from an auxiliary corpus, related or unrelated to the target), then matches observed hash frequency ranks in the client's uploaded data to the planted keywords' known ranks.

### Measured results

| Attack | Dataset | Conditions | Result |
|---|---|---|---|
| IKK (reproduced) | Enron, 150 employees' sent mail, 30,109 docs, 50 MB on disk | 150 unique queries, 15% of queries known, vocabulary swept 500-6500 keywords, 25 trials (15 above 3500 keywords, since one 6500-keyword trial takes over 10 hours) | Recovery near-perfect at 500 keywords, falls with vocabulary size; performs poorly above 5000 keywords |
| Count attack | Enron, same setup | 10% of keywords queried, no known queries, vocabulary swept 500-6500 keywords, 25 trials | Outperforms IKK at every vocabulary size tested; worst trial at 6500 keywords failed to reconstruct only 5 of 650 keywords |
| IKK vs. count, known-query sensitivity | Enron, m=4500 keywords, 150 unique queries | 15% of queries known vs. 5% known | IKK recovers ~25% of queries at 15% known, drops to 0% at 5% known |
| Count attack under index padding | Enron and Apache "java-user" mailing list (2001-2011, ~38,000 emails, 244 MB on disk) | 5000 keywords, 10% queried, 25 trials (5 random paddings x 5 query transcripts) | Reconstruction unaffected up to index-size expansion of ~140% (Enron) / ~330% (Apache); at over 500% expansion, Enron attack still learns all keywords in half of trials; implementation fails completely above 700% expansion |
| Count attack under partial document knowledge | Enron, 500 keywords, 150 queries | Server knows 50-100% of true document set, 25+ trials (5 document subsets x 5 query transcripts) | Outperforms IKK at every knowledge level tested; below 99% document knowledge IKK performs quite poorly; at 50% knowledge the count attack's false-positive rate exceeds its recovery rate |
| Known-document plaintext recovery (L3) | Enron and Apache | Adversary knows 2 or 20 random documents, cumulative recovery rate over 10 selections per condition | In the Apache dataset, with only 2 known documents, 80% of all documents have 20% of their keywords exposed |
| Known-document plaintext recovery, non-random known document | Enron | Single company-wide announcement email, 500 recipients, 832 unique keywords | Average of 35% of indexed keywords recovered across every document in the corpus |
| Chosen-document attack, hash order unknown (L2) | Apache and Enron | 5000 keywords; two settings: 50/50 split of one dataset (server trains on half, client uploads the other half) and cross-dataset (Enron frequencies attack Apache and vice versa); documents of size k=0-20 keywords, 10 runs per setting for the 50/50 case | For the 50/50 split, error rate exceeds recovery rate above k≈19 keywords per planted document; cross-dataset recovery starts lower than 50/50-split recovery but its error rate is not worse, indicating consistent word-frequency rank across the two corpora |

### Parameters
- Vocabulary size (fixed per experiment, most common stemmed keywords after 200-stopword removal): swept 500 to 6500; typical value 5000.
- Fraction of queries known to the adversary (IKK only): 14-15% in the reproduced experiments, versus 0% for the count attack.
- Fraction of keywords queried: 10% in the main count-attack comparison.
- Padding multiple n (index-expansion factor): swept 1x to 8x (0% to 700% expansion).
- Fraction of true document set known to server: swept 50% to 100% in 10% increments.
- Hoeffding-inequality confidence parameter used in the partial-knowledge count attack: ε = sqrt(0.5 · n · log 40), giving a 95% confidence interval on a keyword's true document count.
- Chosen-document size k (keywords per planted document): swept 0 to 20.

### Stated limitations
The attacks require the server to already hold a leakage profile of L1 or greater and, for the count attack, explicit or statistical knowledge of the true document set's keyword-occurrence counts; a server with zero prior document knowledge and disjoint query and training corpora causes both the IKK attack and the count attack to fail completely (the paper's own tested "unknown documents" case). The generalized count attack under partial knowledge shows a sharp accuracy floor: below 60% document knowledge, tightening candidate pruning with confidence intervals performs worse than a coarser worst-case window, because the co-occurrence estimate is higher-dimensional and needs more samples than a single keyword-count estimate to reach comparable accuracy. The authors state active insertion under L3 is "obviously very damaging" and do not further analyze it, leaving its quantification to future work. The authors state a future statistical attack, not yet demonstrated, might succeed even in the disjoint-corpus setting or above 700% padding overhead. The authors state L1 is not proven safe in general: when a large fraction of possible keywords is queried, L1 leakage approaches L2 leakage in practical exposure.

### Requirements it places on the rest of the system
A design using searchable encryption for network-hosted content must state, for its actual index construction, which of the four leakage profiles (L1-L4) it produces, since the attacks in this paper apply differently by profile: L1 requires the adversary already possess or estimate the true document-count-per-keyword to mount the count attack; L2 and L3 are vulnerable to known-document and chosen-document attacks with no separate count knowledge needed. Any content-addressed or peer-served index that lets an adversarial peer observe repeated queries against a corpus it also holds, even partially, supplies the exact precondition (partial document knowledge, observed access pattern) these attacks use; the paper's own experiments show partial knowledge as low as 50% is already exploitable via the confidence-interval attack. A scheme relying on per-query result-length hiding to defend against this must hide the count in a way immune to the padding attack's own bypass point: expansion above roughly 140-330% (dataset-dependent) is required before this paper's count attack degrades, and the paper's own implementation still partially recovers keywords up to 500% expansion.

### Contradicts
None found within this corpus. The paper's own count attack strictly dominates the IKK attack (Islam, Kuzu, Kantarcioglu, NDSS 2012) on every metric tested in this paper, which corrects any claim that IKK represents the strongest available leakage-abuse attack against L1-leakage SE.

### References worth retrieving
- foundational: R. Curtmola, J. A. Garay, S. Kamara, R. Ostrovsky. "Searchable symmetric encryption: improved definitions and efficient constructions." ACM CCS, 2006.
- foundational: M. S. Islam, M. Kuzu, M. Kantarcioglu. "Access pattern disclosure on searchable encryption: Ramification, attack and mitigation." NDSS, 2012. (the IKK attack this paper directly extends)
- competing: D. Cash, S. Jarecki, C. S. Jutla, H. Krawczyk, M.-C. Rosu, M. Steiner. "Highly-scalable searchable symmetric encryption with support for boolean queries." CRYPTO, 2013.
- competing: D. Cash, J. Jaeger, S. Jarecki, C. S. Jutla, H. Krawczyk, M.-C. Rosu, M. Steiner. "Dynamic searchable encryption in very-large databases: Data structures and implementation." NDSS, 2014.
- attack: O. Goldreich, R. Ostrovsky. "Software protection and simulation on oblivious RAMs." Journal of the ACM, 1996. (ORAM, cited as the stronger but slower alternative to SE)
- competing: W. He, D. Akhawe, S. Jain, E. Shi, D. Song. "Shadowcrypt: Encrypted web applications for everyone." ACM CCS, 2014.
- competing: B. Lau, S. Chung, C. Song, Y. Jang, W. Lee, A. Boldyreva. "Mimesis aegis: A mimicry privacy shield." USENIX Security, 2014.

### Verbatim extracts
- "we present a characterization of the leakage profiles of in-the-wild searchable encryption products"
- "the count attack is not given any known queries"
- "worst trial the count attack failed to reconstruct only 5 of 650 keywords"
- "recovery rate drops from 85% to 65% at the first increment of added noise" (describing IKK's own result under co-occurrence noise, not this paper's count attack)
- "unless the server has access to 99% of the true document data, the IKK attack performs quite poorly"
- "80% of the documents will have 20% of their keywords exposed"
- "it is dangerous to attempt to protect queries on known document sets using SE schemes"
