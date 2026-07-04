import re
import urllib.parse
import urllib.request

CHORD_IN_BRACKET = re.compile(
    r'\[([A-G](?:#|b)?(?:maj7|m7|sus4|dim|aug|min|m|7)?)\]',
    re.I,
)
CHORD_PLAIN = re.compile(
    r'\b([A-G](?:#|b)?(?:maj7|m7|sus4|dim|aug|min|m|7)?)\b',
    re.I,
)
CHORD_VALIDATE = re.compile(
    r'^[A-G](?:#|b)?(?:maj7|m7|sus4|dim|aug|min|m|7)?$',
    re.I,
)
CHORDTELA_POST = re.compile(
    r'https://www\.chordtela\.com/\d{4}/\d{2}/[a-z0-9\-]+\.html',
    re.I,
)
UG_TAB_LINK = re.compile(
    r'\[([^\]]+)\]\((https://tabs\.ultimate-guitar\.com/tab/[^)]+-chords-\d+)\)',
    re.I,
)
UG_ARTIST_LINK = re.compile(
    r'\[([^\]]+)\]\(https://www\.ultimate-guitar\.com/artist/[^)]+\)',
    re.I,
)
TITLE_LINE = re.compile(r'^Title:\s*(.+)$', re.M)
SOURCE_FROM_URL = {
    'chordtela.com': 'chordtela',
    'ultimate-guitar.com': 'ultimate-guitar',
    'tabs.ultimate-guitar.com': 'ultimate-guitar',
}

UA = 'Mozilla/5.0 (compatible; strumar/1.0; +https://github.com/ar/strumar)'


def _fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return res.read().decode('utf-8', 'ignore')


def _source_from_url(url):
    host = urllib.parse.urlparse(url).netloc.lower().replace('www.', '')
    for key, name in SOURCE_FROM_URL.items():
        if key in host:
            return name
    return 'unknown'


def _normalize_chord(raw):
    if not raw:
        return None
    token = raw.strip().replace('min', 'm')
    if not CHORD_VALIDATE.match(token):
        return None
    root = token[0].upper()
    rest = token[1:]
    return root + rest


def _parse_title_artist(markdown, source, fallback_title=''):
    title_m = TITLE_LINE.search(markdown)
    title_line = title_m.group(1).strip() if title_m else fallback_title

    if source == 'chordtela':
        m = re.search(r'Kunci Gitar\s+(.+?)\s*[-–]\s*(.+?)\s+Chord', title_line, re.I)
        if m:
            return m.group(2).strip(), m.group(1).strip()
    if source == 'ultimate-guitar':
        m = re.search(r'^(.+?)\s*[-–]\s*(.+?)\s*\(Chords\)', title_line, re.I)
        if m:
            return m.group(2).strip(), m.group(1).strip()
        m = re.search(r'Kunci Gitar\s+(.+?)\s+(.+?)\s+chord', title_line, re.I)
        if m:
            return m.group(2).strip(), m.group(1).strip()

    if ' - ' in title_line:
        artist, title = title_line.split(' - ', 1)
        return title.strip(), artist.strip()
    return title_line or 'Lagu', 'Unknown'


def _trim_markdown(markdown):
    trimmed = markdown
    body_idx = trimmed.find('Markdown Content:')
    if body_idx >= 0:
        trimmed = trimmed[body_idx + len('Markdown Content:'):]

    for marker in (
        'Chord Kunci Gitar Terkait',
        'Related tabs',
        '## Related',
        'Lirik Lagu Lainnya',
        'Sign up Log in',
    ):
        idx = trimmed.find(marker)
        if idx > 400:
            trimmed = trimmed[:idx]
    return trimmed


def _extract_chord_tokens(text):
    tokens = []
    for m in CHORD_IN_BRACKET.finditer(text):
        c = _normalize_chord(m.group(1))
        if c:
            tokens.append(c)
    for m in CHORD_PLAIN.finditer(text):
        c = _normalize_chord(m.group(1))
        if c:
            tokens.append(c)
    return tokens


def _is_progression_line(line):
    tokens = _extract_chord_tokens(line)
    if len(tokens) < 2:
        return False
    plain = re.sub(r'\[.*?\]', '', line)
    plain = re.sub(r'\b[A-G](?:#|b)?(?:maj7|m7|sus4|dim|aug|min|m|7)?\b', '', plain, flags=re.I)
    plain = re.sub(r'[^A-Za-z]+', '', plain)
    return len(plain) < 24


def extract_chords(markdown, source):
    markdown = _trim_markdown(markdown)
    if source == 'ultimate-guitar':
        blocks = re.findall(r'```[\s\S]*?```', markdown)
        text = '\n'.join(blocks) if blocks else markdown
    else:
        section_lines = []
        for line in markdown.splitlines():
            if re.search(r'\b(Intro|Verse|Reff|Ref|Chorus|Bridge|Interlude|Outro|Musik)\b', line, re.I):
                section_lines.append(line)
            elif _is_progression_line(line):
                section_lines.append(line)
        text = '\n'.join(section_lines) if section_lines else markdown

    ordered = []
    seen = set()
    for token in _extract_chord_tokens(text):
        if token not in seen:
            seen.add(token)
            ordered.append({'name': token})

    if len(ordered) < 3:
        for token in _extract_chord_tokens(markdown):
            if token not in seen:
                seen.add(token)
                ordered.append({'name': token})

    return ordered[:12]


