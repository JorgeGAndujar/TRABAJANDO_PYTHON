import sys,os
from PySide6.QtWidgets import QMainWindow, QRadioButton, QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt
import ventana_entrenador as ve
import ventana_seleccionfutbol as vsf
import ventana_futbolista as vf
import ventana_masajista as vm
class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.personalizarVentana()
        self.personalizarComponentes()

    def personalizarVentana(self):
        self.setWindowTitle("VENTANA SELECCION FÚTBOL") # COLOCAR TITULO
        self.setFixedSize(480, 330)  # COLOCAR ANCHO Y ALTO DE LA VENTANA
        self.setStyleSheet("background-color: lightgray;") # COLOR DE LA VENTANA

        # Cambiar el icono de la ventana con una ruta absoluta que se crea a partir de una relativa
        ruta_relativa = "python6_ventana/cross1.png"
        ruta_absoluta = os.path.abspath(ruta_relativa)
        print(ruta_absoluta) # C:\TRABAJANDO_PYTHON\python6_ventana\cross1.png
        self.setWindowIcon(QIcon(ruta_absoluta))

        # Centrar la ventana en la pantalla
        self.pnlPrincipal = QWidget() # Crear un contenedor principal
        self.setCentralWidget(self.pnlPrincipal) # Establecer el contenedor principal para nuestra ventana
    

    def personalizarComponentes(self):
        self.lblTitulo = QLabel("SELECCIONE QUE TABLA REVISAR", self.pnlPrincipal) # crear objeto label
        self.lblTitulo.setFont(QFont("Courier New", 9)) # tipo de letra
        self.lblTitulo.setStyleSheet("background-color: black; color: yellow;")   # color fondo y letra
        self.lblTitulo.setAlignment(Qt.AlignCenter) # centrar titulo
        self.lblTitulo.setGeometry(0, 0, 480, 20) # dnd se situa (ubicación) lugar x, lugar y, distancia en pixeles y ancho en pixeles
        
        # SELECCION
        self.lblMostrarseleccionfutbol = QLabel("TABLA SELECCION DE FUTBOL", self.pnlPrincipal)
        self.lblMostrarseleccionfutbol.setFont(QFont("Courier New", 9))
        self.lblMostrarseleccionfutbol.setGeometry(30, 80, 200, 17)

        self.btoTablaSeleccion = QPushButton("SELECCION FUTBOL", self.pnlPrincipal)
        self.btoTablaSeleccion.setGeometry(235, 80, 120, 20)
        self.btoTablaSeleccion.setFont(QFont("Courier New", 8))
        self.btoTablaSeleccion.clicked.connect(self.abrirVentana1)
        
        # FUTBOLISTAS
        self.lblMostrarfutbolistas = QLabel("TABLA FUTBOLISTAS", self.pnlPrincipal)
        self.lblMostrarfutbolistas.setFont(QFont("Courier New", 9))
        self.lblMostrarfutbolistas.setGeometry(30, 120, 147, 17)

        self.btoTablaFutbolista = QPushButton("FUTBOLISTAS", self.pnlPrincipal)
        self.btoTablaFutbolista.setGeometry(235, 120, 120, 20)
        self.btoTablaFutbolista.setFont(QFont("Courier New", 8))
        self.btoTablaFutbolista.clicked.connect(self.abrirVentana2)
        
        # ENTRENADORES
        self.lblMostrarentrenadores = QLabel("TABLA ENTRENADORES", self.pnlPrincipal)
        self.lblMostrarentrenadores.setFont(QFont("Courier New", 9))
        self.lblMostrarentrenadores.setGeometry(30, 160, 147, 17)

        self.btoTablaEntrenador = QPushButton("ENTRENADOR", self.pnlPrincipal)
        self.btoTablaEntrenador.setGeometry(235, 160, 120, 20)
        self.btoTablaEntrenador.setFont(QFont("Courier New", 8))
        self.btoTablaEntrenador.clicked.connect(self.abrirVentana3)
        
        # MASAJISTAS
        self.lblMostrarmasajistas = QLabel("TABLA MASAJISTAS", self.pnlPrincipal)
        self.lblMostrarmasajistas.setFont(QFont("Courier New", 9))
        self.lblMostrarmasajistas.setGeometry(30, 200, 147, 17)

        self.btoTablaMasajista = QPushButton("MASAJISTA", self.pnlPrincipal)
        self.btoTablaMasajista.setGeometry(235, 200, 120, 20)
        self.btoTablaMasajista.setFont(QFont("Courier New", 8))
        self.btoTablaMasajista.clicked.connect(self.abrirVentana4)

        # SALIR
        self.btoSalir = QPushButton("SALIR", self.pnlPrincipal)
        self.btoSalir.setGeometry(290, 240, 80, 20)
        self.btoSalir.setFont(QFont("Courier New", 8))
        self.btoSalir.clicked.connect(self.salir)

    def abrirVentana1(self):
        self.btoTablaSeleccion = vsf.Ventana()
        self.btoTablaSeleccion.show()
    def abrirVentana2(self):
        self.btoTablaFutbolista = vf.Ventana()
        self.btoTablaFutbolista.show()
    def abrirVentana3(self):
        self.btoTablaEntrenador = ve.Ventana()
        self.btoTablaEntrenador.show()
    def abrirVentana4(self):
        self.btoTablaMasajista = vm.Ventana()
        self.btoTablaMasajista.show()

    
    def salir(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())