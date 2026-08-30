#!/usr/bin/env python3
"""Second-pass retrieval for targets whose first URL served a landing page.

Three mechanical routes, tried in order per target:
  1. Rewrite a known landing-page URL to its PDF form (arXiv /abs/ to /pdf/,
     ePrint page to .pdf, ACM abs to pdf, OpenReview forum to pdf).
  2. Download the landing page and extract every PDF link it offers, then try
     each. This is what recovers USENIX, NDSS, PoPETs, Springer and repository
     pages, which state the PDF location on the page itself.
  3. Ask Semantic Scholar for an open-access PDF location by DOI.

Prints one tab-separated line per target so the caller can tally outcomes.
"""
import json, os, re, subprocess, sys, time, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")


def rewrite(u):
    out = []
    m = re.match(r'https?://arxiv\.org/abs/(.+?)(v\d+)?/?$', u)
    if m:
        out.append("https://arxiv.org/pdf/%s" % m.group(1))
    m = re.match(r'https?://eprint\.iacr\.org/(\d{4})/(\d+)/?$', u)
    if m:
        out.append("https://eprint.iacr.org/%s/%s.pdf" % (m.group(1), m.group(2)))
    m = re.match(r'https?://dl\.acm\.org/doi/(?:abs/)?(.+)$', u)
    if m:
        out.append("https://dl.acm.org/doi/pdf/%s" % m.group(1))
    m = re.match(r'https?://openreview\.net/forum\?id=(.+)$', u)
    if m:
        out.append("https://openreview.net/pdf?id=%s" % m.group(1))
    m = re.match(r'https?://(?:www\.)?semanticscholar\.org/.*', u)
    if m:
        pass
    return out


def page_pdf_links(u):
    r = subprocess.run(["curl", "-sS", "-L", "-m", "45", "-A", UA, u],
                       capture_output=True, text=True, errors="replace")
    html = r.stdout
    links = re.findall(r'''(?:href|content|src)=["']([^"']+?\.pdf[^"']*)["']''', html, re.I)
    links += re.findall(r'''(?:href)=["']([^"']*?/pdf/[^"']*)["']''', html, re.I)
    links += re.findall(r'''["'](https?://[^"']*?(?:download|fulltext|bitstream)[^"']*)["']''', html, re.I)
    out, seen = [], set()
    for L in links:
        full = urllib.parse.urljoin(u, L)
        if full not in seen and full.startswith("http"):
            seen.add(full)
            out.append(full)
    return out[:6]


def s2_pdf(doi):
    if not doi:
        return []
    u = ("https://api.semanticscholar.org/graph/v1/paper/DOI:%s?fields=openAccessPdf"
         % urllib.parse.quote(doi))
    r = subprocess.run(["curl", "-sS", "-m", "30", u], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
        p = (d.get("openAccessPdf") or {}).get("url")
        return [p] if p else []
    except Exception:
        return []


def try_fetch(key, urls):
    if not urls:
        return None
    cmd = ["python3", os.path.join(ROOT, "tools", "fetch-paper.py"), key] + urls
    r = subprocess.run(cmd, capture_output=True, text=True)
    m = re.search(r'chars=(\d+)', r.stdout)
    ok = re.search(r'^OK (\S+)', r.stdout, re.M)
    if m and int(m.group(1)) >= 6000:
        return int(m.group(1)), ok.group(1) if ok else ""
    return None


def main():
    targets = {t['key']: t for t in json.load(open(os.path.join(ROOT, 'registry/targets-deduped.json')))}
    keys = [l.strip() for l in open(sys.argv[1]) if l.strip()]
    for key in keys:
        t = targets.get(key)
        if not t:
            print("%s\tNOTARGET\t0" % key); continue
        txt = os.path.join(ROOT, 'sources/text', key + '.txt')
        if os.path.exists(txt) and os.path.getsize(txt) >= 6000:
            print("%s\tALREADY\t%d" % (key, os.path.getsize(txt))); continue
        cands = t.get('candidate_urls', [])

        rw = []
        for u in cands:
            rw += rewrite(u)
        res = try_fetch(key, rw)
        if res:
            print("%s\tFULL-rewrite\t%d\t%s" % (key, res[0], res[1])); continue

        scraped = []
        for u in cands[:3]:
            try:
                scraped += page_pdf_links(u)
            except Exception:
                pass
        res = try_fetch(key, scraped)
        if res:
            print("%s\tFULL-scrape\t%d\t%s" % (key, res[0], res[1])); continue

        res = try_fetch(key, s2_pdf(t.get('doi', '')))
        if res:
            print("%s\tFULL-s2\t%d\t%s" % (key, res[0], res[1])); continue
        time.sleep(1)
        print("%s\tSTILL-SHORT\t0" % key)


if __name__ == "__main__":
    main()
