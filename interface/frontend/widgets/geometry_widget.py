from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QGroupBox,
    QComboBox,
    QLineEdit,
    QLabel,
    QVBoxLayout,
    QFormLayout,
)


class GeometryWidget(QWidget):

    # Sinais
    tipo_alterado = pyqtSignal(str)
    base_alterada = pyqtSignal(str)
    altura_alterada = pyqtSignal(str)
    diametro_alterado = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        group = QGroupBox("Geometria da Amostra")

        # --- Tipo de seção ---
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["Retangular", "Circular"])
        self.combo_tipo.setObjectName("tipoGeometriaCombo")
        self.combo_tipo.currentTextChanged.connect(self._on_tipo_changed)
        self.combo_tipo.currentTextChanged.connect(self.tipo_alterado.emit)

        # --- Campos: Retangular ---
        self.edit_base = QLineEdit("10")
        self.edit_altura = QLineEdit("10")
        self.edit_base.setObjectName("baseEdit")
        self.edit_altura.setObjectName("alturaEdit")
        self.edit_base.textChanged.connect(self.base_alterada.emit)
        self.edit_altura.textChanged.connect(self.altura_alterada.emit)

        self.label_base = QLabel("Base (mm):")
        self.label_altura = QLabel("Altura (mm):")

        # --- Campo: Circular ---
        self.edit_diametro = QLineEdit("10")
        self.edit_diametro.setObjectName("diametroEdit")
        self.edit_diametro.textChanged.connect(self.diametro_alterado.emit)
        self.label_diametro = QLabel("Diâmetro (mm):")

        # --- Layout em formulário ---
        self.form_layout = QFormLayout()
        self.form_layout.addRow("Tipo:", self.combo_tipo)
        self.form_layout.addRow(self.label_base, self.edit_base)
        self.form_layout.addRow(self.label_altura, self.edit_altura)
        self.form_layout.addRow(self.label_diametro, self.edit_diametro)

        group_layout = QVBoxLayout()
        group_layout.addLayout(self.form_layout)
        group.setLayout(group_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(group)
        self.setLayout(main_layout)

        # Estado inicial: esconde campos que não pertencem ao tipo padrão
        self._on_tipo_changed(self.combo_tipo.currentText())

    def _on_tipo_changed(self, tipo):
        """Mostra apenas os campos relevantes para o tipo de seção selecionado."""
        is_retangular = tipo == "Retangular"

        self.label_base.setVisible(is_retangular)
        self.edit_base.setVisible(is_retangular)
        self.label_altura.setVisible(is_retangular)
        self.edit_altura.setVisible(is_retangular)

        self.label_diametro.setVisible(not is_retangular)
        self.edit_diametro.setVisible(not is_retangular)

    def tipo_selecionado(self):
        return self.combo_tipo.currentText()

    def area_secao(self):
        """Calcula a área da seção transversal (mm²) com base no tipo selecionado."""
        import math

        try:
            if self.tipo_selecionado() == "Retangular":
                base = float(self.edit_base.text())
                altura = float(self.edit_altura.text())
                return base * altura
            else:
                diametro = float(self.edit_diametro.text())
                raio = diametro / 2
                return math.pi * raio ** 2
        except ValueError:
            return None