import sys, os, sqlite3
from PySide6.QtWidgets import QMainWindow, QPushButton, QApplication, QWidget, QLabel
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt
from ventana_insert_productos import Ventana as vip
from ventana_insert_usuarios import Ventana as viu
from ventana_insert_venta import Ventana as viv


class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.personalizarVentana()
        self.personalizarComponentes()

    def personalizarVentana(self):
        self.setWindowTitle("MENU ADMINISTRADOR")
        self.setFixedSize(480, 330)
        self.setStyleSheet("background-color: lightgray;")

        ruta_relativa = "python6_ventana/cross1.png"
        ruta_absoluta = os.path.abspath(ruta_relativa)
        self.setWindowIcon(QIcon(ruta_absoluta))

        self.pnlPrincipal = QWidget()
        self.setCentralWidget(self.pnlPrincipal)

    def personalizarComponentes(self):
        # Etiqueta de título
        self.lblTitulo = QLabel("MENU ADMINISTRADOR", self.pnlPrincipal)
        self.lblTitulo.setFont(QFont("Courier New", 9))
        self.lblTitulo.setStyleSheet("background-color: black; color: yellow;")
        self.lblTitulo.setAlignment(Qt.AlignCenter)
        self.lblTitulo.setGeometry(0, 0, 480, 20)

        # Botón Usuarios
        self.btoUsuarios = QPushButton("USUARIOS", self.pnlPrincipal)
        self.btoUsuarios.setGeometry(100, 100, 100, 30)
        self.btoUsuarios.setFont(QFont("Courier New", 8))
        self.btoUsuarios.clicked.connect(lambda: self.abrirVentana("usuarios"))

        # Botón Almacén
        self.btoAlmacen = QPushButton("ALMACÉN", self.pnlPrincipal)
        self.btoAlmacen.setGeometry(200, 100, 100, 30)
        self.btoAlmacen.setFont(QFont("Courier New", 8))
        self.btoAlmacen.clicked.connect(lambda: self.abrirVentana("almacen"))

        # Botón Cajero
        self.btoCajero = QPushButton("CAJERO", self.pnlPrincipal)
        self.btoCajero.setGeometry(300, 100, 100, 30)
        self.btoCajero.setFont(QFont("Courier New", 8))
        self.btoCajero.clicked.connect(lambda: self.abrirVentana("cajero"))

        # Botón Salir
        self.btoSalir = QPushButton("SALIR", self.pnlPrincipal)
        self.btoSalir.setGeometry(200, 200, 100, 30)
        self.btoSalir.setFont(QFont("Courier New", 8))
        self.btoSalir.clicked.connect(self.salir)

    def abrirVentana(self, opcion):
        if opcion == "usuarios":
            self.ventana_insert_usuarios = viu()
            self.ventana_insert_usuarios.show()
        elif opcion == "almacen":
            self.ventana_insert_productos = vip()
            self.ventana_insert_productos.show()
        elif opcion == "cajero":
            self.ventana_insert_venta = viv()
            self.ventana_insert_venta.show()

    def salir(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())
