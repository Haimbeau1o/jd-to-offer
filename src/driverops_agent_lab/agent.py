from __future__ import annotations

from typing import Any

from driverops_agent_lab.memory import ConversationMemoryStore, DriverLongTermMemory
from driverops_agent_lab.schemas import (
    AgentResponse,
    ExecutionState,
    Observation,
    PlanStep,
    ToolTrace,
)
from driverops_agent_lab.tools import DriverOpsTools


class DriverOpsAgent:
    def __init__(self) -> None:
        self.tools = DriverOpsTools()
        self.memory_store = ConversationMemoryStore()

    def classify_intent(self, query: str) -> str:
        if any(keyword in query for keyword in ["收入", "流水", "赚钱"]):
            return "income_explanation"
        if any(keyword in query for keyword in ["活动", "奖励", "补贴"]):
            return "campaign_lookup"
        if any(keyword in query for keyword in ["热区", "去哪", "哪里单多"]):
            return "hotspot_recommendation"
        if any(keyword in query for keyword in ["规则", "政策", "申诉", "封禁", "取消"]):
            return "policy_qa"
        return "general_support"

    def build_plan(
        self,
        intent: str,
        query: str,
        recent_memory: list[str],
        long_term_memory: DriverLongTermMemory,
    ) -> list[PlanStep]:
        del query
        recent_hint = " 结合最近对话延续当前问题上下文。" if len(recent_memory) > 1 else ""
        memory_hint = self._build_memory_hint(long_term_memory)
        common_opening = PlanStep(
            step_id=1,
            goal="获取司机画像与偏好信息",
            tool_name="get_driver_profile",
            reason=f"任何经营建议都需要先确认司机分层、城市和常跑偏好。{recent_hint}{memory_hint}".strip(),
        )

        income_reason = "基于画像和统计结果生成策略建议。"
        if long_term_memory.preferred_peak_windows:
            windows = "、".join(long_term_memory.preferred_peak_windows[-2:])
            income_reason = f"基于画像和统计结果生成策略建议，并优先参考长期记忆中的高峰时段偏好：{windows}。"

        campaign_reason = "将活动结果转成更可执行的建议。"
        if long_term_memory.preferred_campaigns:
            campaign_reason = (
                f"将活动结果转成更可执行的建议，并结合长期记忆中的活动偏好：{long_term_memory.preferred_campaigns[-1]}。"
            )

        hotspot_reason = "把热区信息转成下一步行动建议。"
        if long_term_memory.recent_recommended_zones:
            hotspot_reason = (
                f"把热区信息转成下一步行动建议，并参考历史热区 {long_term_memory.recent_recommended_zones[-1]} 的长期记忆。"
            )

        plans: dict[str, list[PlanStep]] = {
            "income_explanation": [
                common_opening,
                PlanStep(
                    step_id=2,
                    goal="对比今日与昨日的关键经营指标",
                    tool_name="get_trip_stats",
                    reason="收入解释需要统计事实作为依据。",
                ),
                PlanStep(
                    step_id=3,
                    goal="生成收入解释与经营建议",
                    tool_name="recommend_strategy",
                    reason=income_reason,
                ),
            ],
            "campaign_lookup": [
                common_opening,
                PlanStep(
                    step_id=2,
                    goal="查找符合司机分层和标签的活动",
                    tool_name="get_campaigns",
                    reason="活动推荐需要结合城市、司机等级与偏好标签。",
                ),
                PlanStep(
                    step_id=3,
                    goal="生成活动参与建议",
                    tool_name="recommend_strategy",
                    reason=campaign_reason,
                ),
            ],
            "hotspot_recommendation": [
                common_opening,
                PlanStep(
                    step_id=2,
                    goal="读取当前热区与高收益时段",
                    tool_name="get_trip_stats",
                    reason="热区建议需要实时经营统计支撑。",
                ),
                PlanStep(
                    step_id=3,
                    goal="生成热区行动建议",
                    tool_name="recommend_strategy",
                    reason=hotspot_reason,
                ),
            ],
            "policy_qa": [
                common_opening,
                PlanStep(
                    step_id=2,
                    goal="查询规则知识库",
                    tool_name="search_policy_kb",
                    reason="规则问题必须给出规则依据。",
                ),
                PlanStep(
                    step_id=3,
                    goal="生成规则解释与后续动作",
                    tool_name="recommend_strategy",
                    reason="将规则结果转化为经营建议或申诉动作。",
                ),
            ],
            "general_support": [
                common_opening,
                PlanStep(
                    step_id=2,
                    goal="生成通用经营建议",
                    tool_name="recommend_strategy",
                    reason="在证据不足时先给保守的经营建议。",
                ),
            ],
        }
        return [step.model_copy(deep=True) for step in plans[intent]]

    def run(self, driver_id: str, city: str, query: str) -> AgentResponse:
        intent = self.classify_intent(query)
        self.memory_store.add_query(driver_id, query)
        recent_memory = self.memory_store.get_recent_queries(driver_id)
        long_term_memory = self.memory_store.get_long_term_memory(driver_id)
        plan = self.build_plan(intent, query, recent_memory, long_term_memory)
        state = ExecutionState(intent=intent, plan=plan)
        tool_trace: list[ToolTrace] = []
        context: dict[str, Any] = {
            "driver_id": driver_id,
            "city": city,
            "query": query,
            "intent": intent,
            "long_term_memory": long_term_memory,
        }

        for step in state.plan:
            step.status = "running"
            try:
                observation, trace = self._execute_step(step, context)
            except Exception as exc:
                step.status = "failed"
                state.stop_reason = "fallback_due_to_missing_data"
                state.observations.append(
                    Observation(
                        step_id=step.step_id,
                        tool_name=step.tool_name,
                        summary=f"step failed: {exc}",
                        evidence=[str(exc)],
                        success=False,
                    )
                )
                tool_trace.append(
                    ToolTrace(
                        tool_name=step.tool_name,
                        arguments={"driver_id": driver_id, "city": city},
                        result_summary=f"step failed: {exc}",
                    )
                )
                self._skip_pending_steps(state.plan)
                break

            step.status = "completed"
            state.observations.append(observation)
            tool_trace.append(trace)

        base_recommendations = context.get("recommendations") or self._build_fallback_recommendations(context)
        recommendations = self._apply_memory_context(intent, base_recommendations, long_term_memory)
        context["recommendations"] = recommendations
        stop_reason = state.stop_reason or self._derive_stop_reason(intent=intent, context=context)
        answer_summary = self._compose_answer_summary(
            intent=intent,
            driver_id=driver_id,
            stats=context.get("stats"),
            campaigns=context.get("campaigns"),
            policy_answers=context.get("policy_answers"),
            recommendations=recommendations,
            stop_reason=stop_reason,
        )
        evidence_items = self._collect_evidence_items(state.observations)
        risk_notes = self._build_risk_notes(
            intent=intent,
            context=context,
            observations=state.observations,
            stop_reason=stop_reason,
        )
        self._update_long_term_memory(driver_id, context)

        return AgentResponse(
            driver_id=driver_id,
            city=city,
            intent=intent,
            answer=answer_summary,
            answer_summary=answer_summary,
            evidence_items=evidence_items,
            recommendations=recommendations,
            risk_notes=risk_notes,
            tool_trace=tool_trace,
            memory_snapshot=self.memory_store.build_memory_snapshot(driver_id),
            plan=state.plan,
            observations=state.observations,
            stop_reason=stop_reason,
        )

    def _execute_step(self, step: PlanStep, context: dict[str, Any]) -> tuple[Observation, ToolTrace]:
        if step.tool_name == "get_driver_profile":
            profile = self.tools.get_driver_profile(context["driver_id"])
            context["profile"] = profile
            summary = f"driver tier={profile.tier}, city={profile.city}, tags={','.join(profile.tags)}"
            evidence = [f"preferred_hours={','.join(profile.preferred_hours)}", f"vehicle_type={profile.vehicle_type}"]
            arguments = {"driver_id": context["driver_id"]}
        elif step.tool_name == "get_trip_stats":
            stats = self.tools.get_trip_stats(context["driver_id"])
            context["stats"] = stats
            summary = f"today_income={stats.today_income}, acceptance_rate={stats.acceptance_rate}, peak_zone={stats.peak_zone}"
            evidence = [f"yesterday_income={stats.yesterday_income}", f"top_hours={','.join(stats.top_hours)}"]
            arguments = {"driver_id": context["driver_id"]}
        elif step.tool_name == "get_campaigns":
            campaigns = self.tools.get_campaigns(context["city"], context["profile"])
            context["campaigns"] = campaigns
            summary = f"matched_campaigns={len(campaigns)}"
            evidence = [item.title for item in campaigns[:2]] or ["no_campaign_matched"]
            arguments = {"city": context["city"], "driver_id": context["driver_id"]}
        elif step.tool_name == "search_policy_kb":
            policy_answers = self.tools.search_policy_kb(context["query"])
            context["policy_answers"] = policy_answers
            summary = f"matched_rules={len(policy_answers)}"
            evidence = policy_answers[:2]
            arguments = {"query": context["query"]}
        elif step.tool_name == "recommend_strategy":
            recommendations = self.tools.recommend_strategy(
                context["intent"],
                context["profile"],
                context.get("stats"),
                context.get("campaigns"),
            )
            context["recommendations"] = recommendations
            summary = f"recommendations={len(recommendations)}"
            evidence = recommendations[:2]
            arguments = {"intent": context["intent"], "driver_id": context["driver_id"]}
        else:
            raise ValueError(f"unsupported tool: {step.tool_name}")

        observation = Observation(
            step_id=step.step_id,
            tool_name=step.tool_name,
            summary=summary,
            evidence=evidence,
            success=True,
        )
        trace = ToolTrace(tool_name=step.tool_name, arguments=arguments, result_summary=summary)
        return observation, trace

    def _skip_pending_steps(self, plan: list[PlanStep]) -> None:
        for step in plan:
            if step.status == "pending":
                step.status = "skipped"

    def _build_fallback_recommendations(self, context: dict[str, Any]) -> list[str]:
        profile = context.get("profile")
        if profile is None:
            return []
        return self.tools.recommend_strategy(
            context["intent"],
            profile,
            context.get("stats"),
            context.get("campaigns"),
        )

    def _build_memory_hint(self, long_term_memory: DriverLongTermMemory) -> str:
        hints: list[str] = []
        if long_term_memory.preferred_peak_windows:
            hints.append("长期记忆中的高峰偏好")
        if long_term_memory.preferred_campaigns:
            hints.append("历史活动偏好")
        if long_term_memory.recent_recommended_zones:
            hints.append("最近推荐热区")
        if not hints:
            return ""
        return f" 同时读取{ '、'.join(hints) }。"

    def _apply_memory_context(
        self,
        intent: str,
        recommendations: list[str],
        long_term_memory: DriverLongTermMemory,
    ) -> list[str]:
        memory_aware_recommendations = list(recommendations)
        if intent == "income_explanation" and long_term_memory.preferred_peak_windows:
            self._append_unique_recommendation(
                memory_aware_recommendations,
                f"结合历史偏好，优先守住 {long_term_memory.preferred_peak_windows[-1]} 等高峰窗口，提升收入恢复速度。",
            )
        if intent == "campaign_lookup" and long_term_memory.preferred_campaigns:
            self._append_unique_recommendation(
                memory_aware_recommendations,
                f"结合历史偏好，你最近更关注 {long_term_memory.preferred_campaigns[-1]} 这类活动，可优先检查同类激励。",
            )
        if intent == "hotspot_recommendation" and long_term_memory.recent_recommended_zones:
            self._append_unique_recommendation(
                memory_aware_recommendations,
                f"最近推荐热区仍集中在 {long_term_memory.recent_recommended_zones[-1]}，说明与历史偏好一致，可优先连续覆盖。",
            )
        return memory_aware_recommendations

    def _append_unique_recommendation(self, recommendations: list[str], recommendation: str) -> None:
        if recommendation not in recommendations:
            recommendations.append(recommendation)

    def _update_long_term_memory(self, driver_id: str, context: dict[str, Any]) -> None:
        profile = context.get("profile")
        stats = context.get("stats")
        campaigns = context.get("campaigns") or []

        if profile is not None:
            self.memory_store.remember_peak_windows(driver_id, profile.preferred_hours)
        if stats is not None:
            self.memory_store.remember_peak_windows(driver_id, stats.top_hours)
            self.memory_store.remember_recommended_zone(driver_id, stats.peak_zone)
        if campaigns:
            self.memory_store.remember_campaigns(driver_id, [item.title for item in campaigns[:2]])

    def _collect_evidence_items(self, observations: list[Observation]) -> list[str]:
        evidence_items: list[str] = []
        for observation in observations:
            for item in [observation.summary, *observation.evidence]:
                if item and item not in evidence_items:
                    evidence_items.append(item)
        return evidence_items

    def _derive_stop_reason(self, intent: str, context: dict[str, Any]) -> str:
        if intent == "campaign_lookup" and not context.get("campaigns"):
            return "completed_with_partial_evidence"
        if intent == "policy_qa":
            policy_answers = context.get("policy_answers") or []
            if policy_answers and policy_answers[0].startswith("未找到"):
                return "completed_with_partial_evidence"
        return "completed_with_full_evidence"

    def _build_risk_notes(
        self,
        intent: str,
        context: dict[str, Any],
        observations: list[Observation],
        stop_reason: str,
    ) -> list[str]:
        risk_notes: list[str] = []
        stats = context.get("stats")
        campaigns = context.get("campaigns") or []
        policy_answers = context.get("policy_answers") or []

        if stop_reason == "fallback_due_to_missing_data":
            risk_notes.append("缺少关键经营数据，当前回答已切换为保守兜底建议，建议稍后重试或转人工复核。")
        if stop_reason == "completed_with_partial_evidence" and intent == "campaign_lookup" and not campaigns:
            risk_notes.append("当前未命中适合你的活动，活动建议仅基于司机画像生成，覆盖可能不完整。")
        if stop_reason == "completed_with_partial_evidence" and intent == "policy_qa" and policy_answers:
            risk_notes.append("当前仅检索到模糊规则结果，建议补充订单号、时段或判责信息后再查询。")
        if intent == "income_explanation" and stats is not None:
            if stats.acceptance_rate < 0.75:
                risk_notes.append(f"接单率 {stats.acceptance_rate:.0%} 偏低，可能继续影响活动资格和收入稳定性。")
            if stats.today_income < stats.yesterday_income:
                risk_notes.append(
                    f"今日收入较昨日下降 {abs(stats.today_income - stats.yesterday_income):.0f} 元，需要关注热区覆盖与高峰在线时长。"
                )
        if not risk_notes and any(not observation.success for observation in observations):
            risk_notes.append("执行过程中存在失败步骤，建议补齐数据后重新生成建议。")
        return risk_notes

    def _compose_answer_summary(
        self,
        intent: str,
        driver_id: str,
        stats,
        campaigns,
        policy_answers,
        recommendations: list[str],
        stop_reason: str,
    ) -> str:
        if stop_reason == "fallback_due_to_missing_data":
            fallback_tip = recommendations[0] if recommendations else "建议优先保持高峰时段稳定接单。"
            return f"当前缺少关键经营数据，先基于已有画像给出保守建议：{fallback_tip}"
        if intent == "income_explanation" and stats is not None:
            delta = stats.today_income - stats.yesterday_income
            trend = "下降" if delta < 0 else "上升"
            return (
                f"司机 {driver_id} 今日收入为 {stats.today_income:.0f} 元，相比昨日 {trend} {abs(delta):.0f} 元。"
                f" 主要关注接单率 {stats.acceptance_rate:.0%} 与热区 {stats.peak_zone} 的覆盖情况。"
            )
        if intent == "campaign_lookup":
            if campaigns:
                titles = "；".join(f"{item.title}（{item.reward}）" for item in campaigns[:2])
                return f"当前更适合你的活动有：{titles}。建议结合你的常跑时段优先参加。"
            return "当前没有命中你的分层活动，建议优先保证高峰时段接单稳定性。"
        if intent == "hotspot_recommendation" and stats is not None:
            return f"当前推荐热区是 {stats.peak_zone}，重点覆盖 {', '.join(stats.top_hours)}，优先跑高需求走廊。"
        if intent == "policy_qa" and policy_answers:
            return f"结合规则库，当前建议：{policy_answers[0]}"
        recommendation_tip = f" {recommendations[0]}" if recommendations else ""
        return f"这是一个通用经营建议问题，建议先聚焦高峰时段、热区覆盖和活动匹配。{recommendation_tip}".strip()
