"""
Prep of the train and test datasets
"""

# packages
import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime

def main(PROJECT_DIR):
    """program skeleton"""

    # targets: lab results
    # features: feed
    lab_results = pd.read_csv(os.path.join(PROJECT_DIR,"data", "raw", "LabResults.csv"))
    feed = pd.read_csv(os.path.join(PROJECT_DIR,"data", "raw", "Feed.csv"))

    # converting Date to datetime
    for df in [lab_results, feed]:
        df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d")

    # omitting Non-Dairy cattle groups from the data
    feed = feed[feed.Group_name.str.match("Dairy")]

    # converting the quantities to be per cow
    feed.Quantity = feed.Quantity / feed.Num_of_cows

    # filtering the feed dataframe to the measurments only
    feed_measurments = pd.read_csv(os.path.join(PROJECT_DIR,"data", "others", "Feed_measure.csv"))
    features = feed.merge(feed_measurments)

    # assign sample groups based on the date of the sample
    sample_dates = lab_results.Date.unique()
    sample_dates_df = pd.DataFrame({"Date":sample_dates, "Sample":range(1,len(sample_dates)+1)})
    targets = pd.merge(lab_results, sample_dates_df, on="Date")
    targets.drop(columns=["Somatic_cells","Group"], inplace=True)
    targets = targets.groupby("Date").mean().reset_index()
    
    # average all groups by date 
    feed_measure_dict = features.set_index("Feed_ID")["Feed_name"].drop_duplicates().to_dict()
    features.drop(columns=["Group","Group_name","Feed_num","Feed_name","Units","Num_of_cows"], inplace=True)
    features = features.groupby(["Date","Feed_ID"]).mean().reset_index()

    sample_range = np.array([]).astype(np.datetime64)
    sample_num = np.array([]).astype(np.int64)
    day_from_sample = np.array([]).astype(np.int64)
    week = 7 # days
    for (num, date) in enumerate(sample_dates):
        sample_range = np.concatenate([sample_range, pd.date_range(start=date, periods=week)])
        sample_num = np.concatenate([sample_num, np.array([num]*(week))])
        day_from_sample = np.concatenate([day_from_sample, np.arange(week)])

    sample_range_df = pd.DataFrame({"Date":sample_range, "Sample":sample_num, "Day_from_sample" : day_from_sample})

    features = pd.merge(features, sample_range_df, on="Date")
    # features.drop(columns=["Sample"], inplace=True)
    features_wide = features.pivot(index="Sample", columns=["Day_from_sample","Feed_ID"], values="Quantity")
    features_wide.fillna(0, inplace=True)
    features_wide.reset_index(inplace=True)

    targets.drop(columns=["Date"],inplace=True)
    # combining features with targets
    data = pd.merge(features_wide, targets, on="Sample", how="left")
    data.drop(columns=[data.columns[1]], inplace=True)

    data.to_csv(os.path.join(PROJECT_DIR,"data", "combined", "WeekBeforeSample.csv"), index=False)


if __name__ == "__main__":
    # PROJECT_DIR = "/home/bensiv/Documents/ITC/Main/FinalProject/ICBA_Project/PySrc/icba_project"
    args = sys.argv
    if len(args) == 1:
        PROJECT_DIR = os.getcwd()
    else:
        PROJECT_DIR = args[1]

    main(PROJECT_DIR)


