from prophet import Prophet
import pickle
from src.retailDemand import logger
from src.retailDemand.entity.config_entity import PrepareBaseModelConfig

class BaseModelPrep:
    def __init__(self,config:PrepareBaseModelConfig):
        self.config=config
        self.model=None
    
    def getBaseModel(self)->Prophet:
        model=Prophet(
            seasonality_mode=self.config.seasonality_mode,
            daily_seasonality=self.config.seasonality_mode,
            weekly_seasonality=self.config.weekly_seasonality,
            yearly_seasonality=self.config.yearly_seasonality
        )
        logger.info("Base model prepared")
        return model
    
    def save_base_model(self):
        model=self.getBaseModel()
        model_path=self.config.base_model_path
        with open(model_path,'wb') as f:
            pickle.dump(model,f)
        logger.info(f"Model saved at path {model_path}")