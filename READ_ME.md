# 首都圏電力需要分析レポート

東京電力PowerGridが公開する電力需要実績データを用いて、
首都圏の電力消費パターンを分析・可視化したポートフォリオです。

## 🎯 このプロジェクトについて

電気主任技術者の業務観点から、データ分析・可視化を実施。
将来的にAI活用（需要予測・異常検知）まで発展させる予定です。

## 🛠 使用技術

- Python 3.12
- pandas
- matplotlib / seaborn
- Jupyter Notebook

## 📁 リポジトリ構成

├── data/          # データファイル（取得スクリプトで生成）
├── notebooks/     # 分析用 Jupyter Notebook
├── src/           # データ取得・前処理スクリプト
├── docs/images/   # 出力グラフ
└── README.md


## 🚀 実行方法

```bash
git clone <this-repo>
cd power-demand-analysis
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

📝 開発について
本プロジェクトは Claude（Anthropic）を学習・実装パートナーとして活用しながら、
電気主任技術者の業務知見を反映して開発しています。

👤 著者
電気主任技術者（第三種）／ Python・データ分析を学習中