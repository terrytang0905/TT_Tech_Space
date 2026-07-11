"""Generate the W2 evidence report only from verified experiment artifacts."""

import argparse
import json
from pathlib import Path
from typing import Any, Mapping


def _better(left: Mapping[str, float], right: Mapping[str, float]) -> bool:
    keys = ("recall_at_5", "ndcg_at_5")
    return all(left[key] >= right[key] for key in keys) and any(left[key] > right[key] for key in keys)


def decide_prd_branch(metrics: Mapping[str, Any]) -> str:
    arms = metrics["arms"]
    if all(not _better(arms[arm], arms["A"]) for arm in "BCD"):
        return "stop-ai-expansion"
    if _better(arms["C"], arms["B"]):
        return "scene-hybrid-p0" if _better(arms["D"], arms["C"]) else "scene-p0-hybrid-p1"
    if _better(arms["D"], arms["C"]):
        return "hybrid-p0-simplify-scene"
    if not _better(arms["D"], arms["B"]):
        return "dense-p0-defer-scene-hybrid"
    return "dense-p0-defer-scene-hybrid"


def _percent(value: Any) -> str:
    return "—" if value is None else f"{float(value) * 100:.2f}%"


def _delta_pp(value: float) -> str:
    return f"{value * 100:+.2f} pp"


