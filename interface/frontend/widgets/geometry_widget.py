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

import math


class GeometryWidget(QWidget):

    # =========================================================
    # Sinais
    # =========================================================

    comprimento_alterado = pyqtSignal(float)  # metros
    area_alterada = pyqtSignal(float)         # metros quadrados

    def __init__(self):
        super().__init__()

        group = QGroupBox("Geometria da Amostra")

        # =====================================================
        # Tipo de seção
        # =====================================================

        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["Retangular", "Circular"])
        self.combo_tipo.setObjectName("tipoGeometriaCombo")

        self.combo_tipo.currentTextChanged.connect(
            self._on_tipo_changed
        )

        # =====================================================
        # Comprimento
        # =====================================================

        self.edit_comprimento = QLineEdit("100")
        self.edit_comprimento.setObjectName("comprimentoEdit")

        self.label_comprimento = QLabel("Comprimento (mm):")

        self.edit_comprimento.textChanged.connect(
            self._on_comprimento_changed
        )

        # =====================================================
        # Campos: Retangular
        # =====================================================

        self.edit_base = QLineEdit("10")
        self.edit_altura = QLineEdit("10")

        self.edit_base.setObjectName("baseEdit")
        self.edit_altura.setObjectName("alturaEdit")

        self.label_base = QLabel("Base (mm):")
        self.label_altura = QLabel("Altura (mm):")

        self.edit_base.textChanged.connect(
            self._on_geometria_changed
        )

        self.edit_altura.textChanged.connect(
            self._on_geometria_changed
        )

        # =====================================================
        # Campo: Circular
        # =====================================================

        self.edit_diametro = QLineEdit("10")
        self.edit_diametro.setObjectName("diametroEdit")

        self.label_diametro = QLabel("Diâmetro (mm):")

        self.edit_diametro.textChanged.connect(
            self._on_geometria_changed
        )

        # =====================================================
        # Layout
        # =====================================================

        self.form_layout = QFormLayout()

        self.form_layout.addRow("Tipo:", self.combo_tipo)

        self.form_layout.addRow(
            self.label_comprimento,
            self.edit_comprimento
        )

        self.form_layout.addRow(
            self.label_base,
            self.edit_base
        )

        self.form_layout.addRow(
            self.label_altura,
            self.edit_altura
        )

        self.form_layout.addRow(
            self.label_diametro,
            self.edit_diametro
        )

        group_layout = QVBoxLayout()
        group_layout.addLayout(self.form_layout)

        group.setLayout(group_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(group)

        self.setLayout(main_layout)

        # Estado inicial
        self._on_tipo_changed(
            self.combo_tipo.currentText()
        )

        # Emite os valores iniciais
        self._on_comprimento_changed(
            self.edit_comprimento.text()
        )

        self._on_geometria_changed()

    # =========================================================
    # Eventos
    # =========================================================

    def _on_comprimento_changed(self, texto):
        try:
            comprimento_mm = float(texto)

            if comprimento_mm > 0:
                comprimento_m = comprimento_mm / 1000.0

                self.comprimento_alterado.emit(comprimento_m)

        except ValueError:
            pass

    def _on_geometria_changed(self, *_):
        area = self.area_secao()

        if area is not None and area > 0:
            self.area_alterada.emit(area)

    def _on_tipo_changed(self, tipo):
        """Mostra apenas os campos relevantes para o tipo."""

        is_retangular = tipo == "Retangular"

        self.label_base.setVisible(is_retangular)
        self.edit_base.setVisible(is_retangular)

        self.label_altura.setVisible(is_retangular)
        self.edit_altura.setVisible(is_retangular)

        self.label_diametro.setVisible(not is_retangular)
        self.edit_diametro.setVisible(not is_retangular)

        # O tipo também altera a área
        self._on_geometria_changed()

    # =========================================================
    # Métodos públicos
    # =========================================================

    def tipo_selecionado(self):
        return self.combo_tipo.currentText()

    def comprimento(self):
        """
        Retorna o comprimento em metros.
        O campo de entrada é informado em mm.
        """

        try:
            comprimento_mm = float(
                self.edit_comprimento.text()
            )

            return comprimento_mm / 1000.0

        except ValueError:
            return None

    def area_secao(self):
        """
        Retorna a área da seção transversal em m².

        Os valores informados nos campos são em mm.
        """

        try:
            if self.tipo_selecionado() == "Retangular":

                base_mm = float(self.edit_base.text())
                altura_mm = float(self.edit_altura.text())

                area_mm2 = base_mm * altura_mm

            else:

                diametro_mm = float(self.edit_diametro.text())
                raio_mm = diametro_mm / 2.0

                area_mm2 = math.pi * raio_mm ** 2

            # mm² -> m²
            return area_mm2 / 1_000_000.0

        except ValueError:
            return None