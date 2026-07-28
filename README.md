# Aluminum Handrail CAD, Cut List & QA Generator 🛠️

A parametric FreeCAD Python macro designed for custom aluminum fabrication shops. This script automatically generates a full 3D CAD assembly of an aluminum handrail frame with custom pickets, base plates, and countersunk top cap holes. 

In addition to 3D model generation, it outputs an **AWS D1.2 / D1.2M Structural Aluminum Welding Procedure Specification (WPS)**, an **automated physical joint QA/inspection report**, and automated multi-format CAD deliverables (`.FCStd`, `.step`, and `.dxf`) saved directly to your repository workspace.

---

## 🌟 Key Features

- **Full Parametric CAD Generation:** Easily adjust overall length, post height, bay spacing, picket count, and material wall thickness directly in Python.
  - **Posts:** 3" x 3" x 1/8" wall square aluminum tubing.
  - **Top Cap:** 3" x 2" x 1/8" wall rectangular tubing with 12" O.C. countersunk fastener holes for flat-head machine screws.
  - **Pickets:** 1.5" x 1.5" x 1/8" wall square tubing with equal parametric spacing across all bays.
  - **Base Plates:** 3/8" 6061-T6 aluminum plate with 1/2" anchor clearance holes.
- **Automated CAD Deliverable Exports:**
  - Saves native FreeCAD master project (`.FCStd`).
  - Exports full 3D solid assembly (`.step`) for CAM simulation or client approval.
  - Exports 2D base plate flat pattern (`.dxf`) with automated module fallback handling (`importDXF` -> `Draft` -> `.step`).
- **AWS D1.2 Structural Welding & QA Audit:**
  - Outputs pulsed GMAW/MIG process parameters directly to stdout and the FreeCAD console.
  - Integrates physical sample inspection data tracking (weld bead length, tube outer dimensions, plate heights, and joint alignment angles).
- **Robotic & CNC Fabrication Cut Lists:**
  - Generates text-based shop cut lists (`Aluminum_Handrail_CutList_Robotic.txt`) for tube laser processing and material prep.

---

## 📂 Repository Output Structure

When executed, the script automatically builds and populates the `/exports/` directory inside your repository:

```text
aluminum-handrail-generator/
├── HandrailBuilder.py
└── exports/
    ├── Aluminum_Handrail_Frame.FCStd         # Native FreeCAD Project
    ├── Aluminum_Handrail_Frame.step          # 3D STEP Solid Assembly
    ├── Base_Plate_Flat_Pattern.dxf           # 2D Flat Pattern for Laser/Waterjet
    └── Aluminum_Handrail_CutList_Robotic.txt # Shop Cut List & BOM
