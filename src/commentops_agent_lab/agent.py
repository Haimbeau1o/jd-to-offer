from __future__ import annotations

from commentops_agent_lab.data import load_policy_clauses, load_sample_review_cases
from commentops_agent_lab.schemas import (
    BusinessImpact,
    EvidenceSpan,
    PolicyClause,
    PolicyHit,
    QueueRouting,
    ReviewCase,
    ReviewDecision,
    ReviewResponse,
    RiskSignal,
    SimilarCase,
    ToolTrace,
)


class CommentOpsAgent:
    def __init__(
        self,
        policy_clauses: list[PolicyClause] | None = None,
        case_fixtures: list[ReviewCase] | None = None,
    ) -> None:
        self.policy_clauses = policy_clauses or load_policy_clauses()
        self.case_fixtures = case_fixtures or load_sample_review_cases()

    def run(
        self,
        case_id: str,
        comment_text: str,
        thread_context: list[str] | None = None,
        user_id: str = "user-001",
        reporter_count: int = 0,
        prior_violation_count: int = 0,
        prior_appeal_overturns: int = 0,
        author_tenure_days: int = 365,
        policy_version: str = "comment-policy-v1",
    ) -> ReviewResponse:
        review_case = ReviewCase(
            case_id=case_id,
            user_id=user_id,
            comment_text=comment_text,
            thread_context=thread_context or [],
            reporter_count=reporter_count,
            prior_violation_count=prior_violation_count,
            prior_appeal_overturns=prior_appeal_overturns,
            author_tenure_days=author_tenure_days,
            policy_version=policy_version,
        )
        tool_trace = [
            ToolTrace(
                tool_name="load_comment_context",
                arguments={"case_id": case_id},
                result_summary=f"context_items={len(review_case.thread_context)}",
            )
        ]

        matched_clauses = self._retrieve_policy_clauses(review_case.comment_text)
        matched_policies = self._build_policy_hits(review_case.comment_text, matched_clauses)
        tool_trace.append(
            ToolTrace(
                tool_name="retrieve_policy_clauses",
                arguments={"comment_text": review_case.comment_text},
                result_summary=f"matched_clauses={len(matched_policies)}",
            )
        )

        similar_cases = self._retrieve_similar_cases(review_case, matched_policies)
        tool_trace.append(
            ToolTrace(
                tool_name="search_similar_cases",
                arguments={"case_id": case_id, "target_categories": [item.category for item in matched_policies]},
                result_summary=f"similar_cases={len(similar_cases)}",
            )
        )

        risk_signals = self._synthesize_risk_signals(review_case, matched_clauses)
        tool_trace.append(
            ToolTrace(
                tool_name="synthesize_risk_signals",
                arguments={"reporter_count": reporter_count, "prior_violation_count": prior_violation_count},
                result_summary=f"risk_signals={len(risk_signals)}",
            )
        )

        decision = self._aggregate_decision(review_case=review_case, matched_clauses=matched_clauses, risk_signals=risk_signals)
        tool_trace.append(
            ToolTrace(
                tool_name="aggregate_decision",
                arguments={"matched_clause_ids": [item.clause_id for item in matched_clauses]},
                result_summary=f"action={decision.action}, category={decision.primary_category}",
            )
        )

        queue_routing = self._route_queue(review_case=review_case, decision=decision, risk_signals=risk_signals, matched_clauses=matched_clauses)
        tool_trace.append(
            ToolTrace(
                tool_name="route_review_queue",
                arguments={"action": decision.action, "category": decision.primary_category},
                result_summary=f"queue={queue_routing.queue_name}, priority={queue_routing.priority}",
            )
        )

        business_impact = self._build_business_impact(decision=decision, queue_routing=queue_routing, risk_signals=risk_signals)
        recommended_actions = self._build_recommended_actions(
            decision=decision,
            queue_routing=queue_routing,
            matched_policies=matched_policies,
            similar_cases=similar_cases,
        )
        review_notes = self._build_review_notes(decision=decision, queue_routing=queue_routing, risk_signals=risk_signals)

        return ReviewResponse(
            case_id=case_id,
            user_id=user_id,
            comment_text=review_case.comment_text,
            thread_context=review_case.thread_context,
            matched_policies=matched_policies,
            risk_signals=risk_signals,
            similar_cases=similar_cases,
            queue_routing=queue_routing,
            business_impact=business_impact,
            recommended_actions=recommended_actions,
            decision=decision,
            review_notes=review_notes,
            tool_trace=tool_trace,
            stop_reason=self._derive_stop_reason(decision.action, queue_routing.queue_name),
        )

    def _retrieve_policy_clauses(self, comment_text: str) -> list[PolicyClause]:
        lowered = comment_text.lower()
        matches = [
            clause
            for clause in self.policy_clauses
            if clause.decision != "pass" and any(keyword in lowered for keyword in clause.keywords)
        ]
        if matches:
            return matches
        benign_clause = next((clause for clause in self.policy_clauses if clause.decision == "pass"), None)
        return [benign_clause] if benign_clause is not None else []

    def _build_policy_hits(self, comment_text: str, clauses: list[PolicyClause]) -> list[PolicyHit]:
        policy_hits: list[PolicyHit] = []
        for clause in clauses:
            matched_keywords = [keyword for keyword in clause.keywords if keyword in comment_text]
            policy_hits.append(
                PolicyHit(
                    clause_id=clause.clause_id,
                    title=clause.title,
                    category=clause.category,
                    severity=clause.severity,
                    decision=clause.decision,
                    matched_keywords=matched_keywords,
                    reviewer_guidance=clause.reviewer_guidance,
                )
            )
        return policy_hits

    def _retrieve_similar_cases(self, review_case: ReviewCase, matched_policies: list[PolicyHit]) -> list[SimilarCase]:
        target_categories = {item.category for item in matched_policies if item.category != "benign_conversation"}
        if not target_categories:
            target_categories = {"benign_conversation"}

        similar_items: list[SimilarCase] = []
        for item in self.case_fixtures:
            if item.case_id == review_case.case_id:
                continue
            if item.expected_category not in target_categories:
                continue
            similar_items.append(
                SimilarCase(
                    case_id=item.case_id,
                    comment_text=item.comment_text,
                    final_action=item.expected_action or "unknown",
                    category=item.expected_category or "unknown",
                    queue_name=item.expected_queue or "unknown_queue",
                    summary=item.review_outcome_note or "历史相似 case，可用于辅助当前复核。",
                )
            )
        return similar_items[:2]

    def _synthesize_risk_signals(self, review_case: ReviewCase, matched_clauses: list[PolicyClause]) -> list[RiskSignal]:
        signals: list[RiskSignal] = []
        highest_clause = max(matched_clauses, key=self._severity_rank, default=None)
        if highest_clause is not None:
            signals.append(
                RiskSignal(
                    signal="policy_severity",
                    level=highest_clause.severity,
                    value=highest_clause.title,
                    note="模型命中的最高优先级规则强度。",
                )
            )

        if review_case.prior_violation_count >= 3:
            signals.append(
                RiskSignal(
                    signal="repeat_offender",
                    level="high",
                    value=str(review_case.prior_violation_count),
                    note="用户存在连续违规历史，建议保守处置并保留审计记录。",
                )
            )

        if review_case.prior_appeal_overturns >= 1:
            signals.append(
                RiskSignal(
                    signal="appeal_sensitive_user",
                    level="medium",
                    value=str(review_case.prior_appeal_overturns),
                    note="该用户存在申诉翻案历史，误杀风险更需要关注。",
                )
            )

        if review_case.reporter_count >= 8:
            signals.append(
                RiskSignal(
                    signal="crowd_reports",
                    level="high",
                    value=str(review_case.reporter_count),
                    note="举报密度较高，适合进入额外复查或优先队列。",
                )
            )
        elif review_case.reporter_count >= 3:
            signals.append(
                RiskSignal(
                    signal="crowd_reports",
                    level="medium",
                    value=str(review_case.reporter_count),
                    note="举报量中等，可作为排队优先级参考。",
                )
            )

        if review_case.author_tenure_days < 90:
            signals.append(
                RiskSignal(
                    signal="new_account",
                    level="medium",
                    value=str(review_case.author_tenure_days),
                    note="账号较新，风险画像尚不稳定。",
                )
            )

        if not review_case.thread_context and any(clause.decision == "escalate" for clause in matched_clauses):
            signals.append(
                RiskSignal(
                    signal="context_gap",
                    level="high",
                    value="0",
                    note="上下文不足，无法稳定完成自动审核。",
                )
            )
        return signals

    def _aggregate_decision(
        self,
        review_case: ReviewCase,
        matched_clauses: list[PolicyClause],
        risk_signals: list[RiskSignal],
    ) -> ReviewDecision:
        reject_candidates = [clause for clause in matched_clauses if clause.decision == "reject"]
        reject_clause = max(reject_candidates, key=self._severity_rank, default=None)
        if reject_clause is not None:
            confidence = 0.90 + 0.02 * self._severity_rank(reject_clause)
            confidence = min(confidence, 0.99)
            return ReviewDecision(
                action="reject",
                primary_category=reject_clause.category,
                confidence=confidence,
                policy_clause_ids=[reject_clause.clause_id],
                evidence_spans=[EvidenceSpan(text=self._extract_evidence(review_case.comment_text, reject_clause), label="matched_keyword")],
                rationale=f"评论命中 {reject_clause.title} 规则，且风险级别较高，适合进入自动拦截路径。",
            )

        escalate_clause = next((clause for clause in matched_clauses if clause.decision == "escalate"), None)
        if escalate_clause is not None:
            context_note = "已提供上下文，但语义仍依赖人工判断。" if review_case.thread_context else "当前上下文不足，需人工补充判断。"
            confidence = 0.62 if review_case.thread_context else 0.48
            return ReviewDecision(
                action="escalate",
                primary_category=escalate_clause.category,
                confidence=confidence,
                policy_clause_ids=[escalate_clause.clause_id],
                evidence_spans=[EvidenceSpan(text=self._extract_evidence(review_case.comment_text, escalate_clause), label="contextual_signal")],
                rationale=f"评论命中 {escalate_clause.title} 的上下文敏感表达。{context_note}",
                escalation_reason="context_sensitive_expression",
            )

        confidence = 0.86
        if any(item.signal == "appeal_sensitive_user" for item in risk_signals):
            confidence -= 0.05
        if any(item.signal == "crowd_reports" and item.level == "high" for item in risk_signals):
            confidence -= 0.06
        confidence = max(confidence, 0.68)
        benign_clause = matched_clauses[0] if matched_clauses else None
        clause_ids = [benign_clause.clause_id] if benign_clause is not None else []
        return ReviewDecision(
            action="pass",
            primary_category=benign_clause.category if benign_clause is not None else "benign_conversation",
            confidence=confidence,
            policy_clause_ids=clause_ids,
            evidence_spans=[EvidenceSpan(text=review_case.comment_text[:24], label="benign_text")],
            rationale="评论未命中高风险规则，可先自动放行，再依据用户风险和举报情况决定是否进入抽样复查。",
        )

    def _route_queue(
        self,
        review_case: ReviewCase,
        decision: ReviewDecision,
        risk_signals: list[RiskSignal],
        matched_clauses: list[PolicyClause],
    ) -> QueueRouting:
        if decision.action == "reject" and decision.primary_category == "violent_threat":
            return QueueRouting(
                queue_name="priority_threat_queue",
                priority="P1",
                rationale="涉及高危暴力威胁，适合最高优先级处置。",
                sla_minutes=15,
            )
        if decision.action == "reject":
            return QueueRouting(
                queue_name="abuse_enforcement_queue",
                priority="P2",
                rationale="明确违规评论进入常规处置队列，并保留申诉复核入口。",
                sla_minutes=60,
            )
        if decision.action == "escalate":
            return QueueRouting(
                queue_name="context_review_queue",
                priority="P2",
                rationale="语义依赖上下文和人工判断，应升级给评论复核队列。",
                sla_minutes=30,
            )
        if self._needs_shadow_audit(review_case, risk_signals, matched_clauses):
            return QueueRouting(
                queue_name="shadow_audit_queue",
                priority="P3",
                rationale="文本可放行，但举报密度、历史风险或申诉历史提示需要额外抽样复核。",
                sla_minutes=120,
            )
        return QueueRouting(
            queue_name="auto_pass_archive",
            priority="P4",
            rationale="低风险普通交流，可自动放行并归档。",
            sla_minutes=1440,
        )

    def _build_business_impact(
        self,
        decision: ReviewDecision,
        queue_routing: QueueRouting,
        risk_signals: list[RiskSignal],
    ) -> BusinessImpact:
        if queue_routing.queue_name == "priority_threat_queue":
            return BusinessImpact(
                automation_mode="auto_reject",
                reviewer_load="low",
                risk_level="critical",
                notes=[
                    "优先拦截高危内容，降低严重漏放风险。",
                    "需要保留证据和审计日志以支持后续申诉复核。",
                ],
            )
        if queue_routing.queue_name == "context_review_queue":
            return BusinessImpact(
                automation_mode="human_review",
                reviewer_load="high",
                risk_level="medium",
                notes=[
                    "通过自动路由减少 reviewer 搜索规则的时间。",
                    "把不确定案例稳定收敛到人工复核，降低误杀风险。",
                ],
            )
        if queue_routing.queue_name == "shadow_audit_queue":
            return BusinessImpact(
                automation_mode="guarded_auto_pass",
                reviewer_load="medium",
                risk_level="medium",
                notes=[
                    "兼顾自动化率和安全边界，避免对高风险用户一刀切放行。",
                    "适合运营团队观察举报密度和历史风险之间的关系。",
                ],
            )
        risk_level = "low" if not risk_signals else "medium"
        return BusinessImpact(
            automation_mode="auto_pass",
            reviewer_load="low",
            risk_level=risk_level,
            notes=[
                "直接自动放行，释放 reviewer 对低风险普通评论的处理压力。",
                "可配合抽样复查监控错放风险。",
            ],
        )

    def _build_recommended_actions(
        self,
        decision: ReviewDecision,
        queue_routing: QueueRouting,
        matched_policies: list[PolicyHit],
        similar_cases: list[SimilarCase],
    ) -> list[str]:
        if queue_routing.queue_name == "priority_threat_queue":
            return [
                "保留命中词和上下文证据，供申诉和审计使用。",
                "同步查看账号历史违规记录，评估是否需要升级处置。",
                "向运营侧输出高危威胁 case 标签，用于后续回灌训练。",
            ]
        if queue_routing.queue_name == "context_review_queue":
            actions = [
                "优先查看完整楼中楼上下文和双方历史互动。",
                "结合相似 case 和 reviewer guidance 做一致性裁决。",
                "若仍不确定，保守处理并记录复核原因。",
            ]
            if similar_cases:
                actions.append("参考相似 case 的历史处置结论，减少审核尺度漂移。")
            return actions
        if queue_routing.queue_name == "shadow_audit_queue":
            return [
                "先自动放行，但进入抽样复查队列。",
                "检查高举报量是否来自集中举报或误伤场景。",
                "观察该用户后续行为，决定是否提升风控权重。",
            ]
        guidance = matched_policies[0].reviewer_guidance if matched_policies else []
        return guidance or ["维持自动放行，并纳入常规质检抽样。"]

    def _build_review_notes(
        self,
        decision: ReviewDecision,
        queue_routing: QueueRouting,
        risk_signals: list[RiskSignal],
    ) -> list[str]:
        notes = [
            f"primary_category={decision.primary_category}",
            f"confidence={decision.confidence:.2f}",
            f"queue={queue_routing.queue_name}",
        ]
        if risk_signals:
            notes.append("risk_signals=" + ",".join(item.signal for item in risk_signals))
        if decision.action == "escalate":
            notes.append("该 case 适合由人工结合上下文进行二次确认。")
        if queue_routing.queue_name == "shadow_audit_queue":
            notes.append("自动通过不等于完全放过，仍建议进入抽样复查。")
        return notes

    def _extract_evidence(self, comment_text: str, clause: PolicyClause) -> str:
        for keyword in clause.keywords:
            if keyword in comment_text:
                return keyword
        return comment_text[:24]

    def _needs_shadow_audit(
        self,
        review_case: ReviewCase,
        risk_signals: list[RiskSignal],
        matched_clauses: list[PolicyClause],
    ) -> bool:
        if any(clause.decision in {"reject", "escalate"} for clause in matched_clauses):
            return False
        return (
            review_case.reporter_count >= 8
            or review_case.prior_violation_count >= 3
            or review_case.prior_appeal_overturns >= 2
            or any(item.signal == "appeal_sensitive_user" for item in risk_signals)
        )

    def _derive_stop_reason(self, action: str, queue_name: str) -> str:
        if queue_name == "shadow_audit_queue":
            return "completed_auto_pass_with_shadow_audit"
        if action == "reject":
            return "completed_auto_reject"
        if action == "escalate":
            return "escalated_for_human_review"
        return "completed_auto_pass"

    def _severity_rank(self, clause: PolicyClause) -> int:
        ranks = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4,
        }
        return ranks.get(clause.severity, 0)
