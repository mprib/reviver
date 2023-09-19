import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog
from PySide6.QtCore import Slot
from reviver import USER_DIR

class CustomWidget(QWidget):
    def __init__(self):
        super().__init__()


        self.name_label = QLabel("User's Name:")
        self.name_input = QLineEdit()


        self.archive_dir_label = QLabel("Archive Location:")
        self.directory_parent = str(USER_DIR)
        self.path_label = QLabel(self.new_archive_destination)
        self.browse_button = QPushButton('Browse')
        self.launch_new_button = QPushButton("Launch New")

        self.place_widgets()
        self.connect_widgets()
        
        
    def place_widgets(self):
        self.layout = QVBoxLayout(self)
        
        self.name_containers = QHBoxLayout()
        self.name_containers.addWidget(self.name_label)        
        self.name_containers.addWidget(self.name_input)
        
        self.layout.addLayout(self.name_containers)

        self.directory_container = QHBoxLayout()
        self.directory_container.addWidget(self.archive_dir_label)
        self.directory_container.addWidget(self.path_label)
        self.directory_container.addWidget(self.browse_button)
        
        self.layout.addLayout(self.directory_container) 
   
        self.layout.addWidget(self.launch_new_button)
        
    def connect_widgets(self):
        self.name_input.textChanged.connect(self.update_path)
        self.browse_button.clicked.connect(self.browse)
        
    @Slot()
    def browse(self):
        directory = QFileDialog.getExistingDirectory(self, "Select directory to hold archive..")
        if directory:
            self.directory_parent = directory
            self.path_label.setText(self.new_archive_destination)

    @Slot()
    def update_path(self, text):
        self.path_label.setText(self.new_archive_destination)

    @property
    def new_archive_destination(self)->str:
      
        if len(self.name_input.text())>0:
            addendum =  "_reviver_archive"
        else:
            addendum = "reviver_archive"
        return str(Path(self.directory_parent, self.name_input.text() + addendum))
    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = CustomWidget()
    widget.show()

    sys.exit(app.exec())