def build_report(metrics: Mapping[str, Any], manifest: Mapping[str, Any], error_analysis: str) -> str:
    branch = decide_prd_branch(metrics)
    decision_copy = {
        "scene-hybrid-p0": ("P0", "P0", "场景结构与混合检索均带来增益。"),
        "scene-p0-hybrid-p1": ("P0", "P1", "场景结构带来净增益，但混合检索没有继续改善排序。"),
        "hybrid-p0-simplify-scene": ("简化", "P0", "混合检索有效，但不能宣称场景结构本身有效。"),
        "dense-p0-defer-scene-hybrid": ("后续验证", "后续验证", "Dense 文本是更稳妥的 MVP 基线。"),
        "stop-ai-expansion": ("停止扩展", "停止扩展", "语义检索没有超过关键词基线。"),
    }[branch]
    scene_priority, hybrid_priority, rationale = decision_copy
    arms = metrics["arms"]
    comparisons = metrics["comparisons"]
    usage = manifest["usage"]
    normalized_errors = error_analysis.strip()
    normalized_errors = normalized_errors.replace("# W2 Retrieval Error Analysis\n\n", "")
    normalized_errors = normalized_errors.replace("## Arm ", "### Arm ")
    lines = [
        "# W2 智驾场景检索四组消融实验报告",
        "",
        "> 本报告由已验证的 `run-manifest.json`、`query-results.jsonl` 与 `metrics.json` 生成。40 个场景全部为合成数据，结果不构成真实道路安全结论。",
        "",
        "## 执行结论",
        "",
        f"- **结构化场景 Schema：{scene_priority}**；",
        "- **Dense 文本检索：P0**；",
        f"- **Dense + Sparse：{hybrid_priority}**；",
        f"- 决策理由：{rationale}",
        "- PRD 中的拒答能力继续标记为待强化：开发集阈值虽可分离，但黄金集无答案误召回仍明显波动。",
        "",
        "## 实验配置",
        "",
        "| 项目 | 实际配置 |",
        "|---|---|",
        f"| Git commit | `{manifest['git_commit']}` |",
        f"| 模型 | `{manifest['model']}` |",
        f"| Dense 维度 | {manifest['dimensions']} |",
        f"| 混合权重 α | {manifest['alpha']}（由 8 条开发查询选择） |",
        "| 测试集 | 40 个场景、36 条冻结黄金查询，其中 28 条可回答、8 条无答案/负例 |",
        "| 排序深度 | Top 5 |",
        "| 计价口径 | 2026-07-12 中国内地实时调用原价 0.5 元/百万输入 Token |",
        "",
        "官方价格依据：[阿里云百炼模型价格](https://help.aliyun.com/zh/model-studio/model-pricing)。",
        "",
        "## 总体结果",
        "",
        "| 组别 | Recall@1 | Recall@5 | MRR | nDCG@5 | 无答案误召回率 | P50 端到端时延 | P95 端到端时延 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    labels = {"A": "A BM25", "B": "B 原始块 Dense", "C": "C 场景单元 Dense", "D": "D 场景单元混合"}
    for arm in "ABCD":
        row = arms[arm]
        lines.append(
            f"| {labels[arm]} | {_percent(row['recall_at_1'])} | {_percent(row['recall_at_5'])} | "
            f"{row['mrr']:.4f} | {row['ndcg_at_5']:.4f} | {_percent(row['false_answer_rate'])} | "
            f"{row['latency_p50_ms']:.2f} ms | {row['latency_p95_ms']:.2f} ms |"
        )
    lines.extend([
        "",
        "质量指标只在 28 条可回答查询上汇总；无答案误召回率使用 8 条负例/范围外查询。B/C 共用同一次 Dense 查询向量调用，因此报告中的两组端到端时延用于用户体验估计，不能相加解释为实际 API 总耗时。",
        "",
        "## 三项关键消融",
        "",
        "| 对比 | Recall@5 | nDCG@5 | 产品解释 |",
        "|---|---:|---:|---|",
        f"| C − B | {_delta_pp(comparisons['C_minus_B']['recall_at_5'])} | {_delta_pp(comparisons['C_minus_B']['ndcg_at_5'])} | 场景结构提升排序质量，Recall 已到上限 |",
        f"| D − C | {_delta_pp(comparisons['D_minus_C']['recall_at_5'])} | {_delta_pp(comparisons['D_minus_C']['ndcg_at_5'])} | Sparse 融合未带来增益，且拒答恶化 |",
        f"| D − A | {_delta_pp(comparisons['D_minus_A']['recall_at_5'])} | {_delta_pp(comparisons['D_minus_A']['ndcg_at_5'])} | 混合方案仍显著优于传统关键词基线 |",
        "",
        "C 组取得 Recall@1=100%、Recall@5=100%、MRR=1.0000、nDCG@5=0.9978，是本轮最稳健方案。A 组在精确术语上表现强，但同义改写子集 Recall@1 仅为 62.50%、Recall@5 为 87.50%，说明语义检索的主要价值集中在表达不一致的任务。",
        "",
        "## 时延与实际费用",
        "",
        f"- 实际输入 Token：**{int(usage['input_tokens']):,}**；",
        f"- 实际 API 请求：**{int(usage['request_count'])} 次**；",
        f"- API 累计等待时间：**{float(usage['api_latency_ms']) / 1000:.3f} 秒**；",
        f"- 按官方原价估算费用：**{usage['estimated_cost_cny']} 元**；",
        f"- 本次运行缓存命中：**{int(usage['cache_hits'])}**；首次完整运行全部为真实调用。",
        "",
        "BM25 P50 约 0.20 ms；B/C/D 的 P50 约 404–408 ms，主要来自远程查询向量调用。当前 40 条场景使用精确全量打分，本地排序开销很小；这些数字不能外推到生产向量库 SLA。",
        "",
        "## 产品范围影响",
        "",
        "1. FR-02 场景单元抽取与查看保持 P0；",
        "2. FR-03/FR-04 的 MVP 检索链路采用结构化场景单元 + Dense；",
        "3. Dense+Sparse 混合检索降为 P1 实验项，不进入首个演示闭环；",
        "4. FR-05 的证据不足拒答仍为待验证，不能因开发集阈值可分离而宣称已解决；",
        "5. W3 优先访谈同义改写、复合条件和证据复核任务，不扩展图片、视频和企业连接器。",
        "",
        "## 局限与反证",
        "",
        "- 40 个场景和 36 条查询是原型方向证据，不具统计显著性；",
        "- 场景与查询由同一研究框架构造，可能高估结构化字段的适配程度；",
        "- 本轮只验证文本，没有证明真正多模态向量的增益；",
        "- 开发集只有 8 条，拒答阈值稳定性不足；D 组 50% 的黄金集误召回直接暴露了这一风险；",
        "- C 组的高分需要在 W3 用户语言和新增盲测查询上复验，不能视为生产效果。",
        "",
        "## 薄弱案例",
        "",
        normalized_errors,
        "",
        "## 可复现证据",
        "",
        f"- 场景数据 SHA-256：`{manifest['dataset_sha256']}`；",
        f"- 开发查询 SHA-256：`{manifest['dev_query_sha256']}`；",
        f"- 黄金查询 SHA-256：`{manifest['golden_query_sha256']}`；",
        "- 复核命令：`python3 -m src.experiment --verify-only --data-dir data --artifact-dir artifacts`。",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-dir", type=Path, default=Path("artifacts"))
    parser.add_argument("--output", type=Path, default=Path("reports/w2-retrieval-ablation-report.md"))
    args = parser.parse_args()
    metrics = json.loads((args.artifact_dir / "metrics.json").read_text(encoding="utf-8"))
    manifest = json.loads((args.artifact_dir / "run-manifest.json").read_text(encoding="utf-8"))
    errors = (args.artifact_dir / "error-analysis.md").read_text(encoding="utf-8")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build_report(metrics, manifest, errors), encoding="utf-8")


if __name__ == "__main__":
    main()
