import sys, os, sqlite3, bcrypt
from PySide6.QtWidgets import QMainWindow, QCalendarWidget, QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt, QDate

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.personalizarVentana()
        self.personalizarComponentes()

    def obtener_conexion(self):
        nra = "C:\\TRABAJANDO_PYTHON\\python13_encriptar_contraseña\\ferreteria.sqlite3"
        conexion = None
        try:
            conexion = sqlite3.connect(nra)
            print("OK: CONEXION")
        except sqlite3.Error as error:
            print(f"Error de conexión: {error}")
        return conexion

    def personalizarVentana(self):
        self.setWindowTitle("VENTA")
        self.setFixedSize(480, 380)  # Ajustar tamaño para más espacio
        self.setStyleSheet("background-color: lightgray;")

        ruta_relativa = "python6_ventana/cross1.png"
        ruta_absoluta = os.path.abspath(ruta_relativa)
        self.setWindowIcon(QIcon(ruta_absoluta))

        self.pnlPrincipal = QWidget()
        self.setCentralWidget(self.pnlPrincipal)

    def mostrarFechaSeleccionada(self, fecha):
        fecha_str = "{:02d}/{:02d}/{:04d}".format(fecha.day(), fecha.month(), fecha.year())
        self.lblFecha.setText(fecha_str)
        print(fecha.toString())
        print(fecha.day())
        print(fecha.month())
        print(fecha.year())

    def personalizarComponentes(self):
        # Título de la ventana
        self.lblTitulo = QLabel("VENTAS POR FECHA", self.pnlPrincipal)
        self.lblTitulo.setFont(QFont("Courier New", 9))
        self.lblTitulo.setStyleSheet("background-color: black; color: yellow;")
        self.lblTitulo.setAlignment(Qt.AlignCenter)
        self.lblTitulo.setGeometry(0, 0, 480, 20)

        # Calendario
        self.calendario = QCalendarWidget(self.pnlPrincipal)
        self.calendario.setGridVisible(True)
        self.calendario.setGeometry(10, 30, 460, 200)
        self.calendario.clicked[QDate].connect(self.mostrarFechaSeleccionada)

        # Etiqueta para mostrar la fecha seleccionada
        self.lblFecha = QLabel("AQUÍ SE PONE LA FECHA SELECCIONADA", self.pnlPrincipal)
        self.lblFecha.setFont(QFont("Courier New", 12))
        self.lblFecha.setStyleSheet("color: #FF0000;")
        self.lblFecha.setAlignment(Qt.AlignCenter)
        self.lblFecha.setGeometry(0, 240, 480, 20)

        # Etiqueta para el total
        self.lblTotal = QLabel("TOTAL VENTAS:", self.pnlPrincipal)
        self.lblTotal.setFont(QFont("Courier New", 9))
        self.lblTotal.setGeometry(50, 270, 100, 30)

        # Campo de entrada para el total
        self.txtTotal = QLineEdit(self.pnlPrincipal)
        self.txtTotal.setGeometry(150, 270, 200, 30)
        self.txtTotal.setFont(QFont("Courier New", 9))
        self.txtTotal.setAlignment(Qt.AlignCenter)
        self.txtTotal.setStyleSheet("color: blue;")
        self.txtTotal.setPlaceholderText("Ingrese el total")

        # Botones distribuidos horizontalmente
        self.btoInsert = QPushButton("INSERTAR", self.pnlPrincipal)
        self.btoInsert.setFont(QFont("Courier New", 8))
        self.btoInsert.setGeometry(50, 320, 100, 30)
        self.btoInsert.clicked.connect(self.insert)

        self.btoReiniciar = QPushButton("REINICIAR", self.pnlPrincipal)
        self.btoReiniciar.setFont(QFont("Courier New", 8))
        self.btoReiniciar.setGeometry(190, 320, 100, 30)
        self.btoReiniciar.clicked.connect(self.reiniciar)

        self.btoSalir = QPushButton("SALIR", self.pnlPrincipal)
        self.btoSalir.setFont(QFont("Courier New", 8))
        self.btoSalir.setGeometry(330, 320, 100, 30)
        self.btoSalir.clicked.connect(self.salir)

    def insert(self):
        conexion = self.obtener_conexion()
        if conexion is not None:
            try:
                cursor = conexion.cursor()
                query = """INSERT INTO Venta(fecha_venta, total) VALUES (?, ?);"""
                fecha_venta = self.lblFecha.text()
                total = self.txtTotal.text()  # Obtener texto del campo de entrada
                cursor.execute(query, (fecha_venta, total))
                conexion.commit()
                QMessageBox.information(self, "Información", "Venta insertada correctamente.")
            except sqlite3.IntegrityError as e:
                QMessageBox.critical(self, "Error", f"Error al insertar venta: {e}")
            finally:
                conexion.close()
        else:
            QMessageBox.critical(self, "Error", "Error de conexión con la base de datos.")

    def reiniciar(self):
        self.lblFecha.setText("AQUÍ SE PONE LA FECHA SELECCIONADA")
        self.txtTotal.clear()
        QMessageBox.information(self, "Reiniciar", "Formulario reiniciado.")

    def salir(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())
