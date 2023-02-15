# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
# from dotenv import find_dotenv, load_dotenv
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, accuracy_score, classification_report


import mlflow
from datetime import datetime



# mlfow with auto logging

def main(train_filepath, max_depth):
    # with mlflow.start_run():
    training_timestamp = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
    with mlflow.start_run(run_name=f"model_{training_timestamp}"):
        mlflow.autolog()
        """ Runs data processing scripts to turn raw data from (../raw) into
            cleaned data ready to be analyzed (saved in ../interim).
        """
        logger = logging.getLogger(__name__)
        logger.info('making final data set from raw data')

        data = pd.read_csv(train_filepath)

        # Split the data into features and target
        X = data.drop('popularity', axis=1)
        y = data['popularity']

        # Train the model
        rf = RandomForestClassifier(n_estimators=100, max_depth=max_depth, random_state=47)
        rf.fit(X, y)
        y_pred = rf.predict(X)

        # Save the model
        # joblib.dump(rf, models_dir + '/rf.joblib')
        logger.info('Model successfully trained and saved')
        # mlflow.sklearn.log_model(rf, "model")
        # mlflow.log_param("max_depth", max_depth)

        # Evaluate the model
        logger.info('Accuracy: {}'.format(accuracy_score(y, y_pred)))
        print(classification_report(y, y_pred))

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    # load_dotenv(find_dotenv())

    experiment_name = "ep_popularity_news_with_random_forest"
    mlflow.set_experiment(experiment_name)

    for max_depth in [2, 4, 6]:
        main('data/processed/train.csv', max_depth=max_depth)


