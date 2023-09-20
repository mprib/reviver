from reviver.open_router_query_handler import OpenRouterQueryHandler
from dataclasses import dataclass
import reviver.log
import pandas as pd
log = reviver.log.get(__name__)


@dataclass
class ModelsData:
    raw_data:pd.DataFrame

    def __post_init__(self):
        self.models = {}
        for index, row in self.raw_data.iterrows():
            self.models[row["id"]] = ModelData(name=row["id"],
                                          context_length = row["context_length"],
                                          pricing_completion=row["pricing_completion"],
                                          pricing_prompt = row["pricing_prompt"],
                                          pricing_discount = row["pricing_discount"]
                                          )

@dataclass   
class ModelData:
    name:str
    context_length:int 
    pricing_completion:float
    pricing_prompt:float
    pricing_discount:float
    
    @property
    def completion_cost_dollars_per_1k(self):
        return self.pricing_completion *1000
    
    @property
    def completion_cost_tokens_per_dollar(self):
        return (1/self.pricing_completion)
        

    @property
    def prompt_cost_dollars_per_1k(self):
        return self.pricing_prompt *1000
    
    @property
    def prompt_cost_tokens_per_dollar(self):
        return (1/self.pricing_prompt)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QTableView
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QStandardItemModel, QStandardItem
    import pandas as pd
    from io import StringIO
    import sys
    from dotenv import load_dotenv
    from os import getenv
    from pathlib import Path

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
    app = QApplication(sys.argv)

    model = QStandardItemModel()

    model.setHorizontalHeaderLabels(model_specs.columns)
    for row in model_specs.values:
        items = [QStandardItem(str(i)) for i in row]
        model.appendRow(items)

    view = QTableView()
    view.setModel(model)
    view.show()

    sys.exit(app.exec())
# %%