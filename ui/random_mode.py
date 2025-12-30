from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from ui.problem_view import ProblemView
import random

class RandomModeWidget(QWidget):
    def __init__(self, problems):
        super().__init__()
        self.problems = problems

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.show_random_problem()
        self.vbox.setSpacing(12)
        self.vbox.setContentsMargins(20, 10, 20, 20)

        btn_next = QPushButton("다음 랜덤 문제 ➡")
        btn_next.clicked.connect(self.show_random_problem)
        self.vbox.addWidget(btn_next)

        # 🔥 모드 선택 돌아가기 버튼 추가
        btn_back = QPushButton("⬅ 모드 선택으로 돌아가기")
        btn_back.clicked.connect(self.go_back)
        self.vbox.addWidget(btn_back)

        self.adjust_parent_window()

    def show_random_problem(self):
        if hasattr(self, 'problem_view'):
            self.problem_view.collapse_view()
            self.vbox.removeWidget(self.problem_view)
            self.problem_view.deleteLater()

        problem = random.choice(self.problems)
        self.problem_view = ProblemView(problem)
        self.vbox.insertWidget(0, self.problem_view)

        self.adjust_parent_window()
        
    def go_back(self):
        main_win = self.window()
        if hasattr(main_win, "show_mode_select"):
            main_win.show_mode_select()

    def adjust_parent_window(self):
        w = self.window()
        if w:
            w.adjustSize()
            w.resize(w.sizeHint())
