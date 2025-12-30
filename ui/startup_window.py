# ui/startup_window.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox
)
from core.loader import ProblemBankLoader


class StartupWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SmartTopicQuiz - 준비")
        self.setMinimumWidth(400)
        self.problems = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.btn_load = QPushButton("📂 문제 엑셀 파일 불러오기")
        self.btn_load.clicked.connect(self.load_excel)
        layout.addWidget(self.btn_load)

        self.btn_start = QPushButton("▶ 프로그램 시작")
        self.btn_start.setEnabled(False)
        layout.addWidget(self.btn_start)

        self.setLayout(layout)

    def load_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "문제 엑셀 파일 선택",
            "",
            "Excel Files (*.xlsx *.xls)"
        )
        if not file_path:
            return

        try:
            loader = ProblemBankLoader(file_path)
            problems = loader.load()

            if not problems:
                QMessageBox.warning(self, "데이터 없음", "문제를 불러오지 못했습니다.")
                return

            self.problems = problems
            self.btn_start.setEnabled(True)
            QMessageBox.information(self, "성공", "엑셀 파일이 로드되었습니다.")

        except Exception as e:
            QMessageBox.critical(self, "엑셀 오류", str(e))
