#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, sqlite3
from herencia import Trabajador,Conserje,Secretaria,Directivo

def obtener_conexion():
    nra = "C:\\TRABAJANDO_PYTHON\\poo\\trabajador.sqlite3"
    conexion = None
    try:
        conexion = sqlite3.connect(nra)
        print("OK: CONEXION")
    except sqlite3.Error as error:
        print("ERROR: CONEXION", error)
    return conexion

def obtener_lista_trabajadores_objeto():
    trabajadores_lo = []
    conexion = obtener_conexion()
    if conexion != None:
       cursor = conexion.cursor() 
       try:
           query_trabajador = "SELECT * FROM Trabajador"
           cursor.execute(query_trabajador)
           trabajadores_lt = cursor.fetchall() #siempre regresa en lista de tuplas y con el cursor lo recuperas
           # HACER UN FOR PARA SACAR CADA TUPLA
           for trabajador_t in trabajadores_lt:
               id_trabajador, nombre, apellido = trabajador_t
               cursor.execute('SELECT * FROM Conserje WHERE id_conserje = ?',(id_trabajador,))
               resultado_t = cursor.fetchone()
               if resultado_t:
                  id_trabajador, horas_trabajadas = resultado_t
                  trabajador_o = Conserje(id_trabajador, nombre, apellido, horas_trabajadas)
                  trabajadores_lo.append(trabajador_o)
                  

               cursor.execute('SELECT * FROM Secretaria WHERE id_secretaria = ?',(id_trabajador,))
               resultado_t = cursor.fetchone()
               if resultado_t:
                  id_trabajador, horas_trabajadas, incentivos = resultado_t
                  trabajador_o = Secretaria(id_trabajador, nombre, apellido, horas_trabajadas, incentivos)
                  trabajadores_lo.append(trabajador_o)

               cursor.execute('SELECT * FROM Directivo WHERE id_directivo = ?',(id_trabajador,))
               resultado_t = cursor.fetchone()
               if resultado_t:
                  id_trabajador, metas, dietas, base = resultado_t
                  trabajador_o = Directivo(id_trabajador, nombre, apellido, metas, dietas, base)
                  trabajadores_lo.append(trabajador_o)
               
           return trabajadores_lo
       except Exception as e:
           print("ERROR: SELECT")    
    else:
        print("ERROR: CONEXION")    
    

def ejemplo1():
    pass

def main():
    os.system("cls")
    trabajadores_lo = obtener_lista_trabajadores_objeto()
    '''
    for trabajador_o in trabajadores_lo:
        #print(trabajador_o.nombre, " ", trabajador_o.sueldo())
            print(trabajador_o)
    '''
    Trabajador.mostrar_tabla(trabajadores_lo)
    Trabajador.mostrar_conserje(trabajadores_lo)
    Trabajador.mostrar_secretaria(trabajadores_lo)
    Trabajador.mostrar_directivo(trabajadores_lo)
          
if __name__ == "__main__":
   main()