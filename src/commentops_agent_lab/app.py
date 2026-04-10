from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from commentops_agent_lab.agent import CommentOpsAgent
from commentops_agent_lab.content import (
    agent_evolution_payload,
    project_overview_payload,
    research_log_payload,
    workflow_graph_payload,
)
from commentops_agent_lab.data import load_sample_review_cases
from commentops_agent_lab.eval import EvalReport, run_evaluation
from commentops_agent_lab.schemas import ReviewCase, ReviewResponse


app = FastAPI(title="CommentOps Agent Lab", version="0.3.0")
agent = CommentOpsAgent()


COMMON_STYLES = """
  :root {
    --bg: #f4efe8;
    --panel: rgba(255, 251, 245, 0.86);
    --panel-strong: #fffaf1;
    --line: rgba(18, 30, 44, 0.10);
    --line-strong: rgba(18, 30, 44, 0.16);
    --text: #18222d;
    --muted: #5a6877;
    --accent: #c45a38;
    --accent-2: #24485a;
    --good: #1f7a55;
    --warn: #9b6600;
    --danger: #a7322a;
    --shadow: 0 24px 60px rgba(23, 34, 49, 0.12);
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    color: var(--text);
    font-family: "IBM Plex Sans SC", "PingFang SC", "Helvetica Neue", sans-serif;
    background:
      radial-gradient(circle at top left, rgba(196, 90, 56, 0.18), transparent 28%),
      radial-gradient(circle at top right, rgba(36, 72, 90, 0.16), transparent 28%),
      linear-gradient(180deg, #fbf6ef 0%, #efe7da 100%);
  }
  a { color: inherit; text-decoration: none; }
  .shell {
    max-width: 1460px;
    margin: 0 auto;
    padding: 24px;
  }
  .topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    margin-bottom: 18px;
  }
  .brand {
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 700;
  }
  .brand-badge {
    width: 42px;
    height: 42px;
    border-radius: 14px;
    display: grid;
    place-items: center;
    background: linear-gradient(135deg, var(--accent), #d77b53);
    color: white;
    box-shadow: var(--shadow);
  }
  .nav {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }
  .nav a {
    padding: 10px 14px;
    border-radius: 999px;
    background: rgba(36, 72, 90, 0.07);
    color: var(--accent-2);
    font-size: 14px;
  }
  .nav a.active {
    background: linear-gradient(135deg, var(--accent), #d77b53);
    color: white;
  }
  .hero, .panel, .metric-card, .mini-card, .preset-card, .node-button {
    border: 1px solid var(--line);
    background: var(--panel);
    box-shadow: var(--shadow);
    backdrop-filter: blur(10px);
  }
  .hero, .panel, .metric-card, .mini-card, .preset-card {
    border-radius: 24px;
  }
  .hero {
    padding: 28px;
    margin-bottom: 18px;
  }
  .eyebrow {
    margin-bottom: 10px;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.14em;
    font-size: 12px;
  }
  h1 {
    margin: 0 0 12px;
    font-size: 42px;
    line-height: 1.04;
  }
  h2, h3, h4 { margin: 0 0 10px; }
  .subcopy, .muted {
    color: var(--muted);
    line-height: 1.7;
  }
  .hero-points, .chip-row, .preset-rail, .metrics {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }
  .chip {
    padding: 8px 12px;
    border-radius: 999px;
    background: rgba(36, 72, 90, 0.08);
    color: var(--accent-2);
    font-size: 13px;
  }
  .two-col {
    display: grid;
    grid-template-columns: 390px minmax(0, 1fr);
    gap: 18px;
  }
  .stack {
    display: grid;
    gap: 16px;
  }
  .panel {
    padding: 22px;
  }
  .status {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
    padding: 7px 11px;
    border-radius: 999px;
    background: rgba(36, 72, 90, 0.08);
    color: var(--accent-2);
    font-size: 12px;
  }
  .preset-rail {
    overflow-x: auto;
    padding-bottom: 4px;
  }
  .preset-card {
    min-width: 230px;
    padding: 16px;
    cursor: pointer;
    transition: transform 140ms ease, border-color 140ms ease, background 140ms ease;
  }
  .preset-card:hover, .node-button:hover {
    transform: translateY(-2px);
  }
  .preset-card.active {
    border-color: rgba(196, 90, 56, 0.42);
    background: linear-gradient(180deg, rgba(196, 90, 56, 0.10), rgba(255, 251, 245, 0.94));
  }
  .preset-meta {
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--muted);
  }
  label {
    display: block;
    margin-bottom: 7px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 12px;
  }
  input, textarea {
    width: 100%;
    padding: 14px 16px;
    border-radius: 14px;
    border: 1px solid var(--line-strong);
    background: var(--panel-strong);
    font: inherit;
    color: var(--text);
  }
  textarea { min-height: 108px; resize: vertical; }
  .row {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
  }
  .triple {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
  }
  button {
    border: 0;
    cursor: pointer;
    font: inherit;
    font-weight: 700;
    border-radius: 999px;
    padding: 13px 18px;
  }
  .primary {
    background: linear-gradient(135deg, var(--accent), #d77b53);
    color: white;
  }
  .secondary {
    background: rgba(36, 72, 90, 0.08);
    color: var(--accent-2);
  }
  .button-row {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }
  .metrics {
    margin-top: 18px;
  }
  .metric-card {
    min-width: 180px;
    padding: 18px;
  }
  .metric-label {
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 12px;
  }
  .metric-value {
    margin-top: 8px;
    font-size: 30px;
    font-weight: 800;
  }
  .grid {
    display: grid;
    gap: 18px;
  }
  .result-row {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 18px;
  }
  .decision-banner {
    display: flex;
    justify-content: space-between;
    gap: 18px;
    align-items: center;
    padding: 16px 18px;
    border-radius: 20px;
    background: linear-gradient(135deg, rgba(196, 90, 56, 0.08), rgba(36, 72, 90, 0.08));
  }
  .decision-value {
    font-size: 28px;
    font-weight: 800;
  }
  .decision-value.pass { color: var(--good); }
  .decision-value.reject { color: var(--danger); }
  .decision-value.escalate { color: var(--warn); }
  .mini-card {
    padding: 15px 16px;
  }
  .card-list {
    display: grid;
    gap: 12px;
  }
  .mono {
    font-family: "JetBrains Mono", "SFMono-Regular", monospace;
    font-size: 12px;
  }
  .empty {
    color: var(--muted);
  }
  .workflow-layout {
    display: grid;
    grid-template-columns: minmax(0, 1.25fr) minmax(360px, 0.75fr);
    gap: 18px;
  }
  .lane {
    padding: 16px;
    border-radius: 22px;
    border: 1px solid var(--line);
    background: rgba(255, 255, 255, 0.28);
  }
  .lane-title {
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--muted);
    margin-bottom: 12px;
  }
  .lane-row {
    display: flex;
    gap: 12px;
    align-items: center;
    overflow-x: auto;
    padding-bottom: 8px;
  }
  .arrow {
    color: var(--muted);
    font-size: 22px;
    flex: 0 0 auto;
  }
  .node-button {
    flex: 0 0 220px;
    text-align: left;
    padding: 16px;
    border-radius: 22px;
    transition: transform 140ms ease, border-color 140ms ease, background 140ms ease;
  }
  .node-button.active {
    border-color: rgba(36, 72, 90, 0.34);
    background: linear-gradient(180deg, rgba(36, 72, 90, 0.10), rgba(255, 251, 245, 0.96));
  }
  .node-button.current {
    border-color: rgba(196, 90, 56, 0.40);
    background: linear-gradient(180deg, rgba(196, 90, 56, 0.12), rgba(255, 251, 245, 0.96));
  }
  .section-grid {
    display: grid;
    gap: 18px;
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .timeline {
    display: grid;
    gap: 14px;
  }
  .source-card {
    padding: 16px;
    border-radius: 20px;
    border: 1px solid var(--line);
    background: rgba(255, 255, 255, 0.40);
  }
  .overview-grid, .comparison-grid, .deliverable-grid, .metric-grid {
    display: grid;
    gap: 18px;
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .overview-card, .comparison-card, .deliverable-card, .metric-card-extended {
    padding: 18px;
    border-radius: 22px;
    border: 1px solid var(--line);
    background: rgba(255, 255, 255, 0.48);
  }
  .overview-card p,
  .comparison-card p,
  .deliverable-card p,
  .metric-card-extended p {
    margin: 10px 0 0;
    color: var(--muted);
    line-height: 1.7;
  }
  .doc-path {
    margin-top: 10px;
    padding: 10px 12px;
    border-radius: 14px;
    background: rgba(36, 72, 90, 0.07);
    font-family: "JetBrains Mono", "SFMono-Regular", monospace;
    font-size: 12px;
    color: var(--accent-2);
    word-break: break-all;
  }
  .fit-badge {
    display: inline-flex;
    align-items: center;
    margin-top: 10px;
    padding: 6px 10px;
    border-radius: 999px;
    background: rgba(196, 90, 56, 0.10);
    color: var(--accent);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }
  .overview-band {
    margin-top: 18px;
    padding: 18px;
    border-radius: 24px;
    border: 1px solid var(--line);
    background: linear-gradient(135deg, rgba(196, 90, 56, 0.08), rgba(36, 72, 90, 0.08));
  }
  .overview-band h3 {
    margin-bottom: 8px;
  }
  .overview-band ol.tight {
    margin-top: 12px;
  }
  .workflow-layout {
    display: grid;
    grid-template-columns: minmax(0, 1.52fr) minmax(340px, 0.72fr);
    gap: 18px;
    align-items: start;
  }
  .workflow-left, .workflow-right {
    display: grid;
    gap: 18px;
  }
  .workflow-right {
    position: sticky;
    top: 24px;
    align-self: start;
  }
  .workflow-canvas-panel {
    padding: 22px;
  }
  .workflow-panel-head {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 18px;
    margin-bottom: 14px;
  }
  .workflow-panel-copy {
    max-width: 760px;
    color: var(--muted);
    line-height: 1.7;
  }
  .workflow-controls {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    justify-content: flex-end;
  }
  .workflow-controls button {
    padding: 10px 14px;
  }
  .workflow-hint {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
    margin-bottom: 14px;
    padding: 12px 14px;
    border-radius: 18px;
    border: 1px solid var(--line);
    background: rgba(255, 255, 255, 0.58);
    color: var(--accent-2);
    line-height: 1.6;
  }
  .workflow-pill {
    padding: 8px 12px;
    border-radius: 999px;
    background: rgba(36, 72, 90, 0.08);
    color: var(--accent-2);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }
  .workflow-canvas-shell {
    position: relative;
    height: 620px;
    overflow: hidden;
    border-radius: 28px;
    border: 1px solid var(--line);
    background:
      radial-gradient(circle at top left, rgba(196, 90, 56, 0.16), transparent 26%),
      radial-gradient(circle at bottom right, rgba(36, 72, 90, 0.16), transparent 28%),
      linear-gradient(180deg, rgba(255, 250, 241, 0.94), rgba(246, 239, 228, 0.98));
    cursor: grab;
  }
  .workflow-canvas-shell.dragging {
    cursor: grabbing;
  }
  .workflow-canvas-grid,
  .workflow-canvas-tint {
    position: absolute;
    inset: 0;
    pointer-events: none;
  }
  .workflow-canvas-grid {
    opacity: 0.42;
    background-image:
      linear-gradient(rgba(36, 72, 90, 0.07) 1px, transparent 1px),
      linear-gradient(90deg, rgba(36, 72, 90, 0.07) 1px, transparent 1px);
    background-size: 54px 54px;
  }
  .workflow-canvas-tint {
    background:
      linear-gradient(180deg, rgba(255, 255, 255, 0.00), rgba(255, 255, 255, 0.12)),
      radial-gradient(circle at center, rgba(255, 255, 255, 0.00), rgba(255, 255, 255, 0.18));
  }
  .workflow-viewport {
    position: absolute;
    left: 0;
    top: 0;
    transform-origin: 0 0;
    will-change: transform;
  }
  .workflow-svg {
    display: block;
    overflow: visible;
    user-select: none;
  }
  .workflow-svg .lane-band {
    stroke: rgba(18, 30, 44, 0.08);
    stroke-width: 1;
  }
  .workflow-svg .lane-band.online {
    fill: rgba(36, 72, 90, 0.08);
  }
  .workflow-svg .lane-band.offline {
    fill: rgba(196, 90, 56, 0.08);
  }
  .workflow-svg .lane-label {
    fill: var(--accent-2);
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.08em;
  }
  .workflow-svg .workflow-edge {
    fill: none;
    stroke: rgba(90, 104, 119, 0.34);
    stroke-width: 4;
    stroke-linecap: round;
  }
  .workflow-svg .workflow-edge.active {
    stroke: rgba(36, 72, 90, 0.50);
  }
  .workflow-svg .workflow-edge.current {
    stroke: rgba(196, 90, 56, 0.76);
  }
  .workflow-svg .workflow-node {
    cursor: pointer;
  }
  .workflow-svg .workflow-node rect {
    fill: rgba(255, 251, 245, 0.96);
    stroke: rgba(18, 30, 44, 0.14);
    stroke-width: 1.4;
    filter: drop-shadow(0 14px 26px rgba(23, 34, 49, 0.08));
  }
  .workflow-svg .workflow-node.active rect {
    fill: rgba(255, 255, 255, 0.98);
    stroke: rgba(36, 72, 90, 0.28);
  }
  .workflow-svg .workflow-node.current rect {
    fill: rgba(255, 244, 236, 0.98);
    stroke: rgba(196, 90, 56, 0.56);
    stroke-width: 2.1;
  }
  .workflow-svg .node-id {
    fill: var(--muted);
    font-size: 11px;
    letter-spacing: 0.10em;
    text-transform: uppercase;
  }
  .workflow-svg .node-title {
    fill: var(--text);
    font-size: 18px;
    font-weight: 700;
  }
  .workflow-svg .node-subtitle {
    fill: var(--muted);
    font-size: 13px;
  }
  .workflow-minimap-panel {
    position: absolute;
    left: 18px;
    bottom: 18px;
    width: 236px;
    padding: 12px;
    border-radius: 20px;
    border: 1px solid var(--line);
    background: rgba(255, 252, 247, 0.88);
    box-shadow: 0 16px 34px rgba(23, 34, 49, 0.12);
    backdrop-filter: blur(8px);
  }
  .workflow-minimap-label {
    margin-bottom: 8px;
    color: var(--muted);
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.14em;
  }
  #workflowMinimap {
    width: 100%;
    height: 134px;
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid var(--line);
    background: rgba(255, 255, 255, 0.82);
    cursor: pointer;
  }
  .workflow-runtime-grid {
    display: grid;
    gap: 12px;
  }
  .runtime-card {
    padding: 15px 16px;
    border-radius: 20px;
    border: 1px solid var(--line);
    background: rgba(255, 255, 255, 0.44);
  }
  .runtime-card ul.tight {
    margin-bottom: 0;
  }
  .reference-note {
    margin-top: 8px;
    color: var(--muted);
    line-height: 1.6;
  }
  .reference-tag {
    display: inline-flex;
    align-items: center;
    margin-top: 10px;
    padding: 6px 10px;
    border-radius: 999px;
    background: rgba(196, 90, 56, 0.10);
    color: var(--accent);
    font-size: 12px;
    font-weight: 700;
  }
  ul.tight {
    margin: 8px 0 0 18px;
    color: var(--muted);
  }
  @media (max-width: 1120px) {
    .two-col, .workflow-layout, .result-row, .section-grid, .overview-grid, .comparison-grid, .deliverable-grid, .metric-grid { grid-template-columns: 1fr; }
    .topbar { align-items: flex-start; flex-direction: column; }
    .workflow-right { position: static; }
    .workflow-canvas-shell { height: 540px; }
  }
  @media (max-width: 760px) {
    .workflow-panel-head { flex-direction: column; }
    .workflow-controls { justify-content: flex-start; }
    .workflow-minimap-panel {
      width: 192px;
      left: 14px;
      bottom: 14px;
    }
    .workflow-canvas-shell { height: 500px; }
  }
"""


