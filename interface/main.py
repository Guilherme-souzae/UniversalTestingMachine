import sys
from frontend.styles import APP_STYLE

from PyQt6.QtWidgets import QApplication

from frontend.main_window import MainWindow
from backend.main_controller import MainController

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)
    
    controller = MainController()

    window = MainWindow(controller)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()