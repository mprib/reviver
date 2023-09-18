
# %%
import requests
import re
import reviver.log
logger = reviver.log.get(__name__)
import polars as pl

from keys import OPEN_ROUTER_API_KEY
import json

headers = {
    'Authorization': f'Bearer {OPEN_ROUTER_API_KEY}',
}

response = requests.get('https://openrouter.ai/api/v1/auth/key', headers=headers)

# to view the response content
print(response.content)

key_data = response.content.decode() # comes in as a byte string
key_data = json.loads(key_data)

original_key_limit = key_data["data"]["limit"]
key_usage = key_data["data"]["usage"]
limit_remaining = key_data["data"]["limit_remaining"]

logger.info(f"Key Limit: {original_key_limit}")
logger.info(f"Key Usage: {key_usage}")
logger.info(f"Remaining Limit: {limit_remaining}")

response = requests.get('https://openrouter.ai/api/v1/models', headers=headers)
raw_model_specs = response.content.decode()
raw_model_specs = json.loads(raw_model_specs)["data"]
logger.info(f"Model specs: {raw_model_specs}")

# %%
# here model is a single dictionary 
# need to flatten the model description data. Long term considering placing this in a database

def flatten_dict(data:dict)->dict:
    """
    data: a dictionary with nested dictionaries for some values

    new keys are added which concatenate key_subkey:subvalue
    so that dictionary be converted to dataframe

    note that key names may become quite long
    """
    
    data_copy = data.copy() #can't change data while iterating over it
    for key,value in data_copy.items():
        # merge nested dictionaries  
        if type(value) == dict:
            for subkey, subvalue in value.items():
                data[key + "_" +subkey] = subvalue
            del data[key]

    return data

def convert_numeric_in_dict(data:dict)-> dict:
    # note that this is checking for scientific notation as well as 
    # basic integers and decimals
    numeric_pattern = re.compile(r'^-?[0-9]+\.?[0-9]*([eE][-+]?[0-9]+)?$')

    for key, value in data.items():
        if isinstance(value, str) and numeric_pattern.match(value):
            # Try converting to int, if not possible, convert to float
            try:
                data[key] = int(value)
            except ValueError:
                data[key] = float(value)
    return data

def get_all_keys(all_dicts:list[dict])->list[str]:
    
    keys = []
    for d in all_dicts:
        for key, value in d.items():
            keys.append(key)
        
    keys = list(set(keys))
    return keys

#%%
flat_model_specs = []
for model_specs in raw_model_specs:
    model_specs = flatten_dict(model_specs)
    model_specs = convert_numeric_in_dict(model_specs)
    
    flat_model_specs.append(model_specs)
    
merged_model_specs = {key:[] for key in get_all_keys(flat_model_specs)}

#%% 
for key in merged_model_specs.keys():
    for model_specs in flat_model_specs:
        if key in model_specs.keys():
            value = model_specs[key]
            merged_model_specs[key].append(value)
        else:
            merged_model_specs[key].append(None)


model_specs_reference = pl.DataFrame(merged_model_specs)
# %%
