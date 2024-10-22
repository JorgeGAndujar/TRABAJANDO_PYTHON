import os, random, re
def menu():
    while True:
          os.system('cls')
          print('MENU')
          print('(1) JUGAR PIEDRA-PAPEL-TIJERA')
          print('(2) SALIR')
          
          opcion = input('Ingrese opción? ')

          if opcion == '1':
             os.system('cls');jugar();os.system('pause')
          elif opcion == '2':
              os.system('cls')
              print('Gracias por su visita: ADIOS')
              os.system('pause')
              break
def jugar():
    numero_jugadas = int(input('Cuantas jugadas desea realizar?'))
    empate = 0; ganador = 0; perdedor = 0
    for i in range(numero_jugadas):
        maquina = random.choice(['piedra','papel','tijera'])
        usuario = entrada_usuario('Usuario: Ingrese piedra, papel o tijera?: ' + str((i+1))+ " : ")
        resultado = obtener_resultado_juego(usuario, maquina)
        if resultado == 'EMPATE':
           empate += 1
        elif resultado == 'GANAR':
           ganador += 1
        else:
           perdedor += 1 
    print("Empate : ", empate)
    print("Ganastes: ", ganador)
    print("Perdistes: ", perdedor)

def entrada_usuario(mensaje):
    patron = '(piedra|papel|tijera)'
    cadena = ''
    while True:
          cadena = input(mensaje).lower()
          correcto = re.fullmatch(patron,cadena)
          if not correcto:
             print('Error: Debe ingresar piedra, papel, tijera') 
          else:
             break
    return cadena 

def obtener_resultado_juego(usuario, maquina):
    if usuario == maquina:
       return "EMPATE"
    elif (usuario == 'piedra' and maquina == 'tijera ')or \
         (usuario == 'papel' and maquina == 'piedra ')or \
         (usuario == 'tijera' and maquina == 'papel '):
         return "GANAR"
    else:
         return "PERDER"

def main():
    menu()
          
if __name__ == "__main__":
   main()        