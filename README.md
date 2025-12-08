# DDセンターブリーフィング「データ駆動型人文学研究入門」チュートリアル資料

DDセンターブリーフィング「データ駆動型人文学研究入門」②データ分析と可視化のチュートリアル用データ・スクリプトです。

## 概要

本リポジトリは、江戸後期（1800-1867年）の日本文学資料を対象に、RAWGraphsおよびVoyant Toolsを用いたデータ可視化・テキスト分析を体験するためのチュートリアル資料を提供します。

## ディレクトリ構成

```
ddc-tutorial2025/
├── data/                          # データファイル
│   └── ndl_sru_grouped_result.csv      # NDL SRU検索結果（元データ）
├── notebooks/                     # Jupyter Notebooks（Google Colab対応）
│   ├── tutorial_01_rawgraphs/         # RAWGraphs用データ変換
│   │   ├── fetch_ndc_labels.ipynb         # NDCラベル取得
│   │   ├── convert_for_rawgraphs.ipynb    # データ変換
│   │   └── *.csv                          # 出力データ
│   ├── tutorial_03_palladio/          # Palladio用データ変換
│   │   └── tutorial_03_palladio.ipynb
│   └── tutorial_04_gephi/             # Gephi Lite用ネットワークデータ
│       └── tutorial_04_gephi.ipynb
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

### Palladio
- URL: https://hdlab.stanford.edu/palladio/
- 地図・ネットワーク・時系列の可視化

### Gephi Lite
- URL: https://gephi.org/gephi-lite/
- ネットワーク分析・可視化（Webブラウザで動作）

## ノートブックの使い方

各ノートブックは **Google Colab** で直接開くことができます。ノートブック冒頭の「Open in Colab」バッジをクリックしてください。

### tutorial_01_rawgraphs

| ノートブック | 説明 | Colab |
|-------------|------|-------|
| fetch_ndc_labels.ipynb | ジャパンサーチからNDCラベルを取得 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nakamura196/ddc-tutorial2025/blob/main/notebooks/tutorial_01_rawgraphs/fetch_ndc_labels.ipynb) |
| convert_for_rawgraphs.ipynb | NDL検索結果をRAWGraphs用に変換 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nakamura196/ddc-tutorial2025/blob/main/notebooks/tutorial_01_rawgraphs/convert_for_rawgraphs.ipynb) |

### tutorial_03_palladio

| ノートブック | 説明 | Colab |
|-------------|------|-------|
| tutorial_03_palladio.ipynb | Palladio用データ変換 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nakamura196/ddc-tutorial2025/blob/main/notebooks/tutorial_03_palladio/tutorial_03_palladio.ipynb) |

### tutorial_04_gephi

| ノートブック | 説明 | Colab |
|-------------|------|-------|
| tutorial_04_gephi.ipynb | Gephi Lite用ネットワークデータ作成 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nakamura196/ddc-tutorial2025/blob/main/notebooks/tutorial_04_gephi/tutorial_04_gephi.ipynb) |

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
