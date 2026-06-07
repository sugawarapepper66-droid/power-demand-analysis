# Step 2 復習リスト

「首都圏電力需要分析」プロジェクト Step 2（TEPCO電力需要データ取得）で
ハンズオン形式に習得した概念のリファレンス。

---

## 1. Python 基本構文

- **関数定義**：`def 関数名(引数):` の形、コロン + インデント（4スペース）
- **return**：値を返す。`return` だけ書くと None を返して関数を抜ける（早期 return）
- **f-string**：`f"..."` の中で `{式}` が評価される。`{x:,}` で3桁区切り、`{x:.2f}` で小数2桁
- **if 文**：`if 条件:`、コロン必須
- **for ループ**：`for 変数 in イテラブル:`
- **range(start, stop)**：start を含み stop を**含まない**（半開区間）→ `range(2021, 2026)` は 2021〜2025
- **リスト内包表記**：`[f(x) for x in xs]` は `for` ループ + `append` の短縮版
- **docstring**：`"""..."""` を関数の直下に書くと公式の説明文として扱われる（`help()` で表示）
- **変数は名札**：`df = df.method()` は「名札を新しい結果に貼り替え」（再代入）

---

## 2. ライブラリの3層構造

| 層 | 例 | 準備 |
|---|---|---|
| 組み込み | `print`, `len`, `range`, `type`, `int` | 何も不要 |
| 標準ライブラリ | `Path` (pathlib), `datetime`, `json`, `os` | `import` のみ |
| 外部ライブラリ | `pd.read_csv`, `requests.get` | `pip install` + `import` |

慣例の短縮名：`pandas as pd`、`numpy as np`、`matplotlib.pyplot as plt`、`seaborn as sns`

---

## 3. pathlib (Path)

```python
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent  # スクリプトから2つ上
p = PROJECT_ROOT / "data" / "raw" / "juyo-2024.csv"    # / で結合

p.exists()                                  # bool: ファイル存在チェック
p.mkdir(parents=True, exist_ok=True)        # ディレクトリ作成
p.write_bytes(b"...")                       # バイナリ書き込み
p.write_text("...", encoding="utf-8")       # テキスト書き込み
p.name                                      # ファイル名のみ
p.parent                                    # 親ディレクトリ
```

---

## 4. requests（HTTP通信）

```python
import requests

r = requests.get(url, timeout=30)   # timeout は必ず指定
r.status_code                        # 200, 404, 500 など
r.headers.get("Content-Type")
r.content                            # bytes（生バイト）
r.text                               # str（自動デコード後）
r.raise_for_status()                 # 4xx, 5xx で例外を投げる
```

### HTTPステータスコード

- 2xx：成功（200 OK）
- 3xx：リダイレクト
- 4xx：クライアント側の間違い（404 Not Found, 403 Forbidden）
- 5xx：サーバ側エラー（500, 503）

---

## 5. pandas DataFrame 基本

```python
import pandas as pd

df = pd.read_csv(path, encoding="shift_jis", skiprows=2)

df.shape         # (行数, 列数)
df.columns       # 列名一覧
df.dtypes        # 各列の型
df.info()        # 総合情報（型・欠損・メモリ）
df.head(n)       # 先頭 n 行（デフォルト5）
df.tail(n)       # 末尾 n 行
```

### 列の操作

```python
df["new_col"] = ...                              # 列追加・上書き（破壊的）
df = df.rename(columns={"old": "new"})           # rename は新表を返す（再代入必要）
df.rename(columns={"old": "new"}, errors="raise")  # キー不一致を例外化
```

### 列選択

| 書き方 | 返り値の型 |
|---|---|
| `df["col"]` | **Series**（1列） |
| `df[["a", "b"]]` | **DataFrame**（複数列） |
| `df[df["x"] > 5]` | **DataFrame**（行フィルタ） |
| `df.loc[ラベル, 列]` | 名前で指定 |
| `df.iloc[行番号, 列番号]` | 位置で指定 |

