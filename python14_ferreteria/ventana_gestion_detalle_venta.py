import sys, os
import bcrypt
import mysql.connector
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox,
    QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt

class VentanaGestionDetallesVentas(QWidget):
    def __init__(self):
        super().__init__()
        self.personalizar_ventana()
        self.personalizar_componentes()
        self.cargar_datos()

    def personalizar_ventana(self):
        self.setWindowTitle("Gestión Detalles Ventas")
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: lightgray;")
        ruta_relativa = "python6_ventana/cross1.png"
        ruta_absoluta = os.path.abspath(ruta_relativa)
        self.setWindowIcon(QIcon(ruta_absoluta))

    def personalizar_componentes(self):
        layout = QVBoxLayout()

        # Tabla de Productos
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["ID DETALLE", "ID VENTA", "ID PRODUCTO", "CANTIDAD", "SUBTOTAL"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Campos para CRUD
        self.txt_id_venta = QLineEdit()
        self.txt_id_venta.setPlaceholderText("Id Venta")

        self.txt_id_producto = QLineEdit()
        self.txt_id_producto.setPlaceholderText("Id Producto")

        self.txt_cantidad = QLineEdit()
        self.txt_cantidad.setPlaceholderText("Cantidad")

        self.txt_subtotal = QLineEdit()
        self.txt_subtotal.setPlaceholderText("Subtotal")

        # Botones para el CRUD
        self.btn_agregar_detalle_venta = QPushButton("Agregar Detalle Venta")
        self.btn_agregar_detalle_venta.clicked.connect(self.agregar_detalle_venta)
        self.btn_editar_detalle_venta = QPushButton("Editar Detalle Venta")
        self.btn_editar_detalle_venta.clicked.connect(self.editar_detalle_venta)
        self.btn_eliminar_detalle_venta = QPushButton("Eliminar Detalle Venta")
        self.btn_eliminar_detalle_venta.clicked.connect(self.eliminar_detalle_venta)
        
        layout_botones = QHBoxLayout()
        layout_botones.addWidget(self.btn_agregar_detalle_venta)
        layout_botones.addWidget(self.btn_editar_detalle_venta)
        layout_botones.addWidget(self.btn_eliminar_detalle_venta)

        # Añadir los componentes a la ventana
        layout.addWidget(self.tabla)
        layout.addWidget(self.txt_id_venta)
        layout.addWidget(self.txt_id_producto)
        layout.addWidget(self.txt_cantidad)
        layout.addWidget(self.txt_subtotal)
        layout.addLayout(layout_botones)
        self.setLayout(layout)

    def cargar_datos(self):
        """Carga los productos en la tabla."""
        conexion = self.obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                query = "SELECT id_detalle, id_venta, id_producto, cantidad, subtotal FROM DetalleVentas"
                cursor.execute(query)
                registros_lt = cursor.fetchall()
                self.tabla.setRowCount(len(registros_lt))
                for fila, registro_t in enumerate(registros_lt):
                    for columna, dato in enumerate(registro_t):
                        self.tabla.setItem(fila, columna, QTableWidgetItem(str(dato)))
            except Exception as e:
                QMessageBox.critical(self, "ERROR", f"Error al cargar productos: {e}")    
        else:
            QMessageBox.critical(self, "ERROR", "Error de conexión con la base de datos.") 

    def obtener_conexion(self):
        """Obtiene la conexión a la base de datos."""
        conexion = None
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                port="3307",
                user="root",
                password="12345678",
                database="ferreteria"
            )
            if conexion.is_connected():
                print("Conexión exitosa")
        except Exception as e:
            print(f"Error de conexión: {e}")
            conexion = None
        return conexion

    def agregar_detalle_venta(self):
        conexion = self.obtener_conexion()
        if conexion is not None:
            try:
                cursor = conexion.cursor()
                query = """INSERT INTO DetalleVentas (id_venta, id_producto, cantidad, subtotal)
                           VALUES (%s, %s, %s, %s);"""
                registro_t = (
                    int(self.txt_id_venta.text()),
                    int(self.txt_id_producto.text()),
                    int(self.txt_cantidad.text()),
                    int(self.txt_subtotal.text())  # Corregir aquí para usar text()
                )
                
                cursor.execute(query, registro_t)
                conexion.commit()
                QMessageBox.information(None, "Información", "Detalle Venta insertado correctamente.")
                self.cargar_datos()
                self.limpiar_campos_productos()
            except Exception as e:
                QMessageBox.critical(self, "ERROR", f"Error al insertar detalle de venta: {e}")
            finally:
                conexion.close()
        else:
            QMessageBox.critical(self, "ERROR", "Error de conexión con la base de datos.")

    def editar_detalle_venta(self):
        """Edita un producto seleccionado en la tabla."""
        conexion = self.obtener_conexion()
        if conexion:
            fila_seleccionada = self.tabla.currentRow()
            if fila_seleccionada != -1:
                # Obtener el id del detalle seleccionado
                id_detalle_buscar = self.tabla.item(fila_seleccionada, 0).text()  # Columna 0 es ID DETALLE
                id_venta_update = self.txt_id_venta.text()
                id_producto_update = self.txt_id_producto.text()
                cantidad_update = self.txt_cantidad.text()
                subtotal_update = self.txt_subtotal.text()

                # Verificar si al menos un campo se ha modificado
                if id_venta_update or id_producto_update or cantidad_update or subtotal_update:
                    try:
                        cursor = conexion.cursor()

                        # Actualizar los detalles de venta
                        query = """UPDATE DetalleVentas 
                                   SET id_venta = COALESCE(NULLIF(%s, ''), id_venta),
                                       id_producto = COALESCE(NULLIF(%s, ''), id_producto),
                                       cantidad = COALESCE(NULLIF(%s, ''), cantidad),
                                       subtotal = COALESCE(NULLIF(%s, ''), subtotal)
                                   WHERE id_detalle = %s;"""
                        cursor.execute(query, (id_venta_update, id_producto_update, cantidad_update, subtotal_update, id_detalle_buscar))
                        conexion.commit()
                        QMessageBox.information(self, "Éxito", "Detalle Venta actualizado correctamente.")
                        self.cargar_datos()
                    except Exception as e:
                        QMessageBox.critical(self, "ERROR", f"Error al actualizar los datos: {e}")
                else:
                    QMessageBox.warning(self, "Advertencia", "Debe modificar al menos un campo del producto.")
            else:
                QMessageBox.warning(self, "Advertencia", "Debe seleccionar un producto para editar.")
        else:
            QMessageBox.critical(self, "ERROR", "Error de conexión con la base de datos.")

    def eliminar_detalle_venta(self):
        """Elimina un producto seleccionado de la tabla."""
        conexion = self.obtener_conexion()
        if conexion:
            fila_seleccionada = self.tabla.currentRow()
            if fila_seleccionada != -1:
                id_detalle_buscar = self.tabla.item(fila_seleccionada, 0).text()  # Columna 0 es ID DETALLE
                try:
                    cursor = conexion.cursor()
                    query = "DELETE FROM DetalleVentas WHERE id_detalle = %s;"
                    cursor.execute(query, (id_detalle_buscar,))
                    conexion.commit()
                    QMessageBox.information(self, "Éxito", "Detalle Venta eliminado correctamente.")
                    self.cargar_datos()
                except Exception as e:
                    QMessageBox.critical(self, "ERROR", f"Error al eliminar el producto: {e}")
            else:
                QMessageBox.warning(self, "Advertencia", "Debe seleccionar un producto para eliminar.")
        else:
            QMessageBox.critical(self, "ERROR", "Error de conexión con la base de datos.")
    
    def limpiar_campos_productos(self):
        """Limpia los campos del formulario."""
        self.txt_id_venta.clear()
        self.txt_id_producto.clear()
        self.txt_cantidad.clear()
        self.txt_subtotal.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaGestionDetallesVentas()
    ventana.show()
    sys.exit(app.exec())
