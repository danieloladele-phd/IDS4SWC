import time
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.decomposition import PCA
from sklearn.feature_selection import RFE


def concatenate_csv_files(data_list, size):
    concatenated_df = pd.DataFrame()  # Create an empty DataFrame to store concatenated data
    total_size = len(data_list)
    
    if len(data_list) <= size:
        raise ValueError("size is greater than lenght of list")
    
    for i in range(size):
        df = pd.read_csv(data_list[i])  # Load the CSV file as a DataFrame
        concatenated_df = pd.concat([concatenated_df, df], ignore_index=True)  # Concatenate with previous data
    
    return concatenated_df


def load_dataset(number_sample = 15, y_label = 'label', test_size = 0.3, random_state = 45):
    data = concatenate_csv_files(data_list_path, number_sample)
    
    X = data.drop(columns=[y_label])
    y = data[y_label]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    return X_train, X_test, y_train, y_test


def train_rf_model(X_train, y_train):
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    return rf_model

def evaluate_rf_model(model, X_test, y_test):
    y_prediction = model.predict(X_test)
    report = classification_report(y_test, y_prediction, output_dict=True)
    return report

def apply_rfe(model, X_train, y_train, num_features_to_keep=15):
    rfe_selector = RFE(estimator=model, n_features_to_select=num_features_to_keep)
    rfe_selector = rfe_selector.fit(X_train, y_train)
    X_train_selected = rfe_selector.transform(X_train)
    return X_train_selected

def main():
    # load data
    rt = os.getcwd() + '/data/CICIoT2023'
    data_list_path = [os.path.join(rt, file) for file in os.listdir(rt)]

    X_train, X_test, y_train, y_test = load_dataset()

    start_time_eval = time.time()
    rf_model = train_rf_model(X_train, y_train)
    end_time_eval = time.time()
    result_time = end_time_eval - start_time_eval
    print(f"Training Time before Recursive feature selection: {result_time:.8f} seconds")

    start_time_eval = time.time()
    init_report = evaluate_rf_model(rf_model, X_test, y_test)
    end_time_eval = time.time()
    result_time = end_time_eval - start_time_eval
    print(f"Inferencing Time before Recursive feature selection: {result_time:.8f} seconds")
    print(init_report)

    X_train_selected = apply_rfe(rf_model, X_train, y_train)

    start_time_eval = time.time()
    rf_model_selected = train_rf_model(X_train_selected, y_train)
    end_time_eval = time.time()
    result_time = end_time_eval - start_time_eval
    print(f"Training Time after Recursive feature selection: {result_time:.8f} seconds")

    X_test_selected = apply_rfe(rf_model, X_test, y_test)
    start_time_eval = time.time()
    report = evaluate_rf_model(rf_model_selected, X_test_selected, y_test)
    end_time_eval = time.time()
    result_time = end_time_eval - start_time_eval
    print(f"Inferencing Time after Recursive feature selection: {result_time:.8f} seconds")
    print(report)

if __name__ == "__main__":
    main()
