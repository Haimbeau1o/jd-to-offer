from commentops_agent_lab.agent import CommentOpsAgent
from commentops_agent_lab.eval import run_evaluation


def test_commentops_agent_rejects_explicit_harassment() -> None:
    agent = CommentOpsAgent()

    response = agent.run(
        case_id="comment-harm-001",
        comment_text="你这种垃圾去死吧",
        thread_context=["我不同意你的观点"],
        user_id="user-001",
    )

    assert response.decision.action == "reject"
    assert response.decision.primary_category in {"harassment_abuse", "violent_threat"}
    assert response.decision.policy_clause_ids
    assert response.tool_trace
    assert response.decision.rationale
    assert response.queue_routing.queue_name == "priority_threat_queue"
    assert response.business_impact.automation_mode == "auto_reject"
    assert any(item.signal == "policy_severity" for item in response.risk_signals)
    assert response.matched_policies


def test_commentops_agent_escalates_contextual_comment() -> None:
    agent = CommentOpsAgent()

    response = agent.run(
        case_id="comment-ambiguous-001",
        comment_text="你可真行啊",
        thread_context=["他把我的投稿删了"],
        user_id="user-002",
    )

    assert response.decision.action == "escalate"
    assert response.decision.primary_category == "contextual_abuse"
    assert response.decision.escalation_reason
    assert response.review_notes
    assert response.queue_routing.queue_name == "context_review_queue"
    assert response.similar_cases
    assert response.recommended_actions


def test_commentops_agent_prioritizes_higher_severity_clause() -> None:
    agent = CommentOpsAgent()

    response = agent.run(
        case_id="comment-harm-002",
        comment_text="你这种垃圾去死吧",
        thread_context=["我不同意你的观点"],
        user_id="user-003",
    )

    assert response.decision.primary_category == "violent_threat"


def test_commentops_agent_routes_high_risk_benign_case_to_shadow_audit() -> None:
    agent = CommentOpsAgent()

    response = agent.run(
        case_id="comment-shadow-001",
        comment_text="谢谢分享，学到了",
        thread_context=["原视频在讲 Python 调试技巧"],
        user_id="user-004",
        reporter_count=11,
        prior_violation_count=4,
        prior_appeal_overturns=2,
    )

    assert response.decision.action == "pass"
    assert response.queue_routing.queue_name == "shadow_audit_queue"
    assert any(item.signal == "repeat_offender" for item in response.risk_signals)
    assert any(item.signal == "appeal_sensitive_user" for item in response.risk_signals)


def test_commentops_evaluation_uses_case_risk_metadata_for_queue_routing() -> None:
    report = run_evaluation(agent=CommentOpsAgent())

    shadow_case = next(item for item in report.cases if item.case_id == "comment-shadow-001")

    assert shadow_case.predicted_queue == "shadow_audit_queue"
    assert shadow_case.queue_correct is True
