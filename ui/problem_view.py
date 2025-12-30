import re
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QSizePolicy,
    QHBoxLayout, QPushButton, QMenu, QAction
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
        
        # 태그별 설명
        self.tag_map = self.parse_tagged_description(safe_str(problem.description))

        # 🔹 태그 선택 버튼 (QMenu 기반)
        self.btn_tag_menu = create_quiz_button("태그 선택 ▼")
        layout.addWidget(self.btn_tag_menu)
        
        self.tag_menu = QMenu(self)
        self.tag_actions = {}
        
        for tag in self.tag_map.keys():
            action = QAction(tag, self)
            action.setCheckable(True)
            action.triggered.connect(lambda _, t=tag: self.on_tag_selected(t))
            self.tag_menu.addAction(action)
            self.tag_actions[tag] = action
        
        self.btn_tag_menu.setMenu(self.tag_menu)

        # 설명 버튼 + 텍스트
        self.btn_desc = create_quiz_button("설명 보기")
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
        
    def on_tag_selected(self, tag):
        # 다른 태그 체크 해제
        for t, act in self.tag_actions.items():
            act.setChecked(t == tag)
    
        # 설명 박스에 태그 내용 표시
        self.desc_box.setText(self.tag_map.get(tag, ""))
        self.desc_box.show()
        self.desc_box.setMaximumHeight(16777215)
    
        # 버튼 텍스트에 현재 태그 표시
        self.btn_tag_menu.setText(f"태그: {tag} ▼")
        self.btn_desc.setText("접기")
    
        self._update_height()
   
    def collapse_view(self):
        """설명/암기 영역을 모두 닫고 기본 높이로 복원"""
    
        # 설명 박스 닫기
        self.desc_box.hide()
        self.desc_box.setMaximumHeight(0)
        self.btn_desc.setText("설명 보기")
    
        # 암기법 박스 닫기
        self.memo_box.hide()
        self.memo_box.setMaximumHeight(0)
        self.btn_memo.setText("암기법 보기")
    
        # 태그 버튼 체크 해제
        for act in self.tag_actions.values():
            act.setChecked(False)
        
        self.btn_tag_menu.setText("태그 선택 ▼")
    
        # 높이 재계산
        self._update_height()
        
    def show_tag(self, tag):
        # 다른 태그 버튼 OFF
        for t, btn in self.tag_buttons.items():
            btn.setChecked(t == tag)
    
        # 설명 박스에 태그 내용만 표시
        self.desc_box.setText(self.tag_map.get(tag, ""))
        self.desc_box.show()
        self.desc_box.setMaximumHeight(16777215)
    
        self.btn_desc.setText("접기")
        self._update_height()

       
    def parse_tagged_description(self, text):
        """
        반환:
        {
          '정의': 'IT 서비스를 고객 가치 중심으로 관리',
          '목적': '서비스 품질 향상',
          '구성요소': 'SLA, SLM, KPI'
        }
        """
        result = {}
        matches = re.findall(r'\[(.*?)\]\s*(.*?)(?=\n\[|$)', text, re.S)
        for tag, content in matches:
            result[tag.strip()] = content.strip()
        return result
        
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
