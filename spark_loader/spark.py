from dataclasses import dataclass, field

import pyspark
import yaml
from omegaconf import OmegaConf

from spark_loader import root
from spark_loader.config import JAR_FOLDER, JARS_KEY, KEYFILE_KEY, PACKAGES_KEY
from spark_loader.logging import logger_factory

logger = logger_factory(10)


def setSparkConfig(settings: dict, conf: pyspark.SparkConf) -> None:
    for setting, value in settings["spark"].items():
        if setting == JARS_KEY:
            value = ",".join([f"{root}/{JAR_FOLDER}/{item}" for item in value])
        if setting == PACKAGES_KEY:
            value = ",".join(value)
        if setting == KEYFILE_KEY:
            value = f"{root}/{value}"
        logger.debug("showing settings: ", key=setting, value=value)
        conf.set(setting, value)


def loadSettings(yaml_settings_path) -> dict:
    with open(file=yaml_settings_path, mode="r", encoding="UTF8") as infile:
        return yaml.load(infile, yaml.Loader)


def NewSparkSession(
    master: str, app: str, yaml_settings_path: str, log_level: str = "error"
) -> pyspark.sql.SparkSession:
    """creates a new spark session"""
    try:
        settings = loadSettings(yaml_settings_path)
        conf = pyspark.SparkConf().setMaster(master).setAppName(app)
        setSparkConfig(settings, conf)
        sc = pyspark.SparkContext(conf=conf)
        context = sc.getOrCreate()
        context.setLogLevel(log_level)
        return pyspark.sql.SparkSession(context).builder.getOrCreate()

    except ValueError as exception:
        logger.exception("failed to create new session", exception=exception)
        return pyspark.sql.SparkSession.getActiveSession()


@dataclass
class SparkClient:
    """handles spark connection and dataframe loading"""

    spark: pyspark.sql.SparkSession
    cfg: OmegaConf = field(default=OmegaConf.load(rf"{root}/conf/local.yaml"))

    def __post_init__(self):
        self.db_type = self.cfg.database
        self.options = {
            "viewsEnabled": self.cfg.bigquery.viewsEnabled,
            "parentProject": self.cfg.bigquery.parentProject,
            "materializationDataset": self.cfg.bigquery.materializationDataset,
        }

    def __repr__(self):
        return repr(rf"spark connector, {self.options}")

    def getData(self, query: str) -> pyspark.sql.DataFrame:
        return (
            self.spark.read.format(self.db_type)
            .options(**self.options)
            .option("query", query)
            .load()
        )

    @staticmethod
    def writeToGcs(df: pyspark.sql.DataFrame, bucket: str, file_name: str) -> None:
        df.write.parquet(f"gs://{bucket}/{file_name}.parquet")
