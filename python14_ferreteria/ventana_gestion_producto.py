import sys, os
import bcrypt
import mysql.connector
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox,
    QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt

class VentanaGestionProductos(QWidget):
    def __init__(self):
        super().__init__()
        self.personalizar_ventana()
        self.personalizar_componentes()
        self.cargar_datos()

    def personalizar_ventana(self):
        self.setWindowTitle("Gestión de Productos")
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: lightgray;")
        ruta_relativa = "python6_ventana/cross1.png"
        ruta_absoluta = os.path.abspath(ruta_relativa)
        self.setWindowIcon(QIcon(ruta_absoluta))

    def personalizar_componentes(self):
        layout = QVBoxLayout()

        # Tabla de Productos
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(["ID PRODUCTO", "NOMBRE PRODUCTO", "DESCRIPCION", "PRECIO", "STOCK", "CATEGORIA"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Campos para CRUD
        self.txt_nombre_producto = QLineEdit()
        self.txt_nombre_producto.setPlaceholderText("Nombre Producto")

        self.txt_descripcion = QLineEdit()
        self.txt_descripcion.setPlaceholderText("Descripción")

        self.txt_precio = QLineEdit()
        self.txt_precio.setPlaceholderText("Precio")

        self.txt_stock = QLineEdit()
        self.txt_stock.setPlaceholderText("Stock")

        self.txt_categoria = QLineEdit()
        self.txt_categoria.setPlaceholderText("Seleccione una categoria")

        # Inicializar el QComboBox para las categorías
        self.cbo_categoria = QComboBox()

        # Botones para el CRUD
        self.btn_agregar_producto = QPushButton("Agregar Producto")
        self.btn_agregar_producto.clicked.connect(self.agregar_producto)
        self.btn_editar_producto = QPushButton("Editar Producto")
        self.btn_editar_producto.clicked.connect(self.editar_producto)
        self.btn_eliminar_producto = QPushButton("Eliminar Producto")
        self.btn_eliminar_producto.clicked.connect(self.eliminar_producto)
        
        layout_botones = QHBoxLayout()
        layout_botones.addWidget(self.btn_agregar_producto)
        layout_botones.addWidget(self.btn_editar_producto)
        layout_botones.addWidget(self.btn_eliminar_producto)

        # Cargar las categorías al combobox
        self.cargar_categoria()

        # Añadir los componentes a la ventana
        layout.addWidget(self.tabla)
        layout.addWidget(self.txt_nombre_producto)
        layout.addWidget(self.txt_descripcion)
        layout.addWidget(self.txt_precio)
        layout.addWidget(self.txt_stock)
        layout.addWidget(self.cbo_categoria)
        layout.addWidget(self.txt_categoria)
        layout.addLayout(layout_botones)
        self.setLayout(layout)

    def cargar_categoria(self):
        """Carga las categorías existentes desde la base de datos en el combobox."""
        conexion = self.obtener_conexion()
        if conexion:
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT DISTINCT categoria FROM Producto")
                    categorias = cursor.fetchall()
                    self.cbo_categoria.clear()
                    self.cbo_categoria.addItem("Selecciona una categoría")  # Primer item vacío
                    for categoria in categorias:
                        self.cbo_categoria.addItem(categoria[0])
            except Exception as e:
                QMessageBox.critical(self, "ERROR", f"Error al cargar categorías: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "No se pudo conectar con la base de datos.")
        
    def cargar_datos(self):
        """Carga los productos en la tabla."""
        conexion = self.obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                query = "SELECT id_producto, nombre, descripcion, precio, stock, categoria FROM Producto"
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

    def agregar_producto(self):
        conexion = self.obtener_conexion()
        if conexion != None:
            try:
                cursor = conexion.cursor()
                categoria_nueva = self.txt_categoria.text().strip()  # Categoría nueva ingresada
                categoria_seleccionada = self.cbo_categoria.currentText()  # Categoría seleccionada
                categoria_final = categoria_nueva if categoria_nueva else categoria_seleccionada

                if categoria_final == "" or categoria_final == "Selecciona una categoría":

                    QMessageBox.warning(None, "Advertencia", "Debe llenar todos los campos correctamente.")
                    return
                query = """INSERT INTO Producto(nombre, descripcion, precio, stock, categoria)
                           VALUES (%s, %s, %s, %s, %s);"""
                registro_t = (
                    self.txt_nombre_producto.text(),
                    self.txt_descripcion.text(),
                    float(self.txt_precio.text()),
                    int(self.txt_stock.text()),
                    categoria_final)
                
                cursor.execute(query, registro_t)
                conexion.commit()
                QMessageBox.information(None, "Información", "Producto insertado correctamente.")
                self.cargar_datos()
                self.cargar_categoria()
                self.limpiar_campos_productos()
                return
            except Exception as e:
                QMessageBox.critical(self, "ERROR", "Error al insertar producto.")
            finally:
                conexion.close()
        else:
           QMessageBox.critical(self, "ERROR", "Error de conexión con la base de datos.")

    def editar_producto(self):
        """Edita un producto seleccionado en la tabla."""
        conexion = self.obtener_conexion()
        if conexion:
            fila_seleccionada = self.tabla.currentRow()
            if fila_seleccionada != -1:
                # Obtener el id del producto seleccionado
                id_producto_buscar = self.tabla.item(fila_seleccionada, 0).text()  # Columna 0 es ID
                nombre_producto_update = self.txt_nombre_producto.text()
                descripcion_update = self.txt_descripcion.text()
                precio_update = self.txt_precio.text()
                stock_update = self.txt_stock.text()
                categoria_update = self.cbo_categoria.currentText()

                # Verificar si al menos un campo se ha modificado
                if nombre_producto_update or descripcion_update or precio_update or stock_update or categoria_update != "Selecciona una categoría":
                    try:
                        cursor = conexion.cursor()

                        # Si no se ha modificado un campo, se mantiene su valor anterior
                        query = """UPDATE Producto 
                                SET nombre = COALESCE(NULLIF(%s, ''), nombre),
                                    descripcion = COALESCE(NULLIF(%s, ''), descripcion),
                                    precio = COALESCE(NULLIF(%s, ''), precio),
                                    stock = COALESCE(NULLIF(%s, ''), stock),
                                    categoria = COALESCE(NULLIF(%s, ''), categoria)
                                WHERE id_producto = %s;"""
                        cursor.execute(query, (nombre_producto_update, descripcion_update, precio_update, stock_update, categoria_update, id_producto_buscar))
                        conexion.commit()
                        QMessageBox.information(self, "Éxito", "Producto actualizado correctamente.")
                        self.cargar_datos()
                    except Exception as e:
                        QMessageBox.critical(self, "ERROR", f"Error al actualizar los datos: {e}")
                else:
                    QMessageBox.warning(self, "Advertencia", "Debe modificar al menos un campo del producto.")
            else:
                QMessageBox.warning(self, "Advertencia", "Debe seleccionar un producto para editar.")
        else:
            QMessageBox.critical(self, "ERROR", "Error de conexión con la base de datos.")

    def eliminar_producto(self):
        """Elimina un producto seleccionado de la tabla."""
        conexion = self.obtener_conexion()
        if conexion:
            fila_seleccionada = self.tabla.currentRow()
            if fila_seleccionada != -1:
                nombre_producto_buscar = self.tabla.item(fila_seleccionada, 1).text()
                try:
                    cursor = conexion.cursor()
                    query = "DELETE FROM Producto WHERE nombre = %s;"
                    cursor.execute(query, (nombre_producto_buscar,))
                    conexion.commit()
                    QMessageBox.information(self, "Éxito", "Producto eliminado correctamente.")
                    self.cargar_datos()
                except Exception as e:
                    QMessageBox.critical(self, "ERROR", f"Error al eliminar el producto: {e}")
            else:
                QMessageBox.warning(self, "Advertencia", "Debe seleccionar un producto para eliminar.")
        else:
            QMessageBox.critical(self, "ERROR", "Error de conexión con la base de datos.")
    
    def limpiar_campos_productos(self):
        """Limpia los campos del formulario."""
        self.txt_nombre_producto.clear()
        self.txt_descripcion.clear()
        self.txt_precio.clear()
        self.txt_stock.clear()
        self.cbo_categoria.setCurrentIndex(0)
        self.txt_categoria.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaGestionProductos()
    ventana.show()
    sys.exit(app.exec())
