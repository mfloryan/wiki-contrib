import locale
from dateutil import parser
from matplotlib import font_manager as fm
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator

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


def add_footer(fig, text):
    fig.text(0, 0, text, wrap=True, ha="left", va="bottom", fontsize=10)
    fig.tight_layout(rect=[0, 0.02, 1, 1])


def plot_sweden_migration(df, footer_text, lang="en"):
    migration_data = df[["year", "immigrations", "emigrations"]].dropna()

    # Create figure and axis
    fig, ax = create_figure()

    # Plot lines using the specified color palette
    ax.bar(
        migration_data["year"],
        -migration_data["emigrations"],
        color=BangWongColors.ORANGE,
        width=1,
        label=TRANSLATIONS[lang]["emigration"],
    )
    ax.bar(
        migration_data["year"],
        migration_data["immigrations"],
        color=BangWongColors.LIGHT_BLUE,
        width=1,
        label=TRANSLATIONS[lang]["immigration"],
    )

    ax.plot(
        migration_data["year"],
        migration_data["immigrations"] - migration_data["emigrations"],
        color=BangWongColors.BLACK,
        alpha=0.8,
        linewidth=1,
        label=TRANSLATIONS[lang]["net_migration"],
    )

    ax.axhline(y=0, color="black", linewidth=1, alpha=0.6)

    ax.set_ylabel(TRANSLATIONS[lang]["y_label"], ha="left", y=0)
    ax.set_title(
        (
            TRANSLATIONS[lang]["title"] + " "
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
        migration_data["year"].min() - 0.5, migration_data["year"].max() + 0.5
    )

    ax.legend(reverse=True)
    add_footer(fig, footer_text)

    return fig


def format_date(date_str, lang="en"):
    try:
        current_locale = locale.getlocale()
        locale.setlocale(locale.LC_TIME, LOCALE_MAPPING[lang])

        date = parser.isoparse(date_str)
        formatted_date = date.strftime("%-d %b %Y")

        locale.setlocale(locale.LC_TIME, current_locale)

        return formatted_date
    except locale.Error:
        return parser.isoparse(date_str).strftime("%-d %b %Y")


def format_footer(metadata, lang="en"):
    return (
        f"{TRANSLATIONS[lang]['source']}: {metadata[0]['source']}"
        f" - {metadata[0]['label']}"
        f" ({metadata[0]['infofile']}) - "
        f"{TRANSLATIONS[lang]['updated']}: "
        f"{format_date(metadata[0]['updated'], lang)}"
    )


TRANSLATIONS = {
    "en": {
        "title": "Immigration and Emigration in Sweden",
        "y_label": "Number of People per Year",
        "immigration": "Immigration",
        "emigration": "Emigration",
        "net_migration": "Net Migration",
        "source": "Source",
        "updated": "Updated",
    },
    "pl": {
        "title": "Imigracja i Emigracja w Szwecji",
        "y_label": "Liczba Osób Rocznie",
        "immigration": "Imigracja",
        "emigration": "Emigracja",
        "net_migration": "Migracja Netto",
        "source": "Źródło",
        "updated": "Zaktualizowano",
    },
    "sv": {
        "title": "Invandrare och utvandrare, Sverige",
        "y_label": "Antal personer per år",
        "immigration": "Invandrare",
        "emigration": "Utvandrare",
        "net_migration": "Nettomigration",
        "source": "Källa",
        "updated": "Uppdaterad",
    },
}

LOCALE_MAPPING = {
    "en": "en_GB.UTF-8",
    "pl": "pl_PL.UTF-8",
    "sv": "sv_SE.UTF-8",
}

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

pd, metadata = api_client.get_dataframe(
    StatisticsSweden.Endpoint.POPULATION_CHANGES, fields
)

configure_plots()

for lang in ["en", "pl", "sv"]:
    footer = format_footer(metadata, lang)
    fig = plot_sweden_migration(pd, footer, lang)
    plt.savefig(
        f"Annual Immigration and Emigration in Sweden (1875-2023)-{lang}.svg",
        dpi=150,
        bbox_inches="tight",
    )
    plt.close()
