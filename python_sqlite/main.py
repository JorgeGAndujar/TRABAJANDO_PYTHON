#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, sqlite3

def ejemplo1():
    nra = "C:\\TRABAJANDO_PYTHON\\python_sqlite\\test.sqlite3"
    conexion = None
    try:
        conexion = sqlite3.connect(nra)
        print("OK: CONEXION")
    except sqlite3.Error as error:
        conexion = None
    if conexion is not None:
       print("OK:CONEXION") 
    else:
       print("ERROR: CONEXION") 

def obtener_conexion():
    nra = "C:\\TRABAJANDO_PYTHON\\python_sqlite\\test.sqlite3"
    conexion = None
    try:
        conexion = sqlite3.connect(nra)
        print("OK: CONEXION")
    except sqlite3.Error as error:
        conexion = None
    return conexion

def insert1():
    conexion = obtener_conexion()
    clientes_lt = [
        ("Juan Goycochea", 25, 50000, 3),
        ("María Paredes", 30, 75000, 5)
    ]
    if conexion is not None:
       cursor = conexion.cursor() # (cursor)igual que preparedStatement
       try:
            for cliente_t in clientes_lt:
                query = "INSERT INTO Cliente (nombre, edad, ingresos, historial_compras) \
                         VALUES (?, ?, ?, ?)"
                cursor.execute(query, cliente_t)
            conexion.commit() # GUARDAR LOS CAMBIOS
            print("OK: INSERT")
            
       except Exception as e:
            print("ERROR: INSERT", e)
    else:
       print("ERROR: CONEXION")

def select1():
    conexion = obtener_conexion()
    if conexion is not None:
       cursor = conexion.cursor() # (cursor)igual que preparedStatement
       try:
            cursor.execute("SELECT * FROM Cliente")
            resultados_lt = cursor.fetchall() #(lt de lista de tupla)
            print(resultados_lt)
       except Exception as e:
            print("ERROR: QUERY", e)
    else:
       print("ERROR: CONEXION")

def insert2():
    conexion = obtener_conexion()
    # nombre = input("Ingrese nombre? ")
    # edad = input("Ingrese edad? ")
    # ingresos = input("Ingrese ingresos? ")
    # historial_compras = input("Ingrese historial_compras? ")
    # cliente_t = (nombre, edad , ingresos, historia_compras)
    cliente_t = (input("Ingrese nombre? "),
                 int(input("Ingrese edad? ")),
                 int(input("Ingrese ingresos? ")),
                 int(input("Ingrese historial_compras? ")))
    if conexion is not None:
       cursor = conexion.cursor() # (cursor)igual que preparedStatement
       try:
            query = "INSERT INTO Cliente (nombre, edad, ingresos, historial_compras) \
                         VALUES (?, ?, ?, ?)"
            cursor.execute(query, cliente_t)
            conexion.commit() # GUARDAR LOS CAMBIOS
            print("OK: INSERT")
            
       except Exception as e:
            print("ERROR: INSERT", e)
    else:
       print("ERROR: CONEXION")

def update1():
    conexion = obtener_conexion()
    if conexion is not None:
       cursor = conexion.cursor()
       try:
           query = "UPDATE Cliente SET nombre = ?, edad = ?, ingresos = ?, historial_compras = ?  WHERE id_cliente = ?"
           cursor.execute(query,('Delly Lescano',56,45000,8,1))
           conexion.commit() #GUARDAR CAMBIOS
           # VALIDACION PARA COMPROBAR ID
           if cursor.rowcount > 0:
              print("OK: UPDATE")
           else:
              print("NO EXISTE CLIENTE CON ESE ID")
       except Exception as e:
           print("ERROR: UPDATE: ", e)
    else:
       print("ERROR: CONEXION")   

def delete1():
    conexion = obtener_conexion()
    if conexion != None:
       id_cliente_eliminar = int(input("Ingresar id cliente eliminar?"))
       #print("OK: CONEXION")
       try:
           query = "DELETE FROM Cliente WHERE id_cliente = ?"
           cursor = conexion.cursor()
           cursor.execute(query,(id_cliente_eliminar,))
           conexion.commit() #GUARDAR LOS CAMBIOS 
           if cursor.rowcount > 0:
              print("OK: CLIENTE ELIMINADO") 
           else:
              print("ERROR: CLIENTE ELIMINADO") 
       except Exception as e:
              print("ERROR: DELETE")
    else:
       print("ERROR: CONEXION") 




def main():
    os.system("cls")
    delete1()
    select1()
          
if __name__ == "__main__":
   main()