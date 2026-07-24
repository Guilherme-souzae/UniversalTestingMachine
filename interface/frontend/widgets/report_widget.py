from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QGroupBox,
    QCheckBox,
    QVBoxLayout,
    QGridLayout,
)

class ReportWidget(QWidget):

    # Sinais
    indicador_alterado = pyqtSignal(str, bool)

    def __init__(self):
        super().__init__()

        group = QGroupBox("Indicadores para Relatório")

        self.chk_forca = QCheckBox("Força (N)")
        self.chk_deslocamento = QCheckBox("Deslocamento")
        self.chk_tempo = QCheckBox("Tempo")
        self.chk_tensao = QCheckBox("Tensão (σ)")
        self.chk_deformacao = QCheckBox("Deformação (ε)")
        self.chk_modulo_young = QCheckBox("Módulo Young (E)")

        self.chk_forca.setObjectName("forcaCheck")
        self.chk_deslocamento.setObjectName("deslocamentoCheck")
        self.chk_tempo.setObjectName("tempoCheck")
        self.chk_tensao.setObjectName("tensaoCheck")
        self.chk_deformacao.setObjectName("deformacaoCheck")
        self.chk_modulo_young.setObjectName("moduloYoungCheck")

        # Todos marcados por padrão (conforme imagem)
        self._checkboxes = {
            "forca": self.chk_forca,
            "deslocamento": self.chk_deslocamento,
            "tempo": self.chk_tempo,
            "tensao": self.chk_tensao,
            "deformacao": self.chk_deformacao,
            "modulo_young": self.chk_modulo_young,
        }

        for nome, chk in self._checkboxes.items():
            chk.setChecked(True)
            chk.toggled.connect(
                lambda estado, nome=nome: self.indicador_alterado.emit(nome, estado)
            )

        # Layout em grade: 2 colunas, 3 linhas (igual à imagem)
        group_layout = QGridLayout()
        group_layout.addWidget(self.chk_forca, 0, 0)
        group_layout.addWidget(self.chk_deslocamento, 0, 1)
        group_layout.addWidget(self.chk_tempo, 1, 0)
        group_layout.addWidget(self.chk_tensao, 1, 1)
        group_layout.addWidget(self.chk_deformacao, 2, 0)
        group_layout.addWidget(self.chk_modulo_young, 2, 1)

        group.setLayout(group_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(group)

        self.setLayout(main_layout)