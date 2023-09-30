from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QDialog,
    QDialogButtonBox,
)
from dotenv import load_dotenv, set_key
from os import getenv, path
from pathlib import Path
import sys


class ApiKeyWidget(QWidget):
    def __init__(self, env_location: Path):
        super().__init__()
        self.env_location = env_location
        self.env_path_label = QLabel(f"Keys stored in: {env_location}")
        self.open_router_api_key_label = QLabel(
            "Open Router API Key: " + self.anonymize_key(getenv("OPEN_ROUTER_API_KEY"))
        )
        self.set_open_router_api_button = QPushButton("Set API Key")

        self.open_ai_api_key_label = QLabel(
            "Open AI API Key: " + self.anonymize_key(getenv("OPEN_AI_API_KEY"))
        )
        self.set_open_ai_api_button = QPushButton("Set API Key")

        self.place_widgets()
        self.connect_widgets()

    def place_widgets(self):
        self.layout = QGridLayout()
        self.layout.addWidget(self.env_path_label, 0, 0, 1, 3)
        self.layout.addWidget(self.open_router_api_key_label, 1, 0)
        self.layout.addWidget(self.set_open_router_api_button, 1, 2)
        self.layout.addWidget(self.open_ai_api_key_label, 2, 0)
        self.layout.addWidget(self.set_open_ai_api_button, 2, 2)
        self.setLayout(self.layout)

    def connect_widgets(self):
        self.set_open_router_api_button.clicked.connect(
            self.on_set_open_router_button_clicked
        )
        self.set_open_ai_api_button.clicked.connect(self.on_set_open_ai_button_clicked)

    def anonymize_key(self, key):
        if key:
            return key[0:2] + "*" * (len(key) - 6) + key[-2:]
        else:
            return "Not Set"

    def on_set_open_router_button_clicked(self):
        dialog = ApiEntryDialog()

        if dialog.exec():
            new_key = dialog.key_entry.text()
            set_key(self.env_location, "OPEN_ROUTER_API_KEY", new_key)
            self.open_router_api_key_label.setText(
                "Open Router API Key: " + self.anonymize_key(new_key)
            )

    def on_set_open_ai_button_clicked(self):
        dialog = ApiEntryDialog()

        if dialog.exec():
            new_key = dialog.key_entry.text()
            set_key(self.env_location, "OPEN_AI_API_KEY", new_key)
            self.open_ai_api_key_label.setText(
                "Open AI API Key: " + self.anonymize_key(new_key)
            )


class ApiEntryDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Set API Key")

        dialog_layout = QVBoxLayout(self)

        dialog_layout.addWidget(QLabel("Enter API Key:"))

        self.key_entry = QLineEdit()
        dialog_layout.addWidget(self.key_entry)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        dialog_layout.addWidget(button_box)


if __name__ == "__main__":
    archive_dir = Path(Path.home(), "reviver")
    env_location = Path(archive_dir, ".env")
    load_dotenv(dotenv_path=env_location)

    app = QApplication(sys.argv)

    widget = ApiKeyWidget(env_location)
    widget.show()

    sys.exit(app.exec())
