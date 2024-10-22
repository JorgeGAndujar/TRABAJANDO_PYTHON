import os, random
from misclases import Circulo, area


def ejemplo1():
    c1 = Circulo(random.randint(1,100))
    print("Radio: ", c1.radio)
    c1.radio = 20
    print("Radio: ", c1.radio)

def ejemplo2():
    # CREAS OBJETOS Y LO METES EN UNA LISTA
    lista_objetos = []
    for i in range(100):
        c = Circulo(random.randint(1,100))
        lista_objetos.append(c)
    
    # LLAMAS A LOS OBJETOS
    i = 0 # inicializar el contador
    for objeto in lista_objetos:
        i = i + 1 # incremento
        print(f'Objeto {i}',"Radio: ",objeto.radio)

def ejemplo3():
    c1 = Circulo(random.randint(1,10))
    print(c1.get_radio()) #get para recuperar(acceder)
    # print(c1.__radio) no se puede porque es privado
    c1.set_radio(20) # para modificar el atributo
    print(c1.get_radio())

def ejemplo4():
    radio = int(input("Ingresar radio? "))
    c = Circulo(radio)
    print("Radio: ", c.get_radio())
    print("Area: ", c.area())
    print(c)
    # llamando a la funcion
    print("Area (llamar funcion): ", area(radio))

def main():
    ejemplo4()
          
if __name__ == "__main__":
   main()