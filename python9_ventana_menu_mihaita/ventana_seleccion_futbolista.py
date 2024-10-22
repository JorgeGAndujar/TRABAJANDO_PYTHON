import sys,os,sqlite3
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt
from herencia_seleccionfutbol import SeleccionFutbol,Entrenador,Masajista,Futbolista

seleccionfutbol_lo = []

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.personalizarVentana()
        self.personalizarComponentes()
        self.cargarDatosTabla()
    
    def obtener_tabla(self):
        return self.tblMostrar

    def personalizarVentana(self):
        self.setFixedSize(800, 400) #Tamaño de la ventana ancho y altura
        self.setWindowTitle("Futbolistas") #Título para la ventana
        self.setStyleSheet("background-color: lightgray;") #Color de fondo para la ventana

        # Cambiar el icono de la ventana con una ruta absoluta que se crea a partir de una relativa
        ruta_relativa = "python6_ventana/icon.png"
        ruta_absoluta = os.path.abspath(ruta_relativa)
        print(ruta_absoluta) # F:\CURSOS\TRABAJANDO\PROJECTS___PYTHON\PYTHON_TEXTO\PYTHON\PYTHON_0033\cross1.png
        self.setWindowIcon(QIcon(ruta_absoluta))

    def personalizarComponentes(self):
        self.tblMostrar = QTableWidget(self)
        self.tblMostrar.setColumnCount(6)
        self.tblMostrar.setRowCount(0)
        self.tblMostrar.setHorizontalHeaderLabels(["ID", "NOMBRE", "APELLIDOS","EDAD","Dorsal", "Demarcacion"])
        self.tblMostrar.horizontalHeader().setStyleSheet("color: black; background-color: white;")
        self.tblMostrar.verticalHeader().setStyleSheet("color: black; background-color: white;")
        self.tblMostrar.horizontalHeader().setFont(QFont("Courier New", 15, QFont.Bold)) #Fuente de letra y tamaño de letra de la cabecera
        self.tblMostrar.setFont(QFont("Courier New", 12)) #Fuente de letra y tamaño de letra del cuerpo
        self.tblMostrar.setGeometry(10, 10, 780, 380)

        # Estilizar la tabla para que el texto de las celdas sea negro, la esquina tenga el mismo estilo que los encabezados y los bordes de las celdas sean consistentes
        self.tblMostrar.setStyleSheet("""
            QTableWidget {
                color: black;  /* Color del texto de las celdas */
                background-color: gray;  /* Color de fondo del cuerpo */
                gridline-color: lightgray;  /* Color de las líneas de la cuadrícula */
            }
            QHeaderView::section {
                color: black;  /* Color del texto del encabezado */
                background-color: white;  /* Color de fondo del encabezado */
                border: 1px solid lightgray;  /* Borde del encabezado */
            }
            QTableCornerButton::section {
                background-color: white;  /* Color de la esquina entre el encabezado horizontal y vertical */
                border: 1px solid lightgray;  /* Borde de la esquina */
            }
        """)

        header = self.tblMostrar.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)  # Ajustar automáticamente el ancho de las columnas
        header.setStretchLastSection(True) # Estirar la última sección (última columna) para llenar el espacio

    def cargarDatosTabla(self):
        self.limpiarTabla()
        seleccionfutbol_lo = obtener_lista_seleccionfutbol_objeto()
        for i,objeto in enumerate(seleccionfutbol_lo):
            self.tblMostrar.insertRow(i) #Añadir una nueva fila en blanco en la posición i: 0,1,2,3...14
            self.tblMostrar.setItem(i, 0, QTableWidgetItem(objeto.id_seleccionfutbol)) #Posición i: fila, 0: columna
            self.tblMostrar.setItem(i, 1, QTableWidgetItem(objeto.nombre))
            self.tblMostrar.setItem(i, 2, QTableWidgetItem(objeto.apellidos))
            self.tblMostrar.setItem(i, 3, QTableWidgetItem(str(objeto.edad)))
            self.tblMostrar.setItem(i, 4, QTableWidgetItem(str(objeto.dorsal)))
            self.tblMostrar.setItem(i, 5, QTableWidgetItem(objeto.demarcacion))
        
    def decimalesfijo(self,estatura):
        parte_entera = int(estatura)
        parte_decimal = estatura - parte_entera
        parte_decimal_1 = int(parte_decimal * 100)
        if parte_decimal_1 % 10 == 0:
           return str(estatura) + "0"
        else:
           return str(estatura)

    def limpiarTabla(self):
        self.tblMostrar.setRowCount(0)

def obtener_conexion():
    nra = "C:\\TRABAJANDO_PYTHON\\python9_ventana_menu_mihaita\\seleccionfutbol.sqlite3"
    conexion = None
    try:
       conexion = sqlite3.connect(nra)
    except sqlite3.Error as error:
       conexion = None
    return conexion

def obtener_lista_seleccionfutbol_objeto():
    conexion = obtener_conexion()
    if conexion != None:
       cursor = conexion.cursor()
       try:
          query_seleccionfutbol = "SELECT * FROM SeleccionFutbol" 
          cursor.execute(query_seleccionfutbol)
          seleccionfutbol_lt = cursor.fetchall()
          for seleccionfutbol_t in seleccionfutbol_lt:
              id_seleccionfutbol, nombre, apellidos, edad = seleccionfutbol_t

              cursor.execute('SELECT * FROM Futbolista WHERE id_futbolista = ?',(id_seleccionfutbol,))
              resultado_t = cursor.fetchone()
              if resultado_t:
                 id_futbolista, dorsal, demarcacion = resultado_t
                 seleccionfutbol_o = Futbolista(id_futbolista, nombre, apellidos, edad, dorsal, demarcacion)
                 seleccionfutbol_lo.append(seleccionfutbol_o)

          print("LISTA FUTBOLISTAS.")
          return seleccionfutbol_lo             
       except Exception as e:
          print("ERROR: SELECT ", e)
          return None
    else:
        print("ERROR: CONEXION")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())