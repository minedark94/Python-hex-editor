import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QTextEdit, QVBoxLayout, QWidget, QSplitter, QPushButton, QFileDialog, QLineEdit, QLabel
import requests
from PIL import Image, ExifTags
from PySide6.QtGui import QPixmap

import binascii

class HexEditorWindow(QWidget):
    def __init__(self):
        super(HexEditorWindow, self).__init__()
        layout = QVBoxLayout()

        # Create a horizontal splitter
        splitter = QSplitter()

        # Text View
        self.text_editor = QTextEdit()
        splitter.addWidget(self.text_editor)

        # Hex View
        self.hex_editor = QTextEdit()
        splitter.addWidget(self.hex_editor)

        layout.addWidget(splitter)

        # Add an URL input field
        self.url_input = QLineEdit()
        layout.addWidget(self.url_input)

        # Add a Load button
        load_button = QPushButton('Load File')
        load_button.clicked.connect(self.load_file)
        layout.addWidget(load_button)

        # Add a Load from URL button
        load_url_button = QPushButton('Load from URL')
        load_url_button.clicked.connect(self.load_from_url)
        layout.addWidget(load_url_button)

        self.setLayout(layout)

        # Connect text change events to update each other
        self.text_editor.textChanged.connect(self.update_hex_view)
        self.hex_editor.textChanged.connect(self.update_text_view)

    def load_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt);;Hex Files (*.hex)", options=options)

        if file_name:
            with open(file_name, 'rb') as file:
                file_content = file.read()
                self.text_editor.setPlainText(file_content.decode('utf-8'))
                hex_content = ' '.join(f'{byte:02X}' for byte in file_content)
                self.hex_editor.setPlainText(hex_content)

    def load_from_url(self):
        url = self.url_input.text()
        if url:
            try:
                response = requests.get(url)
                response.raise_for_status()
                content = response.content

                self.text_editor.setPlainText(content.decode('utf-8'))
                hex_content = ' '.join(f'{byte:02X}' for byte in content)
                self.hex_editor.setPlainText(hex_content)
            except requests.exceptions.RequestException as e:
                self.text_editor.setPlainText(f"Error: {str(e)}")
                self.hex_editor.setPlainText("")

    def update_hex_view(self):
        text_content = self.text_editor.toPlainText()
        hex_content = ' '.join(f'{ord(char):02X}' for char in text_content)
        self.hex_editor.setPlainText(hex_content)

    def update_text_view(self):
        hex_content = self.hex_editor.toPlainText()
        hex_values = hex_content.split()
        text_content = ''.join(chr(int(value, 16)) for value in hex_values)
        self.text_editor.setPlainText(text_content)

class HexNetworkViewerWindow(QWidget):
    def __init__(self):
        super(HexNetworkViewerWindow, self).__init__()
        layout = QVBoxLayout()

        # Create a horizontal splitter
        splitter = QSplitter()

        # Text View
        self.text_viewer = QTextEdit()
        splitter.addWidget(self.text_viewer)

        # Hex View
        self.hex_viewer = QTextEdit()
        splitter.addWidget(self.hex_viewer)

        layout.addWidget(splitter)
        self.setLayout(layout)

class ImageMetadataWindow(QWidget):
    def __init__(self):
        super(ImageMetadataWindow, self).__init__()
        layout = QVBoxLayout()

        # Create a QLabel for displaying the image
        self.image_label = QLabel()
        layout.addWidget(self.image_label)

        # Create a QTextEdit for displaying image metadata
        self.image_metadata = QTextEdit()
        layout.addWidget(self.image_metadata)

        # Create a Load Image button
        load_button = QPushButton('Load Image')
        load_button.clicked.connect(self.load_image)
        layout.addWidget(load_button)

        self.setLayout(layout)

    def load_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.jpg *.jpeg *.png *.bmp *.gif)", options=options)

        if file_name:
            # Load the image using Pillow
            image = Image.open(file_name)

            # Display the image
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap)

            # Get and display all image metadata
            metadata_text = "Image Metadata:\n"
            for key, value in image.info.items():
                metadata_text += f"{key}: {value}\n"
            self.image_metadata.setPlainText(metadata_text)

class MultiFunctionAnalyzer(QMainWindow):
    def __init__(self):
        super(MultiFunctionAnalyzer, self).__init__()

        self.setWindowTitle("Multi-Function File Analyzer")
        self.setGeometry(100, 100, 800, 600)

        tab_widget = QTabWidget()
        hex_editor_tab = HexEditorWindow()
        hex_network_viewer_tab = HexNetworkViewerWindow()
        image_metadata_tab = ImageMetadataWindow()

        tab_widget.addTab(hex_editor_tab, "Hex Editor")
        tab_widget.addTab(hex_network_viewer_tab, "Hex Network Viewer")
        tab_widget.addTab(image_metadata_tab, "Image Metadata")

        self.setCentralWidget(tab_widget)

def main():
    app = QApplication(sys.argv)
    window = MultiFunctionAnalyzer()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
