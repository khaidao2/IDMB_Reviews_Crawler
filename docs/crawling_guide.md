# Hướng dẫn Crawl và Quy trình Crawl

Dự án này bao gồm hai phần chính để thu thập dữ liệu từ IMDb:
1.  **Crawl thông tin phim**: Sử dụng GraphQL API của IMDb.
2.  **Crawl đánh giá (review)**: Sử dụng Selenium để giả lập trình duyệt và lấy dữ liệu động.

---

## 1. Môi trường và Cài đặt

Trước khi chạy, đảm bảo bạn đã cài đặt Python và các thư viện cần thiết.

### Cài đặt thư viện
Chạy lệnh sau để cài đặt các dependencies:
```bash
pip install -r requirements.txt
```
Các thư viện chính bao gồm:
- `requests`: Để gọi API GraphQL.
- `selenium`: Để điều khiển trình duyệt Chrome.
- `webdriver-manager`: Tự động quản lý Chrome Driver.
- `beautifulsoup4`: Phân tích cú pháp HTML.
- `pandas`: Xử lý và lưu dữ liệu CSV.

---

## 2. Quy trình Crawl Phim (Movie Crawler)

Script: `src/crawl_film.py`

### Cách hoạt động
- **Nguồn dữ liệu**: Sử dụng API GraphQL của IMDb (`AdvancedTitleSearch`).
- **Logic**:
    - Gửi request POST đến endpoint GraphQL với các tham số lọc: `titleTypeConstraint` (movie), `genreConstraint` (Drama), sắp xếp theo số lượng bình chọn (`USER_RATING_COUNT`).
    - Phân trang (Pagination) sử dụng cursor `after` được trả về từ response trước đó.

### Trích dẫn Code

**1. Cấu hình GraphQL Query (`src/crawl_film.py`):**
Sử dụng `operationName: AdvancedTitleSearch` để lấy dữ liệu.

```python
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
    # ... call requests.post ...
```

**2. Xử lý Phân trang (Pagination):**
Vòng lặp `while True` sẽ chạy liên tục, cập nhật `after` cursor sau mỗi lần request để lấy trang tiếp theo.

```python
    while True:
        page += 1
        log(f"Crawl movie page {page}")

        data = fetch_page(after)
        if data.get("_STOP"):
            break

        # ... process data ...

        page_info = search["pageInfo"]
        after = page_info.get("endCursor") # Lấy cursor cho trang sau
        save_state(after, page)

        if not page_info.get("hasNextPage"):
            break

        time.sleep(BASE_SLEEP)
```

### Cách chạy
```bash
python src/crawl_film.py
```

### Output
- File: `output/imdb_movies.csv`
- File trạng thái: `storage/state.json`

---

## 3. Quy trình Crawl Đánh giá (Review Crawler)

Script: `src/crawl_review.py` (Logic chính) và `src/main.py` (CLI entry point).

### Cách hoạt động
- **Nguồn dữ liệu**: Trang review của từng phim trên IMDb.
- **Công nghệ**: Selenium WebDriver (Chrome).
- **Luồng xử lý**:
    1.  `src/main.py` nhận tham số (ID hoặc URL) từ dòng lệnh.
    2.  Gọi hàm `start_crawl` trong `src/crawl_review.py`.
    3.  Khởi tạo WebDriver và truy cập URL.
    4.  Tự động cuộn trang (Infinite Scroll) để tải toàn bộ review.
    5.  Parse HTML bằng BeautifulSoup và lưu vào CSV.

### Trích dẫn Code (`src/crawl_review.py`)

**1. Khởi tạo WebDriver:**
```python
def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")
    # ...
    return driver
```

**2. Logic Cuộn trang (Scroll):**
```python
        # ---- scroll to load all reviews ----
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
```

**3. Phân tích HTML:**
```python
def parse_reviews(html: str, title_id: str):
    soup = BeautifulSoup(html, "html.parser")
    reviews = soup.select("article.user-review-item")

    for r in reviews:
        # ... extract data ...
        row = {
            "title_id": title_id,
            "author": author,
            # ...
        }
        append_csv(row)
```

### Cách chạy
Sử dụng CLI `src/main.py` để crawl theo ID hoặc URL bất kỳ:

```bash
# Crawl bằng ID
python src/main.py tt0499549

# Hoặc bằng URL
python src/main.py https://www.imdb.com/title/tt0499549/
```

### Output
- File: `imdb_reviews.csv` (lưu tại thư mục gốc).

---

## 4. Cấu trúc Project

- `src/`: Chứa mã nguồn chính.
    - `crawl_film.py`: Logic crawl thông tin phim (GraphQL).
    - `crawl_review.py`: Logic crawl review (Selenium), chứa các hàm xử lý chính.
    - `main.py`: Giao diện dòng lệnh (CLI) để chạy crawler review.
    - `storage/`: Chứa file trạng thái (`state.json`) và các file tạm.
- `output/`: Thư mục chứa kết quả crawl (CSV phim).
