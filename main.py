import sys, os
from PyQt5.QtWidgets import QApplication
from ui.startup_window import StartupWindow
from ui.main_window import MainWindow

main_window_instance = None   # ← 전역에 보관할 변수

def resource_path(relative_path):
    """ PyInstaller 빌드 환경에서도 파일 경로를 안전하게 찾는 함수 """
    if hasattr(sys, '_MEIPASS'):     # frozen 상태
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main():
    global main_window_instance

    app = QApplication(sys.argv)

    # 스타일 적용
    style_file = resource_path("ui/style.qss")
    with open(style_file, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

    # 작은 창 실행
    startup = StartupWindow()
    startup.show()

    # 프로그램 시작 버튼 이벤트
    def start_program():
        global main_window_instance
        
        if startup.problems:
            main_window_instance = MainWindow(startup.problems)
            main_window_instance.show()
            startup.close()

    startup.btn_start.clicked.connect(start_program)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
