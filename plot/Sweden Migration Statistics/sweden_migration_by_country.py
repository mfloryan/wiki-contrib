import math

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from dateutil import parser
from matplotlib.patches import Patch

from colours import BangWongColors
from statistics_sweden import StatisticsSwedenAPI


def configure_plots():
    fm.fontManager.addfont(
        "/Users/mfloryan/Library/Fonts/LiberationSans-Regular.ttf"
    )

    fm.fontManager.addfont(
        "/Users/mfloryan/Library/Fonts/LiberationSans-Bold.ttf"
    )

    plt.rcParams.update(
        {
            "font.size": 14,
            "font.sans-serif": "Liberation Sans",
            "axes.labelsize": 16,
            "axes.titlesize": 20,
            "xtick.labelsize": 14,
            "ytick.labelsize": 14,
            "legend.fontsize": 14,
            "figure.titlesize": 20,
            "svg.fonttype": "none",
        }
    )


def plot_total_immgigration_bar_chart(data, footer_text):
    fig, ax = plt.subplots(figsize=(12, 8))

    # Define color mapping using Bang Wong's palette
    color_map = {
        "Sweden": BangWongColors.BLUE,
        "Norway": BangWongColors.LIGHT_BLUE,
        "Denmark": BangWongColors.LIGHT_BLUE,
        "Finland": BangWongColors.LIGHT_BLUE,
        "Germany": BangWongColors.GREEN,
        "Poland": BangWongColors.GREEN,
        "Somalia": BangWongColors.ORANGE,
        "China": BangWongColors.PINK,
        "India": BangWongColors.PINK,
        "Iran": BangWongColors.RED_ORANGE,
        "Afghanistan": BangWongColors.RED_ORANGE,
        "Iraq": BangWongColors.RED_ORANGE,
        "Syria": BangWongColors.RED_ORANGE,
    }

    ax.barh(
        data.index,
        data.values,
        color=[color_map[country] for country in data.index],
    )
    ax.set_axisbelow(True)
    ax.grid(axis="x", alpha=0.3)

    ax.set_title(
        "Share of Total Immigration to Sweden by Country of Birth (2000-2023)",
        pad=24,
        fontweight="bold",
    )
    fig.text(
        0.5,
        1,
        "Countries contributing ≥2% of total",
        ha="center",
        transform=ax.transAxes,
        va="bottom",
        fontsize=14,
    )

    ax.set_xlabel("Percentage of Total Immigration")

    # Add percentage labels
    for i, v in enumerate(data):
        ax.text(
            v - 0.1, i, f"{v:.1f}%", va="center", ha="right", color="white"
        )

    ax.set_xlim(right=math.ceil(data.max()))

    legend_elements = [
        Patch(facecolor=BangWongColors.BLUE, label="Sweden"),
        Patch(facecolor=BangWongColors.LIGHT_BLUE, label="Nordic Countries"),
        Patch(
            facecolor=BangWongColors.GREEN, label="Other European Countries"
        ),
        Patch(facecolor=BangWongColors.ORANGE, label="Africa"),
        Patch(
            facecolor=BangWongColors.RED_ORANGE,
            label="Middle East and Central Asia",
        ),
        Patch(facecolor=BangWongColors.PINK, label="East and South Asia"),
    ]
    ax.legend(handles=legend_elements, loc="lower right")

    fig.text(0, 0, footer_text, wrap=True, ha="left", va="bottom", fontsize=10)
    fig.tight_layout(rect=[0, 0.02, 1, 1])
    # fig.savefig(
    #     (
    #         "Share of Total Immigration "
    #         "to Sweden by Country of Birth (2000-2023)"
    #         ".svg"
    #     ),
    #     dpi=150,
    #     bbox_inches="tight",
    # )


