# Step 3 復習リスト

「首都圏電力需要分析」プロジェクト Step 3（Stage 1 可視化）で
ハンズオン形式に習得した概念のリファレンス。

---

## 1. matplotlib の 3 層モデル

```
┌─────────────────────────────────┐
│  figure（紙）                    │
│   ┌─────────────────────────┐  │
│   │  axes（描画領域）         │  │
│   │     ━━━━╱╲╱╲╱╲ plot     │  │
│   └─────────────────────────┘  │
└─────────────────────────────────┘
```

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 4))   # 紙 + 領域
ax.plot(x, y, linewidth=0.5)               # 線を引く
ax.set_title("タイトル")
ax.set_xlabel("X軸")
ax.set_ylabel("Y軸")
ax.grid(True, alpha=0.3)
plt.show()
```

- **`fig, ax = plt.subplots(...)`** はタプルのアンパック代入
- 同じ `ax` に `plot` を複数回呼ぶと**重ね描き**（自動で色違い）
- `figsize=(横, 縦)` はインチ単位

### よく使うメソッド

| メソッド | 用途 |
|---|---|
| `ax.plot(x, y)` | 折れ線 |
| `ax.scatter(x, y)` | 散布図 |
| `ax.bar(x, y)` | 棒グラフ |
| `ax.set_title()` | タイトル |
| `ax.set_xlabel()` / `set_ylabel()` | 軸ラベル |
| `ax.set_xticks(range(0, 24))` | 目盛りを明示指定 |
| `ax.legend(loc="upper right")` | 凡例 |
| `ax.grid(True, alpha=0.3)` | グリッド |
| `ax.annotate("text", xy=(x,y))` | 注釈 |

---

## 2. 日本語フォント対策

```python
plt.rcParams["font.family"] = "Meiryo"   # Windows 標準
# 候補を複数列挙したい場合
plt.rcParams["font.family"] = ["Meiryo", "MS Gothic", "Yu Gothic", "sans-serif"]
```

指定しないと日本語が**豆腐文字（□□□）**になる。`rcParams` は matplotlib のグローバル設定で、**ノート最上部に1回**書けば以降全グラフに反映される。

---

## 3. pandas datetime と `.dt` アクセサ

datetime型のSeriesからは**部品単位**で値を取り出せる：

```python
df["datetime"].dt.year         # 年
df["datetime"].dt.month        # 月
df["datetime"].dt.day          # 日
df["datetime"].dt.hour         # 時
df["datetime"].dt.dayofyear    # 1月1日からの経過日（1〜366）
df["datetime"].dt.dayofweek    # 曜日（月=0, 日=6）
df["datetime"].dt.date         # 日付のみ（時刻なし）
df["datetime"].dt.time         # 時刻のみ
```

**注意**：`dayofweek` は **月=0, 日=6**（ISO 8601 準拠）。日本のカレンダー感覚（日曜始まり）とは違う。

---

## 4. `.resample()` — 時系列ダウンサンプリング

`groupby` の時系列版。**時間軸インデックス**を前提に時間ビンで集計する：

```python
df_daily = (
    df_all
    .set_index("datetime")              # datetime をインデックスに
    .resample("D")["demand"].mean()     # 日ビンで平均
    .reset_index()                       # インデックスを通常列に戻す
)
```

### 集計頻度の指定

| 指定 | 意味 |
|---|---|
| `"h"` | 1時間 |
| `"D"` | 1日 |
| `"W"` | 1週 |
| `"ME"` | 月末 |
| `"YE"` | 年末 |
| `"5min"` | 5分 |

---

## 5. `pivot_table` — 縦持ち↔横持ち変換

groupby の結果が「縦長」になるのを、**行列形式**に並べ替える：

```python
heatmap_data = df_all.pivot_table(
    index="year",       # 行ラベル
    columns="month",    # 列ラベル
    values="demand",    # マスに入れる値
    aggfunc="mean",     # 集計関数
)
```

| 引数 | 用途 |
|---|---|
| `index` | 行ラベル |
| `columns` | 列ラベル |
| `values` | マスに集計する対象列 |
| `aggfunc` | `"mean"`, `"sum"`, `"max"`, `"size"`, `"count"` など |

→ 等価な groupby 版：`df.groupby(["year","month"])["demand"].mean().unstack()`

---

## 6. seaborn ヒートマップ

`matplotlib` のラッパで、行列の色塗りが1関数で書ける：

```python
import seaborn as sns

