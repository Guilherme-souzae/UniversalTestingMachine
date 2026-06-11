from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)

class TestWidget(QWidget):
    
    # Sinais
    start_clicked = pyqtSignal()
    pause_clicked = pyqtSignal()
    reset_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.btn_start = QPushButton("INICIAR ENSAIO")
        self.btn_pause = QPushButton("PAUSAR")
        self.btn_reset = QPushButton("RESETAR")

        self.btn_start.setObjectName("startButton")
        self.btn_pause.setObjectName("pauseButton")
        self.btn_reset.setObjectName("resetButton")

        self.btn_start.clicked.connect(self.start_clicked.emit)
        self.btn_pause.clicked.connect(self.pause_clicked.emit)
        self.btn_reset.clicked.connect(self.reset_clicked.emit)

        self.btn_start.setMinimumHeight(50)
        self.btn_pause.setMinimumHeight(50)
        self.btn_reset.setMinimumHeight(50)

        controls_layout = QHBoxLayout()

        controls_layout.addWidget(self.btn_start)
        controls_layout.addWidget(self.btn_pause)
        controls_layout.addWidget(self.btn_reset)

        main_layout = QVBoxLayout()

        main_layout.addLayout(controls_layout)

        self.setLayout(main_layout)