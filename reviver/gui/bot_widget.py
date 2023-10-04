from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QPushButton,
    QWidget,
    QFormLayout,
    QTextEdit,
    QSlider,
    QVBoxLayout,
    QHBoxLayout,
    QDoubleSpinBox,
    QSpinBox,
)
from PySide6.QtCore import Qt
import reviver.log
from reviver.gui.models_widget import ModelsWidget
from reviver.controller import Controller

log = reviver.log.get(__name__)


class BotWidget(QWidget):
    def __init__(self, controller: Controller, bot_name=None, parent=None):
        super(BotWidget, self).__init__(parent)
        self.controller = controller

        # Create widgets for each parameter of the Bot class
        self.name_widget = QLabel()
        self.model_name = QPushButton()
        # self.hidden_widget = QCheckBox()

        # System prompt will have option to expand
        self.system_prompt_container = QVBoxLayout()
        self.system_prompt_widget = QTextEdit()
        self.expand_button = QPushButton("Expand")
        self.system_prompt_container.addWidget(self.system_prompt_widget)
        self.system_prompt_container.addWidget(self.expand_button)

        self.max_tokens_widget = self.create_slider_spinbox_pair(1, 1000, 1)
        self.temperature_widget = self.create_slider_spinbox_pair(0, 2, 0.05)
        self.top_p_widget = self.create_slider_spinbox_pair(0, 1, 0.05)
        self.frequency_penalty_widget = self.create_slider_spinbox_pair(0, 2, 0.05)
        self.presence_penalty_widget = self.create_slider_spinbox_pair(0, 2, 0.05)

        # Add Save and Cancel buttons
        self.save_button = QPushButton("Save Changes")
        self.cancel_button = QPushButton("Cancel Changes")

        self.place_widgets()
        self.connect_widgets()
        self.bot_name = bot_name
        self.display_bot(self.bot_name)  # will set self.bot to bot within

    def connect_widgets(self):
        self.expand_button.clicked.connect(self.expand_system_prompt)
        self.save_button.clicked.connect(self.update_bot)
        self.cancel_button.clicked.connect(
            self.restore_bot
        )  # revert the form to what it was (the current bot state)
        self.model_name.clicked.connect(self.show_models_widget)

    def place_widgets(self):
        self.setLayout(QVBoxLayout())
        # Initialize form layout
        self.form = QFormLayout()

        # Add widgets to form layout
        self.form.addRow("name", self.name_widget)
        self.form.addRow("model", self.model_name)
        # self.form.addRow("hidden", self.hidden_widget)
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

        if step_size == 1:
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

    def restore_bot(self):
        self.display_bot(self.bot_name)

    def set_all_children_enabled(self, enabled: bool):
        for child in self.children():
            if isinstance(child, QWidget):  # check if the child is a widget
                child.setEnabled(enabled)

    def display_bot(self, bot_name: str = None):
        if bot_name is not None:
            self.bot_name = bot_name  # maintain reference for restoring
            bot_data = self.controller.get_bot_data(bot_name)
            set_child_widget_enabled(self, True)
            name = bot_data["name"]
            model = bot_data["model"]
            system_prompt = bot_data["system_prompt"]
            max_tokens = bot_data["max_tokens"]
            temperature = bot_data["temperature"]
            top_p = bot_data["top_p"]
            frequency_penalty = bot_data["frequency_penalty"]
            presence_penalty = bot_data["presence_penalty"]
        else:
            log.info("Disabling children widgets")
            set_child_widget_enabled(self, False)
            name = ""
            model = ""
            system_prompt = ""
            max_tokens = 0
            temperature = 0
            top_p = 0
            frequency_penalty = 0
            presence_penalty = 0

        def set_slider_spinbox_value(layout, value):
            # Slider is the first child in the layout
            slider = layout.itemAt(0).widget()
            slider.setValue(value)

            # SpinBox is the second child in the layout
            spinbox = layout.itemAt(1).widget()
            spinbox.setValue(value)

        self.name_widget.setText(name)

        self.model_name.setText(model or "None")
        self.system_prompt_widget.setText(system_prompt)

        set_slider_spinbox_value(self.max_tokens_widget, max_tokens)
        set_slider_spinbox_value(self.temperature_widget, temperature)
        set_slider_spinbox_value(self.top_p_widget, top_p)
        set_slider_spinbox_value(self.frequency_penalty_widget, frequency_penalty)
        set_slider_spinbox_value(self.presence_penalty_widget, presence_penalty)

    def update_bot(self):
        def get_slider_spinbox_value(layout):
            # Slider is the first child in the layout
            spinbox = layout.itemAt(1).widget()
            return spinbox.value()

        # pull down current parameters of bot
        name = self.name_widget.text()
        model = self.model_name.text()
        system_prompt = self.system_prompt_widget.toPlainText()
        max_tokens = get_slider_spinbox_value(self.max_tokens_widget)
        temperature = get_slider_spinbox_value(self.temperature_widget)
        top_p = get_slider_spinbox_value(self.top_p_widget)
        frequency_penalty = get_slider_spinbox_value(self.frequency_penalty_widget)
        presence_penalty = get_slider_spinbox_value(self.presence_penalty_widget)

        # update bot
        log.info(f"Directing controller to update Bot {name}")
        self.controller.update_bot(
            bot_name=name,
            model=model,
            system_prompt=system_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
        )

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
        ok_button = QPushButton("Return")
        cancel_button = QPushButton("Cancel")

        ok_button.clicked.connect(
            lambda: self.update_system_prompt_and_close_dialog(text_edit)
        )
        cancel_button.clicked.connect(self.dialog.close)

        layout.addWidget(ok_button)
        layout.addWidget(cancel_button)

        self.dialog.show()

    def update_system_prompt_and_close_dialog(self, text_edit):
        # Update the system prompt with the contents of the QTextEdit in the dialog
        self.system_prompt_widget.setText(text_edit.toPlainText())
        # Close the dialog
        self.dialog.close()

    def show_models_widget(self):
        log.info("Launching models widget")
        spec_sheet = self.controller.get_spec_sheet()
        self.models_widget = ModelsWidget(spec_sheet)
        self.models_widget.selected_model.connect(self.update_model_widget)
        self.models_widget.show()

    def update_model_widget(self, model_name: str):
        log.info(f"Setting model name to {model_name}")
        self.model_name.setText(model_name)


def set_child_widget_enabled(parent_widget, enabled: bool):
    for child in parent_widget.children():
        if isinstance(child, QWidget):  # check if the child is a widget
            child.setEnabled(enabled)
            set_child_widget_enabled(
                child, enabled
            )  # recursively disable grandchildren


if __name__ == "__main__":
    from reviver.controller import Controller

    from pathlib import Path

    archive_dir = Path(Path.home(), "reviver")
    controller = Controller(archive_dir)
    controller.add_bot("test_bot")
    app = QApplication()
    bot_widget = BotWidget(controller, "test_bot")
    bot_widget.show()
    app.exec()
