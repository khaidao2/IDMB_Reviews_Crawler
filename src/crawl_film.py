import requests
import time
import csv
import os
import json
from typing import Optional, Dict, List
from utils import log
from storage.storage import init_csv, MOVIE_FIELDS


IMDB_GRAPHQL_URL = "https://caching.graphql.imdb.com/"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/graphql+json, application/json",
    "Content-Type": "application/json",
    "Origin": "https://www.imdb.com",
    "Referer": "https://www.imdb.com/",
}

PERSISTED_QUERY_HASH = "9fc7c8867ff66c1e1aa0f39d0fd4869c64db97cddda14fea1c048ca4b568f06a"

OUTPUT_CSV = "output/imdb_movies.csv"
STATE_FILE = "storage/state.json"

PAGE_SIZE = 50
BASE_SLEEP = 0.5


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"after": None, "page": 0}


def save_state(after, page):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"after": after, "page": page}, f)


def fetch_page(after):
    payload = {
        "operationName": "AdvancedTitleSearch",
        "variables": {
            "first": PAGE_SIZE,
            "after": after,
            "genreConstraint": {"allGenreIds": ["Drama"]},
            "languageConstraint": {"allLanguages": ["en"]},
            "locale": "en-US",
            "sortBy": "USER_RATING_COUNT",
            "sortOrder": "DESC",
            "titleTypeConstraint": {"anyTitleTypeIds": ["movie"]}
        },
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": PERSISTED_QUERY_HASH
            }
        }
    }

    r = requests.post(IMDB_GRAPHQL_URL, headers=HEADERS, json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()

    if "errors" in data:
        msg = data["errors"][0]["message"]
        if "Cannot paginate beyond 10000 results" in msg:
            log("IMDb 10k limit reached → stop", "WARN")
            return {"_STOP": True}
        raise RuntimeError(data["errors"])

    return data


def fetch_and_append_all_movies():
    init_csv(OUTPUT_CSV, MOVIE_FIELDS)

    state = load_state()
    after = state["after"]
    page = state["page"]

    while True:
        page += 1
        log(f"Crawl movie page {page}")

        data = fetch_page(after)
        if data.get("_STOP"):
            break

        search = data["data"]["advancedTitleSearch"]
        edges = search["edges"]
        page_info = search["pageInfo"]

        rows = []
        for e in edges:
            t = e["node"]["title"]
            runtime = (t.get("runtime") or {}).get("seconds")

            rows.append({
                "page": page,
                "imdb_id": t["id"],
                "title": (t.get("titleText") or {}).get("text"),
                "year": (t.get("releaseYear") or {}).get("year"),
                "rating": (t.get("ratingsSummary") or {}).get("aggregateRating"),
                "rating_count": (t.get("ratingsSummary") or {}).get("voteCount"),
                "runtime_minutes": runtime // 60 if runtime else None,
                "certificate": (t.get("certificate") or {}).get("rating"),
                "genres": ", ".join(
                    g["genre"]["text"]
                    for g in ((t.get("titleGenres") or {}).get("genres") or [])
                ),
                "plot": ((t.get("plot") or {}).get("plotText") or {}).get("plainText"),
                "url": f"https://www.imdb.com/title/{t['id']}/"
            })

        with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=MOVIE_FIELDS)
            writer.writerows(rows)

        after = page_info.get("endCursor")
        save_state(after, page)

        if not page_info.get("hasNextPage"):
            break

        time.sleep(BASE_SLEEP)
