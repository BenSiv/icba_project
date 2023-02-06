"""
model test for the week before sample dataset
"""

# packages
import os
import sys
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import r2_score
import matplotlib.pyplot as plt


def main(PROJECT_DIR):
    """program skeleton"""
    train_set = pd.read_csv(os.path.join(PROJECT_DIR,"data", "splitted", "week_before","train.csv"))
    val_set = pd.read_csv(os.path.join(PROJECT_DIR,"data", "splitted", "week_before","val.csv"))

    X_train = train_set.drop(columns=["Milk","Fat","Protein","Lactose"]).set_index("Sample")
    y_train = train_set[["Sample","Milk","Fat","Protein","Lactose"]].set_index("Sample")

    X_val = val_set.drop(columns=["Milk","Fat","Protein","Lactose"]).set_index("Sample")
    y_val = val_set[["Sample","Milk","Fat","Protein","Lactose"]].set_index("Sample")

    regressor_dict = dict()
    for col in y_train:
        regressor_dict[f"reg_{col}"] = RandomForestRegressor()
        regressor_dict[f"reg_{col}"].fit(X_train, y_train[col])

    for col in y_train:
        y_pred = regressor_dict[f"reg_{col}"].predict(X_val)
        temp_df = pd.DataFrame({"ground_truth" : y_val[col].reset_index(drop=True) ,"prediction" : y_pred})
        # print(f"""R squered: {r2_score(temp_df["ground_truth"], temp_df["prediction"])}""")
        temp_df.plot()
        plt.ylabel(col)
        plt.savefig(os.path.join(PROJECT_DIR,"figures", "week_before", "random_forest", f"{col}.png"))

if __name == "__main__":
    # PROJECT_DIR = "/home/bensiv/Documents/ITC/Main/FinalProject/ICBA_Project/PySrc/icba_project"
    args = sys.argv
    if len(args) == 1:
        PROJECT_DIR = os.getcwd()
    else:
        PROJECT_DIR = args[1]

    main(PROJECT_DIR)