def _render_nav(active: str) -> str:
    items = [
        ("overview", "项目全景", "/project-overview"),
        ("evolution", "工程进化", "/agent-evolution"),
        ("demo", "工作台", "/demo"),
        ("workflow", "在线链路", "/workflow"),
        ("research", "调研记录", "/research-log"),
        ("docs", "API Docs", "/docs"),
    ]
    links = []
    for key, label, href in items:
        css = "active" if key == active else ""
        links.append(f'<a class="{css}" href="{href}">{label}</a>')
    return "".join(links)


def _render_page(title: str, active_nav: str, body: str, scripts: str = "") -> str:
    html = """
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>__TITLE__</title>
    <style>__STYLES__</style>
  </head>
  <body>
    <div class="shell">
      <div class="topbar">
        <div class="brand">
          <div class="brand-badge">CQ</div>
          <div>
            <div style="font-size:13px;color:var(--muted);">CommentOps Agent Lab</div>
            <div style="font-size:18px;">CQC-style Comment Moderation Workbench</div>
          </div>
        </div>
        <div class="nav">__NAV__</div>
      </div>
      __BODY__
    </div>
    <script>__SCRIPTS__</script>
  </body>
</html>
"""
    return (
        html.replace("__TITLE__", title)
        .replace("__STYLES__", COMMON_STYLES)
        .replace("__NAV__", _render_nav(active_nav))
        .replace("__BODY__", body)
        .replace("__SCRIPTS__", scripts)
    )


