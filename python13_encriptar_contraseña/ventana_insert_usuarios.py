import sys, os, sqlite3, bcrypt
from PySide6.QtWidgets import QMainWindow, QRadioButton, QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QComboBox
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt


class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.personalizarVentana()
        self.personalizarComponentes()
        self.crear_tabla()

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
        self.setWindowTitle("INSERTAR USUARIO")
        self.setFixedSize(480, 330)
        self.setStyleSheet("background-color: lightgray;")

        ruta_relativa = "python6_ventana/cross1.png"
        ruta_absoluta = os.path.abspath(ruta_relativa)
        self.setWindowIcon(QIcon(ruta_absoluta))

        self.pnlPrincipal = QWidget()
        self.setCentralWidget(self.pnlPrincipal)

    def personalizarComponentes(self):
        self.lblTitulo = QLabel("INSERTAR USUARIO", self.pnlPrincipal)
        self.lblTitulo.setFont(QFont("Courier New", 9))
        self.lblTitulo.setStyleSheet("background-color: black; color: yellow;")
        self.lblTitulo.setAlignment(Qt.AlignCenter)
        self.lblTitulo.setGeometry(0, 0, 480, 20)

        self.lblUsuario = QLabel("INGRESE USUARIO?", self.pnlPrincipal)
        self.lblUsuario.setFont(QFont("Courier New", 9))
        self.lblUsuario.setGeometry(50, 80, 147, 17)

        self.lblContrasena = QLabel("INGRESE CONTRASEÑA?", self.pnlPrincipal)
        self.lblContrasena.setFont(QFont("Courier New", 9))
        self.lblContrasena.setGeometry(50, 120, 147, 17)

        self.cboRol = QComboBox(self.pnlPrincipal)
        self.cboRol.setFont(QFont("Courier New", 8))
        self.cboRol.setGeometry(157, 160, 165, 20)
        self.cboRol.addItem("SELECCIONE ROL")
        self.cboRol.addItem("Administrador")
        self.cboRol.addItem("Cajero")
        self.cboRol.addItem("Almacén")

        self.txtUsuario = QLineEdit(self.pnlPrincipal)
        self.txtUsuario.setGeometry(235, 80, 120, 20)
        self.txtUsuario.setFont(QFont("Courier New", 9))
        self.txtUsuario.setAlignment(Qt.AlignCenter)
        self.txtUsuario.setStyleSheet("color: blue;")

        self.txtContraseña = QLineEdit(self.pnlPrincipal)
        self.txtContraseña.setGeometry(235, 120, 120, 20)
        self.txtContraseña.setFont(QFont("Courier New", 9))
        self.txtContraseña.setAlignment(Qt.AlignCenter)
        self.txtContraseña.setStyleSheet("color: blue;")

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

    def encriptar_contrasena(self, contrasena):
        contrasena_byte = contrasena.encode()
        contrasena_hashed = bcrypt.hashpw(contrasena_byte, bcrypt.gensalt())
        return contrasena_hashed.decode()

    def crear_tabla(self):
        conexion = self.obtener_conexion()
        if conexion is not None:
            try:
                cursor = conexion.cursor()
                sql = """
                    CREATE TABLE IF NOT EXISTS Usuario (
                        id_usuario     INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre_usuario TEXT NOT NULL UNIQUE,
                        contrasena     TEXT NOT NULL,
                        rol            TEXT NOT NULL CHECK (rol IN ('Administrador', 'Cajero', 'Almacén'))
                    );"""
                sql2 = '''
                    CREATE TABLE IF NOT EXISTS Venta (
                        id_venta    INTEGER PRIMARY KEY AUTOINCREMENT,
                        fecha_venta TEXT NOT NULL,
                        total       REAL NOT NULL
                    );''' 
                sql3 = '''
                    CREATE TABLE IF NOT EXISTS Producto (
                        id_producto         INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre_producto     TEXT NOT NULL,
                        precio              REAL NOT NULL,
                        stock               INTEGER NOT NULL
                    );'''
                cursor.execute(sql)
                cursor.execute(sql2)
                cursor.execute(sql3)
                conexion.commit()
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Error al crear la tabla: {e}")
            finally:
                conexion.close()
        else:
            QMessageBox.critical(None, "Error", "Error de conexión con la base de datos.")

    def insert(self):
        conexion = self.obtener_conexion()
        if conexion is not None:
            try:
                cursor = conexion.cursor()
                query = """INSERT INTO Usuario(nombre_usuario, contrasena, rol)
                           VALUES (?, ?, ?);"""
                nombre_usuario = self.txtUsuario.text()
                contrasena = self.txtContraseña.text()
                rol = self.cboRol.currentText()

                if rol == "SELECCIONE ROL":
                    QMessageBox.warning(None, "Advertencia", "Debe seleccionar un rol válido.")
                    return

                cursor.execute(query, (nombre_usuario, self.encriptar_contrasena(contrasena), rol))
                conexion.commit()
                QMessageBox.information(None, "Información", "Usuario insertado correctamente.")
            except sqlite3.IntegrityError as e:
                QMessageBox.critical(None, "Error", f"Error al insertar usuario: {e}")
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
