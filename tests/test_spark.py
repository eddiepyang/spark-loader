from spark_loader import root
from spark_loader.spark import NewSparkSession


def test_NewSparkSession():
    session = NewSparkSession(
        "local", "local", f"{root}/spark_loader/local_settings/local.yaml"
    )
    assert session.active()
    assert session.conf.get("spark.driver.memory") == "16g"


if __name__ == "__main__":
    session = NewSparkSession(
        "local", "local", f"{root}/spark_loader/local_settings/local.yaml"
    )
    data = range(10000)
    distData = session.sparkContext.parallelize(data)
    print(session.active())
    print(distData.filter(lambda x: not x & 1).take(10))
