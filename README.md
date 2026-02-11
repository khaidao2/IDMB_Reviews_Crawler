# IMDb Reviews Crawler

Dự án này cung cấp công cụ tự động thu thập dữ liệu (crawl) thông tin phim và đánh giá (review) từ trang IMDb.

## 🚀 Tính năng

-   **Crawl Phim (Movie Crawler)**: Sử dụng GraphQL API của IMDb để lấy danh sách phim theo tiêu chí (Drama, Movie, sắp xếp theo lượt bình chọn).
-   **Crawl Đánh giá (Review Crawler)**: Sử dụng Selenium để giả lập trình duyệt, tự động cuộn trang và lấy toàn bộ đánh giá của phim.
-   **Tự động hoá**: Hỗ trợ lưu trạng thái (state) để chạy tiếp khi bị ngắt quãng.

## 📋 Yêu cầu hệ thống

-   Python 3.8+
-   Google Chrome (phiên bản mới nhất)

## 🛠 Cài đặt

1.  Clone dự án về máy.
2.  Cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

## 📖 Hướng dẫn sử dụng

### 1. Thu thập thông tin phim

Chạy lệnh sau để bắt đầu crawl danh sách phim:

```bash
python src/crawl_film.py
```

-   Dữ liệu sẽ được lưu tại: `output/imdb_movies.csv`
-   Trạng thái crawl (trang hiện tại) được lưu tại: `storage/state.json`

### 2. Thu thập đánh giá (Review)

Để crawl review cho danh sách phim đã định nghĩa (ví dụ: các phần phim Avatar), chạy:

```bash
python src/main.py
```

-   Dữ liệu review sẽ được lưu tại: `imdb_avatar_reviews.csv`

Để crawl review cho một phim bất kỳ, bạn có thể sửa đổi `src/crawl_review.py` hoặc sử dụng các hàm trong đó.

## 📂 Cấu trúc dữ liệu đầu ra

Dữ liệu CSV bao gồm các trường chính:
-   `title_id`: ID phim trên IMDb (vd: tt0499549)
-   `rating`: Điểm đánh giá (0-10)
-   `summary`: Tiêu đề review
-   `text`: Nội dung review
-   `helpful`: Số người thấy review hữu ích
-   `created_at`: Ngày đăng

## 📚 Tài liệu chi tiết

Vui lòng xem [Hướng dẫn Crawl và Quy trình Crawl](docs/crawling_guide.md) để biết thêm về:
-   Cơ chế hoạt động chi tiết.
-   Phân tích code (GraphQL query, Selenium Selenium automation).
-   Cấu trúc source code.
