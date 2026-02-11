import csv
import os

MOVIE_FIELDS = [
    "page",
    "imdb_id",
    "title",
    "year",
    "rating",
    "rating_count",
    "runtime_minutes",
    "certificate",
    "genres",
    "plot",
    "url"
]

REVIEW_FIELDS = [
    "title_id",
    "review_id",
    "author",
    "rating",
    "summary",
    "text",
    "helpful",
    "created_at"
]


def init_csv(path, fields):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