fig, ax = plt.subplots(figsize=(10, 4))
sns.heatmap(
    heatmap_data,
    annot=True,           # マスに数値表示
    fmt=".0f",            # 書式（小数0桁）
    cmap="YlOrRd",        # カラーマップ
    cbar_kws={"label": "需要 (万kW)"},
    ax=ax,
)
```

| 引数 | 用途 |
|---|---|
| `annot` | マスに数値を書くか |
| `fmt` | 数値書式（`.0f`=整数, `.1f`=1桁, `.0%`=%） |
| `cmap` | カラーマップ名 |
| `vmin` / `vmax` | カラーの値域を固定（複数図で揃えるとき） |
| `mask` | True のマスを非表示 |
| `square` | 正方形マスにする |
| `annot_kws` | 注釈文字の設定（`{"size": 7}` など） |

---

## 7. カラーマップ（cmap）の選び方

### 3 カテゴリ

| 系統 | 性質 | 代表例 | 用途 |
|---|---|---|---|
| **Sequential** | 単方向グラデ | `YlOrRd`, `Blues`, `viridis` | **大小がある量** |
| **Diverging** | 中央が白で両端に色 | `RdBu`, `coolwarm` | **±の偏差** |
| **Qualitative** | 区別できる別色 | `tab10`, `Set1` | **カテゴリラベル** |

### 命名規則（頭文字つなぎ）

| 略号 | 展開 | 色の流れ |
|---|---|---|
| `YlOrRd` | Yellow → Orange → Red | 黄→橙→赤 |
| `YlGnBu` | Yellow → Green → Blue | 黄→緑→青 |
| `RdBu` | Red ↔ Blue | 赤↔白↔青 |
| `OrRd` | Orange → Red | 橙→赤 |

- 末尾に `_r` を付けると**反転**（`YlOrRd_r` は赤→橙→黄）
- `viridis` は**知覚均等＋色覚配慮**で学術論文の定番
- 一覧確認：`plt.colormaps()`

---

## 8. ブールインデキシング — `df[条件]`

「**○×札を作って → 行を取り出す**」の2段構え：

```python
# ① ○×札（boolean Series）を作る
mask = df_all["year"] == 2022

# ② 札を df[ ] に渡して行を抽出
df_all[mask]
df_all[df_all["year"] == 2022]   # 1行で書いた版
```

### 複数条件

`and` / `or` ではなく **`&` / `|` / `~`** を使い、各条件は `()` で囲む：

```python
df_all[(df_all["year"] == 2022) & (df_all["month"] == 8)]   # AND
df_all[(df_all["year"] == 2022) | (df_all["month"] == 8)]   # OR
df_all[~(df_all["year"] == 2025)]                             # NOT
```

### マスクの便利な使い方

```python
mask.sum()          # True の数
mask.any()          # 1つでも True か
mask.all()          # 全部 True か
df_all[mask]        # True の行を抽出
df_all[~mask]       # False の行を抽出
df_all.loc[mask, "demand"]   # True の行の demand 列だけ
```

---

## 9. `idxmax` と `.loc` — 最大値の場所を取り出す

```python
s.max()        # 最大「値」
s.idxmax()     # 最大値の「インデックス」
```

組み合わせの定番パターン：

```python
peak_idx = df_all["demand"].idxmax()     # 最大値の場所
peak_row = df_all.loc[peak_idx]           # その行全体を取り出す
peak_row["datetime"]                      # 日時
peak_row["demand"]                        # 値
```

`.idxmin()` も同様。`argmax` / `argmin` は**位置**（0から始まる序数）を返すが、pandas では `idxmax` の方が一般的。

---

## 10. `.isin()` — 複数値で絞り込み

`==` は単一値、`.isin()` は**リスト全体とのOR比較**：

```python
df_all[df_all["month"].isin([6, 7, 8, 9])]    # 夏（6〜9月）
df_all[df_all["year"].isin([2022, 2023])]      # 2022年か2023年
```

否定したい時は `~`：

```python
df_all[~df_all["month"].isin([12, 1, 2])]      # 冬以外
```

---

## 11. 図の保存 — `fig.savefig()`

```python
fig.savefig(IMG_DIR / "01_xxx.png", dpi=120, bbox_inches="tight")
plt.show()    # ← 保存の後に呼ぶ
```

| 引数 | 用途 | 推奨値 |
|---|---|---|
| 第1引数 | 保存先 Path（拡張子で形式自動判別） | `.png` |
| `dpi` | 解像度 | **120**（Web）／ 300（印刷） |
| `bbox_inches` | 余白の扱い | **`"tight"`**（自動最小化） |
| `transparent` | 背景透過 | `False` |

### 形式の使い分け

| 拡張子 | 用途 |
|---|---|
| `.png` | ラスタ・標準（README向き） |
| `.svg` | ベクタ・拡大しても劣化しない |
| `.pdf` | 印刷向け |
| `.jpg` | 写真向き（グラフには非推奨） |

---

## 12. プロパティ vs メソッド（カッコの有無）

| 種類 | 呼び方 | カッコ | 例 |
|---|---|---|---|
| **プロパティ** | 値を取り出す | **なし** | `df.shape`, `s.dt.year`, `df.columns` |
| **メソッド** | 関数を呼ぶ | **あり** | `df.head()`, `s.dt.day_name()`, `df.rename()` |

### 見分け方

- **引数が要らず、ただ取り出すだけ** → プロパティ（カッコなし）
- **引数 or 動作が必要** → メソッド（カッコあり）

### `.dt` アクセサの典型例

```python
# プロパティ（カッコなし）
s.dt.year / s.dt.month / s.dt.day / s.dt.hour
s.dt.date / s.dt.time / s.dt.dayofweek / s.dt.dayofyear

