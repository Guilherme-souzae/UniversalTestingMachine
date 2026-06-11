APP_STYLE = """
QWidget {
    background-color: #2b2b2b;
    color: #ffffff;
    font-size: 14px;
}

/* GroupBox */
QGroupBox {
    border: 2px solid #444444;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 12px;

    font-size: 15px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 5px;
}

/* Botões padrão */
QPushButton {
    background-color: #3c3f41;
    border: 1px solid #555555;
    border-radius: 6px;

    padding: 8px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #4a4d50;
}

QPushButton:pressed {
    background-color: #2d2f31;
}

/* Botão conectar */
QPushButton#connectButton {
    background-color: #6c3483;
    color: white;
    font-size: 16px;
    letter-spacing: 1px;
}

QPushButton#connectButton:hover {
    background-color: #7d3c98;
}

QPushButton#connectButton:pressed {
    background-color: #512e5f;
}

QPushButton#connectButton:disabled {
    background-color: #3c3f41;
    color: #888888;
    border-color: #444444;
}

/* Botão iniciar ensaio */
QPushButton#startButton {
    background-color: #1e8449;
    color: white;
    font-size: 15px;
}

QPushButton#startButton:hover {
    background-color: #27ae60;
}

QPushButton#startButton:pressed {
    background-color: #145a32;
}

QPushButton#startButton:disabled {
    background-color: #3c3f41;
    color: #888888;
}

/* Botão pausar */
QPushButton#pauseButton {
    background-color: #d68910;
    color: white;
    font-size: 15px;
}

QPushButton#pauseButton:hover {
    background-color: #f39c12;
}

QPushButton#pauseButton:pressed {
    background-color: #9a6109;
}

QPushButton#pauseButton:disabled {
    background-color: #3c3f41;
    color: #888888;
}

/* Botão resetar */
QPushButton#resetButton {
    background-color: #717d7e;
    color: white;
    font-size: 15px;
}

QPushButton#resetButton:hover {
    background-color: #909497;
}

QPushButton#resetButton:pressed {
    background-color: #515a5a;
}

QPushButton#resetButton:disabled {
    background-color: #3c3f41;
    color: #888888;
}

/* Gráfico pyqtgraph */
PlotWidget {
    background-color: #1e1e1e;
    border: 1px solid #444444;
    border-radius: 6px;
}

/* Botão emergência */
QPushButton#emergencyButton {
    background-color: #d63031;
    color: white;
    font-size: 22px;
}

QPushButton#emergencyButton:hover {
    background-color: #e74c3c;
}

QPushButton#emergencyButton:pressed {
    background-color: #b71c1c;
}

/* Botão subir */
QPushButton#upButton {
    background-color: #27ae60;
    font-size: 16px;
}

QPushButton#upButton:hover {
    background-color: #2ecc71;
}

/* Botão descer */
QPushButton#downButton {
    background-color: #2980b9;
    font-size: 16px;
}

QPushButton#downButton:hover {
    background-color: #3498db;
}
"""