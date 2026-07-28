# Aluminum Handrail CAD, Cut List & QA Generator 🛠️

A parametric FreeCAD Python macro designed for custom aluminum fabrication shops. This script automatically generates a full 3D CAD assembly of an aluminum handrail frame with custom pickets, base plates, and countersunk top cap holes.

In addition to 3D model generation, it outputs an **AWS D1.2 / D1.2M Structural Aluminum Welding Procedure Specification (WPS)**, an **automated physical joint QA/inspection report**, multi-format CAD deliverables (`.FCStd`, `.step`, and `.dxf`), and Python-driven **automated image annotation graphics** for visual shop inspection documentation.

---

## 📸 Visual Quality Inspection & Spec Assets

The repo includes automated Python image processing tools (`annotate_frame_corner.py`) that overlay vector callouts and exact drafted specs onto physical shop photographs:

| AWS D1.2 Weld Joint Specimen | Top Cap Corner Miter & Fastener Layout |
| :---: | :---: |
| ![AWS D1.2 Weld Inspection Specimen](weld_inspection_spec.png) | ![Handrail Corner Miter Spec](handrail_corner_spec.png) |
| **`weld_inspection_spec.png`** | **`handrail_corner_spec.png`** |

---

## 🌟 Key Features

- **Full Parametric CAD Generation:** Easily adjust overall length, post height, bay spacing, picket count, and material wall thickness directly in Python.
  - **Posts:** 3" x 3" x 1/8" wall square aluminum tubing.
  - **Top Cap:** 3" x 2" x 1/8" wall rectangular tubing with 12" O.C. countersunk fastener holes for flat-head machine screws.
  - **Pickets:** 1.5" x 1.5" x 1/8" wall square tubing with equal parametric spacing across all bays.
  - **Base Plates:** 3/8" 6061-T6 aluminum plate with 1/2" anchor clearance holes.
- **Automated CAD Deliverable Exports (`/exports/`):**
  - Native FreeCAD Master Project (`.FCStd`).
  - Full 3D Solid Assembly (`.step`) for CAM simulation or client approval.
  - 2D Base Plate Flat Pattern (`.dxf`) for laser/waterjet cutting.
  - 3D Flat Pattern Solid (`.step`) fallback export.
- **AWS D1.2 Structural Welding & QA Audit:**
  - Outputs pulsed GMAW/MIG process parameters directly to stdout and the FreeCAD console.
  - Integrates physical sample inspection data tracking (weld bead length, tube outer dimensions, plate heights, and joint alignment angles).
- **Robotic & CNC Fabrication Cut Lists:**
  - Generates text-based shop cut lists (`Aluminum_Handrail_CutList_Robotic.txt`) for tube laser processing and material prep.

---

## 📂 Repository Output Structure

```text
aluminum-handrail-generator/
├── annotate_frame_corner.py          # Python Tool: Generates annotated top cap miter graphic
├── HandrailBuilder.py                # Main FreeCAD Parametric Macro Script
├── handrail_corner.png               # Raw Photo: Top cap corner miter joint
├── handrail_corner_spec.png          # Graphic: Annotated corner miter & fastener specs
├── README.md                         # Project Documentation
├── weld_inspection_spec.jpg          # Raw Photo: Weld joint physical specimen
├── weld_inspection_spec.png          # Graphic: Annotated weld specimen & AWS specs
└── exports/
    ├── Aluminum_Handrail_CutList_Robotic.txt # Shop Cut List & BOM for Laser/Prep
    ├── Aluminum_Handrail_Frame.FCStd         # Native FreeCAD Master Project File
    ├── Aluminum_Handrail_Frame.step          # 3D STEP Solid Assembly File
    ├── Base_Plate_Flat_Pattern.dxf           # 2D Flat Pattern for Laser/Waterjet
    └── Base_Plate_Flat_Pattern.step          # 3D STEP Flat Pattern Fallback Export