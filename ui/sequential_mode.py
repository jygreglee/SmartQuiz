from PyQt5.QtWidgets import QWidget, QVBoxLayout
from ui.problem_view import ProblemView
from ui.utils import create_quiz_button
from core.manager import ProblemManager

class SequentialModeWidget(QWidget):
    def __init__(self, problems):
        super().__init__()
        self.manager = ProblemManager(problems)
        self.adjustSize()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(12)
        self.layout.setContentsMargins(20, 10, 20, 20)
        
        self.problem_view = ProblemView(self.manager.current())
        self.layout.addWidget(self.problem_view)

        # 이전 문제
        btn_prev = create_quiz_button("⬅ 이전 문제")
        btn_prev.clicked.connect(self.show_prev)
        self.layout.addWidget(btn_prev)

        # 다음 문제
        btn_next = create_quiz_button("다음 문제 ➡")
        btn_next.clicked.connect(self.show_next)
        self.layout.addWidget(btn_next)

        # 모드 선택으로 돌아가기
        btn_back = create_quiz_button("⬅ 모드 선택으로 돌아가기")
        btn_back.clicked.connect(self.go_back)
        self.layout.addWidget(btn_back)

        # 창 초기 리사이즈
        self.propagate_resize()

    # ---------------------------
    # 🔥 부모 창 리사이즈 반영
    # ---------------------------
    def propagate_resize(self):
        parent = self.window()
        if parent:
            # 🔥 현재 설정된 창 너비 유지
            fixed_width = parent.width()
    
            parent.adjustSize()  # 내용 기반 크기 계산
            new_height = parent.sizeHint().height()
    
            # 🔥 너비 고정, 높이만 조정
            parent.resize(fixed_width, new_height)

    # ---------------------------
    # 🔥 문제 변경 시 ProblemView 교체
    # ---------------------------
    def change_problem(self):
        # 기존 뷰 제거
        self.layout.removeWidget(self.problem_view)
        self.problem_view.deleteLater()

        # 새 문제 뷰 생성
        self.problem_view = ProblemView(self.manager.current())
        self.layout.insertWidget(0, self.problem_view)

        # 창 크기 갱신
        self.propagate_resize()

    # ---------------------------
    def show_prev(self):
        self.manager.prev()
        self.change_problem()

    def show_next(self):
        # 🔥 먼저 현재 문제 화면 접기
        if self.problem_view:
            self.problem_view.collapse_view()
            
        self.manager.next()
        self.change_problem()

    def go_back(self):
        main_win = self.window()
        if hasattr(main_win, "show_mode_select"):
            main_win.show_mode_select()