def render_demo_page() -> str:
    body = """
<section class="hero">
  <div class="eyebrow">Review Workbench</div>
  <h1>从“看一条评论”升级成“处理一个审核 case”</h1>
  <div class="subcopy">
    这个页面不是单条评论分类器，而是评论审核工作台。它把评论文本、上下文、举报量、历史违规、申诉翻案历史、
    policy evidence、similar cases 和 queue routing 串到同一个 reviewer-facing workflow 里。
  </div>
  <div class="hero-points">
    <span class="chip">Policy-grounded decisions</span>
    <span class="chip">Guarded auto-pass</span>
    <span class="chip">Human review queue routing</span>
    <span class="chip">Similar case support</span>
    <span class="chip">Training-ready traces</span>
  </div>
  <div id="metricGrid" class="metrics"></div>
</section>

<div class="two-col">
  <div class="stack">
    <div class="panel">
      <div class="status">Preset Cases</div>
      <h3>直接点击切换案例</h3>
      <div class="muted">我把 preset 从下拉框改成了可见的案例卡片，切换后会自动填充并执行一次审核。</div>
      <div id="presetRail" class="preset-rail" style="margin-top:14px;"></div>
    </div>
    <div class="panel">
      <div class="status">Case Intake</div>
      <div class="stack">
        <div class="row">
          <div>
            <label for="caseId">Case ID</label>
            <input id="caseId" value="demo-case-001" />
          </div>
          <div>
            <label for="userId">User ID</label>
            <input id="userId" value="user-demo-001" />
          </div>
        </div>
        <div>
          <label for="commentText">Comment Text</label>
          <textarea id="commentText">你这种垃圾去死吧</textarea>
        </div>
        <div>
          <label for="threadContext">Thread Context</label>
          <textarea id="threadContext">我不同意你的观点</textarea>
        </div>
        <div class="triple">
          <div>
            <label for="reporterCount">Reporters</label>
            <input id="reporterCount" type="number" min="0" value="6" />
          </div>
          <div>
            <label for="priorViolations">Prior Violations</label>
            <input id="priorViolations" type="number" min="0" value="3" />
          </div>
          <div>
            <label for="priorAppeals">Appeal Overturns</label>
            <input id="priorAppeals" type="number" min="0" value="0" />
          </div>
        </div>
        <div class="row">
          <div>
            <label for="authorTenure">Account Age (days)</label>
            <input id="authorTenure" type="number" min="0" value="85" />
          </div>
          <div>
            <label for="policyVersion">Policy Version</label>
            <input id="policyVersion" value="comment-policy-v1" />
          </div>
        </div>
        <div class="button-row">
          <button class="primary" onclick="runReview()">运行审核</button>
          <a class="secondary" href="/workflow" style="display:inline-flex;align-items:center;">查看完整在线链路</a>
        </div>
      </div>
    </div>
  </div>

  <div class="grid">
    <div class="panel">
      <div class="status">Decision</div>
      <div class="decision-banner">
        <div>
          <div class="metric-label">Moderation Action</div>
          <div id="decisionValue" class="decision-value">Awaiting review</div>
          <div id="decisionRationale" class="subcopy" style="margin-top:8px;max-width:none;"></div>
        </div>
        <div style="text-align:right;">
          <div class="metric-label">Confidence</div>
          <div id="confidenceValue" class="metric-value" style="font-size:26px;">--</div>
          <div id="stopReason" class="metric-label" style="margin-top:6px;">--</div>
        </div>
      </div>
    </div>
    <div class="result-row">
      <div class="panel">
        <div class="status">Routing & Impact</div>
        <div class="card-list">
          <div class="mini-card">
            <strong>Queue Routing</strong>
            <div id="queueCard" class="empty">Run a review.</div>
          </div>
          <div class="mini-card">
            <strong>Business Impact</strong>
            <div id="businessCard" class="empty">Run a review.</div>
          </div>
        </div>
      </div>
      <div class="panel">
        <div class="status">Risk Signals</div>
        <div id="riskSignals" class="card-list">
          <div class="empty">Run a review.</div>
        </div>
      </div>
    </div>
    <div class="result-row">
      <div class="panel">
        <div class="status">Policy Evidence</div>
        <div id="policyHits" class="card-list">
          <div class="empty">Run a review.</div>
        </div>
      </div>
      <div class="panel">
        <div class="status">Similar Cases</div>
        <div id="similarCases" class="card-list">
          <div class="empty">Run a review.</div>
        </div>
      </div>
    </div>
    <div class="result-row">
      <div class="panel">
        <div class="status">Recommended Actions</div>
        <div id="recommendedActions" class="card-list">
          <div class="empty">Run a review.</div>
        </div>
      </div>
      <div class="panel">
        <div class="status">Reviewer Notes & Trace</div>
        <div id="reviewNotes" class="card-list">
          <div class="empty">Run a review.</div>
        </div>
        <div id="toolTrace" class="card-list" style="margin-top:12px;"></div>
      </div>
    </div>
  </div>
</div>
"""
    scripts = """
let presets = [];
let activePresetId = null;

function percentage(value) {
  return `${Math.round(value * 100)}%`;
}

function renderList(containerId, items, renderer, emptyText='No items.') {
  const root = document.getElementById(containerId);
  if (!items || items.length === 0) {
    root.innerHTML = `<div class="empty">${emptyText}</div>`;
    return;
  }
  root.innerHTML = items.map(renderer).join('');
}

function renderMetrics(report) {
  const items = [
    { label: 'Action Accuracy', value: percentage(report.action_accuracy) },
    { label: 'Queue Accuracy', value: percentage(report.queue_routing_accuracy) },
    { label: 'Human Review Rate', value: percentage(report.human_review_rate) },
    { label: 'Auto Reject Rate', value: percentage(report.auto_reject_rate) },
  ];
  document.getElementById('metricGrid').innerHTML = items.map((item) => `
    <div class="metric-card">
      <div class="metric-label">${item.label}</div>
      <div class="metric-value">${item.value}</div>
    </div>
  `).join('');
}

function renderPresetRail() {
  const rail = document.getElementById('presetRail');
  rail.innerHTML = presets.map((preset) => `
    <div class="preset-card ${preset.case_id === activePresetId ? 'active' : ''}" onclick="activatePreset('${preset.case_id}')">
      <div class="preset-meta">${preset.expected_queue || 'no-queue'}</div>
      <h4>${preset.case_id}</h4>
      <div class="muted">${preset.comment_text}</div>
      <div style="margin-top:10px;" class="chip-row">
        <span class="chip">${preset.expected_action || 'unknown'}</span>
        <span class="chip">${preset.expected_category || 'unknown'}</span>
      </div>
    </div>
  `).join('');
}

function applyPreset(preset) {
  activePresetId = preset.case_id;
  document.getElementById('caseId').value = preset.case_id;
  document.getElementById('userId').value = preset.user_id;
  document.getElementById('commentText').value = preset.comment_text;
  document.getElementById('threadContext').value = (preset.thread_context || []).join('\\n');
  document.getElementById('reporterCount').value = preset.reporter_count || 0;
  document.getElementById('priorViolations').value = preset.prior_violation_count || 0;
  document.getElementById('priorAppeals').value = preset.prior_appeal_overturns || 0;
  document.getElementById('authorTenure').value = preset.author_tenure_days || 365;
  document.getElementById('policyVersion').value = preset.policy_version || 'comment-policy-v1';
  renderPresetRail();
}

async function activatePreset(caseId) {
  const preset = presets.find((item) => item.case_id === caseId);
  if (!preset) return;
  applyPreset(preset);
  await runReview();
}

async function runReview() {
  const payload = {
    case_id: document.getElementById('caseId').value,
    user_id: document.getElementById('userId').value,
    comment_text: document.getElementById('commentText').value,
    thread_context: document.getElementById('threadContext').value.split('\\n').map((item) => item.trim()).filter(Boolean),
    reporter_count: Number(document.getElementById('reporterCount').value || 0),
    prior_violation_count: Number(document.getElementById('priorViolations').value || 0),
    prior_appeal_overturns: Number(document.getElementById('priorAppeals').value || 0),
    author_tenure_days: Number(document.getElementById('authorTenure').value || 365),
    policy_version: document.getElementById('policyVersion').value,
  };
  const response = await fetch('/review', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  renderResponse(data);
}

function renderResponse(data) {
  const decision = document.getElementById('decisionValue');
  decision.textContent = `${data.decision.action.toUpperCase()} · ${data.decision.primary_category}`;
  decision.className = `decision-value ${data.decision.action}`;
  document.getElementById('decisionRationale').textContent = data.decision.rationale;
  document.getElementById('confidenceValue').textContent = `${Math.round(data.decision.confidence * 100)}%`;
  document.getElementById('stopReason').textContent = data.stop_reason;
  document.getElementById('queueCard').innerHTML = `
    <div><strong>${data.queue_routing.queue_name}</strong> · ${data.queue_routing.priority}</div>
    <div style="margin-top:8px;color:var(--muted);">${data.queue_routing.rationale}</div>
    <div class="mono" style="margin-top:10px;">SLA ${data.queue_routing.sla_minutes} min</div>
  `;
  document.getElementById('businessCard').innerHTML = `
    <div><strong>${data.business_impact.automation_mode}</strong></div>
    <div style="margin-top:8px;color:var(--muted);">reviewer_load=${data.business_impact.reviewer_load}, risk=${data.business_impact.risk_level}</div>
    <ul class="tight">${data.business_impact.notes.map((item) => `<li>${item}</li>`).join('')}</ul>
  `;
  renderList('riskSignals', data.risk_signals, (item) => `
    <div class="mini-card">
      <strong>${item.signal}</strong>
      <div>${item.level} · ${item.value}</div>
      <div style="margin-top:8px;color:var(--muted);">${item.note}</div>
    </div>
  `, 'No risk signals.');
  renderList('policyHits', data.matched_policies, (item) => `
    <div class="mini-card">
      <strong>${item.title}</strong>
      <div>${item.category} · ${item.severity} · ${item.decision}</div>
      <div style="margin-top:8px;color:var(--muted);">keywords: ${(item.matched_keywords || []).join(', ') || 'none'}</div>
      <ul class="tight">${(item.reviewer_guidance || []).map((entry) => `<li>${entry}</li>`).join('')}</ul>
    </div>
  `);
  renderList('similarCases', data.similar_cases, (item) => `
    <div class="mini-card">
      <strong>${item.case_id}</strong>
      <div>${item.final_action} · ${item.category} · ${item.queue_name}</div>
      <div style="margin-top:8px;color:var(--muted);">${item.comment_text}</div>
      <div style="margin-top:8px;color:var(--muted);">${item.summary}</div>
    </div>
  `, 'No similar cases for this review.');
  renderList('recommendedActions', data.recommended_actions, (item) => `<div class="mini-card">${item}</div>`);
  renderList('reviewNotes', data.review_notes, (item) => `<div class="mini-card">${item}</div>`);
  renderList('toolTrace', data.tool_trace, (item) => `
    <div class="mini-card">
      <strong>${item.tool_name}</strong>
      <div class="mono">${JSON.stringify(item.arguments)}</div>
      <div style="margin-top:8px;color:var(--muted);">${item.result_summary}</div>
    </div>
  `, 'No tool trace.');
}

async function bootstrap() {
  const [presetResponse, summaryResponse] = await Promise.all([
    fetch('/review-presets'),
    fetch('/dashboard-summary'),
  ]);
  presets = await presetResponse.json();
  const summary = await summaryResponse.json();
  renderMetrics(summary);
  if (presets.length) {
    applyPreset(presets[0]);
    await activatePreset(presets[0].case_id);
  }
}

bootstrap();
"""
    return _render_page("CommentOps Review Workbench", "demo", body, scripts)


