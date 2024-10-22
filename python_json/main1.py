import os, csv, json
from tabulate import tabulate

def ejemplo1():
    nra = 'C:\\TRABAJANDO_PYTHON\\python.csv\\trabajador.csv'  # Ajusta la ruta
    encabezados = ['id','nombre','apellido','tipo','sueldo']
    try:
        with open(nra, 'r', encoding='UTF-8') as f:
                  trabajadores = csv.reader(f,delimiter=';')
                  trabajadores_l = list(trabajadores)
                  
                  trabajadores_ld = []
                  for trabajador_l in trabajadores_l:
                      trabajador_d = {}
                      trabajador_d[encabezados[0]] = trabajador_l[0] # id
                      trabajador_d[encabezados[1]] = trabajador_l[1] # nombre
                      trabajador_d[encabezados[2]] = trabajador_l[2] # apellido
                      trabajador_d[encabezados[3]] = int(trabajador_l[3]) # tipo
                      trabajador_d[encabezados[4]] = trabajador_l[4] # sueldo
                      trabajadores_ld.append(trabajador_d)

                  escribir_json(trabajadores_ld)
                  
                  for trabajador_d in trabajadores_ld:
                      print(trabajador_d)

                      
    except:
       print("ERROR: LECTURA")

def escribir_json(trabajadores_ld):
    nra = "C:\\TRABAJANDO_PYTHON\\python_json\\trabajadores1.json"
    with open(nra, 'w') as json_file:
         json.dump(trabajadores_ld, json_file, indent=4)
    print("OK: ESCRIBIR JSON")
    

def main():
    os.system("cls")
    ejemplo1()
          
if __name__ == "__main__":
   main()