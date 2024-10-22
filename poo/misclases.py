import math
class Circulo:
    # CONSTRUCTOR (INICIALIZAR LOS ATRIBUTOS DEL OBJETO)
    def __init__(self,radio):
     # self.radio = radio #publico sin raya (TODOS PUEDEN ACCEDER Y MODIFICAR)
       self.__radio = radio #privado con raya(solo con metodos puedes set(poner(modificar)) y get(recuperar(acceder)))
     
    # MÉTODOS (ENCASULADO DENTRO DE LA CLASE)
    def set_radio(self, radio):
        self.__radio = radio

    def get_radio(self):
        return self.__radio
    
    def area(self):
        return math.pi * self.__radio * self.__radio
      # return math.pi * self.__radio ** 2
      # return math.pi * math.pow(self.__radio,2)
    
    # COMO to String
    def __str__(self):
        return f'Radio: {self.__radio} Area: {self.area()}' # return "Radio: " + str(self.radio)

# FUNCION
def area(radio):
    return math.pi * math.pow(radio, 2)

