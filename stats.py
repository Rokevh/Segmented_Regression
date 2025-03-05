import datetime as dt
import pandas as pd
from scipy.stats import linregress
from tools import Timer
T = Timer()

# Export epoch data
epoch_trends = "epoch_trends.csv"
org_trends = "org_trends.csv"

# Import tiering data
tiering_data = "Tiering.csv"
raw_df = pd.read_csv("Data/" + tiering_data)


# Calculate tiering epochs
temp_df = raw_df[["ORG CODE", "PERIOD", "STANDARD", "TOTAL TREATED", "WITHIN STANDARD", "Tiering Status"]]
temp_df = temp_df.sort_values(by=["ORG CODE", "STANDARD", "PERIOD"])

temp_df["Date"] = pd.to_datetime(temp_df["PERIOD"])
temp_df["Ordinal"] = temp_df["Date"].map(dt.datetime.toordinal)

df = temp_df.groupby(["ORG CODE", "STANDARD", "PERIOD", "Ordinal", "Tiering Status"], as_index=False)[["TOTAL TREATED", "WITHIN STANDARD"]].sum()

df["Performance"] = df["WITHIN STANDARD"] / df["TOTAL TREATED"]
print(df)
df.to_csv("Data/cumulative_performance.csv", index=False)

df["Epoch"] = df.groupby(["ORG CODE", "STANDARD"])["Tiering Status"].transform(
    lambda x: (x != x.shift()).cumsum()
)

group_list = ["ORG CODE", "STANDARD", "Epoch", "Tiering Status"]

def slopes(df, group_list):
    
    slope_data = []
    
    T.start("Calculate slopes")
    grouped = df.groupby(group_list)
    for group_name, group in grouped:
        if group["Ordinal"].nunique() == 1:
            slope = float("nan")
            intercept = float("nan")
        elif len(group) > 1:
            slope, intercept, _, _, _ = linregress(group["Ordinal"], group["Performance"])
        else:
            slope = float("nan")
            intercept = float("nan")

        start_date = group["Ordinal"].min()
        end_date = group["Ordinal"].max()
        
        slope_data.append(
                {
                **dict(zip(group_list, group_name)),
                "slope": slope,
                "intercept": intercept,
                "start_date": start_date,
                "end_date": end_date
                }
            )
    T.stop("Calculate slopes")
    return pd.DataFrame(slope_data)
    
epoch_slopes_df = slopes(df, group_list)
org_slopes_df = slopes(df, ["ORG CODE", "STANDARD"])

epoch_slopes_df.to_csv("Data/"+ epoch_trends, index=False)
org_slopes_df.to_csv("Data/"+ org_trends, index=False)