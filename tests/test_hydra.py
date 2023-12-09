import hydra
from omegaconf import DictConfig, OmegaConf


@hydra.main(config_path="../spark_loader/local_settings", config_name="local")
def test_my_app(cfg: DictConfig):
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    test_my_app()
