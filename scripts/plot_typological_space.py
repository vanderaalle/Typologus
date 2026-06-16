"""
Typological Space — publication-quality 3D scatter plot
Varèse: Poème électronique sound objects (Lombardo & Valle 2014)

Orientation matches Lombardo & Valle (Figura 10.11):
  X  — Profile/Sustain: tenuto (neg) … anamorph (0) … iterativo (pos), left→right
  Y  — Calibre: 0 (top/narrow) → 2 (bottom/wide), axis inverted
  Z  — Variation: 0 (front) → 3 (back), into depth

Usage:
  python plot_typological_space.py [data.json]
"""

import sys, json, pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d import Axes3D   # noqa

# ── Data ──────────────────────────────────────────────────────────────────────
BUILTIN_JSON = pathlib.Path(__file__).with_name("sound_objects.json")

def load_data(path=None):
    with open(path or BUILTIN_JSON) as f:
        return json.load(f)

# ── Visual encoding ───────────────────────────────────────────────────────────
PROFILE_COLOR = {
    "anamorph": "#2176AE",   # blue   — centre
    "eumorph":  "#E07B39",   # orange — mid bands
    "amorph":   "#C0392B",   # red    — extremes
    "mixed":    "#27AE60",   # green  — transitional
}
SUSTAIN_MARKER = {
    "sustained":  "o",
    "impulsive":  "^",
    "iterative":  "s",
}
MS = 38

# ── rcParams ──────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family":       "serif",
    "font.size":         8,
    "axes.labelsize":    9,
    "axes.titlesize":    9,
    "axes.linewidth":    0.7,
    "xtick.major.width": 0.7,
    "ytick.major.width": 0.7,
    "xtick.major.size":  3,
    "ytick.major.size":  3,
    "figure.dpi":        300,
    "savefig.dpi":       300,
    "text.usetex":       False,
})

# ── Tick definitions ──────────────────────────────────────────────────────────
X_TICKS  = [-2, -1, 0, 1, 2]
X_LABELS = ["Amorph\n(sus.)", "Eumorph\n(sus.)", "Anamorph\n(imp.)",
             "Eumorph\n(iter.)", "Amorph\n(iter.)"]
Y_TICKS  = [0, 0.5, 1.0, 1.5, 2.0]
Z_TICKS  = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

# ── Axis styling ──────────────────────────────────────────────────────────────
def style_3d(ax):
    ax.set_facecolor("white")
    for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
        pane.fill = False
        pane.set_edgecolor("#bbbbbb")
        pane.set_linewidth(0.4)
    ax.grid(True, linewidth=0.3, color="#dddddd", linestyle="--")
    ax.tick_params(labelsize=6, pad=1)

def set_3d_axes(ax):
    ax.set_xlim(-2.5,  2.5)
    ax.set_ylim( 0,    3.0)   # Y = variation, 0 at bottom, 3 at top
    ax.set_zlim( 0,    2.2)   # Z = calibre, 0 at front, 2 at back
    ax.set_xticks(X_TICKS);  ax.set_xticklabels(X_LABELS, fontsize=5)
    ax.set_yticks(Z_TICKS)
    ax.set_zticks(Y_TICKS)
    ax.invert_zaxis()          # calibre: 0 at top, 2 at bottom
    ax.set_xlabel("Profile / Sustain", labelpad=6,  fontsize=8)
    ax.set_ylabel("Variation",         labelpad=4,  fontsize=8)
    ax.set_zlabel("Calibre",           labelpad=4,  fontsize=8)

def style_2d(ax):
    ax.set_facecolor("white")
    ax.spines[["top","right"]].set_visible(False)
    ax.spines[["left","bottom"]].set_linewidth(0.7)
    ax.tick_params(labelsize=7)
    ax.grid(True, linewidth=0.3, color="#dddddd", linestyle="--", zorder=0)

# ── Legend ────────────────────────────────────────────────────────────────────
def make_legend_handles():
    ph = [mpatches.Patch(facecolor=c, edgecolor="none", label=k.capitalize())
          for k, c in PROFILE_COLOR.items()]
    sh = [Line2D([0],[0], marker=SUSTAIN_MARKER[s], color="none",
                 markerfacecolor="#444", markeredgecolor="#444",
                 markersize=5, label=s.capitalize())
          for s in SUSTAIN_MARKER]
    return ph, sh

# ── Scatter helpers ───────────────────────────────────────────────────────────
def scatter3d(ax, data, size=MS, alpha=0.85, labels=False):
    for sustain, marker in SUSTAIN_MARKER.items():
        grp = [o for o in data if o["sustain"] == sustain]
        if not grp: continue
        xs = [ o["x"] for o in grp]
        ys = [ o["z"] for o in grp]   # variation → vertical axis
        zs = [ o["y"] for o in grp]   # calibre → depth
        cs = [PROFILE_COLOR.get(o["profile"], "#888") for o in grp]
        ax.scatter(xs, ys, zs, c=cs, marker=marker, s=size,
                   edgecolors="white", linewidths=0.3,
                   alpha=alpha, depthshade=True, zorder=3)
        if labels:
            for o, x, y, z in zip(grp, xs, ys, zs):
                ax.text(x+0.04, y+0.04, z+0.04, str(o["id"]),
                        fontsize=4.5, color="#333", alpha=0.8)

