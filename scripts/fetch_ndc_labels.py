#!/usr/bin/env python3
"""
ジャパンサーチ SPARQL エンドポイントから NDC9 ラベルを取得するスクリプト

データソース: https://jpsearch.go.jp/rdf/sparql/
NDC URI形式: http://jla.or.jp/data/ndc9#{code}

出力: ndc9_class91_hierarchical.csv
  - code: NDCコード
  - label_ja: 日本語ラベル
  - label_hierarchical: 階層ラベル（上位分類を含む）

使用例:
    python fetch_ndc_labels.py          # 91類（日本文学）を取得
    python fetch_ndc_labels.py 8        # 8類（言語）を取得
"""

import csv
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path


SPARQL_ENDPOINT = "https://jpsearch.go.jp/rdf/sparql/"


def fetch_ndc_hierarchical(class_prefix: str = "91") -> list[dict]:
    """
    SPARQLで階層情報付きのNDCラベルを一括取得

    Args:
        class_prefix: NDCクラスの接頭辞（例: "91", "8"）

    Returns:
        [{code, label_ja, label_hierarchical}, ...] のリスト
    """
    query = f"""PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?code ?labelJa ?parentCode ?parentLabel ?grandCode ?grandLabel
WHERE {{
  ?uri skos:notation ?code ;
       skos:prefLabel ?labelJa .
  FILTER(STRSTARTS(?code, '{class_prefix}'))
  FILTER(LANG(?labelJa) = 'ja')
  OPTIONAL {{
    ?uri skos:broader ?parent .
    ?parent skos:notation ?parentCode ;
            skos:prefLabel ?parentLabel .
    FILTER(LANG(?parentLabel) = 'ja')
    OPTIONAL {{
      ?parent skos:broader ?grand .
      ?grand skos:notation ?grandCode ;
             skos:prefLabel ?grandLabel .
      FILTER(LANG(?grandLabel) = 'ja')
    }}
  }}
}}
ORDER BY ?code"""

    url = SPARQL_ENDPOINT + "?" + urllib.parse.urlencode({
        'query': query,
        'output': 'json'
    })

    req = urllib.request.Request(url, headers={'User-Agent': 'Python/3'})
    with urllib.request.urlopen(req, timeout=30) as res:
        data = json.loads(res.read().decode('utf-8'))

    results = []
    for r in data['results']['bindings']:
        code = r['code']['value']
        label = r['labelJa']['value']
        parent_label = r.get('parentLabel', {}).get('value', '')
        grand_label = r.get('grandLabel', {}).get('value', '')

        # 階層ラベルを構築
        parts = []
        if grand_label:
            parts.append(grand_label)
        if parent_label:
            parts.append(parent_label)
        parts.append(label)

        # 重複を除去（親と同じラベルの場合）
        unique_parts = []
        for p in parts:
            if not unique_parts or p != unique_parts[-1]:
                unique_parts.append(p)

        hierarchical = '/'.join(unique_parts)

        results.append({
            'code': code,
            'label_ja': label,
            'label_hierarchical': hierarchical
        })

    return results


def save_csv(results: list[dict], output_path: Path):
    """結果をCSVファイルに保存"""
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['code', 'label_ja', 'label_hierarchical'])
        writer.writeheader()
        writer.writerows(results)


def main():
    """メイン処理"""
    # コマンドライン引数を処理
    class_prefix = sys.argv[1] if len(sys.argv) > 1 else "91"

    print(f"NDC9 {class_prefix}類のラベルを取得中...")

    try:
        results = fetch_ndc_hierarchical(class_prefix)
    except urllib.error.HTTPError as e:
        print(f"エラー: HTTP {e.code}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"エラー: {e.reason}", file=sys.stderr)
        sys.exit(1)

    # 出力ファイル名
    base_dir = Path(__file__).parent
    output_file = base_dir / f'ndc9_class{class_prefix}_hierarchical.csv'

    save_csv(results, output_file)

    print(f"出力: {len(results)}件")
    print(f"保存先: {output_file}")

    # サンプル表示
    print("\nサンプル（最初の10件）:")
    for r in results[:10]:
        print(f"  {r['code']}: {r['label_hierarchical']}")


if __name__ == '__main__':
    main()