def parse_song_from_markdown(markdown, url, source=None):
    source = source or _source_from_url(url)
    title, artist = _parse_title_artist(markdown, source)
    chords = extract_chords(markdown, source)

    capo = None
    capo_m = re.search(r'Capo(?:\s+di\s+fret)?[:\s]+(?:fret\s+)?(\d+)', markdown, re.I)
    if capo_m:
        capo = int(capo_m.group(1))

    return {
        'id': f'online:{source}:{urllib.parse.quote(url, safe="")}',
        'title': title,
        'artist': artist,
        'source': source,
        'url': url,
        'meter': '4/4',
        'tempo': 90,
        'pickPattern': 'pola-2',
        'capo': capo,
        'chords': chords,
    }


def fetch_page_markdown(url):
    if not url.startswith('http'):
        raise ValueError('URL tidak valid')
    source = _source_from_url(url)
    if source == 'unknown':
        raise ValueError('Sumber tidak didukung — gunakan ChordTela atau Ultimate Guitar')

    jina_url = 'https://r.jina.ai/' + url
    return _fetch(jina_url, timeout=35), source


def fetch_song(url):
    markdown, source = fetch_page_markdown(url)
    song = parse_song_from_markdown(markdown, url, source)
    if not song['chords']:
        raise ValueError('Chord tidak ketemu di halaman ini')
    return song


def _title_case_slug(words):
    return ' '.join(w.capitalize() for w in words if w)


def _meta_from_slug(slug, query=''):
    parts = [p for p in slug.replace('.html', '').split('-') if p]
    if len(parts) < 2:
        return 'Unknown', slug
    qwords = [w for w in re.split(r'\s+', query.lower()) if len(w) > 2]
    best_split = 2
    best_score = -1
    for split in range(1, min(len(parts), 5)):
        title_words = parts[-split:]
        title_slug = ' '.join(title_words)
        score = sum(1 for w in qwords if w in title_slug)
        if score > best_score:
            best_score = score
            best_split = split
    title = _title_case_slug(parts[-best_split:])
    artist = _title_case_slug(parts[:-best_split]) or 'Unknown'
    return artist, title


def _result_item(source, url, artist, title):
    return {
        'id': f'{source}:{url}',
        'title': title,
        'artist': artist,
        'url': url,
        'source': source,
        'label': f'{title} — {artist} ({source})',
    }


def search_chordtela(query, limit=6):
    page = 'https://www.chordtela.com/?s=' + urllib.parse.quote(query)
    markdown = _fetch('https://r.jina.ai/' + page, timeout=25)
    results = []
    seen = set()

    for m in re.finditer(
        r'Kunci Gitar\s+([^-\n]+?)\s*-\s*(.+?)\s+Chord',
        markdown,
        re.I,
    ):
        artist = re.sub(r'\*+', '', m.group(1)).strip()
        title = re.sub(r'\*+', '', m.group(2)).strip()
        window = markdown[m.end():m.end() + 500]
        url_m = CHORDTELA_POST.search(window)
        if not url_m:
            continue
        url = url_m.group(0)
        if url in seen:
            continue
        seen.add(url)
        results.append(_result_item('chordtela', url, artist, title))
        if len(results) >= limit:
            return results

    for url in CHORDTELA_POST.findall(markdown):
        if url in seen:
            continue
        seen.add(url)
        slug = url.rsplit('/', 1)[-1]
        artist, title = _meta_from_slug(slug, query)
        results.append(_result_item('chordtela', url, artist, title))
        if len(results) >= limit:
            break
    return results


def search_ultimate_guitar(query, limit=6):
    page = (
        'https://www.ultimate-guitar.com/search.php?search_type=title&value='
        + urllib.parse.quote(query)
    )
    markdown = _fetch('https://r.jina.ai/' + page, timeout=30)
    results = []
    seen = set()
    lines = markdown.splitlines()

    for i, line in enumerate(lines):
        for m in UG_TAB_LINK.finditer(line):
            title = m.group(1).strip()
            url = m.group(2).strip()
            if '/tab/' not in url or url in seen:
                continue
            seen.add(url)
            artist = 'Unknown'
            for j in range(max(0, i - 4), i):
                art_m = UG_ARTIST_LINK.search(lines[j])
                if art_m:
                    artist = art_m.group(1).replace('_', ' ').strip()
                    break
            results.append(_result_item('ultimate-guitar', url, artist, title))
            if len(results) >= limit:
                return results
    return results


def _relevance_score(query, item):
    blob = f"{item['title']} {item['artist']} {item['url']}".lower()
    words = [w for w in query.lower().split() if len(w) > 2]
    if not words:
        return 0
    hits = sum(1 for w in words if w in blob)
    score = hits * 3
    if hits == len(words):
        score += 12
    if words[0] in item['url'].lower():
        score += 2
    return score


def search_songs(query, limit=8):
    query = query.strip()
    if len(query) < 2:
        return []

    merged = []
    seen_urls = set()
    for finder in (search_chordtela, search_ultimate_guitar):
        try:
            for item in finder(query, limit=limit):
                if item['url'] in seen_urls:
                    continue
                seen_urls.add(item['url'])
                merged.append(item)
        except Exception:
            continue

    words = [w for w in query.lower().split() if len(w) > 2]
    if len(words) >= 2:
        filtered = [
            item for item in merged
            if sum(1 for w in words if w in item['url'].lower()) >= 2
        ]
        if filtered:
            merged = filtered

    merged.sort(key=lambda item: _relevance_score(query, item), reverse=True)
    return merged[:limit]