# メソッド（カッコあり）
s.dt.day_name() / s.dt.month_name()
s.dt.strftime("%Y-%m-%d")
s.dt.normalize() / s.dt.to_period("M")
```

### 典型エラー

```python
s.dt.date()   # ❌ TypeError: 'Series' object is not callable
                # → date はプロパティ、カッコ不要
```

---

## 13. 設計原則 — DRY と「3 strikes ルール」

| 重複回数 | 行動 |
|---|---|
| 1回 | そのまま書く |
| 2回 | 重複を許容する |
| 3回 | **関数 or ループに切り出す** |

### DRY が必要な場面

- 本番アプリ：**バグ修正の一貫性、仕様変更追従、監査性**
- 複数人開発：**1つの真実（Single Source of Truth）**
- 頻繁に変更されるロジック

### 重複を許す場面

- 学習用 notebook、個人スクリプト
- **意味が違うが形が同じ**コード（誤った抽象化はかえって悪手）
- テストコード（DAMP 原則：Descriptive And Meaningful Phrases）

> **"Duplication is far cheaper than the wrong abstraction."**
> — Sandi Metz

---

## 14. Python の `=` — 「定義」ではなく「貼り付け」

`=` は**右辺を評価して左辺に名札を貼る**操作。両方向の同期ではない。

```python
a = [1, 2, 3]
b = a              # 同じリストに別の付箋
b.append(4)
print(a)           # → [1, 2, 3, 4]  （a も変わる！）
```

### DataFrame の列ラベル書き換え

```python
# ✅ 正解：右辺のリストを左辺の columns 属性に書き込む
df.columns = ["A", "B", "C"]

# ❌ こうしても DataFrame の columns は変わらない
cols = df.columns
cols = ["A", "B", "C"]   # cols の付箋を貼り替えただけ
```

### コピーしたい時

```python
b = a.copy()     # 浅いコピー
import copy
b = copy.deepcopy(a)   # 深いコピー（入れ子も独立）
```

---

## 15. matplotlib の色・マーカー

### 色の指定方法

```python
ax.plot(x, y, color="red")           # 名前
ax.plot(x, y, color="#E74C3C")       # 16進
ax.plot(x, y, color=(0.9, 0.3, 0.2)) # RGB タプル（0-1）
ax.plot(x, y, color="C0")            # デフォルトサイクル0番目
```

### マーカー記号

| 記号 | 形 |
|---|---|
| `"o"` | 円 |
| `"s"` | 四角 |
| `"^"` / `"v"` | 上向き / 下向き三角 |
| `"D"` | 菱形 |
| `"*"` | 星 |
| `"x"` / `"+"` | バツ / プラス |
| `"."` | 小さい点 |

### 線スタイル

| 指定 | スタイル |
|---|---|
| `"-"` | 実線 |
| `"--"` | 破線 |
| `":"` | 点線 |
| `"-."` | 一点鎖線 |
| `linewidth=0.5` | 太さ |
| `alpha=0.3` | 透明度 |

---

## 16. Markdown — README の画像埋め込み

```markdown
![代替テキスト](docs/images/01_xxx.png)

