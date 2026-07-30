"""
handrail_fitup.py
-----------------
Physical boundary validation layer for aluminum handrail assemblies.
Clamps raw parameters at the door before cut-list or CAD geometry math executes.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import NamedTuple


class FitupResult(Enum):
    PASSED = auto()
    REJECTED = auto()


class InspectionReport(NamedTuple):
    status: FitupResult
    code: str
    message: str


@dataclass(frozen=True)
class HandrailAssemblySpec:
    """Immutable specification for a target handrail run."""

    overall_run_inches: float
    stair_pitch_degrees: float
    target_post_spacing_inches: float
    rail_height_inches: float
    wall_clearance_inches: float
    post_count: int = 3


# --- PHYSICAL INSPECTION GUARDS ---


def is_stair_pitch_within_code(pitch_deg: float) -> bool:
    """IBC limits standard stair incline angles (0° to 42°)."""
    return 0.0 <= pitch_deg <= 42.0


def is_post_spacing_clamped(run_length: float, post_count: int) -> bool:
    """Verifies actual span between posts does not exceed 72" (6ft) deflection limits."""
    if post_count < 2:
        return False
    actual_span = run_length / (post_count - 1)
    return actual_span <= 72.0


def is_rail_height_code_compliant(height_inches: float) -> bool:
    """IBC code requires handrail height to sit between 34" and 38" above the stair nosing."""
    return 34.0 <= height_inches <= 38.0


def is_wall_clearance_safe(clearance_inches: float) -> bool:
    """IBC code requires minimum 1.5" finger clearance from wall surface."""
    return clearance_inches >= 1.5


# --- MAIN FIT-UP INSPECTION ---


def verify_handrail_fitup(spec: HandrailAssemblySpec) -> InspectionReport:
    """Rejects invalid geometry before passing stock parameters to cut-list math."""

    if not is_stair_pitch_within_code(spec.stair_pitch_degrees):
        return InspectionReport(
            status=FitupResult.REJECTED,
            code="STAIR_PITCH_OUT_OF_BOUNDS",
            message=(
                f"Pitch of {spec.stair_pitch_degrees}° violates code limits "
                "(0° - 42°)."
            ),
        )

    if not is_post_spacing_clamped(spec.overall_run_inches, spec.post_count):
        actual_span = spec.overall_run_inches / max(1, spec.post_count - 1)
        return InspectionReport(
            status=FitupResult.REJECTED,
            code="POST_SPAN_EXCEEDED",
            message=(
                f"Span of {actual_span:.1f}\" exceeds maximum 72.0\" deflection "
                "limit. Increase post count."
            ),
        )

    if not is_rail_height_code_compliant(spec.rail_height_inches):
        return InspectionReport(
            status=FitupResult.REJECTED,
            code="RAIL_HEIGHT_NON_COMPLIANT",
            message=(
                f"Rail height of {spec.rail_height_inches}\" must be between "
                '34" and 38".'
            ),
        )

    if not is_wall_clearance_safe(spec.wall_clearance_inches):
        return InspectionReport(
            status=FitupResult.REJECTED,
            code="WALL_CLEARANCE_UNSAFE",
            message=(
                f"Wall clearance of {spec.wall_clearance_inches}\" is under "
                'the 1.5" minimum.'
            ),
        )

    return InspectionReport(
        status=FitupResult.PASSED,
        code="INSPECTION_OK",
        message="Fit-up passed cleanly. Assembly spec ready for cut list generation.",
    )