---

## 6. pandas 日時変換

```python
df["datetime"] = pd.to_datetime(
    df["DATE"] + " " + df["TIME"],
    format="%Y/%m/%d %H:%M",
)
```

### format 記号

| 記号 | 意味 |
|---|---|
| %Y | 4桁年 |
| %m | 月（01-12） |
| %d | 日 |
| %H | 時（00-23） |
| %M | 分 |
| %S | 秒 |

`format` は省略可能だが、明示すると速度・正確性とも有利。

---

## 7. pandas 連結と集計

```python
# 縦に連結
df_all = pd.concat([df1, df2, df3], ignore_index=True)

# グループ化集計
summary = (
    df_all.groupby("year")
    .agg(
        rows=("demand", "size"),
        n_missing=("demand", lambda s: s.isna().sum()),
        mean_demand=("demand", "mean"),
        max_demand=("demand", "max"),
    )
    .reset_index()
)
```

### 集計関数（文字列指定）

`"size"`, `"count"`, `"sum"`, `"mean"`, `"min"`, `"max"`, `"std"`, `"median"`

カスタム集計は **lambda 式**：`lambda s: s.isna().sum()`

---

## 8. メソッドチェーン

`()` で囲むと複数行に分けて書ける：

```python
result = (
    df
    .groupby("year")
    .agg(...)
    .reset_index()
    .sort_values("rows")
)
```

---

## 9. 関数 vs メソッド

| 種類 | 形式 | 例 |
|---|---|---|
| 組み込み関数 | `func(arg)` | `print()`, `len()` |
| モジュール関数 | `module.func(arg)` | `pd.read_csv()`, `requests.get()` |
| メソッド | `obj.method(arg)` | `df.head()`, `path.exists()` |

メソッドの正体：**クラスの中で定義された関数**。第1引数 `self` にドット前の値が自動で入る。

---

## 10. Jupyter Notebook

- 中身：JSON 形式（セルの配列）
- セル種類：**Code** / **Markdown**
- カーネル = Python プロセス。**メモリに変数が保持される**
- セルは順序自由に実行できる（実行順 ≠ 表示順）
- **困ったらカーネル再起動** + 上から実行

### 状態表示

| 表示 | 意味 |
|---|---|
| `[ ]` | 未実行 |
| `[*]` | 実行中 |
| `[N]` | N 回目に実行完了 |

### キー操作

- **Shift + Enter**：実行 → 次のセルに進む
- **Ctrl + Enter**：実行 → 同じセルに留まる
- **B**：下に新セル
- **M**：Markdown セルに変換
- **Y**：Code セルに戻す

---

## 11. Git 基礎（3層モデル）

```
ワーキングツリー → ステージング → リポジトリ
   (作業中)        (撮影候補)      (確定履歴)
                ↑              ↑
              git add       git commit
```

### よく使うコマンド

```powershell
git status                      # 現状確認
git diff                        # 未ステージの差分
git diff --staged               # ステージ済みの差分
git add ファイル名              # ステージング（具体名で）
git commit -m "メッセージ"      # コミット
git log --oneline -10           # 直近10件の履歴
git log --oneline --graph       # グラフ付き履歴
```

---

## 12. Git タイムトラベル

| コマンド | 用途 |
|---|---|
| `git show <commit>` | そのコミットの内容（diff）を見る |
| `git show <commit>:<file>` | そのコミット時点のファイル内容 |
| `git diff <commit>` | 現在との差分 |
| `git checkout <commit>` | その時点に移動（detached HEAD） |
| `git checkout master` | 元に戻る |
| `git restore --source=<commit> <file>` | 特定ファイルだけ過去版に |
| `git revert <commit>` | 取り消しコミットを新規作成（安全） |
| `git reset --soft HEAD~1` | 直近コミットだけ消す（編集残る） |
| `git reset --hard <commit>` | 履歴・編集ごと消す ⚠️ 危険 |