[リンクテキスト](docs/step2_review.md)

# 見出し1
## 見出し2
### 見出し3

- 箇条書き
1. 番号付き

`インラインコード`

```python
# コードブロック（言語名で構文ハイライト）
```
```

VS Code でプレビュー：`Ctrl+Shift+V`

---

## 17. PEP 8 — 空白の慣例

二項演算子の前後に**空白を入れる**：

```python
# ✅ PEP 8 準拠
a = b + c
path = PROJECT_ROOT / "data" / "raw"

# ⚠️ 非準拠（動くが慣例外）
a = b+c
path = PROJECT_ROOT/"data"/"raw"
```

`Path` の `/` は内部的に `__truediv__`（割り算演算子）の流用なので、`+` や `*` と同じ扱い。

### 自動整形ツール

| ツール | 機能 |
|---|---|
| **black** | 強制的に PEP 8 整形 |
| **ruff** | 高速。linter + formatter 兼用 |
| **autopep8** | 古典的整形ツール |

→ VS Code で「保存時自動整形」を設定するのが現代的。

---

## 18. グラフ × 電気主任目線のストーリー

各グラフに業務知見を載せると、面接で**語り種**になる：

| グラフ | 読み筋 |
|---|---|
| 全期間時系列 | **設備容量は夏ピーク基準**。春秋の谷は**点検適期** |
| 年次比較（経過日重ね） | GW・お盆の凹み＝**産業需要のウェイト** |
| 月平均ヒートマップ | 夏ピーク**上昇トレンド**、冬ピーク**低下傾向**＝非対称 |
| 時間帯×曜日 | 平日昼＝**産業需要**、夜＝**家庭需要**、深夜＝**ベース需要** |
| ピーク日24h | 夏=午後単峰（PV適合）、冬=朝＋夕方ピーク（PV非適合） |

### 面接の語り種フレーズ

> 「夏ピークは増加・冬ピークは安定〜微減という**非対称な傾向**。再エネ・蓄電池・DRの議論はこの非対称性を前提にする必要がある」

---

## 19. Git — 可視化成果物のコミット

```powershell
# 状況確認
git status
git diff --stat

# 個別 add（git add . は事故の元）
git add notebooks/01_load_check.ipynb
git add READ_ME.md
git add requirements.txt
git add docs/

# コミット
git commit -m "feat: add Stage 1 visualization charts (3-A to 3-E)"

# 履歴確認
git log --oneline -10
git log --oneline --graph -10
```

### よくあるタイポ

| 正解 | 間違いがち |
|---|---|
| `--oneline` | `--online` |
| `--graph` | `--graf` |
| `--cached` / `--staged` | `--cache` |

### LF/CRLF 警告

```
warning: in the working copy of 'xxx.ipynb', LF will be replaced by CRLF
```

→ Windows と Unix の改行コード違いによる**自動変換通知**。**無視してOK**。

---

## 20. 今後発展できる領域（Step 4 以降）

- **季節分解**：`statsmodels.tsa.seasonal_decompose` でトレンド／季節／残差を分離
- **異常検知**：Isolation Forest, Z-score, Prophet の anomaly
- **需要予測**：Prophet, ARIMA, LSTM
- **可視化拡張**：Plotly（インタラクティブ）、Streamlit（Webダッシュボード）
- **コード品質**：black / ruff（自動整形）、pytest（テスト）、型ヒント
- **再現性**：nbstripout（notebook 出力削除）、dvc（データバージョン管理）
- **CI/CD**：GitHub Actions で自動テスト・自動デプロイ
