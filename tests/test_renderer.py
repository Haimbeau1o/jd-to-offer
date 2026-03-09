from pathlib import Path

from jd_offer.renderer import render_case_bundle



def test_render_case_bundle(tmp_path: Path) -> None:
    outdir = tmp_path / "case"
    render_case_bundle(
        case_slug="didi-agent-2026",
        outdir=outdir,
        payload={
            "jd_decomposition": "x",
            "knowledge_system": "y",
            "resource_pack": "z",
            "project_blueprint": "a",
            "interview_assets": "b",
        },
    )
    assert (outdir / "01_jd_decomposition.md").exists()
    assert (outdir / "05_interview_assets.md").exists()
    assert (outdir / "manifest.yaml").exists()
