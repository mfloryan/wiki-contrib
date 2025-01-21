from matplotlib import pyplot as plt

from statistics_sweden import StatisticsSweden


def plot_migration_rates(df):
    df["immigration_rate"] = (df["immigrations"] / df["population"]) * 1000
    df["emigration_rate"] = (df["emigrations"] / df["population"]) * 1000
    df["net_migration_rate"] = df["immigration_rate"] - df["emigration_rate"]

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot rates
    ax.plot(
        df["year"],
        df["immigration_rate"],
        color="#0072B2",  # Bang Wong Blue
        linewidth=2,
        label="Immigration rate",
    )

    ax.plot(
        df["year"],
        df["emigration_rate"],
        color="#E69F00",  # Bang Wong Orange
        linewidth=2,
        label="Emigration rate",
    )

    # Plot net migration rate as filled area
    ax.fill_between(
        df["year"],
        df["net_migration_rate"],
        color="#009E73",  # Bang Wong Green
        alpha=0.3,
        label="Net migration rate",
    )

    # Add horizontal line at y=0 for reference
    ax.axhline(y=0, color="#000000", linestyle="--", alpha=0.3)

    # Customize plot
    ax.set_xlabel("Year")
    ax.set_ylabel("Rate per 1,000 inhabitants")
    ax.set_title(
        "Migration Rates Over Time\n"
        "Showing Dramatic Shift from Emigration to Immigration Country"
    )

    # Add legend
    ax.legend(loc="upper left")

    # Add annotations for key observations
    ax.annotate(
        "Peak net migration",
        xy=(2019, 6.59),
        xytext=(2019, 8),
        ha="center",
        arrowprops=dict(facecolor="black", shrink=0.05),
    )

    ax.annotate(
        "Historical emigration period",
        xy=(1879, -3.29),
        xytext=(1879, -5),
        ha="center",
        arrowprops=dict(facecolor="black", shrink=0.05),
    )

    # Adjust layout
    plt.tight_layout()

    return fig, ax


api_client = StatisticsSweden()

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

df, metadata = api_client.get_dataframe(
    StatisticsSweden.Endpoint.POPULATION_CHANGES,
    fields
)

migration_data = df[
    ["year", "population", "immigrations", "emigrations"]
].dropna()

plot_migration_rates(df)

plt.show()
