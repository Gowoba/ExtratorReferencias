import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit, QFileDialog, QHBoxLayout, QLineEdit
from teste import listar_referencias  # Importando a função do teste.py
import PyPDF2
import pandas


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Extrator de Referencias')
        self.setGeometry(100, 100, 550, 300)

        self.layout = QVBoxLayout()
        self.h_layout = QHBoxLayout()

        self.button = QPushButton('Selecionar Pasta', self)
        self.button.setFixedSize(150, 40)
        self.button.clicked.connect(self.select_folder)
        self.h_layout.addWidget(self.button)

        self.path_display = QLineEdit(self)
        self.path_display.setReadOnly(True)
        self.h_layout.addWidget(self.path_display)

        self.layout.addLayout(self.h_layout)

        self.list_button = QPushButton('Listar Referências', self)
        self.list_button.setFixedSize(150, 40)
        self.list_button.clicked.connect(self.listar_referencias)  # Conectando o botão à função
        self.layout.addWidget(self.list_button)

        self.log = QTextEdit(self)
        self.log.setReadOnly(True)
        self.layout.addWidget(self.log)

        self.setLayout(self.layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Selecionar Pasta')
        if folder:
            self.path_display.setText(folder)
            self.log.append(f'Pasta selecionada: {folder}')

    def listar_referencias(self):
        folder_path = self.path_display.text()
        if not folder_path:
            self.log.append("Erro: Nenhuma pasta selecionada!")
            return

        try:
            referencias = listar_referencias(folder_path)  # Chama a função de teste.py
            self.log.append("Referências encontradas:")
            for ref in referencias:
                self.log.append(ref)
        except Exception as e:
            self.log.append(f"Erro ao listar referências: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
