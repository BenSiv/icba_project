"""
Prep of the train and test datasets
"""


# packages
import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime

def get_days_prior(date, period):
    results = pd.date_range(start=date, periods=period)
    return results

def main():
    """program skeleton"""

    WeekBeforeSample = pd.read_csv(os.path.join(PROJECT_DIR,"data", "combined", "WeekBeforeSample.csv"))
    WeekBeforeSample.drop(columns=["Unnamed: 0"], inplace=True)

    X = WeekBeforeSample.drop(columns=["Milk","Fat","Protein","Lactose"])
    y = WeekBeforeSample[["Sample","Milk","Fat","Protein","Lactose"]]

    # train 60%, validation 20%, test, 20%
    seps = np.linspace(0,len(y),10).astype(int)
    split_indices = {
        "train" : (seps[0],seps[5]),
        "val" : (seps[5],seps[7]),
        "test" : (seps[7],seps[9])
    }

    data_sets = dict()
    for data_set in ["train", "val", "test"]:
        start, end = split_indices[data_set]
        data_sets[data_set] = WeekBeforeSample.iloc[start:end , :]

    for data_set, data in data_sets.items():
        data.to_csv(os.path.join(PROJECT_DIR,"data", "splitted", f"{data_set}.csv"))



if __name__ == "__main__":
    # PROJECT_DIR = "/home/bensiv/Documents/ITC/Main/FinalProject/ICBA_Project/PySrc/icba_project"
    args = sys.argv
    if len(args) == 1:
        PROJECT_DIR = os.getcwd()
    else:
        PROJECT_DIR = args[1]

    main(PROJECT_DIR)


