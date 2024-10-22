#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import csv
import json
from tabulate import tabulate


def ejemplo1():
    nra = 'C:\\TRABAJANDO_PYTHON\\python.csv\\trabajador.csv'  # Ajusta la ruta
    # nra = 'C:/TRABAJANDO_PYTHON/python.csv/trabajador.csv'  # Ajusta la ruta 
    try:
        with open(nra, 'r',encoding='UTF-8') as f:
            trabajadores = csv.reader(f, delimiter=';')
            trabajadores_l = list(trabajadores)
            trabajadores_d = {}
            trabajador_ld = []
            for trabajador_l in trabajadores_l:
                trabajador_d = {}
                trabajador_d['id'] = trabajador_l[0]
                trabajador_d['nombre'] = trabajador_l[1]
                trabajador_d['apellido'] = trabajador_l[2]
                trabajador_d['tipo'] = int(trabajador_l[3])
                trabajador_d['sueldo'] = trabajador_l[4]
                trabajador_ld.append(trabajador_d)

            escribir_json(trabajador_ld)

            for trabajador_d in trabajador_ld:
                print(trabajador_d)

    except FileNotFoundError:
        print("ERROR: Archivo no encontrado")
    except Exception as e:
        print(f"ERROR: {e}")

def escribir_json(trabajadores_ld):
    nra = "C:\TRABAJANDO_PYTHON\python_json\datos_trabajador.json"
    with open(nra, 'w') as json_file:
         json.dump(trabajadores_ld, json_file, indent=4)
    print("OK: ESCRIBIR JSON")

def main():
    os.system("cls" if os.name == "nt" else "clear")
    ejemplo1()

if __name__ == "__main__":
    main()
