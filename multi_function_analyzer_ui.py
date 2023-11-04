import sys
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QTextEdit,
                               QVBoxLayout, QWidget, QSplitter, QPushButton,
                               QFileDialog, QLineEdit, QLabel, QListWidget, QListWidgetItem, QHBoxLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import requests, json
from PIL import Image
from PIL.ExifTags import TAGS

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

        # Save button
        save_button = QPushButton('Save File')
        save_button.clicked.connect(self.save_file)
        layout.addWidget(save_button)

        # File Information
        self.file_info_label = QLabel("")
        layout.addWidget(self.file_info_label)

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
                self.text_editor.setPlainText(file_content.decode('utf-8', 'replace'))
                hex_content = ' '.join(f'{byte:02X}' for byte in file_content)
                self.hex_editor.setPlainText(hex_content)
                file_info = os.stat(file_name)
                file_size = file_info.st_size
                file_mtime = datetime.fromtimestamp(file_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                self.file_info_label.setText(f"Size: {file_size} bytes\nLast Modified: {file_mtime}")

    def load_from_url(self):
        url = self.url_input.text()
        if url:
            try:
                response = requests.get(url)
                response.raise_for_status()
                content = response.content
                headers_text = '\n'.join(f'{key}: {value}' for key, value in response.headers.items())
                self.text_editor.setPlainText(headers_text + "\n\n" + content.decode('utf-8', 'replace'))
                hex_content = ' '.join(f'{byte:02X}' for byte in content)
                self.hex_editor.setPlainText(hex_content)
            except requests.exceptions.RequestException as e:
                self.text_editor.setPlainText(f"Error: {str(e)}")
                self.hex_editor.setPlainText("")

    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*);;Text Files (*.txt);;Hex Files (*.hex)")
        if file_name:
            with open(file_name, 'wb') as file:
                hex_content = self.hex_editor.toPlainText().split()
                file_content = bytes([int(value, 16) for value in hex_content])
                file.write(file_content)

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
        main_layout = QVBoxLayout(self)

        # Create a horizontal splitter for text and hex views
        view_splitter = QSplitter(Qt.Horizontal)

        # Text View (left)
        self.text_viewer = QTextEdit()
        self.text_viewer.setReadOnly(True)
        view_splitter.addWidget(self.text_viewer)

        # Hex View (right)
        self.hex_viewer = QTextEdit()
        self.hex_viewer.setReadOnly(True)
        view_splitter.addWidget(self.hex_viewer)

        # Set sizes for the splitter to give more space to the text view
        view_splitter.setSizes([400, 200])

        # Add the horizontal splitter to the main layout
        main_layout.addWidget(view_splitter)

        # Headers List View (bottom)
        self.headers_list = QListWidget()
        main_layout.addWidget(self.headers_list)

        # URL Input and Load Button
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        url_layout.addWidget(self.url_input)
        load_button = QPushButton("Load from URL")
        load_button.clicked.connect(self.load_from_url)
        url_layout.addWidget(load_button)

        main_layout.addLayout(url_layout)

    def load_from_url(self):
        url = self.url_input.text()
        if url:
            try:
                response = requests.get(url)
                response.raise_for_status()
                
                # Display content in the Text Viewer (e.g., HTML)
                self.text_viewer.setPlainText(response.text)

                # Add headers to the Headers List View
                self.headers_list.clear()  # Clear existing items
                for key, value in response.headers.items():
                    item_text = f'{key}: {value}'
                    self.headers_list.addItem(QListWidgetItem(item_text))

                # Display content in hex in the Hex Viewer
                hex_content = ' '.join(f'{byte:02X}' for byte in response.content)
                self.hex_viewer.setPlainText(hex_content)
            except requests.exceptions.RequestException as e:
                self.text_viewer.setPlainText(f"Error: {str(e)}")
                self.hex_viewer.setPlainText("")

class ImageMetadataWindow(QWidget):
    def __init__(self):
        super(ImageMetadataWindow, self).__init__()
        layout = QVBoxLayout(self)

        # Create a QLabel for displaying the image
        self.image_label = QLabel()
        self.image_label.setScaledContents(True)
        layout.addWidget(self.image_label)

        # Create a QTextEdit for displaying image metadata
        self.image_metadata = QTextEdit()
        self.image_metadata.setReadOnly(True)
        layout.addWidget(self.image_metadata)

        # Create buttons
        load_button = QPushButton('Load Image')
        load_button.clicked.connect(self.load_image)
        export_button = QPushButton('Export Metadata as JSON')
        export_button.clicked.connect(self.export_metadata)
        layout.addWidget(load_button)
        layout.addWidget(export_button)

    def load_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.jpg *.jpeg *.png *.bmp *.gif)", options=options)

        if file_name:
            # Load the image using Pillow
            image = Image.open(file_name)

            # Display the image with a maximum size
            max_size = (600, 600)
            pixmap = QPixmap(file_name).scaled(max_size[0], max_size[1], Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)

            # Get and display all image metadata
            self.metadata = self.extract_metadata(image)
            metadata_text = json.dumps(self.metadata, indent=4)
            self.image_metadata.setPlainText(metadata_text)

    def extract_metadata(self, image):
        # Ouvrir l'image
        

        # Obtenir les métadonnées EXIF
        exif_data = image._getexif()

        # Créer un dictionnaire pour les métadonnées
        metadata = {}

        # Ajouter des métadonnées spécifiques non-EXIF
        metadata["FileType"] = image.format
        metadata["ImageWidth"] = image.width
        metadata["ImageHeight"] = image.height
        metadata["ImageSize"] = f"{image.width}x{image.height}"
        metadata["Megapixels"] = round((image.width * image.height) / 1000000, 2)

        # Obtenir les métadonnées EXIF
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag, tag)
                if tag_name in ["ExifImageWidth", "ExifImageHeight", "Make", "Model", "Software", "DateTimeOriginal", "GPSInfo"]:
                    # Convertir les valeurs IFDRational en chaîne de caractères
                    if isinstance(value, tuple):
                        value = f"{value[0]}/{value[1]}"
                    metadata[tag_name] = value
        
        return metadata


    def export_metadata(self):
        if hasattr(self, 'metadata'):
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Metadata", "", "JSON Files (*.json)", options=options)
            if file_name:
                with open(file_name, 'w') as f:
                    json.dump(self.metadata, f, indent=4)


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
        tab_widget.addTab(image_metadata_tab, "Image Metadata Viewer")

        self.setCentralWidget(tab_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MultiFunctionAnalyzer()
    window.show()
    sys.exit(app.exec())
