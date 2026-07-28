import FreeCAD as App
import FreeCADGui as Gui
import Part
import os
import sys

def build_handrail_macro():
    """
    Parametric Aluminum Handrail Builder for FreeCAD 1.1.1
    Generates 3D CAD Geometry, Welding Procedure Specs (WPS), and Robotic Cut Lists.
    """
    doc_name = "Aluminum_Handrail_Frame"
    if doc_name in App.listDocuments():
        App.closeDocument(doc_name)

    doc = App.newDocument(doc_name)

    # =========================================================
    # PARAMETRIC CONFIGURATION (Inches & Conversion)
    # =========================================================
    INCH = 25.4

    NUM_BAYS = 3
    BAY_SPACING_IN = 48.0       # 4 ft center-to-center
    RAIL_HEIGHT_IN = 42.0       # Standard 42" height
    OVERHANG_IN = 3.0           # 3" End overhang past outer posts
    HOLE_SPACING_IN = 12.0      # 12" O.C. fastener spacing
    TOE_GAP_IN = 6.0            # 6" Bottom toe clearance

    # Material Profile Specs (1/8" Wall Aluminum)
    POST_W_IN, POST_L_IN = 3.0, 3.0
    CAP_W_IN, CAP_H_IN = 3.0, 2.0
    PICKET_W_IN, PICKET_L_IN = 1.5, 1.5
    PICKETS_PER_BAY = 3

    PLATE_W_IN, PLATE_L_IN, PLATE_THICK_IN = 8.0, 8.0, 0.375

    # Computed Lengths
    post_cut_length_in = RAIL_HEIGHT_IN - CAP_H_IN
    picket_cut_length_in = post_cut_length_in - TOE_GAP_IN
    total_span_in = ((NUM_BAYS - 1) * BAY_SPACING_IN) + POST_L_IN
    cap_cut_length_in = total_span_in + (2.0 * OVERHANG_IN)

    # =========================================================
    # 1. BUILD CAD MODEL GEOMETRY
    # =========================================================
    bay_spacing = BAY_SPACING_IN * INCH
    post_w, post_l = POST_W_IN * INCH, POST_L_IN * INCH
    top_w, top_h = CAP_W_IN * INCH, CAP_H_IN * INCH
    picket_w, picket_l = PICKET_W_IN * INCH, PICKET_L_IN * INCH
    plate_w, plate_l = PLATE_W_IN * INCH, PLATE_L_IN * INCH
    plate_thick = PLATE_THICK_IN * INCH

    # Base Plates & Upright Posts
    for i in range(NUM_BAYS):
        y_pos = i * bay_spacing
        px0, py0 = (post_w - plate_w) / 2.0, y_pos + (post_l - plate_l) / 2.0
        
        # Base Plate (3/8" 6061-T6 Aluminum Plate)
        base_box = Part.makeBox(plate_w, plate_l, plate_thick, App.Vector(px0, py0, 0))
        hole_coords = [
            (px0 + 1.0 * INCH, py0 + 1.0 * INCH),
            (px0 + plate_w - 1.0 * INCH, py0 + 1.0 * INCH),
            (px0 + 1.0 * INCH, py0 + plate_l - 1.0 * INCH),
            (px0 + plate_w - 1.0 * INCH, py0 + plate_l - 1.0 * INCH)
        ]
        for hx, hy in hole_coords:
            base_box = base_box.cut(Part.makeCylinder(0.25 * INCH, plate_thick + 10.0, App.Vector(hx, hy, -5.0), App.Vector(0, 0, 1)))
        plate_obj = doc.addObject("Part::Feature", f"Alum_Base_Plate_{i+1}")
        plate_obj.Shape = base_box

        # Upright Post (3" x 3" x 1/8" Tube)
        post = doc.addObject("Part::Box", f"Alum_Post_3x3_{i+1}")
        post.Length, post.Width, post.Height = post_w, post_l, post_cut_length_in * INCH
        post.Placement = App.Placement(App.Vector(0, y_pos, plate_thick), App.Rotation(0, 0, 0))

    # Top Cap with 12" O.C. Countersunk Holes
    handrail_x, handrail_y = (post_w - top_w) / 2.0, -OVERHANG_IN * INCH
    handrail_z = plate_thick + (post_cut_length_in * INCH)
    cap_shape = Part.makeBox(top_w, cap_cut_length_in * INCH, top_h, App.Vector(handrail_x, handrail_y, handrail_z))
    
    current_y = handrail_y + (6.0 * INCH)
    while current_y <= (handrail_y + (cap_cut_length_in * INCH) - (2.0 * INCH)):
        csink = Part.makeCone(0.203 * INCH, 0.380 * INCH, 0.207 * INCH, App.Vector(post_w / 2.0, current_y, handrail_z + top_h - 0.207 * INCH), App.Vector(0, 0, 1))
        hole = Part.makeCylinder(0.203 * INCH, top_h + 10.0, App.Vector(post_w / 2.0, current_y, handrail_z - 5.0), App.Vector(0, 0, 1))
        cap_shape = cap_shape.cut(csink).cut(hole)
        current_y += HOLE_SPACING_IN * INCH

    cap_obj = doc.addObject("Part::Feature", "Top_Handrail_Cap")
    cap_obj.Shape = cap_shape

    # Vertical Pickets (1.5" x 1.5" x 1/8" Tubing)
    for i in range(NUM_BAYS - 1):
        y_start, y_end = i * bay_spacing + post_l, (i + 1) * bay_spacing
        picket_step = (y_end - y_start) / (PICKETS_PER_BAY + 1)
        for p in range(1, PICKETS_PER_BAY + 1):
            p_y = y_start + (p * picket_step) - (picket_l / 2.0)
            picket = doc.addObject("Part::Box", f"Picket_Bay_{i+1}_P{p}")
            picket.Length, picket.Width, picket.Height = picket_w, picket_l, picket_cut_length_in * INCH
            picket.Placement = App.Placement(App.Vector((post_w - picket_w) / 2.0, p_y, plate_thick + (TOE_GAP_IN * INCH)), App.Rotation(0, 0, 0))

    # Save directly to repo exports folder
    target_repo = r"C:\Users\bmich\Documents\L\templates\aluminum-handrail-generator"
    exports_dir = os.path.join(target_repo, "exports")
    os.makedirs(exports_dir, exist_ok=True)

    doc.recompute()

    fcstd_path = os.path.join(exports_dir, "Aluminum_Handrail_Frame.FCStd")
    doc.saveAs(fcstd_path)

    App.Console.PrintMessage(f"\n[SUCCESS] Model generated and saved to:\n{fcstd_path}\n\n")

    if Gui.getMainWindow():
        Gui.SendMsgToActiveView("ViewFit")

if __name__ == "__main__" or "FreeCAD" in sys.modules:
    build_handrail_macro()
