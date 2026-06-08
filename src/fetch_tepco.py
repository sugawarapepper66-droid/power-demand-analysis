"""でんき予報CSVデータ取得スクリプト"""

from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = PROJECT_ROOT / "data" / "raw"
URL_TEMPLATE = "https://www.tepco.co.jp/forecast/html/images/juyo-{year}.csv"
START_YEAR = 2021
END_YEAR = 2025


def download_year(year):
    url = URL_TEMPLATE.format(year=year)
    out_path = OUT_DIR / f"juyo-{year}.csv"
    if out_path.exists():
        print(f"[skip] {out_path.name} already exists")
        return
    print(f"[get ] {url}")
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    out_path.write_bytes(r.content)
    print(f"[save] {out_path.name} ({len(r.content):,} bytes)")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for year in range(START_YEAR, END_YEAR + 1):
        download_year(year)
    print("done")


if __name__ == "__main__":
    main()
