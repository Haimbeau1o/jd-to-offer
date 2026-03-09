from fastapi.testclient import TestClient

from driverops_agent_lab.agent import DriverOpsAgent
from driverops_agent_lab.app import app


client = TestClient(app)


def test_driverops_agent_handles_income_query() -> None:
    agent = DriverOpsAgent()
    response = agent.run(driver_id="driver-001", city="beijing", query="帮我解释下我今天收入为什么下降了")
    assert response.intent == "income_explanation"
    tool_names = [item.tool_name for item in response.tool_trace]
    assert "get_driver_profile" in tool_names
    assert "get_trip_stats" in tool_names
    assert response.recommendations
    assert "收入" in response.answer


def test_driverops_agent_handles_campaign_query() -> None:
    agent = DriverOpsAgent()
    response = agent.run(driver_id="driver-001", city="beijing", query="今天有什么活动适合我")
    assert response.intent == "campaign_lookup"
    tool_names = [item.tool_name for item in response.tool_trace]
    assert "get_campaigns" in tool_names
    assert any("活动" in item or "奖励" in item for item in response.recommendations)


def test_driverops_memory_tracks_recent_queries() -> None:
    agent = DriverOpsAgent()
    agent.run(driver_id="driver-001", city="beijing", query="今天活动有哪些")
    agent.run(driver_id="driver-001", city="beijing", query="帮我看看热区建议")
    snapshot = agent.memory_store.get_recent_queries("driver-001")
    assert len(snapshot) == 2
    assert snapshot[-1] == "帮我看看热区建议"


def test_driverops_fastapi_chat_endpoint() -> None:
    response = client.post(
        "/chat",
        json={
            "driver_id": "driver-001",
            "city": "beijing",
            "query": "今天哪些活动更适合我？",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["intent"] == "campaign_lookup"
    assert payload["tool_trace"]


def test_driverops_demo_page() -> None:
    response = client.get("/demo")
    assert response.status_code == 200
    assert "DriverOps Agent Lab Demo" in response.text
    assert "/chat" in response.text


def test_driverops_agent_emits_plan_and_observations() -> None:
    agent = DriverOpsAgent()
    response = agent.run(driver_id="driver-001", city="beijing", query="帮我解释下我今天收入为什么下降了")
    assert response.plan
    assert 2 <= len(response.plan) <= 4
    assert response.observations
    assert response.stop_reason in {
        "completed_with_full_evidence",
        "completed_with_partial_evidence",
        "fallback_due_to_missing_data",
    }


def test_driverops_plan_steps_execute_in_order() -> None:
    agent = DriverOpsAgent()
    response = agent.run(driver_id="driver-001", city="beijing", query="帮我看看热区建议")
    step_ids = [step.step_id for step in response.plan]
    assert step_ids == sorted(step_ids)
    assert all(step.status in {"completed", "skipped"} for step in response.plan)
    assert [item.step_id for item in response.observations]


def test_driverops_different_intents_get_different_plans() -> None:
    agent = DriverOpsAgent()
    income = agent.run(driver_id="driver-001", city="beijing", query="帮我解释下我今天收入为什么下降了")
    campaign = agent.run(driver_id="driver-001", city="beijing", query="今天有什么活动适合我")
    income_tools = [step.tool_name for step in income.plan]
    campaign_tools = [step.tool_name for step in campaign.plan]
    assert income_tools != campaign_tools
    assert "get_trip_stats" in income_tools
    assert "get_campaigns" in campaign_tools


def test_driverops_agent_returns_grounded_answer_for_income_query() -> None:
    agent = DriverOpsAgent()
    response = agent.run(driver_id="driver-001", city="beijing", query="帮我解释下我今天收入为什么下降了")

    assert response.answer_summary
    assert response.answer == response.answer_summary
    assert response.evidence_items
    assert any("today_income=420.0" in item for item in response.evidence_items)
    assert any("peak_zone=国贸-望京" in item for item in response.evidence_items)
    assert any("国贸-望京" in item for item in response.recommendations)
    assert response.risk_notes
    assert any("接单率" in item for item in response.risk_notes)
    assert response.stop_reason == "completed_with_full_evidence"




def test_driverops_agent_marks_partial_evidence_when_no_campaign_matches() -> None:
    agent = DriverOpsAgent()
    response = agent.run(driver_id="driver-002", city="beijing", query="今天有什么活动适合我")

    assert response.stop_reason == "completed_with_partial_evidence"
    assert response.answer_summary
    assert response.answer == response.answer_summary
    assert response.evidence_items
    assert any("no_campaign_matched" in item for item in response.evidence_items)
    assert response.risk_notes
    assert any("活动" in item for item in response.risk_notes)
    assert response.recommendations

def test_driverops_agent_falls_back_with_explicit_risks_when_tool_data_is_missing() -> None:
    agent = DriverOpsAgent()

    def broken_stats(_: str):
        raise RuntimeError("trip stats unavailable")

    agent.tools.get_trip_stats = broken_stats
    response = agent.run(driver_id="driver-001", city="beijing", query="帮我解释下我今天收入为什么下降了")

    assert response.stop_reason == "fallback_due_to_missing_data"
    assert response.answer_summary
    assert response.answer == response.answer_summary
    assert response.evidence_items
    assert any("trip stats unavailable" in item for item in response.evidence_items)
    assert response.risk_notes
    assert any("缺少" in item or "无法" in item for item in response.risk_notes)
