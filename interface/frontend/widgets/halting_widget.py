from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QGroupBox,
    QCheckBox,
    QLineEdit,
    QVBoxLayout,
)


class HaltingWidget(QWidget):

    # Sinais
    carga_maxima_toggled = pyqtSignal(bool)
    deslocamento_maximo_toggled = pyqtSignal(bool)
    deslocamento_maximo_changed = pyqtSignal(str)
    sem_parada_toggled = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        group = QGroupBox("Habilitar Parada Forçada por:")

        self.chk_carga_maxima = QCheckBox("Carga Máxima (Célula 20kg)")
        self.chk_deslocamento_maximo = QCheckBox("Deslocamento Máximo (mm):")
        self.edit_deslocamento_maximo = QLineEdit("350")
        self.chk_sem_parada = QCheckBox("Sem Parada (Manual)")

        self.chk_carga_maxima.setObjectName("cargaMaximaCheck")
        self.chk_deslocamento_maximo.setObjectName("deslocamentoMaximoCheck")
        self.edit_deslocamento_maximo.setObjectName("deslocamentoMaximoEdit")
        self.chk_sem_parada.setObjectName("semParadaCheck")

        self.chk_carga_maxima.toggled.connect(self.carga_maxima_toggled.emit)
        self.chk_deslocamento_maximo.toggled.connect(self.deslocamento_maximo_toggled.emit)
        self.edit_deslocamento_maximo.textChanged.connect(self.deslocamento_maximo_changed.emit)
        self.chk_sem_parada.toggled.connect(self.sem_parada_toggled.emit)

        deslocamento_layout = QVBoxLayout()
        deslocamento_layout.addWidget(self.chk_deslocamento_maximo)
        deslocamento_layout.addWidget(self.edit_deslocamento_maximo)

        group_layout = QVBoxLayout()
        group_layout.addWidget(self.chk_carga_maxima)
        group_layout.addLayout(deslocamento_layout)
        group_layout.addWidget(self.chk_sem_parada)

        group.setLayout(group_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(group)

        self.setLayout(main_layout)