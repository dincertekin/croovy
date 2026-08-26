import argparse
from crawler.fetcher import run_crawler
from indexer.setup_index import create_search_index

def main():
    parser = argparse.ArgumentParser(description="Croovy Database & Crawler Tools")
    subparsers = parser.add_subparsers(dest="command")

    # Setup index command
    subparsers.add_parser("init-index", help="Initialize RediSearch schema")

    # Crawl command
    crawl_parser = subparsers.add_parser("crawl", help="Start web crawler")
    crawl_parser.add_argument("-u", "--url", type=str, required=True, help="Seed URL")
    crawl_parser.add_argument("-m", "--max", type=int, default=50, help="Max pages to crawl")

    args = parser.parse_args()

    if args.command == "init-index":
        create_search_index()
    elif args.command == "crawl":
        run_crawler(args.url, max_pages=args.max)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
