import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox, QGroupBox, QGridLayout, QTabWidget, QCheckBox)
from PyQt6.QtCore import Qt, QTimer

from main_controller import MainController
from canvas_graph import GraficoCanvas
from styles import STYLESHEET

class MainWindow(QWidget):
    def __init__(self, controller: MainController):
        super().__init__()
        self.ctrl = controller

        self.ctrl.dados_recebidos.connect(self._on_dados)
        self.ctrl.ensaio_iniciado.connect(self._on_ensaio_iniciado)
        self.ctrl.ensaio_resetado.connect(self._on_ensaio_resetado)
        self.ctrl.referencia_salva.connect(self._on_referencia_salva)

        self.setWindowTitle("Sistema de Controle - Máquina de Ensaio de Tração")
        self.setGeometry(30, 30, 1300, 950)
        self.contador_ref = 0

        # Botões 
        self.setStyleSheet(STYLESHEET)
        
        main_layout = QVBoxLayout()
        
        # --- CABEÇALHO DE EMERGÊNCIA ---
        self.layout_emergencia = QHBoxLayout()
        self.btn_emergencia = QPushButton("EMERGÊNCIA")
        self.btn_emergencia.setCheckable(True)
        self.btn_emergencia.setStyleSheet("background-color: #ff4d4d; color: white; font-weight: bold; font-size: 22px; height: 60px;")
        self.btn_emergencia.toggled.connect(self.gerenciar_emergencia)
        
        self.btn_reiniciar = QPushButton("REINICIAR")
        self.btn_reiniciar.setStyleSheet("background-color: #3498db; color: white; font-weight: bold; height: 60px;")
        self.btn_reiniciar.hide()
        self.btn_reiniciar.clicked.connect(self._on_btn_reiniciar)
        
        self.layout_emergencia.addWidget(self.btn_emergencia, 4)
        self.layout_emergencia.addWidget(self.btn_reiniciar, 1)
        main_layout.addLayout(self.layout_emergencia)

        # Mensagem Pop-up Verde
        self.label_status = QLabel("")
        self.label_status.setStyleSheet("color: #00ff00; font-weight: bold; font-size: 15px;")
        self.label_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.label_status)
        
        self.abas = QTabWidget()
        self.aba_config = QWidget(); self.aba_relatorio = QWidget()
        self.abas.addTab(self.aba_config, "Configurações")
        self.abas.addTab(self.aba_relatorio, "Relatório e Gráficos")
        main_layout.addWidget(self.abas)
        
        self.setLayout(main_layout)
        self.montar_aba_config()
        self.montar_aba_relatorio()

    def gerenciar_emergencia(self, travado):
        self.abas.setEnabled(not travado)
        self.btn_reiniciar.setVisible(travado)
        if travado:
            self.btn_emergencia.setText("SISTEMA BLOQUEADO")
            self.btn_emergencia.setStyleSheet("background-color: #555555; color: #888888; font-weight: bold; font-size: 22px; height: 60px;")
        else:
            self.btn_emergencia.setText("EMERGÊNCIA")
            self.btn_emergencia.setStyleSheet("background-color: #ff4d4d; color: white; font-weight: bold; font-size: 22px; height: 60px;")

    def montar_aba_config(self):
        layout = QGridLayout()
        
        # 1. CONTROLE DAS GARRAS
        grupo_manual = QGroupBox("Controle das Garras (Ajuste Manual)")
        lay_manual = QVBoxLayout()
        lay_btns = QHBoxLayout()
        self.btn_subir = QPushButton("▲ SUBIR"); self.btn_descer = QPushButton("▼ DESCER")
        self.btn_subir.setObjectName("btn_seta"); self.btn_descer.setObjectName("btn_seta")

        self.btn_subir.clicked.connect(self._on_btn_subir)
        self.btn_descer.clicked.connect(self._on_btn_descer)

        lay_btns.addWidget(self.btn_subir); lay_btns.addWidget(self.btn_descer)
        lay_manual.addLayout(lay_btns)
        lay_manual.addWidget(QLabel("Velocidade Manual (mm/min):"))
        lay_manual.addWidget(QLineEdit("50"))
        
        lay_manual.addWidget(QLabel("Posições Salvas:"))
        self.combo_posicoes = QComboBox(); self.combo_posicoes.addItem("Referência Padrão")
        lay_manual.addWidget(self.combo_posicoes)
        
        self.btn_referenciar = QPushButton("Referenciar Posição e Velocidade")
        self.btn_referenciar.setObjectName("btn_referenciar")
        self.btn_referenciar.setEnabled(False)
        self.btn_referenciar.clicked.connect(self.salvar_referencia)
        lay_manual.addWidget(self.btn_referenciar)
        grupo_manual.setLayout(lay_manual)
        layout.addWidget(grupo_manual, 0, 0)

        # 2. PARADA FORÇADA (Restaurado e Esmaecendo) 
        grupo_parada = QGroupBox("Habilitar Parada Forçada por:")
        lay_parada = QVBoxLayout()
        self.check_forca = QCheckBox("Carga Máxima (Célula 20kg)")
        self.check_desloc = QCheckBox("Deslocamento Máximo (mm):")
        self.input_desloc = QLineEdit("350"); self.input_desloc.setEnabled(False)
        self.check_manual = QCheckBox("Sem Parada (Manual)")
        
        self.checks = [self.check_forca, self.check_desloc, self.check_manual]
        for cb in self.checks:
            cb.toggled.connect(self.logica_parada_exclusiva)
            lay_parada.addWidget(cb)
            if cb == self.check_desloc: lay_parada.addWidget(self.input_desloc)
            
        grupo_parada.setLayout(lay_parada)
        layout.addWidget(grupo_parada, 1, 0)

        # 3. GEOMETRIA E INDICADORES
        col2 = QVBoxLayout()
        grupo_geo = QGroupBox("Geometria da Amostra")
        lay_geo = QGridLayout()
        self.combo_tipo = QComboBox(); self.combo_tipo.addItems(["Retangular", "Tubo", "Cilíndrico"])
        lay_geo.addWidget(QLabel("Tipo:"), 0, 0); lay_geo.addWidget(self.combo_tipo, 0, 1)
        lay_geo.addWidget(QLabel("Base (mm):"), 1, 0); lay_geo.addWidget(QLineEdit("10"), 1, 1)
        grupo_geo.setLayout(lay_geo)
        col2.addWidget(grupo_geo)

        grupo_ind = QGroupBox("Indicadores para Relatório")
        lay_ind = QGridLayout()
        self.dict_indics = {}
        nomes = ["Força (N)", "Deslocamento", "Tempo", "Tensão (σ)", "Deformação (ε)", "Módulo Young (E)"]
        for i, nome in enumerate(nomes):
            cb = QCheckBox(nome); cb.setChecked(True)
            cb.toggled.connect(self.atualizar_visual_aba2)
            self.dict_indics[nome] = cb
            lay_ind.addWidget(cb, i//2, i%2)
        grupo_ind.setLayout(lay_ind)
        col2.addWidget(grupo_ind)
        
        layout.addLayout(col2, 0, 1, 2, 1)
        self.aba_config.setLayout(layout)

        # 4. CONEXÃO SERIAL
        grupo_serial = QGroupBox("Conexão Serial (Arduino)")
        lay_serial = QGridLayout()

        lay_serial.addWidget(QLabel("Porta (ex: COM3 ou /dev/ttyUSB0):"), 0, 0, 1, 2)

        self.input_porta = QLineEdit("COM3")
        self.input_porta.setPlaceholderText("Ex: COM3 ou /dev/ttyUSB0")
        lay_serial.addWidget(self.input_porta, 1, 0, 1, 2)

        self.btn_conectar = QPushButton("🔌 Conectar")
        self.btn_conectar.setObjectName("btn_iniciar")  # reutiliza estilo verde
        self.btn_conectar.clicked.connect(self._on_btn_conectar)

        self.btn_desconectar = QPushButton("✖ Desconectar")
        self.btn_desconectar.setObjectName("btn_resetar")  # reutiliza estilo vermelho
        self.btn_desconectar.setEnabled(False)
        self.btn_desconectar.clicked.connect(self._on_btn_desconectar)

        lay_serial.addWidget(self.btn_conectar, 2, 0)
        lay_serial.addWidget(self.btn_desconectar, 2, 1)

        self.label_conexao = QLabel("● Desconectado")
        self.label_conexao.setStyleSheet("color: #ff4d4d; font-weight: bold;")
        self.label_conexao.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay_serial.addWidget(self.label_conexao, 3, 0, 1, 2)

        grupo_serial.setLayout(lay_serial)
        layout.addWidget(grupo_serial, 2, 0)  # linha 2, coluna 0

    def salvar_referencia(self):
        self.contador_ref += 1
        nome = f"Referência {self.contador_ref}"
        self.combo_posicoes.addItem(nome); self.combo_posicoes.setCurrentText(nome)
        self.label_status.setText(f"✔ {nome} salva com sucesso!"); QTimer.singleShot(2500, lambda: self.label_status.setText(""))
        self.btn_referenciar.setEnabled(False)

    def logica_parada_exclusiva(self, marcado):
        sender = self.sender()
        if marcado:
            for cb in self.checks:
                if cb != sender: cb.setChecked(False); cb.setEnabled(False) # Esmaece pro user
            if sender == self.check_desloc: self.input_desloc.setEnabled(True)
        else:
            if not any(c.isChecked() for c in self.checks):
                for cb in self.checks: cb.setEnabled(True)
                self.input_desloc.setEnabled(False)

    def montar_aba_relatorio(self):
        layout_aba = QVBoxLayout()
        
        # Gráficos
        lay_grafs = QHBoxLayout()
        self.grafico1 = GraficoCanvas()
        self.grafico1.setStyleSheet("background: white; border: 1px solid gray;")
        self.grafico2 = GraficoCanvas()
        self.grafico2.setStyleSheet("background: white; border: 1px solid gray;")
        lay_grafs.addWidget(self.grafico1); lay_grafs.addWidget(self.grafico2)
        layout_aba.addLayout(lay_grafs, 6)
        
        # Resultados Numéricos
        self.grid_res = QGridLayout()
        self.res_widgets = {}
        for i, nome in enumerate(self.dict_indics.keys()):
            l_n = QLabel(f"{nome}:"); l_v = QLabel("---")
            l_v.setStyleSheet("background-color: #3d3d3d; color: #00ff00; padding: 4px; border: 1px solid #555;")
            self.grid_res.addWidget(l_n, i//3, (i%3)*2); self.grid_res.addWidget(l_v, i//3, (i%3)*2 + 1)
            self.res_widgets[nome] = (l_n, l_v)
        layout_aba.addLayout(self.grid_res, 1)
        
        # --- CONTROLES DE ENSAIO ---
        lay_controles = QHBoxLayout()
        
        self.btn_iniciar = QPushButton("INICIAR ENSAIO"); self.btn_iniciar.setObjectName("btn_iniciar")
        self.btn_pausar = QPushButton("PAUSAR"); self.btn_pausar.setObjectName("btn_pausar"); self.btn_pausar.setEnabled(False)
        self.btn_resetar = QPushButton("RESETAR"); self.btn_resetar.setObjectName("btn_resetar"); self.btn_resetar.setEnabled(False)
        self.btn_salvar = QPushButton("SALVAR"); self.btn_salvar.setObjectName("btn_salvar"); self.btn_salvar.setEnabled(False)
        
        self.btn_iniciar.clicked.connect(self._on_btn_ensaio)
        self.btn_resetar.clicked.connect(self._on_btn_rensaio)
        
        # Layout divide igualmente o espaço 
        for btn in [self.btn_iniciar, self.btn_pausar, self.btn_resetar, self.btn_salvar]:
            lay_controles.addWidget(btn)
            
        layout_aba.addLayout(lay_controles)
        self.aba_relatorio.setLayout(layout_aba)
        self.atualizar_visual_aba2()

    def atualizar_visual_aba2(self):
        for nome, cb in self.dict_indics.items():
            l_n, l_v = self.res_widgets[nome]
            ativo = cb.isChecked()
            l_n.setStyleSheet("color: white;" if ativo else "color: #444;")
            l_v.setStyleSheet(f"background: {'#3d3d3d' if ativo else '#2b2b2b'}; color: {'#00ff00' if ativo else '#333'}; padding: 4px; border: 1px solid #555;")

    # --- Reações a eventos do controller ---
    def _on_dados(self, x: float, y: float):
        print("plotando")
        self.grafico1.adicionar_ponto(x, y)
        self.grafico1.plotar()

    def _on_ensaio_iniciado(self):
        self.btn_iniciar.setEnabled(False)
        self.btn_pausar.setEnabled(True)
        self.btn_resetar.setEnabled(True)
        self.label_status.setText("▶ Ensaio em andamento...")

    def _on_ensaio_resetado(self):
        self.grafico1.resetar_grafico()
        self.grafico1.plotar()
        self.btn_iniciar.setEnabled(True)
        self.btn_pausar.setEnabled(False)
        self.btn_resetar.setEnabled(False)
        self.label_status.setText("↺ Sistema resetado.")
        QTimer.singleShot(2000, lambda: self.label_status.setText(""))

    def _on_referencia_salva(self, nome: str):
        self.combo_posicoes.addItem(nome)
        self.combo_posicoes.setCurrentText(nome)
        self.label_status.setText(f"✔ {nome} salva com sucesso!")
        QTimer.singleShot(2500, lambda: self.label_status.setText(""))
        self.btn_referenciar.setEnabled(False)

    # --- Comandos ---
    def _on_btn_subir(self):
        self.btn_referenciar.setEnabled(True)
        self.ctrl.subir()

    def _on_btn_descer(self):
        self.btn_referenciar.setEnabled(True)
        self.ctrl.descer()

    def _on_btn_reiniciar(self):
        self.btn_emergencia.setChecked(False)
        self.ctrl.reiniciar()

    def _on_btn_ensaio(self):
        self.ctrl.iniciar_ensaio()

    def _on_btn_rensaio(self):
        self.ctrl.resetar_ensaio()

    def _on_btn_conectar(self):
        porta = self.input_porta.text().strip()
        baud = 9600

        sucesso = self.ctrl.conectar_serial(porta, baud)

        if sucesso:
            self.label_conexao.setText("● Conectado")
            self.label_conexao.setStyleSheet("color: #00ff00; font-weight: bold;")
            self.btn_conectar.setEnabled(False)
            self.btn_desconectar.setEnabled(True)
            self.label_status.setText(f"✔ Conectado em {porta} @ {baud} bps")
            QTimer.singleShot(2500, lambda: self.label_status.setText(""))
        else:
            self.label_conexao.setText("● Falha na conexão")
            self.label_conexao.setStyleSheet("color: #ffaa00; font-weight: bold;")
            self.label_status.setText(f"✖ Não foi possível conectar em {porta}")
            QTimer.singleShot(3000, lambda: self.label_status.setText(""))

    def _on_btn_desconectar(self):
        self.ctrl.desconectar_serial()  # implemente no controller
        self.label_conexao.setText("● Desconectado")
        self.label_conexao.setStyleSheet("color: #ff4d4d; font-weight: bold;")
        self.btn_conectar.setEnabled(True)
        self.btn_desconectar.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = MainController()
    window = MainWindow(controller)
    window.show()
    sys.exit(app.exec())