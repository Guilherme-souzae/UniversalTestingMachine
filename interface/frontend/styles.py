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