def scatter2d(ax, data, xkey, ykey, size=MS*0.7, alpha=0.85, labels=False):
    for sustain, marker in SUSTAIN_MARKER.items():
        grp = [o for o in data if o["sustain"] == sustain]
        if not grp: continue
        xs = [o[xkey] for o in grp]
        ys = [o[ykey] for o in grp]
        cs = [PROFILE_COLOR.get(o["profile"], "#888") for o in grp]
        ax.scatter(xs, ys, c=cs, marker=marker, s=size,
                   edgecolors="white", linewidths=0.3, alpha=alpha, zorder=3)
        if labels:
            for o, x, y in zip(grp, xs, ys):
                ax.annotate(str(o["id"]), (x, y), fontsize=4.5,
                            color="#333", alpha=0.8,
                            xytext=(3,3), textcoords="offset points")

# ── Plot 1: standalone 3D ─────────────────────────────────────────────────────
def plot_3d(data, out_path, elev=20, azim=230, show_labels=True):
    """
    elev=25, azim=230 gives a front-left-above view matching Figura 10.11:
    - X axis (profile/sustain) runs left→right
    - Y axis (calibre) runs top→bottom (inverted)
    - Z axis (variation) recedes into depth
    """
    fig = plt.figure(figsize=(8, 6), facecolor="white")
    ax  = fig.add_subplot(111, projection="3d")
    style_3d(ax)
    scatter3d(ax, data, labels=show_labels)
    set_3d_axes(ax)
    ax.view_init(elev=elev, azim=azim)

    ph, sh = make_legend_handles()
    leg1 = ax.legend(handles=ph, title="Profile", loc="upper left",
                     fontsize=6, title_fontsize=7, framealpha=0.9,
                     edgecolor="#ccc", bbox_to_anchor=(0.0, 1.0))
    ax.add_artist(leg1)
    ax.legend(handles=sh, title="Sustain", loc="upper right",
              fontsize=6, title_fontsize=7, framealpha=0.9, edgecolor="#ccc")

    ax.set_title(
        "Varèse: Poème électronique — Sound Objects in Typological Space\n"
        f"(Lombardo & Valle 2014)   N = {len(data)}",
        fontsize=8, pad=10, color="#222"
    )
    fig.savefig(out_path, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print(f"  → {out_path}")

# ── Plot 2: overview 2×2 ─────────────────────────────────────────────────────
def plot_overview(data, out_path, elev=20, azim=230, show_labels=True):
    fig = plt.figure(figsize=(12, 9), facecolor="white")

    ax3d = fig.add_subplot(2, 2, 1, projection="3d")
    ax_xy = fig.add_subplot(2, 2, 2)   # profile × calibre
    ax_xz = fig.add_subplot(2, 2, 3)   # profile × variation
    ax_yz = fig.add_subplot(2, 2, 4)   # calibre × variation

    # 3D
    style_3d(ax3d)
    scatter3d(ax3d, data, size=25, labels=show_labels)
    set_3d_axes(ax3d)
    ax3d.view_init(elev=elev, azim=azim)
    ax3d.set_title("3D view", fontsize=8)

    # XY — profile × variation
    style_2d(ax_xy)
    scatter2d(ax_xy, data, "x", "z", labels=show_labels)
    ax_xy.set_xlabel("Profile / Sustain", fontsize=8)
    ax_xy.set_ylabel("Variation", fontsize=8)
    ax_xy.set_xticks(X_TICKS); ax_xy.set_xticklabels(X_LABELS, fontsize=5)
    ax_xy.set_title("Profile / Sustain  ×  Variation", fontsize=8)

    # XZ — profile × calibre (calibre 2→0, top to bottom)
    style_2d(ax_xz)
    scatter2d(ax_xz, data, "x", "y", labels=show_labels)
    ax_xz.invert_yaxis()
    ax_xz.set_xlabel("Profile / Sustain", fontsize=8)
    ax_xz.set_ylabel("Calibre (Mass)", fontsize=8)
    ax_xz.set_xticks(X_TICKS); ax_xz.set_xticklabels(X_LABELS, fontsize=5)
    ax_xz.set_title("Profile / Sustain  ×  Calibre", fontsize=8)

    # YZ — variation × calibre (calibre 2→0, top to bottom)
    style_2d(ax_yz)
    scatter2d(ax_yz, data, "z", "y", labels=show_labels)
    ax_yz.invert_yaxis()
    ax_yz.set_xlabel("Variation", fontsize=8)
    ax_yz.set_ylabel("Calibre (Mass)", fontsize=8)
    ax_yz.set_title("Variation  ×  Calibre", fontsize=8)

    ph, sh = make_legend_handles()
    fig.legend(handles=ph + sh, loc="lower center", ncol=7,
               fontsize=7, framealpha=0.9, edgecolor="#ccc",
               title="Profile (colour)  ·  Sustain (shape)",
               title_fontsize=7, bbox_to_anchor=(0.5, 0.0))

    fig.suptitle(
        "Varèse: Poème électronique — Sound Objects in Typological Space\n"
        f"(Lombardo & Valle 2014)   N = {len(data)}",
        fontsize=9, y=1.01, color="#222"
    )
    fig.tight_layout(rect=[0, 0.06, 1, 1])
    fig.savefig(out_path, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print(f"  → {out_path}")

# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else None
    data = load_data(src)
    print(f"Loaded {len(data)} sound objects.")
    out = pathlib.Path(".")
    print("Generating plots…")
    plot_3d(data,       out / "typological_space_3d.pdf",       show_labels=True)
    plot_overview(data, out / "typological_space_overview.pdf",  show_labels=True)
    print("Done.")
