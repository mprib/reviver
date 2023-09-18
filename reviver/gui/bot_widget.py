from PySide6.QtWidgets import QApplication, QDialog,  QPushButton, QWidget, QFormLayout, QLineEdit, QTextEdit, QCheckBox, QSlider, QVBoxLayout, QHBoxLayout, QDoubleSpinBox, QSpinBox
from PySide6.QtCore import Qt
from reviver.bot import Bot
import reviver.log
log = reviver.log.get(__name__)

class BotWidget(QWidget):
    def __init__(self, bot: Bot, parent=None):
        super(BotWidget, self).__init__(parent)
        self.bot = bot
        # Create widgets for each parameter of the Bot class
        self.name_widget = QLineEdit()
        self.model_widget = QLineEdit()
        self.hidden_widget = QCheckBox()

        # System prompt will have option to expand
        self.system_prompt_container = QVBoxLayout()
        self.system_prompt_widget = QTextEdit()
        self.expand_button = QPushButton("Expand")
        self.system_prompt_container.addWidget(self.system_prompt_widget)
        self.system_prompt_container.addWidget(self.expand_button)

        self.max_tokens_widget = self.create_slider_spinbox_pair(1, 1000, 1)
        self.temperature_widget = self.create_slider_spinbox_pair(0, 2,.05)
        self.top_p_widget = self.create_slider_spinbox_pair(0, 1,.05)
        self.frequency_penalty_widget = self.create_slider_spinbox_pair(0, 2,.05)
        self.presence_penalty_widget = self.create_slider_spinbox_pair(0, 2,.05)

        # Add Save and Cancel buttons
        self.save_button = QPushButton("Save Changes")
        self.cancel_button = QPushButton("Cancel Changes")

        self.place_widgets()
        self.connect_widgets()
        self.load_bot()


    def connect_widgets(self):
        self.expand_button.clicked.connect(self.expand_system_prompt)
        self.save_button.clicked.connect(self.update_bot)
        self.cancel_button.clicked.connect(self.load_bot) # revert the form to what it was (the current bot state)

    def place_widgets(self):
        self.setLayout(QVBoxLayout())
        # Initialize form layout
        self.form = QFormLayout()

        # Add widgets to form layout
        self.form.addRow("name", self.name_widget)
        self.form.addRow("model", self.model_widget)
        self.form.addRow("hidden", self.hidden_widget)
        self.form.addRow("system_prompt", self.system_prompt_container)
        self.form.addRow("max_tokens", self.max_tokens_widget)
        self.form.addRow("temperature", self.temperature_widget)
        self.form.addRow("top_p", self.top_p_widget)
        self.form.addRow("frequency_penalty", self.frequency_penalty_widget)
        self.form.addRow("presence_penalty", self.presence_penalty_widget)

        self.layout().addLayout(self.form)
        
        self.controls = QHBoxLayout()
        self.controls.addWidget(self.cancel_button)
        self.controls.addWidget(self.save_button)

        self.layout().addLayout(self.controls)

    def create_slider_spinbox_pair(self, min_value, max_value, step_size):

        multiplier = 100  # for two decimal points precision

        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min_value * multiplier)
        slider.setMaximum(max_value * multiplier)
        slider.setSingleStep(step_size * multiplier)
        slider.setValue(min_value * multiplier)


        if step_size ==1:
            spinbox = QSpinBox()
        else:
            spinbox = QDoubleSpinBox()

        spinbox.setMinimum(min_value)
        spinbox.setMaximum(max_value)
        spinbox.setSingleStep(step_size)
        spinbox.setValue(min_value)

        slider.valueChanged.connect(lambda value: spinbox.setValue(value / multiplier))
        spinbox.valueChanged.connect(lambda value: slider.setValue(value * multiplier))
        # spinbox.valueChanged.connect(slot)

        container = QHBoxLayout()
        container.addWidget(slider)
        container.addWidget(spinbox)

        return container


    def load_bot(self):
        def set_slider_spinbox_value(layout, value):
            # Slider is the first child in the layout
            slider = layout.itemAt(0).widget()
            slider.setValue(value)
        
            # SpinBox is the second child in the layout
            spinbox = layout.itemAt(1).widget()
            spinbox.setValue(value)

        self.name_widget.setText(self.bot.name)
        self.model_widget.setText(self.bot.model)
        self.hidden_widget.setChecked(self.bot.hidden)
        self.system_prompt_widget.setText(self.bot.system_prompt)
        
        set_slider_spinbox_value(self.max_tokens_widget, self.bot.max_tokens)
        set_slider_spinbox_value(self.temperature_widget, self.bot.temperature)
        set_slider_spinbox_value(self.top_p_widget, self.bot.top_p)
        set_slider_spinbox_value(self.frequency_penalty_widget, self.bot.frequency_penalty)
        set_slider_spinbox_value(self.presence_penalty_widget, self.bot.presence_penalty)



    def update_bot(self):
        def get_slider_spinbox_value(layout):
            # Slider is the first child in the layout
            spinbox = layout.itemAt(1).widget()
            return spinbox.value()

        # Update bot object
        self.bot.name = self.name_widget.text()
        self.bot.model = self.model_widget.text()
        self.bot.hidden = self.hidden_widget.isChecked()
        self.bot.system_prompt = self.system_prompt_widget.toPlainText()
    
        self.bot.max_tokens = get_slider_spinbox_value(self.max_tokens_widget)
        self.bot.temperature = get_slider_spinbox_value(self.temperature_widget)
        self.bot.top_p = get_slider_spinbox_value(self.top_p_widget)
        self.bot.frequency_penalty = get_slider_spinbox_value(self.frequency_penalty_widget)
        self.bot.presence_penalty = get_slider_spinbox_value(self.presence_penalty_widget)

        # Log the update
        log.info(f"Bot {self.bot.name} updated successfully")
        log.info(f"current params are: {self.bot}")

    def expand_system_prompt(self):
        # Create a new dialog with a QTextEdit to facilitate longer format input
        self.dialog = QDialog()
        layout = QVBoxLayout()
        self.dialog.setLayout(layout)

        text_edit = QTextEdit()
        layout.addWidget(text_edit)

        # Populate the new QTextEdit with the current system prompt
        text_edit.setText(self.system_prompt_widget.toPlainText())

        # Create OK and Cancel buttons for the dialog
        ok_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")

        ok_button.clicked.connect(lambda: self.update_system_prompt_and_close_dialog(text_edit))
        cancel_button.clicked.connect(self.dialog.close)

        layout.addWidget(ok_button)
        layout.addWidget(cancel_button)

        self.dialog.show()

    def update_system_prompt_and_close_dialog(self, text_edit):
        # Update the system prompt with the contents of the QTextEdit in the dialog
        self.system_prompt_widget.setText(text_edit.toPlainText())
        # Close the dialog
        self.dialog.close()
 
        
        
if __name__ == "__main__":
    bot = Bot(_id=1,name="",model=None,rank=5, hidden=False)
    app = QApplication()
    bot_widget = BotWidget(bot=bot)
    bot_widget.show()
    app.exec()