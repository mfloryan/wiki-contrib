import pandas as pd
import pycountry


european_countries = {
    'AL', 'AD', 'AT', 'BE', 'BA', 'BG', 'HR', 'CY', 'CZ', 'DK', 
    'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IS', 'IE', 'IT', 'LV', 
    'LI', 'LT', 'LU', 'MT', 'MC', 'ME', 'NL', 'MK', 'NO', 'PL', 
    'PT', 'RO', 'SM', 'RS', 'SK', 'SI', 'ES', 'SE', 'CH', 'GB',
    'VA', 'UA', 'MD', 'BY'
}


def convert_country_code(code3):
    try:
        return pycountry.countries.get(alpha_3=code3).alpha_2
    except (AttributeError, KeyError):
        return None


def get_color(value):
    if value <= 30000:
        return '#fee5d9'
    elif value <= 40000:
        return '#fcc5c0'
    elif value <= 50000:
        return '#fa9fb5'
    elif value <= 60000:
        return '#f768a1'
    elif value <= 70000:
        return '#dd3497'
    elif value <= 80000:
        return '#ae017e'
    else:
        return '#7a0177'


def generate_css():
    color_groups = df_europe.groupby('color')['country'].apply(list)

    css_rules = []
    for color, countries in color_groups.items():
        country_selectors = [f"#{code.lower()}" for code in countries]
        selector = ','.join(country_selectors)
        css_rules.append(f"{selector} {{fill:{color}}}")

    return '\n'.join(css_rules)


df = pd.read_csv(
    'API_NY.GDP.PCAP.PP.CD_DS2_en_csv_v2_46/API_NY.GDP.PCAP.PP.CD_DS2_en_csv_v2_46.csv',
    skiprows=4)

df = df.drop(df.columns[-1], axis=1)
df = df.drop(df.columns[2:60], axis=1)
df['country'] = df['Country Code'].apply(convert_country_code)
df['latest'] = df['2023'].combine_first(df['2022'])

df_europe = df[df['country'].isin(european_countries)]
df_europe.dropna(subset=['latest'], inplace=True)

min_val = (df_europe['latest'].min() // 10000) * 10000
max_val = ((df_europe['latest'].max() // 10000) + 1) * 10000

print(f"Min value (rounded to 10k): {min_val}")
print(f"Max value (rounded to 10k): {max_val}")

ranges = [0, 30000, 40000, 50000, 60000, 70000, 80000, float('inf')]

# Let's see how this distributes
bins = pd.cut(df_europe['latest'],
              bins=ranges,
              include_lowest=True)
print(bins.value_counts().sort_index())

df_europe['color'] = df_europe['latest'].apply(get_color)

print(generate_css())
