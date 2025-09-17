import os
from pathlib import Path
import zipfile
import gdown
from src.retailDemand.entity.config_entity import DataInjestionConfig
from src.retailDemand import logger
import pandas as pd

class DataInjestion:
    def __init__(self,config:DataInjestionConfig):
        self.config=config
    
    def download_file(self):
        try:
            dataset_url=self.config.source_url
            zip_download_dir=self.config.local_data_file
            os.makedirs("artifacts/data_injestion",exist_ok=True)
            logger.info(f"Downloading data from {dataset_url} into {zip_download_dir}")

            file_id=dataset_url.split("/")[-2]
            prefix="https://drive.google.com/uc?/export=download&id="
            gdown.download(prefix+file_id,zip_download_dir)
            logger.info(f"Downloaded data from {dataset_url} to {zip_download_dir}")

        except Exception as e:
            raise e
        
    def extract_zip_file(self)->Path:
        unzip_path=self.config.unzip_dir
        os.makedirs(unzip_path,exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file,'r') as zip_ref:
            zip_ref.extractall(unzip_path)
            folders = {name.split('/')[0] for name in zip_ref.namelist() if '/' in name}
            logger.info(list(folders)[0])
            logger.info(zip_ref)
        fname=list(folders)[0]
        logger.info(f"Final unzip path: {Path(unzip_path)/fname}")
        return Path(unzip_path)/fname
    
    def dataPrep(self)->pd.DataFrame:
        try:
            final_dir_path=self.extract_zip_file()
            fPath=final_dir_path/"features.csv"
            tPath=final_dir_path/"train.csv"
            sPath=final_dir_path/"stores.csv"

            logger.info("Loading csv files for merging")
            df1=pd.read_csv(tPath)
            df2=pd.read_csv(fPath)
            df3=pd.read_csv(sPath)

            temp_data=df1.merge(df2,on=['Store','Date','IsHoliday'],how='inner')
            final_data=temp_data.merge(df3,on=['Store'],how='inner')

            final_data['Date']=pd.to_datetime(final_data['Date'])

            final_data['Year']=final_data['Date'].dt.year
            final_data['Month']=final_data['Date'].dt.month
            final_data['Week']=final_data['Date'].dt.isocalendar().week
            final_data['Day_Name']=final_data['Date'].dt.day_name
            final_data['Month_Name']=final_data['Date'].dt.month_name

            if 'Weekly_Sales' in final_data.columns and 'Weekly_Sales_x' not in final_data.columns:
                final_data['Weekly_Sales_x'] = final_data['Weekly_Sales']

            logger.info(f"Final merged data shape: {final_data.shape}")
            logger.info(f"Columns: {list(final_data.columns)}")

            return final_data
        except Exception as e:
            logger.error(f"Error loading and merging data: {str(e)}")
            raise

    def save_data(self,name:str="final_data.csv")->Path:
        final_data=self.dataPrep()
        save_dir=self.config.final_dataset_dir
        save_path=Path(save_dir)/name

        final_data.to_csv(save_path,index=False)
        logger.info(f"Final data saved to: {save_path}")
        # logger.info(f"Saved data shape: {self.data.shape}")
        logger.info(f"Ready for model training")

        return save_path