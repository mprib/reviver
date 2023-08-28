#%%
import requests
import reviver.logger
logger = reviver.logger.get(__name__)
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
model_data = response.content.decode()
model_data = json.loads(model_data)
logger.info(f"Model data: {model_data}")

# %%
# need to flatten the model description data. Long term considering placing this in a database
# here model is a single dictionary 
for model  in model_data["data"]:
    for key,value in model.copy().items():
        # merge nested dictionaries  
        if type(value) == dict:
            for subkey, subvalue in value.items():
                model[key + "_" +subkey] = subvalue
            del model[key]
# %%
# combine all items together
model_overview = None
for model in model_data["data"]:
    if model_overview is None:
        model_overview = pl.DataFrame(model)
                                      
    else:
        model_overview = pl.concat([model_overview, pl.DataFrame(model)])
        

    
# %%
