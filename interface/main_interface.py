import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QLineEdit, QComboBox, 
                             QGroupBox, QGridLayout, QTabWidget, QCheckBox, QFrame)
from PyQt6.QtCore import Qt, QTimer

from uart_bridge import Arduino
from commands import Comando

class UniversalMaterialTestingSystem(QWidget):
    def __init__(self):
        super().__init__()

        self.arduino = Arduino("COM3", 9600)

        self.setWindowTitle("Sistema de Controle - Máquina de Ensaio de Tração")
        self.setGeometry(30, 30, 1300, 950)
        self.contador_ref = 0
        
        # Botões 
        self.setStyleSheet("""
            QWidget { background-color: #2b2b2b; color: #ffffff; font-family: 'Segoe UI'; }
            QGroupBox { font-weight: bold; border: 2px solid #555; margin-top: 15px; padding: 10px; border-radius: 5px; }
            
            /* Botões Gerais e de Relatório */
            QPushButton { border-radius: 5px; font-weight: bold; height: 50px; font-size: 14px; }
            QPushButton:disabled { background-color: #3d3d3d; color: #777; border: 1px solid #444; }

            /* Cores dos Botões de Relatório (SÓ ATIVAM QUANDO HABILITADOS) */
            QPushButton#btn_iniciar:enabled { background-color: #27ae60; color: white; }
            QPushButton#btn_pausar:enabled { background-color: #f39c12; color: white; }
            QPushButton#btn_resetar:enabled { background-color: #c0392b; color: white; }
            QPushButton#btn_salvar:enabled { background-color: #2980b9; color: white; }

            /* Estilo das Setas de Ajuste Manual (Simétricas) */
            QPushButton#btn_seta { background-color: #444; border: 1px solid #666; height: 80px; }
            QPushButton#btn_seta:pressed { background-color: #333; border: 2px solid #3498db; color: #3498db; }
            
            /* Botão de Referenciar: Estilo Sólido Garantido */
            QPushButton#btn_referenciar:enabled { background-color: #3498db; color: white; border: 1px solid #2980b9; }

            /* Checkboxes com sinal de CHECK (V) Branco */
            QCheckBox::indicator { width: 22px; height: 22px; border: 1px solid #777; border-radius: 4px; background-color: #3d3d3d; }
            QCheckBox::indicator:checked { background-color: #3498db; border-color: #3498db; }
            QCheckBox::indicator:checked:after { content: '✔'; color: white; font-weight: bold; position: absolute; left: 4px; top: 0px; }
            
            /* Efeito de Esmaecimento Visual */
            QCheckBox:disabled { color: #555; }
            QCheckBox::indicator:disabled { border-color: #444; background-color: #222; }
        """)
        
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
        self.btn_reiniciar.clicked.connect(self.comando_reiniciar)
        
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

        self.btn_subir.clicked.connect(self.comando_subir)
        self.btn_descer.clicked.connect(self.comando_descer)

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
        self.grafico1 = QFrame(); self.grafico1.setStyleSheet("background: white; border: 1px solid gray;")
        self.grafico2 = QFrame(); self.grafico2.setStyleSheet("background: white; border: 1px solid gray;")
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
        
        self.btn_iniciar.clicked.connect(self.comando_iniciar_ensaio)
        self.btn_resetar.clicked.connect(self.comando_resetar_ensaio)
        
        # Layout divide igualmente o espaço 
        for btn in [self.btn_iniciar, self.btn_pausar, self.btn_resetar, self.btn_salvar]:
            lay_controles.addWidget(btn)
            
        layout_aba.addLayout(lay_controles)
        self.aba_relatorio.setLayout(layout_aba)
        self.atualizar_visual_aba2()

    def iniciar_ensaio_processo(self):
        self.btn_iniciar.setEnabled(False)
        self.btn_pausar.setEnabled(True); self.btn_resetar.setEnabled(True); self.btn_salvar.setEnabled(True)
        self.label_status.setText("▶ Ensaio em andamento...")

    def resetar_ensaio_processo(self):
        self.btn_iniciar.setEnabled(True)
        self.btn_pausar.setEnabled(False); self.btn_resetar.setEnabled(False); self.btn_salvar.setEnabled(False)
        self.label_status.setText("↺ Sistema resetado.")
        QTimer.singleShot(2000, lambda: self.label_status.setText(""))

    def atualizar_visual_aba2(self):
        for nome, cb in self.dict_indics.items():
            l_n, l_v = self.res_widgets[nome]
            ativo = cb.isChecked()
            l_n.setStyleSheet("color: white;" if ativo else "color: #444;")
            l_v.setStyleSheet(f"background: {'#3d3d3d' if ativo else '#2b2b2b'}; color: {'#00ff00' if ativo else '#333'}; padding: 4px; border: 1px solid #555;")

    # Comandos
    def comando_subir(self):
        self.btn_referenciar.setEnabled(True)
        self.arduino.enviar_comando(Comando.SUBIR)

    def comando_descer(self):
        self.btn_referenciar.setEnabled(True)
        self.arduino.enviar_comando(Comando.DESCER)

    def comando_reiniciar(self):
        self.btn_emergencia.setChecked(False)
        self.arduino.enviar_comando(Comando.RESET)

    def comando_iniciar_ensaio(self):
        self.iniciar_ensaio_processo()
        self.arduino.enviar_comando(Comando.ENSAIO)

        self.timer_leitura = QTimer()
        self.timer_leitura.timeout.connect(self.arduino.ler_dados)
        self.timer_leitura.start(100)

    def comando_resetar_ensaio(self):
        self.resetar_ensaio_processo()
        self.arduino.enviar_comando(Comando.R_ENSAIO)
        self.timer_leitura.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UniversalMaterialTestingSystem()
    window.show()
    sys.exit(app.exec())