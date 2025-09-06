import os
from box.exceptions import BoxValueError
from box import ConfigBox
from ensure import ensure_annotations
import yaml
from retailDemand import logger
import json
import joblib
from pathlib import Path
from typing import Any
import base64

@ensure_annotations
def read_yaml(path:Path)-> ConfigBox:
    try:
        with open(path) as yamlFile:
            content=yaml.safe_load(yamlFile)
            logger.info(f"yaml file: {path} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("Empty yaml")
    except Exception as e:
        raise e

@ensure_annotations
def createDir(path:list,verbose=True):
    for p in path:
        os.makedirs(path,exist_ok=True)
        if verbose:
            logger.info(f"Created directory at: {p}")

@ensure_annotations
def saveJson(path:Path,data:dict):
    with open(path,"w") as f:
        json.dump(data,f,indent=4)
    logger.info(f"json saved at{path}")

@ensure_annotations
def loadJson(path:Path)->ConfigBox:
    with open(path) as f:
        content=json.load(f)
    logger.info(f"json file loaded: {path}")
    return ConfigBox(content)

@ensure_annotations
def saveBin(data:Any,path:Path):
    joblib.dump(value=data,filename=path)
    logger.info(f"Binary file saved at {path}")