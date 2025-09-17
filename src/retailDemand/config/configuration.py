from pathlib import Path
from src.retailDemand.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from src.retailDemand.entity.config_entity import DataInjestionConfig, ModelEvaluationConfig, ModelPredictionConfig, ModelTrainingConfig,PrepareBaseModelConfig
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
            source_url=config.source_url,
            final_dataset_dir=config.final_dataset_dir
        )
        return data_injestion_config
    
    def getPrepareBaseModelConfig(self)->PrepareBaseModelConfig:
        config=self.config.prepare_base_model

        createDir([config.root_dir])
        prepare_base_model_config=PrepareBaseModelConfig(
            root_dir=Path(config.root_dir),
            base_model_path=Path(config.base_model_path),
            seasonality_mode=str(config.seasonality_mode),
            weekly_seasonality=bool(config.weekly_seasonality),
            daily_seasonality=bool(config.daily_seasonality),
            yearly_seasonality=bool(config.yearly_seasonality)
        )

        return prepare_base_model_config
    
    def getModelTrainingConfig(self)-> ModelTrainingConfig:
        config=self.config.model_train

        createDir([config.root_dir])
        model_train_config=ModelTrainingConfig(
            root_dir=Path(config.root_dir),
            trained_model_path=Path(config.trained_model_path),
            dataset_path=Path(config.dataset_path),
            base_model_path=Path(config.base_model_path),
            store_column=self.params.STORE_COLUMN,
            date_column=self.params.DATE_COLUMN,
            target_column=self.params.TARGET_COLUMN,
            train_split=self.params.TRAIN_SPLIT
        )
        return model_train_config
    
    def getModelEvaluationConfig(self)->ModelEvaluationConfig:
        config=self.config.model_evaluation

        createDir([config.root_dir])
        model_eval_config=ModelEvaluationConfig(
            root_dir=Path(config.root_dir),
            evaluation_results_path=Path(config.evaluation_results_path),
            train_split=self.params.TRAIN_SPLIT,
            forecast_periods=self.params.FORECAST_PERIODS,
            frequency=self.params.FREQUENCY,
            dataset_path=Path(config.dataset_path),
            model_path=Path(config.model_path),
            store_column=self.params.STORE_COLUMN,
            date_column=self.params.DATE_COLUMN,
            target_column=self.params.TARGET_COLUMN
        )
        return model_eval_config
    
    def getModelPredConfig(self)->ModelPredictionConfig:
        config=self.config.model_prediction

        createDir([config.root_dir])
        model_pred_config=ModelPredictionConfig(
            root_dir=Path(config.root_dir),
            dataset_path=Path(config.dataset_path),
            model_path=Path(config.model_path)
        )
        return model_pred_config