__version__ = "0.1"
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QIcon, QPalette, QColor 
from PyQt5.QtCore import Qt

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Clave fija para propósitos de demostración (32 bytes para AES-256)
fixed_key = b'12345678901234567890123456789012'

# Encriptar el archivo
def encrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        data = file.read()

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    with open(file_path + '.enc', 'wb') as file:
        file.write(iv + encrypted_data)

# Desencriptar el archivo
def decrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        iv = file.read(16)
        encrypted_data = file.read()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()

    with open(file_path[:-4], 'wb') as file:
        file.write(data)

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.filechooser = QPushButton('Seleccionar Archivo')
        self.filechooser.setStyleSheet("background-color:rgb(122, 119, 119); border-radius: 20px;")  # Color de fondo y bordes redondeados
        self.filechooser.clicked.connect(self.select_file)
        self.layout.addWidget(self.filechooser)

        self.button_encrypt = QPushButton('Encriptar')
        self.button_encrypt.setStyleSheet("background-color: blue; color: white; border-radius: 10px;")  # Color azul y bordes redondeados
        self.button_encrypt.clicked.connect(self.encrypt_file)
        self.layout.addWidget(self.button_encrypt)

        self.button_decrypt = QPushButton('Desencriptar')
        self.button_decrypt.setStyleSheet("background-color: red; color: white; border-radius: 10px;")  # Color rojo y bordes redondeados
        self.button_decrypt.clicked.connect(self.decrypt_file)
        self.layout.addWidget(self.button_decrypt)

        self.result_label = QLabel('')
        self.layout.addWidget(self.result_label)

        self.setLayout(self.layout)
        self.setWindowIcon(QIcon('/home/Kenoxys/Descargas/Proyecto-Encrit/icon.png'))

    def select_file(self):
        options = QFileDialog.Options()
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo", "", "All Files (*)", options=options)
        if self.file_path:
            self.result_label.setText(f"Archivo seleccionado: {self.file_path}")

    def encrypt_file(self):
        if hasattr(self, 'file_path') and self.file_path:
            if os.path.isfile(self.file_path):
                encrypt_file(self.file_path, fixed_key)
                self.result_label.setText("Archivo encriptado correctamente")
            else:
                self.result_label.setText("Error: El elemento seleccionado no es un archivo.")
        else:
            self.result_label.setText("Por favor, selecciona un archivo primero")

    def decrypt_file(self):
        if hasattr(self, 'file_path') and self.file_path:
            if self.file_path.endswith(".enc"):
                decrypt_file(self.file_path, fixed_key)
                self.result_label.setText("Archivo desencriptado (si el proceso fue exitoso)")
            else:
                self.result_label.setText("El archivo no tiene la extensión .enc")
        else:
            self.result_label.setText("Por favor, selecciona un archivo encriptado")

if __name__ == '__main__':
    app = QApplication([])
    window = MyApp()
    window.setWindowTitle('Encriptar/Desencriptar Archivo')
    window.resize(400, 200)
    window.show()
    app.exec_()
