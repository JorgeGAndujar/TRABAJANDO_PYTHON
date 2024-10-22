#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import csv
from tabulate import tabulate


def ejemplo1():
    nra = 'C:\\TRABAJANDO_PYTHON\\python.csv\\trabajador.csv'  # Ajusta la ruta
    # nra = 'C:/TRABAJANDO_PYTHON/python.csv/trabajador.csv'  # Ajusta la ruta 
    encabezados = ['ID','NOMBRE','APELLIDO','TIPO','SUELDO']
    try:
        with open(nra, 'r',encoding='UTF-8') as f:
            filas = csv.reader(f, delimiter=';')
            filas_l = list(filas)
            print(filas_l)
            tabla = []  

            tipo = input('Ingrese el tipo de trabajador?')
            for i, fila in enumerate(filas_l):
                # print(fila)
                if tipo == fila[3]:
                   tabla.append(fila)
            print(tabulate(tabla, headers=encabezados, tablefmt='fancy_grid'))

    except FileNotFoundError:
        print("ERROR: Archivo no encontrado")
    except Exception as e:
        print(f"ERROR: {e}")

def main():
    os.system("cls" if os.name == "nt" else "clear")
    ejemplo1()

if __name__ == "__main__":
    main()
