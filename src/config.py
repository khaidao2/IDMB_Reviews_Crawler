from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

STORAGE_DIR = PROJECT_ROOT / "storage"
RAW_DIR = STORAGE_DIR / "raw"
JSON_CACHE_DIR = STORAGE_DIR / "json-cache"
LOG_DIR = STORAGE_DIR / "logs"

OUTPUT_DIR = PROJECT_ROOT / "output"
CSV_DIR = OUTPUT_DIR / "csv"
REPORT_DIR = OUTPUT_DIR / "reports"