def plot_total_emigration_bar_chart(data, footer_text):
    fig, ax = plt.subplots(figsize=(12, 8))

    color_map = {
        "Sweden": BangWongColors.BLUE,  # Domestic (highlight)
        "Finland": BangWongColors.LIGHT_BLUE,  # Nordic countries
        "Denmark": BangWongColors.LIGHT_BLUE,
        "Norway": BangWongColors.LIGHT_BLUE,
        "Iraq": BangWongColors.ORANGE,  # Middle East
        "Germany": BangWongColors.GREEN,  # Rest of Europe
        "Poland": BangWongColors.GREEN,
        "India": BangWongColors.PINK,  # Asia
        "China": BangWongColors.PINK,
        "USA": BangWongColors.RED_ORANGE,  # Americas
    }

    ax.barh(
        data.index,
        data.values,
        color=[color_map[country] for country in data.index],
    )
    ax.set_axisbelow(True)
    ax.grid(axis="x", alpha=0.3)

    ax.set_title(
        (
            "Share of Total Emigration "
            "from Sweden by Country of Birth (2000-2023)"
        ),
        pad=24,
        fontweight="bold",
    )
    fig.text(
        0.5,
        1,
        "Countries contributing ≥2% of total",
        ha="center",
        transform=ax.transAxes,
        va="bottom",
        fontsize=14,
    )

    ax.set_xlabel("Percentage of Total Emigration")

    for i, v in enumerate(data):
        if data.index[i] == "Sweden":
            ax.text(
                v - 0.1, i, f"{v:.1f}%", va="center", ha="right", color="white"
            )
        else:
            ax.text(
                v + 0.1, i, f"{v:.1f}%", va="center", ha="left", color="black"
            )

    ax.set_xlim(right=math.ceil(data.max()))

    legend_elements = [
        Patch(facecolor=BangWongColors.BLUE, label="Sweden"),
        Patch(facecolor=BangWongColors.LIGHT_BLUE, label="Nordic Countries"),
        Patch(
            facecolor=BangWongColors.GREEN, label="Other European Countries"
        ),
        Patch(facecolor=BangWongColors.ORANGE, label="Middle East"),
        Patch(facecolor=BangWongColors.PINK, label="Asia"),
        Patch(facecolor=BangWongColors.RED_ORANGE, label="Americas"),
    ]
    ax.legend(handles=legend_elements, loc="lower right")

    fig.text(0, 0, footer_text, wrap=True, ha="left", va="bottom", fontsize=10)
    fig.tight_layout(rect=[0, 0.02, 1, 1])
    fig.savefig(
        (
            "Share of Total Emigration "
            "from Sweden by Country of Birth (2000-2023)"
            ".svg"
        ),
        dpi=150,
        bbox_inches="tight",
    )


def plot_swedish_born_migration_flows(data, footer_text):
    fig, ax = plt.subplots(figsize=(15, 8))

    # Plot immigrations as positive bars
    ax.bar(
        data["year"],
        data["immigrations"],
        color=BangWongColors.BLUE,
        label="Immigration",
    )

    # Plot emigrations as negative bars
    ax.bar(
        data["year"],
        -data["emigrations"],  # Negative values for downward bars
        color=BangWongColors.RED_ORANGE,
        label="Emigration",
    )

    ax.set_title(
        "Migration of Swedish-Born Individuals (2000-2023)",
        pad=20,
        fontweight="bold",
    )

    ax.set_ylabel("Number of People")
    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, p: format(int(x), ","))
    )

    # Add legend with custom styling
    ax.legend(loc="upper right")

    # Add horizontal line at y=0
    ax.axhline(y=0, color=BangWongColors.BLACK, linestyle="-", linewidth=0.5)

    ax.grid(True, alpha=0.5, linestyle="--")

    fig.text(0, 0, footer_text, wrap=True, ha="left", va="bottom", fontsize=10)
    fig.tight_layout(rect=[0, 0.02, 1, 1])

    fig.savefig(
        (
            "Migration Flows "
            "of Swedish-Born Individuals (2000-2023)"
            ".svg"
        ),
        dpi=150,
        bbox_inches="tight",
    )


def plot_asylum_seekers_migration(df_summed, footer_text):

    main_countries = ["Syria", "Afghanistan", "Iraq"]

    horn_countries = ["Somalia", "Eritrea", "Ethiopia"]

    yugoslavia_countries = [
        "Yugoslavia",
        "Serbia",
        "Serbia and Montenegro",
        "Croatia",
        "Montenegro",
        "Bosnia and Herzegovina",
    ]

    # Define colors using BangWong class
    colors = {
        "Syria": BangWongColors.ORANGE,
        "Afghanistan": BangWongColors.LIGHT_BLUE,
        "Iraq": BangWongColors.GREEN,
        "Horn of Africa": BangWongColors.BLUE,
        "Former Yugoslavia": BangWongColors.RED_ORANGE,
    }

    all_countries = main_countries + horn_countries + yugoslavia_countries
    conflict_df = df_summed[df_summed["country_of_birth"].isin(all_countries)]

    fig, ax = plt.subplots(figsize=(12, 6))

    for country in main_countries:
        country_data = conflict_df[conflict_df["country_of_birth"] == country]
        ax.plot(
            country_data["year"],
            country_data["immigrations"],
            label=country,
            marker="o",
            color=colors[country],
            linewidth=2,
            markersize=5,
        )

    horn_data = (
        conflict_df[conflict_df["country_of_birth"].isin(horn_countries)]
        .groupby("year")["immigrations"]
        .sum()
        .reset_index()
    )
    ax.plot(
        horn_data["year"],
        horn_data["immigrations"],
        label="Horn of Africa",
        marker="o",
        color=colors["Horn of Africa"],
        linewidth=2,
        markersize=5,
    )

    yugoslavia_data = (
        conflict_df[conflict_df["country_of_birth"].isin(yugoslavia_countries)]
        .groupby("year")["immigrations"]
        .sum()
        .reset_index()
    )
    ax.plot(
        yugoslavia_data["year"],
        yugoslavia_data["immigrations"],
        label="Former Yugoslavia",
        marker="o",
        color=colors["Former Yugoslavia"],
        linewidth=2,
        markersize=5,
    )

    ax.set_title(
        (
            "Immigration to Sweden from Countries\n"
            "with Significant Asylum Applications (2000-2023)"
        ),
        pad=20,
        fontweight="bold",
    )
    ax.set_ylabel("Number of Immigrants", fontsize=10)

    ax.grid(True, linestyle="--", alpha=0.7)
    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, p: format(int(x), ","))
    )

    ax.legend(loc="upper left")

    fig.text(0, 0, footer_text, wrap=True, ha="left", va="bottom", fontsize=10)
    fig.tight_layout(rect=[0, 0.02, 1, 1])

    fig.savefig(
        (
            "Immigration to Sweden from Countries "
            "with Significant Asylum Applications (2000-2023)"
            ".svg"
        ),
        dpi=150,
        bbox_inches="tight",
    )


