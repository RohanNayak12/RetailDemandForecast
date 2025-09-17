import pickle
from typing import Any, Dict

import pandas as pd
from src.retailDemand import logger
from src.retailDemand.entity.config_entity import ModelPredictionConfig


class ModelPredictor:
    def __init__(self,config:ModelPredictionConfig):
        self.config=config
        self.models={}

    def load_models(self)->dict:
        models={}
        model_path=self.config.model_path
        if not model_path.exists():
            logger.error("No model path exists")
        
        model_files=list(model_path.glob("prophet_*.pkl"))

        if not model_files:
            logger.warning("No models found")
        logger.info(f"Found {len(model_files)} models")

        for model_file in model_files:
            file=model_file.stem
            store=int(file.split("_")[1])
            with open(model_file,'rb') as f:
                model=pickle.load(f)
            models[store]=model
            logger.info(f"Model loaded for store {store}")
        self.models=models

    def predSales(self,store_id:int,date:str)->Dict[str,Any]:
        if store_id not in self.models:
            raise ValueError(f"Model for store {store_id} not found.")
        
        model=self.models[store_id]
        future=pd.DataFrame({'ds':[pd.to_datetime(date)]})
        forecast=model.predict(future)

        res={
            "store_id":store_id,
            "prediction_date":date,
            "predicted_sales":round(forecast['yhat'].iloc[0],2),
            'lower_bound': round(forecast['yhat_lower'].iloc[0], 2),
            'upper_bound': round(forecast['yhat_upper'].iloc[0], 2)
        }

        logger.info(f"prediction for store {store_id} on {date} is ${res['predicted_sales']:,.2f}")
        return res