def render_workflow_page() -> str:
    body = """
<section class="hero">
  <div class="eyebrow">Interactive Review Workflow</div>
  <h1>在线链路：这套审核系统为什么本质上是 Agent</h1>
  <div class="subcopy">
    这里把完整链路拆成两个泳道：<span class="mono">online_review</span> 和 <span class="mono">offline_optimization</span>。
    上方选案例，左下角是可缩放的主画布，右侧只承载当前运行和节点解释，不再和主链路争抢视觉中心。
    点击节点后会看到该步骤的职责、为什么它属于 Agent 工作流、当前实现方式，以及下一步优化思路。
  </div>
  <div class="hero-points">
    <span class="chip">Zoomable SVG canvas</span>
    <span class="chip">Bottom-left minimap</span>
    <span class="chip">Policy-grounded chain</span>
    <span class="chip">Eval-aware workflow</span>
  </div>
</section>

<div class="workflow-layout">
  <div class="workflow-left">
    <div class="panel">
      <div class="status">Preset Cases</div>
      <div class="muted">先切换案例，再到左下角画布里看完整在线链路和离线优化闭环。</div>
      <div id="workflowPresetRail" class="preset-rail"></div>
    </div>
    <div class="panel workflow-canvas-panel">
      <div class="workflow-panel-head">
        <div>
          <div class="status">Zoomable Workflow Canvas</div>
          <div class="workflow-panel-copy">
            画布基于节点绝对坐标渲染，而不是按钮列表。这样在线链路本身就是页面主角，`Current Run` 和 `Node Detail`
            只负责解释当前状态，不再遮挡主路径。
          </div>
        </div>
        <div class="workflow-controls">
          <div id="workflowViewportStats" class="workflow-pill">loading viewport</div>
          <button id="zoomOutView" class="secondary" type="button" onclick="zoomOutViewAction()">缩小</button>
          <button id="zoomInView" class="secondary" type="button" onclick="zoomInViewAction()">放大</button>
          <button id="resetView" class="primary" type="button" onclick="resetViewAction()">重置视图</button>
        </div>
      </div>
      <div class="workflow-hint">
        <span class="workflow-pill">拖动画布</span>
        <span class="workflow-pill">滚轮缩放</span>
        <span class="workflow-pill">点击节点看详情</span>
        <span>左下角 minimap 用于快速跳转，避免右侧运行信息遮挡完整链路。</span>
      </div>
      <div id="workflowCanvasShell" class="workflow-canvas-shell">
        <div class="workflow-canvas-grid"></div>
        <div class="workflow-canvas-tint"></div>
        <div id="workflowViewport" class="workflow-viewport">
          <svg id="workflowSvg" class="workflow-svg" xmlns="http://www.w3.org/2000/svg" aria-label="Comment moderation workflow graph"></svg>
        </div>
        <div class="workflow-minimap-panel">
          <div class="workflow-minimap-label">画布总览</div>
          <div id="workflowMinimap"></div>
        </div>
      </div>
    </div>
  </div>
  <div class="workflow-right">
    <div class="panel">
      <div class="status">Current Run</div>
      <div id="workflowRunSummary" class="empty">选择一个案例后，会展示当前在线链路结果。</div>
    </div>
    <div class="panel">
      <div class="status">Node Detail</div>
      <div id="nodeDetail" class="empty">点击左侧链路节点查看说明。</div>
    </div>
    <div class="panel">
      <div class="status">Implementation References</div>
      <div id="workflowReferences" class="card-list"></div>
    </div>
  </div>
</div>
"""
    scripts = """
let workflowGraph = null;
let workflowPresets = [];
let currentReview = null;
let currentNodeId = 'decision_policy';
let currentPresetId = null;
let currentSummary = null;
let graphSize = { width: 1760, height: 560 };
let viewport = { x: 0, y: 0, zoom: 0 };
let defaultViewport = { x: 0, y: 0, zoom: 0 };
let dragState = null;
let suppressNodeClick = false;
let minimapState = null;

const ONLINE_LANE_ID = 'online_review';
const OFFLINE_LANE_ID = 'offline_optimization';
const NODE_WIDTH = 194;
const NODE_HEIGHT = 108;
const MIN_ZOOM = 0.34;
const MAX_ZOOM = 1.72;
const ZOOM_STEP = 1.15;

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}

function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function wrapNodeText(text, limit = 16, maxLines = 2) {
  const source = String(text || '').trim();
  if (!source) return [];
  const lines = [];
  let cursor = 0;
  while (cursor < source.length && lines.length < maxLines) {
    const next = source.slice(cursor, cursor + limit);
    cursor += limit;
    lines.push(next);
  }
  if (cursor < source.length && lines.length) {
    const last = lines[lines.length - 1];
    lines[lines.length - 1] = `${last.slice(0, Math.max(1, limit - 1))}…`;
  }
  return lines;
}

function nodeById(nodeId) {
  return (workflowGraph?.nodes || []).find((item) => item.id === nodeId);
}

function activeNodeIds() {
  if (!workflowGraph) return [];
  const onlineIds = workflowGraph.nodes.filter((item) => item.lane === ONLINE_LANE_ID).map((item) => item.id);
  const offlineIds = workflowGraph.nodes.filter((item) => item.lane === OFFLINE_LANE_ID).map((item) => item.id);
  return currentReview ? [...onlineIds, ...offlineIds] : onlineIds;
}

function computeGraphSize() {
  const nodes = workflowGraph?.nodes || [];
  const width = Math.max(...nodes.map((node) => node.position.x + NODE_WIDTH), 1500) + 110;
  const height = Math.max(...nodes.map((node) => node.position.y + NODE_HEIGHT), 430) + 90;
  graphSize = { width, height };
}

function computeLaneBand(lane) {
  const laneNodes = workflowGraph.nodes.filter((item) => item.lane === lane);
  const top = Math.min(...laneNodes.map((item) => item.position.y)) - 26;
  const bottom = Math.max(...laneNodes.map((item) => item.position.y + NODE_HEIGHT)) + 26;
  return {
    y: top,
    height: bottom - top,
    css: lane === ONLINE_LANE_ID ? 'online' : 'offline',
  };
}

function renderWorkflowPresets() {
  const rail = document.getElementById('workflowPresetRail');
  rail.innerHTML = workflowPresets.map((preset) => `
    <div class="preset-card ${preset.case_id === currentPresetId ? 'active' : ''}" onclick="selectWorkflowPreset('${preset.case_id}')">
      <div class="preset-meta">${escapeHtml(preset.expected_queue || 'no-queue')}</div>
      <h4>${escapeHtml(preset.case_id)}</h4>
      <div class="muted">${escapeHtml(preset.comment_text)}</div>
    </div>
  `).join('');
}

function renderWorkflowReferences() {
  const root = document.getElementById('workflowReferences');
  root.innerHTML = (workflowGraph.references || []).map((item) => `
    <div class="mini-card">
      <strong><a href="${item.url}" target="_blank" rel="noreferrer">${escapeHtml(item.title)}</a></strong>
      ${item.note ? `<div class="reference-note">${escapeHtml(item.note)}</div>` : ''}
      <div class="reference-tag">${item.url.includes('developer.mozilla.org') || item.url.includes('reactflow.dev') || item.url.includes('mermaid.js.org') ? 'interaction reference' : 'business / eval reference'}</div>
    </div>
  `).join('');
}

function edgePath(fromNode, toNode) {
  const fromCenter = {
    x: fromNode.position.x + NODE_WIDTH / 2,
    y: fromNode.position.y + NODE_HEIGHT / 2,
  };
  const toCenter = {
    x: toNode.position.x + NODE_WIDTH / 2,
    y: toNode.position.y + NODE_HEIGHT / 2,
  };
  const dx = toCenter.x - fromCenter.x;
  const dy = toCenter.y - fromCenter.y;

  if (Math.abs(dx) >= Math.abs(dy)) {
    const movingRight = dx >= 0;
    const start = movingRight
      ? { x: fromNode.position.x + NODE_WIDTH, y: fromCenter.y }
      : { x: fromNode.position.x, y: fromCenter.y };
    const end = movingRight
      ? { x: toNode.position.x, y: toCenter.y }
      : { x: toNode.position.x + NODE_WIDTH, y: toCenter.y };
    const control = Math.max(64, Math.abs(dx) * 0.42);
    return `M ${start.x} ${start.y} C ${start.x + (movingRight ? control : -control)} ${start.y}, ${end.x - (movingRight ? control : -control)} ${end.y}, ${end.x} ${end.y}`;
  }

  const movingDown = dy >= 0;
  const start = movingDown
    ? { x: fromCenter.x, y: fromNode.position.y + NODE_HEIGHT }
    : { x: fromCenter.x, y: fromNode.position.y };
  const end = movingDown
    ? { x: toCenter.x, y: toNode.position.y }
    : { x: toCenter.x, y: toNode.position.y + NODE_HEIGHT };
  const control = Math.max(78, Math.abs(dy) * 0.50);
  return `M ${start.x} ${start.y} C ${start.x} ${start.y + (movingDown ? control : -control)}, ${end.x} ${end.y - (movingDown ? control : -control)}, ${end.x} ${end.y}`;
}

function renderLaneBands() {
  return workflowGraph.lanes.map((lane) => {
    const band = computeLaneBand(lane);
    return `
      <g>
        <rect class="lane-band ${band.css}" x="32" y="${band.y}" width="${graphSize.width - 64}" height="${band.height}" rx="28" ry="28"></rect>
        <text class="lane-label" x="58" y="${band.y + 28}">${lane}</text>
      </g>
    `;
  }).join('');
}

function renderEdges() {
  const activeIds = new Set(activeNodeIds());
  return workflowGraph.edges.map((edge) => {
    const fromNode = nodeById(edge.from);
    const toNode = nodeById(edge.to);
    if (!fromNode || !toNode) return '';
    const active = activeIds.has(edge.from) && activeIds.has(edge.to);
    const current = edge.from === currentNodeId || edge.to === currentNodeId;
    const markerId = current ? 'workflowArrowCurrent' : active ? 'workflowArrowActive' : 'workflowArrow';
    return `
      <path class="workflow-edge ${active ? 'active' : ''} ${current ? 'current' : ''}" d="${edgePath(fromNode, toNode)}" marker-end="url(#${markerId})"></path>
    `;
  }).join('');
}

function renderNodes() {
  const activeIds = new Set(activeNodeIds());
  return workflowGraph.nodes.map((node) => {
    const subtitleLines = wrapNodeText(node.subtitle, 16, 2);
    const subtitleTspans = subtitleLines.map((line, index) => `
      <tspan x="20" dy="${index === 0 ? 0 : 16}">${escapeHtml(line)}</tspan>
    `).join('');
    return `
      <g class="workflow-node ${activeIds.has(node.id) ? 'active' : ''} ${node.id === currentNodeId ? 'current' : ''}" transform="translate(${node.position.x}, ${node.position.y})" onclick="focusNode('${node.id}', true)">
        <rect width="${NODE_WIDTH}" height="${NODE_HEIGHT}" rx="22" ry="22"></rect>
        <text class="node-id" x="20" y="22">${escapeHtml(node.id)}</text>
        <text class="node-title" x="20" y="50">${escapeHtml(node.title)}</text>
        <text class="node-subtitle" x="20" y="74">${subtitleTspans}</text>
      </g>
    `;
  }).join('');
}

function updateViewportTransform() {
  const viewportRoot = document.getElementById('workflowViewport');
  if (!viewportRoot) return;
  viewportRoot.style.width = `${graphSize.width}px`;
  viewportRoot.style.height = `${graphSize.height}px`;
  viewportRoot.style.transform = `translate(${viewport.x}px, ${viewport.y}px) scale(${viewport.zoom})`;
}

function updateViewportStats() {
  const stats = document.getElementById('workflowViewportStats');
  if (!stats) return;
  stats.textContent = `zoom ${Math.round(viewport.zoom * 100)}%`;
}

function renderMinimap() {
  const shell = document.getElementById('workflowCanvasShell');
  const root = document.getElementById('workflowMinimap');
  if (!shell || !root || !workflowGraph) return;

  const minimapWidth = root.clientWidth || 212;
  const minimapHeight = root.clientHeight || 134;
  const scale = Math.min((minimapWidth - 20) / graphSize.width, (minimapHeight - 20) / graphSize.height);
  const offsetX = (minimapWidth - graphSize.width * scale) / 2;
  const offsetY = (minimapHeight - graphSize.height * scale) / 2;
  minimapState = { scale, offsetX, offsetY };

  const activeIds = new Set(activeNodeIds());
  const visibleGraphX = clamp(-viewport.x / viewport.zoom, 0, graphSize.width);
  const visibleGraphY = clamp(-viewport.y / viewport.zoom, 0, graphSize.height);
  const visibleGraphWidth = Math.min(shell.clientWidth / viewport.zoom, graphSize.width);
  const visibleGraphHeight = Math.min(shell.clientHeight / viewport.zoom, graphSize.height);

  const edges = (workflowGraph.edges || []).map((edge) => {
    const fromNode = nodeById(edge.from);
    const toNode = nodeById(edge.to);
    if (!fromNode || !toNode) return '';
    const fromX = (fromNode.position.x + NODE_WIDTH / 2) * scale + offsetX;
    const fromY = (fromNode.position.y + NODE_HEIGHT / 2) * scale + offsetY;
    const toX = (toNode.position.x + NODE_WIDTH / 2) * scale + offsetX;
    const toY = (toNode.position.y + NODE_HEIGHT / 2) * scale + offsetY;
    return `<line x1="${fromX}" y1="${fromY}" x2="${toX}" y2="${toY}" stroke="${activeIds.has(edge.from) && activeIds.has(edge.to) ? 'rgba(36,72,90,0.55)' : 'rgba(90,104,119,0.28)'}" stroke-width="2" />`;
  }).join('');

  const nodes = workflowGraph.nodes.map((node) => `
    <rect x="${node.position.x * scale + offsetX}" y="${node.position.y * scale + offsetY}" width="${NODE_WIDTH * scale}" height="${NODE_HEIGHT * scale}" rx="7" ry="7" fill="${node.id === currentNodeId ? 'rgba(196,90,56,0.42)' : activeIds.has(node.id) ? 'rgba(36,72,90,0.22)' : 'rgba(18,30,44,0.12)'}" stroke="${node.id === currentNodeId ? 'rgba(196,90,56,0.82)' : 'rgba(18,30,44,0.14)'}" stroke-width="1" />
  `).join('');

  root.innerHTML = `
    <svg width="${minimapWidth}" height="${minimapHeight}" viewBox="0 0 ${minimapWidth} ${minimapHeight}" xmlns="http://www.w3.org/2000/svg">
      <rect x="0" y="0" width="${minimapWidth}" height="${minimapHeight}" rx="14" ry="14" fill="rgba(255,255,255,0.94)" />
      <rect x="${offsetX}" y="${offsetY}" width="${graphSize.width * scale}" height="${graphSize.height * scale}" rx="12" ry="12" fill="rgba(36,72,90,0.04)" stroke="rgba(18,30,44,0.08)" stroke-width="1" />
      ${edges}
      ${nodes}
      <rect x="${visibleGraphX * scale + offsetX}" y="${visibleGraphY * scale + offsetY}" width="${visibleGraphWidth * scale}" height="${visibleGraphHeight * scale}" rx="12" ry="12" fill="rgba(196,90,56,0.08)" stroke="rgba(196,90,56,0.92)" stroke-width="2.2" />
    </svg>
  `;
}

function applyViewport() {
  updateViewportTransform();
  updateViewportStats();
  renderMinimap();
}

function fitViewToGraph() {
  const shell = document.getElementById('workflowCanvasShell');
  if (!shell) return;
  const padding = 48;
  const zoom = clamp(
    Math.min((shell.clientWidth - padding * 2) / graphSize.width, (shell.clientHeight - padding * 2) / graphSize.height),
    MIN_ZOOM,
    1,
  );
  const x = (shell.clientWidth - graphSize.width * zoom) / 2;
  const y = (shell.clientHeight - graphSize.height * zoom) / 2;
  defaultViewport = { x, y, zoom };
  viewport = { ...defaultViewport };
  applyViewport();
}

function centerViewportOnGraphPoint(graphX, graphY, zoom = viewport.zoom) {
  const shell = document.getElementById('workflowCanvasShell');
  if (!shell) return;
  viewport = {
    x: shell.clientWidth / 2 - graphX * zoom,
    y: shell.clientHeight / 2 - graphY * zoom,
    zoom,
  };
  applyViewport();
}

function centerOnNode(nodeId) {
  const node = nodeById(nodeId);
  if (!node) return;
  centerViewportOnGraphPoint(node.position.x + NODE_WIDTH / 2, node.position.y + NODE_HEIGHT / 2, viewport.zoom);
}

function zoomAroundPoint(screenX, screenY, factor) {
  const shell = document.getElementById('workflowCanvasShell');
  if (!shell) return;
  const rect = shell.getBoundingClientRect();
  const localX = screenX - rect.left;
  const localY = screenY - rect.top;
  const graphX = (localX - viewport.x) / viewport.zoom;
  const graphY = (localY - viewport.y) / viewport.zoom;
  const nextZoom = clamp(viewport.zoom * factor, MIN_ZOOM, MAX_ZOOM);
  viewport = {
    x: localX - graphX * nextZoom,
    y: localY - graphY * nextZoom,
    zoom: nextZoom,
  };
  applyViewport();
}

function zoomInViewAction() {
  const shell = document.getElementById('workflowCanvasShell');
  if (!shell) return;
  const rect = shell.getBoundingClientRect();
  zoomAroundPoint(rect.left + rect.width / 2, rect.top + rect.height / 2, ZOOM_STEP);
}

function zoomOutViewAction() {
  const shell = document.getElementById('workflowCanvasShell');
  if (!shell) return;
  const rect = shell.getBoundingClientRect();
  zoomAroundPoint(rect.left + rect.width / 2, rect.top + rect.height / 2, 1 / ZOOM_STEP);
}

function resetViewAction() {
  viewport = { ...defaultViewport };
  applyViewport();
}

function startCanvasDrag(event) {
  if (event.button !== 0) return;
  if (event.target.closest('.workflow-minimap-panel') || event.target.closest('button') || event.target.closest('a')) return;
  dragState = {
    x: event.clientX,
    y: event.clientY,
    viewportX: viewport.x,
    viewportY: viewport.y,
    moved: false,
  };
}

function moveCanvasDrag(event) {
  if (!dragState) return;
  const shell = document.getElementById('workflowCanvasShell');
  const dx = event.clientX - dragState.x;
  const dy = event.clientY - dragState.y;
  if (Math.abs(dx) > 3 || Math.abs(dy) > 3) {
    dragState.moved = true;
    suppressNodeClick = true;
    shell?.classList.add('dragging');
  }
  viewport = {
    x: dragState.viewportX + dx,
    y: dragState.viewportY + dy,
    zoom: viewport.zoom,
  };
  applyViewport();
}

function endCanvasDrag() {
  const shell = document.getElementById('workflowCanvasShell');
  if (dragState?.moved) {
    window.setTimeout(() => {
      suppressNodeClick = false;
    }, 0);
  } else {
    suppressNodeClick = false;
  }
  dragState = null;
  shell?.classList.remove('dragging');
}

function handleCanvasWheel(event) {
  event.preventDefault();
  zoomAroundPoint(event.clientX, event.clientY, event.deltaY < 0 ? 1.08 : 0.92);
}

function handleMinimapClick(event) {
  if (!minimapState) return;
  const rect = event.currentTarget.getBoundingClientRect();
  const graphX = clamp((event.clientX - rect.left - minimapState.offsetX) / minimapState.scale, 0, graphSize.width);
  const graphY = clamp((event.clientY - rect.top - minimapState.offsetY) / minimapState.scale, 0, graphSize.height);
  centerViewportOnGraphPoint(graphX, graphY, viewport.zoom);
}

function bindCanvasInteractions() {
  const shell = document.getElementById('workflowCanvasShell');
  const minimap = document.getElementById('workflowMinimap');
  if (!shell || shell.dataset.bound === 'true') return;
  shell.dataset.bound = 'true';
  shell.addEventListener('pointerdown', startCanvasDrag);
  shell.addEventListener('wheel', handleCanvasWheel, { passive: false });
  minimap?.addEventListener('click', handleMinimapClick);
  window.addEventListener('pointermove', moveCanvasDrag);
  window.addEventListener('pointerup', endCanvasDrag);
  window.addEventListener('pointercancel', endCanvasDrag);
  window.addEventListener('resize', renderMinimap);
}

function renderWorkflowCanvas() {
  if (!workflowGraph) return;
  computeGraphSize();
  const viewportRoot = document.getElementById('workflowViewport');
  const svg = document.getElementById('workflowSvg');
  if (!viewportRoot || !svg) return;

  viewportRoot.style.width = `${graphSize.width}px`;
  viewportRoot.style.height = `${graphSize.height}px`;
  svg.setAttribute('width', String(graphSize.width));
  svg.setAttribute('height', String(graphSize.height));
  svg.setAttribute('viewBox', `0 0 ${graphSize.width} ${graphSize.height}`);

  svg.innerHTML = `
    <defs>
      <marker id="workflowArrow" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="12" markerHeight="12" orient="auto-start-reverse">
        <path d="M 0 0 L 12 6 L 0 12 z" fill="rgba(90,104,119,0.36)"></path>
      </marker>
      <marker id="workflowArrowActive" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="12" markerHeight="12" orient="auto-start-reverse">
        <path d="M 0 0 L 12 6 L 0 12 z" fill="rgba(36,72,90,0.56)"></path>
      </marker>
      <marker id="workflowArrowCurrent" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="12" markerHeight="12" orient="auto-start-reverse">
        <path d="M 0 0 L 12 6 L 0 12 z" fill="rgba(196,90,56,0.78)"></path>
      </marker>
    </defs>
    ${renderLaneBands()}
    ${renderEdges()}
    ${renderNodes()}
  `;

  if (!defaultViewport.zoom || !viewport.zoom) {
    fitViewToGraph();
  } else {
    applyViewport();
  }
}

function nodeRuntimeDetail(nodeId) {
  if (!currentReview) return '当前还没有运行结果，先选择一个案例。';
  const map = {
    case_intake: `case_id=${currentReview.case_id}, reporters=${currentReview.risk_signals?.find((item) => item.signal === 'crowd_reports')?.value || 0}`,
    context_loader: `thread_context_count=${(currentReview.thread_context || []).length}`,
    policy_retrieval: `matched_policies=${(currentReview.matched_policies || []).map((item) => item.title).join(', ') || 'none'}`,
    similar_case_retrieval: `similar_cases=${(currentReview.similar_cases || []).length}`,
    risk_synthesis: `risk_signals=${(currentReview.risk_signals || []).map((item) => item.signal).join(', ') || 'none'}`,
    decision_policy: `action=${currentReview.decision.action}, confidence=${Math.round(currentReview.decision.confidence * 100)}%`,
    queue_routing: `queue=${currentReview.queue_routing.queue_name}, priority=${currentReview.queue_routing.priority}`,
    reviewer_handoff: `recommended_actions=${(currentReview.recommended_actions || []).length}`,
    eval_snapshot: currentSummary ? `queue_accuracy=${Math.round(currentSummary.queue_routing_accuracy * 100)}%, human_review_rate=${Math.round(currentSummary.human_review_rate * 100)}%` : 'summary unavailable',
    failure_review: '当前 failure review 已导出为 artifact，用于定位人工压力和申诉敏感样本。',
    sft_export: '当前 SFT 样本包含 decision、queue_routing、risk_signals、similar_cases。',
    preference_export: '当前 preference 样本和 failure review 一起支撑后续 reward / preference 优化。',
  };
  const trace = (currentReview.tool_trace || []).find((item) => {
    const traceMap = {
      context_loader: 'load_comment_context',
      policy_retrieval: 'retrieve_policy_clauses',
      similar_case_retrieval: 'search_similar_cases',
      risk_synthesis: 'synthesize_risk_signals',
      decision_policy: 'aggregate_decision',
      queue_routing: 'route_review_queue',
    };
    return item.tool_name === traceMap[nodeId];
  });
  return trace ? `${map[nodeId] || ''} | trace=${trace.result_summary}` : (map[nodeId] || 'No runtime detail.');
}

function renderNodeDetail() {
  const node = workflowGraph.nodes.find((item) => item.id === currentNodeId);
  if (!node) return;
  document.getElementById('nodeDetail').innerHTML = `
    <div class="workflow-runtime-grid">
      <div class="runtime-card">
        <div class="preset-meta">${escapeHtml(node.lane)}</div>
        <h3>${escapeHtml(node.title)}</h3>
        <div class="muted">${escapeHtml(node.subtitle)}</div>
        <p class="subcopy" style="margin-top:10px;">${escapeHtml(node.summary)}</p>
      </div>
      <div class="runtime-card">
        <strong>为什么它属于 Agent 链路</strong>
        <div class="muted" style="margin-top:8px;">${escapeHtml(node.why_agentic)}</div>
      </div>
      <div class="runtime-card">
        <strong>当前实现</strong>
        <div class="muted" style="margin-top:8px;">${escapeHtml(node.current_impl)}</div>
      </div>
      <div class="runtime-card">
        <strong>输入 / 输出</strong>
        <div class="mono" style="margin-top:8px;">in: ${escapeHtml((node.inputs || []).join(', '))}</div>
        <div class="mono" style="margin-top:8px;">out: ${escapeHtml((node.outputs || []).join(', '))}</div>
      </div>
      <div class="runtime-card">
        <strong>当前在线运行结果</strong>
        <div class="muted" style="margin-top:8px;">${escapeHtml(nodeRuntimeDetail(node.id))}</div>
      </div>
      <div class="runtime-card">
        <strong>优化思路</strong>
        <ul class="tight">${(node.optimize_next || []).map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul>
      </div>
    </div>
  `;
}

function renderRunSummary() {
  if (!currentReview) {
    document.getElementById('workflowRunSummary').innerHTML = '选择一个案例后，会展示当前在线链路结果。';
    return;
  }
  document.getElementById('workflowRunSummary').innerHTML = `
    <div class="workflow-runtime-grid">
      <div class="runtime-card">
        <strong>${escapeHtml(currentReview.case_id)}</strong>
        <div class="muted" style="margin-top:8px;">${escapeHtml(currentReview.comment_text)}</div>
        <div style="margin-top:10px;" class="chip-row">
          <span class="chip">${escapeHtml(currentReview.decision.action)}</span>
          <span class="chip">${escapeHtml(currentReview.decision.primary_category)}</span>
          <span class="chip">${escapeHtml(currentReview.queue_routing.queue_name)}</span>
        </div>
      </div>
      <div class="runtime-card">
        <strong>在线结果摘要</strong>
        <ul class="tight">
          <li>matched_policies=${(currentReview.matched_policies || []).length}</li>
          <li>risk_signals=${(currentReview.risk_signals || []).length}</li>
          <li>similar_cases=${(currentReview.similar_cases || []).length}</li>
          <li>stop_reason=${escapeHtml(currentReview.stop_reason)}</li>
        </ul>
      </div>
      <div class="runtime-card">
        <strong>评测闭环提示</strong>
        <ul class="tight">
          <li>queue_accuracy=${currentSummary ? Math.round(currentSummary.queue_routing_accuracy * 100) : '--'}%</li>
          <li>human_review_rate=${currentSummary ? Math.round(currentSummary.human_review_rate * 100) : '--'}%</li>
          <li>auto_reject_rate=${currentSummary ? Math.round(currentSummary.auto_reject_rate * 100) : '--'}%</li>
        </ul>
      </div>
      <div class="runtime-card">
        <strong>Tool Trace</strong>
        <ul class="tight">${(currentReview.tool_trace || []).map((item) => `<li>${escapeHtml(item.tool_name)} -> ${escapeHtml(item.result_summary)}</li>`).join('')}</ul>
      </div>
    </div>
  `;
}

function focusNode(nodeId, shouldCenter = false) {
  if (suppressNodeClick) return;
  currentNodeId = nodeId;
  renderWorkflowCanvas();
  renderNodeDetail();
  if (shouldCenter) {
    centerOnNode(nodeId);
  }
}

async function selectWorkflowPreset(caseId) {
  const preset = workflowPresets.find((item) => item.case_id === caseId);
  if (!preset) return;
  currentPresetId = caseId;
  renderWorkflowPresets();
  const response = await fetch('/review', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(preset),
  });
  currentReview = await response.json();
  renderWorkflowCanvas();
  renderNodeDetail();
  renderRunSummary();
}

async function bootstrapWorkflow() {
  const [graphResponse, presetResponse, summaryResponse] = await Promise.all([
    fetch('/workflow-graph'),
    fetch('/review-presets'),
    fetch('/dashboard-summary'),
  ]);
  workflowGraph = await graphResponse.json();
  workflowPresets = await presetResponse.json();
  currentSummary = await summaryResponse.json();
  renderWorkflowReferences();
  renderWorkflowPresets();
  bindCanvasInteractions();
  renderWorkflowCanvas();
  renderNodeDetail();
  renderRunSummary();
  if (workflowPresets.length) {
    await selectWorkflowPreset(workflowPresets[0].case_id);
  }
}

bootstrapWorkflow();
"""
    return _render_page("Interactive Review Workflow", "workflow", body, scripts)


