from typing import Optional
from PySide6.QtWidgets import QApplication, QTableView, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
import pandas as pd
from io import StringIO
import sys
from dotenv import load_dotenv
from os import getenv
from pathlib import Path
from reviver.models_data import ModelsData

class ModelsWidget(QWidget):
    
    def __init__(self, models_data:ModelsData)->None:
        super().__init__()





if __name__ == "__main__":
    archive_dir = Path(Path.home(), "reviver")
    env_location = Path(archive_dir,".env")
    load_dotenv(dotenv_path=env_location)
    key = getenv("OPEN_ROUTER_API_KEY")

    query_handler = OpenRouterQueryHandler(key)

    key_usage = query_handler.get_key_usage()

    print(key_usage)
    model_specs =  query_handler.get_model_specs()


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
