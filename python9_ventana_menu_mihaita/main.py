import sys, os
from PySide6.QtWidgets import (
    QVBoxLayout, QApplication, QMainWindow, QWidget, 
    QPushButton, QHBoxLayout, QStackedLayout,
)
from PySide6.QtGui import QIcon

from ventana_seleccionfutbol import Ventana as vsf
from ventana_seleccion_futbolista import Ventana as vf
from ventana_seleccion_entrenador import Ventana as ve
from ventana_seleccion_masajista import Ventana as vm

def mostrar_seleccion():
    layout_stack.setCurrentIndex(0)

def mostrar_futbolistas():
    layout_stack.setCurrentIndex(1)

def mostrar_entrenadores():
    layout_stack.setCurrentIndex(2)

def mostrar_masajistas():
    layout_stack.setCurrentIndex(3)

# 0. CONSTRUIR UNA APLICACION
app = QApplication(sys.argv) 

# 1. CREAR LA VENTANA PRINCIPAL
ventana_principal = QMainWindow()
# MODIFICAR EL TAMAÑO
ventana_principal.resize(800,400)
ventana_principal.setWindowTitle("HERENCIA SELECCIÓN FUTBOL")
# CAMBIAR EL ICONO DE LA VENTANA 
ruta_relativa = "python6_ventana/cross1.png"
ruta_absoluta = os.path.abspath(ruta_relativa)
print(ruta_absoluta)
ventana_principal.setWindowIcon(QIcon(ruta_absoluta))

# 2. CREAR UN PANEL PRINCIPAL QWIDGET
panel_principal = QWidget()

# 3. CREAR UN ADMINISTRADOR PRINCIPAL PARA EL PANEL PRINCIPAL
layout_principal = QVBoxLayout()

# 4. CREAR COMPONENTES Y AÑADIRLOS AL ADMINISTRADOR PRINCIPAL

# PANEL SELECCION
panel_seleccion = QWidget()
layout_sf = QVBoxLayout()
ventana = vsf()
tblMostrar = ventana.obtener_tabla()
layout_sf.addWidget(tblMostrar)
panel_seleccion.setLayout(layout_sf)

# PANEL FUTBOLISTA
panel_futbolista = QWidget()
layout_f = QVBoxLayout()
ventana = vf()
tblMostrar = ventana.obtener_tabla()
layout_f.addWidget(tblMostrar)
panel_futbolista.setLayout(layout_f)

# PANEL ENTRENADOR
panel_entrenador = QWidget()
layout_e = QVBoxLayout()
ventana = ve()
tblMostrar = ventana.obtener_tabla()
layout_e.addWidget(tblMostrar)
panel_entrenador.setLayout(layout_e)

# PANEL MASAJISTA
panel_masajista = QWidget()
layout_m = QVBoxLayout()
ventana = vm()
tblMostrar = ventana.obtener_tabla()
layout_m.addWidget(tblMostrar)
panel_masajista.setLayout(layout_m)

# COLOCAR PILA
layout_stack = QStackedLayout()
layout_stack.addWidget(panel_seleccion)  # 0
layout_stack.addWidget(panel_futbolista)  # 1
layout_stack.addWidget(panel_entrenador)  # 2
layout_stack.addWidget(panel_masajista)   # 3

# LAYOUT DE LOS 4 BOTONES
layout_4 = QHBoxLayout()
btn1 = QPushButton("Seleccion Futbol")
btn2 = QPushButton("Futbolistas")
btn3 = QPushButton("Entrenador")
btn4 = QPushButton("Masajista")
btn1.clicked.connect(mostrar_seleccion)
btn2.clicked.connect(mostrar_futbolistas)
btn3.clicked.connect(mostrar_entrenadores)
btn4.clicked.connect(mostrar_masajistas)

layout_4.addWidget(btn1)
layout_4.addWidget(btn2)
layout_4.addWidget(btn3)
layout_4.addWidget(btn4)

layout_principal.addLayout(layout_stack)
layout_principal.addLayout(layout_4)

# 5. PONER EL ADMINISTRADOR PRINCIPAL AL PANEL PRINCIPAL
panel_principal.setLayout(layout_principal)

# 6. PONER EL PANEL PRINCIPAL A LA VENTANA PRINCIPAL
ventana_principal.setCentralWidget(panel_principal)

# 7. MOSTRAR VENTANA PRINCIPAL
ventana_principal.show()

# 8. EJECUTAR APLICACION
sys.exit(app.exec())
