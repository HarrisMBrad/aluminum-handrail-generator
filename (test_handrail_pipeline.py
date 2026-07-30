"""
test_handrail_pipeline.py
--------------------------
QC test suite for pipeline state machine transitions and guards.
"""

import pytest
from handrail_fitup import HandrailAssemblySpec
from handrail_pipeline import AssemblyState, HandrailPipeline


@pytest.fixture
def valid_spec():
    return HandrailAssemblySpec(
        overall_run_inches=120.0,
        stair_pitch_degrees=32.0,
        target_post_spacing_inches=40.0,
        rail_height_inches=36.0,
        wall_clearance_inches=2.0,
        post_count=4,
    )


def test_successful_pipeline_flow(valid_spec):
    pipeline = HandrailPipeline(valid_spec)
    assert pipeline.state == AssemblyState.DRAFT

    # 1. Clamp & Inspect
    report = pipeline.clamp_and_inspect()
    assert report.status.name == "PASSED"
    assert pipeline.state == AssemblyState.FIXTURED

    # 2. Record Cut List
    pipeline.record_cutlist({"top_rail_len": 124.5, "posts": 4})
    assert pipeline.state == AssemblyState.CUTLIST_GENERATED

    # 3. Finalize Export
    pipeline.finalize_export()
    assert pipeline.state == AssemblyState.EXPORT_READY


def test_illegal_cutlist_generation_blocked(valid_spec):
    pipeline = HandrailPipeline(valid_spec)
    # Attempting to record cut list without inspecting first should throw RuntimeError
    with pytest.raises(RuntimeError, match="Pipeline violation"):
        pipeline.record_cutlist({"top_rail_len": 124.5})
        