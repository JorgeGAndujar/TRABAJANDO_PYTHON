import sys, os
import bcrypt
import mysql.connector
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,QComboBox,
    QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt


class VentanaGestionUsuarios(QWidget):
    def __init__(self):
        super().__init__()
        self.personalizar_ventana()
        self.personalizar_componentes()
        self.cargar_datos()

    
    def personalizar_ventana(self):
        self.setWindowTitle("Gestión de Usuarios")  # Título para la ventana
        self.setFixedSize(600, 400)  # Tamaño de la ventana ancho y altura
        self.setStyleSheet("background-color: lightgray;")  # Color de fondo para la ventana

        # Cambiar el icono de la ventana con una ruta absoluta que se crea a partir de una relativa
        ruta_relativa = "python6_ventana/cross1.png"
        ruta_absoluta = os.path.abspath(ruta_relativa)
        #print(ruta_absoluta) # 
        self.setWindowIcon(QIcon(ruta_absoluta))

    def personalizar_componentes(self):
        layout = QVBoxLayout()

        # Tabla de Usuarios
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["NOMBRE USUARIO","CONTRASEÑA","ROL"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Campos para CRUD
        self.txt_nombre_usuario = QLineEdit()
        self.txt_nombre_usuario.setPlaceholderText("Nombre Usuario")

        self.txt_contrasena = QLineEdit()
        self.txt_contrasena.setPlaceholderText("Contraseña")

        self.cbo_rol = QComboBox()
        self.cbo_rol.setFont(QFont("Courier New", 8))
        self.cbo_rol.addItem("SELECCIONE ROL")
        self.cbo_rol.addItem("Administrador")
        self.cbo_rol.addItem("Cajero")
        self.cbo_rol.addItem("Almacén")

        self.txt_contrasena = QLineEdit()
        self.txt_contrasena.setPlaceholderText("Contraseña")
        
        # Botones para el CRUD
        self.btn_agregar_usuario = QPushButton("Agregar Usuario")
        self.btn_agregar_usuario.clicked.connect(self.agregar_usuario)
        self.btn_editar_usuario = QPushButton("Editar Usuario")
        self.btn_editar_usuario.clicked.connect(self.editar_usuario)
        self.btn_eliminar_usuario = QPushButton("Eliminar Usuario")
        self.btn_eliminar_usuario.clicked.connect(self.eliminar_usuario)
        layout_botones = QHBoxLayout()
        layout_botones.addWidget(self.btn_agregar_usuario)
        layout_botones.addWidget(self.btn_editar_usuario)
        layout_botones.addWidget(self.btn_eliminar_usuario)
        


        # AÑADIR AL ADMINISTRADOR, Poner el administrador principal a la ventana
        layout.addWidget(self.tabla)
        layout.addWidget(self.txt_nombre_usuario)
        layout.addWidget(self.txt_contrasena)
        layout.addWidget(self.cbo_rol)
        layout.addLayout(layout_botones)
        # AÑADO A LA VENTANA(SELF)
        self.setLayout(layout)
    
    def cargar_datos(self):
        conexion = self.obtener_conexion()
        if conexion != None:
            #QMessageBox.information(self, "OK", "Conexión.")
            try:
                cursor = conexion.cursor()
                query = "SELECT nombre_usuario,contrasena,rol FROM Usuario"
                cursor.execute(query)
                registros_lt = cursor.fetchall()
                self.tabla.setRowCount(len(registros_lt))
                for fila, registro_t in enumerate(registros_lt):
                    for columna, dato in enumerate(registro_t):
                        self.tabla.setItem(fila,columna, QTableWidgetItem(str(dato)))
            except Exception as e:
                QMessageBox.critical(self, "ERROR", "Query Select")    
        else:
           QMessageBox.critical(self, "ERROR", "Error de conexión con la base de datos.") 


    def obtener_conexion(self):
        conexion = None
        try:
            print("Intentando conectar a la base de datos...")
            conexion = mysql.connector.connect(
            host="localhost",
            port="3307",
            user="root",
            password="12345678",
            database="ferreteria")
            if conexion.is_connected():
               print("OK: CONEXION")
        except Exception as e:
            print(f"Error de conexión: {e}")
            conexion = None
        return conexion  # Retorna la conexión
    
    def agregar_usuario(self):
        conexion = self.obtener_conexion()
        if conexion != None:
            #QMessageBox.information(self, "OK", "Conexión.")
            try:
                cursor = conexion.cursor()
                query = """INSERT INTO Usuario(nombre_usuario, contrasena, rol)
                           VALUES (%s, %s, %s);"""
                nombre_usuario = self.txt_nombre_usuario.text()
                contrasena = self.txt_contrasena.text()
                rol = self.cbo_rol.currentText()

                if rol == "SELECCIONE ROL":
                    QMessageBox.warning(None, "Advertencia", "Debe seleccionar un rol válido.")
                    return

                cursor.execute(query, (nombre_usuario, self.encriptar_contrasena(contrasena), rol))
                conexion.commit()
                QMessageBox.information(None, "Información", "Usuario insertado correctamente.")
                self.cargar_datos()
                self.limpiar_campos_usuario()
               
            except Exception as e:
                QMessageBox.critical(self, "ERROR", "Query Insert.")
        else:
           QMessageBox.critical(self, "ERROR", "Error de conexión con la base de datos.")

    def encriptar_contrasena(self, contrasena):
        #CONVERTIR LA CONTRASEÑA A BYTE
        contrasena_byte = contrasena.encode()
        contrasena_hashed = bcrypt.hashpw(contrasena_byte, bcrypt.gensalt())
        return contrasena_hashed.decode() 

    def editar_usuario(self):
        conexion = self.obtener_conexion()
        if conexion != None:
            fila_seleccionada = self.tabla.currentRow()
            if fila_seleccionada != -1:
                nombre_usuario_buscar = self.tabla.item(fila_seleccionada,0).text()
                nombre_usuario_update = self.txt_nombre_usuario.text()
                contrasena_update = self.txt_contrasena.text()
                rol_update = self.cbo_rol.currentText()
                if len(nombre_usuario_update) > 0 and len (contrasena_update) > 0 \
                    and len(rol_update) > 0:
                    try:
                        cursor = conexion.cursor()
                        query = """UPDATE Usuario SET nombre_usuario = %s, contrasena = %s, rol = %s
                                   WHERE nombre_usuario = %s;"""
                        cursor.execute(query,(nombre_usuario_update,self.encriptar_contrasena(contrasena_update),rol_update,nombre_usuario_buscar))
                        conexion.commit()
                        QMessageBox.information(self, "OK", "Datos Actualizados")
                        self.cargar_datos()
                        self.limpiar_campos_usuario()

                    except Exception as e:
                        QMessageBox.critical(self, "ERROR", "Query Update.")
                else:
                    QMessageBox.warning(self, "Warning", "Debe llenar todos los campos del Usuario")
            else:
                QMessageBox.warning(self, "Warning", "Debe seleccionar")        
        else:
           QMessageBox.critical(self, "ERROR", "Error de conexión con la base de datos.") 

    def eliminar_usuario(self):
        conexion = self.obtener_conexion()
        if conexion is not None:  # Asegurarse de que la conexión no sea None
            fila_seleccionada = self.tabla.currentRow()
            if fila_seleccionada != -1:
                nombre_usuario_buscar = self.tabla.item(fila_seleccionada, 0).text()  # Obtener el nombre del usuario seleccionado
                try:
                    cursor = conexion.cursor()
                    # Consulta SQL corregida
                    query = "DELETE FROM Usuario WHERE nombre_usuario = %s;"
                    # Ejecutar la consulta con el nombre de usuario seleccionado
                    cursor.execute(query, (nombre_usuario_buscar,))
                    conexion.commit()  # Confirmar la transacción
                    QMessageBox.information(self, "OK", "Usuario eliminado exitosamente.")
                    # Actualizar los datos y limpiar los campos
                    self.cargar_datos()
                    self.limpiar_campos_usuario()
                except Exception as e:
                    # Mostrar el error con el mensaje detallado
                    QMessageBox.critical(self, "ERROR", f"Error al eliminar usuario: {str(e)}")      
            else:
                QMessageBox.warning(self, "Advertencia", "Por favor, selecciona un usuario para eliminar.")
        else:
            QMessageBox.critical(self, "ERROR", "Error de conexión con la base de datos.")

    def limpiar_campos_usuario(self):
        self.txt_nombre_usuario.clear() 
        self.txt_contrasena.clear()
        self.cbo_rol.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaGestionUsuarios()
    ventana.show()
    sys.exit(app.exec())


