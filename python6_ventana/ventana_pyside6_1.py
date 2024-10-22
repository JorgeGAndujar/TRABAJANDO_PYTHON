# pip install pyside6
# DOCUMENTACIÓN
# https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QWidget.html
import sys
from PySide6.QtWidgets import QWidget, QApplication
'''
app = QApplication(sys.argv)  # CREAR UNA APLICACION
ventana = QWidget() # CREAR UN OBJETO TIPO VENTANA
ventana.show() # MOSTRAR EL OBJETO
sys.exit(app.exec()) # EJECUTA
'''
class Ventana(QWidget):
    def __init__(self):
        super().__init__()

if __name__ == "__main__": # PUNTO DE ENTRADA(Main)
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())

