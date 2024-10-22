import sys, os
import bcrypt
import mysql.connector
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox,
    QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt
from ventana_principal import VentanaPrincipal

class VentanaLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.personalizar_ventana()
        self.personalizar_componentes()
    

    def personalizar_ventana(self):
        self.setWindowTitle("Gestión de Usuarios")  # Título para la ventana
        self.setFixedSize(400, 200)  # Tamaño de la ventana ancho y altura
        self.setStyleSheet("background-color: lightgray;")  # Color de fondo para la ventana

        # Cambiar el icono de la ventana con una ruta absoluta que se crea a partir de una relativa
        ruta_relativa = "python6_ventana/cross1.png"
        ruta_absoluta = os.path.abspath(ruta_relativa)
        #print(ruta_absoluta) # 
        self.setWindowIcon(QIcon(ruta_absoluta))

    def personalizar_componentes(self):
        self.lbl_nombre_usuario = QLabel("Usuario")
        self.lbl_contrasena = QLabel("Contraseña")
        
        self.txt_nombre_usuario = QLineEdit()
        self.txt_contrasena = QLineEdit()
        self.txt_contrasena.setEchoMode(QLineEdit.Password)

        self.btn_loguin = QPushButton("Iniciar Sesión")
        self.btn_loguin.clicked.connect(self.validar_credenciales)

        layout_principal = QVBoxLayout()
        layout_principal.addWidget(self.lbl_nombre_usuario)
        layout_principal.addWidget(self.txt_nombre_usuario)
        layout_principal.addWidget(self.lbl_contrasena)
        layout_principal.addWidget(self.txt_contrasena)
        layout_principal.addWidget(self.btn_loguin)

        self.setLayout(layout_principal)

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
    
    
    def validar_credenciales(self):
        conexion = self.obtener_conexion()
        if conexion != None:
           try: 
               nombre_usuario = self.txt_nombre_usuario.text()
               contrasena = self.txt_contrasena.text()
               cursor = conexion.cursor()
               query = "SELECT contrasena, rol FROM Usuario Where nombre_usuario = %s"
               cursor.execute(query, (nombre_usuario,))
               resultado_t = cursor.fetchone()
               if resultado_t:
                  contrasena_hash,rol = resultado_t
                  if bcrypt.checkpw(contrasena.encode(), contrasena_hash.encode()):
                    self.abrir_ventana_principal(rol) 
                  else:
                    QMessageBox.critical(self, "ERROR", "Contraseña Incorrecta.")
               else:
                   QMessageBox.critical(self, "ERROR", "Usuario no Valido.")     
                   
           except Exception as e:
               QMessageBox.critical(self, "ERROR", "Query Select.")
        else:
            QMessageBox.critical(self, "ERROR", "Error de conexión con la base de datos.") 

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Cuando se presiona Enter, se dispara la acción del botón
            self.validar_credenciales()

    
    def abrir_ventana_principal(self,rol):
        self.txt_nombre_usuario.clear()
        self.txt_contrasena.clear()
        self.hide() # se oculta la ventana login
        self.ventana_principal = VentanaPrincipal(rol,self)
        self.ventana_principal.show()
        # QMessageBox.information(self, "OK", "Rol: " + rol)

if __name__ == "__main__":
   app = QApplication(sys.argv)
   ventana = VentanaLogin() 
   ventana.show()
   sys.exit(app.exec())
