#!/usr/bin/env python3
"""Build a dependency-free interactive portfolio prototype from verified artifacts."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def load_payload(project_root: Path) -> dict[str, Any]:
    scenes = read_jsonl(project_root / "data" / "scenes.jsonl")
    queries = read_jsonl(project_root / "data" / "golden_queries.jsonl")
    query_results = read_jsonl(project_root / "artifacts" / "query-results.jsonl")
    metrics = json.loads((project_root / "artifacts" / "metrics.json").read_text(encoding="utf-8"))

    result_index: dict[str, dict[str, Any]] = {}
    for row in query_results:
        result_index.setdefault(row["query_id"], {})[row["arm"]] = row

    return {
        "scenes": {scene["scene_id"]: scene for scene in scenes},
        "queries": queries,
        "results": result_index,
        "metrics": metrics,
    }


def render_html(payload: dict[str, Any]) -> str:
    serialized_payload = html.escape(
        json.dumps(payload, ensure_ascii=False, sort_keys=True),
        quote=False,
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>场景知识 Agent 原型</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #17202a;
      --muted: #5d6673;
      --line: #d8dee7;
      --panel: #ffffff;
      --bg: #f5f7fa;
      --blue: #2563eb;
      --teal: #0f766e;
      --amber: #b45309;
      --red: #b91c1c;
      --green: #15803d;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      background: var(--bg);
      color: var(--ink);
      font: 15px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    button, input, select {{ font: inherit; }}
    .app {{
      display: grid;
      grid-template-columns: 330px minmax(0, 1fr) 360px;
      min-height: 100vh;
    }}
    aside, main {{
      min-width: 0;
    }}
    .sidebar {{
      border-right: 1px solid var(--line);
      background: #eef2f7;
      padding: 18px;
      overflow: auto;
    }}
    .workspace {{
      padding: 20px;
      overflow: auto;
    }}
    .evidence {{
      border-left: 1px solid var(--line);
      background: #f8fafc;
      padding: 18px;
      overflow: auto;
    }}
    h1, h2, h3, p {{ margin-top: 0; }}
    h1 {{ font-size: 22px; margin-bottom: 4px; }}
    h2 {{ font-size: 15px; margin-bottom: 10px; }}
    h3 {{ font-size: 14px; margin-bottom: 8px; }}
    .muted {{ color: var(--muted); }}
    .search {{
      display: flex;
      gap: 8px;
      margin: 18px 0 14px;
    }}
    input[type="search"] {{
      min-width: 0;
      flex: 1;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 10px 11px;
      background: white;
    }}
    .icon-button, .query-button, .chip {{
      border: 1px solid var(--line);
      background: white;
      color: var(--ink);
      border-radius: 6px;
    }}
    .icon-button {{
      width: 42px;
      height: 42px;
      display: inline-grid;
      place-items: center;
      cursor: pointer;
    }}
    .icon-button:hover, .query-button:hover {{ border-color: var(--blue); }}
    .query-list {{
      display: grid;
      gap: 8px;
    }}
    .query-button {{
      width: 100%;
      text-align: left;
      padding: 10px;
      cursor: pointer;
    }}
    .query-button[aria-current="true"] {{
      border-color: var(--blue);
      box-shadow: inset 3px 0 0 var(--blue);
    }}
    .query-meta {{
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      margin-top: 6px;
    }}
    .chip {{
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      padding: 2px 8px;
      font-size: 12px;
      color: var(--muted);
    }}
    .toolbar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 16px;
    }}
    .select-wrap {{
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--muted);
    }}
    select {{
      border: 1px solid var(--line);
      background: white;
      border-radius: 6px;
      padding: 8px 10px;
    }}
    .metric-grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
      margin-bottom: 16px;
    }}
    .metric, .result-card, .panel {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
    }}
    .metric {{
      padding: 12px;
      min-height: 82px;
    }}
    .metric strong {{
      display: block;
      font-size: 22px;
      line-height: 1.1;
    }}
    .result-list {{
      display: grid;
      gap: 10px;
    }}
    .result-card {{
      display: grid;
      grid-template-columns: 54px minmax(0, 1fr);
      gap: 12px;
      padding: 14px;
      cursor: pointer;
    }}
    .result-card[aria-selected="true"] {{
      border-color: var(--teal);
      box-shadow: inset 4px 0 0 var(--teal);
    }}
    .rank {{
      width: 42px;
      height: 42px;
      border-radius: 50%;
      display: grid;
      place-items: center;
      color: white;
      background: var(--teal);
      font-weight: 700;
    }}
    .result-title {{
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: baseline;
    }}
    .score {{
      color: var(--muted);
      white-space: nowrap;
      font-variant-numeric: tabular-nums;
    }}
    .field-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 8px;
      margin: 12px 0;
    }}
    .field {{
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 8px;
      background: #fbfdff;
    }}
    .field span {{
      display: block;
      color: var(--muted);
      font-size: 12px;
      margin-bottom: 2px;
    }}
    .panel {{
      padding: 14px;
      margin-bottom: 14px;
    }}
    .quality-bars {{
      display: grid;
      gap: 8px;
    }}
    .bar-row {{
      display: grid;
      grid-template-columns: 28px 1fr 56px;
      align-items: center;
      gap: 8px;
    }}
    .bar {{
      height: 10px;
      background: #e5e7eb;
      border-radius: 999px;
      overflow: hidden;
    }}
    .bar-fill {{
      height: 100%;
      background: var(--blue);
    }}
    .risk-list {{
      margin: 0;
      padding-left: 18px;
    }}
    .decision {{
      display: grid;
      grid-template-columns: 34px minmax(0, 1fr);
      gap: 9px;
      align-items: start;
      margin-bottom: 10px;
    }}
    .step {{
      width: 28px;
      height: 28px;
      border-radius: 50%;
      display: grid;
      place-items: center;
      color: white;
      background: var(--blue);
      font-size: 12px;
      font-weight: 700;
    }}
    .badge-ok {{ color: var(--green); }}
    .badge-warn {{ color: var(--amber); }}
    .badge-danger {{ color: var(--red); }}
    canvas {{
      width: 100%;
      height: 150px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: white;
    }}
    @media (max-width: 1120px) {{
      .app {{ grid-template-columns: 300px 1fr; }}
      .evidence {{ grid-column: 1 / -1; border-left: 0; border-top: 1px solid var(--line); }}
    }}
    @media (max-width: 760px) {{
      .app {{ display: block; }}
      .sidebar, .workspace, .evidence {{ border: 0; }}
      .metric-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .field-grid {{ grid-template-columns: 1fr; }}
      .toolbar {{ align-items: stretch; flex-direction: column; }}
    }}
  </style>
</head>
<body>
  <div class="app">
    <aside class="sidebar">
      <h1>场景知识 Agent</h1>
      <p class="muted">W4 可交互原型：用 W2 冻结证据演示场景检索、证据复核和评估闭环。</p>
      <div class="search">
        <input id="searchInput" type="search" placeholder="输入场景问题或关键词" aria-label="搜索黄金查询">
        <button id="searchButton" class="icon-button" aria-label="搜索" title="搜索">⌕</button>
      </div>
      <h2>黄金查询</h2>
      <div id="queryList" class="query-list"></div>
    </aside>

    <main class="workspace">
      <div class="toolbar">
        <div>
          <h2 id="activeQuestion">选择一个黄金查询</h2>
          <p id="activeMeta" class="muted"></p>
        </div>
        <label class="select-wrap">检索方案
          <select id="armSelect">
            <option value="C">C 场景单元 Dense</option>
            <option value="A">A BM25</option>
            <option value="B">B 原始块 Dense</option>
            <option value="D">D Dense + Sparse</option>
          </select>
        </label>
      </div>
      <section class="metric-grid" aria-label="当前检索方案指标">
        <div class="metric"><span class="muted">Recall@1</span><strong id="metricRecall1">-</strong></div>
        <div class="metric"><span class="muted">nDCG@5</span><strong id="metricNdcg">-</strong></div>
        <div class="metric"><span class="muted">误召回</span><strong id="metricFar">-</strong></div>
        <div class="metric"><span class="muted">P50 时延</span><strong id="metricLatency">-</strong></div>
      </section>
      <section id="resultList" class="result-list" aria-label="检索结果"></section>
    </main>

    <aside class="evidence">
      <section class="panel">
        <h2>证据复核</h2>
        <div id="sceneDetail" class="muted">选择一条结果查看结构化证据。</div>
      </section>
      <section class="panel">
        <h2>评估对照</h2>
        <canvas id="metricChart" width="680" height="300" aria-label="四组 nDCG 对照图"></canvas>
      </section>
      <section class="panel">
        <h2>决策链</h2>
        <div class="decision"><span class="step">1</span><div><strong>锁定结构化场景单元</strong><br><span class="muted">C 组 nDCG@5 最高，排序更稳。</span></div></div>
        <div class="decision"><span class="step">2</span><div><strong>保留人工复核</strong><br><span class="muted">无答案拒答仍需强化，不能跳过审核。</span></div></div>
        <div class="decision"><span class="step">3</span><div><strong>混合检索降级为 P1</strong><br><span class="muted">D 组未改善排序，误召回更高。</span></div></div>
      </section>
    </aside>
  </div>

  <script id="prototype-data" type="application/json">{serialized_payload}</script>
  <script>
    const payload = JSON.parse(document.getElementById('prototype-data').textContent);
    const state = {{ queryId: payload.queries[0].query_id, arm: 'C', selectedSceneId: null, filter: '' }};
    const armNames = {{ A: 'A BM25', B: 'B 原始块 Dense', C: 'C 场景单元 Dense', D: 'D Dense + Sparse' }};
    const pct = value => `${{(value * 100).toFixed(1)}}%`;
    const score = value => Number(value).toFixed(3);

    function currentQuery() {{
      return payload.queries.find(query => query.query_id === state.queryId);
    }}

    function currentResult() {{
      return payload.results[state.queryId][state.arm];
    }}

    function renderQueries() {{
      const queryList = document.getElementById('queryList');
      const needle = state.filter.trim().toLowerCase();
      const queries = payload.queries.filter(query => {{
        if (!needle) return true;
        return `${{query.query_id}} ${{query.query_type}} ${{query.text}}`.toLowerCase().includes(needle);
      }});
      queryList.innerHTML = queries.map(query => `
        <button class="query-button" data-query="${{query.query_id}}" aria-current="${{query.query_id === state.queryId}}">
          <strong>${{query.text}}</strong>
          <span class="query-meta">
            <span class="chip">${{query.query_id}}</span>
            <span class="chip">${{query.query_type}}</span>
            <span class="chip">${{query.answerable ? '可回答' : '负例'}}</span>
          </span>
        </button>
      `).join('');
      queryList.querySelectorAll('button').forEach(button => {{
        button.addEventListener('click', () => {{
          state.queryId = button.dataset.query;
          state.selectedSceneId = null;
          renderAll();
        }});
      }});
    }}

    function renderMetrics() {{
      const metrics = payload.metrics.arms[state.arm];
      document.getElementById('metricRecall1').textContent = pct(metrics.recall_at_1);
      document.getElementById('metricNdcg').textContent = score(metrics.ndcg_at_5);
      document.getElementById('metricFar').textContent = pct(metrics.false_answer_rate);
      document.getElementById('metricLatency').textContent = `${{metrics.latency_p50_ms.toFixed(1)}} ms`;
    }}

    function relevanceLabel(query, sceneId) {{
      const relevance = query.relevance[sceneId] || 0;
      if (relevance >= 3) return '<span class="badge-ok">强相关</span>';
      if (relevance === 2) return '<span class="badge-ok">相关</span>';
      if (relevance === 1) return '<span class="badge-warn">弱相关</span>';
      return '<span class="badge-danger">未标注相关</span>';
    }}

    function renderResults() {{
      const query = currentQuery();
      const result = currentResult();
      const list = document.getElementById('resultList');
      document.getElementById('activeQuestion').textContent = query.text;
      document.getElementById('activeMeta').textContent = `${{query.query_id}} · ${{query.query_type}} · ${{query.answerable ? '期望命中相关场景' : '应触发人工复核/拒答'}}`;
      if (!state.selectedSceneId) state.selectedSceneId = result.ranking[0];
      list.innerHTML = result.ranking.map((sceneId, index) => {{
        const scene = payload.scenes[sceneId];
        return `
          <article class="result-card" data-scene="${{sceneId}}" aria-selected="${{sceneId === state.selectedSceneId}}">
            <div class="rank">${{index + 1}}</div>
            <div>
              <div class="result-title"><h3>${{scene.scene_id}} · ${{scene.title}}</h3><span class="score">${{score(result.scores[index])}}</span></div>
              <p>${{scene.summary}}</p>
              <span class="query-meta">
                <span class="chip">${{scene.environment.weather}}</span>
                <span class="chip">${{scene.environment.road_type}}</span>
                <span class="chip">${{scene.environment.surface}}</span>
                <span class="chip">${{relevanceLabel(query, sceneId)}}</span>
              </span>
            </div>
          </article>
        `;
      }}).join('');
      list.querySelectorAll('article').forEach(card => {{
        card.addEventListener('click', () => {{
          state.selectedSceneId = card.dataset.scene;
          renderResults();
          renderSceneDetail();
        }});
      }});
      renderSceneDetail();
    }}

    function renderSceneDetail() {{
      const scene = payload.scenes[state.selectedSceneId];
      const query = currentQuery();
      document.getElementById('sceneDetail').innerHTML = `
        <h3>${{scene.scene_id}} · ${{scene.title}}</h3>
        <p>${{relevanceLabel(query, scene.scene_id)}} · 数据边界：合成场景，仅用于产品原型验证。</p>
        <div class="field-grid">
          <div class="field"><span>环境</span>${{scene.environment.weather}} / ${{scene.environment.lighting}} / ${{scene.environment.road_type}} / ${{scene.environment.surface}}</div>
          <div class="field"><span>参与者</span>${{scene.actors.join('、')}}</div>
          <div class="field"><span>触发事件</span>${{scene.trigger}}</div>
          <div class="field"><span>系统响应</span>${{scene.system_behavior}}</div>
          <div class="field"><span>期望行为</span>${{scene.expected_behavior}}</div>
          <div class="field"><span>风险</span>${{scene.risk}}</div>
        </div>
        <h3>证据片段</h3>
        <ul class="risk-list">${{scene.evidence.map(item => `<li>${{item}}</li>`).join('')}}</ul>
      `;
    }}

    function drawChart() {{
      const canvas = document.getElementById('metricChart');
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.font = '24px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif';
      const arms = ['A', 'B', 'C', 'D'];
      const maxWidth = 430;
      arms.forEach((arm, index) => {{
        const y = 52 + index * 56;
        const value = payload.metrics.arms[arm].ndcg_at_5;
        ctx.fillStyle = '#17202a';
        ctx.fillText(armNames[arm], 24, y + 10);
        ctx.fillStyle = '#dbeafe';
        ctx.fillRect(190, y - 18, maxWidth, 28);
        ctx.fillStyle = arm === state.arm ? '#0f766e' : '#2563eb';
        ctx.fillRect(190, y - 18, maxWidth * value, 28);
        ctx.fillStyle = '#17202a';
        ctx.fillText(value.toFixed(4), 635 - 72, y + 10);
      }});
    }}

    function renderAll() {{
      renderQueries();
      renderMetrics();
      renderResults();
      drawChart();
    }}

    document.getElementById('armSelect').addEventListener('change', event => {{
      state.arm = event.target.value;
      state.selectedSceneId = null;
      renderAll();
    }});
    document.getElementById('searchButton').addEventListener('click', () => {{
      state.filter = document.getElementById('searchInput').value;
      renderQueries();
    }});
    document.getElementById('searchInput').addEventListener('input', event => {{
      state.filter = event.target.value;
      renderQueries();
    }});

    renderAll();
  </script>
</body>
</html>
"""


def build(project_root: Path, output_path: Path) -> None:
    payload = load_payload(project_root)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_html(payload), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the static W4 prototype.")
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "prototype" / "index.html",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    build(args.project_root.resolve(), args.output.resolve())
    print(f"written: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
