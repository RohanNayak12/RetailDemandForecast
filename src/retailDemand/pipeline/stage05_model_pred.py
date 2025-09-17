from src.retailDemand.components.model_pred import ModelPredictor
from src.retailDemand.config.configuration import ConfigurationManager
from src.retailDemand import logger
from src.retailDemand.entity.config_entity import ModelPredictionConfig


class ModelPredictorPipeline:
    def __init__(self):
        pass

    def main(self):
        config=ConfigurationManager()
        model_pred=ModelPredictor(config.getModelPredConfig())
        model_pred.load_models()
        model_pred.predSales(store_id=3,date="2010-02-05")  

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