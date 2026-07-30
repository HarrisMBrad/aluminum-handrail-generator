"""
test_handrail_cutlist.py
------------------------
QC test suite for handrail geometry and stock yield math.
"""

from handrail_cutlist import (
    calculate_miter_angle,
    calculate_post_height,
    calculate_slanted_top_rail_length,
    compute_stock_yield,
    generate_handrail_cutlist,
)
from handrail_fitup import HandrailAssemblySpec


def test_top_rail_hypotenuse_flat_and_pitched():
    # 0 pitch = straight 120" run
    assert calculate_slanted_top_rail_length(120.0, 0.0) == 120.0

    # 30 pitch over 120" run = 120 / cos(30 deg) ≈ 138.564"
    pitched_len = calculate_slanted_top_rail_length(120.0, 30.0)
    assert pitched_len == 138.564


def test_miter_angle_bisect():
    assert calculate_miter_angle(32.0) == 16.0
    assert calculate_miter_angle(0.0) == 0.0


def test_post_height_deduction():
    # 36" height - 1.5" tube profile = 34.5"
    assert calculate_post_height(36.0, 1.5) == 34.5


def test_stock_yield_calculation():
    # Cuts: 1x 138.564" + 4x 34.5" = 276.564" material
    # Needs two 240" stock bars
    cuts = [138.564, 34.5, 34.5, 34.5, 34.5]
    stock_yield = compute_stock_yield(cuts)

    assert stock_yield.bars_required_240in == 2
    assert stock_yield.kerf_loss_inches == 0.625  # 5 cuts * 0.125" kerf


def test_full_cutlist_payload_generation():
    spec = HandrailAssemblySpec(
        overall_run_inches=120.0,
        stair_pitch_degrees=32.0,
        target_post_spacing_inches=40.0,
        rail_height_inches=36.0,
        wall_clearance_inches=2.0,
        post_count=4,
    )
    payload = generate_handrail_cutlist(spec)

    assert "cut_items" in payload
    assert "stock_yield" in payload
    assert len(payload["cut_items"]) == 2
    assert payload["stock_yield"]["bars_20ft_required"] >= 1