from PySide6.QtWidgets import QApplication,  QWidget, QFormLayout, QLineEdit, QTextEdit, QCheckBox, QSlider, QHBoxLayout, QDoubleSpinBox, QSpinBox
from PySide6.QtCore import Qt
from reviver.bot import Bot

class BotWidget(QWidget):
    def __init__(self, bot: Bot, parent=None):
        super(BotWidget, self).__init__(parent)
        self.bot = bot

        # Initialize form layout
        self.form = QFormLayout()

        # Create widgets for each parameter of the Bot class
        self.name_widget = QLineEdit()
        self.model_widget = QLineEdit()
        self.hidden_widget = QCheckBox()
        self.system_prompt_widget = QTextEdit()
        self.max_tokens_widget = self.create_slider_spinbox_pair(1, 1000, 1, self.update_max_tokens)
        self.temperature_widget = self.create_slider_spinbox_pair(0, 2,.05, self.update_temperature)
        self.top_p_widget = self.create_slider_spinbox_pair(0, 1,.05,  self.update_top_p)
        self.frequency_penalty_widget = self.create_slider_spinbox_pair(0, 2,.05, self.update_frequency_penalty)
        self.presence_penalty_widget = self.create_slider_spinbox_pair(0, 2,.05, self.update_presence_penalty)

        # Add widgets to form layout
        self.form.addRow("name", self.name_widget)
        self.form.addRow("model", self.model_widget)
        self.form.addRow("hidden", self.hidden_widget)
        self.form.addRow("system_prompt", self.system_prompt_widget)
        self.form.addRow("max_tokens", self.max_tokens_widget)
        self.form.addRow("temperature", self.temperature_widget)
        self.form.addRow("top_p", self.top_p_widget)
        self.form.addRow("frequency_penalty", self.frequency_penalty_widget)
        self.form.addRow("presence_penalty", self.presence_penalty_widget)

        # Set the form layout to the widget
        self.setLayout(self.form)

        # Load bot data into widgets
        self.load_bot()

    def create_slider_spinbox_pair(self, min_value, max_value, step_size, slot):

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
        spinbox.valueChanged.connect(slot)

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


    def update_id(self, value):
        self.bot._id = int(value)

    def update_name(self, value):
        self.bot.name = value

    def update_model(self, value):
        self.bot.model = value

    def update_rank(self, value):
        self.bot.rank = value

    def update_hidden(self, value):
        self.bot.hidden = value

    def update_system_prompt(self, value):
        self.bot.system_prompt = value

    def update_max_tokens(self, value):
        self.bot.max_tokens = value

    def update_temperature(self, value):
        self.bot.temperature = value

    def update_top_p(self, value):
        self.bot.top_p = value

    def update_frequency_penalty(self, value):
        self.bot.frequency_penalty = value

    def update_presence_penalty(self, value):
        self.bot.presence_penalty = value
        
        
        
if __name__ == "__main__":
    bot = Bot(_id=1,name="",model=None,rank=5, hidden=False)
    app = QApplication()
    bot_widget = BotWidget(bot=bot)
    bot_widget.show()
    app.exec()