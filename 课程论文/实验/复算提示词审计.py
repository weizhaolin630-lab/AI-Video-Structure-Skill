"""Count the archived prompts and summarize the explicit manual annotations."""

import json
import re
import sys
from pathlib import Path
from urllib.parse import quote


HERE = Path(__file__).resolve().parent
CASES = HERE / "提示词案例.json"
SOURCE = HERE.parents[1] / "AI Tech - Video Structure.md"


def normalize_source(lines):
    text = re.sub(r"\\([\\`*_{}\[\]()#+\-.!|])", r"\1", "\n".join(lines))
    return re.sub(r"\s+", "", text)


def characters(text):
    return sum(not character.isspace() for character in text)


def main():
    cases = json.loads(CASES.read_text(encoding="utf-8"))
    source = SOURCE.read_text(encoding="utf-8").splitlines()
    totals = [0] * 6
    print("| 案例 | 简述字符 | 原稿字符 | 结构化字符 | 原稿→结构化缩减 | 简述锚点 | 原稿锚点 | 结构化锚点 |")
    print("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for case in cases:
        start, end = case["source_lines"]
        attachment = f"(图片和附件/{quote(case['attachment'])})"
        if not 3 <= start <= end <= len(source) or attachment not in source[start - 3]:
            raise ValueError(f"{case['id']} 的原稿行段已变动，请核对附件与正文边界")
        if end < len(source) and source[end].strip():
            raise ValueError(f"{case['id']} 的原稿行段已变动，请核对附件与正文边界")
        original = normalize_source(source[start - 1:end])
        lengths = [characters(item) for item in (case["brief"], original, case["structured"])]
        count = len(case["anchors"])
        hits = [len(case["brief_retained"]), count, len(case["structured_retained"])]
        for key in ("brief_retained", "structured_retained"):
            assert sorted(set(case[key])) == case[key]
            assert all(1 <= index <= count for index in case[key])
        for index, value in enumerate(lengths + hits):
            totals[index] += value
        saved = 1 - lengths[2] / lengths[1]
        print(f'| {case["id"]} | {lengths[0]} | {lengths[1]} | {lengths[2]} | {saved:.1%} | '
              f'{hits[0]}/{count} | {count}/{count} | {hits[2]}/{count} |')
    brief, original, structured, brief_hits, possible, structured_hits = totals
    print(f"| 合计 | {brief} | {original} | {structured} | {1 - structured / original:.1%} | "
          f"{brief_hits}/{possible} | {possible}/{possible} | {structured_hits}/{possible} |")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
