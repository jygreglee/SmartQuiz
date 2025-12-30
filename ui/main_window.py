from PyQt5.QtWidgets import QMainWindow
from ui.mode_select import ModeSelectWidget
from ui.search_mode import SearchModeWidget
from ui.random_mode import RandomModeWidget
from ui.sequential_mode import SequentialModeWidget

class MainWindow(QMainWindow):
    def __init__(self, problems):
        super().__init__()
        self.problems = problems
        self.setWindowTitle("SmartTopicQuiz")
        self.show_mode_select()

    def show_mode_select(self):
        widget = ModeSelectWidget()
        widget.mode_selected.connect(self.start_mode)
        self.setCentralWidget(widget)
        
        # 🔥 모드 선택 화면일 때만 최소 크기 설정
        self.setMinimumSize(400, 200)
        self.adjustSize()

    def start_mode(self, mode):
        # 🔥 최소 크기 해제
        self.setMinimumSize(0, 0)
        if mode == "search":
            self.setCentralWidget(SearchModeWidget(self.problems))
        elif mode == "random":
            self.setCentralWidget(RandomModeWidget(self.problems))
        elif mode == "seq":
            self.setCentralWidget(SequentialModeWidget(self.problems))