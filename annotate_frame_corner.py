import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

# =========================================================
# 1. PATH CONFIGURATION & FILE RESOLUTION (CROSS-PLATFORM)
# =========================================================
# Dynamically locate repository root regardless of OS environment
repo_dir = os.path.dirname(os.path.abspath(__file__))
image_filenames = ["handrail_corner.png", "handrail_corner.jpg", "image_3.png", "1000006413.jpg"]

search_paths = []
for fname in image_filenames:
    search_paths.extend([
        os.path.join(repo_dir, fname),
        os.path.join(repo_dir, "exports", fname),
        os.path.abspath(fname)
    ])

input_image_path = None
for path in search_paths:
    if os.path.exists(path):
        input_image_path = path
        break

if not input_image_path:
    raise FileNotFoundError(
        f"Could not locate 'handrail_corner.png' in repository path: {repo_dir}\n"
        f"Please verify the image file exists in the workspace."
    )

output_image_path = os.path.join(repo_dir, "handrail_corner_spec.png")

# =========================================================
# 2. IMAGE LOADING & MATPLOTLIB CANVAS SETUP
# =========================================================
img = Image.open(input_image_path)
width, height = img.size

fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
ax.imshow(img)
ax.axis("off")  # Suppress pixel grid

# Style definitions
cyan = "#00FFFF"
magenta = "#FF00FF"
white = "#FFFFFF"

box_style = dict(boxstyle="round,pad=0.3", facecolor="#1E1E1E", edgecolor=cyan, alpha=0.85, lw=1.2)
mag_box_style = dict(boxstyle="round,pad=0.3", facecolor="#1E1E1E", edgecolor=magenta, alpha=0.85, lw=1.2)

def add_callout(text, xy_target, xy_text, color=cyan, style=box_style):
    """Helper function to render vector arrow callouts and bounding text boxes."""
    ax.annotate(
        text,
        xy=xy_target,
        xytext=xy_text,
        arrowprops=dict(arrowstyle="->", color=color, lw=1.5),
        color=white,
        fontsize=9,
        fontweight="bold",
        bbox=style,
        ha="center",
        va="center"
    )

# =========================================================
# 3. DRAFTING OVERLAY CALLOUTS
# =========================================================
# 45-Degree Miter Joint
add_callout("45.0° Top Cap Miter Joint", 
            xy_target=(width * 0.58, height * 0.35), 
            xy_text=(width * 0.80, height * 0.20), 
            color=magenta, style=mag_box_style)

# Countersunk Fasteners on Side Face
add_callout("Dual 82° Flat-Head Fasteners\n(Flush Side Mount)", 
            xy_target=(width * 0.48, height * 0.48), 
            xy_text=(width * 0.20, height * 0.48), 
            color=magenta, style=mag_box_style)

# Red Scribe Layout Lines
add_callout("Layout Crosshairs &\nScribe Alignment Lines", 
            xy_target=(width * 0.44, height * 0.38), 
            xy_text=(width * 0.20, height * 0.28), 
            color=cyan)

# Upright Corner Post Connection
add_callout("3\" x 3\" Upright Post\nCorner Socket Connection", 
            xy_target=(width * 0.55, height * 0.65), 
            xy_text=(width * 0.82, height * 0.65), 
            color=cyan)

# Top Cap Profile
add_callout("3\" x 2\" x 1/8\" Top Cap Profile", 
            xy_target=(width * 0.28, height * 0.32), 
            xy_text=(width * 0.18, height * 0.12), 
            color=cyan)

# =========================================================
# 4. EXPORT GRAPHIC ASSET
# =========================================================
plt.tight_layout(pad=0)
plt.savefig(output_image_path, bbox_inches="tight", pad_inches=0.0, dpi=300)
plt.close()

print(f"[SUCCESS] Source image resolved: {input_image_path}")
print(f"[SUCCESS] Graphic exported to:  {output_image_path}")