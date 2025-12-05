#!/usr/bin/env python3
"""
NDL SRU検索結果をRAWGraphs用に変換するスクリプト

入力: ndl_sru_grouped_result.csv
出力: ndl_sru_for_rawgraphs.csv

NDCラベル: ndc9_class91_hierarchical.csv（fetch_ndc_labels.pyで取得）

フィールド:
  - year: 出版年（1800-1867）
  - title: 作品名
  - ndc_code: NDCコード（番号のみ）
  - genre: NDCコード:ジャンル名（階層ラベル）
  - genre_major: 大分類のみ（詩歌、小説等）
  - location: 出版地（正規化済み）
  - creator_normalized: 上位著者（その他/不明）
"""

import csv
from collections import Counter
from pathlib import Path


def load_ndc_labels(csv_path: Path) -> dict[str, str]:
    """
    NDCラベルCSVを読み込んで辞書を返す

    Args:
        csv_path: ndc9_class91_hierarchical.csv のパス

    Returns:
        {NDCコード: 階層ラベル} の辞書
    """
    labels = {}
    if not csv_path.exists():
        print(f"警告: {csv_path} が見つかりません。fetch_ndc_labels.py を実行してください。")
        return labels

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            code = row['code']
            # 階層ラベルを使用
            labels[code] = row['label_hierarchical']

    return labels


def ndc_to_genre(ndc: str, ndc_labels: dict[str, str]) -> tuple[str, str, str]:
    """
    単一のNDCコードからジャンル情報を返す

    Returns:
        (ndc_code, genre, genre_major) のタプル
        - ndc_code: NDCコード（番号のみ）
        - genre: NDCコード:階層ラベル
        - genre_major: 大分類のみ
    """
    if not ndc:
        return ("", "不明", "不明")

    ndc = ndc.strip()
    matched_code = ""
    matched_label = ""

    # 完全一致を優先して検索
    if ndc in ndc_labels:
        matched_code = ndc
        matched_label = ndc_labels[ndc]
    else:
        # 前方一致で検索（より具体的なコードを先にチェック）
        for code in sorted(ndc_labels.keys(), key=len, reverse=True):
            if ndc.startswith(code):
                matched_code = code
                matched_label = ndc_labels[code]
                break

    if not matched_code:
        return (ndc, "その他", "その他")

    # 大分類を抽出（階層ラベルの最初の部分）
    genre_major = matched_label.split('/')[0] if matched_label else "その他"

    return (matched_code, f"{matched_code}:{matched_label}", genre_major)


def normalize_location(loc: str) -> str:
    """単一の出版地を正規化する"""
    if not loc:
        return "不明"

    loc = loc.strip()

    # 江戸系
    if any(x in loc for x in ['江戸', '東都', '東京']):
        return "江戸"
    # 京都系
    elif any(x in loc for x in ['京都', '皇都', '平安', '京']):
        return "京都"
    # 大阪系
    elif any(x in loc for x in ['大阪', '大坂', '浪華', '浪花', '坂陽']):
        return "大阪"
    elif '名古屋' in loc:
        return "名古屋"
    elif '長崎' in loc:
        return "長崎"
    elif '金沢' in loc:
        return "金沢"
    elif '出版地不明' in loc:
        return "不明"
    elif loc:
        return "その他"
    else:
        return "不明"


def split_multi_value(value: str, separator: str = ';') -> list[str]:
    """セミコロン区切りの複数値を分割してリストで返す"""
    if not value:
        return ['']
    return [v.strip() for v in value.split(separator)]


def extract_year(issued: str, min_year: int = 1800, max_year: int = 1867) -> int | None:
    """issued文字列から年を抽出する（範囲外はNone）"""
    if not issued:
        return None

    year_str = issued[:4]
    try:
        year = int(year_str)
        if min_year <= year <= max_year:
            return year
    except ValueError:
        pass

    return None


def parse_creator_name(creator: str) -> str:
    """単一の著者名から名前部分のみを抽出（生没年を除去）"""
    if not creator:
        return ""
    creator = creator.strip()
    parts = creator.split(',')
    if len(parts) >= 2:
        return f"{parts[0].strip()} {parts[1].strip()}"
    else:
        return creator.split('∥')[0].strip()


def get_top_creators(rows: list[dict], top_n: int = 15) -> set[str]:
    """上位N名の著者名セットを返す（複数著者も全てカウント）"""
    creator_count = Counter()

    for row in rows:
        creators_raw = row.get('creators_name', '')
        if creators_raw:
            # 全ての著者をカウント
            for creator in split_multi_value(creators_raw):
                name = parse_creator_name(creator)
                if name:
                    creator_count[name] += 1

    return set(name for name, _ in creator_count.most_common(top_n))


