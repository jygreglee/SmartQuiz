from PyQt5.QtWidgets import QPushButton, QSizePolicy

def create_quiz_button(text):
    btn = QPushButton(text)
    btn.setFixedHeight(48)
    btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    btn.setStyleSheet("""
        QPushButton {
            background-color: #1976D2;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
        }
        QPushButton:hover {
            background-color: #1E88E5;
        }
        QPushButton:pressed {
            background-color: #1565C0;
        }
    """)
    return btn
