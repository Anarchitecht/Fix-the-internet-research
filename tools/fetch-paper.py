#!/usr/bin/env python3
"""Retrieve one paper and extract its full text.

Usage: fetch-paper.py KEY URL [URL ...]

Tries each URL in order until one yields a document. A PDF is saved to
sources/pdf/KEY.pdf and its text to sources/text/KEY.txt. An HTML page is saved
to sources/text/KEY.txt with tags stripped. Prints the outcome, the page count,
and the character count, so the caller can tell a real full text from a
paywall stub: under 6000 characters means the retrieval did not produce a paper.
"""
import sys, os, re, subprocess, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_DIR = os.path.join(ROOT, "sources", "pdf")
TXT_DIR = os.path.join(ROOT, "sources", "text")
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")


def get(url, out):
    cmd = ["curl", "-sS", "-L", "-m", "90", "--retry", "2", "--retry-delay", "3",
           "-A", UA, "-o", out, "-w", "%{http_code} %{content_type}", url]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        return None, None, r.stderr.strip()[:200]
    parts = r.stdout.strip().split(None, 1)
    code = parts[0] if parts else "000"
    ctype = parts[1] if len(parts) > 1 else ""
    return code, ctype, None


def pdf_text(path):
    import pypdf
    reader = pypdf.PdfReader(path)
    pages = [p.extract_text() or "" for p in reader.pages]
    return len(reader.pages), "\n\n".join(pages)


def html_text(path):
    raw = open(path, "rb").read().decode("utf-8", "replace")
    raw = re.sub(r"(?is)<(script|style|nav|footer|header)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    raw = html.unescape(raw)
    return re.sub(r"[ \t]+", " ", re.sub(r"\n{3,}", "\n\n", raw)).strip()


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    key, urls = sys.argv[1], sys.argv[2:]
    os.makedirs(PDF_DIR, exist_ok=True)
    os.makedirs(TXT_DIR, exist_ok=True)
    tmp = os.path.join(PDF_DIR, key + ".download")
    txt_path = os.path.join(TXT_DIR, key + ".txt")

    for url in urls:
        code, ctype, err = get(url, tmp)
        if err:
            print(f"TRIED {url} -> transport error: {err}")
            continue
        size = os.path.getsize(tmp) if os.path.exists(tmp) else 0
        if code != "200" or size < 1500:
            print(f"TRIED {url} -> HTTP {code}, {size} bytes")
            continue
        head = open(tmp, "rb").read(5)
        try:
            if head.startswith(b"%PDF"):
                pdf_path = os.path.join(PDF_DIR, key + ".pdf")
                os.replace(tmp, pdf_path)
                npages, text = pdf_text(pdf_path)
            else:
                npages, text = 0, html_text(tmp)
                os.remove(tmp)
        except Exception as e:
            print(f"TRIED {url} -> parse failed: {type(e).__name__}: {e}")
            continue
        # A landing page can exceed the character floor, so check for the markup only a
        # publisher or repository page carries. Several of these together mean the retrieval
        # produced a page about the paper rather than the paper.
        LANDING = ("Which authors of this paper are endorsers", "Bibliographic Tools",
                   "Skip to main content", "Connected Papers Toggle", "Semantic Scholar Toggle",
                   "Recommenders and Search Tools", "Institutional Login",
                   "Sign in to view", "Request a copy")
        hits = sum(1 for sig in LANDING if sig.lower() in text[:20000].lower())
        if hits >= 2 or (hits >= 1 and len(text) < 30000):
            print(f"TRIED {url} -> landing page, not the paper ({hits} page-furniture markers)")
            continue
        open(txt_path, "w").write(text)
        verdict = "FULL TEXT" if len(text) >= 6000 else "TOO SHORT - probably a stub or a paywall page"
        print(f"OK {url}\n  key={key} pages={npages} chars={len(text)} -> {txt_path}\n  {verdict}")
        return 0

    print(f"FAILED {key}: no URL yielded a document")
    return 1


if __name__ == "__main__":
    sys.exit(main())
