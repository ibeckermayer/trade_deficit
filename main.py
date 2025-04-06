import pandas as pd
import requests
import matplotlib.pyplot as plt

# Insert your FRED API key here:
FRED_API_KEY = "d9c81d3f7cebab38286e3eac02d1d075"


def fetch_fred_data(series_id):
    """Fetch data from FRED for a given series ID."""
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {"series_id": series_id, "api_key": FRED_API_KEY, "file_type": "json"}
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data["observations"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    return df


# Fetch nominal personal saving data (PMSAVE) in billions of dollars, seasonally adjusted
df_pmsave = fetch_fred_data("PMSAVE")

# Fetch the Consumer Price Index for All Urban Consumers (CPIAUCSL)
df_cpi = fetch_fred_data("CPIAUCSL")

# Merge the datasets on the date index.
df = pd.merge(
    df_pmsave, df_cpi, left_index=True, right_index=True, suffixes=("_pmsave", "_cpi")
)

# Calculate Real (Inflation-Adjusted) PMSAVE
df["real_pmsave"] = df["value_pmsave"] / (df["value_cpi"] / 100)

# Plot the inflation-adjusted PMSAVE
plt.figure(figsize=(10, 6))
plt.plot(df.index, df["real_pmsave"], label="Real PMSAVE", color="b")
plt.xlabel("Date")
plt.ylabel("Inflation Adjusted PMSAVE (Billions of Dollars)")
plt.title("Inflation Adjusted Personal Savings (Real PMSAVE)")
plt.legend()
plt.tight_layout()
plt.show()
