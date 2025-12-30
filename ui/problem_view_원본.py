from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QSizePolicy
)
from PyQt5.QtGui import QFontMetrics
from ui.utils import create_quiz_button

class ProblemView(QWidget):
    def __init__(self, problem):
        super().__init__()

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.setFixedWidth(500)

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)

        def safe_str(v):
            if v is None: return ""
            if isinstance(v, float): return ""
            return str(v)

        title = QLabel(problem.topic)
        title.setWordWrap(True)
        title.setObjectName("title")
        layout.addWidget(title)
        
        self.fit_font_to_width(title, 480)

        lbl_imp = QLabel(f"중요도: {problem.importance}")
        layout.addWidget(lbl_imp)

        # 설명 버튼 + 텍스트
        self.btn_desc = create_quiz_button("키워드 설명 보기")
        self.btn_desc.clicked.connect(self.toggle_desc)
        layout.addWidget(self.btn_desc)

        self.desc_box = QTextEdit()
        self.desc_box.setReadOnly(True)
        self.desc_box.setText(safe_str(problem.description))
        self.desc_box.hide()
        self.desc_box.setMaximumHeight(0)     # ★ 핵심
        
        # 🔥 가로로는 고정한 상태에서 높이만 변경되게 함
        layout.addWidget(self.desc_box)

        # 암기법 버튼 + 텍스트
        self.btn_memo = create_quiz_button("암기법 보기")
        self.btn_memo.clicked.connect(self.toggle_memo)
        layout.addWidget(self.btn_memo)

        self.memo_box = QTextEdit()
        self.memo_box.setReadOnly(True)
        self.memo_box.setText(safe_str(problem.mnemonic))
        self.memo_box.hide()
        self.memo_box.setMaximumHeight(0)     # ★ 핵심
        
        layout.addWidget(self.memo_box)

        self.setLayout(layout)
        
    def fit_font_to_width(self, label, max_width):
        font = label.font()
        fm = QFontMetrics(font)
    
        while fm.width(label.text()) > max_width and font.pointSize() > 8:
            font.setPointSize(font.pointSize() - 1)
            label.setFont(font)
            fm = QFontMetrics(font)

    def _update_height(self):
        """부모 스크롤 → 그 부모(Window)로 자연스럽게 전파"""
        self.updateGeometry()
        pw = self.parentWidget()
        if pw:
            pw.updateGeometry()
            w = pw.window()
            if w:
                w.adjustSize()
                w.resize(w.width(), w.sizeHint().height())

    def toggle_desc(self):
        self.desc_box.setMaximumWidth(500)
        if self.desc_box.isVisible():
            self.desc_box.hide()
            self.desc_box.setMaximumHeight(0)
            self.btn_desc.setText("키워드 설명 보기")
        else:
            self.desc_box.show()
            self.desc_box.setMaximumHeight(16777215)
            self.btn_desc.setText("접기")

        self._update_height()

    def toggle_memo(self):
        self.memo_box.setMaximumWidth(500)
        if self.memo_box.isVisible():
            self.memo_box.hide()
            self.memo_box.setMaximumHeight(0)
            self.btn_memo.setText("암기법 보기")
        else:
            self.memo_box.show()
            self.memo_box.setMaximumHeight(16777215)
            self.btn_memo.setText("접기")

        self._update_height()
