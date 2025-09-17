from src.retailDemand.components.model_eval import ModelEvaluation
from src.retailDemand.config.configuration import ConfigurationManager
from src.retailDemand import logger
from src.retailDemand.entity.config_entity import ModelEvaluationConfig


class ModelEvaluationPipeline:
    def __init__(self):
        pass

    def main(self):
        config=ConfigurationManager()
        model_eval=ModelEvaluation(config.getModelEvaluationConfig())
        model_eval.load_models()
        model_eval.load_dataset()
        model_eval.evalAll()
        model_eval.save_evaluation_results()
        model_eval.track_mlflow()

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