from pathlib import Path
import pickle
import pandas as pd
from src.retailDemand.entity.config_entity import ModelTrainingConfig
from src.retailDemand import logger
from prophet import Prophet

class ModelTrain:
    def __init__(self,config:ModelTrainingConfig):
        self.config=config
        self.dataset=None
        self.models={}
        self.base_params=None
    
    def load_dataset(self):
        df_path=self.config.dataset_path
        df=pd.read_csv(df_path)
        self.dataset=df
        logger.info("Dataset loaded for model tarining")

    def load_base_model_params(self):
        if self.base_params is not None:
            return self.base_params

        base_model_path=self.config.base_model_path

        if not Path(base_model_path).exists():
            raise FileNotFoundError(f"No base model at {base_model_path}")
        
        with open(base_model_path,'rb') as f:
            base_model=pickle.load(f)
        logger.info("Base model loaded successfully")
    
        # Debug: Log base model attributes
        logger.info(f"Base model type: {type(base_model)}")

        self.base_params = {
        'growth': str(getattr(base_model, 'growth', 'linear')),
        'seasonality_mode': str(getattr(base_model, 'seasonality_mode', 'multiplicative')),
        'daily_seasonality': bool(getattr(base_model, 'daily_seasonality', False)),
        'weekly_seasonality': bool(getattr(base_model, 'weekly_seasonality', True)),
        'yearly_seasonality': bool(getattr(base_model, 'yearly_seasonality', True)),
        'changepoint_prior_scale': float(getattr(base_model, 'changepoint_prior_scale', 0.05)),
        'seasonality_prior_scale': float(getattr(base_model, 'seasonality_prior_scale', 10.0)),
        'holidays_prior_scale': float(getattr(base_model, 'holidays_prior_scale', 10.0)),
        'interval_width': float(getattr(base_model, 'interval_width', 0.80)),
        'mcmc_samples': int(getattr(base_model, 'mcmc_samples', 0)),
        'uncertainty_samples': int(getattr(base_model, 'uncertainty_samples', 1000))
    }
        if self.base_params['seasonality_mode'] not in ['additive', 'multiplicative']:
            logger.warning(f"Invalid seasonality_mode: {self.base_params['seasonality_mode']}, using 'multiplicative'")
            self.base_params['seasonality_mode'] = 'multiplicative'
        
        logger.info("Extracted base model parameters:")
        for key, value in self.base_params.items():
            logger.info(f"  {key} ({type(value).__name__}): {value}")
    
    def create_new_model_instance(self)->Prophet:
        self.load_base_model_params()
        model=Prophet(**self.base_params)
        logger.info(f"Created base model's new instance")
        return model

    def store_data_prep(self,store_id:int)->pd.DataFrame:
        store_data=self.dataset[self.dataset[self.config.store_column]==store_id]

        store_data=store_data[[self.config.date_column,self.config.target_column]]
        store_data=store_data.groupby(self.config.date_column).sum()
        store_data.reset_index(inplace=True)
        store_data.columns=['ds','y']
        logger.info(f"Data prepared for store {store_id}")
        return store_data
    
    def train_store(self,store_id:int)->Prophet:
        logger.info(f"Started training for store {store_id}")
        data=self.store_data_prep(store_id=store_id)
        train_data=data.iloc[:self.config.train_split]
        model=self.create_new_model_instance()
        model.fit(train_data)
        self.models[store_id]=model
        logger.info(f"Model trained for store {store_id}")
        return model
    
    def trainAll(self):
        stores=self.dataset[self.config.store_column].unique()
        logger.info(f"Starting model training for {len(stores)} stores")

        for store_id in stores:
            #store_data=self.store_data_prep(store_id)
            self.train_store(store_id)
            logger.info(f"Model trained for store {store_id}")
    
    def save_models(self):
        save_dir = Path(self.config.trained_model_path)
        save_dir.mkdir(parents=True, exist_ok=True)
        for store_id,model in self.models.items():
            model_path=self.config.trained_model_path/f"prophet_{store_id}.pkl"
            with open(model_path,'wb') as f:
                pickle.dump(model,f)
            logger.info(f"model saved for store {store_id} at {model_path}")