def render_project_overview_page() -> str:
    payload = project_overview_payload()
    storyline_html = "".join(
        f"""
        <div class="overview-card">
          <div class="status">{item['status']}</div>
          <h3>{item['title']}</h3>
          <p>{item['body']}</p>
          <ul class="tight">{''.join(f'<li>{point}</li>' for point in item['items'])}</ul>
        </div>
        """
        for item in payload["storyline"]
    )
    architecture_html = "".join(
        f"""
        <div class="comparison-card">
          <h3>{item['name']}</h3>
          <div class="fit-badge">适配度 {item['fit']}</div>
          <p>{item['why']}</p>
          <ul class="tight">{''.join(f'<li>{point}</li>' for point in item['tradeoffs'])}</ul>
        </div>
        """
        for item in payload["architecture_options"]
    )
    langgraph_items = payload["langgraph_mapping"]
    metric_html = "".join(
        f"""
        <div class="metric-card-extended">
          <h3>{group['title']}</h3>
          <ul class="tight">{''.join(f'<li>{item}</li>' for item in group['items'])}</ul>
        </div>
        """
        for group in payload["metric_groups"]
    )
    deliverables_html = "".join(
        f"""
        <div class="deliverable-card">
          <div class="status">{item['kind']}</div>
          <h3>{item['title']}</h3>
          <p>{item['purpose']}</p>
          <div class="doc-path">{item['path']}</div>
        </div>
        """
        for item in payload["deliverables"]
    )
    flow_html = "".join(f"<li>{item}</li>" for item in payload["presentation_flow"])
    body = f"""
<section class="hero">
  <div class="eyebrow">项目全景</div>
  <h1>把 CommentOps Agent 讲成一个完整业务系统</h1>
  <div class="subcopy">{payload['summary']}</div>
  <div class="hero-points">{''.join(f'<span class="chip">{item}</span>' for item in payload['hero_chips'])}</div>
</section>

<div class="panel">
  <div class="status">主叙事</div>
  <div class="overview-grid">{storyline_html}</div>
</div>

<div class="panel" style="margin-top:18px;">
  <div class="status">架构选型对比</div>
  <div class="comparison-grid">{architecture_html}</div>
</div>

<div class="section-grid" style="margin-top:18px;">
  <div class="panel">
    <div class="status">LangGraph 映射</div>
    <div class="mini-card">
      <strong>为什么偏向 Graph API / StateGraph</strong>
      <ul class="tight">{''.join(f'<li>{item}</li>' for item in langgraph_items['why_graph_api'])}</ul>
    </div>
    <div class="mini-card" style="margin-top:14px;">
      <strong>核心状态字段</strong>
      <div class="mono" style="margin-top:8px;">{', '.join(langgraph_items['state_fields'])}</div>
    </div>
    <div class="mini-card" style="margin-top:14px;">
      <strong>节点拆法</strong>
      <ul class="tight">{''.join(f'<li>{item}</li>' for item in langgraph_items['nodes'])}</ul>
    </div>
    <div class="mini-card" style="margin-top:14px;">
      <strong>interrupt / human review 条件</strong>
      <ul class="tight">{''.join(f'<li>{item}</li>' for item in langgraph_items['interrupts'])}</ul>
    </div>
  </div>
  <div class="stack">
    <div class="panel">
      <div class="status">评测矩阵</div>
      <div class="metric-grid">{metric_html}</div>
    </div>
    <div class="overview-band">
      <div class="status">推荐讲法</div>
      <h3>从业务到闭环的五步表达</h3>
      <ol class="tight">{flow_html}</ol>
    </div>
  </div>
</div>

<div class="panel" style="margin-top:18px;">
  <div class="status">文档与产出</div>
  <div class="deliverable-grid">{deliverables_html}</div>
</div>
"""
    return _render_page("项目全景", "overview", body, "")


