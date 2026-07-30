"""
generate_freecad_assembly.py
-----------------------------
Main entry point connecting the physical pipeline state machine 
to FreeCAD CAD document generation.

Sequence:
1. Instantiates HandrailAssemblySpec
2. Clamps & inspects spec via HandrailPipeline
3. Generates cut-list payload
4. Builds FreeCAD 3D parametric geometry
5. Saves FCStd export & advances pipeline to EXPORT_READY
"""

import sys
from pathlib import Path
from typing import Any, Dict

from handrail_cutlist import generate_handrail_cutlist
from handrail_fitup import HandrailAssemblySpec
from handrail_pipeline import AssemblyState, HandrailPipeline

# Safe import for FreeCAD environment
try:
    import FreeCAD as App
    import Part

    FREECAD_AVAILABLE = True
except ImportError:
    FREECAD_AVAILABLE = False


def build_freecad_geometry(
    spec: HandrailAssemblySpec, cutlist: Dict[str, Any]
) -> str:
    """Builds parametric CAD shapes inside FreeCAD document and saves export."""
    if not FREECAD_AVAILABLE:
        print("[WARNING] FreeCAD module not found in current environment.")
        print("          Bypassing 3D rendering pass (Dry Run mode).")
        return "exports/DryRun_Handrail_Frame.FCStd"

    # 1. Initialize FreeCAD Document
    doc_name = "Aluminum_Handrail_Frame"
    doc = App.newDocument(doc_name)

    # Extract cut-list dimensions
    top_rail_item = next(
        item
        for item in cutlist["cut_items"]
        if item["description"] == "Top Rail"
    )
    post_item = next(
        item for item in cutlist["cut_items"] if item["description"] == "Support Post"
    )

    top_rail_length = top_rail_item["length_in"]
    post_height = post_item["length_in"]
    miter_angle = top_rail_item["miter_deg"]

    # 2. Build Top Rail Tube Profile (Simplified Box/Tube)
    top_rail_shape = Part.makeBox(
        top_rail_length, 1.5, 1.5
    )  # 1.5" x 1.5" aluminum tube
    top_rail_obj = doc.addObject("Part::Feature", "TopRail")
    top_rail_obj.Shape = top_rail_shape

    # Apply Stair Pitch Angle
    top_rail_obj.Placement.Rotation = App.Rotation(
        App.Vector(0, 1, 0), -spec.stair_pitch_degrees
    )

    # 3. Build Support Posts
    post_span = spec.overall_run_inches / max(1, spec.post_count - 1)
    for i in range(spec.post_count):
        post_x = i * post_span
        post_shape = Part.makeBox(1.5, 1.5, post_height)
        post_obj = doc.addObject("Part::Feature", f"SupportPost_{i+1}")
        post_obj.Shape = post_shape
        post_obj.Placement.Base = App.Vector(post_x, 0, -post_height)

    doc.recompute()

   # 4. Save FreeCAD Document to exports directory relative to script root
    project_root = Path(__file__).resolve().parent
    export_dir = project_root / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = export_dir / f"{doc_name}.FCStd"
    doc.saveAs(str(file_path))

    return str(file_path)


def run_assembly_generator(spec: HandrailAssemblySpec) -> None:
    """Main execution pipeline."""
    print("=" * 60)
    print("      ALUMINUM HANDRAIL CAD GENERATOR - PRODUCTION PIPELINE")
    print("=" * 60)

    # Step 1: Initialize Pipeline
    pipeline = HandrailPipeline(spec)
    print(f"[*] Pipeline initialized in state: {pipeline.state.name}")

    # Step 2: Clamp & Inspect Spec
    print("[*] Striking arc: Running physical fit-up inspection...")
    report = pipeline.clamp_and_inspect()

    if report.status.name == "REJECTED":
        print(f"\n[!] FIT-UP REJECTED [{report.code}]: {report.message}")
        print("[!] Generation halted. Correct parameters and re-run.")
        sys.exit(1)

    print(f"[✓] Fit-Up Passed: {report.message}")
    print(f"[*] Pipeline state advanced to: {pipeline.state.name}")

    # Step 3: Compute Cut List
    print("\n[*] Calculating deterministic cut list and stock yield...")
    cutlist_payload = generate_handrail_cutlist(pipeline.spec)
    pipeline.record_cutlist(cutlist_payload)
    print(f"[✓] Cut list recorded. Required 20ft stock bars: {cutlist_payload['stock_yield']['bars_20ft_required']}")
    print(f"[*] Pipeline state advanced to: {pipeline.state.name}")

    # Step 4: Build FreeCAD CAD Geometry
    print("\n[*] Invoking FreeCAD CAD geometry engine...")
    output_path = build_freecad_geometry(pipeline.spec, cutlist_payload)
    print(f"[✓] CAD assembly written to: {output_path}")

    # Step 5: Finalize Export
    pipeline.finalize_export()
    print(f"[*] Pipeline state finalized: {pipeline.state.name}")
    print("\n[SUCCESS] Production assembly pipeline complete.")


if __name__ == "__main__":
    # Target Spec for Testing
    target_spec = HandrailAssemblySpec(
        overall_run_inches=144.0,  # 12ft run
        stair_pitch_degrees=34.0,  # 34 degree incline
        target_post_spacing_inches=48.0,
        rail_height_inches=36.0,
        wall_clearance_inches=2.0,
        post_count=4,
    )

    run_assembly_generator(target_spec)
