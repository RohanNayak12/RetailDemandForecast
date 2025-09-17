from src.retailDemand.pipeline.stage03_model_train import ModelTrainingPipeline
from src.retailDemand.pipeline.stage04_model_eval import ModelEvaluationPipeline
from src.retailDemand.pipeline.stage01_data_injestion import DataInjestionTrainingPipeline
from src.retailDemand.pipeline.stage02_creating_model import BaseModelCreationPipeline
from src.retailDemand.pipeline.stage05_model_pred import ModelPredictorPipeline
from src.retailDemand import logger


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

STAGE_NAME= "Model Training Stage"

if __name__=="__main__":
    try:
        logger.info(f">>>>>>>> stage {STAGE_NAME} started <<<<<<<")
        obj= ModelTrainingPipeline()
        obj.main()
        logger.info(f">>>>>>>> stage {STAGE_NAME} ended <<<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e
    
STAGE_NAME= "Model Evaluation Stage"

if __name__=="__main__":
    try:
        logger.info(f">>>>>>>> stage {STAGE_NAME} started <<<<<<<")
        obj= ModelEvaluationPipeline()
        obj.main()
        logger.info(f">>>>>>>> stage {STAGE_NAME} ended <<<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e

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