#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, sqlite3

def menu():

    while True:
        os.system('cls')
        print('(1) ELIMINAR TABLAS')
        print('(2) CREAR TABLAS')
        print('(3) INSERTAR REGISTROS EN TABLAS')
        print('(4) MOSTRAR INGRESANDO EL NOMBRE DE LA TABLA')
        print('(5) SALIR')
        
        opcion = input('Ingrese opción? ')

        if opcion == '1':
             os.system('cls');eliminar_tablas();os.system('pause')
        elif opcion == '2':
             os.system('cls');crear_tablas();os.system('pause')
        elif opcion == '3':
             os.system('cls');insertar_registros();os.system('pause')
        elif opcion == '4':
             os.system('cls');mostrar_registros_tablas();os.system('pause')
        elif opcion == '5':
             break

def obtener_conexion():
    nra = "C:\\TRABAJANDO_PYTHON\\python_sqlite\\hospital.sqlite3"
    conexion = None
    try:
        conexion = sqlite3.connect(nra)
        print("OK: CONEXION")
    except sqlite3.Error as error:
        conexion = None
    return conexion


def eliminar_tablas():
    print('ELIMINAR TABLAS')
    print('---------------')
    conexion = obtener_conexion()
    if conexion != None:
       cursor = conexion.cursor()
       try:
           query = "SELECT DISTINCT strftime('%Y', fecha) FROM Consulta;"
           cursor.execute(query)
           resultados_lt = cursor.fetchall() #(lt de lista de tupla)
           for resultado_t in resultados_lt: # sacar de la lt el valor de la tupla
               year = resultado_t[0]
               query_tabla = '''DROP TABLE CONSULTA''' + year 
               cursor.execute(query_tabla)
               conexion.commit()
               print("OK: DROP TABLE ", year)

       except Exception as e:
           print('ERROR: DROP TABLE') 
    else:
       print("ERROR: CONEXION") 


def crear_tablas():
    print('CREAR TABLAS')
    print('------------')
    conexion = obtener_conexion()
    if conexion != None:
       cursor = conexion.cursor()
       try:
           query = "SELECT DISTINCT strftime('%Y', fecha) FROM Consulta;"
           cursor.execute(query)
           resultados_lt = cursor.fetchall() #(lt de lista de tupla)
           for resultado_t in resultados_lt: # sacar de la lt el valor de la tupla
               year = resultado_t[0]

               query_tabla = '''CREATE TABLE CONSULTA'''+ year + ''' (
                                 numeroConsulta TEXT(10) NOT NULL,
                                 fecha          TEXT     NOT NULL,
                                 nombreMedico   TEXT(50) NOT NULL,
                                 deinpr         TEXT(20) NOT NULL,
                                 procedencia    TEXT(20) NOT NULL,
                                 PRIMARY KEY (numeroConsulta)
                                );
                             '''
               cursor.execute(query_tabla)
               print("OK: CREATE TABLE ", year)

       except Exception as e:
           print('ERROR: CREATE TABLE') 
    else:
       print("ERROR: CONEXION") 

def insertar_registros():
    print('INSERTAR REGISTROS')
    print('------------------')
    conexion = obtener_conexion()
    if conexion != None:
       cursor = conexion.cursor()
       try:
           query = "SELECT numeroConsulta, fecha, nombreMedico, deinpr, procedencia  FROM Consulta"
           cursor.execute(query)
           resultados_lt = cursor.fetchall() #(lt de lista de tupla)
           fecha = []
           for resultado_t in resultados_lt:
               fecha = resultado_t[1] # 2012-01-01
               partes = fecha.split('-') # [2012, 01, 01]
               grabar_registro(resultado_t, partes[0],conexion)
       except Exception as e:
           print('ERROR: INSERT') 
    else:
       print("ERROR: CONEXION") 

def grabar_registro(resultado_t, year, conexion):
    try:
        cursor = conexion.cursor()
        query = "INSERT INTO CONSULTA" + year + "(numeroConsulta, fecha, nombreMedico, deinpr, procedencia) VALUES (?,?,?,?,?)"
        cursor.execute(query, resultado_t)
        conexion.commit()
        print("OK: INSERT")
    except Exception as e:
        print("ERROR: INSERT" ,e)


def mostrar_registros_tablas():
    print('MOSTRAR REGISTROS TABLA')
    print('-----------------------')
    nombre_tabla = input("Ingresar nombre de la tabla a mostrar? ")
    conexion = obtener_conexion()
    if conexion != None:
       cursor = conexion.cursor()
       try:
           query = f"SELECT * FROM {nombre_tabla}"
           cursor.execute(query)
           resultados_lt = cursor.fetchall()
           for resultado_t in resultados_lt:
               print(resultado_t)
           print("OK: SELECT")
       except Exception as e:
           print("ERROR: SELECT")
    else:
       print("ERROR: CONEXION") 



def main():
    os.system("cls")
    menu()
          
if __name__ == "__main__":
   main()