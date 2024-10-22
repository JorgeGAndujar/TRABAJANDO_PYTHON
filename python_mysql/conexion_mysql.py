import os
import mysql.connector
from tabulate import tabulate
import csv

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
        host="localhost",
        port="3307",
        user="root",
        password="12345678",
        database="test")
    except:
        conexion = None
    return conexion


def ejemplo1():
    conexion = None
    try:
        conexion = mysql.connector.connect(
        host="localhost",
        port="3307",
        user="root",
        password="12345678",
        database="test")
    except:
        conexion = None

    if conexion != None:
       print('OK: CONEXION')
       
    else:
       print('ERROR: CONEXION')

# CRUD = CREAR(INSERT) - LEER(SELECT) - ACTUALIZAR(UPDATE) - ELIMINAR(DELETE)

def insert1():
    conexion = obtener_conexion()
    clientes_lt = [
        ("Juan Goycochea", 25, 50000, 3),
        ("María Paredes", 30, 75000, 5)
    ]
    if conexion is not None:
       cursor = conexion.cursor() # (cursor)igual que preparedStatement
       try:
            for cliente_t in clientes_lt:
                query = "INSERT INTO Cliente (nombre, edad, ingresos, historial_compras) \
                         VALUES (%s, %s, %s, %s)"
                cursor.execute(query, cliente_t)
            conexion.commit() # GUARDAR LOS CAMBIOS
            print("OK: INSERT")
            
       except Exception as e:
            print("ERROR: INSERT", e)
    else:
       print("ERROR: CONEXION")

def insert2():
    conexion = obtener_conexion()
    # nombre = input("Ingrese nombre? ")
    # edad = input("Ingrese edad? ")
    # ingresos = input("Ingrese ingresos? ")
    # historial_compras = input("Ingrese historial_compras? ")
    # cliente_t = (nombre, edad , ingresos, historia_compras)
    cliente_t = (input("Ingrese nombre? "),
                 int(input("Ingrese edad? ")),
                 int(input("Ingrese ingresos? ")),
                 int(input("Ingrese historial_compras? ")))
    if conexion is not None:
       cursor = conexion.cursor() # (cursor)igual que preparedStatement
       try:
            query = "INSERT INTO Cliente (nombre, edad, ingresos, historial_compras) \
                         VALUES (%s, %s, %s, %s)"
            cursor.execute(query, cliente_t)
            conexion.commit() # GUARDAR LOS CAMBIOS
            print("OK: INSERT")
            
       except Exception as e:
            print("ERROR: INSERT", e)
    else:
       print("ERROR: CONEXION")

def insert3():
    conexion = obtener_conexion()
    if conexion is not None:
       cursor = conexion.cursor() # (cursor)igual que preparedStatement
       try:
            query = "INSERT INTO Cliente (nombre, edad, ingresos, historial_compras) \
                     VALUES ('Melisa Diaz', 38, 87000, 8)"
            cursor.execute(query)
            conexion.commit() # GUARDAR LOS CAMBIOS
            print("OK: INSERT")
            
       except Exception as e:
            print("ERROR: INSERT", e)
    else:
       print("ERROR: CONEXION")

def insert4():
    nra ="C:\\TRABAJANDO_PYTHON\\python_mysql\clientes.csv"
    if os.path.exists(nra):
       print('OK: ARCHIVO EXISTE')
       try:
         with open(nra,'r',encoding='UTF-8') as f:
              filas = csv.reader(f,delimiter=';')
              filas_l = list(filas)
              for registro_l in filas_l:
                  query = registro_l[0]
                  insert_cliente(query)
       except Exception as e:
           print("ERROR: LECTURA")
    else:
       print("ERROR: ARCHIVO NO EXISTE")    

def insert_cliente(query):
    conexion = obtener_conexion()
    if conexion is not None:
       cursor = conexion.cursor() # (cursor)igual que preparedStatement
       try:
            cursor.execute(query)
            conexion.commit() # GUARDAR LOS CAMBIOS
            print("OK: INSERT")
            
       except Exception as e:
            print("ERROR: INSERT", e)
    else:
       print("ERROR: CONEXION")

def select1():
    conexion = obtener_conexion()
    if conexion is not None:
       cursor = conexion.cursor() # (cursor)igual que preparedStatement
       try:
            cursor.execute("SELECT * FROM Cliente")
            resultados_lt = cursor.fetchall() #(lt de lista de tupla)
            print(resultados_lt)
       except Exception as e:
            print("ERROR: QUERY", e)
    else:
       print("ERROR: CONEXION")

def select2():
    conexion = obtener_conexion()
    if conexion is not None:
       cursor = conexion.cursor() # (cursor)igual que preparedStatement
       try:
            cursor.execute("SELECT * FROM Cliente")
            resultados_lt = cursor.fetchall() #(lt de lista de tupla)
            if resultados_lt:
               cabeceras = ['ID Cliente','Nombre','Edad','Infresos','Historial Compras']
               print(tabulate(resultados_lt, headers=cabeceras, tablefmt='fancy_grid'))
            else:
               print("ERROR: TABLA VACIA")
            
       except Exception as e:
            print("ERROR: SELECT", e)
    else:
       print("ERROR: CONEXION")

def update1():
    conexion = obtener_conexion()
    if conexion is not None:
       cursor = conexion.cursor()
       try:
           query = "UPDATE Cliente SET nombre = %s, edad = %s, ingresos = %s, historial_compras = %s WHERE id_cliente = %s"
           cursor.execute(query,('Delly Lescano',56,45000,8,200))
           conexion.commit() #GUARDAR CAMBIOS
           # VALIDACION PARA COMPROBAR ID
           if cursor.rowcount > 0:
              print("OK: UPDATE")
           else:
              print("NO EXISTE CLIENTE CON ESE ID")
       except Exception as e:
           print("ERROR: UPDATE: ", e)
    else:
       print("ERROR: CONEXION")   

