"""
handrail_pipeline.py
--------------------
State machine controller for the handrail generation pipeline.
Enforces rigid sequential transitions:
DRAFT -> FIXTURED -> CUTLIST_GENERATED -> EXPORT_READY.

Prevents downstream CAD execution or file output on unvalidated assemblies.
"""

from enum import Enum, auto
from typing import Any, Dict, Optional

from handrail_fitup import (
    FitupResult,
    HandrailAssemblySpec,
    InspectionReport,
    verify_handrail_fitup,
)


class AssemblyState(Enum):
    DRAFT = auto()
    FIXTURED = auto()
    CUTLIST_GENERATED = auto()
    EXPORT_READY = auto()
    REJECTED = auto()


class HandrailPipeline:
    """Rigid assembly pipeline state machine.

    Prevents out-of-order execution or exporting unverified geometry.
    """

    def __init__(self, spec: HandrailAssemblySpec):
        self.spec = spec
        self.state = AssemblyState.DRAFT
        self.inspection_report: Optional[InspectionReport] = None
        self.cutlist_data: Optional[Dict[str, Any]] = None

    # --- GUARD CLAUSES ---

    def can_generate_cutlist(self) -> bool:
        """Guard: Returns True only if spec is properly fixtured and passed fit-up."""
        return (
            self.state == AssemblyState.FIXTURED
            and self.inspection_report is not None
            and self.inspection_report.status == FitupResult.PASSED
        )

    def can_export(self) -> bool:
        """Guard: Returns True only if cut-list math and geometry calculations completed."""
        return self.state == AssemblyState.CUTLIST_GENERATED

    # --- STATE TRANSITIONS ---

    def clamp_and_inspect(self) -> InspectionReport:
        """Clamps the spec in place and runs physical fit-up inspection."""
        if self.state not in (AssemblyState.DRAFT, AssemblyState.REJECTED):
            raise RuntimeError(
                f"State violation: Cannot re-inspect assembly from state {self.state.name}."
            )

        report = verify_handrail_fitup(self.spec)
        self.inspection_report = report

        if report.status == FitupResult.PASSED:
            self.state = AssemblyState.FIXTURED
        else:
            self.state = AssemblyState.REJECTED

        return report

    def record_cutlist(self, cutlist_payload: Dict[str, Any]) -> None:
        """Transitions state to CUTLIST_GENERATED once geometry engine completes."""
        if not self.can_generate_cutlist():
            raise RuntimeError(
                f"Pipeline violation: Cannot record cut list in state {self.state.name}. "
                "Assembly must be FIXTURED with a passed fit-up report."
            )
        self.cutlist_data = cutlist_payload
        self.state = AssemblyState.CUTLIST_GENERATED

    def finalize_export(self) -> None:
        """Transitions state to EXPORT_READY after CAD models/files are generated."""
        if not self.can_export():
            raise RuntimeError(
                f"Pipeline violation: Cannot finalize export in state {self.state.name}. "
                "Cut list calculation must complete first."
            )
        self.state = AssemblyState.EXPORT_READY
        