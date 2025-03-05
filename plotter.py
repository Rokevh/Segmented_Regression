import pandas as pd
import matplotlib.pyplot as plt

# File names
performance = "Data/cumulative_performance.csv"
epoch = "Data/epoch_trends.csv"

performance_df = pd.read_csv(performance)
epoch_df = pd.read_csv(epoch)

print(performance_df)


plot_org = "RBT"
plot_std = "28-day FDS"

df_filtered = performance_df[
    (performance_df["ORG CODE"] == plot_org) & (performance_df["STANDARD"] == plot_std)
    ]
plt.figure(figsize=(10,6))
plt.plot(
    df_filtered["Ordinal"],
    df_filtered["Performance"],
    marker="o",
    label=plot_org
)

tier_colors = {
    "1": "red",
    "2": "orange",
    "ROE": "green"
}

for _, row in epoch_df.iterrows():
    if row["ORG CODE"] == plot_org and row["STANDARD"] == plot_std:

        slope = row["slope"]
        start_date = row["start_date"]
        end_date = row["end_date"]
        tiering_status = row["Tiering Status"]

        start_performance = df_filtered[
            df_filtered["Ordinal"] == start_date
        ]["Performance"]

        date_range = df_filtered.loc[
            (df_filtered["Ordinal"] >= start_date)
            & (df_filtered["Ordinal"] <= end_date)
        ]["Ordinal"]
        print(type(date_range))

        plt.axvspan(start_date, end_date, color=tier_colors[tiering_status], alpha=0.3)

        #y_range = [float(start_performance) + float(slope) * (float(x) - date_range.iat[1]) for x in date_range] # float(x) may cause issues in future
        
        #plt.plot(date_range, y_range, color=tier_colors[tiering_status])

plt.show()