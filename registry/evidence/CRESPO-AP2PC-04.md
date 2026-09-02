## [CRESPO-AP2PC-04] Semantic Overlay Networks for P2P Systems

**Citation:** Arturo Crespo, Hector Garcia-Molina. "Semantic Overlay Networks for P2P Systems." AP2PC (Agents and Peer-to-Peer Computing, revised and invited papers), 2004/2005. DOI 10.1007/11574781_1.
**Retrieved:** full text via http://infolab.stanford.edu/~crespo/publications/op2p.pdf
**Source URL:** http://infolab.stanford.edu/~crespo/publications/op2p.pdf
**Domain:** B

### What it does
The paper reduces the number of nodes a query must reach in an unstructured peer-to-peer (P2P) network, by grouping nodes with semantically similar content into a Semantic Overlay Network (SON) and routing each query only to the SON or SONs likely to hold matching content, instead of forwarding every query to every node. A classification hierarchy (for example: music style, split into substyles; or decade; or tone) defines one candidate SON per category in the hierarchy. Each node classifies its own documents into categories and joins the SON of every category for which it holds matching content (the paper calls this the conservative join strategy). A query is classified into a category using the same hierarchy and sent to the node's neighbor(s) within the corresponding SON, which forwards it only to the other members of that SON; nodes outside the matching SON never receive the query. A refinement, Layered SONs, has a node join a category's SON only when the fraction of that node's documents falling in that category exceeds a threshold percentage; categories below the threshold are aggregated upward into their parent category's SON, and every node always joins the SON at the root of the hierarchy so no document becomes permanently unreachable. The paper does not specify intra-SON routing (how a query reaches all members once inside one SON); it treats that as a separately solved problem and represents each SON as a flat set of nodes.

