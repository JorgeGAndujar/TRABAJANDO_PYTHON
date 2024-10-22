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
        self.setFixedSize(600, 330) #Tamaño de la ventana ancho y altura
        self.setWindowTitle("Integrantes de la Seleccion") #Título para la ventana
        self.setStyleSheet("background-color: lightgray;") #Color de fondo para la ventana

        # Cambiar el icono de la ventana con una ruta absoluta que se crea a partir de una relativa
        ruta_relativa = "python6_ventana/icon.png"
        ruta_absoluta = os.path.abspath(ruta_relativa)
        print(ruta_absoluta) # F:\CURSOS\TRABAJANDO\PROJECTS___PYTHON\PYTHON_TEXTO\PYTHON\PYTHON_0033\cross1.png
        self.setWindowIcon(QIcon(ruta_absoluta))

    def personalizarComponentes(self):
        self.tblMostrar = QTableWidget(self)
        self.tblMostrar.setColumnCount(5)
        self.tblMostrar.setRowCount(0)
        self.tblMostrar.setHorizontalHeaderLabels(["ID", "NOMBRE", "APELLIDOS","EDAD","TIPO"])
        self.tblMostrar.horizontalHeader().setStyleSheet("color: black; background-color: white;")
        self.tblMostrar.verticalHeader().setStyleSheet("color: black; background-color: white;")
        self.tblMostrar.horizontalHeader().setFont(QFont("Courier New", 18, QFont.Bold)) #Fuente de letra y tamaño de letra de la cabecera
        self.tblMostrar.setFont(QFont("Courier New", 14)) #Fuente de letra y tamaño de letra del cuerpo
        self.tblMostrar.setGeometry(10, 10, 580, 307)

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
            self.tblMostrar.setItem(i, 4, QTableWidgetItem(str(objeto.__class__.__name__)))            
            #self.tblMostrar.setItem(i, 1, QTableWidgetItem(nombre[i]))
            #self.tblMostrar.setItem(i, 2, QTableWidgetItem(str(estatura[i])))
        '''
        # Almacenar el índice de la columna "ID" para ajustar la alineación al centro más tarde
        self.indice_id = 0 #self.indice_id = self.tblMostrar.horizontalHeader().visualIndex(0)
        # Almacenar el índice de la columna "ESTATURA" para ajustar la alineación a la derecha 
        self.indice_estatura = 2 #self.indice_estatura = self.tblMostrar.horizontalHeader().visualIndex(2)
        for i in range(self.tblMostrar.rowCount()):
            # Alinear la columna "ID" al centro
            item0 = self.tblMostrar.item(i, self.indice_id)
            item0.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            # Alinear la columna "ESTATURA" a la derecha
            item2 = self.tblMostrar.item(i, self.indice_estatura)
            item2.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        '''
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

id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
nombre = ["Luis", "Miguel", "Carlos", "Javier", "Carmen", "Maria", "Lucia", "Carmen", "Arturo", "Ismael", "Delly", "Vanessa", "Melissa", "Raul", "Arturo"]
estatura = [1.72, 1.73, 1.74, 1.75, 1.76, 1.60, 1.61, 1.62, 1.63, 1.64, 1.65, 1.56, 1.64, 1.67, 1.61]

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

              cursor.execute('SELECT * FROM Entrenador WHERE id_entrenador = ?',(id_seleccionfutbol,))
              resultado_t = cursor.fetchone()
              if resultado_t:
                 id_entrenador, id_federacion = resultado_t
                 seleccionfutbol_o = Entrenador(id_entrenador, nombre, apellidos, edad, id_federacion)
                 seleccionfutbol_lo.append(seleccionfutbol_o)

              cursor.execute('SELECT * FROM Masajista WHERE id_masajista = ?',(id_seleccionfutbol,))
              resultado_t = cursor.fetchone()
              if resultado_t:
                 id_masajista, titulacion, anio_experiencia = resultado_t
                 seleccionfutbol_o = Masajista(id_masajista, nombre, apellidos, edad, titulacion, anio_experiencia)
                 seleccionfutbol_lo.append(seleccionfutbol_o)
          print("OK: LISTA SELECCION FUTBOL")
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