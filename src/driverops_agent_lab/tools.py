from __future__ import annotations

from driverops_agent_lab.data import CAMPAIGNS, DRIVER_PROFILES, POLICY_KB, TRIP_STATS
from driverops_agent_lab.schemas import Campaign, DriverProfile, TripStats


class DriverOpsTools:
    def get_driver_profile(self, driver_id: str) -> DriverProfile:
        return DRIVER_PROFILES[driver_id]

    def get_trip_stats(self, driver_id: str) -> TripStats:
        return TRIP_STATS[driver_id]

    def get_campaigns(self, city: str, profile: DriverProfile) -> list[Campaign]:
        matched = []
        for campaign in CAMPAIGNS:
            if campaign.city != city:
                continue
            if campaign.segment == profile.tier or campaign.segment in profile.tags:
                matched.append(campaign)
        return matched

    def search_policy_kb(self, query: str) -> list[str]:
        results = []
        for item in POLICY_KB:
            if any(keyword in query for keyword in item["keywords"]):
                results.append(item["answer"])
        return results or ["未找到精确规则，建议转人工或继续补充具体问题。"]

    def recommend_strategy(
        self,
        intent: str,
        profile: DriverProfile,
        stats: TripStats | None,
        campaigns: list[Campaign] | None,
    ) -> list[str]:
        recommendations: list[str] = []
        if intent == "income_explanation" and stats is not None:
            delta = stats.today_income - stats.yesterday_income
            if delta < 0:
                recommendations.append("今天收入低于昨天，优先补晚高峰和高热区时段，减少低质空驶。")
            if stats.acceptance_rate < 0.75:
                recommendations.append("接单率偏低，建议在高峰时段减少挑单，以提升活动资格和流水稳定性。")
            recommendations.append(f"重点关注 {stats.peak_zone} 和 {', '.join(stats.top_hours)} 这两个高收益窗口。")
        if intent == "campaign_lookup" and campaigns:
            recommendations.extend([f"活动推荐：{item.title}，{item.reward}，时间窗 {item.window}" for item in campaigns[:2]])
        if intent == "hotspot_recommendation" and stats is not None:
            recommendations.append(f"当前推荐热区：{stats.peak_zone}，建议优先覆盖 {', '.join(stats.top_hours)}。")
        if intent == "policy_qa":
            recommendations.append("规则问题优先给出依据，再提示申诉或人工入口，避免直接给结论。")
        if not recommendations:
            recommendations.append(f"结合 {profile.city} 城市和 {profile.tier} 司机等级，优先做高峰时段稳定接单。")
        return recommendations
