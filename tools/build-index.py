#!/usr/bin/env python3
"""Build a compact index of the evidence entries.

Each row states the key, the domain, the year, the title, and the first sentence of the measured
results. An agent reads this one file to decide which entries to open, instead of searching the
whole evidence file. Also writes a requirements index, which is what the composition check runs on:
one row per entry stating what that mechanism needs from the rest of the system.
"""
import glob, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def section(text, name):
    m = re.search(r'###\s+%s\s*\n(.*?)(?=\n###\s|\Z)' % re.escape(name), text, re.S)
    return m.group(1).strip() if m else ''


def first_sentences(s, n=2):
    s = re.sub(r'\s+', ' ', re.sub(r'\|', ' / ', s)).strip()
    parts = re.split(r'(?<=[.;])\s+', s)
    return ' '.join(parts[:n])[:400]


def main():
    targets = {}
    tp = os.path.join(ROOT, 'registry/targets-deduped.json')
    if os.path.exists(tp):
        targets = {t['key']: t for t in json.load(open(tp))}

    rows, reqs = [], []
    for f in sorted(glob.glob(os.path.join(ROOT, 'registry/evidence/*.md'))):
        key = os.path.basename(f)[:-3]
        text = open(f, errors='replace').read()
        t = targets.get(key, {})
        title = t.get('title', '')
        if not title:
            m = re.match(r'##\s*\[?[A-Z0-9-]+\]?\s*(.+)', text)
            title = m.group(1).strip() if m else key
        rows.append({
            'key': key,
            'domain': t.get('domain', '?'),
            'year': t.get('year', ''),
            'title': title[:110],
            'measured': first_sentences(section(text, 'Measured results')),
        })
        r = section(text, 'Requirements it places on the rest of the system')
        if r:
            reqs.append({'key': key, 'domain': t.get('domain', '?'),
                         'title': title[:90], 'requires': first_sentences(r, 4)})

    with open(os.path.join(ROOT, 'registry/index-measurements.md'), 'w') as fh:
        fh.write('# Measurement index\n\nOne row per evidence entry. `Measured` is the opening of that '
                 'entry\'s measured-results section, so a reader can tell which entries hold a figure '
                 'for a given quantity without opening all of them.\n\n')
        fh.write('| Key | Dom | Year | Title | Measured |\n|---|---|---|---|---|\n')
        for r in rows:
            fh.write('| `%s` | %s | %s | %s | %s |\n' % (r['key'], r['domain'], r['year'],
                                                         r['title'].replace('|', '/'),
                                                         r['measured'].replace('|', '/')))

    with open(os.path.join(ROOT, 'registry/index-requirements.md'), 'w') as fh:
        fh.write('# Requirements index\n\nWhat each mechanism needs from the rest of the system. The '
                 'composition check runs on this: a conflict exists when one selected component '
                 'removes something another selected component requires.\n\n')
        fh.write('| Key | Dom | Title | Requires from elsewhere |\n|---|---|---|---|\n')
        for r in reqs:
            fh.write('| `%s` | %s | %s | %s |\n' % (r['key'], r['domain'],
                                                    r['title'].replace('|', '/'),
                                                    r['requires'].replace('|', '/')))
    print('index-measurements.md: %d rows' % len(rows))
    print('index-requirements.md: %d rows' % len(reqs))


if __name__ == '__main__':
    main()
