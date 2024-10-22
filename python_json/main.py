#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, json
from tabulate import tabulate

def ejemplo1():
    nra ="C:\\TRABAJANDO_PYTHON\\python_json\\datos.json"
    encabezado =['NOMBRE Y APELLIDO', 'EDAD', 'CURSO']
    with open(nra,'r',encoding='UTF-8') as f:
         filas_l = json.load(f)
         tabla = []
         for fila_d in filas_l:
             fila_l = []
             for clave in fila_d:
                 valor = fila_d[clave]
                 fila_l.append(valor)
             tabla.append(fila_l)
         print(tabulate(tabla, headers=encabezado, tablefmt='fancy_grid',stralign='center'))

def main():
    os.system("cls")
    ejemplo1()
          
if __name__ == "__main__":
   main()