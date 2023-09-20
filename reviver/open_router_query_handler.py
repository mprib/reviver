#%%
import requests
import re
from dotenv import load_dotenv
import reviver.log
import pandas as pd
from os import getenv
import json
from pathlib import Path
log = reviver.log.get(__name__)

class OpenRouterQueryHandler:
    def __init__(self, API_KEY:str) -> None:
        self.headers = {
            "Authorization": f"Bearer {API_KEY}",
        }

    def get_key_usage(self)->dict:
        response = requests.get(
            "https://openrouter.ai/api/v1/auth/key", headers=self.headers
        )
        key_data = response.content.decode()  # comes in as a byte string
        key_data = json.loads(key_data)["data"] # dict nested under key "data"

        del key_data['label'] # don't pass around key data to *anyone*
        original_key_limit = key_data["limit"]
        key_usage = key_data["usage"]
        limit_remaining = key_data["limit_remaining"]

        log.info(f"Key Limit: {original_key_limit}")
        log.info(f"Key Usage: {key_usage}")
        log.info(f"Remaining Limit: {limit_remaining}")

        return key_data

    def get_model_specs(self)->pd.DataFrame:
        response = requests.get(
            "https://openrouter.ai/api/v1/models", headers=self.headers
        )
        raw_model_specs = response.content.decode()
        raw_model_specs = json.loads(raw_model_specs)["data"]

        flat_model_specs = []
        for model_specs in raw_model_specs:
            model_specs = flatten_dict(model_specs)
            model_specs = convert_numeric_in_dict(model_specs)

            flat_model_specs.append(model_specs)

        merged_model_specs = {key: [] for key in get_all_keys(flat_model_specs)}

        for key in merged_model_specs.keys():
            for model_specs in flat_model_specs:
                if key in model_specs.keys():
                    value = model_specs[key]
                    merged_model_specs[key].append(value)
                else:
                    merged_model_specs[key].append(None)


        model_specs_reference = pd.DataFrame(merged_model_specs)
        return model_specs_reference


def flatten_dict(data: dict) -> dict:
    """
    data: a dictionary with nested dictionaries for some values

    new keys are added which concatenate key_subkey:subvalue
    so that dictionary be converted to dataframe

    note that key names may become quite long
    """

    data_copy = data.copy()  # can't change data while iterating over it
    for key, value in data_copy.items():
        # merge nested dictionaries
        if type(value) == dict:
            for subkey, subvalue in value.items():
                data[key + "_" + subkey] = subvalue
            del data[key]

    return data


def convert_numeric_in_dict(data: dict) -> dict:
    # note that this is checking for scientific notation as well as
    # basic integers and decimals
    numeric_pattern = re.compile(r"^-?[0-9]+\.?[0-9]*([eE][-+]?[0-9]+)?$")

    for key, value in data.items():
        if isinstance(value, str) and numeric_pattern.match(value):
            # Try converting to int, if not possible, convert to float
            try:
                data[key] = int(value)
            except ValueError:
                data[key] = float(value)
    return data


def get_all_keys(all_dicts: list[dict]) -> list[str]:
    keys = []
    for d in all_dicts:
        for key, value in d.items():
            keys.append(key)

    keys = list(set(keys))
    return keys



if __name__ == "__main__":
    
    archive_dir = Path(Path.home(), "reviver")
    env_location = Path(archive_dir,".env")
    load_dotenv(dotenv_path=env_location)
    key = getenv("OPEN_ROUTER_API_KEY")

    query_handler = OpenRouterQueryHandler(key)
    
    key_usage = query_handler.get_key_usage()
    
    print(key_usage)
    model_specs =  query_handler.get_model_specs()

    log.info(model_specs.to_csv())
    model_specs

