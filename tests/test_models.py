
#%%

from reviver.models_data import ModelsData
from dotenv import load_dotenv
from reviver import ROOT
from pathlib import Path
import os
import reviver.log

log = reviver.log.get(__name__)

from reviver.open_router_query_handler import OpenRouterQueryHandler

def test_models():
    
    env_loc = Path(ROOT, ".env")
    load_dotenv(env_loc)

    open_router_api = os.getenv("OPEN_ROUTER_API_KEY")
    query_handler = OpenRouterQueryHandler(open_router_api)

    raw_data = query_handler.get_model_specs()
    models_data = ModelsData(raw_data=raw_data)

    

    log.info(models_data.raw_data)
    
if __name__=="__main__":
    test_models()
# %%
