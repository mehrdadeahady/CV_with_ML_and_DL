try:
    from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel,QScrollArea, QPushButton, QDialogButtonBox
    from PyQt6.QtCore import QUrl, Qt
except:
    print("You Should Install PyQt6 Library!")

import sys

class ScrollableMessageBox(QDialog):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(680, 600)

        layout = QVBoxLayout(self)

        # Scroll area setup
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)

        # Content widget inside scroll area
        content = QLabel(message)
        content.setWordWrap(True)

        content.setStyleSheet("""
                                QLabel { padding: 0px; text-align: center;
                                }
                             """)

        # Also center the text using alignment flags
        #content.setAlignment(Qt.AlignmentFlag.AlignCenter)

        scroll.setWidget(content)
        layout.addWidget(scroll)

        # OK button
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

def show_scrollable_message(title, message):
    dialog = ScrollableMessageBox(title, message)
    #dialog.show()
    dialog.exec()

