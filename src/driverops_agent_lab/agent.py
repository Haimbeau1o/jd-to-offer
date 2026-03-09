from __future__ import annotations

from driverops_agent_lab.memory import ConversationMemoryStore
from driverops_agent_lab.schemas import AgentResponse, ToolTrace
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

    def run(self, driver_id: str, city: str, query: str) -> AgentResponse:
        intent = self.classify_intent(query)
        self.memory_store.add_query(driver_id, query)
        profile = self.tools.get_driver_profile(driver_id)

        tool_trace: list[ToolTrace] = [
            ToolTrace(
                tool_name="get_driver_profile",
                arguments={"driver_id": driver_id},
                result_summary=f"driver tier={profile.tier}, city={profile.city}, tags={','.join(profile.tags)}",
            )
        ]

        stats = None
        campaigns = None
        policy_answers = None

        if intent in {"income_explanation", "hotspot_recommendation"}:
            stats = self.tools.get_trip_stats(driver_id)
            tool_trace.append(
                ToolTrace(
                    tool_name="get_trip_stats",
                    arguments={"driver_id": driver_id},
                    result_summary=f"today_income={stats.today_income}, acceptance_rate={stats.acceptance_rate}, peak_zone={stats.peak_zone}",
                )
            )

        if intent == "campaign_lookup":
            campaigns = self.tools.get_campaigns(city, profile)
            tool_trace.append(
                ToolTrace(
                    tool_name="get_campaigns",
                    arguments={"city": city, "driver_id": driver_id},
                    result_summary=f"matched_campaigns={len(campaigns)}",
                )
            )

        if intent == "policy_qa":
            policy_answers = self.tools.search_policy_kb(query)
            tool_trace.append(
                ToolTrace(
                    tool_name="search_policy_kb",
                    arguments={"query": query},
                    result_summary=f"matched_rules={len(policy_answers)}",
                )
            )

        recommendations = self.tools.recommend_strategy(intent, profile, stats, campaigns)
        tool_trace.append(
            ToolTrace(
                tool_name="recommend_strategy",
                arguments={"intent": intent, "driver_id": driver_id},
                result_summary=f"recommendations={len(recommendations)}",
            )
        )

        answer = self._compose_answer(intent, profile.driver_id, stats, campaigns, policy_answers, recommendations)
        return AgentResponse(
            driver_id=driver_id,
            city=city,
            intent=intent,
            answer=answer,
            recommendations=recommendations,
            tool_trace=tool_trace,
            memory_snapshot=self.memory_store.get_recent_queries(driver_id),
        )

    def _compose_answer(self, intent: str, driver_id: str, stats, campaigns, policy_answers, recommendations: list[str]) -> str:
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
        return f"这是一个通用经营建议问题，建议先聚焦高峰时段、热区覆盖和活动匹配。{' '.join(recommendations[:1])}"
