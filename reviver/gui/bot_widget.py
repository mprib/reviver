from PySide6.QtWidgets import QApplication,  QWidget, QFormLayout, QLineEdit,QTextEdit, QCheckBox, QSpinBox, QDoubleSpinBox, QSlider
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
        self.max_tokens_widget = QSlider()
        self.temperature_widget = QSlider()
        self.top_p_widget = QSlider()
        self.frequency_penalty_widget = QSlider()
        self.presence_penalty_widget = QSlider()

        # Connect widgets to update methods
        self.name_widget.textChanged.connect(self.update_name)
        self.model_widget.textChanged.connect(self.update_model)
        self.hidden_widget.toggled.connect(self.update_hidden)
        self.system_prompt_widget.textChanged.connect(self.update_system_prompt)
        self.max_tokens_widget.valueChanged.connect(self.update_max_tokens)
        self.temperature_widget.valueChanged.connect(self.update_temperature)
        self.top_p_widget.valueChanged.connect(self.update_top_p)
        self.frequency_penalty_widget.valueChanged.connect(self.update_frequency_penalty)
        self.presence_penalty_widget.valueChanged.connect(self.update_presence_penalty)

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

    def load_bot(self):
        self.name_widget.setText(self.bot.name)
        self.model_widget.setText(self.bot.model)
        self.hidden_widget.setChecked(self.bot.hidden)
        self.system_prompt_widget.setText(self.bot.system_prompt)
        self.max_tokens_widget.setValue(self.bot.max_tokens)
        self.temperature_widget.setValue(self.bot.temperature)
        self.top_p_widget.setValue(self.bot.top_p)
        self.frequency_penalty_widget.setValue(self.bot.frequency_penalty)
        self.presence_penalty_widget.setValue(self.bot.presence_penalty)

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