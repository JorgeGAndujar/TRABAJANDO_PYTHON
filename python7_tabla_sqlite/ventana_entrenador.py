import sys,os,sqlite3
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView
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
        self.setFixedSize(600, 330) #Tamaño de la ventana ancho y altura
        self.setWindowTitle("ENTRENADOR") #Título para la ventana
        self.setStyleSheet("background-color: lightgray;") #Color de fondo para la ventana

        # Cambiar el icono de la ventana con una ruta absoluta que se crea a partir de una relativa
        ruta_relativa = "python6_ventana/cross1.png"
        ruta_absoluta = os.path.abspath(ruta_relativa)
        print(ruta_absoluta) # C:\TRABAJANDO_PYTHON\python6_ventana\cross1.png
        self.setWindowIcon(QIcon(ruta_absoluta))

    def personalizarComponentes(self):
        self.tblMostrar = QTableWidget(self) # hacer una tabla
        self.tblMostrar.setColumnCount(5) # columnas
        self.tblMostrar.setRowCount(0) # filas
        self.tblMostrar.setHorizontalHeaderLabels(["ID","NOMBRE","APELLIDOS","EDAD","ID FEDERACIÓN"]) # cabecera
        self.tblMostrar.horizontalHeader().setStyleSheet("color: black; background-color: white;")
        self.tblMostrar.horizontalHeader().setFont(QFont("Courier New", 9, QFont.Bold)) #Fuente de letra y tamaño de letra de la cabecera
        self.tblMostrar.setFont(QFont("Courier New", 9)) #Fuente de letra y tamaño de letra del cuerpo
        self.tblMostrar.setStyleSheet("background-color: lightgray;") #Color de fondo del cuerpo
        self.tblMostrar.setGeometry(10, 10, 580, 307)

        header = self.tblMostrar.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)  # Ajustar automáticamente el ancho de las columnas
        header.setStretchLastSection(True)  # Estirar la última sección (última columna) para llenar el espacio PROPORCIONA

    def cargarDatosTabla(self):
        self.limpiarTabla()
        
        seleccionfutbol_lo = obtener_lista_seleccionfutbol_objeto()

              
        for i,objeto in enumerate(seleccionfutbol_lo):
            self.tblMostrar.insertRow(i) #Añadir una nueva fila en blanco en la posición i: 0,1,2,3...14
            self.tblMostrar.setItem(i, 0, QTableWidgetItem(objeto.id_seleccionfutbol)) #Posición i: fila, 0: columna
            self.tblMostrar.setItem(i, 1, QTableWidgetItem(objeto.nombre))
            self.tblMostrar.setItem(i, 2, QTableWidgetItem(objeto.apellidos))
            self.tblMostrar.setItem(i, 3, QTableWidgetItem(str(objeto.edad)))
            self.tblMostrar.setItem(i, 4, QTableWidgetItem(str(objeto.id_federacion)))

    def limpiarTabla(self):
        self.tblMostrar.setRowCount(0)

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
    if conexion != None:
       cursor = conexion.cursor() 
       try:
           query_seleccionfutbol = "SELECT * FROM Seleccionfutbol"
           cursor.execute(query_seleccionfutbol)
           seleccionfutbol_lt = cursor.fetchall() #siempre regresa en lista de tuplas y con el cursor lo recuperas
           # HACER UN FOR PARA SACAR CADA TUPLA
           for seleccionfutbol_t in seleccionfutbol_lt:
               id_seleccionfutbol, nombre, apellidos, edad = seleccionfutbol_t
               cursor.execute('SELECT * FROM Entrenador WHERE id_entrenador = ?',(id_seleccionfutbol,))
               resultado_t = cursor.fetchone()
               if resultado_t:
                  id_entrenador, id_federacion = resultado_t
                  seleccionfubol_o = Entrenador(id_entrenador, nombre, apellidos, edad, id_federacion )
                  seleccionfutbol_lo.append(seleccionfubol_o)
                  

           print("OK: LISTA DE SELECCION FUTBOL")
           return seleccionfutbol_lo
       except Exception as e:
           print("ERROR: SELECT",e)    
           return None
    else:
        print("ERROR: CONEXION")    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())