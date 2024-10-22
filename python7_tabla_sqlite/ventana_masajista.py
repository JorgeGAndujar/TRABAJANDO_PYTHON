import sys, os, sqlite3
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout, QWidget
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt
from herencia_seleccionfutbol import SelecionFutbol, Entrenador, Masajista, Futbolista

seleccionfutbol_lo = []

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.personalizarVentana()
        self.personalizarComponentes()
        self.cargarDatosTabla()

    def personalizarVentana(self):
        self.setFixedSize(800, 400)  # Tamaño de la ventana, ahora más espaciosa
        self.setWindowTitle("MASAJISTA")  # Título para la ventana
        self.setStyleSheet("background-color: lightgray;")  # Color de fondo para la ventana

        # Cambiar el icono de la ventana con una ruta absoluta
        ruta_relativa = "python6_ventana/cross1.png"
        ruta_absoluta = os.path.abspath(ruta_relativa)
        self.setWindowIcon(QIcon(ruta_absoluta))

    def personalizarComponentes(self):
        # Crear un widget central para la ventana
        widgetCentral = QWidget(self)
        self.setCentralWidget(widgetCentral)

        # Crear un layout vertical para gestionar el espacio
        layout = QVBoxLayout()

        # Crear la tabla
        self.tblMostrar = QTableWidget(self)
        self.tblMostrar.setColumnCount(6)  # Número de columnas
        self.tblMostrar.setHorizontalHeaderLabels(["ID", "NOMBRE", "APELLIDOS", "EDAD", "TITULACION", "AÑOS EXPERIENCIA"])  # Cabecera
        self.tblMostrar.horizontalHeader().setStyleSheet("color: black; background-color: white;")
        self.tblMostrar.horizontalHeader().setFont(QFont("Courier New", 9, QFont.Bold))  # Fuente de la cabecera
        self.tblMostrar.setFont(QFont("Courier New", 9))  # Fuente para el cuerpo de la tabla
        self.tblMostrar.setStyleSheet("background-color: lightgray;")  # Color de fondo
        self.tblMostrar.setSizeAdjustPolicy(QTableWidget.AdjustToContents)  # Ajustar el tamaño de las celdas
        self.tblMostrar.setEditTriggers(QTableWidget.NoEditTriggers)  # Desactivar la edición de la tabla

        # Añadir la tabla al layout
        layout.addWidget(self.tblMostrar)

        # Asignar el layout al widget central
        widgetCentral.setLayout(layout)

        # Ajustar el comportamiento de las columnas
        header = self.tblMostrar.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)  # Ajustar el ancho de las columnas automáticamente

    def cargarDatosTabla(self):
        self.limpiarTabla()
        
        seleccionfutbol_lo = obtener_lista_seleccionfutbol_objeto()  # Obtener los objetos de la base de datos

        for i, objeto in enumerate(seleccionfutbol_lo):
            self.tblMostrar.insertRow(i)  # Añadir una nueva fila en la posición i: 0,1,2...
            self.tblMostrar.setItem(i, 0, QTableWidgetItem(objeto.id_seleccionfutbol))  # Columna 0
            self.tblMostrar.setItem(i, 1, QTableWidgetItem(objeto.nombre))  # Columna 1
            self.tblMostrar.setItem(i, 2, QTableWidgetItem(objeto.apellidos))  # Columna 2
            self.tblMostrar.setItem(i, 3, QTableWidgetItem(str(objeto.edad)))  # Columna 3
            self.tblMostrar.setItem(i, 4, QTableWidgetItem(objeto.titulacion))  # Columna 4
            self.tblMostrar.setItem(i, 5, QTableWidgetItem(str(objeto.anio_experiencia)))  # Columna 5

    def limpiarTabla(self):
        self.tblMostrar.setRowCount(0)  # Limpiar todas las filas

def obtener_conexion():
    nra = "C:\\TRABAJANDO_PYTHON\\python7_tabla_sqlite\\seleccionfutbol.sqlite3"
    conexion = None
    try:
        conexion = sqlite3.connect(nra)
        print("OK: CONEXION")
    except sqlite3.Error as error:
        print("ERROR: CONEXION", error)
    return conexion

def obtener_lista_seleccionfutbol_objeto():
    conexion = obtener_conexion()
    seleccionfutbol_lo = []  # Lista local de objetos (no global)
    if conexion is not None:
        cursor = conexion.cursor()
        try:
            query_seleccionfutbol = "SELECT * FROM Seleccionfutbol"
            cursor.execute(query_seleccionfutbol)
            seleccionfutbol_lt = cursor.fetchall()  # Obtener los datos de la base de datos

            for seleccionfutbol_t in seleccionfutbol_lt:
                id_seleccionfutbol, nombre, apellidos, edad = seleccionfutbol_t
                cursor.execute('SELECT * FROM Masajista WHERE id_masajista = ?', (id_seleccionfutbol,))
                resultado_t = cursor.fetchone()
                if resultado_t:
                    id_masajista, titulacion, anio_experiencia = resultado_t
                    seleccionfubol_o = Masajista(id_masajista, nombre, apellidos, edad, titulacion, anio_experiencia)
                    seleccionfutbol_lo.append(seleccionfubol_o)
            print("OK: LISTA DE SELECCION FUTBOL")
            return seleccionfutbol_lo
        except Exception as e:
            print("ERROR: SELECT", e)
            return []
    else:
        print("ERROR: CONEXION")
        return []

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())
