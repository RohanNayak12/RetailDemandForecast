from src.retailDemand import logger
from src.retailDemand.pipeline.stage01_data_injestion import DataInjestionTrainingPipeline

STAGE_NAME= "Data Injestion Stage"

if __name__=="__main__":
    try:
        logger.info(f">>>>>>>> stage {STAGE_NAME} started <<<<<<<")
        obj= DataInjestionTrainingPipeline()
        obj.main()
        logger.info(f">>>>>>>> stage {STAGE_NAME} ended <<<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e