import argparse
import sys
from crawl_review import start_crawl

def main():
    parser = argparse.ArgumentParser(description="IMDb Review Crawler")
    parser.add_argument(
        "identifier",
        help="IMDb Movie ID (e.g., tt0499549) or Full URL (e.g., https://www.imdb.com/title/tt0499549/)"
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    
    print(f"Starting crawl for: {args.identifier}")
    start_crawl(args.identifier)

if __name__ == "__main__":
    main()
