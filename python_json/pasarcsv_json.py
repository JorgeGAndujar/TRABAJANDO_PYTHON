import os
import csv
import json

def ejemplo1():
    nra = 'C:\\TRABAJANDO_PYTHON\\python.csv\\trabajador.csv'  # Ajusta la ruta
    try:
        with open(nra, 'r', encoding='UTF-8') as f:
            # Leer los datos del CSV
            trabajadores = csv.reader(f, delimiter=';')
            encabezados = next(trabajadores)  # Leer la primera fila como encabezados

            # Crear una lista de diccionarios para todos los trabajadores
            lista_trabajadores = []
            for fila in trabajadores:
                trabajador = {encabezados[i]: fila[i] for i in range(len(encabezados))}
                lista_trabajadores.append(trabajador)

            # Guardar la lista en un archivo JSON
            with open('C:\\TRABAJANDO_PYTHON\\python_json\\trabajadores.json', 'w', encoding='UTF-8') as json_file:
                json.dump(lista_trabajadores, json_file, ensure_ascii=False, indent=4)

            print("Archivo 'trabajadores.json' creado con éxito.")

    except FileNotFoundError:
        print("ERROR: Archivo no encontrado")
    except Exception as e:
        print(f"ERROR: {e}")

def main():
    os.system("cls" if os.name == "nt" else "clear")
    ejemplo1()

if __name__ == "__main__":
    main()
