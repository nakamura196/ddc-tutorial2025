# DDセンターブリーフィング「データ駆動型人文学研究入門」チュートリアル資料

DDセンターブリーフィング「データ駆動型人文学研究入門」②データ分析と可視化のチュートリアル用データ・スクリプトです。

## 概要

本リポジトリは、江戸後期（1800-1867年）の日本文学資料を対象に、RAWGraphsおよびVoyant Toolsを用いたデータ可視化・テキスト分析を体験するためのチュートリアル資料を提供します。

## ディレクトリ構成

```
ddc-tutorial2025/
├── data/                          # データファイル
│   ├── ndl_sru_grouped_result.csv      # NDL SRU検索結果（元データ）
│   ├── ndl_sru_for_rawgraphs.csv       # RAWGraphs用に正規化したデータ
│   ├── ndl_sru_for_rawgraphs_exclude1800.csv  # 年代不明(1800)を除外したデータ
│   └── ndc9_class91_hierarchical.csv   # NDC9 91類の階層構造
├── scripts/                       # スクリプト
│   ├── convert_for_rawgraphs.py        # データ変換スクリプト
│   └── fetch_ndc_labels.py             # NDCラベル取得スクリプト
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

## データについて

### ndl_sru_for_rawgraphs.csv

RAWGraphsでの可視化用に正規化したデータです。

| フィールド | 説明 | 例 |
|-----------|------|-----|
| year | 出版年（西暦） | 1842 |
| title | 作品名 | 南総里見八犬伝 |
| ndc_code | NDCコード | 913.57 |
| genre | ジャンル名（詳細） | 小説．物語/草双紙（合巻） |
| genre_major | ジャンル名（大分類） | 小説．物語 |
| location | 出版地（正規化済み） | 江戸 |
| creator_normalized | 著者名（正規化済み） | 曲亭 馬琴 |

### データソース

- **国立国会図書館サーチ (NDL Search)**: SRU API を使用して検索・取得
- **ジャパンサーチ SPARQL**: NDC（日本十進分類法）ラベルの取得

## 使用ツール

### RAWGraphs
- URL: https://app.rawgraphs.io/
- 日本語版: https://rawgraphs-ja.vercel.app/
- 構造化データの可視化（棒グラフ、Circle Packing、Alluvial Diagramなど）

### Voyant Tools
- URL: https://voyant-tools.org/
- テキスト分析（語頻度、共起、トレンドなど）

## スクリプトの使い方

### データ変換

```bash
python3 scripts/convert_for_rawgraphs.py
```

元データ（`ndl_sru_grouped_result.csv`）をRAWGraphs用に変換します。

### NDCラベル取得

```bash
# 91類（日本文学）全体を取得
python3 scripts/fetch_ndc_labels.py

# 特定の類を取得
python3 scripts/fetch_ndc_labels.py 911
```

ジャパンサーチのSPARQLエンドポイントからNDC9のラベルを取得します。

## 参考リンク

- [国立国会図書館サーチ](https://ndlsearch.ndl.go.jp/)
- [ジャパンサーチ](https://jpsearch.go.jp/)
- [RAWGraphs](https://www.rawgraphs.io/)
- [Voyant Tools](https://voyant-tools.org/)
- [日本十進分類法（NDC）](https://www.jla.or.jp/ndc/)

## ライセンス

本リポジトリのコードは MIT License の下で公開されています。

データについては、それぞれのデータソースの利用規約に従ってください。

## 著者

- 中村覚（東京大学）
