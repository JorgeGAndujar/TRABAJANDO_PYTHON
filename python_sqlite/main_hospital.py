#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, sqlite3
from tabulate import tabulate

def ejemplo1():
    nra = "C:\\TRABAJANDO_PYTHON\\python_sqlite\\hospital.sqlite3"
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
    nra = "C:\\TRABAJANDO_PYTHON\\python_sqlite\\hospital.sqlite3"
    conexion = None
    try:
        conexion = sqlite3.connect(nra)
        print("OK: CONEXION")
    except sqlite3.Error as error:
        conexion = None
    return conexion

def select1():
    conexion = obtener_conexion()
    if conexion is not None:
       cursor = conexion.cursor() # (cursor)igual que preparedStatement
       try:
            cursor.execute("SELECT nombreMedico, COUNT(*) AS CONSULTAS FROM Consulta GROUP BY nombreMedico ORDER BY nombreMedico;")
            resultados_lt = cursor.fetchall() #(lt de lista de tupla)
            if resultados_lt:
               cabeceras = ['nombre Medico','numero Consultas']
               print(tabulate(resultados_lt, headers=cabeceras, tablefmt='fancy_grid'))
            else:
               print("ERROR: TABLA VACIA")
            
       except Exception as e:
            print("ERROR: SELECT", e)
    else:
       print("ERROR: CONEXION")

def menu():
    while True:
        # Limpia la consola según el sistema operativo
        os.system('cls' if os.name == 'nt' else 'clear')  
        print('MENU')
        print('(1) CREAR TABLAS SEGUN EL AÑO QUE PIDAS')
        print('(2) SALIR')
        opcion = input('Ingrese opción: ')
        
        if opcion == '1':
            os.system('cls' if os.name == 'nt' else 'clear')  # Limpia la consola nuevamente
            crear_tablas()  # Llama a la función crear tablas
            os.system('pause')  # Pausa para que el jugador vea los resultados
        elif opcion == '2':
            os.system('cls' if os.name == 'nt' else 'clear')  # Limpia la consola antes de salir
            print('Gracias por su visita: ADIOS')
            os.system('pause')  # Pausa antes de cerrar
            break  # Sale del bucle y termina el programa
        else:
            print('Opción no válida. Intente de nuevo.')  # Mensaje para opciones inválidas

def crear_tablas():
    conexion = obtener_conexion()
    if conexion is not None:
       cursor = conexion.cursor() # (cursor)igual que preparedStatement
       try:
            query = "SELECT strftime('%Y', fecha), nombreMedico FROM Consulta WHERE strftime('%Y', fecha) = ?"
            input("QUÉ AÑO QUIERES CONSULTAR? ")
            consultas_lt = cursor.fetchall() #(lt de lista de tupla)
            if consultas_lt:
               cabeceras = ['nombre Medico','numero Consultas']
               print(tabulate(consultas_lt, headers=cabeceras, tablefmt='fancy_grid'))
            else:
               print("ERROR: TABLA VACIA")
            
       except Exception as e:
            print("ERROR: SELECT", e)


    else:
       print("ERROR: CONEXION")   

def main():
    os.system("cls")
    menu()
          
if __name__ == "__main__":
   main()