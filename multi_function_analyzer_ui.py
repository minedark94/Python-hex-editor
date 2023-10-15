import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QTextEdit, QVBoxLayout, QWidget

class HexEditorWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.hex_editor = QTextEdit()
        layout.addWidget(self.hex_editor)
        self.setLayout(layout)

class HexNetworkViewerWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.network_viewer = QTextEdit()
        layout.addWidget(self.network_viewer)
        self.setLayout(layout)

class ImageMetadataWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.image_metadata = QTextEdit()
        layout.addWidget(self.image_metadata)
        self.setLayout(layout)

class MultiFunctionAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()

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
