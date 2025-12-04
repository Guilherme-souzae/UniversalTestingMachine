# --- main_interface.py ---

import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QLabel, QLineEdit, QPushButton, 
                             QGridLayout)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt

# 1. CLASSE PRINCIPAL DA MÁQUINA DE TRAÇÃO
class UniversalTestingMachineGUI(QWidget):
    """
    Define a janela principal da interface da Máquina de Tração.
    Herdando de QWidget, é a base para a nossa interface.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Máquina de Ensaio de Tração Universal - Didática')
        self.setWindowIcon(QIcon('icon.png')) # Você pode adicionar um ícone depois!
        self.resize(800, 600)  # Define um tamanho inicial para a janela
        
        # Chama a função para configurar o layout e os componentes
        self.init_ui()

    def init_ui(self):
        # Layout principal que organizará a janela
        main_layout = QVBoxLayout(self)

        # 2. CABEÇALHO/TÍTULO
        title_label = QLabel('Sistema de Controle de Tração Didática')
        title_font = QFont('Arial', 24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Linha divisória
        main_layout.addSpacing(20)

        # 3. ÁREA DE CONTROLES E VISUALIZAÇÃO (Grid Layout para organização)
        control_area = QGridLayout()
        
        # --- Seção 3.1: Configurações do Ensaio ---
        control_area.addWidget(QLabel("### Configurações"), 0, 0)
        
        # Exemplo de componente: Campo de entrada para o nome da amostra
        control_area.addWidget(QLabel("Nome da Amostra:"), 1, 0)
        self.sample_name_input = QLineEdit()
        self.sample_name_input.setPlaceholderText("Ex: Aço 1045")
        control_area.addWidget(self.sample_name_input, 1, 1)

        # --- Seção 3.2: Controles da Máquina ---
        self.start_button = QPushButton("INICIAR ENSAIO")
        self.start_button.setFont(QFont('Arial', 12))
        self.start_button.setStyleSheet("background-color: green; color: white;")
        control_area.addWidget(self.start_button, 2, 0, 1, 2) # Ocupa 1 linha, 2 colunas

        main_layout.addLayout(control_area)
        
        # 4. RODAPÉ (Status)
        self.status_label = QLabel("Status: Pronto para configurar...")
        main_layout.addWidget(self.status_label)


# 5. FUNÇÃO DE INICIALIZAÇÃO DO PROGRAMA
if __name__ == '__main__':
    # Cria uma instância da aplicação PyQt
    app = QApplication(sys.argv)
    
    # Cria uma instância da nossa janela principal
    main_window = UniversalTestingMachineGUI()
    
    # Mostra a janela
    main_window.show()
    
    # Inicia o loop principal da aplicação (Onde o programa espera por eventos)
    sys.exit(app.exec())