import random, os, re, sqlite3

# Definir la lista de letras
letras_l = ['A', 'B', 'C', 'D']

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

# Función para obtener todas las preguntas y opciones de la base de datos
def obtener_preguntas_bd():
    conexion = obtener_conexion()
    preguntas = []
    if conexion is not None:
        cursor = conexion.cursor()
        try:
            # Consulta para obtener las preguntas y sus opciones
            query = """
                SELECT p.id_pregunta, p.pregunta, o.opcion, o.letra, p.respuesta 
                FROM Pregunta p 
                JOIN Opcion o ON p.id_pregunta = o.id_pregunta
                ORDER BY p.id_pregunta, o.letra;
            """
            cursor.execute(query)
            datos = cursor.fetchall()
            
            # Procesar datos para estructurarlos en una lista de preguntas con opciones
            preguntas_dict = {}
            for pregunta_id, pregunta, opcion, letra, respuesta_correcta in datos:
                if pregunta_id not in preguntas_dict:
                    preguntas_dict[pregunta_id] = {
                        "pregunta": pregunta,
                        "opciones_l": [],
                        "respuesta": respuesta_correcta
                    }
                preguntas_dict[pregunta_id]["opciones_l"].append(opcion)
            
            preguntas = list(preguntas_dict.values())
            
        except Exception as e:
            print("ERROR en la consulta:", e)
        finally:
            conexion.close()
    else:
        print("ERROR: CONEXION")
    return preguntas

# Menú principal
def menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('MENU')
        print('(1) MOSTRAR TODAS LAS PREGUNTAS')
        print('(2) TEST')
        print('(3) SALIR')
        
        opcion = input('Ingrese opción? ')

        if opcion == '1':
            os.system('cls' if os.name == 'nt' else 'clear')
            opcion1()
            input("Presione Enter para continuar...")
        elif opcion == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            opcion2()
            input("Presione Enter para continuar...")
        elif opcion == '3':
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Gracias por su visita: ADIOS')
            break
        else:
            print("Opción no válida.")

# Opción para mostrar todas las preguntas
def opcion1():
    preguntas = obtener_preguntas_bd()
    if preguntas:
        for index, pregunta_d in enumerate(preguntas):
            print((index + 1), ":", pregunta_d['pregunta'])
            for i, opcion in enumerate(pregunta_d['opciones_l']):
                print(f"   {letras_l[i]}. {opcion}")
    else:
        print("No hay preguntas disponibles.")

# Opción para realizar un test con preguntas aleatorias
def opcion2():
    preguntas = obtener_preguntas_bd()
    if not preguntas:
        print("No hay preguntas cargadas.")
        return
    
    while True:
        try:
            numero_preguntas_aleatorias = int(input('Ingrese número de preguntas? '))
            if numero_preguntas_aleatorias > len(preguntas):
                print(f"Solo hay {len(preguntas)} preguntas disponibles.")
                continue
            
            preguntas_aleatorias = obtener_preguntas_aleatoria(preguntas, numero_preguntas_aleatorias)
            puntaje = 0
            correcta = 0
            for index, pregunta_d in enumerate(preguntas_aleatorias):
                print(f"{index+1}) {pregunta_d['pregunta']}")
                for i, opcion_s in enumerate(pregunta_d['opciones_l']):
                    print(f"{letras_l[i]}. {opcion_s}")
                respuesta_usuario = entrada_opcion("Ingrese su respuesta: ")
                if respuesta_usuario == pregunta_d['respuesta']:
                    puntaje += 1
                    correcta += 1
                else:
                    puntaje -= 0.25
            print(f"\nPuntaje: {puntaje}")
            print(f"{correcta} correctas de {len(preguntas_aleatorias)}")
            break
        except ValueError:
            print("Por favor ingrese un número válido.")

# Validación de la entrada de opciones
def entrada_opcion(mensaje): 
    patron = '(A|B|C|D)'
    while True:
        opcion = input(mensaje).upper()
        if re.fullmatch(patron, opcion):
            return opcion
        print('Error: Solo debe de ingresar A, B, C o D')

# Selección de preguntas aleatorias
def obtener_preguntas_aleatoria(preguntas, numero_preguntas_aleatorias):
    return random.sample(preguntas, numero_preguntas_aleatorias)

# Función principal
def main():
    menu()
          
if __name__ == "__main__":
    main()
