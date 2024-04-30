#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import wandb
import pandas as pd



logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)
    logger.info("Downloading the artifact to get the data")
    artifact = run.use_artifact(args.input_artifact)
    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    df['last_review'] = pd.to_datetime(df['last_review'])
    df = df.dropna()
    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()
    df.to_csv('clean_sample.csv', index=False)
    artifact = wandb.Artifact(
        name=args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    logger.info("Logging clean artifact")
    run.log_artifact(artifact)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This steps cleans the data")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="raw_data",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="clean_sample.csv",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="clean_sample",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="Changes done to clean the raw data",
        required = True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="min valid price of the home per night",
        required = True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="max valid price of the home per night",
        required = True
    )


    args = parser.parse_args()

    go(args)
