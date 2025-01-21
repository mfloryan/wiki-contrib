from statistics_sweden import StatisticsSweden
import pandas as pd

api_client = StatisticsSweden()

df_groups, metadata1 = api_client.get_dataframe(
    StatisticsSweden.Endpoint.POPULATION_CITIZENSHIP_GROUP,
    {"HDI": ["TOT"], "Kon": ["1+2"], "Alder": ["TOT1"], "Tid": ["2023"]},
)

df_groups.drop(["human_development_index", "sex", "age"], axis=1, inplace=True)
df_groups = df_groups[df_groups.citizenship != "total"]
df_groups["percentage"] = (
    df_groups["number"] / df_groups["number"].sum() * 100
).round(2)

print(df_groups)

df_citizenship, metadata = api_client.get_dataframe(
    StatisticsSweden.Endpoint.FOREIGN_CITIZENS_COUNTRY,
    {
        "Tid": ["2023"],
        "Alder": ["tot"],
    },
)
df_citizenship = df_citizenship[
    df_citizenship.country_of_citizenship != "total"
]

df_citizenship = (
    df_citizenship.groupby(["country_of_citizenship"])["number"]
    .sum()
    .reset_index()
)

df_citizenship.loc[len(df_citizenship)] = [
    "Sweden",
    df_groups[df_groups.citizenship == "Swedish citizenship"]["number"].values[
        0
    ],
]

df_citizenship["percentage"] = (
    df_citizenship["number"] / df_groups["number"].sum() * 100
).round(2)
df_citizenship = df_citizenship.sort_values("number", ascending=False)

print(df_citizenship[df_citizenship.number >= 10_000])

df_birth_country, meta2 = api_client.get_dataframe(
    StatisticsSweden.Endpoint.POPULATION_BIRTH_COUNTRY, {"Tid": ["2023"]}
)

df_birth_country = (
    df_birth_country.groupby(["country_of_birth"])["number"]
    .sum()
    .reset_index()
)

df_birth_country["percentage"] = (
    df_birth_country["number"] / df_birth_country["number"].sum() * 100
).round(2)

df_birth_country = df_birth_country.sort_values("number", ascending=False)

print(df_birth_country[df_birth_country["number"] >= 10_000])

merged_df = pd.merge(
    df_citizenship,
    df_birth_country,
    left_on="country_of_citizenship",
    right_on="country_of_birth",
    how="inner",
    suffixes=("_citizenship", "_birth"),
)

print(merged_df)


def format_wikitable(df, total, n=20):
    df = df.head(n).copy()
    df["percentage"] = (df["number"] / total * 100).round(2)

    # Start table
    wiki = '{| class="wikitable sortable"\n! Narodowość\n! Odsetek\n'

    for _, row in df.iterrows():
        wiki += (
            f"|-\n| {row['country_of_citizenship']} || {row['percentage']}%\n"
        )

    # Close table
    wiki += "|}"

    return wiki


# print(format_wikitable(df_citizenship, df_groups["number"].sum()))
