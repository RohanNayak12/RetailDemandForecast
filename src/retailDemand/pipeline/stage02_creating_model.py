from src.retailDemand.components.base_model_creation import BaseModelPrep
from src.retailDemand.config.configuration import ConfigurationManager
from src.retailDemand import logger


class BaseModelCreationPipeline:
    def __init__(self):
        pass

    def main(self):
        config=ConfigurationManager()
        base_model_prep=BaseModelPrep(config.getPrepareBaseModelConfig())
        base_model_prep.save_base_model()

STAGE_NAME= "Base Model Preparation Stage"

if __name__=="__main__":
    try:
        logger.info(f">>>>>>>> stage {STAGE_NAME} started <<<<<<<")
        obj= BaseModelCreationPipeline()
        obj.main()
        logger.info(f">>>>>>>> stage {STAGE_NAME} ended <<<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e