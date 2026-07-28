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

## 👨‍🏭 Welding Procedure Specification (WPS) Callouts

The macro prints shop-ready parameters for pulsed GMAW / MIG welding on 1/8" structural aluminum:

* **Base Material:** 6061-T6 / 6063-T5 Structural Aluminum
* **Filler Wire:** ER5356 (0.035" / 0.9 mm)
* **Shielding Gas:** 100% Argon @ 25–30 CFH
* **Machine Settings:** 19.5V – 21.5V | 340–390 IPM Wire Feed Speed
* **Joint Prep:** Stainless steel brush oxide removal + Acetone wipe prior to arc strike. Push technique ONLY (10°–15° angle).

---

## 📄 License

Distributed under the MIT License. Feel free to modify and adapt for your own shop workflows.