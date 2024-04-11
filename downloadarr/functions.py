import os
import yaml
import re
from pathlib import Path
import datetime

def check_file_existence(file_path):
    if not os.path.exists(file_path):
        return False
    else:
        return True

def load_config(file_path):
    if check_file_existence(file_path):
        print("Loading config ...")
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    else:
        print("Config file does not exist: " + file_path)
        return None

def string_cleaner(input_string):
    if isinstance(input_string, str):
        raw_string = re.sub(r'[\/:*?"<>|]', " ", input_string)
        raw_string = raw_string.replace(".","")
        temp_string = re.sub(r"\s+", " ", raw_string)
        cleaned_string = temp_string.strip()
        return cleaned_string

