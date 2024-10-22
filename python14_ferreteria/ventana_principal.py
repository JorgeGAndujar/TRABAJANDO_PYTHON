import sys,os
import bcrypt
import mysql.connector
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView, QMainWindow
)
from PySide6.QtGui import QFont, QIcon
from ventana_gestion_usuarios import VentanaGestionUsuarios
from ventana_gestion_producto import VentanaGestionProductos
from ventana_ventas import VentanaVentas
from ventana_inventario import VentanaInventario

class VentanaPrincipal(QMainWindow):
    def __init__(self, rol, objeto_ventana_login):
          super().__init__()
          self.setWindowTitle("Menu")  # Título para la ventana
          self.setFixedSize(400, 200)  # Tamaño de la ventana ancho y altura

          # Cambiar el icono de la ventanapython9_ventana_menu_mihaita/cross1.png con una ruta absoluta que se crea a partir de una relativa
          ruta_relativa = "python14_ferreteria/cross1.png"
          ruta_absoluta = os.path.abspath(ruta_relativa)
          self.setWindowIcon(QIcon(ruta_absoluta)) 

          layout_principal = QVBoxLayout()
          panel_principal = QWidget() 
          panel_principal.setLayout(layout_principal) 
          self.setCentralWidget(panel_principal)

          self.rol = rol
          self.objeto_ventana = objeto_ventana_login

          if rol == 'Administrador':
             self.abrir_ventana_menu_administrador(layout_principal)
          elif rol == 'Cajero':
             self.abrir_ventana_menu_cajero(layout_principal)
          elif rol == 'Almacén':
             self.abrir_ventana_menu_almacen(layout_principal)


    def abrir_ventana_menu_administrador(self, layout_principal):
          btn_cerrar_sesion = QPushButton("Cerrar Sesión")
          btn_cerrar_sesion.clicked.connect(self.cerrar_sesion)
          btn_gestion_usuarios = QPushButton("Gestión Usuarios")
          btn_gestion_usuarios.clicked.connect(self.gestion_usuarios)
          btn_gestion_productos = QPushButton("Gestión Productos")
          btn_gestion_productos.clicked.connect(self.gestion_producto)
          btn_venta = QPushButton("Gestión Cajero")
          btn_venta.clicked.connect(self.gestion_ventas)
          btn_almacen = QPushButton("Gestión Almacén")
          btn_almacen.clicked.connect(self.gestion_almacen)

          layout_principal.addWidget(btn_gestion_usuarios)
          layout_principal.addWidget(btn_gestion_productos)
          layout_principal.addWidget(btn_venta)
          layout_principal.addWidget(btn_almacen)

          layout_principal.addWidget(btn_cerrar_sesion)
          

    def abrir_ventana_menu_cajero(self, layout_principal):
          btn_cerrar_sesion = QPushButton("Cerrar Sesión")
          btn_cerrar_sesion.clicked.connect(self.cerrar_sesion)
          btn_venta = QPushButton("Gestión Cajero")
          btn_venta.clicked.connect(self.gestion_ventas)

          layout_principal.addWidget(btn_venta)
          layout_principal.addWidget(btn_cerrar_sesion)
          
    def abrir_ventana_menu_almacen(self, layout_principal):
          btn_cerrar_sesion = QPushButton("Cerrar Sesión")
          btn_cerrar_sesion.clicked.connect(self.cerrar_sesion)
          btn_almacen = QPushButton("Gestión Almacén")
          btn_almacen.clicked.connect(self.gestion_almacen)
          
          layout_principal.addWidget(btn_almacen)
          layout_principal.addWidget(btn_cerrar_sesion)

    def cerrar_sesion(self):
        self.close()
        self.objeto_ventana.show()


    def gestion_usuarios(self):
        self.ventana_gestion_usuarios = VentanaGestionUsuarios()
        self.ventana_gestion_usuarios.show()

    def gestion_producto(self):
        self.ventana_gestion_producto = VentanaGestionProductos()
        self.ventana_gestion_producto.show()

    def gestion_ventas(self):
        self.ventana_ventas = VentanaVentas()
        self.ventana_ventas.show()
        
        
    def gestion_almacen(self):
        self.ventana_inventario = VentanaInventario()
        self.ventana_inventario.show()
        
        

          
          