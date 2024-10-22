import sys, os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt
import ventana_seleccion_entrenador as entrenador
import ventana_seleccion_futbolista as futbolista
import ventana_seleccion_masajista as masajista
import ventana_seleccionfutbol as seleccionfutbol


class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.personalizarVentana()
        self.personalizarComponentes()

    def personalizarVentana(self):
        self.setWindowTitle("Menu")
        self.setStyleSheet("color: black;background-color: lightgray;")
        self.setFixedSize(480, 380)

        # Configuración del ícono
        ruta_relativa = "python6_ventana/cross1.png"
        ruta_absoluta = os.path.abspath(ruta_relativa)
        self.setWindowIcon(QIcon(ruta_absoluta))

        self.pnlPrincipal = QWidget()
        self.setCentralWidget(self.pnlPrincipal)
    
    def personalizarComponentes(self):
        # Botón para Entrenador
        self.btnEntrenador = QPushButton("Entrenador", self.pnlPrincipal)
        self.btnEntrenador.setGeometry(150, 50, 180, 40)
        self.btnEntrenador.setFont(QFont("Courier New", 14, QFont.Bold))
        self.btnEntrenador.clicked.connect(self.abrirVentanaEntrenador)

        # Botón para Futbolista
        self.btnFutbolista = QPushButton("Futbolista", self.pnlPrincipal)
        self.btnFutbolista.setGeometry(150, 110, 180, 40)
        self.btnFutbolista.setFont(QFont("Courier New", 14, QFont.Bold))
        self.btnFutbolista.clicked.connect(self.abrirVentanaFutbolista)

        # Botón para Masajista
        self.btnMasajista = QPushButton("Masajista", self.pnlPrincipal)
        self.btnMasajista.setGeometry(150, 170, 180, 40)
        self.btnMasajista.setFont(QFont("Courier New", 14, QFont.Bold))
        self.btnMasajista.clicked.connect(self.abrirVentanaMasajista)

        # Botón para Selección de Fútbol
        self.btnSeleccionFutbol = QPushButton("Seleccion Futbol", self.pnlPrincipal)
        self.btnSeleccionFutbol.setGeometry(150, 230, 180, 40)
        self.btnSeleccionFutbol.setFont(QFont("Courier New", 14, QFont.Bold))
        self.btnSeleccionFutbol.clicked.connect(self.abrirVentanaSeleccionFutbol)

        # Botón para Salir
        self.btnSalir = QPushButton("Salir", self.pnlPrincipal)
        self.btnSalir.setGeometry(150, 290, 180, 40)
        self.btnSalir.setFont(QFont("Courier New", 14, QFont.Bold))
        self.btnSalir.clicked.connect(self.close)
        

    # Métodos para abrir las ventanas
    def abrirVentanaEntrenador(self):
        self.ventanaEntrenador = entrenador.Ventana()
        self.ventanaEntrenador.show()

    def abrirVentanaFutbolista(self):
        self.ventanaFutbolista = futbolista.Ventana()
        self.ventanaFutbolista.show()

    def abrirVentanaMasajista(self):
        self.ventanaMasajista = masajista.Ventana()
        self.ventanaMasajista.show()

    def abrirVentanaSeleccionFutbol(self):
        self.ventanaSeleccionFutbol = seleccionfutbol.Ventana()
        self.ventanaSeleccionFutbol.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())