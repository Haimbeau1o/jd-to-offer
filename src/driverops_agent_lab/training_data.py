from __future__ import annotations

from pathlib import Path
import json

from pydantic import BaseModel, Field


class TrainingSample(BaseModel):
    messages: list[dict[str, str]] = Field(default_factory=list)
    metadata: dict[str, str] = Field(default_factory=dict)


def build_training_samples() -> list[TrainingSample]:
    return [
        TrainingSample(
            messages=[
                {"role": "system", "content": "你是司机经营助手，优先用结构化工具和业务事实回答问题。"},
                {"role": "user", "content": "帮我解释下我今天收入为什么下降了"},
                {"role": "assistant", "content": "我先查看你的画像和今日行程统计，再给出收入解释和优化建议。"},
            ],
            metadata={"intent": "income_explanation", "skills": "react,tool_use,memory"},
        ),
        TrainingSample(
            messages=[
                {"role": "system", "content": "你是司机经营助手，优先做活动匹配和策略推荐。"},
                {"role": "user", "content": "今天有什么活动适合我"},
                {"role": "assistant", "content": "我会结合司机分层、城市和常跑时段来筛选活动。"},
            ],
            metadata={"intent": "campaign_lookup", "skills": "campaign_recommendation,tool_use"},
        ),
        TrainingSample(
            messages=[
                {"role": "system", "content": "你是司机经营助手，回答规则问题时要给出依据与后续动作。"},
                {"role": "user", "content": "完单率规则会影响活动资格吗"},
                {"role": "assistant", "content": "我先查询规则知识库，再解释影响范围和建议动作。"},
            ],
            metadata={"intent": "policy_qa", "skills": "policy_grounding,tool_use"},
        ),
    ]


def export_training_samples(outpath: Path, samples: list[TrainingSample] | None = None) -> Path:
    records = samples or build_training_samples()
    outpath.parent.mkdir(parents=True, exist_ok=True)
    with outpath.open("w", encoding="utf-8") as handle:
        for sample in records:
            handle.write(json.dumps(sample.model_dump(), ensure_ascii=False) + "\n")
    return outpath
