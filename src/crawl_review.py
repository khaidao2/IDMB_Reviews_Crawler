import time
import csv
import os
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager


# ================= CONFIG =================
IMDB_REVIEW_URL = "https://www.imdb.com/title/tt0499549/reviews/?sort=submission_date,desc"
OUTPUT_CSV = "imdb_avatar_reviews.csv"

SEE_ALL_XPATH = '//*[@id="__next"]/main/div/section/div/section/div/div[1]/section[1]/div[3]/div/span[2]/button/span'


# ================= SETUP DRIVER =================
def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    return driver


# ================= APPEND CSV =================
def append_csv(row: dict):
    df = pd.DataFrame([row])

    if not os.path.exists(OUTPUT_CSV):
        df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    else:
        df.to_csv(
            OUTPUT_CSV,
            mode="a",
            header=False,
            index=False,
            encoding="utf-8-sig"
        )


# ================= PARSE REVIEW =================
def parse_reviews(html: str):
    soup = BeautifulSoup(html, "html.parser")
    reviews = soup.select("article.user-review-item")

    print(f"FOUND {len(reviews)} reviews")

    for r in reviews:
        try:
            title_id = "tt0499549"

            author = r.select_one('[data-testid="author-link"]')
            author = author.text.strip() if author else None

            rating = r.select_one(".ipc-rating-star--rating")
            rating = rating.text.strip() if rating else None

            summary = r.select_one('[data-testid="review-summary"] h3')
            summary = summary.text.strip() if summary else None

            text = r.select_one(".ipc-html-content-inner-div")
            text = text.text.strip() if text else None

            helpful = r.select_one(".ipc-voting__label__count--up")
            helpful = helpful.text.strip() if helpful else "0"

            created_at = r.select_one(".review-date")
            created_at = created_at.text.strip() if created_at else None

            row = {
                "title_id": title_id,
                "author": author,
                "rating": rating,
                "summary": summary,
                "text": text,
                "helpful": helpful,
                "created_at": created_at,
                "crawled_at": datetime.utcnow().isoformat()
            }

            append_csv(row)
            print(f"APPEND | author={author} | rating={rating}")

        except Exception as e:
            print("PARSE ERROR:", e)


# ================= MAIN =================
def crawl():
    driver = init_driver()
    driver.get(IMDB_REVIEW_URL)

    wait = WebDriverWait(driver, 20)

    # ---- wait page load ----
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "article.user-review-item"))
    )

    time.sleep(2)

    # ---- click SEE ALL ----
    try:
        see_all_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, SEE_ALL_XPATH))
        )
        driver.execute_script("arguments[0].click();", see_all_btn)
        print("CLICKED SEE ALL")
        time.sleep(3)
    except Exception:
        print("NO SEE ALL BUTTON (already expanded?)")

    # ---- scroll to load all reviews ----
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    print("SCROLL DONE")

    # ---- parse html ----
    html = driver.page_source
    parse_reviews(html)

    driver.quit()
    print("DONE")


if __name__ == "__main__":
    crawl()
