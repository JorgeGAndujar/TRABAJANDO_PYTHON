from abc import ABC, abstractmethod
from tabulate import tabulate

class Trabajador:
      
      def __init__(self, id_trabajador, nombre, apellido):
           self.id_trabajador = id_trabajador
           self.nombre = nombre
           self.apellido = apellido
         
      
      @abstractmethod
      def sueldo(self): # Polimorfismo: Cada hijo lo implementa de manera distina
          pass
      
      @staticmethod
      def mostrar_tabla(trabajadores_lo):
          data = []
          for objeto in trabajadores_lo:
              data.append([objeto.id_trabajador, objeto.nombre, objeto.apellido, objeto.sueldo()])
          cabecera = ["ID TRABAJADOR","NOMBRE","APELLIDO","SUELDO"]
          print(tabulate(data, headers=cabecera, tablefmt='fancy_grid'))

      @staticmethod
      def mostrar_conserje(trabajadores_lo):
          data = []
          for objeto in trabajadores_lo:
              if isinstance(objeto, Conserje):# diferenciar un objeto, filtrar instanciando cada uno(TIPO)
                 data.append([objeto.id_trabajador, objeto.nombre, objeto.apellido, objeto.horas_trabajadas, objeto.sueldo()])
          cabecera = ["ID TRABAJADOR","NOMBRE","APELLIDO","HORAS TRABAJADAS","SUELDO"]
          print(tabulate(data, headers=cabecera, tablefmt='fancy_grid'))

      @staticmethod
      def mostrar_secretaria(trabajadores_lo):
          data = []
          for objeto in trabajadores_lo:
              if isinstance(objeto, Secretaria):# diferenciar un objeto, filtrar instanciando cada uno(TIPO)
                 data.append([objeto.id_trabajador, objeto.nombre, objeto.apellido, objeto.horas_trabajadas, objeto.incentivos, objeto.sueldo()])
          cabecera = ["ID TRABAJADOR","NOMBRE","APELLIDO","HORAS TRABAJADAS","INCENTIVOS","SUELDO"]
          print(tabulate(data, headers=cabecera, tablefmt='fancy_grid'))

      @staticmethod
      def mostrar_directivo(trabajadores_lo):
          data = []
          for objeto in trabajadores_lo:
              if isinstance(objeto, Directivo):# diferenciar un objeto, filtrar instanciando cada uno(TIPO)
                 data.append([objeto.id_trabajador, objeto.nombre, objeto.apellido, objeto.base, objeto.dietas, objeto.metas,objeto.sueldo()])
          cabecera = ["ID TRABAJADOR","NOMBRE","APELLIDO","HORAS TRABAJADAS","BASE","DIETAS","METAS","SUELDO"]
          print(tabulate(data, headers=cabecera, tablefmt='fancy_grid'))
      
class Conserje(Trabajador):
      
      def __init__(self, id_trabajador, nombre, apellido, horas_trabajadas):
          super().__init__(id_trabajador, nombre, apellido)
          self.horas_trabajadas = horas_trabajadas

      def sueldo(self):
          return self.horas_trabajadas * 10
      
      def __str__(self):
          return self.id_trabajador + ';' + self.nombre + ';' + self.apellido + ';' + str(self.horas_trabajadas)
      
     

class Secretaria(Trabajador):
      
      def __init__(self, id_trabajador, nombre, apellido, horas_trabajadas, incentivos):
          super().__init__(id_trabajador, nombre, apellido)
          self.horas_trabajadas = horas_trabajadas
          self.incentivos = incentivos

      def sueldo(self):
          return self.horas_trabajadas * 12 + self.incentivos
      
      def __str__(self):
          return self.id_trabajador + ';' + self.nombre + ';' + self.apellido + ';' + str(self.horas_trabajadas) + ';' + str(self.incentivos)


class Directivo(Trabajador):
      
      def __init__(self, id_trabajador, nombre, apellido, base, dietas, metas):
          super().__init__(id_trabajador, nombre, apellido)
          self.base = base
          self.dietas = dietas
          self.metas = metas

      def sueldo(self):
          return self.base + self.dietas + self.metas
      
      def __str__(self):
          return self.id_trabajador + ';' + self.nombre + ';' + self.apellido + ';' + str(self.base) + ';' + str(self.dietas) + ';' + str(self.metas)