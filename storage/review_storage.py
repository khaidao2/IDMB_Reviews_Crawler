import csv
from storage.storage import init_csv, REVIEW_FIELDS

REVIEW_CSV = "output/imdb_reviews.csv"


def append_reviews(reviews):
    init_csv(REVIEW_CSV, REVIEW_FIELDS)

    with open(REVIEW_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=REVIEW_FIELDS)
        writer.writerows(reviews)
