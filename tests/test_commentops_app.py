from fastapi.testclient import TestClient

from commentops_agent_lab.app import app


client = TestClient(app)


def test_commentops_review_presets_expose_multiple_cases() -> None:
    response = client.get("/review-presets")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) >= 4
    case_ids = {item["case_id"] for item in payload}
    assert "comment-harm-001" in case_ids
    assert "comment-ambiguous-001" in case_ids
    assert "comment-shadow-001" in case_ids


def test_commentops_workflow_graph_endpoint_exposes_online_and_offline_chain() -> None:
    response = client.get("/workflow-graph")

    assert response.status_code == 200
    payload = response.json()
    assert payload["lanes"] == ["online_review", "offline_optimization"]
    node_ids = {item["id"] for item in payload["nodes"]}
    assert "case_intake" in node_ids
    assert "decision_policy" in node_ids
    assert "failure_review" in node_ids
    assert payload["references"]


def test_commentops_workflow_page_contains_interactive_chain() -> None:
    response = client.get("/workflow")

    assert response.status_code == 200
    assert "Interactive Review Workflow" in response.text
    assert "/workflow-graph" in response.text
    assert "offline_optimization" in response.text
    assert "workflowCanvasShell" in response.text
    assert "workflowSvg" in response.text
    assert "workflowMinimap" in response.text
    assert "zoomInView" in response.text
    assert "zoomOutView" in response.text
    assert "resetView" in response.text
    assert "拖动画布" in response.text


def test_commentops_research_log_page_contains_sources_and_eval_loop() -> None:
    response = client.get("/research-log")

    assert response.status_code == 200
    assert "调研记录" in response.text
    assert "TikTok" in response.text
    assert "评测闭环" in response.text
    assert "为什么这是 Agent" in response.text
    assert "业务理解与优化目标" in response.text
    assert "问题抽象" in response.text
    assert "LangGraph" in response.text
    assert "Graph API" in response.text
    assert "评测指标" in response.text


def test_commentops_project_overview_page_explains_full_story() -> None:
    response = client.get("/project-overview")

    assert response.status_code == 200
    assert "项目全景" in response.text
    assert "业务理解" in response.text
    assert "LangGraph 映射" in response.text
    assert "文档与产出" in response.text
    assert "2026-04-01-commentops-agent-architecture-and-eval-framework.md" in response.text


def test_commentops_agent_evolution_data_exposes_maturity_metrics_and_roi() -> None:
    response = client.get("/agent-evolution-data")

    assert response.status_code == 200
    payload = response.json()
    assert payload["title"] == "工程进化"
    assert payload["maturity_snapshot"]
    assert payload["metric_groups"]
    assert payload["roadmap_stages"]
    assert payload["roi_buckets"]
    assert payload["industry_mappings"]


def test_commentops_agent_evolution_page_contains_maturity_metrics_and_roi() -> None:
    response = client.get("/agent-evolution")

    assert response.status_code == 200
    assert "工程进化" in response.text
    assert "当前成熟度" in response.text
    assert "评测指标" in response.text
    assert "ROI" in response.text
    assert "TikTok" in response.text
    assert "Meta" in response.text
    assert "YouTube" in response.text
    assert "OpenAI" in response.text
    assert "Anthropic" in response.text
    assert "/agent-evolution" in response.text