def render_agent_evolution_page() -> str:
    payload = agent_evolution_payload()
    snapshot = payload["maturity_snapshot"]
    snapshot_html = "".join(
        f"""
        <div class="overview-card">
          <div class="status">{label}</div>
          <h3>{title}</h3>
          <ul class="tight">{''.join(f'<li>{item}</li>' for item in items)}</ul>
        </div>
        """
        for label, title, items in [
            ("Already Built", "已经具备的工程骨架", snapshot["already_built"]),
            ("Known Gaps", "当前最关键短板", snapshot["known_gaps"]),
            ("Next Priorities", "下一步最该补的能力", snapshot["next_priorities"]),
        ]
    )
    layers_html = "".join(
        f"""
        <div class="comparison-card">
          <h3>{item['name']}</h3>
          <p><strong>解决的问题：</strong>{item['problem']}</p>
          <ul class="tight">
            <li><strong>当前：</strong>{item['current']}</li>
            <li><strong>下一步：</strong>{item['next']}</li>
            <li><strong>关键指标：</strong>{item['metric']}</li>
          </ul>
        </div>
        """
        for item in payload["engineering_layers"]
    )
    metric_html = "".join(
        f"""
        <div class="metric-card-extended">
          <div class="status">{group['status']}</div>
          <h3>{group['title']}</h3>
          <ul class="tight">{''.join(f'<li>{item}</li>' for item in group['items'])}</ul>
        </div>
        """
        for group in payload["metric_groups"]
    )
    roadmap_html = "".join(
        f"""
        <div class="deliverable-card">
          <div class="status">{item['name']}</div>
          <h3>{item['title']}</h3>
          <p><strong>重点：</strong>{item['focus']}</p>
          <p><strong>门槛：</strong>{item['gate']}</p>
          <div class="doc-path">ROI：{item['roi']}</div>
        </div>
        """
        for item in payload["roadmap_stages"]
    )
    roi_html = "".join(
        f"""
        <div class="overview-card">
          <div class="status">ROI</div>
          <h3>{item['title']}</h3>
          <p>{item['why']}</p>
          <ul class="tight">{''.join(f'<li>{point}</li>' for point in item['items'])}</ul>
        </div>
        """
        for item in payload["roi_buckets"]
    )
    mappings_html = "".join(
        f"""
        <div class="comparison-card">
          <div class="status">{item['source']}</div>
          <h3>{item['source']} 给我们的设计约束</h3>
          <p><strong>大厂经验：</strong>{item['lesson']}</p>
          <p><strong>落到当前 Agent：</strong>{item['application']}</p>
        </div>
        """
        for item in payload["industry_mappings"]
    )
    references_html = "".join(
        f"""
        <div class="source-card">
          <strong><a href="{item['url']}" target="_blank" rel="noreferrer">{item['label']}</a></strong>
          <div class="muted" style="margin-top:8px;">{item['why_it_matters']}</div>
        </div>
        """
        for item in payload["references"]
    )
    body = f"""
<section class="hero">
  <div class="eyebrow">工程进化</div>
  <h1>从能跑的审核 Agent，到值得讲的工程化系统</h1>
  <div class="subcopy">{payload['summary']}</div>
  <div class="hero-points">{''.join(f'<span class="chip">{item}</span>' for item in payload['hero_chips'])}</div>
</section>

<div class="overview-band">
  <div class="status">当前成熟度</div>
  <h3>{snapshot['headline']}</h3>
  <div class="muted">{snapshot['stage']}</div>
</div>

<div class="panel" style="margin-top:18px;">
  <div class="status">成熟度快照</div>
  <div class="overview-grid">{snapshot_html}</div>
</div>

<div class="panel" style="margin-top:18px;">
  <div class="status">工程分层</div>
  <h3>优化先分层，再决定是修 prompt、修规则、修路由，还是进训练</h3>
  <div class="comparison-grid">{layers_html}</div>
</div>

<div class="panel" style="margin-top:18px;">
  <div class="status">评测指标</div>
  <h3>评测指标不能只看 accuracy，还要覆盖效率、稳定性和 ROI</h3>
  <div class="metric-grid">{metric_html}</div>
</div>

<div class="panel" style="margin-top:18px;">
  <div class="status">Agent 演化路线</div>
  <h3>从 V0 到 V5，先做高 ROI 升级，再考虑复杂 agentic patterns</h3>
  <div class="deliverable-grid">{roadmap_html}</div>
</div>

<div class="panel" style="margin-top:18px;">
  <div class="status">ROI 排序</div>
  <h3>不是所有高级能力都该现在做，ROI 决定迭代顺序</h3>
  <div class="overview-grid">{roi_html}</div>
</div>

<div class="panel" style="margin-top:18px;">
  <div class="status">大厂经验映射</div>
  <h3>结合 TikTok、Meta、YouTube、OpenAI、Anthropic 的公开信号校正设计</h3>
  <div class="comparison-grid">{mappings_html}</div>
</div>

<div class="panel" style="margin-top:18px;">
  <div class="status">优质信息源</div>
  <div class="timeline">{references_html}</div>
</div>
"""
    return _render_page("工程进化", "evolution", body, "")


