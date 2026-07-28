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
- **Automated Image Annotation Pipeline:**
  - Includes `annotate_frame_corner.py` to generate high-resolution engineering overlays on physical shop photos using Matplotlib and Pillow.
  - Produces spec assets including `handrail_corner_spec.png` (45° top cap miter joint & fastener callouts) and `weld_inspection_spec.png` (AWS D1.2 joint metrics).

---

## 📐 Default Parameters

| Parameter | Default Value | Description |
| :--- | :--- | :--- |
| **Bays** | `3` | Number of upright posts (2 bays total) |
| **Bay Spacing** | `48.0"` | Center-to-center distance between posts |
| **Rail Height** | `42.0"` | Total assembly height from floor to top cap |
| **Toe Clearance** | `6.0"` | Bottom gap under vertical pickets |
| **Cap Overhang** | `3.0"` | Overhang past the outer faces of outer posts |
| **Fastener Spacing**| `12.0" O.C.` | Countersunk hole pattern spacing along top cap |

---

## ⚡ Quick Start / How to Run

1. Open **FreeCAD**.
2. Go to **Macro → Macros...** from the top menu.
3. Click **Create**, name the macro `HandrailBuilder.py`, and paste the script code inside.
4. Click the **Green Execute Button** (▶) or press `Ctrl + F6`.
5. The 3D model will render instantly in the viewport, and the cut list text file will auto-save to your FreeCAD application directory.

To run the automated photo annotation tool separately in terminal/PowerShell:
```bash
python annotate_frame_corner.py
