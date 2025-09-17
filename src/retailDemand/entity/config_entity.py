from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataInjestionConfig:
    root_dir:Path
    source_url:str
    local_data_file:Path
    unzip_dir:Path
    final_dataset_dir:Path

@dataclass(frozen=True)
class PrepareBaseModelConfig:
    root_dir:Path
    base_model_path:Path
    seasonality_mode:str
    daily_seasonality:bool
    weekly_seasonality:bool
    yearly_seasonality:bool

@dataclass(frozen=True)
class ModelTrainingConfig:
  root_dir: Path
  trained_model_path: Path
  dataset_path: Path
  base_model_path:Path
  store_column:str='Store'
  date_column: str = 'Date'
  target_column: str = 'Weekly_Sales_x'
  train_split: int = 120

@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    evaluation_results_path: Path
    dataset_path: Path
    model_path: Path
    train_split: int = 120
    forecast_periods: int = 23
    frequency: str='W-Fri'
    store_column:str='Store'
    date_column: str = 'Date'
    target_column: str = 'Weekly_Sales_x'

@dataclass
class ModelPredictionConfig:
    root_dir: Path
    dataset_path: Path
    model_path: Path
    
