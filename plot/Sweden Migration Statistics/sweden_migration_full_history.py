from dateutil import parser
from matplotlib import font_manager as fm
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator

from colours import BangWongColors
from statistics_sweden import StatisticsSwedenAPI


def configure_plots():
    _configure_fonts()

    plt.rcParams.update(
        {
            # Text and font settings
            "font.size": 14,
            "font.sans-serif": "Liberation Sans",
            "axes.labelsize": 12,
            "axes.titlesize": 22,
            "axes.titleweight": "bold",
            "xtick.labelsize": 14,
            "ytick.labelsize": 14,
            "legend.fontsize": 14,
            "svg.fonttype": "none",
            # Grid settings
            "grid.alpha": 0.5,
            "grid.linestyle": "--",
            # Figure settings
            "figure.figsize": (12, 6),
            # Legend settings
            "legend.frameon": True,
            "legend.loc": "upper left",
        }
    )


def _configure_fonts():
    fm.fontManager.addfont(
        "/Users/mfloryan/Library/Fonts/LiberationSans-Regular.ttf"
    )
    fm.fontManager.addfont(
        "/Users/mfloryan/Library/Fonts/LiberationSans-Bold.ttf"
    )


def create_figure():
    fig, ax = plt.subplots()
    ax.grid(True)
    return fig, ax


def add_footer(fig, text):
    fig.text(0, 0, text, wrap=True, ha="left", va="bottom", fontsize=10)
    fig.tight_layout(rect=[0, 0.02, 1, 1])


def plot_sweden_migration(df, footer_text):
    migration_data = df[["year", "immigrations", "emigrations"]].dropna()

    # Create figure and axis
    fig, ax = create_figure()

    # Plot lines using the specified color palette
    ax.bar(
        migration_data["year"],
        -migration_data["emigrations"],
        color=BangWongColors.ORANGE,
        width=1,
        label="Emigration",
    )
    ax.bar(
        migration_data["year"],
        migration_data["immigrations"],
        color=BangWongColors.LIGHT_BLUE,
        width=1,
        label="Immigration",
    )

    ax.plot(
        migration_data["year"],
        migration_data["immigrations"] - migration_data["emigrations"],
        color=BangWongColors.BLACK,
        alpha=0.8,
        linewidth=1,
        label="Net Migration",
    )

    ax.axhline(y=0, color="black", linewidth=1, alpha=0.6)

    ax.set_ylabel("Number of People per Year", ha="left", y=0)
    ax.set_title(
        (
            f"Immigration and Emigration in Sweden "
            f"({migration_data["year"].min()} - "
            f"{migration_data["year"].max()})"
        ),
        pad=15,
    )

    # Add grid for better readability
    ax.yaxis.set_major_formatter(lambda x, p: f"{abs(int(x)):,}")
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_major_locator(MultipleLocator(20_000))
    ax.set_xlim(
        migration_data["year"].min() - 0.5,
        migration_data["year"].max() + 0.5
    )

    ax.legend(reverse=True)
    add_footer(fig, footer_text)

    return fig


api_client = StatisticsSwedenAPI(
    "https://api.scb.se/OV0104/v1/doris/en/"
    "ssd/START/BE/BE0101/BE0101G/BefUtvKon1749"
)

fields = {
    "Kon": ["1+2"],
    "ContentsCode": [
        "000000LV",
        "0000001H",
        "0000001F",
        "000000LX",
        "0000001G",
    ],
}

pd, metadata = api_client.get_dataframe(fields)

configure_plots()
footer = (
    f"Source: {metadata[0]['source']}"
    f" - {metadata[0]['label']}"
    f" ({metadata[0]['infofile']}) - "
    f"Updated: {parser.isoparse(metadata[0]['updated'])
                .strftime('%-d %b %Y')}"
)

fig = plot_sweden_migration(pd, footer)

fig.savefig(
    (
        "Annual Immigration and Emigration "
        f"in Sweden ({pd['year'].min()}-{pd['year'].max()})"
        ".svg"
    ),
    dpi=150,
    bbox_inches="tight",
)

plt.show()
plt.close()
