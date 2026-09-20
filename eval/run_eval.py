"""检索质量评测脚本

用法（从项目根目录运行）:
    .venv\\Scripts\\python.exe eval\\run_eval.py

指标:
    检索命中率 = 预期来源文件出现在 top-k 检索结果中的比例
    （expected_source 为 null 的题目是负样本，不计入命中率）
"""
import sys
import json
import argparse
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.rag.store import vector_store

DEFAULT_DATASET = Path(__file__).parent / "datasets" / "qa_test.json"


def load_dataset(path):
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate(dataset, k):
    retriever = vector_store.as_retriever(search_kwargs={"k": k})

    results = []
    for item in dataset:
        docs = retriever.invoke(item["question"])
        sources = [d.metadata.get("source") for d in docs]
        expected = item.get("expected_source")

        if expected is None:
            status = "NEG"
            hit = None
        else:
            hit = expected in sources
            status = "HIT" if hit else "MISS"

        results.append({
            "id": item["id"],
            "question": item["question"],
            "category": item.get("category", "未分类"),
            "expected": expected,
            "actual": sources,
            "status": status,
            "hit": hit,
        })
    return results


def report(results, k):
    print(f"评测集规模: {len(results)} 题 | top-k = {k}")
    print("=" * 70)

    for r in results:
        mark = {"HIT": "HIT ", "MISS": "MISS", "NEG": "NEG "}[r["status"]]
        print(f"{r['id']:>2}. [{mark}] {r['question'][:34]}")
        print(f"         期望: {r['expected']}")
        print(f"         实际: {r['actual']}")

    scored = [r for r in results if r["hit"] is not None]
    hits = sum(1 for r in scored if r["hit"])

    print()
    print("按类别:")
    categories = {}
    for r in scored:
        c = r["category"]
        categories.setdefault(c, [0, 0])
        categories[c][1] += 1
        if r["hit"]:
            categories[c][0] += 1
    for c, (h, t) in sorted(categories.items()):
        print(f"  {c:<10} {h}/{t}")

    print()
    neg = [r for r in results if r["status"] == "NEG"]
    print(f"负样本 {len(neg)} 题（知识库外问题）:")
    for r in neg:
        print(f"  题{r['id']}: 检索返回 {r['actual']}")
    print()
    print(f"检索命中率: {hits}/{len(scored)} = {hits / len(scored) * 100:.1f}%")
    return {"hit_rate": hits / len(scored), "hits": hits, "scored": len(scored)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", type=int, default=3, help="检索返回条数")
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--out", default=None, help="把结果写入 json 文件")
    args = parser.parse_args()

    dataset = load_dataset(Path(args.dataset))
    results = evaluate(dataset, args.k)
    summary = report(results, args.k)

    if args.out:
        out_path = Path(args.out)
        out_path.write_text(
            json.dumps({"summary": summary, "results": results},
                       ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"\n结果已保存: {out_path}")


if __name__ == "__main__":
    main()
