#!/usr/bin/env python
# -*- coding: utf8 -*-
import os, sqlite3

letras_l= ['A','B','C','D']
preguntas_ld = [
   {'pregunta':'¿La función principal del sistema operativo es:?',
    'opciones_l':['Facilitar el uso de la computadora al usuario',
                  'Hacer la programación más fácil para los programadores',
                  'Administrar recursos',
                  'Todas las anteriores '
                ],
    'respuesta': letras_l[3] 
   },
   {'pregunta': '¿Las partes de un sistema operativo son:?',
    'opciones_l':['Núcleo, drivers y programas',
                  'Núcleo, consola de comandos y aplicacione',
                  'Núcleo, intérprete de comandos y sistema de archivos',
                  'Sistema de archivos, compiladores / intérpretes y administrador de recursos'
                 ],
    'respuesta': letras_l[2]   
   },
   {'pregunta': '¿Para poder programar un algoritmo:?',
     'opciones_l':['Debe tener un número infinito de pasos',
                   'Debe tener al menos una salida',
                   'Cada paso debe ser escrito lo más corto posible',
                   'Ninguna de las anteriores'
                 ],
    'respuesta': letras_l[2]    
   },
   {'pregunta': '¿El ensamblador y el código máquina son:?',
     'opciones_l':['Lenguajes de programación de bajo nivel',
                   'Lenguajes de programación de alto nivel',
                   'Parte del sistema operativo',
                   'Entornos de programación'
                 ],
    'respuesta': letras_l[0]    
   },
   {'pregunta': '¿El compilador de Python permite ejecutar un archivo con extensión .py:?',
     'opciones_l':['Siempre que se ejecute como superusuario',
                   'Verdadero',
                   'Falso. Python no tiene compilador',
                   'Falso. Los archivos .py no pueden ser ejecutados'
                 ],
    'respuesta': letras_l[1]    
   },
   {'pregunta': '¿La parte de la computadora responsable de realizar cálculos aritméticos y lógicos se llama:?',
     'opciones_l':['RAM',
                   'CPU',
                   'ROM',
                   'Registros'
                 ],
    'respuesta': letras_l[1]    
   },
   {'pregunta': '¿Qué tipo de salidas de energía tiene el bus GPIO?',
     'opciones_l':['De 3.3V y 5V',
                   'No tiene salidas de energía',
                   'SPI e I2C',
                   'PoE (Power over Ethernet)'
                 ],
    'respuesta': letras_l[0]    
   },
   {'pregunta': '¿La memoria ROM...?',
     'opciones_l':['Es volátil',
                   'Tiene gran capacidad',
                   'Almacena las instrucciones de arranque del procesador',
                   'Almacena el sistema operativo del procesador'
                 ],
    'respuesta': letras_l[2]    
   },
   {'pregunta': '¿El siguiente comando de la consola $ mv blink.py blink2.py?',
     'opciones_l':['Renombra el archivo blink.py como blink2.py',
                   'Es incorrecto',
                   'Renombra el archivo blink2.py como blink.py',
                   'Mueve el archivo blink.py a home'
                 ],
    'respuesta': letras_l[0]    
   },
   {'pregunta': '¿Cuál de las siguientes reglas no es correcta?',
     'opciones_l':['Un símbolo de decisión puede ser alcanzado por varias líneas',
                   'Varias líneas pueden llegar a un símbolo de proceso',
                   'Todos los símbolos deben estar conectados',
                   'Todas las líneas que queramos pueden salir de un símbolo de decisión'
                 ],
    'respuesta': letras_l[3]    
   }
   
]

def obtener_conexion():
    nra = "C:\\TRABAJANDO_PYTHON\\python_sqlite_bancopreguntas\\bancopreguntas.sqlite3"
    conexion = None
    try:
        conexion = sqlite3.connect(nra)
        print("OK: CONEXION")
    except sqlite3.Error as error:
        conexion = None
    return conexion

def crear_tablas_bancopreguntas():
    conexion = obtener_conexion()
    if conexion != None:
        print("OK: CONEXION")
        cursor = conexion.cursor()
        try:
            query_crear_pregunta = '''
                                    CREATE TABLE IF NOT EXISTS Pregunta(
                                        id_pregunta   INTEGER       NOT NULL PRIMARY KEY AUTOINCREMENT,
                                        pregunta      TEXT          NOT NULL,
                                        respuesta     CHAR(1)       NOT NULL
                                    );
                                    '''
            cursor.execute(query_crear_pregunta)
            query_crear_opcion = '''
                                 CREATE TABLE IF NOT EXISTS Opcion (
                                    id_opcion           INTEGER     NOT NULL PRIMARY KEY AUTOINCREMENT,
                                    id_pregunta         INTEGER     NOT NULL,
                                    opcion              TEXT        NOT NULL,
                                    letra               CHAR(1)     NOT NULL,
                                    FOREIGN KEY (id_pregunta) REFERENCES Pregunta (id_pregunta)
                                 );
                                 '''
            cursor.execute(query_crear_opcion)

        except Exception as e:
            print("ERROR: CREATE TABLE")    
    else:
        print("ERROR: CONEXION")

def insertar_datos_bancopreguntas():
    conexion = obtener_conexion()
    if conexion != None:
        cursor = conexion.cursor()
        try:
            query_pregunta = "INSERT INTO Pregunta (pregunta, respuesta) VALUES(?,?);"
            query_opcion = "INSERT INTO Opcion (id_pregunta, opcion, letra) VALUES(?,?,?);"
            for pregunta_d in preguntas_ld:
                pregunta = pregunta_d['pregunta']
                respuesta = pregunta_d['respuesta']
                cursor.execute(query_pregunta,(pregunta,respuesta))
                # GRABAR PREGUNTA Y RESPUESTA (TABLA PREGUNTA)
                id_pregunta = cursor.lastrowid
                opciones_l = pregunta_d['opciones_l']
                for letra, opcion in zip(letras_l,opciones_l):
                    # GRABAR ID_PREGUNTA ,OPCION, LETRA (TABLA OPCION)
                    cursor.execute(query_opcion,(id_pregunta,opcion,letra))
            conexion.commit()
            print("OK: INSERT")
        except Exception as e:
            print("ERROR: INSERT", e)
    else:
        print("ERROR: CONEXION")


       
def main():
    os.system("cls")
    crear_tablas_bancopreguntas()
    insertar_datos_bancopreguntas()
          
if __name__ == "__main__":
   main()