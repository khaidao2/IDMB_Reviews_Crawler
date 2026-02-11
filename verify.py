import pandas as pd

# ================== LOAD DATA ==================
df = pd.read_csv("imdb_avatar_reviews.csv")

print("===== BASIC INFO =====")
print(f"Total rows   : {len(df)}")
print(f"Total columns: {df.shape[1]}")
print()

# ================== DUPLICATE ALL COLUMNS ==================
# Duplicate = tất cả cột giống hệt nhau
dup_all_mask = df.duplicated(keep=False)
dup_all_rows = df[dup_all_mask]

print("===== DUPLICATE (ALL COLUMNS) =====")
print(f"Total duplicate rows: {dup_all_mask.sum()}")
print(f"Has duplicate       : {dup_all_mask.any()}")
print()

print("Sample duplicate rows:")
print(dup_all_rows.head())
print()

# ================== COUNT BY title_id ==================
if 'title_id' not in df.columns:
    raise ValueError("❌ Không tìm thấy cột 'title_id'")

count_by_title = (
    df.groupby('title_id')
      .size()
      .reset_index(name='count')
      .sort_values('count', ascending=False)
)

print("===== COUNT BY title_id (TOP 10) =====")
print(count_by_title.head(10))
print()

# ================== DUPLICATED title_id (COUNT > 1) ==================
dup_titles = count_by_title[count_by_title['count'] > 1]

print("===== title_id xuất hiện > 1 lần =====")
print(f"Total duplicated title_id: {len(dup_titles)}")
print(dup_titles.head())
print()

# ================== SAVE OUTPUT ==================
dup_all_rows.to_csv("duplicate_all_columns.csv", index=False)
count_by_title.to_csv("count_by_title_id.csv", index=False)

print("✅ Saved files:")
print("- duplicate_all_columns.csv")
print("- count_by_title_id.csv")
