import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from colours import BangWongColors
from statistics_sweden import StatisticsSwedenAPI


def generate_plot(df, metadata):

    fm.fontManager.addfont(
        "/Users/mfloryan/Library/Fonts/LiberationSans-Regular.ttf"
    )
    fm.fontManager.addfont(
        "/Users/mfloryan/Library/Fonts/LiberationSans-Bold.ttf"
    )
    plt.rcParams["font.sans-serif"] = ["Liberation Sans"]

    plt.rcParams.update(
        {
            "font.size": 14,
            "axes.labelsize": 16,
            "axes.titlesize": 20,
            "xtick.labelsize": 14,
            "ytick.labelsize": 14,
            "legend.fontsize": 14,
            "figure.titlesize": 20,
            "svg.fonttype": "none",
        }
    )

    plt.figure(figsize=(12, 6))
    ax = plt.gca()

    plt.bar(
        df["year"],
        yearly_totals["immigrations"],
        color=BangWongColors.BLUE,
        label="immigration",
    )
    plt.bar(
        df["year"],
        -yearly_totals["emigrations"],
        color=BangWongColors.RED_ORANGE,
        label="emigration",
    )

    plt.title("Swedish migration per year ", fontweight="bold")
    plt.grid(True, linestyle="--", alpha=0.7)

    plt.legend(facecolor="white", edgecolor="silver", borderpad=1)

    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, p: format(int(x), ","))
    )

    ax.tick_params(length=0)

    for spine in ax.spines.values():
        spine.set_color("silver")

    plt.axhline(y=0, color="black", linewidth=0.5, linestyle="-", zorder=10)

    end_year = df["year"].max()
    all_years = df["year"].unique()
    plt.xticks(
        all_years,
        [
            str(year) if (int(year) % 5 == 0 or year == end_year) else ""
            for year in all_years
        ],
    )

    plt.tight_layout()

    footer_text = (
        f"Source: {metadata[0]['source']}"
        f" - {metadata[0]['label']}"
        f" ({metadata[0]['infofile']})"
    )

    plt.figtext(
        0.08, 0.02, footer_text, wrap=True, ha="left", va="bottom", fontsize=10
    )

    plt.subplots_adjust(bottom=0.1)

    plt.savefig(
        (
            "Statistics Sweden (SCB) "
            "annual Immigration and Emigration 2000-2023"
            ".svg"
        ),
        dpi=150,
        bbox_inches="tight",
    )
    plt.close()


api_client = StatisticsSwedenAPI(
    "https://api.scb.se/"
    "OV0104/v1/doris/en/ssd/START/"
    "BE/BE0101/BE0101J/ImmiEmiFod"
)

fields = {
    "Kon": ["1", "2"],
    "Fodelseland": ["TOT"],
}

df, metadata = api_client.get_dataframe(fields)

yearly_totals = (
    df.groupby("year")
    .agg({"immigrations": "sum", "emigrations": "sum"})
    .reset_index()
)

generate_plot(yearly_totals, metadata)
