"""
Prep of the train and test datasets
"""

PROJECT_DIR = "/home/bensiv/Documents/ITC/Main/FinalProject/ICBA_Project/"

# packages
import os
import numpy as np
import pandas as pd
from datetime import datetime

def get_days_prior(date, period):
    results = pd.date_range(start=date, periods=period)
    return results

def main():
    """program skeleton"""

    # targets: lab results
    # features: feed + temps
    lab_results = pd.read_csv(os.path.join(PROJECT_DIR,"CSVs", "Raw","LabResults.csv"))
    feed = pd.read_csv(os.path.join(PROJECT_DIR,"CSVs", "Raw","Feed.csv"))
    temps = pd.read_csv(os.path.join(PROJECT_DIR,"CSVs", "Others","Temps.csv"))

    # converting Date to datetime
    for df in [lab_results, feed, temps]:
        df['Date'] = pd.to_datetime(df['Date'])#, unit="D")

    # Omitting Non-Dairy cattle groups from the data
    feed = feed[feed.Group_name.str.match("Dairy")]

    # Converting the quantities to be per cow
    feed.Quantity = feed.Quantity / feed.Num_of_cows

    #  combining features first
    features = pd.merge(feed, temps, on="Date")

    # assign sample groups based on the date of the sample
    sample_dates = lab_results.Date.unique()
    sample_dates_df = pd.DataFrame({"Date":sample_dates, "Sample":range(1,len(sample_dates)+1)})
    targets = pd.merge(lab_results, sample_dates_df, on="Date")
    

    sample_range = np.array([]).astype(np.datetime64)
    sample_num = np.array([]).astype(np.int64)
    week = 7 # days
    for (num, date) in enumerate(sample_dates):
        sample_range = np.concatenate([sample_range, pd.date_range(start=date, periods=week)])
        sample_num = np.concatenate([sample_num, np.array([num]*(week))])

    sample_range_df = pd.DataFrame({"Date":sample_range, "Sample":sample_num})

    features = pd.merge(features, sample_range_df, on="Date", how="left")

    features.dropna(subset=["Sample"], inplace=True)

    # combining features with targets
    data = pd.merge(features, targets, on=["Group", "Sample"], how="left")

    col_to_drop = ["Somatic_cells", "Group_name", "Units", "Num_of_cows", "Feed_name", "Feed_num", "Date_y"]
    data.drop(columns=col_to_drop, inplace=True)
    data.rename(columns={"Date_x" : "Date"}, inplace=True)

    data.Feed_ID = [f"feed{i}" for i in data.Feed_ID]
    

if __name__ == "__main__":
    main()


