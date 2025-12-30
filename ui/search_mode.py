from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton
from ui.problem_view import ProblemView
from PyQt5.QtWidgets import QCompleter


class SearchModeWidget(QWidget):
    def __init__(self, problems):
        super().__init__()
        self.problems = problems

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        # 🔹 자동완성용 단어 목록 생성
        topic_list = [p.topic for p in self.problems]
        completer = QCompleter(topic_list)
        completer.setCaseSensitivity(False)

        # 🔹 검색창
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("검색어 입력")
        self.search_box.setCompleter(completer)
        self.vbox.addWidget(self.search_box)

        # 🔹 검색 버튼
        btn = QPushButton("검색")
        btn.clicked.connect(self.search)
        self.vbox.addWidget(btn)

        self.problem_view = None

        # 🔥 ① 초기 ProblemView 자동생성
        self.show_initial_problem()

        # 🔹 뒤로가기 버튼
        btn_back = QPushButton("⬅ 모드 선택으로 돌아가기")
        btn_back.clicked.connect(self.go_back)
        self.vbox.addWidget(btn_back)

        self.adjust_parent_window()

    # ---------------------------------------------------
    # 🔥 ② 처음 진입 시 첫 문제를 자동 표시
    # ---------------------------------------------------
    def show_initial_problem(self):
        first_problem = self.problems[0]   # 첫 번째 행 문제를 기본 출력

        self.problem_view = ProblemView(first_problem)
        self.vbox.insertWidget(2, self.problem_view)

    # ---------------------------------------------------
    # 🔍 ③ 검색 기능
    # ---------------------------------------------------
    def search(self):
        keyword = self.search_box.text().strip()
        if not keyword:
            return

        for p in self.problems:
            if keyword.lower() in p.topic.lower():

                if self.problem_view:
                    if hasattr(self.problem_view, "collapse_view"):
                        self.problem_view.collapse_view()
                    
                    self.vbox.removeWidget(self.problem_view)
                    self.problem_view.deleteLater()

                self.problem_view = ProblemView(p)

                # 뒤로가기 버튼 바로 위에 삽입
                insert_index = self.vbox.count() - 1
                self.vbox.insertWidget(insert_index, self.problem_view)

                self.adjust_parent_window()
                return

    # ---------------------------------------------------
    def go_back(self):
        main_win = self.window()
        if hasattr(main_win, "show_mode_select"):
            main_win.show_mode_select()

    def adjust_parent_window(self):
        w = self.window()
        if w:
            w.adjustSize()
            w.resize(w.sizeHint())