def normalize_creator(creator: str, top_creators: set[str]) -> str:
    """単一の著者名を正規化（上位著者以外は「その他」）"""
    if not creator:
        return "不明"

    name = parse_creator_name(creator)
    if not name:
        return "不明"

    if name in top_creators:
        return name
    else:
        return "その他"


def get_first_value(value: str, separator: str = ';') -> str:
    """セミコロン区切りの複数値から最初の値のみを取得"""
    if not value:
        return ''
    return value.split(separator)[0].strip()


def convert(input_path: str, output_path: str, ndc_labels_path: str, top_n_creators: int = 15):
    """メイン変換処理（複数値は最初の値のみ使用）"""

    # NDCラベルを読み込み
    ndc_labels = load_ndc_labels(Path(ndc_labels_path))
    print(f"NDCラベル: {len(ndc_labels)}件")

    # 入力ファイル読み込み
    with open(input_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"入力: {len(rows)}件")

    # 上位著者を抽出
    top_creators = get_top_creators(rows, top_n_creators)
    print(f"\n上位{top_n_creators}著者:")
    for c in sorted(top_creators):
        print(f"  - {c}")

    # 変換処理（複数値は最初の値のみ使用）
    output_rows = []
    skipped_count = 0

    for row in rows:
        # 各フィールドの最初の値を取得
        year = extract_year(get_first_value(row.get('issued', '')))
        if year is None:
            skipped_count += 1
            continue  # 年が取得できない行はスキップ

        # NDC情報を取得（コード、階層ラベル、大分類）
        ndc_code, genre, genre_major = ndc_to_genre(
            get_first_value(row.get('ndc_raw', '')), ndc_labels
        )

        output_rows.append({
            'year': year,
            'title': get_first_value(row.get('title_main', '')),
            'ndc_code': ndc_code,
            'genre': genre,
            'genre_major': genre_major,
            'location': normalize_location(get_first_value(row.get('publisher_location', ''))),
            'creator_normalized': normalize_creator(get_first_value(row.get('creators_name', '')), top_creators)
        })

    # 1800年を除外したデータ
    output_rows_filtered = [r for r in output_rows if r['year'] != 1800]
    count_1800 = len(output_rows) - len(output_rows_filtered)

    # 出力（全データ）
    fieldnames = ['year', 'title', 'ndc_code', 'genre', 'genre_major', 'location', 'creator_normalized']
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    # 出力（1800年除外版）
    output_path_filtered = output_path.replace('.csv', '_exclude1800.csv')
    with open(output_path_filtered, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows_filtered)

    print(f"\n出力: {len(output_rows)}件（年不明{skipped_count}件除外）")
    print(f"  - 全データ: {output_path}")
    print(f"  - 1800年除外: {output_path_filtered}（{count_1800}件除外、{len(output_rows_filtered)}件）")

    # 統計表示
    print("\n=== ジャンル大分類 ===")
    genre_major_count = Counter(r['genre_major'] for r in output_rows)
    for g, c in sorted(genre_major_count.items(), key=lambda x: -x[1]):
        print(f"  {c:4d}: {g}")

    print("\n=== ジャンル詳細分布 ===")
    genre_count = Counter(r['genre'] for r in output_rows)
    for g, c in sorted(genre_count.items(), key=lambda x: -x[1]):
        print(f"  {c:4d}: {g}")

    print("\n=== 出版地分布 ===")
    loc_count = Counter(r['location'] for r in output_rows)
    for l, c in sorted(loc_count.items(), key=lambda x: -x[1]):
        print(f"  {c:4d}: {l}")

    print("\n=== 著者分布 ===")
    creator_count = Counter(r['creator_normalized'] for r in output_rows)
    for cr, c in sorted(creator_count.items(), key=lambda x: -x[1]):
        print(f"  {c:4d}: {cr}")


if __name__ == '__main__':
    # パス設定
    base_dir = Path(__file__).parent
    input_file = base_dir / 'ndl_sru_grouped_result.csv'
    output_file = base_dir / 'ndl_sru_for_rawgraphs.csv'
    ndc_labels_file = base_dir / 'ndc9_class91_hierarchical.csv'

    convert(str(input_file), str(output_file), str(ndc_labels_file), top_n_creators=15)
