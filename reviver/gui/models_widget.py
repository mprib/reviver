from PySide6.QtWidgets import (
    QApplication,
    QTableView,
    QWidget,
    QDialog,
    QHBoxLayout,
    QAbstractItemView,
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Signal, Qt
import sys
from dotenv import load_dotenv
from os import getenv
from pathlib import Path
from reviver.models_data import ModelSpecSheet
import reviver.log

log = reviver.log.get(__name__)


class ModelsWidget(QDialog):
    selected_model = Signal(str)

    def __init__(self, model_specs: ModelSpecSheet) -> None:
        super().__init__()

        self.item_model = QStandardItemModel()
        self.item_model.setHorizontalHeaderLabels(model_specs.in_dollars_per_1k.columns)
        for row in model_specs.in_dollars_per_1k.values:
            items = [QStandardItem(str(i)) for i in row]
            # for item in items:
            #     item.setTextAlignment(Qt.AlignHCenter) # change the alignment
            self.item_model.appendRow(items)

        self.view = QTableView()
        self.view.setModel(self.item_model)

        # make sure columns are appropriate width
        self.view.resizeColumnsToContents()

        # Set table as non-editable
        self.view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Enable row-based selection
        self.view.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Set sorting enabled
        self.view.setSortingEnabled(True)

        # Set alternating row colors
        self.view.setAlternatingRowColors(True)
        self.view.setStyleSheet(
            "alternate-background-color: #eee; background-color: #fff;"
        )

        self.place_widgets()
        self.connect_widgets()

    def showEvent(self, event):
        super().showEvent(event)

        # Calculate the total width based on the content's size and the vertical header's width
        width = (
            self.view.verticalHeader().width()
            + self.view.horizontalHeader().length()
            + self.view.frameWidth() * 2
        )

        # Calculate the total height based on the content's size and the horizontal header's height
        height = (
            self.view.horizontalHeader().height()
            + self.view.verticalHeader().sectionSize(0) * self.item_model.rowCount()
            + self.view.frameWidth() * 2
        )

        # Resize the widget based on the calculated size
        self.resize(width + 50, height + 50)

    def place_widgets(self):
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.view)

        # resize widget for contents
        self.setGeometry(self.view.geometry())

    def get_format_dict(self, model_specs_df):
        format_dict = {}
        for column in model_specs_df.columns:
            if model_specs_df.dtypes[column] == float:
                format_dict[column] = "${:,.6f}"
            elif model_specs_df.dtypes[column] == int:
                format_dict[column] = "{:,}"
        return format_dict

    def connect_widgets(self):
        self.view.doubleClicked.connect(self.emit_selected_model)
        pass

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.emit_selected_model()
 
    def emit_selected_model(self):
        index = self.view.currentIndex().row()
        model_name = self.item_model.item(index,0).text() # name in column 1
        self.selected_model.emit(model_name)
        self.close()  

if __name__ == "__main__":
    archive_dir = Path(Path.home(), "reviver")
    env_location = Path(archive_dir, ".env")
    load_dotenv(dotenv_path=env_location)
    key = getenv("OPEN_ROUTER_API_KEY")

    spec_sheet = ModelSpecSheet(key)

    app = QApplication(sys.argv)
    models_widget = ModelsWidget(spec_sheet)
    models_widget.show()

    sys.exit(app.exec())
    # %%
