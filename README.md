# Aluminum Handrail CAD & Cut List Generator 🛠️

A parametric FreeCAD Python macro designed for custom metal fabrication shops. This script automatically generates a full 3D CAD assembly of an aluminum handrail with custom pickets, base plates, and countersunk top cap holes, while simultaneously generating a Welding Procedure Specification (WPS) and an automated CNC/robotic tube cut list.

---

## 🌟 Key Features

- **Full Parametric CAD Generation:** Easily adjust overall length, post height, bay spacing, picket count, and material wall thickness directly in Python.
  - **Posts:** 3" x 3" x 1/8" wall square aluminum tubing.
  - **Top Cap:** 3" x 2" x 1/8" wall rectangular tubing with 12" O.C. 82° countersunk fastener holes for 3/8" flat-head machine screws.
  - **Pickets:** 1.5" x 1.5" x 1/8" wall square tubing with parametric spacing across all bays.
  - **Base Plates:** 3/8" 6061-T6 plate with 1/2" anchor clearance holes.
- **Shop & Robotic Automation Outputs:**
  - Prints **Aluminum MIG (GMAW) Welding Specs** directly to the FreeCAD console.
  - Generates and exports a text-based **Robotic Tube Laser / Cut Cell sequence** (`Aluminum_Handrail_CutList_Robotic.txt`) to your system directory.

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
2. Go to **Macro $\rightarrow$ Macros...** from the top menu.
3. Click **Create**, name the macro `HandrailBuilder.py`, and paste the script code inside.
4. Click the **Green Execute Button** ($\triangleright$) or press `Ctrl + F6`.
5. The 3D model will render instantly in the viewport, and the cut list text file will auto-save to your FreeCAD application directory.

---

## Summary of Changes
- **Automated Image Annotation Pipeline:** Added `annotate_frame_corner.py` script to generate high-resolution engineering overlays on physical shop photographs using Matplotlib/Pillow.
- **Inspection Assets Added:** 
  - `handrail_corner_spec.png`: 45° top cap miter joint, dual 82° countersunk fastener layout, and post connection specs.
  - `weld_inspection_spec.png`: AWS D1.2 structural weld joint metrics, bead lengths, and scribe alignment data.
- **Documentation Updated (`README.md`):** Updated project structure, added side-by-side inspection graphic callouts, synced `/exports/` output listings, and added PowerShell execution instructions.

## Verification / Testing
- Verified `annotate_frame_corner.py` execution locally in PowerShell.
- Confirmed output graphic asset resolutions and accurate label positioning against source photos.
- Verified FreeCAD macro execution and export file paths.

## 📄 License

Distributed under the MIT License. Feel free to modify and adapt for your own shop workflows.
