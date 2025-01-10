from datetime import timedelta
import requests
import requests_cache
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


def load_data():
    url = (
        "https://api.scb.se/"
        "OV0104/v1/doris/sv/ssd/START/"
        "BE/BE0101/BE0101J/ImmiEmiFod"
    )
    query = {
        "query": [
            {
                "code": "Fodelseland",
                "selection": {
                    "filter": "vs:LandISOAlfa2-96TotA",
                    "values": ["TOT"],
                },
            },
            {
                "code": "Kon",
                "selection": {"filter": "item", "values": ["1", "2"]},
            },
        ],
        "response": {"format": "json"},
    }

    response = requests.post(url, json=query, timeout=None)
    response.raise_for_status()
    return response.json()


def process_json_to_df(data_json):
    rows = []
    for entry in data_json["data"]:
        fodelseland, kon, year = entry["key"]
        invandringar, utvandringar = entry["values"]

        rows.append(
            {
                "gender": kon,
                "year": year,
                "in": int(invandringar),
                "out": int(utvandringar),
            }
        )

    df = pd.DataFrame(rows)

    return df


requests_cache.install_cache(
    cache_name="../../http_cache",
    backend="filesystem",
    expire_after=timedelta(days=30),
    allowable_methods=("GET", "POST"),
)


data = load_data()
df = process_json_to_df(data)

yearly_totals = (
    df.groupby("year").agg({"in": "sum", "out": "sum"}).reset_index()
)


fm.fontManager.addfont(
    "/Users/mfloryan/Library/Fonts/LiberationSans-Regular.ttf"
)
fm.fontManager.addfont("/Users/mfloryan/Library/Fonts/LiberationSans-Bold.ttf")
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
    }
)

plt.figure(figsize=(12, 6))
# plt.style.use('seaborn-v0_8-whitegrid')
ax = plt.gca()


plt.plot(
    yearly_totals["year"],
    yearly_totals["in"],
    label="_nolegend_",
    color="#2B6CB0",
    linewidth=3,
    alpha=0.4,
)
plt.plot(
    yearly_totals["year"],
    yearly_totals["in"],
    label="immigration",
    marker="o",
    linestyle="none",
    color="#2B6CB0",
)
plt.plot(
    yearly_totals["year"],
    yearly_totals["out"],
    label="_nolegend_",
    color="#C05621",
    linewidth=3,
    alpha=0.4,
)
plt.plot(
    yearly_totals["year"],
    yearly_totals["out"],
    label="emigration",
    marker="o",
    linestyle="none",
    color="#C05621",
)

plt.gca().yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, p: format(int(x), ","))
)

plt.title("Swedish migration per year ", fontweight="bold")
plt.grid(True, linestyle="--", alpha=0.7)

plt.xticks(rotation=45)
plt.ylim(bottom=0)
plt.legend(facecolor="white", edgecolor="silver", borderpad=1)

ax.tick_params(length=0)

for spine in ax.spines.values():
    spine.set_color("silver")

plt.tight_layout()

footer_text = (
    f"Source: Statistics Sweden {data['metadata'][0]['source']}"
    f" - {data['metadata'][0]['label']} ({data['metadata'][0]['infofile']})"
)

plt.figtext(
    0.08, 0.02, footer_text, wrap=True, ha="left", va="bottom", fontsize=10
)
plt.subplots_adjust(bottom=0.15)

plt.savefig(
    "Statistics Sweden (SCB) annual Immigration and Emigration 2000-2023.svg",
    dpi=150,
    bbox_inches="tight",
)
plt.close()
