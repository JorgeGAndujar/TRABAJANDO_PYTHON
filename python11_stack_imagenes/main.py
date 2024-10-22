import sys
from PySide6.QtWidgets import (
     QVBoxLayout, QApplication, QMainWindow, QWidget, 
     QLabel, QStackedLayout,QPushButton, QHBoxLayout
)
from PySide6.QtGui import QPixmap

def mostrar_anterior():
    index = layout_stack.currentIndex() # 1
    if index > 0 :
       layout_stack.setCurrentIndex(index -1)
    else:
       layout_stack.setCurrentIndex(layout_stack.count()-1)   # te permite recuperar un bucle , te dirige a la ultima
def mostrar_siguiente():
    index = layout_stack.currentIndex() # 1
    if index < layout_stack.count()-1:
       layout_stack.setCurrentIndex(index + 1)
    else:
       layout_stack.setCurrentIndex(0)
# 0. CONSTRUIR UNA APLICACION

app = QApplication(sys.argv) 

# 1. CREAR LA VENTANA PRINCIPAL

ventana_principal = QMainWindow()

# 2. CREAR UN PANEL PRINCIPAL QWIDGET

panel_principal = QWidget()

# 3. CREAR UN ADMINISTRADOR PRINCIPAL PARA ELL PANEL PRINCIPAL

layout_principal = QVBoxLayout()

# 4. CREAR COMPONENTES Y AÑADIRLOS AL ADMINSTRADOR PRINCIPAL
# crear un layout pila
layout_stack = QStackedLayout()

# PRIMER BLOQUE
imagenes_l = []
ruta_absoluta = "C:\\TRABAJANDO_PYTHON\\python11_stack_imagenes\\imagenes"
for i in range(1,7,1): # ultimo 1 es el incremento
    if i < 10:
       s = "0" + str(i)
    else:
       s = str(i)
    ruta_foto = f"{ruta_absoluta}\\{s}.png" 
    imagenes_l.append(ruta_foto)

for imagen in imagenes_l:
    panel = QWidget()
    layout = QVBoxLayout()
    lblImagen = QLabel()

    pixmap = QPixmap(imagen)

    if pixmap.isNull():
       lblImagen.setText("Imagen no se puede cargar") 
    else:
       lblImagen.setPixmap(pixmap.scaled(500,600)) 
    # AÑADIR AL ADMINISTRADOR
    layout.addWidget(lblImagen)
    panel.setLayout(layout)

    layout_stack.addWidget(panel) # 0, 1, 2, 3, 4, 5

# SEGUNDO BLOQUE
# crear administrador
layout_botones = QHBoxLayout()

btnAnterior = QPushButton("Anterior")
btnSiguiente = QPushButton("Siguiente")
# EVENTOS
btnAnterior.clicked.connect(mostrar_anterior)
btnSiguiente.clicked.connect(mostrar_siguiente)

# agregar btn al administrador
layout_botones.addWidget(btnAnterior)
layout_botones.addWidget(btnSiguiente)

# PONER LOS DOS BLOQUES ANTERIORES AL PRINCIPAL
layout_principal.addLayout(layout_stack)
layout_principal.addLayout(layout_botones)

# 5. PONER EL ADMINISTRADOR PRINCIPAL AL PANEL PRINCIPAL

panel_principal.setLayout(layout_principal)

# 6. PONER EL PANEL PRINCIPAL A LA VENTANA PRINCIPAL

ventana_principal.setCentralWidget(panel_principal)

# 7. MOSTRAR VENTANA PRINCIPAL

ventana_principal.show()

# 8. EJECUTAR APLICACION

sys.exit(app.exec())       