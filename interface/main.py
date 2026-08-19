import sys
from PyQt6.QtCore import qInstallMessageHandler, QtMsgType
from frontend.styles import APP_STYLE

from PyQt6.QtWidgets import QApplication

from frontend.main_window import MainWindow
from backend.main_controller import MainController


def qt_message_filter(msg_type, context, message):
    # Ignora especificamente o warning de point size
    if "setPointSize" in message:
        return
    # Deixa passar qualquer outra mensagem normalmente
    if msg_type == QtMsgType.QtWarningMsg:
        print(f"Qt Warning: {message}")
    elif msg_type == QtMsgType.QtCriticalMsg:
        print(f"Qt Critical: {message}")
    elif msg_type == QtMsgType.QtFatalMsg:
        print(f"Qt Fatal: {message}")


def main():
    qInstallMessageHandler(qt_message_filter)

    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)

    controller = MainController()

    window = MainWindow(controller)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()