def render_research_log_page() -> str:
    payload = research_log_payload()
    sections_html = "".join(
        f"""
        <div class="mini-card">
          <h3>{section['title']}</h3>
          <ul class="tight">{''.join(f'<li>{item}</li>' for item in section['body'])}</ul>
        </div>
        """
        for section in payload["sections"]
    )
    sources_html = "".join(
        f"""
        <div class="source-card">
          <strong><a href="{item['url']}" target="_blank" rel="noreferrer">{item['label']}</a></strong>
          <div class="muted" style="margin-top:8px;">{item['why_it_matters']}</div>
        </div>
        """
        for item in payload["sources"]
    )
    loop_html = "".join(f"<li>{item}</li>" for item in payload["evaluation_loop"])
    summary_panels_html = "".join(
        f"""
        <div class="panel">
          <div class="status">{panel['status']}</div>
          <div class="mini-card">
            <strong>{panel['title']}</strong>
            <ul class="tight">{''.join(f"<li>{item}</li>" for item in panel['items'])}</ul>
          </div>
        </div>
        """
        for panel in payload["summary_panels"]
    )
    body = f"""
<section class="hero">
  <div class="eyebrow">调研记录</div>
  <h1>从 JD 到系统设计，我如何把业务问题落成 Agent 与评测闭环</h1>
  <div class="subcopy">{payload['summary']}</div>
</section>

<div class="section-grid">
  <div class="panel">
    <div class="status">设计思路</div>
    <div class="timeline">{sections_html}</div>
  </div>
  <div class="stack">
    {summary_panels_html}
    <div class="panel">
      <div class="status">评测闭环</div>
      <div class="mini-card">
        <strong>评测闭环不是额外加分项，而是核心能力证明</strong>
        <ol class="tight">{loop_html}</ol>
      </div>
    </div>
  </div>
</div>

<div class="panel" style="margin-top:18px;">
  <div class="status">优质信息源</div>
  <div class="timeline">{sources_html}</div>
</div>
"""
    return _render_page("调研记录", "research", body, "")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/review-presets", response_model=list[ReviewCase])
