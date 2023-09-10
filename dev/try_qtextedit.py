from PySide6.QtWidgets import QApplication, QTextEdit

app = QApplication([])
text_edit = QTextEdit()
text_edit.setHtml("""
    <p style='color: blue;'>Human: Hello</p>
    <p style='color: green;'>AI: Hi there</p>
    
    kjkt
""")
text_edit.show()
app.exec()