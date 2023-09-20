from reviver.open_router_query_handler import OpenRouterQueryHandler
from dataclasses import dataclass
import math
import reviver.log
import pandas as pd
log = reviver.log.get(__name__)


@dataclass
class ModelSpecSheet:
    api_key:str

    def __post_init__(self):
        
        # while i'm not terribly happy with creating an object within another
        # this is a slightly cleaner way of managing this.        

        query_handler = OpenRouterQueryHandler(self.api_key)
        
        self.raw_data = query_handler.get_model_specs()
        self.models = {}
        for index, row in self.raw_data.iterrows():
            self.models[row["id"]] = ModelSpecs(name=row["id"],
                                          _context_length = row["context_length"],
                                          pricing_completion=row["pricing_completion"],
                                          pricing_prompt = row["pricing_prompt"],
                                          _pricing_discount = row["pricing_discount"]
                                          )
    
    
    @property
    def in_dollars_per_1k(self)->pd.DataFrame:
        # going to construct         

        dollars_per_1k = {"Name":[],
                          "Prompt cost\n(per 1k tokens)":[],
                          "Completion cost\n(per 1k tokens)":[],
                          "Context\n(tokens)":[]}
    
        for name, model in self.models.items():
            dollars_per_1k["Name"].append(name)
            dollars_per_1k["Prompt cost\n(per 1k tokens)"].append(model.prompt_cost_dollars_per_1k)
            dollars_per_1k["Completion cost\n(per 1k tokens)"].append(model.completion_cost_dollars_per_1k)
            dollars_per_1k["Context\n(tokens)"].append(model.context_length) 

        return pd.DataFrame(dollars_per_1k)
   
    @property
    def dollars_per_1k_format(self)->dict:
        
        format = {"Name":"{}",
                  "Prompt cost\n(per 1k tokens)":"${:,.6f}",
                  "Completion cost\n(per 1k tokens)":"${:,.6f}",
                  "Context\n(tokens)":"{:,}",}
        
        return format 
           
    @property
    def in_tokens_per_dollar()->pd.DataFrame:
        pass
@dataclass   
class ModelSpecs:
    name:str
    _context_length:int 
    pricing_completion:float
    pricing_prompt:float
    _pricing_discount:float
    
    @property
    def pricing_discount(self):
        if math.isnan(self._pricing_discount):
            return 0
    
        else:
            return self._pricing_discount
             
    @property
    def completion_cost_dollars_per_1k(self):
        value = round(self.pricing_completion*(1-self.pricing_discount)*1000,6)
        return "${:,.6f}".format(value)
    
    @property
    def prompt_cost_dollars_per_1k(self):
        value = round(self.pricing_prompt*(1-self.pricing_discount) *1000, 6)
        return "${:,.6f}".format(value)
    
    @property
    def context_length(self):
        
        return "{:,}".format(self._context_length)
