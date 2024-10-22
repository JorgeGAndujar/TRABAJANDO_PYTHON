import sys, os
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QLineEdit, QPushButton, QMessageBox, QMenu
from PySide6.QtGui import QIcon, QFont, QAction
from PySide6.QtCore import Qt
import ventana_pyside6_2 as v
# OTRA FORMA
# from ventana_pyside6_2 import *

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.personalizarVentana()
        self.personalizarComponentes()

    def personalizarVentana(self):
        self.setWindowTitle("VENTANA PYSIDE6")
        self.setStyleSheet("background-color: lightgray;")
        self.setFixedSize(480, 330) # Ubicar la ventana en el centro de la pantalla no se puede redimensionar la ventana 

        ruta_relativa = "python6_ventana/cross1.png"
        ruta_absoluta = os.path.abspath(ruta_relativa)
        print(ruta_absoluta) # C:\TRABAJANDO_PYTHON\python6_ventana\cross1.png
        self.setWindowIcon(QIcon(ruta_absoluta))

        self.pnlPrincipal = QWidget() # Crear un contenedor
        self.setCentralWidget(self.pnlPrincipal) # Establecer el contenedor como principal para nuestra ventana
    
    def personalizarComponentes(self):
        self.lblLogin = QLabel("LOGIN", self.pnlPrincipal)
        self.lblLogin.setFont(QFont("Courier New", 9))
        self.lblLogin.setStyleSheet("background-color: black; color:white;")
        self.lblLogin.setAlignment(Qt.AlignCenter)
        self.lblLogin.setGeometry(200, 80, 100, 20)

        self.txtLogin = QLineEdit(self.pnlPrincipal)
        self.txtLogin.setGeometry(200, 110, 100, 20)
        self.txtLogin.setFont(QFont("Courier New", 9))
        self.txtLogin.setAlignment(Qt.AlignCenter)
        self.txtLogin.setStyleSheet("color: blue;")
        self.txtLogin.setPlaceholderText("INGRESE LOGIN") 

        self.lblPassword = QLabel("PASSWORD", self.pnlPrincipal)
        self.lblPassword.setFont(QFont("Courier New",9))
        self.lblPassword.setStyleSheet("background-color: black; color:white;")
        self.lblPassword.setAlignment(Qt.AlignCenter)
        self.lblPassword.setGeometry(200, 140, 100, 20)


        self.txtPassword = QLineEdit(self.pnlPrincipal)
        self.txtPassword.setGeometry(200, 170, 100, 20)
        self.txtPassword.setFont(QFont("Courier New",9))
        self.txtPassword.setAlignment(Qt.AlignCenter)
        self.txtPassword.setStyleSheet("color: blue;")  
        self.txtPassword.setEchoMode(QLineEdit.Password)
        self.txtPassword.setPlaceholderText("INGRESE CLAVE") # PONER EN GRIS LO Q TIENES Q INGRESAR
        self.txtPassword.setMaxLength(8) # PONER UN TOPE DE CARACTERES

        self.btoAceptar = QPushButton("ACEPTAR", self.pnlPrincipal)
        self.btoAceptar.setGeometry(200, 220, 100, 20)
        self.btoAceptar.setFont(QFont("Courier New", 8))
        self.btoAceptar.clicked.connect(self.botAceptarClic)    

    def botAceptarClic(self):
        login = self.txtLogin.text()
        password = self.txtPassword.text()
        if login == 'JORGE' and password == '12345678':
            QMessageBox.information(self, 'LOGIN CORRECTO', 'BIENVENIDO, ' + login + '!')
            self.close()
            self.abrirVentana()
        else:
            QMessageBox.warning(self, 'LOGIN INCORRECTO', 'LOGIN O PASSWORD INVALIDO')   

    def abrirVentana(self):
        self.ventana_sumar_button = v.Ventana()
        self.ventana_sumar_button.show()
        # self.objeto = Ventana
        # self.objeto

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())