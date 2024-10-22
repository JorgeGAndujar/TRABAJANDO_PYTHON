import sys, os, sqlite3, bcrypt
from PySide6.QtWidgets import QMainWindow, QRadioButton, QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QComboBox
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt


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
        self.setWindowTitle("INSERTAR PRODUCTO")
        self.setFixedSize(480, 330)
        self.setStyleSheet("background-color: lightgray;")

        ruta_relativa = "python6_ventana/cross1.png"
        ruta_absoluta = os.path.abspath(ruta_relativa)
        self.setWindowIcon(QIcon(ruta_absoluta))

        self.pnlPrincipal = QWidget()
        self.setCentralWidget(self.pnlPrincipal)

    def personalizarComponentes(self):
        self.lblTitulo = QLabel("INSERTAR PRODUCTO", self.pnlPrincipal)
        self.lblTitulo.setFont(QFont("Courier New", 9))
        self.lblTitulo.setStyleSheet("background-color: black; color: yellow;")
        self.lblTitulo.setAlignment(Qt.AlignCenter)
        self.lblTitulo.setGeometry(0, 0, 480, 20)

        self.lblProducto = QLabel("INGRESE PRODUCTO?", self.pnlPrincipal)
        self.lblProducto.setFont(QFont("Courier New", 9))
        self.lblProducto.setGeometry(50, 80, 147, 17)

        self.lblPrecio = QLabel("INGRESE PRECIO?", self.pnlPrincipal)
        self.lblPrecio.setFont(QFont("Courier New", 9))
        self.lblPrecio.setGeometry(50, 120, 147, 17)

        self.lblStock = QLabel("INGRESE Cant STOCK?", self.pnlPrincipal)
        self.lblStock.setFont(QFont("Courier New", 9))
        self.lblStock.setGeometry(50, 160, 147, 17)

        self.txtProducto = QLineEdit(self.pnlPrincipal)
        self.txtProducto.setGeometry(235, 80, 120, 20)
        self.txtProducto.setFont(QFont("Courier New", 9))
        self.txtProducto.setAlignment(Qt.AlignCenter)
        self.txtProducto.setStyleSheet("color: blue;")

        self.txtPrecio = QLineEdit(self.pnlPrincipal)
        self.txtPrecio.setGeometry(235, 120, 120, 20)
        self.txtPrecio.setFont(QFont("Courier New", 9))
        self.txtPrecio.setAlignment(Qt.AlignCenter)
        self.txtPrecio.setStyleSheet("color: blue;")

        self.txtStock = QLineEdit(self.pnlPrincipal)
        self.txtStock.setGeometry(235, 160, 120, 20)
        self.txtStock.setFont(QFont("Courier New", 9))
        self.txtStock.setAlignment(Qt.AlignCenter)
        self.txtStock.setStyleSheet("color: blue;")

        self.btoInsert = QPushButton("INSERTAR", self.pnlPrincipal)
        self.btoInsert.setGeometry(110, 240, 80, 20)
        self.btoInsert.setFont(QFont("Courier New", 8))
        self.btoInsert.clicked.connect(self.insert)

        self.btoReiniciar = QPushButton("REINICIAR", self.pnlPrincipal)
        self.btoReiniciar.setGeometry(200, 240, 80, 20)
        self.btoReiniciar.setFont(QFont("Courier New", 8))
        self.btoReiniciar.clicked.connect(self.reiniciar)

        self.btoSalir = QPushButton("SALIR", self.pnlPrincipal)
        self.btoSalir.setGeometry(290, 240, 80, 20)
        self.btoSalir.setFont(QFont("Courier New", 8))
        self.btoSalir.clicked.connect(self.salir)

    def insert(self):
        conexion = self.obtener_conexion()
        if conexion is not None:
            try:
                cursor = conexion.cursor()
                query = """INSERT INTO Producto(nombre_producto, precio, stock)
                           VALUES (?, ?, ?);"""
                nombre_producto = self.txtProducto.text()
                precio = self.txtPrecio.text()
                stock = self.txtStock.text()

                cursor.execute(query, (nombre_producto, precio, stock))
                conexion.commit()
                QMessageBox.information(None, "Información", "PRODUCTO insertado correctamente.")
            except sqlite3.IntegrityError as e:
                QMessageBox.critical(None, "Error", f"Error al insertar producto: {e}")
            finally:
                conexion.close()
        else:
            QMessageBox.critical(None, "Error", "Error de conexión con la base de datos.")

    def reiniciar(self):
        self.txtUsuario.clear()
        self.txtContraseña.clear()
        self.cboRol.setCurrentIndex(0)

    def salir(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())
