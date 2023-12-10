""" stuff """
from dataclasses import dataclass

JARS_KEY = "spark.jars"
PACKAGES_KEY = "spark.jars.packages"
KEYFILE_KEY = "spark.hadoop.google.cloud.auth.service.account.json.keyfile"

JAR_FOLDER = "jars"


@dataclass
class ProjectConfig:
    """config for working with GCP projects"""

    VIEWS_BOOLEAN_STRING: str  # string value of boolean
    WRITE_PROJECT: str  # project to write to
    WRITE_DATASET: str  # dataset to write to
    DATABASE: str  # database like snowflake or bigquery
    BUCKET: str  # set gcs or s3 bucket name here