# MARK: Main

api_client = StatisticsSwedenAPI(
    "https://api.scb.se/OV0104/v1/doris/en/"
    "ssd/START/BE/BE0101/BE0101J/ImmiEmiFod"
)
(df, metadata) = api_client.get_dataframe()
df = df[df["country_of_birth"] != "total"].copy()

country_name_fixes = {
    "Syrian Arab Republic": "Syria",
    "Iran (Islamic Republic of)": "Iran",
    "Russian Federation": "Russia",
    "Türkiye": "Turkey",
    "Viet Nam": "Vietnam",
    "United States of America": "USA",
}

df["country_of_birth"] = df["country_of_birth"].map(
    lambda x: country_name_fixes.get(x, x)
)

df_summed = df.groupby(["year", "country_of_birth"], as_index=False).agg(
    {"immigrations": "sum", "emigrations": "sum"}
)

country_totals_in = (
    df_summed.groupby("country_of_birth")["immigrations"]
    .sum()
    .sort_values(ascending=False)
)

country_totals_out = (
    df_summed.groupby("country_of_birth")["emigrations"]
    .sum()
    .sort_values(ascending=False)
)

# Calculate percentage of total immigration for each country
total_immigration = country_totals_in.sum()
total_emmigration = country_totals_out.sum()
# Calculate percentage shares
country_percentages_in = (country_totals_in / total_immigration) * 100
country_percentages_out = (country_totals_out / total_emmigration) * 100

# Filter for countries with >= 2%
significant_countries_in = country_percentages_in[country_percentages_in >= 2]
significant_countries_in = significant_countries_in.sort_values(ascending=True)

significant_countries_out = country_percentages_out[
    country_percentages_out >= 2
]
significant_countries_out = significant_countries_out.sort_values(
    ascending=True
)

configure_plots()

footer_text = (
    f"Source: {metadata[0]['source']}"
    f" - {metadata[0]['label']}"
    f" ({metadata[0]['infofile']}) - "
    f"Updated: {parser.isoparse(metadata[0]['updated'])
                .strftime('%-d %b %Y')}"
)

plot_total_immgigration_bar_chart(significant_countries_in, footer_text)
plot_total_emigration_bar_chart(significant_countries_out, footer_text)

top_countries = country_totals_in.head(10).index
df_top = df_summed[df_summed["country_of_birth"].isin(top_countries)]

# MARK: Significant

pivot_df = df_top.pivot(
    index="year", columns="country_of_birth", values="immigrations"
)
chart_data = pivot_df.reset_index()

pivot_df.plot(kind="bar", stacked=True, figsize=(15, 8))

# Customize the plot
plt.title("Immigration by Country Over Time")
plt.xlabel("Year")
plt.ylabel("Number of Immigrants")
plt.legend(
    title="Country of Birth", bbox_to_anchor=(1.05, 1), loc="upper left"
)
plt.tight_layout()

# MARK: Asylum

plot_asylum_seekers_migration(df_summed, footer_text)

# MARK: Swedish

# Filter for Swedish-born people
sweden_data = df_summed[df_summed["country_of_birth"] == "Sweden"]

plot_swedish_born_migration_flows(sweden_data, footer_text)

# MARK: labour
# labor_countries = ["Poland", "India", "China", "Germany"]
# labor_df = df_summed[df_summed["country_of_birth"].isin(labor_countries)]

# plt.figure(figsize=(12, 6))
# for country in labor_countries:
#     country_data = labor_df[labor_df["country_of_birth"] == country]
#     plt.plot(
#         country_data["year"],
#         country_data["immigrations"],
#         label=country,
#         marker="o",
#     )

# plt.title("Labor Migration to Sweden (2000-2023)")
# plt.xlabel("Year")
# plt.ylabel("Number of Immigrants")
# plt.legend()
# plt.grid(True)

plt.show()
