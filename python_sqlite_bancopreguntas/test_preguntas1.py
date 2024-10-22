import random, os, re, sqlite3
# Conexión a la base de datos
def obtener_conexion():
    nra = "C:\\TRABAJANDO_PYTHON\\python_sqlite_bancopreguntas\\bancopreguntas.sqlite3"
    conexion = None
    try:
        conexion = sqlite3.connect(nra)
        print("OK: CONEXION")
    except sqlite3.Error as error:
        print("ERROR: CONEXION", error)
    return conexion

letras_l = ['A','B','C','D']
preguntas_l = []

def construir_lista_preguntas():
    conexion = obtener_conexion()
    if conexion != None:
       cursor = conexion.cursor()
       try:
           query_pregunta = "SELECT * FROM Pregunta"
           cursor.execute(query_pregunta)
           respuestas_lt = cursor.fetchall()
           for respuesta_t in respuestas_lt:
               pregunta_d = {}
               id_pregunta,pregunta,respuesta = respuesta_t
               query_opcion = "SELECT opcion FROM Opcion WHERE id_pregunta = ?"
               cursor.execute(query_opcion,(id_pregunta,))
               opciones_t = cursor.fetchall()
               lista = [] 
               for opcion in opciones_t:
                   print(opcion)
                   lista.append(opcion[0])
               pregunta_d['pregunta'] = pregunta
               pregunta_d['opciones_l'] = lista
               pregunta_d['respuesta'] = respuesta
               preguntas_l.append(pregunta_d)
       except Exception as e:
              print("ERROR: QUERY")     
    else:
       print("ERROR: CONEXION")     

def menu():
    while True:
          os.system('cls')
          print('MENU')
          print('(1) MOSTRAR TODAS LAS PREGUNTAS')
          print('(2) TEST')
          print('(3) SALIR')
          
          opcion = input('Ingrese opción? ')

          if opcion == '1':
             os.system('cls');opcion1();os.system('pause')
          elif opcion == '2':
             os.system('cls');opcion2();os.system('pause')
          elif opcion == '3':
              os.system('cls')
              print('Gracias por su visita: ADIOS')
              os.system('pause')
              break
          
def opcion1():
    for index,pregunta_d in enumerate(preguntas_l):
        print((index+1),":",pregunta_d['pregunta'])

def opcion2():
    while True:
          numero_preguntas_aleatorias = int(input('Ingrese numero de preguntas? '))
          if numero_preguntas_aleatorias > len(preguntas_l):
             continue
          preguntasaleatorias_l = obtener_preguntas_aleatoria(preguntas_l, numero_preguntas_aleatorias)
          puntaje = 0
          correcta = 0
          for index,pregunta_d in enumerate(preguntasaleatorias_l):
              print(str((index+1))+') '+pregunta_d['pregunta'])
              for i, opcion_s in enumerate(pregunta_d['opciones_l']):
                  print(letras_l[i],'. ',opcion_s)
              print()
              respuesta_usuario = entrada_opcion('Ingrese su respuesta?')
              if respuesta_usuario != "":
                 if respuesta_usuario == pregunta_d['respuesta']:
                    puntaje += 1
                    correcta += 1
                 else:
                    puntaje -= 0.25
          print("Puntaje: ", puntaje)
          print(correcta, " correctas de ", len(preguntasaleatorias_l))
def entrada_opcion(mensaje): 
    patron = '(A|B|C|D|)'
    opcion = ""
    while True:
          opcion = input(mensaje).upper()
          correcto = re.fullmatch(patron,opcion)
          if not correcto:
             print('Error: Solo debe de ingresar A,B,C,D')
          else:
             break
    return opcion

def obtener_preguntas_aleatoria(preguntas_l, numero_preguntas_aleatorias):
    return random.sample(preguntas_l, numero_preguntas_aleatorias)
             

def main():
    construir_lista_preguntas()
    menu()
          
if __name__ == "__main__":
   main()

'''
for index,pregunta_d in enumerate(preguntas_l):
    print((index+1),":",pregunta_d['pregunta'])

print()

preguntas_aleatorias_l = random.sample(preguntas_l,3)

for index,pregunta_d in enumerate(preguntas_aleatorias_l):
    print((index+1),":",pregunta_d['pregunta'])
'''