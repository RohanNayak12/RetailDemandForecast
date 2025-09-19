from typing import Any, Dict
from src.retailDemand.components.model_pred import ModelPredictor
from src.retailDemand.config.configuration import ConfigurationManager
from src.retailDemand import logger
from src.retailDemand.entity.config_entity import ModelPredictionConfig


class ModelPredictorPipeline:
    def __init__(self,store_id:int,date:str):
        self.store_id=store_id
        self.date=date

    def main(self)->Dict[str,Any]:
        config=ConfigurationManager()
        model_pred=ModelPredictor(config.getModelPredConfig())
        model_pred.load_models()
        return model_pred.predSales(self.store_id,self.date)  

STAGE_NAME= "Model Prediction Stage"

if __name__=="__main__":
    try:
        logger.info(f">>>>>>>> stage {STAGE_NAME} started <<<<<<<")
        obj= ModelPredictorPipeline()
        obj.main()
        logger.info(f">>>>>>>> stage {STAGE_NAME} ended <<<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e