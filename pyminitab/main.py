"""
Generate minitab like plots
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from matplotlib.patches import Rectangle

# parameters
FIGSIZE = (10, 5)


def non_none(lst: list):
    return [x for x in lst if x is not None][0]


def hist(
    data: np.ndarray, LSL: float = None, USL: float = None, title: str = "", nbins=None
):
    "generate minitab style histgram with statistic info"

    # decide case
    case = None
    target = None
    if (LSL is None) and (USL is None):
        case = "no bound"
    elif (LSL is not None) and (USL is not None):
        case = "two bound"
    else:
        case = "one bound"

    if case == "two bound":
        target = (LSL + USL) / 2

    # Calculate statistics
    sample_mean = np.mean(data)
    sample_std = np.std(data, ddof=1)

    # Process capability indices
    Cp = None
    Cpk = None
    if case == "two bound":
        Cp = (USL - LSL) / (6 * sample_std)
        Cpl = (sample_mean - LSL) / (3 * sample_std)
        Cpu = (USL - sample_mean) / (3 * sample_std)
        Cpk = min(Cpl, Cpu)
    elif case == "one bound":
        if USL is not None:
            Cpu = (USL - sample_mean) / (3 * sample_std)
            Cpk = Cpu
        else:
            Cpl = (sample_mean - LSL) / (3 * sample_std)
            Cpk = Cpl

    # Create a figure with a GridSpec layout
    fig = plt.figure(figsize=FIGSIZE)
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 2, 1])

    # Set the figure background color
    fig.patch.set_facecolor("lightgrey")

    # Statistics on the left side
    ax_left = fig.add_subplot(gs[0, 0])
    ax_left.axis("off")
    if case == "no bound":
        stats_text_left = "\n".join(
            (
                f"Process Data",
                f"Sample Mean: {sample_mean:.4f}",
                f"Sample Std Dev: {sample_std:.4f}",
                f"Sample N: {len(data)}",
            )
        )
    else:
        stats_text_left = "\n".join(
            (
                f"Process Data",
                f"LSL: {LSL}",
                f"Target: {target}",
                f"USL: {USL}",
                f"Sample Mean: {sample_mean:.4f}",
                f"Sample Std Dev: {sample_std:.4f}",
                f"Sample N: {len(data)}",
            )
        )
    ax_left.text(
        0.05,
        0.95,
        stats_text_left,
        transform=ax_left.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=dict(facecolor="white", edgecolor="black"),
    )

    # Main plot
    ax_main = fig.add_subplot(gs[0, 1])
    # Update the bar color to match the provided image color
    bar_color = "#336699"
    count, bins, ignored = ax_main.hist(
        data, bins=nbins, density=True, alpha=0.6, color=bar_color, edgecolor="black"
    )

    # Add normal distribution curve
    # xmin, xmax = ax_main.set_xlim(LSL - 0.02, USL + 0.02)
    xmin, xmax = ax_main.get_xlim()
    if LSL is not None:
        xmin = LSL
    if USL is not None:
        xmax = USL
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, sample_mean, sample_std)

    ax_main.plot(
        x, p, color="#8B0000", linewidth=2, label="Overall"
    )  # Darker red for the curve

    # Add specification limits and labels

    if LSL is not None:
        ax_main.axvline(
            LSL, color="#8B0000", linestyle="--"
        )  # Darker red for the lines
        ax_main.text(
            LSL, ax_main.get_ylim()[1], "LSL", color="#8B0000", ha="center", va="bottom"
        )  # Darker red for the text
    if USL is not None:
        ax_main.axvline(
            USL, color="#8B0000", linestyle="--"
        )  # Darker red for the lines

        ax_main.text(
            USL, ax_main.get_ylim()[1], "USL", color="#8B0000", ha="center", va="bottom"
        )  # Darker red for the text

    # Labels and title
    # ax_main.set_xlabel("Diameter")
    ax_main.set_title(title, fontsize=16, pad=30)

    # Remove y-axis label and ticks
    ax_main.set_ylabel("")
    ax_main.yaxis.set_visible(False)

    # Turn off the legend
    ax_main.legend().set_visible(False)

    # Statistics on the right side
    ax_right = fig.add_subplot(gs[0, 2])
    ax_right.axis("off")

    if case == "one bound":
        stats_text_right = "\n".join(
            (
                f"Potential (Within) Capability",
                f"Cpk: {Cpk:.2f}",
            )
        )
    elif case == "no bound":
        stats_text_right = "\n".join(
            (
                f"Overall Capability",
                f"Cpm: *",
            )
        )
    elif case == "two bound":
        stats_text_right = "\n".join(
            (
                f"Overall Capability",
                f"Potential (Within) Capability",
                f"Cp: {Cp:.2f}",
                f"CPL: {Cpl:.2f}",
                f"CPU: {Cpu:.2f}",
                f"Cpk: {Cpk:.2f}",
            )
        )
    ax_right.text(
        0.05,
        0.95,
        stats_text_right,
        transform=ax_right.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=dict(facecolor="white", edgecolor="black"),
    )

    # Adjust layout
    plt.tight_layout()

    fig = plt.gcf()

    return fig


def main():
    # Generate some sample data
    np.random.seed(42)
    data = np.random.normal(loc=0.546, scale=0.019, size=100)

    # Specifications
    LSL = 0.5
    # USL = 0.6
    USL = None
    fig = hist(data, LSL, USL, nbins=20)
    fig.savefig("test.png")


if __name__ == "__main__":
    main()
