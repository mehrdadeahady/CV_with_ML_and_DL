from PyQt6.QtWidgets import QFileDialog, QMenu
from PyQt6.QtPdf import QPdfDocument
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtCore import Qt
import shutil
import ctypes

class CustomPdfView(QPdfView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.pdf_document = None

    def show_context_menu(self, pos):
        menu = QMenu(self)
        download_action = menu.addAction("Download PDF")
        action = menu.exec(self.mapToGlobal(pos))
        if action == download_action:
            self.download_pdf()
     
    def download_pdf(self):
        if not hasattr(self, "pdf_path") or not self.pdf_path:
            print("No source file path available.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF", self.pdf_path , "PDF Files (*.pdf)"  #"document.pdf"
        )
        if file_path:
            try:
                shutil.copyfile(self.pdf_path, file_path)
                print(f"PDF saved to {file_path}")
                return f"PDF saved to {file_path}"
            except Exception as e:
                print(f"Failed to save PDF: {e}")
                return f"Failed to save PDF: {e}"

