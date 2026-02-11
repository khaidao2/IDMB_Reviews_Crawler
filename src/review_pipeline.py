import time
from crawl_review import crawl_reviews
from storage.review_storage import append_reviews
from utils import log


def crawl_all_reviews(title_id):
    after = None
    page = 0

    while True:
        page += 1
        log(f"Reviews {title_id} | page {page}")

        reviews, page_info = crawl_reviews(title_id, after=after)

        if reviews:
            append_reviews(reviews)

        if not page_info.get("hasNextPage"):
            break

        after = page_info.get("endCursor")
        time.sleep(0.5)
