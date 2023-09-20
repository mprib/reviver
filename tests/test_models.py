
#%%

from reviver.models_data import ModelSpecSheet
from dotenv import load_dotenv
from reviver import ROOT
from pathlib import Path
import os
import reviver.log

log = reviver.log.get(__name__)

from reviver.open_router_query_handler import OpenRouterQueryHandler

def test_models():
    
    # make sure API keys are set in the environment
    env_loc = Path(ROOT, ".env")
    load_dotenv(env_loc)
    open_router_api = os.getenv("OPEN_ROUTER_API_KEY")
    

    all_model_specs = ModelSpecSheet(open_router_api)

    log.info(all_model_specs.raw_data)

    # just running some very basic assertions to make sure data got pulled down correctly
    for name, model in all_model_specs.models.items():
        assert(model._context_length > 0)
        assert(model.pricing_completion > 0) 
        assert(model.pricing_prompt > 0) 

if __name__=="__main__":
    test_models()
# %%
