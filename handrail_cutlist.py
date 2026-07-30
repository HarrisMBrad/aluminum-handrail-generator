"""
handrail_cutlist.py
-------------------
Deterministic geometry & cut-list calculation core for aluminum handrails.
Assumes spec has already passed physical fit-up inspection.
"""

import math
from dataclasses import dataclass
from typing import Any, Dict, List

from handrail_fitup import HandrailAssemblySpec


@dataclass(frozen=True)
class CutItem:
    description: str
    length_inches: float
    miter_angle_deg: float
    qty: int


@dataclass(frozen=True)
class StockYield:
    bars_required_240in: int
    total_waste_inches: float
    kerf_loss_inches: float


# --- FABRICATION MATH FUNCTIONS ---


def calculate_miter_angle(pitch_degrees: float) -> float:
    """Calculates top-rail end miter angle from stair pitch (bisected angle)."""
    if pitch_degrees == 0.0:
        return 0.0
    # Complementary angle split for plumb/level joint
    return round(pitch_degrees / 2.0, 2)


def calculate_slanted_top_rail_length(
    run_inches: float, pitch_degrees: float
) -> float:
    """Calculates true diagonal hypotenuse length of top rail across stair run."""
    pitch_radians = math.radians(pitch_degrees)
    hypotenuse = run_inches / math.cos(pitch_radians)
    return round(hypotenuse, 3)


def calculate_post_height(
    rail_height_inches: float, tube_profile_height_inches: float = 1.5
) -> float:
    """Calculates net post cut height deducting top-rail tube profile thickness."""
    return round(rail_height_inches - tube_profile_height_inches, 3)


def compute_stock_yield(
    cut_lengths: List[float],
    stock_length_inches: float = 240.0,
    blade_kerf_inches: float = 0.125,
) -> StockYield:
    """Calculates required standard 20-foot (240") stock bars using First-Fit Decreasing.

    Accounts for saw blade kerf on every cut.
    """
    sorted_cuts = sorted(cut_lengths, reverse=True)
    bars: List[float] = []

    for cut in sorted_cuts:
        placed = False
        for i in range(len(bars)):
            # Check if cut + kerf fits in remaining space of existing bar
            if bars[i] + cut + blade_kerf_inches <= stock_length_inches:
                bars[i] += cut + blade_kerf_inches
                placed = True
                break
        if not placed:
            # Open a new stock bar
            bars.append(cut + blade_kerf_inches)

    total_cut_material = sum(cut_lengths)
    total_kerf = len(cut_lengths) * blade_kerf_inches
    total_stock_used = len(bars) * stock_length_inches
    total_waste = round(total_stock_used - (total_cut_material + total_kerf), 3)

    return StockYield(
        bars_required_240in=len(bars),
        total_waste_inches=total_waste,
        kerf_loss_inches=round(total_kerf, 3),
    )


# --- MAIN CUT LIST GENERATOR ---


def generate_handrail_cutlist(spec: HandrailAssemblySpec) -> Dict[str, Any]:
    """Generates complete cut list payload ready to pass to handrail_pipeline.py."""

    top_rail_len = calculate_slanted_top_rail_length(
        spec.overall_run_inches, spec.stair_pitch_degrees
    )
    post_height = calculate_post_height(spec.rail_height_inches)
    miter_angle = calculate_miter_angle(spec.stair_pitch_degrees)

    cuts = [
        CutItem(
            description="Top Rail",
            length_inches=top_rail_len,
            miter_angle_deg=miter_angle,
            qty=1,
        ),
        CutItem(
            description="Support Post",
            length_inches=post_height,
            miter_angle_deg=0.0,
            qty=spec.post_count,
        ),
    ]

    # Collect individual cut lengths for stock yield calculation
    all_lengths = [top_rail_len] + ([post_height] * spec.post_count)
    yield_summary = compute_stock_yield(all_lengths)

    return {
        "cut_items": [
            {
                "description": c.description,
                "length_in": c.length_inches,
                "miter_deg": c.miter_angle_deg,
                "qty": c.qty,
            }
            for c in cuts
        ],
        "stock_yield": {
            "bars_20ft_required": yield_summary.bars_required_240in,
            "waste_inches": yield_summary.total_waste_inches,
            "kerf_loss_inches": yield_summary.kerf_loss_inches,
        },
    }
