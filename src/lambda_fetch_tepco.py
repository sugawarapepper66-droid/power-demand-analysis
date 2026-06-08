"""AWS Lambda 関数：TEPCO でんき予報CSVを取得して S3 に保存する。

EventBridge から毎日起動され、その年の juyo-{year}.csv を取得して
S3 バケットの raw/ プレフィックスに保存（上書き）する。

- requests は Lambda 標準ランタイムに無いため urllib.request（標準ライブラリ）を使用
- boto3 は Lambda 標準搭載のため追加パッケージ不要
- バケット名は環境変数 BUCKET_NAME から受け取る（コードに直書きしない）
- 年初など今年版が未公開（404）の場合は前年版にフォールバックする

ローカル実行用の取得スクリプトは src/fetch_tepco.py（こちらは複数年を一括取得）。
"""

import os
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

import boto3

URL_TEMPLATE = "https://www.tepco.co.jp/forecast/html/images/juyo-{year}.csv"
BUCKET = os.environ["BUCKET_NAME"]

s3 = boto3.client("s3")


def fetch_csv(year):
    """指定年の CSV をダウンロードしてバイト列で返す。"""
    url = URL_TEMPLATE.format(year=year)
    with urllib.request.urlopen(url, timeout=30) as resp:
        return resp.read()


def lambda_handler(event, context):
    # 日本時間の「今年」を求める
    jst = timezone(timedelta(hours=9))
    year = datetime.now(jst).year

    # 今年版がまだ公開されていなければ（404）前年版にフォールバック
    try:
        data = fetch_csv(year)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            year -= 1
            data = fetch_csv(year)
        else:
            raise

    # S3 に保存（同じキーは上書き＝最新断面に更新）
    key = f"raw/juyo-{year}.csv"
    s3.put_object(Bucket=BUCKET, Key=key, Body=data)

    msg = f"saved s3://{BUCKET}/{key} ({len(data):,} bytes)"
    print(msg)
    return {"statusCode": 200, "body": msg}