def update2():
    conexion = obtener_conexion()
    if conexion is not None:
       cursor = conexion.cursor()
       try:
           id_cliente = int(input("Ingresar id Cliente a modificar"))
           if buscar_cliente(id_cliente):
              cliente_t = (input("Ingrese nombre? "),
                                int(input("Ingrese edad? ")),
                                int(input("Ingrese ingresos? ")),
                                int(input("Ingrese historial_compras? ")),
                                id_cliente)
                
              query = "UPDATE Cliente SET nombre = %s, edad = %s, ingresos = %s, historial_compras = %s WHERE id_cliente = %s"
              cursor.execute(query,cliente_t)
              conexion.commit() #GUARDAR CAMBIOS
              # VALIDACION PARA COMPROBAR ID
              if cursor.rowcount > 0:
                 print("OK: UPDATE")
              else:
                 print("NO EXISTE CLIENTE CON ESE ID")
           else:
               print("NO EXISTE CLIENTE CON ESE ID")
       except Exception as e:
           print("ERROR: UPDATE: ", e)
    else:
       print("ERROR: CONEXION")   

def buscar_cliente(id_cliente):
    conexion = obtener_conexion()
    if conexion is not None:
        cursor = conexion.cursor() # (cursor)igual que preparedStatement
        try:
                query= "SELECT * FROM Cliente WHERE id_cliente = %s"
                cursor.execute(query,(id_cliente,))
                registro_t = cursor.fetchone()
                if registro_t == None:
                   return False
                else:
                   return True
        except Exception as e:
                print("ERROR: QUERY", e)
    else:
        print("ERROR: CONEXION")


def delete1():
    conexion = obtener_conexion()
    id_cliente_eliminar = int(input("Ingresar id cliente eliminar?"))
    if conexion != None:
       print("OK: CONEXION")
       try:
           query = "DELETE FROM Cliente WHERE id_cliente = %s"
           cursor = conexion.cursor()
           cursor.execute(query,(id_cliente_eliminar,))
           conexion.commit() #GUARDAR LOS CAMBIOS 
           if cursor.rowcount > 0:
              print("OK: CLIENTE ELIMINADO") 
           else:
              print("ERROR: CLIENTE ELIMINADO") 
       except Exception as e:
              print("ERROR: DELETE")
    else:
       print("ERROR: CONEXION") 

def delete2():
    conexion = obtener_conexion()
    historial_compra_eliminar = int(input("Ingresar historial_compras eliminar?"))
    if conexion != None:
       print("OK: CONEXION")
       try:
           query = "DELETE FROM Cliente WHERE historial_compras = %s"
           cursor = conexion.cursor()
           cursor.execute(query,(historial_compra_eliminar,))
           conexion.commit() #GUARDAR LOS CAMBIOS 
           if cursor.rowcount > 0:
              print("OK: TODOS LOS CON HISTORIAL COMPRAS ELIMINADO") 
           else:
              print("ERROR: CLIENTE NO EXISTE CON ESE HISTORIAL DE COMPRAS") 
       except Exception as e:
              print("ERROR: DELETE")
    else:
       print("ERROR: CONEXION")  

def delete3():
    lista_ids = []
    for i in range(37,45,1):
        lista_ids.append(i)
    conexion = obtener_conexion()
    if conexion != None:
       print("OK: CONEXION")
       try:
           cursor = conexion.cursor()
           query = "DELETE FROM Cliente WHERE id_cliente = %s"
           for id_cliente_eliminar in lista_ids:
               cursor.execute(query,(id_cliente_eliminar,))
               conexion.commit() #GUARDAR LOS CAMBIOS 
               if cursor.rowcount > 0:
                  print("OK: CLIENTE ELIMINADO") 
               else:
                  print("ERROR: CLIENTE ELIMINADO") 
       except Exception as e:
              print("ERROR: DELETE")
    else:
       print("ERROR: CONEXION")

def delete4():
    conexion = obtener_conexion()
    if conexion != None:
       print("OK: CONEXION")
       try:
           cursor = conexion.cursor()
           query = "DELETE FROM Cliente WHERE id_cliente = %s"
           while True:
               id_cliente_eliminar = int(input("Ingresar el id_cliente_eliminar ?"))
               cursor.execute(query,(id_cliente_eliminar,))
               conexion.commit() #GUARDAR LOS CAMBIOS 
               if cursor.rowcount > 0:
                  print("OK: CLIENTE ELIMINADO") 
               else:
                  print("CLIENTE NO EXISTE") 
               continuar = input("Desea continuar cualquier letra? y F para terminar ")
               if continuar == "F":
                  break 
       except Exception as e:
              print("ERROR: DELETE")
    else:
       print("ERROR: CONEXION")   

def delete5():
    conexion = obtener_conexion()
    if conexion != None:
       print("OK: CONEXION")
       try:
           cursor = conexion.cursor()
           query = "DELETE FROM Cliente WHERE id_cliente = %s"
           while True:
               id_cliente_eliminar = int(input("Ingresar el id_cliente_eliminar ?, terminar con -1?"))
               if id_cliente_eliminar == -1:
                  break 
               cursor.execute(query,(id_cliente_eliminar,))
               conexion.commit() #GUARDAR LOS CAMBIOS 
               if cursor.rowcount > 0:
                  print("OK: CLIENTE ELIMINADO") 
               else:
                  print("CLIENTE NO EXISTE") 
       except Exception as e:
              print("ERROR: DELETE")
    else:
       print("ERROR: CONEXION")   


def main():
    os.system("cls")
    delete5()
    select2()
          
if __name__ == "__main__":
   main()

