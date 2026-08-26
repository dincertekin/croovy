import time
import requests
from crawler.parser import parse_page
from crawler.queue import RedisCrawlQueue

def run_crawler(seed_url: str, max_pages: int = 50, delay: float = 1.0):
    queue = RedisCrawlQueue()
    queue.push_url(seed_url)

    pages_crawled = 0

    while pages_crawled < max_pages:
        url = queue.pop_url()
        if not url:
            print("Queue is empty. Crawl complete.")
            break

        if not queue.mark_visited(url):
            continue

        print(f"[{pages_crawled + 1}/{max_pages}] Crawling: {url}")

        try:
            response = requests.get(url, timeout=5, headers={"User-Agent": "CroovyBot/1.0"})
            if response.status_code != 200 or 'text/html' not in response.headers.get('Content-Type', ''):
                continue

            parsed = parse_page(response.text, url)

            # Persist document
            queue.store_document(url, {
                "url": url,
                "title": parsed['title'],
                "description": parsed['description'],
                "author": parsed['author'],
                "keywords": parsed['keywords'],
                "rating": parsed['rating'],
                "robots": parsed['robots'],
                "content": parsed['content']
            })

            # Queue outlinks
            for link in parsed['links']:
                queue.push_url(link)

            pages_crawled += 1
            time.sleep(delay)

        except requests.exceptions.RequestException as error:
            print(f"Error fetching {url}: {error}")
