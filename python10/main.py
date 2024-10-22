import sys, sqlite3
from PySide6.QtWidgets import QCalendarWidget, QMessageBox, QComboBox, QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt, QDate
def obtener_conexion():
    nra = "C:\\TRABAJANDO_PYTHON\\python10\\persona.sqlite3"
    conexion = None
    try:
        conexion = sqlite3.connect(nra)
        print("OK: CONEXION")
    except sqlite3.Error as error:
        conexion = None
    return conexion

def insertar(nombre,apellido,sexo,fecha_nacimiento):
    conexion = obtener_conexion()
    if conexion != None:
        QMessageBox.information(None,"OK","CONEXION")
        try:
            cursor = conexion.cursor()
            query = "INSERT INTO Persona (nombre,apellido,sexo,fecha_nacimiento) VALUES(?,?,?,?);"
            registro_t = (nombre,apellido,sexo,fecha_nacimiento)
            cursor.execute(query, registro_t)
            conexion.commit()
            QMessageBox.information(None,"OK","INSERT")
        except Exception as e:
               QMessageBox.critical(None,"ERROR","INSERT")
    else:
       QMessageBox.critical(None,"ERROR","CONEXION") 

def obtener_datos():
    nombre = txtNombre.text()
    apellido = txtApellido.text()
    sexo = cboSexo.currentText()
    fecha_nacimiento = txtNacimiento.text()
    bandera = False
    if sexo == 'Seleccione':
       QMessageBox.critical(None,"ERROR","DEBE SELECCIONAR SU SEXO")
    elif sexo == 'Hombre':
       sexo = 'H'; bandera = True
    else:
       sexo = 'M'; bandera = True
    if bandera == True:
       insertar(nombre,apellido,sexo,fecha_nacimiento)
    QMessageBox.information(None,"OK","DATOS CORRECTOS")
       

def mostrarFechaSeleccionada(fecha):
        fecha_str = "{:02d}/{:02d}/{:04d}".format(fecha.day(), fecha.month(), fecha.year())   
        txtNacimiento.setText(fecha_str)

# 0. CONSTRUIR UNA APLICACIÓN
app = QApplication(sys.argv) #<------------------------INICIO

# 1. CREAR LA VENTANA PRINCIPAL
ventana_principal = QMainWindow() # CONTRUIR UN OBJETO

# 2. CREAR UN PANEL QWIDGET
panel = QWidget()

# 3. CREAR UN ADMINISTRADOR(layout) DE PANEL(QWIDGET)
layoutGrid = QGridLayout() #<--- PERMITE ADMINISTRAR LOS ELEMENTOS DEL PANEL

# 4. CREAR COMPONENTES Y GESTIONARLOS CON EL ADMINISTRADOR
lblNombre = QLabel("Nombre?")
txtNombre = QLineEdit()
layoutGrid.addWidget(lblNombre,0,0) # <-- LE DAS UN LUGAR
layoutGrid.addWidget(txtNombre,0,1)

lblApellido = QLabel("Apellido?")
txtApellido = QLineEdit()
layoutGrid.addWidget(lblApellido,1,0) # <-- COORDENADAS
layoutGrid.addWidget(txtApellido,1,1)

calendario = QCalendarWidget()
calendario.setGridVisible(True)
calendario.setGeometry(10, 10, 460, 250)
layoutGrid.addWidget(calendario,5,1)
calendario.clicked[QDate].connect(mostrarFechaSeleccionada) #1 
txtNacimiento = QLineEdit()
layoutGrid.addWidget(txtNacimiento,6,1)

cboSexo = QComboBox()
cboSexo.addItem("Seleccione")
cboSexo.addItem("Hombre")
cboSexo.addItem("Mujer")
layoutGrid.addWidget(cboSexo,2,1)

btnEnviar = QPushButton("ENVIAR")
btnEnviar.clicked.connect(obtener_datos)
layoutGrid.addWidget(btnEnviar,7,1)

# 5. ASIGNAR EL ADMINNISTRADOR AL PANEL
panel.setLayout(layoutGrid)

# 6. PONER EN EL PANEL LA VENTANA PRINCIPAL
ventana_principal.setCentralWidget(panel)

# 7. MOSTRAR LA VENTANA PRINCIPAL
ventana_principal.show() # MUESTRAS

# 8. EJECUTAR APLICACIÓN
sys.exit(app.exec()) #<------------------------EJECUTA LA APLICACIÓN