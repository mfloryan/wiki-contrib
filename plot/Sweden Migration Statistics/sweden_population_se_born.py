from dateutil import parser

from matplotlib import pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.ticker import PercentFormatter

from colours import BangWongColors
from statistics_sweden import StatisticsSweden


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


def format_date(date_str):
    date = parser.isoparse(date_str)
    formatted_date = date.strftime("%-d %b %Y")
    return formatted_date


def format_footer(metadata):
    return (
        f"Source: {metadata[0]['source']}"
        f" - {metadata[0]['label']}"
        f" ({metadata[0]['infofile']}) - "
        f"Updated: "
        f"{format_date(metadata[0]['updated'])}"
    )


def add_footer(fig, text):
    fig.text(0, 0, text, wrap=True, ha="left", va="bottom", fontsize=10)
    fig.tight_layout(rect=[0, 0.02, 1, 1])


def plot_se_born_rate(df, footer_text):
    fig, ax = create_figure()

    ax.plot(
        df["year"],
        df["percent"],
        color=BangWongColors.BLUE,
        linewidth=2,
        marker="o",
        markersize=8,
    )

    ax.set_title("Percentage of Swedish-Born Population in Sweden (2000-2023)")
    ax.yaxis.set_major_formatter(PercentFormatter(1))

    add_footer(fig, footer_text)

    return fig


api_client = StatisticsSweden()

df, metadata = api_client.get_dataframe(
    StatisticsSweden.Endpoint.POPULATION_REGION_BIRTH,
    {
        "Fodelseregion": ["TOTfod", "SE"],
        "Kon": ["1+2"],
        "Region": [
            "01",
            "03",
            "04",
            "05",
            "06",
            "07",
            "08",
            "09",
            "10",
            "12",
            "13",
            "14",
            "17",
            "18",
            "19",
            "20",
            "21",
            "22",
            "23",
            "24",
            "25",
        ],
    },
)

df_summed = (
    df.groupby(["year", "region_of_birth"])["number"].sum().reset_index()
)

df_wide = df_summed.pivot(
    index="year", columns="region_of_birth", values="number"
)

df_wide = df_wide.rename(
    columns={
        "All birth countries": "total_population",
        "Sweden": "swedish_born",
    }
).reset_index()

df_wide["percent"] = df_wide["swedish_born"] / df_wide["total_population"]

footer = format_footer(metadata)
configure_plots()
fig = plot_se_born_rate(df_wide, footer)

fig.savefig(
    "Percentage of Swedish-Born Population in Sweden (2000-2023).svg",
    dpi=150,
    bbox_inches="tight",
)

plt.show()