---

## 13. コミットメッセージ規約（Conventional Commits）

形式：`type: 内容`

| type | 用途 |
|---|---|
| feat | 新機能 |
| fix | バグ修正 |
| refactor | 動作を変えずに構造改善 |
| docs | ドキュメント |
| chore | 雑務（設定変更、依存更新） |
| test | テスト関連 |

ルール：
- 動詞は**命令形**（`add`, `fix`、`added` ではない）
- 1行目は**50文字以内**
- 本文は2行目以降に空行を挟んで書く

---

## 14. .gitignore の glob パターン

| パターン | マッチ | 非マッチ |
|---|---|---|
| `*.csv` | あらゆる .csv | （なし） |
| `data/*.csv` | `data/foo.csv` | **`data/raw/foo.csv`** |
| `data/**/*.csv` | `data/foo.csv`, `data/raw/foo.csv`, さらに深い階層も | （より広範囲） |
| `!data/sample.csv` | 例外的に追跡する | （否定パターン） |

サブディレクトリも含めたいなら `**` を使う。

---

## 15. エラーメッセージの読み方

```
NameError                Traceback (most recent call last)
File "...", line 19, in main
    download_year(2024)             ← 呼び出し元
File "...", line 10, in download_year
    url = URL_TEMPLATE.format(year=year)   ← エラー発生箇所
                                   ^^^^     ← 問題の箇所
NameError: name 'year' is not defined      ← 真因（一番下）
```

- **下から読む**（一番下が真因）
- `---->` の行が問題のコード
- `^^^^` がトリガーの式

### 典型エラー

| エラー | 主な原因 |
|---|---|
| NameError | 変数未定義（typo、import 忘れ、スコープ外） |
| TypeError | 型不一致（bytes に数値フォーマット等） |
| FileNotFoundError | パスや拡張子の間違い |
| SyntaxError | コロン抜け、カッコ未閉じ |
| ValueError | 値はあるが内容が無効（format 不一致など） |
| KeyError | dict/DataFrame の存在しないキー |

---

## 16. デバッグ：典型バグ

- **全角・半角の混在**：`(` と `（`、`kw` と `kＷ` は別文字
- **関数名と引数名のタイポ**：F2 (Rename Symbol) で一括置換
- **ループ変数を渡し忘れる**：`for y in years: f(2024)` のように固定値ハードコード
- **カーネルの stale state**：再起動 + 上から実行
- **pandas rename は不一致でも無視**：`errors="raise"` で明示
- **f-string の `{}` 外に式を書いてしまう**：`(len{x})` ではなく `({len(x)})`

---

## 17. 設計原則

| 原則 | 例 |
|---|---|
| **マジックナンバー回避** | `2021` → `START_YEAR = 2021` |
| **Fail Fast** | `raise_for_status()` で失敗を早く検出 |
| **早期 return** | ネストを浅く保つ |
| **関心の分離** | 取得（`src/`）と分析（`notebooks/`）を別ファイルに |
| **再実行に強い** | `if exists(): return` で重複処理を避ける |
| **読みやすさ優先** | 1行で書けても複数行に分けるべき場面がある |

---

## 18. 命名規則（変数名）

- **複数形の `s`**：`years`, `dfs`, `files`（リストや複数を示す）
- **単数 / 複数のペア**：`for year in years:`、`for df in dfs:` は読みやすい
- **業界の慣例短縮**：`df`（DataFrame）、`r`（Response）、`p`（Path）
- **避けたい名前**：`list`, `type`, `sum`, `id`, `input`, `open`（組み込みを上書きしてしまう）

---

## 19. 今後発展できる領域

- pandas: `.resample()`, `.rolling()`, ピボットテーブル
- matplotlib / seaborn の可視化
- 単体テスト（pytest）
- 型ヒント（`def f(year: int) -> Path`）
- フォーマッタ（black, ruff）
- pre-commit hooks
- Streamlit でダッシュボード化
