from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import pyqtSignal

class ModeSelectWidget(QWidget):
    mode_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        
        title = QLabel("문제풀이 모드 선택")
        title.setObjectName("title")
        layout.addWidget(title)
        self.setMinimumWidth(400)
        
        btn_search = QPushButton("🔍 검색 모드")
        btn_random = QPushButton("🎲 랜덤 모드")
        btn_seq = QPushButton("➡️ 차례 모드")

        btn_search.clicked.connect(lambda: self.mode_selected.emit("search"))
        btn_random.clicked.connect(lambda: self.mode_selected.emit("random"))
        btn_seq.clicked.connect(lambda: self.mode_selected.emit("seq"))

        layout.addSpacing(20)
        layout.addWidget(btn_search)
        layout.addWidget(btn_random)
        layout.addWidget(btn_seq)
        layout.addStretch()

        self.setLayout(layout)
