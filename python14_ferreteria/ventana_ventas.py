import sys, os
import bcrypt
import mysql.connector
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,QComboBox,
    QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView, QSpinBox
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt
from metodos import obtener_productos_disponibles, obtener_conexion
from datetime import datetime

class VentanaVentas(QWidget):
    def __init__(self):
        super().__init__()
        #self.productos_disponibles_d = obtener_productos_disponibles()
        #print(self.productos_disponibles_d)
        self.productos_disponibles_d = {}
        self.carrito_lt = []
        self.personalizar_ventana()
        self.personalizar_componentes()
    
    def personalizar_ventana(self):
        self.setWindowTitle("Cajero")  # Título para la ventana
        self.setFixedSize(800, 600)  # Tamaño de la ventana ancho y altura
        self.setStyleSheet("background-color: lightgray;")  # Color de fondo para la ventana

        # Cambiar el icono de la ventana con una ruta absoluta que se crea a partir de una relativa
        ruta_relativa = "python6_ventana/cross1.png"
        ruta_absoluta = os.path.abspath(ruta_relativa)
        #print(ruta_absoluta) # 
        self.setWindowIcon(QIcon(ruta_absoluta))

    def personalizar_componentes(self):
        layout_principal = QVBoxLayout()
        # TABLA
        self.tbl_carrito = QTableWidget()
        self.tbl_carrito.setColumnCount(5)
        self.tbl_carrito.setHorizontalHeaderLabels(["ID","PRODUCTO","CANTIDAD","PRECIO","SUBTOTAL"])
        self.tbl_carrito.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # COMBOBOX
        self.cbo_seleccion_producto = QComboBox()
        self.cargar_datos_combobox()

        # SPIN
        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setRange(1,100)

        # BOTONES
        self.btn_anadir_carrito = QPushButton("Añadir al Carrito")
        self.btn_anadir_carrito.clicked.connect(self.agregar_al_carrito)
        self.btn_eliminar_seleccion = QPushButton("Eliminar Seleccion")
        self.btn_eliminar_seleccion.clicked.connect(self.eliminar_seleccion)
         
        # CREAR ADMINISTRADOR HORIZONTAL
        layout_horizontal = QHBoxLayout()
        layout_horizontal.addWidget(self.cbo_seleccion_producto)
        layout_horizontal.addWidget(self.spin_cantidad)
        layout_horizontal.addWidget(self.btn_anadir_carrito)
        layout_horizontal.addWidget(self.btn_eliminar_seleccion)

        # CREAR ETIQUETA
        self.lbl_total = QLabel("Total: €0.00")
        self.lbl_total.setAlignment(Qt.AlignRight)

        # BOTÓN CONFIRMAR VENTA
        self.btn_confirmar_venta = QPushButton("Confirmar Venta")
        self.btn_confirmar_venta.clicked.connect(self.confirmar_venta)
        
              
        layout_principal.addWidget(self.tbl_carrito)
        layout_principal.addLayout(layout_horizontal)
        layout_principal.addWidget(self.lbl_total)
        layout_principal.addWidget(self.btn_confirmar_venta)

        self.setLayout(layout_principal)

    def cargar_datos_combobox(self):
        self.productos_disponibles_d = obtener_productos_disponibles()
        #print(self.productos_disponibles_d)
        self.cbo_seleccion_producto.clear()
        self.cbo_seleccion_producto.addItems(self.productos_disponibles_d.keys())

    def agregar_al_carrito(self):
        producto_seleccionado = self.cbo_seleccion_producto.currentText()
        #print(producto_seleccionado)
        cantidad = self.spin_cantidad.value()

        if producto_seleccionado not in self.productos_disponibles_d:
           QMessageBox.warning(self, "Error", "Producto no disponible")
           return
        
        id_producto, nombre, precio, stock = self.productos_disponibles_d[producto_seleccionado]
        
        if cantidad > stock:
           QMessageBox.warning(self, "Error", "Stock insuficiente") 
           return
        
        # ACTUALIZAR STOCK
        self.productos_disponibles_d[producto_seleccionado]= (id_producto, nombre, precio, stock - cantidad)
        subtotal = round(precio * cantidad,2)
        self.carrito_lt.append([id_producto, nombre, cantidad, precio, subtotal])
        self.actualizar_tabla_carrito()
    
    def actualizar_tabla_carrito(self):
        self.tbl_carrito.setRowCount(len(self.carrito_lt))
        total = 0
        for fila, (id_producto,nombre,cantidad,precio,subtotal) in enumerate(self.carrito_lt):
            total = total + subtotal
            # PINTAR TABLA
            self.tbl_carrito.setItem(fila, 0, QTableWidgetItem(str(id_producto)))
            self.tbl_carrito.setItem(fila, 1, QTableWidgetItem(nombre))
            self.tbl_carrito.setItem(fila, 2, QTableWidgetItem(str(cantidad)))
            self.tbl_carrito.setItem(fila, 3, QTableWidgetItem(str(precio)))
            self.tbl_carrito.setItem(fila, 4, QTableWidgetItem(f"{subtotal:.2f}"))
        self.lbl_total.setText(f"Total: €{total:.2f}")

    def confirmar_venta(self):
        conexion = obtener_conexion()
        if conexion != None:
            try:
                total = 0
                for _,_,_,_,subtotal in self.carrito_lt:
                    total = total + subtotal

                cursor = conexion.cursor() 
                query = "INSERT INTO Venta (fecha, total) VALUES (%s, %s)"
                cursor.execute(query,(datetime.now(),total))
                id_venta = cursor.lastrowid
                
                query1 = "INSERT INTO DetalleVentas (id_venta,id_producto,cantidad,subtotal) VALUES (%s,%s,%s,%s)"
                query2 = "UPDATE Producto SET stock = stock - %s WHERE id_producto = %s"
                #(id_producto,nombre,cantidad,precio,subtotal) = carrito_lt
                for id_producto,_,cantidad,_,subtotal in self.carrito_lt:
                    cursor.execute(query1,(id_venta,id_producto,cantidad,subtotal))
                    cursor.execute(query2,(cantidad, id_producto))
                
                conexion.commit()
                QMessageBox.information(self, "OK", "Venta Confirmada.")
                self.carrito_lt.clear()
                self.actualizar_tabla_carrito()
                self.cargar_datos_combobox()
        
            except Exception as e:
               QMessageBox.critical(self, "ERROR", "Confirmar Venta.") 
        else:
            QMessageBox.critical(self, "ERROR", "Error de conexión con la base de datos.")

    def eliminar_seleccion(self): 
        fila_seleccionada = self.tbl_carrito.currentRow()  
        if fila_seleccionada == -1: 
           QMessageBox.warning(self, "Error", "Seleccione un producto para eliminar") 
           return
        # Restituir stock del producto eliminado
        id_producto, nombre, cantidad, _, _ = self.carrito_lt.pop(fila_seleccionada)
        
        producto_key = next(k for k, v in self.productos_disponibles_d.items() if v[0] == id_producto)
        id_producto, nombre, precio, stock = self.productos_disponibles_d[producto_key]
        self.productos_disponibles_d[producto_key] = (id_producto, nombre, precio, stock + cantidad)
        self.actualizar_tabla_carrito()

    


if __name__ == "__main__":
   app = QApplication(sys.argv)
   ventana = VentanaVentas() 
   ventana.show()
   sys.exit(app.exec())