### Measured results
| Result | Conditions |
|---|---|
| Document classifier misclassification rate: 25% of individual files classified incorrectly | 200 randomly selected filenames from the 1,800-node Napster crawl, manually classified by the authors and compared against automatic classifier output using the All Music database with phonetic-search fallback for misspellings |
| Node-level misclassification rate: only 4% of nodes classified incorrectly, despite 25% per-document error | 20 randomly selected nodes, all their documents classified, node assigned to every substyle any of its documents matched; a node counted as incorrect only if it lacked assignment to a substyle it should have belonged to |
| Style classification: 24% of nodes (425 of ~1,800) have files in only one style category; 90% of nodes have files in 8 or fewer of 26 style categories | 1,800-node Napster crawl (University of Washington, May 2001), style/substyle classification hierarchy (26 style categories, 255 substyle categories) applied via the All Music database |
| Substyle classification: 18% of nodes (328) have files in only one substyle; 90% of nodes have files in 30 or fewer of 255 substyle categories | Same 1,800-node crawl and hierarchy |
| Largest style SON ("Rock") would contain documents belonging to nearly all ~1,800 nodes under conservative joining; largest substyle SON ("Alternative Pop Rock") contains 1,031 nodes (57%) even after subdividing Rock into substyles | Same crawl, conservative join strategy (join every SON for which the node holds at least one matching document) |
| Query classification (manual, by the paper's authors) of 50 distinct real queries: 8% classified at the hierarchy root, 78% at the style level, 14% at the substyle level | 50-query trace drawn from real OpenNap query logs at a Stanford server, deduplicated from a larger trace |
| Layered SONs (35% join threshold) reduce SON membership: 34% of nodes (616) belong to just one style SON (vs 24% conservative), and 97% belong to 4 or fewer style SONs (vs 90% at 8-or-fewer under conservative) | Same 1,800-node crawl, Style/Substyle hierarchy, Layered SON join threshold set to 35% |
| At 50% recall, Layered SONs require 461 messages versus 1,731 for a Gnutella-like flood, a 375% reduction in message count; at 92% recall Layered SONs use about 1/5 the messages Gnutella requires | Simulated acyclic network, average node degree 4, 1,800-node crawl, 50 real queries classified at the substyle (most precise) level, averaged over 50 simulation runs on randomly generated topologies |
| Average maximum recall achieved by Layered SONs across all 50 queries (all classification levels combined) is 93%, not 100%, attributed to node-classification mistakes | Same simulation setup, all 50 queries regardless of classification precision, averaged over 50 topology-randomized runs |

### Parameters
- Napster crawl size: 1,800 nodes, University of Washington crawl, May 2001
- Style categories: 26 (single-category-per-file); substyle categories: 255 (multi-category-per-file); decade categories: 8 buckets (10's-or-before through 90's-or-newer, single-category); tone categories: 128 (multi-category-per-file)
- Layered SON join threshold: swept implicitly from 0% (equivalent to conservative joining) up to the reported 35% experiment
- Simulated network topology: acyclic graph, average node degree 4 (both SON and Gnutella-baseline networks), 50 runs per data point on independently randomized topologies
- Query set: 50 distinct real queries from an OpenNap server trace at Stanford, deduplicated from a larger trace the paper attributes to duplicates from OpenNap-overlay routing cycles

### Stated limitations
The paper states it does not address security problems, noting that "inconsistent hierarchies" among nodes are a possible consequence left unaddressed. It states it does not focus on how queries are routed once inside a single overlay network (intra-SON routing), treating this as solved by existing techniques and out of scope. The acyclic-network assumption used in the message-count experiments is stated by the authors to be unrealistic; they justify it by stating that cycles increase message counts independently of SON structure, so the acyclic result is a lower bound on messages, not a realistic absolute figure. Layered SONs are stated to trade a small reduction in maximum achievable recall (93% average, not 100%) for lower per-node SON membership and lower query cost, versus the conservative strategy's guarantee of finding all matching documents. The paper states that due to space limits it omits full experimental results and formal definitions, pointing to an extended technical report version. Query classification in the experiments was performed manually by the paper's own authors, not by an automatic query classifier, and the paper states it therefore cannot evaluate the correctness of query classification, only its precision (how often a query lands at the root, style, or substyle level).

### Requirements it places on the rest of the system
Every participating node must run the same classification hierarchy and the same (or a compatible) document classifier, because SON membership is determined by which hierarchy category a document's automatic classification falls into; a node using a different hierarchy would join incompatible SON identifiers and queries would not reach it. Query issuers must classify each outgoing query into the same hierarchy before dispatch, and the paper's own measurement shows classification precision varies by query (78% land only at the coarse style level, not the finer substyle level in its experiment), which directly sets how many nodes a query reaches — a coarser classification sends the query to a larger SON. The scheme requires a separate, already-solved intra-SON routing mechanism to deliver a query to every member of a chosen SON once it enters that SON; this paper supplies none itself. Layered SONs require every node to always join the root-level SON regardless of the join threshold, to guarantee that documents in below-threshold categories remain reachable via a full search of the root SON; omitting the root join makes those documents permanently unfindable within the scheme.

### Contradicts
None found against other entries in this batch as of this extraction.

### References worth retrieving
- Crespo, Garcia-Molina. "Semantic overlay networks for P2P systems." Technical report, Stanford University, January 2003. -- foundational (this paper's own extended/formal version, referenced repeatedly for definitions and results omitted here for space)
- Ratnasamy, Francis, Handley, Karp, Shenker. "A scalable content-addressable network." SIGCOMM 2001. -- competing (structured-overlay alternative the paper contrasts against for lack of node autonomy)
- Stoica, Morris, Karger, Kaashoek, Balakrishnan. "Chord: A scalable peer-to-peer lookup service for internet applications." SIGCOMM 2001. -- competing (already in corpus as STOICA-SIGCOMM-01)
- Rowstron, Druschel. "Pastry: Scalable, distributed object location and routing for large-scale peer-to-peer systems." Middleware 2001. -- competing
- Kubiatowicz, Bindel, Chen, Czerwinski, Eaton, Geels, Gummadi, Rhea, Weatherspoon, Weimer, Wells, Zhao. "OceanStore: An architecture for global-scale persistent storage." ASPLOS 2000. -- competing
- Zhao et al. (ref [21], cited but not spelled out in the retrieved bibliography excerpt). "Tapestry." -- foundational
- Nejdl, Siberski, Wolpers, Schmitz. "Routing and clustering in schema-based super peer networks." -- competing (Edutella, a decentralized clustering approach the paper contrasts against)
- Schlosser, Sintek, Decker, Nejdl. "A scalable and ontology-based P2P infrastructure for semantic web services." -- competing (HyperCup)
- Sahami, Baldonado. "SONIA: A service for organizing networked information autonomously." Digital Libraries 1998. -- foundational (centralized clustering baseline the paper contrasts against)
- Saroiu, Gummadi, Gribble. "A measurement study of peer-to-peer file sharing systems." UW-CSE-01-06-02, 2002. -- foundational (already in corpus, retrieved as GUMMADI-CCR-02 -- see mismatch note in that entry)

### Verbatim extracts
"nodes that have few results for this query will not receive it"
"we do not address security problems in this paper, but inconsistent hierarchies may be"
"we found that 25% of the files were classified incorrectly"
"we found that only 4% of the nodes were classified incorrectly"
"Layered SONs required only 461 messages, while Gnutella needed 1731 messages"
"average maximum recall was 93%"
