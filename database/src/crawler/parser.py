import re
from urllib.parse import urljoin, urlparse, urlunparse
from bs4 import BeautifulSoup

def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))

def is_valid_url(url: str) -> bool:
    pattern = re.compile(
        r'^(https?://)'
        r'(([A-Za-z0-9-]+\.)+[A-Za-z]{2,})'
        r'(/[A-Za-z0-9._~:/?#[\]@!$&\'()*+,;=%-]*)?$'
    )
    return bool(re.match(pattern, url))

def parse_page(html_text: str, base_url: str):
    soup = BeautifulSoup(html_text, 'html.parser')

    title = soup.title.string.strip() if soup.title and soup.title.string else "No Title"

    meta_data = {
        'description': '',
        'author': '',
        'keywords': '',
        'rating': 'adult',
        'robots': 'noindex, nofollow'
    }

    for meta in soup.find_all('meta'):
        name = meta.attrs.get('name', '').lower()
        content = meta.attrs.get('content', '')
        if name in meta_data:
            meta_data[name] = content

    content = " ".join(soup.stripped_strings)

    links = set()
    for anchor in soup.find_all('a', href=True):
        full_link = urljoin(base_url, anchor['href'])
        normalized = normalize_url(full_link)
        if is_valid_url(normalized):
            links.add(normalized)

    return {
        'title': title,
        'description': meta_data['description'],
        'author': meta_data['author'],
        'keywords': meta_data['keywords'],
        'rating': meta_data['rating'],
        'robots': meta_data['robots'],
        'content': content,
        'links': list(links)
    }
