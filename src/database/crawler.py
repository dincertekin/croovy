import argparse
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import redis
import time

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
visited_urls = set()

def normalize_url(url):
    parsed_url = urlparse(url)
    return urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))

def is_valid_url(url):
    url_pattern = re.compile(
        r'^(https?://)'  # http:// or https://
        r'(([A-Za-z0-9-]+\.)+[A-Za-z]{2,})'  # Domain name
        r'(/[A-Za-z0-9._~:/?#[\]@!$&\'()*+,;=%-]*)?$'  # Path
    )
    return re.match(url_pattern, url) is not None

def extract_metadata(soup):
    page_title = soup.title.string if soup.title else "No Title"
    page_description = None
    page_keywords = None
    page_author = None
    page_rating = "adult"  # Default value
    page_robots = "noindex, nofollow"  # Default value
    
    for meta_tag in soup.find_all('meta'):
        if 'name' in meta_tag.attrs:
            if meta_tag.attrs['name'].lower() == 'description':
                page_description = meta_tag.attrs.get('content', '')
            elif meta_tag.attrs['name'].lower() == 'keywords':
                page_keywords = meta_tag.attrs.get('content', '')
            elif meta_tag.attrs['name'].lower() == 'author':
                page_author = meta_tag.attrs.get('content', '')
            elif meta_tag.attrs['name'].lower() == 'rating':
                page_rating = meta_tag.attrs.get('content', page_rating)
            elif meta_tag.attrs['name'].lower() == 'robots':
                page_robots = meta_tag.attrs.get('content', page_robots)

    return page_title, page_description, page_keywords, page_author, page_rating, page_robots

def crawl_url(url):
    if url in visited_urls:
        return

    visited_urls.add(url)

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        page_title, page_description, page_keywords, page_author, page_rating, page_robots = extract_metadata(soup)
        
        page_title = page_title or "No Title"
        page_description = page_description or ""
        page_keywords = page_keywords or ""
        page_author = page_author or ""
        
        page_content = " ".join(soup.stripped_strings)
        page_content = page_content or ""

        normalized_url = normalize_url(url)

        if not redis_client.exists(normalized_url):
            redis_client.json().set(normalized_url, "$", {
                "url": url,
                "title": page_title,
                "description": page_description,
                "author": page_author,
                "keywords": page_keywords,
                "rating": page_rating,
                "robots": page_robots,
                "content": page_content
            })
            print(f"Indexed: {url}")
        else:
            print(f"Already indexed: {url}")

        found_links = set()
        for anchor_tag in soup.find_all('a', href=True):
            full_link = urljoin(url, anchor_tag['href'])
            normalized_link = normalize_url(full_link)
            if is_valid_url(normalized_link) and normalized_link not in visited_urls:
                found_links.add(normalized_link)

        for link in found_links:
            crawl_url(link)

        print(f"Found {len(found_links)} links.")
        time.sleep(1)

    except requests.exceptions.RequestException as error:
        print(f"Error crawling {url}: {error}")

parser = argparse.ArgumentParser(description='A simple web crawler.')
parser.add_argument('-u', '--url', type=str, required=True, help='The URL to crawl.')

args = parser.parse_args()

crawl_url(args.url)
