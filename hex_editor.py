import sys
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QTextEdit, QPushButton, QApplication, QSplitter, QWidget

class HexEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Hex Editor')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QSplitter()
        self.setCentralWidget(self.central_widget)

        # Create the text view
        self.text_widget = QTextEdit()
        self.central_widget.addWidget(self.text_widget)

        # Create the hex view
        self.hex_widget = QTextEdit()
        self.central_widget.addWidget(self.hex_widget)

        # Create a button to save
        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save)
        self.central_widget.addWidget(self.save_button)

    def save(self):
        # Implement the save functionality here
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = HexEditor()
    editor.show()
    sys.exit(app.exec_())
