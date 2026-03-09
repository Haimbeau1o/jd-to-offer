from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class JDDocument(BaseModel):
    title: str
    responsibilities: list[str] = Field(default_factory=list)
    requirements: list[str] = Field(default_factory=list)
    bonus_items: list[str] = Field(default_factory=list)
    raw_text: str


class CompetencyDefinition(BaseModel):
    name: str
    display_name: str
    trigger_keywords: list[str] = Field(default_factory=list)
    foundational_subtopics: list[str] = Field(default_factory=list)
    project_signals: list[str] = Field(default_factory=list)
    interview_signals: list[str] = Field(default_factory=list)
    resource_tags: list[str] = Field(default_factory=list)


class CompetencyScore(BaseModel):
    name: str
    display_name: str
    score: int
    matched_keywords: list[str] = Field(default_factory=list)
    foundational_subtopics: list[str] = Field(default_factory=list)
    project_signals: list[str] = Field(default_factory=list)
    interview_signals: list[str] = Field(default_factory=list)
    resource_tags: list[str] = Field(default_factory=list)


class CompetencyMap(BaseModel):
    items: list[CompetencyScore] = Field(default_factory=list)

    @property
    def top_names(self) -> list[str]:
        return [item.name for item in self.items]


class ResourceEntry(BaseModel):
    id: str
    title: str
    url: str
    source_type: str
    tags: list[str] = Field(default_factory=list)
    why: str
    verified_on: str


class ProjectTemplate(BaseModel):
    id: str
    name: str
    summary: str
    use_when: list[str] = Field(default_factory=list)
    tech_stack: list[str] = Field(default_factory=list)
    modules: list[str] = Field(default_factory=list)
    milestones: list[str] = Field(default_factory=list)
    metrics: list[str] = Field(default_factory=list)
    demo_scenarios: list[str] = Field(default_factory=list)


class CaseBundle(BaseModel):
    jd_decomposition: str
    knowledge_system: str
    resource_pack: str
    project_blueprint: str
    interview_assets: str


class Manifest(BaseModel):
    case_slug: str
    generated_at: str
    source_jd: str | None = None
    company: str | None = None
    role: str | None = None
    competencies: list[str] = Field(default_factory=list)
    files: dict[str, str] = Field(default_factory=dict)
    extra: dict[str, Any] = Field(default_factory=dict)
