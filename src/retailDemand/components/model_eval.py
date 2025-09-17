import pickle
from typing import Dict
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
from src.retailDemand import logger
from src.retailDemand.entity.config_entity import ModelEvaluationConfig


class ModelEvaluation:
    def __init__(self,config:ModelEvaluationConfig):
        self.config=config
        self.models=None
        self.forecasts={}
        self.dataset=None
        self.results={}

    def load_models(self)->dict:
        models={}
        models_path=self.config.model_path
        if not models_path.exists():
            logger.error("No model path exists")
        
        model_files=list(models_path.glob("prophet_*.pkl"))

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

    def load_dataset(self):
        df_path=self.config.dataset_path
        df=pd.read_csv(df_path)
        self.dataset=df
        logger.info("Dataset loaded for model tarining")

    def store_data_prep(self,store_id:int)->pd.DataFrame:
        store_data=self.dataset[self.dataset[self.config.store_column]==store_id]

        store_data=store_data[[self.config.date_column,self.config.target_column]]
        store_data=store_data.groupby(self.config.date_column).sum()
        store_data.reset_index(inplace=True)
        store_data.columns=['ds','y']
        logger.info(f"Data prepared for store {store_id}")
        return store_data
    
    def predictStore(self,store_id:int)-> pd.DataFrame:
        model=self.models[store_id]

        future=model.make_future_dataframe(
            periods=self.config.forecast_periods,
            freq=self.config.frequency
        )
        forecast=model.predict(future)
        self.forecasts[store_id]=forecast

        logger.info(f"Forecasts generated for store {store_id}")
        return forecast
    
    def modelEval(self,store_id:int)->Dict[str,float]:
        store_data=self.store_data_prep(store_id)
        testData=store_data.iloc[self.config.train_split:]
        
        if store_id not in self.forecasts:
            raise ValueError(f"No store found for id= {store_id}")
        
        forecast=self.forecasts[store_id]
        y_pred=forecast['yhat'].tail(len(testData)).values
        y_true=testData['y'].values

        mape=mean_absolute_percentage_error(y_true=y_true,y_pred=y_pred)*100
        mae=mean_absolute_error(y_true,y_pred)

        metrics = {
            'MAPE': round(mape, 4),
            'MAE': round(mae, 4)
        }

        self.results[store_id] = metrics
        logger.info(f"Evaluation completed for store {store_id}: MAPE={mape:.2f}%")

        return metrics
    
    def evalAll(self):
        stores=self.dataset[self.config.store_column].unique()
        
        logger.info(f"Starting training {len(stores)} stores")

        for store_id in stores:
            self.predictStore(store_id)
            self.modelEval(store_id)

    def save_evaluation_results(self):
        if not self.results:
            logger.warning("No results to save")
            return
        
        results_df = pd.DataFrame.from_dict(self.results, orient='index')
        results_df.reset_index(inplace=True)
        results_df.columns = ['Store', 'MAPE', 'MAE']
        
        results_path = self.config.evaluation_results_path
        results_path.parent.mkdir(parents=True, exist_ok=True)
        results_df.to_csv(results_path, index=False)
        
        logger.info(f"Evaluation Results Summary:")
        logger.info(f"  Average MAPE: {results_df['MAPE'].mean():.2f}%")
        logger.info(f"  Median MAPE: {results_df['MAPE'].median():.2f}%")
        logger.info(f"  Best MAPE: {results_df['MAPE'].min():.2f}% (Store {results_df.loc[results_df['MAPE'].idxmin(), 'Store']})")
        logger.info(f"  Results saved to: {results_path}")
        
        return results_df