def review_presets() -> list[ReviewCase]:
    return load_sample_review_cases()


@app.get("/dashboard-summary", response_model=EvalReport)
def dashboard_summary() -> EvalReport:
    return run_evaluation(agent=agent)


@app.get("/workflow-graph")
def workflow_graph() -> dict:
    return workflow_graph_payload()


@app.get("/research-log-data")
def research_log_data() -> dict:
    return research_log_payload()


@app.get("/project-overview-data")
def project_overview_data() -> dict:
    return project_overview_payload()


@app.get("/agent-evolution-data")
def agent_evolution_data() -> dict:
    return agent_evolution_payload()


@app.get("/project-overview", response_class=HTMLResponse)
def project_overview_page() -> str:
    return render_project_overview_page()


@app.get("/agent-evolution", response_class=HTMLResponse)
def agent_evolution_page() -> str:
    return render_agent_evolution_page()


@app.get("/demo", response_class=HTMLResponse)
def demo() -> str:
    return render_demo_page()


@app.get("/workflow", response_class=HTMLResponse)
def workflow_page() -> str:
    return render_workflow_page()


@app.get("/research-log", response_class=HTMLResponse)
def research_log_page() -> str:
    return render_research_log_page()


@app.post("/review", response_model=ReviewResponse)
def review(payload: ReviewCase) -> ReviewResponse:
    return agent.run(
        case_id=payload.case_id,
        comment_text=payload.comment_text,
        thread_context=payload.thread_context,
        user_id=payload.user_id,
        reporter_count=payload.reporter_count,
        prior_violation_count=payload.prior_violation_count,
        prior_appeal_overturns=payload.prior_appeal_overturns,
        author_tenure_days=payload.author_tenure_days,
        policy_version=payload.policy_version,
    )
