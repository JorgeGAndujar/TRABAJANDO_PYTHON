import sys, os
import bcrypt
import mysql.connector
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox,
    QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView, QCalendarWidget
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt, QDate
from datetime import datetime  # Asegúrate de importar datetime aquí

class VentanaGestionVenta(QWidget):
    def __init__(self):
        super().__init__()
        self.personalizar_ventana()
        self.personalizar_componentes()
        self.cargar_datos()

    def personalizar_ventana(self):
        self.setWindowTitle("Gestion Venta")  # Título para la ventana
        self.setFixedSize(600, 400)  # Tamaño de la ventana ancho y altura
        self.setStyleSheet("background-color: lightgray;")  # Color de fondo para la ventana

        # Cambiar el icono de la ventana con una ruta absoluta que se crea a partir de una relativa
        ruta_relativa = "python6_ventana/cross1.png"
        ruta_absoluta = os.path.abspath(ruta_relativa)
        self.setWindowIcon(QIcon(ruta_absoluta))

    def obtener_fecha_hora(self):
        """Obtiene la fecha y hora actual y la pone en el campo txt_fecha_hora."""
        fecha_hora_actual = datetime.now()
        # Formatear la fecha y hora como 'DD/MM/YYYY HH:MM:SS'
        fecha_hora_str = fecha_hora_actual.strftime("%d/%m/%Y %H:%M:%S")
        self.txt_fecha_hora.setText(fecha_hora_str)  # Asignar al campo de texto

    def personalizar_componentes(self):
        layout = QVBoxLayout()

        # Tabla de Usuarios
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["ID VENTA", "FECHA", "TOTAL"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Campo de texto para la fecha y hora
        self.txt_fecha_hora = QLineEdit(self)
        self.txt_fecha_hora.setPlaceholderText("Fecha y hora")

        # Campo de texto para el total de la venta
        self.txt_total = QLineEdit(self)
        self.txt_total.setPlaceholderText("Total de la venta")

        # Llamar a obtener_fecha_hora para mostrar la fecha y hora actual
        self.obtener_fecha_hora()

        # Botones para el CRUD
        self.btn_agregar_venta = QPushButton("Agregar Venta")
        self.btn_agregar_venta.clicked.connect(self.agregar_venta)
        self.btn_editar_venta = QPushButton("Editar Venta")
        self.btn_editar_venta.clicked.connect(self.editar_venta)
        self.btn_eliminar_venta = QPushButton("Eliminar Venta")
        self.btn_eliminar_venta.clicked.connect(self.eliminar_venta)
        layout_botones = QHBoxLayout()
        layout_botones.addWidget(self.btn_agregar_venta)
        layout_botones.addWidget(self.btn_editar_venta)
        layout_botones.addWidget(self.btn_eliminar_venta)

        # AÑADIR A LA VENTANA(SELF)
        layout.addWidget(self.tabla)
        layout.addWidget(self.txt_fecha_hora)
        layout.addWidget(self.txt_total)
        layout.addLayout(layout_botones)
        self.setLayout(layout)

    def cargar_datos(self):
        conexion = self.obtener_conexion()
        if conexion != None:
            try:
                cursor = conexion.cursor()
                query = "SELECT id_venta,fecha,total FROM Venta"
                cursor.execute(query)
                registros_lt = cursor.fetchall()
                self.tabla.setRowCount(len(registros_lt))
                for fila, registro_t in enumerate(registros_lt):
                    for columna, dato in enumerate(registro_t):
                        self.tabla.setItem(fila, columna, QTableWidgetItem(str(dato)))
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
                database="ferreteria"
            )
            if conexion.is_connected():
                print("OK: CONEXION")
        except Exception as e:
            print(f"Error de conexión: {e}")
            conexion = None
        return conexion  # Retorna la conexión

    def agregar_venta(self):
        conexion = self.obtener_conexion()
        if conexion != None:
            try:
                cursor = conexion.cursor()
                query = """INSERT INTO Venta(fecha, total)
                           VALUES (%s, %s);"""
                fecha = self.txt_fecha_hora.text()
                total = self.txt_total.text()
                cursor.execute(query, (fecha, total))
                conexion.commit()
                QMessageBox.information(None, "Información", "Venta insertada correctamente.")
                self.cargar_datos()
                self.limpiar_campos_usuario()
            except Exception as e:
                QMessageBox.critical(self, "ERROR", "Query Insert.")
        else:
            QMessageBox.critical(self, "ERROR", "Error de conexión con la base de datos.")

    def editar_venta(self):
        conexion = self.obtener_conexion()
        if conexion != None:
            fila_seleccionada = self.tabla.currentRow()
            if fila_seleccionada != -1:
                id_venta = self.tabla.item(fila_seleccionada, 0).text()
                fecha_update = self.txt_fecha_hora.text()
                total_update = self.txt_total.text()

                # Validar si la fecha fue modificada
                if fecha_update:
                    try:
                        # Convertir la fecha al formato adecuado para la base de datos
                        fecha_update = datetime.strptime(fecha_update, "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        QMessageBox.warning(self, "Error", "La fecha no tiene el formato correcto. Debe ser 'DD/MM/YYYY HH:MM:SS'.")
                        return
                else:
                    fecha_update = None  # No actualizar la fecha si el campo está vacío

                # Validar si el total fue modificado
                if total_update:
                    try:
                        total_update = float(total_update)
                    except ValueError:
                        QMessageBox.warning(self, "Error", "El total debe ser un número.")
                        return
                else:
                    total_update = None  # No actualizar el total si el campo está vacío

                # Construir la consulta de actualización
                query = "UPDATE Venta SET "
                params = []

                if fecha_update:
                    query += "fecha = %s, "
                    params.append(fecha_update)
                if total_update is not None:
                    query += "total = %s "
                    params.append(total_update)

                query = query.rstrip(", ")  # Eliminar la última coma si es necesario
                query += " WHERE id_venta = %s"
                params.append(id_venta)

                try:
                    cursor = conexion.cursor()
                    cursor.execute(query, tuple(params))
                    conexion.commit()
                    QMessageBox.information(self, "OK", "Datos actualizados correctamente.")
                    self.cargar_datos()
                    self.limpiar_campos_usuario()
                except Exception as e:
                    QMessageBox.critical(self, "ERROR", f"Error en el Query Update: {str(e)}")
            else:
                QMessageBox.warning(self, "Warning", "Debe seleccionar una venta para editar.")
        else:
            QMessageBox.critical(self, "ERROR", "Error de conexión con la base de datos.")


    def eliminar_venta(self):
        conexion = self.obtener_conexion()
        if conexion is not None:
            fila_seleccionada = self.tabla.currentRow()
            if fila_seleccionada != -1:
                fecha_hora_buscar = self.tabla.item(fila_seleccionada, 0).text()
                try:
                    cursor = conexion.cursor()
                    query = "DELETE FROM Venta WHERE fecha = %s;"
                    cursor.execute(query, (fecha_hora_buscar,))
                    conexion.commit()
                    QMessageBox.information(self, "OK", "Venta eliminada exitosamente.")
                    self.cargar_datos()
                    self.limpiar_campos_usuario()
                except Exception as e:
                        QMessageBox.critical(self, "ERROR", f"Error al eliminar venta: {str(e)}")
            else:
                QMessageBox.warning(self, "Advertencia", "Por favor, selecciona una venta para eliminar.")
        else:
            QMessageBox.critical(self, "ERROR", "Error de conexión con la base de datos.")

    def limpiar_campos_usuario(self):
        self.txt_fecha_hora.clear()
        self.txt_total.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaGestionVenta()
    ventana.show()
    sys.exit(app.exec())
