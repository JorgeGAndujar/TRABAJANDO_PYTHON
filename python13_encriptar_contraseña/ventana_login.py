import sys
import os
import sqlite3
import bcrypt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QLineEdit, QPushButton, QMessageBox
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt
from ventana_insert_usuarios import Ventana as VentanaInsertUsuarios  # Importar la clase de la otra ventana
from ventana_insert_venta import Ventana as VentanaGastosDia
from ventana_insert_productos import Ventana as VentanaProdutos
from ventana_menu import Ventana as VentanaMenu

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.personalizarVentana()
        self.personalizarComponentes()

    def verificar_contrasena(self, contrasena_ingresada, contraseña_almacenada):
        """Verificar si la contraseña ingresada coincide con la almacenada."""
        return bcrypt.checkpw(contrasena_ingresada.encode(), contraseña_almacenada.encode())

    def obtener_conexion(self):
        """Conectar a la base de datos."""
        ruta_bd = "C:\\TRABAJANDO_PYTHON\\python13_encriptar_contraseña\\ferreteria.sqlite3"
        try:
            conexion = sqlite3.connect(ruta_bd)
            print("Conexión exitosa a la base de datos.")
            return conexion
        except sqlite3.Error as error:
            print(f"Error al conectar con la base de datos: {error}")
            return None

    def personalizarVentana(self):
        """Configurar las propiedades principales de la ventana."""
        self.setWindowTitle("LOGIN")
        self.setStyleSheet("background-color: lightgray;")
        self.setFixedSize(480, 330)

        ruta_relativa_icono = "python6_ventana/cross1.png"
        ruta_absoluta_icono = os.path.abspath(ruta_relativa_icono)
        self.setWindowIcon(QIcon(ruta_absoluta_icono))

        self.pnlPrincipal = QWidget()
        self.setCentralWidget(self.pnlPrincipal)

    def personalizarComponentes(self):
        """Agregar y personalizar los componentes de la ventana."""
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
        self.lblPassword.setFont(QFont("Courier New", 9))
        self.lblPassword.setStyleSheet("background-color: black; color:white;")
        self.lblPassword.setAlignment(Qt.AlignCenter)
        self.lblPassword.setGeometry(200, 140, 100, 20)

        self.txtPassword = QLineEdit(self.pnlPrincipal)
        self.txtPassword.setGeometry(200, 170, 100, 20)
        self.txtPassword.setFont(QFont("Courier New", 9))
        self.txtPassword.setAlignment(Qt.AlignCenter)
        self.txtPassword.setStyleSheet("color: blue;")
        self.txtPassword.setEchoMode(QLineEdit.Password)
        self.txtPassword.setPlaceholderText("INGRESE CLAVE")

        self.btoAceptar = QPushButton("ACEPTAR", self.pnlPrincipal)
        self.btoAceptar.setGeometry(200, 220, 100, 20)
        self.btoAceptar.setFont(QFont("Courier New", 8))
        self.btoAceptar.clicked.connect(self.botAceptarClic)

    def botAceptarClic(self):
        """Validar las credenciales ingresadas y abrir la ventana correspondiente."""
        usuario = self.txtLogin.text()
        contrasena = self.txtPassword.text()
        conexion = self.obtener_conexion()

        if conexion is not None:
            cursor = conexion.cursor()
            sql = "SELECT nombre_usuario, contrasena, rol FROM Usuario WHERE nombre_usuario = ?"
            cursor.execute(sql, (usuario,))
            resultado = cursor.fetchone()

            if resultado:
                nombre_usuario, contrasena_hashed, rol = resultado
                if self.verificar_contrasena(contrasena, contrasena_hashed):
                    QMessageBox.information(self, "Login correcto", f"Bienvenido, {rol} {nombre_usuario}!")
                    self.close()
                    self.abrirVentana(rol)
                else:
                    QMessageBox.critical(self, "Error", "Contraseña incorrecta.")
            else:
                QMessageBox.critical(self, "Error", "Usuario no encontrado.")
        else:
            QMessageBox.critical(self, "Error", "Error de conexión con la base de datos.")

    def abrirVentana(self, rol):
        """Abrir la ventana de acuerdo al rol del usuario."""
        if rol == "Administrador":
            self.ventana_menu = VentanaMenu()
            self.ventana_menu.show()   
        if rol == "Almacén":
            self.ventana_insert_productos = VentanaProdutos()
            self.ventana_insert_productos.show()
        if rol == "Cajero":
            self.ventana_insert_venta = VentanaGastosDia()
            self.ventana_insert_venta.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())
