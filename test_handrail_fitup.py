"""
test_handrail_fitup.py
-----------------------
QC test suite for physical fit-up boundary inspection.
"""

from handrail_fitup import (
    FitupResult,
    HandrailAssemblySpec,
    verify_handrail_fitup,
)


def test_valid_handrail_spec_passes():
    spec = HandrailAssemblySpec(
        overall_run_inches=120.0,
        stair_pitch_degrees=32.0,
        target_post_spacing_inches=40.0,
        rail_height_inches=36.0,
        wall_clearance_inches=2.0,
        post_count=4,
    )
    report = verify_handrail_fitup(spec)
    assert report.status == FitupResult.PASSED
    assert report.code == "INSPECTION_OK"


def test_excessive_pitch_rejected():
    spec = HandrailAssemblySpec(
        overall_run_inches=120.0,
        stair_pitch_degrees=45.0,  # Exceeds 42° max
        target_post_spacing_inches=40.0,
        rail_height_inches=36.0,
        wall_clearance_inches=2.0,
        post_count=4,
    )
    report = verify_handrail_fitup(spec)
    assert report.status == FitupResult.REJECTED
    assert report.code == "STAIR_PITCH_OUT_OF_BOUNDS"


def test_post_span_deflection_rejected():
    spec = HandrailAssemblySpec(
        overall_run_inches=180.0,
        stair_pitch_degrees=32.0,
        target_post_spacing_inches=90.0,
        rail_height_inches=36.0,
        wall_clearance_inches=2.0,
        post_count=2,  # 180" span between 2 posts exceeds 72" limit
    )
    report = verify_handrail_fitup(spec)
    assert report.status == FitupResult.REJECTED
    assert report.code == "POST_SPAN_EXCEEDED"


def test_unsafe_wall_clearance_rejected():
    spec = HandrailAssemblySpec(
        overall_run_inches=120.0,
        stair_pitch_degrees=32.0,
        target_post_spacing_inches=40.0,
        rail_height_inches=36.0,
        wall_clearance_inches=1.0,  # Under 1.5" minimum
        post_count=4,
    )
    report = verify_handrail_fitup(spec)
    assert report.status == FitupResult.REJECTED
    assert report.code == "WALL_CLEARANCE_UNSAFE"
    