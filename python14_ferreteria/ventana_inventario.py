import sys
import os
import mysql.connector
from PySide6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QMessageBox,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView, QSpinBox
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from metodos import obtener_conexion


class VentanaInventario(QWidget):
    def __init__(self):
        super().__init__()
        self.personalizar_ventana()
        self.personalizar_componentes()
        self.inicializar_tabla()

    def personalizar_ventana(self):
        self.setWindowTitle("Almacén")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: lightgray;")

        # Icono de la ventana
        ruta_relativa = "python6_ventana/cross1.png"
        ruta_absoluta = os.path.abspath(ruta_relativa)
        self.setWindowIcon(QIcon(ruta_absoluta))

    def personalizar_componentes(self):
        layout_principal = QVBoxLayout()

        # TABLA
        self.tbl_tabla_productos = QTableWidget()
        self.tbl_tabla_productos.setColumnCount(5)
        self.tbl_tabla_productos.setHorizontalHeaderLabels(["ID", "NOMBRE", "DESCRIPCIÓN", "PRECIO", "STOCK"])
        self.tbl_tabla_productos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Desactiva el enfoque automático
        self.tbl_tabla_productos.setFocusPolicy(Qt.NoFocus)

        self.actualizar_tabla_productos()

        # CAJA
        self.txt_id_producto_entrada = QLineEdit()
        self.txt_id_producto_entrada.setPlaceholderText("ID del Producto")

        # SPIN
        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setRange(1, 1000)

        # BOTONES
        self.btn_incrementar_stock = QPushButton("Aumentar Stock")
        self.btn_incrementar_stock.clicked.connect(self.incrementar_stock)

        self.btn_decrementar_stock = QPushButton("Disminuir Stock")
        self.btn_decrementar_stock.clicked.connect(self.decrementar_stock)

        self.btn_actualizar_tabla_productos = QPushButton("Actualizar Tabla Producto")
        self.btn_actualizar_tabla_productos.clicked.connect(self.actualizar_tabla_productos)

        # LAYOUTS
        layout_horizontal = QHBoxLayout()
        layout_horizontal.addWidget(self.txt_id_producto_entrada)
        layout_horizontal.addWidget(self.spin_cantidad)
        layout_horizontal.addWidget(self.btn_incrementar_stock)
        layout_horizontal.addWidget(self.btn_decrementar_stock)

        layout_principal.addWidget(self.tbl_tabla_productos)
        layout_principal.addLayout(layout_horizontal)
        layout_principal.addWidget(self.btn_actualizar_tabla_productos)

        self.setLayout(layout_principal)

    def inicializar_tabla(self):
        """Limpia la selección inicial de la tabla."""
        self.tbl_tabla_productos.clearSelection()

    def incrementar_stock(self):
        conexion = obtener_conexion()
        if conexion is not None:
            try:
                fila_seleccionada = self.tbl_tabla_productos.currentRow()
                if fila_seleccionada == -1:
                    QMessageBox.warning(self, "Error", "Seleccione un producto para actualizar el stock")
                    return

                id_producto = self.tbl_tabla_productos.item(fila_seleccionada, 0).text()
                self.txt_id_producto_entrada.setText(id_producto)

                cursor = conexion.cursor()
                cantidad = self.spin_cantidad.value()
                query = "UPDATE Producto SET stock = stock + %s WHERE id_producto = %s"
                cursor.execute(query, (cantidad, id_producto))

                if cursor.rowcount == 0:
                    QMessageBox.warning(self, "Error", f"ID {id_producto} no encontrado")
                else:
                    QMessageBox.information(self, "Éxito", f"Stock del producto con ID {id_producto} incrementado en {cantidad} unidades")

                conexion.commit()
                self.actualizar_tabla_productos()

            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Error", f"Error en la consulta: {e}")
            finally:
                conexion.close()
        else:
            QMessageBox.critical(self, "Error", "Error de conexión")

    def decrementar_stock(self):
        conexion = obtener_conexion()
        if conexion is not None:
            try:
                fila_seleccionada = self.tbl_tabla_productos.currentRow()
                if fila_seleccionada == -1:
                    QMessageBox.warning(self, "Error", "Seleccione un producto para disminuir el stock")
                    return

                id_producto = self.tbl_tabla_productos.item(fila_seleccionada, 0).text()
                self.txt_id_producto_entrada.setText(id_producto)

                cursor = conexion.cursor()
                cantidad = self.spin_cantidad.value()

                query = "SELECT stock FROM Producto WHERE id_producto = %s"
                cursor.execute(query, (id_producto,))
                producto = cursor.fetchone()

                if not producto:
                    QMessageBox.warning(self, "Error", f"ID {id_producto} no encontrado")
                    return

                if cantidad <= producto[0]:
                    query = "UPDATE Producto SET stock = stock - %s WHERE id_producto = %s"
                    cursor.execute(query, (cantidad, id_producto))
                    QMessageBox.information(self, "Éxito", f"Stock del producto con ID {id_producto} disminuido en {cantidad} unidades")
                else:
                    QMessageBox.warning(self, "Error", f"Cantidad {cantidad} debe ser menor o igual al stock actual")

                conexion.commit()
                self.actualizar_tabla_productos()

            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Error", f"Error en la consulta: {e}")
            finally:
                conexion.close()
        else:
            QMessageBox.critical(self, "Error", "Error de conexión")

    def actualizar_tabla_productos(self):
        conexion = obtener_conexion()
        if conexion is not None:
            try:
                cursor = conexion.cursor()
                query = "SELECT id_producto, nombre, descripcion, precio, stock FROM Producto"
                cursor.execute(query)
                productos_lt = cursor.fetchall()

                self.pintar_tabla(productos_lt)

                # Limpia la selección después de llenar la tabla
                self.tbl_tabla_productos.clearSelection()
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Error", f"Error en la consulta: {e}")
            finally:
                conexion.close()
        else:
            QMessageBox.critical(self, "Error", "Error de conexión")

    def pintar_tabla(self, productos_lt):
        self.tbl_tabla_productos.setRowCount(len(productos_lt))
        for fila, (id_producto, nombre, descripcion, precio, stock) in enumerate(productos_lt):
            self.tbl_tabla_productos.setItem(fila, 0, QTableWidgetItem(str(id_producto)))
            self.tbl_tabla_productos.setItem(fila, 1, QTableWidgetItem(nombre))
            self.tbl_tabla_productos.setItem(fila, 2, QTableWidgetItem(descripcion))
            self.tbl_tabla_productos.setItem(fila, 3, QTableWidgetItem(str(precio)))
            self.tbl_tabla_productos.setItem(fila, 4, QTableWidgetItem(str(stock)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaInventario()
    ventana.show()
    sys.exit(app.exec())

