import pandas as pd
import os
from tools import Timer
T = Timer() # instantiate timer

# Import data, remove superfluous columns
raw_data = "20250114 Impact of Tiering - 3 Standards Copy.xlsx"
processed_data = "Tiering.csv"
epoch_data = "Tiering_Status_Epochs.csv"

if os.path.exists("Data/" + processed_data) == False:
    
    # Importing and filtering raw data
    T.start("Importing data")
    df_full = pd.read_excel("Data/"+ raw_data, sheet_name="CWT CRS Provider Extract")
    df = df_full.drop(columns=["Region", "ICB", "Alliance", "Provider"])
    T.stop("Importing data")

    T.start("Export to CSV")
    df.to_csv("Data/" + processed_data, index=False)
    T.stop("Export to CSV")

else:

    # Loading pre-filtered data
    T.start("Importing CSV data")
    df = pd.read_csv("Data/"+ processed_data)
    T.stop("Importing CSV Data")



if os.path.exists("Data/" + epoch_data) == False:
    # Sort by standard, org code, cancer type, date
    df = df.sort_values(by=["STANDARD", "ORG CODE", "CANCER TYPE", "PERIOD"])

    
    # Start at the first epoch
    T.start("Calculate epochs")
    df["Epoch"] = 1
    
    # When tiering status changes, increment 1 to epoch 
    df["Epoch"] = df.groupby(["ORG CODE", "STANDARD", "CANCER TYPE"])["Tiering Status"].apply(lambda x: (x != x.shift()).cumsum()
                                                                                            ).reset_index(level=[0,1,2], drop=True)
    
    # Export epoch
    df.to_csv("Tiering_Status_Epochs.csv", index=False)
    T.stop("Calculate epochs, export epoch data")

else:
    print("Epochs already calculated")