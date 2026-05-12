STYLESHEET = """
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
        """