import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle, Polygon


def display_speedometer(
    high_target, low_target, mean_target, current_price, currency="$"
):
    values = np.array(
        [high_target, low_target, mean_target, current_price],
        dtype=float,
    )

    if not np.isfinite(values).all():
        raise ValueError("All prices must be finite numbers.")

    high_target, low_target, mean_target, current_price = values

    if high_target <= low_target:
        raise ValueError("high_target must be greater than low_target.")

    if not low_target <= mean_target <= high_target:
        raise ValueError("mean_target must fall between low and high.")

    background = "#F8FAFC"
    text_color = "#0F172A"
    muted = "#64748B"
    accent = "#2563EB"

    fig, ax = plt.subplots(figsize=(9, 5), facecolor=background)
    ax.set_aspect("equal")
    ax.set_xlim(-1.30, 1.30)
    ax.set_ylim(-0.58, 1.35)
    ax.axis("off")

    def format_price(value):
        return f"{currency}{value:,.2f}"

    segments = 180

    for i in range(segments):
        fraction = i / (segments - 1)

        ax.add_patch(Wedge(
            (0, 0),
            1,
            180 - (i + 1) * 180 / segments,
            180 - i * 180 / segments,
            width=0.14,
            facecolor=plt.cm.Blues(0.25 + 0.60 * fraction),
            edgecolor="none",
        ))

    for i, fraction in enumerate(np.linspace(0, 1, 9)):
        angle = np.pi * (1 - fraction)
        direction = np.array([np.cos(angle), np.sin(angle)])
        major = i % 2 == 0

        start = 1.025 * direction
        end = (1.075 if major else 1.055) * direction

        ax.plot(
            [start[0], end[0]],
            [start[1], end[1]],
            color=muted,
            lw=1.4 if major else 0.8,
        )

        if i in (2, 4, 6):
            position = 1.17 * direction
            value = low_target + fraction * (high_target - low_target)

            ax.text(
                *position,
                format_price(value),
                ha="center",
                va="center",
                fontsize=10,
                color=muted,
            )


    fraction = np.clip(
        (current_price - low_target) / (high_target - low_target),
        0,
        1,
    )
    angle = np.pi * (1 - fraction)

    direction = np.array([np.cos(angle), np.sin(angle)])
    perpendicular = np.array([-np.sin(angle), np.cos(angle)])

    ax.add_patch(Polygon(
        [
            0.80 * direction,
            -0.08 * direction + 0.035 * perpendicular,
            -0.08 * direction - 0.035 * perpendicular,
        ],
        closed=True,
        facecolor=text_color,
        zorder=5,
    ))

    ax.add_patch(Circle(
        (0, 0), 0.065, color=text_color, zorder=6
    ))
    ax.add_patch(Circle(
        (0, 0), 0.025, color=background, zorder=7
    ))

    for x, label, value in [
        (-0.94, "LOW TARGET", low_target),
        (0.94, "HIGH TARGET", high_target),
    ]:
        ax.text(
            x, -0.10, label,
            ha="center", fontsize=10, color=muted,
        )
        ax.text(
            x, -0.22, format_price(value),
            ha="center", fontsize=13,
            fontweight="bold", color=text_color,
        )

    ax.text(
        0, -0.20, format_price(current_price),
        ha="center", va="center", fontsize=29,
        fontweight="bold", color=accent,
    )
    ax.text(
        0, -0.34, "CURRENT PRICE",
        ha="center", fontsize=10, color=muted,
    )
    ax.text(
        0, -0.46, f"Mean target: {format_price(mean_target)}",
        ha="center", fontsize=11, color=muted,
    )

    if current_price < low_target:
        status = "Current price below target range"
    elif current_price > high_target:
        status = "Current price above target range"
    else:
        status = ""

    if status:
        ax.text(
            0, -0.57, status,
            ha="center", fontsize=9, color=muted,
        )

    ax.set_title(
        "Analyst Price Targets",
        fontsize=19,
        fontweight="bold",
        color=text_color,
        pad=18,
    )

    fig.tight_layout()
    plt.show()

    return fig, ax