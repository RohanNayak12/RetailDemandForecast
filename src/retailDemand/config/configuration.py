from src.retailDemand.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from src.retailDemand.entity.config_entity import DataInjestionConfig
from src.retailDemand.utils.common import createDir, read_yaml


class ConfigurationManager:
    def __init__(
            self,
            config_file_path=CONFIG_FILE_PATH,
            params_file_path=PARAMS_FILE_PATH):
        
        self.config=read_yaml(config_file_path)
        self.params=read_yaml(params_file_path)

        createDir([self.config.artifacts_root])

    def getDataInjestionConfig(self)->DataInjestionConfig:
        config=self.config.data_injestion

        createDir([config.root_dir])
        data_injestion_config=DataInjestionConfig(
            root_dir=config.root_dir,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir,
            source_url=config.source_url
        )
        return data_injestion_config