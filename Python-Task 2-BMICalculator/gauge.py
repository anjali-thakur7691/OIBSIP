"""A live BMI semicircle gauge used in the Streamlit result screen."""
import math

import matplotlib

# Streamlit renders figures in the browser; it does not need a desktop Tk window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge


def create_bmi_gauge(bmi: float, category: str):
    """Return a colourful BMI meter figure, inspired by a medical dashboard gauge."""
    ranges = [
        (10, 18.5, "UNDERWEIGHT", "#60A5FA"),
        (18.5, 25, "NORMAL", "#34D399"),
        (25, 30, "OVERWEIGHT", "#FBBF24"),
        (30, 40, "OBESE", "#F472B6"),
    ]
    minimum, maximum = 10, 40

    def angle(value):
        value = max(minimum, min(maximum, value))
        return 180 - ((value - minimum) / (maximum - minimum) * 180)

    fig, ax = plt.subplots(figsize=(9, 4.9), facecolor="#F8FAFC")
    ax.set_facecolor("#F8FAFC")
    for start, end, label, colour in ranges:
        ax.add_patch(Wedge((0, 0), 1.06, angle(end), angle(start), width=.32,
                           facecolor=colour, edgecolor="#F8FAFC", linewidth=4))
        mid = math.radians((angle(start) + angle(end)) / 2)
        ax.text(.78 * math.cos(mid), .78 * math.sin(mid), label,
                ha="center", va="center", fontsize=9, fontweight="bold", color="#172554")

    needle_angle = math.radians(angle(bmi))
    ax.plot([0, .73 * math.cos(needle_angle)], [0, .73 * math.sin(needle_angle)],
            color="#312E81", linewidth=7, solid_capstyle="round", zorder=5)
    ax.add_patch(Circle((0, 0), .105, color="#312E81", zorder=6))
    ax.add_patch(Circle((0, 0), .045, color="white", zorder=7))
    ax.text(0, -.22, f"BMI {bmi:.1f}", ha="center", va="center", fontsize=22,
            fontweight="bold", color="#312E81")
    ax.text(0, -.40, category.upper(), ha="center", va="center", fontsize=11,
            fontweight="bold", color="#64748B")
    ax.set_xlim(-1.23, 1.23); ax.set_ylim(-.52, 1.2); ax.set_aspect("equal"); ax.axis("off")
    fig.tight_layout(pad=.2)
    return fig
