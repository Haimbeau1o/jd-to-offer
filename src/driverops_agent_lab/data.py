from __future__ import annotations

from driverops_agent_lab.schemas import Campaign, DriverProfile, TripStats


DRIVER_PROFILES = {
    "driver-001": DriverProfile(
        driver_id="driver-001",
        city="beijing",
        tier="gold",
        vehicle_type="economy",
        preferred_hours=["07:00-10:00", "17:00-21:00"],
        tags=["morning_peak", "airport_pref"],
    ),
    "driver-002": DriverProfile(
        driver_id="driver-002",
        city="shanghai",
        tier="silver",
        vehicle_type="economy",
        preferred_hours=["11:00-14:00", "18:00-22:00"],
        tags=["downtown_pref"],
    ),
}

TRIP_STATS = {
    "driver-001": TripStats(
        driver_id="driver-001",
        today_income=420.0,
        yesterday_income=510.0,
        completion_rate=0.93,
        acceptance_rate=0.71,
        peak_zone="国贸-望京",
        top_hours=["07:30-09:30", "18:00-20:00"],
    ),
    "driver-002": TripStats(
        driver_id="driver-002",
        today_income=560.0,
        yesterday_income=530.0,
        completion_rate=0.95,
        acceptance_rate=0.84,
        peak_zone="陆家嘴-世纪大道",
        top_hours=["08:00-10:00", "19:00-21:00"],
    ),
}

CAMPAIGNS = [
    Campaign(
        campaign_id="bj-peak-001",
        city="beijing",
        title="晚高峰完单冲刺",
        segment="gold",
        reward="连续完成 8 单奖励 120 元",
        window="17:00-21:00",
    ),
    Campaign(
        campaign_id="bj-airport-002",
        city="beijing",
        title="机场接送单加速包",
        segment="airport_pref",
        reward="机场单每单额外奖励 12 元",
        window="06:00-11:00",
    ),
    Campaign(
        campaign_id="sh-midday-001",
        city="shanghai",
        title="午高峰激励",
        segment="silver",
        reward="午高峰完成 6 单奖励 80 元",
        window="11:00-14:00",
    ),
]

POLICY_KB = [
    {
        "keywords": ["规则", "取消", "完单率"],
        "answer": "完单率和取消率会影响部分活动资格，建议优先关注近 7 日完单率是否达标。",
    },
    {
        "keywords": ["申诉", "误判", "封禁"],
        "answer": "如遇异常判责，可在司机端申诉入口提交订单号、时段与证据截图。",
    },
]
