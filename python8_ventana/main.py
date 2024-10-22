import sys
import os
import sqlite3
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt
from herencia_seleccion_futbol import SeleccionFutbol, Entrenador, Masajista, Futbolista

# Variable global para almacenar los objetos de la selección de fútbol
seleccionfutbol_lo = []

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.personalizarVentana()
        self.personalizarComponentes()

    def personalizarVentana(self):
        self.setFixedSize(600, 400)  # Aumentamos el tamaño de la ventana
        self.setWindowTitle("Ventana de Selección de Fútbol")  # Título para la ventana
        self.setStyleSheet("background-color: lightgray;")  # Color de fondo para la ventana

        # Cambiar el icono de la ventana
        ruta_relativa = "python8_ventana/cross1.png"
        ruta_absoluta = os.path.abspath(ruta_relativa)
        print(ruta_absoluta)  # Solo para verificar la ruta
        self.setWindowIcon(QIcon(ruta_absoluta))

    def personalizarComponentes(self):
        # Creamos los botones para seleccionar las categorías
        self.btnSeleccionFutbol = QPushButton("Seleccion de Futbol", self)
        self.btnEntrenador = QPushButton("Entrenador", self)
        self.btnFutbolista = QPushButton("Futbolista", self)
        self.btnMasajista = QPushButton("Masajista", self)

        # Conectamos los botones a las funciones correspondientes
        self.btnSeleccionFutbol.clicked.connect(self.mostrarSeleccionFutbol)
        self.btnEntrenador.clicked.connect(self.mostrarEntrenador)
        self.btnFutbolista.clicked.connect(self.mostrarFutbolista)
        self.btnMasajista.clicked.connect(self.mostrarMasajista)

        # Creamos la tabla donde se mostrarán los datos
        self.tblMostrar = QTableWidget(self)
        self.tblMostrar.setColumnCount(5)
        self.tblMostrar.setHorizontalHeaderLabels(["ID", "Nombre", "Apellidos", "Edad", "Roll"])
        self.tblMostrar.setStyleSheet("background-color: lightgray;")
        self.tblMostrar.setGeometry(10, 100, 580, 270)  # Posición y tamaño de la tabla
        self.tblMostrar.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Creamos el layout
        layout = QVBoxLayout()

        # Agregamos los botones al layout
        boton_layout = QHBoxLayout()
        boton_layout.addWidget(self.btnSeleccionFutbol)
        boton_layout.addWidget(self.btnEntrenador)
        boton_layout.addWidget(self.btnFutbolista)
        boton_layout.addWidget(self.btnMasajista)

        layout.addLayout(boton_layout)
        layout.addWidget(self.tblMostrar)

        # Creamos un QWidget central
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def mostrarSeleccionFutbol(self):
        self.cargarDatosTabla("SeleccionFutbol")

    def mostrarEntrenador(self):
        self.cargarDatosTabla("Entrenador")

    def mostrarFutbolista(self):
        self.cargarDatosTabla("Futbolista")

    def mostrarMasajista(self):
        self.cargarDatosTabla("Masajista")

    def cargarDatosTabla(self, tipo):
        self.limpiarTabla()  # Limpiamos la tabla antes de cargar nuevos datos
        global seleccionfutbol_lo
        seleccionfutbol_lo.clear()
        seleccionfutbol_lo = obtener_lista_seleccionfutbol_objeto()
        j = 0
        for objeto in seleccionfutbol_lo:
            if tipo == "SeleccionFutbol" or tipo == objeto.__class__.__name__:
                self.tblMostrar.insertRow(j)
                self.tblMostrar.setItem(j, 0, QTableWidgetItem(str(objeto.id_seleccionfutbol)))
                self.tblMostrar.setItem(j, 1, QTableWidgetItem(objeto.nombre))
                self.tblMostrar.setItem(j, 2, QTableWidgetItem(objeto.apellidos))
                self.tblMostrar.setItem(j, 3, QTableWidgetItem(str(objeto.edad)))
                self.tblMostrar.setItem(j, 4, QTableWidgetItem(objeto.__class__.__name__))
                j = j + 1

    def limpiarTabla(self):
        self.tblMostrar.setRowCount(0)

def obtener_conexion():
    nra = "C:\\TRABAJANDO_PYTHON\\python8_ventana\\seleccionfutbol.sqlite3"
    conexion = None
    try:
        conexion = sqlite3.connect(nra)
    except sqlite3.Error as error:
        conexion = None
    return conexion


def obtener_lista_seleccionfutbol_objeto():
    seleccionfutbol_lo.clear()  # Limpiar lista global antes de cargar nuevos objetos
    conexion = obtener_conexion()
    if conexion != None:
        cursor = conexion.cursor()
        try:
            query_seleccionfutbol = "SELECT * FROM SeleccionFutbol"
            cursor.execute(query_seleccionfutbol)
            seleccionfutbol_lt = cursor.fetchall()
            for seleccionfutbol_t in seleccionfutbol_lt:
                id_seleccionfutbol, nombre, apellidos, edad = seleccionfutbol_t

                cursor.execute('SELECT * FROM Futbolista WHERE id_futbolista = ?', (id_seleccionfutbol,))
                resultado_t = cursor.fetchone()
                if resultado_t:
                    id_futbolista, dorsal, demarcacion = resultado_t
                    seleccionfutbol_o = Futbolista(id_futbolista, nombre, apellidos, edad, dorsal, demarcacion)
                    seleccionfutbol_lo.append(seleccionfutbol_o)

                cursor.execute('SELECT * FROM Entrenador WHERE id_entrenador = ?', (id_seleccionfutbol,))
                resultado_t = cursor.fetchone()
                if resultado_t:
                    id_entrenador, id_federacion = resultado_t
                    seleccionfutbol_o = Entrenador(id_entrenador, nombre, apellidos, edad, id_federacion)
                    seleccionfutbol_lo.append(seleccionfutbol_o)

                cursor.execute('SELECT * FROM Masajista WHERE id_masajista = ?', (id_seleccionfutbol,))
                resultado_t = cursor.fetchone()
                if resultado_t:
                    id_masajista, titulacion, anio_experiencia = resultado_t
                    seleccionfutbol_o = Masajista(id_masajista, nombre, apellidos, edad, titulacion, anio_experiencia)
                    seleccionfutbol_lo.append(seleccionfutbol_o)

            print("OK: LISTA SELECCION FUTBOL")

            return seleccionfutbol_lo
        except Exception as e:
            print("ERROR: SELECT", e)

    else:
        print("ERROR: CONEXION")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())