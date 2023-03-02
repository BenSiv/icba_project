"""
model test for the week before sample dataset
"""

# packages
import os
import sys
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
# from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

def train_per_col(X, y, model):
    regressor_dict = dict()
    for col in y:
        regressor_dict[f"reg_{col}"] = model()
        regressor_dict[f"reg_{col}"].fit(X, y[col])
    return regressor_dict

def plot_time_series_prediction(X, y, regressor_dict, test_date, output_dir):
    for col in y:
        y_pred = regressor_dict[f"reg_{col}"].predict(X)
        temp_df = pd.DataFrame({"ground_truth" : y[col].reset_index(drop=True) ,"prediction" : y_pred})
        # print(f"""R squered: {r2_score(temp_df["ground_truth"], temp_df["prediction"])}""")
        temp_df.plot()
        plt.ylabel(col)
        # adding a line of the point of testing
        x_point = [test_date]*len(temp_df)
        y_range = np.linspace(temp_df.min().min(),temp_df.max().max(),len(temp_df))
        plt.plot(x_point, y_range, linestyle="dashed")
        plt.title(f"""model: {regressor_dict[f"reg_{col}"].__class__.__name__}""")
        plt.savefig(os.path.join(output_dir, f"{col}.png"))



def main(PROJECT_DIR):
    """program skeleton"""
    data_set = pd.read_csv(os.path.join(PROJECT_DIR,"data", "combined", "WeekBeforeSample.csv"))

    X = data_set.drop(columns=["Milk","Fat","Protein","Lactose"]).set_index("Sample")
    y = data_set[["Sample","Milk","Fat","Protein","Lactose"]].set_index("Sample")

    train_set = pd.read_csv(os.path.join(PROJECT_DIR,"data", "splitted", "week_before","train.csv"))
    # val_set = pd.read_csv(os.path.join(PROJECT_DIR,"data", "splitted", "week_before","val.csv"))

    X_train = train_set.drop(columns=["Milk","Fat","Protein","Lactose"]).set_index("Sample")
    y_train = train_set[["Sample","Milk","Fat","Protein","Lactose"]].set_index("Sample")

    # X_val = val_set.drop(columns=["Milk","Fat","Protein","Lactose"]).set_index("Sample")
    # y_val = val_set[["Sample","Milk","Fat","Protein","Lactose"]].set_index("Sample")

    regressor_dict = train_per_col(X_train, y_train, GradientBoostingRegressor)
    
    output_dir = os.path.join(PROJECT_DIR,"figures", "week_before", "gradient_boosting")
    test_date = X_train.index[-1]
    plot_time_series_prediction(X, y, regressor_dict, test_date, output_dir)


if __name__ == "__main__":
    # PROJECT_DIR = "/home/bensiv/Documents/ITC/Main/FinalProject/ICBA_Project/PySrc/icba_project"
    args = sys.argv
    if len(args) == 1:
        PROJECT_DIR = os.getcwd()
    else:
        PROJECT_DIR = args[1]

    main(PROJECT_DIR)