import pandas as pd
import matplotlib.pyplot as plt

# Import files
cumul_perf = "Data/cumulative_performance.csv"
epoch = "Data/epoch_trends.csv"

perf_df = pd.read_csv(cumul_perf)
epoch_df = pd.read_csv(epoch)

"""
Currently placeholding user input. Would love to handle the changing graphs without editing the source code.
"""
plot_org = "REM"
plot_std = "28-day FDS"

tier_colors = {
    "1": "red",
    "2": "orange",
    "ROE": "green"
}

p_filter_df = perf_df[
    (perf_df["ORG CODE"] == plot_org) & (perf_df["STANDARD"] == plot_std)
]

fig, (ax1, ax2) = plt.subplots(2, figsize=(10,6))
axs = [ax1,ax2]
ax1.plot(
    p_filter_df["Ordinal"],
    p_filter_df["Performance"],
    zorder=10
)

ax2.plot(
    p_filter_df["Ordinal"],
    p_filter_df["TOTAL TREATED"],
    color="r",
    zorder=10
)
ax2.plot(
    p_filter_df["Ordinal"],
    p_filter_df["WITHIN STANDARD"],
    color="g",
    zorder=10
)

fill_kwargs = {
    "alpha": 0.3,
    "zorder": 1
}

ax2.set_ylim(None, None)
ax2.fill_between(p_filter_df["Ordinal"], p_filter_df["WITHIN STANDARD"], color="g", **fill_kwargs)
ax2.fill_between(p_filter_df["Ordinal"], p_filter_df["WITHIN STANDARD"], p_filter_df["TOTAL TREATED"], color="r", **fill_kwargs)

for ax in axs:
    ax.xaxis.set_ticklabels(p_filter_df["PERIOD"])


for ax in (ax1, ax2):
    for _, row in epoch_df.iterrows():
        if row["ORG CODE"] == plot_org and row["STANDARD"] == plot_std:
            
            slope = row["slope"]
            start_date = row["start_date"]
            end_date = row["end_date"]
            intercept = row["intercept"]
            tiering_status = row["Tiering Status"]

            date_range = p_filter_df.loc[
                (p_filter_df["Ordinal"] >= start_date)
                & (p_filter_df["Ordinal"] <= end_date)
            ]["Ordinal"]

            ax.axvspan(
                (start_date-10), 
                (end_date+10), 
                color=tier_colors[tiering_status], 
                zorder=2,
                alpha=0.3
            )


            y_range = [slope * (x + intercept/slope) for x in date_range]
            ax1.plot(date_range, y_range, color=tier_colors[tiering_status])


# Define a function that displays all providers in one massive plot. Ideally, I'd
# want this to be organised by how well 

plt.show()