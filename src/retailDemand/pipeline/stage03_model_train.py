from src.retailDemand.components.model_train import ModelTrain
from src.retailDemand.config.configuration import ConfigurationManager
from src.retailDemand import logger


class ModelTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config=ConfigurationManager()
        train_model=ModelTrain(config.getModelTrainingConfig())
        train_model.load_dataset()
        train_model.trainAll()
        train_model.save_models()

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