from herencia import Trabajador,Conserje,Secretaria,Directivo
import os, sqlite3
trabajadores_ld =[
{
    "id_trabajador": 'T1',
    "nombre": 'Miguel',
    'tipo_trabajador': 'Conserje',
    'horas_trabajadas': 130
},
{
    "id_trabajador": 'T2',
    "nombre": 'Carlos',
    'tipo_trabajador': 'Conserje',
    'horas_trabajadas': 160
},
{
    "id_trabajador": 'T3',
    "nombre": 'Laura',
    'tipo_trabajador': 'Secretaria',
    'horas_trabajadas': 160,
    'incentivos': 200
},
{
    "id_trabajador": 'T4',
    "nombre": 'María',
    'tipo_trabajador': 'Secretaria',
    'horas_trabajadas': 160,
    'incentivos': 0
},
{
    "id_trabajador": 'T5',
    "nombre": 'Melissa',
    'tipo_trabajador': 'Directivo',
    'base': 5000,
    'dietas': 2000,
    'metas': 1000
},
{
    "id_trabajador": 'T6',
    "nombre": 'Pablo',
    'tipo_trabajador': 'Directivo',
    'base': 4000,
    'dietas': 1000,
    'metas': 1000
}
]
def obtener_conexion():
    nra = "C:\\TRABAJANDO_PYTHON\\poo\\herencia.sqlite3"
    conexion = None
    try:
        conexion = sqlite3.connect(nra)
        print("OK: CONEXION")
    except sqlite3.Error as error:
        print("ERROR: CONEXION", error)
    return conexion

def crear_base_datos():
    conexion = obtener_conexion()
    if conexion is not None:
        print("OK: CONEXION")
        cursor = conexion.cursor()
        try:
            # Crear la tabla Trabajador
            query_trabajador = '''
                                    CREATE TABLE IF NOT EXISTS Trabajador(
                                        id_trabajador      CHAR(5)       NOT NULL PRIMARY KEY,
                                        nombre             TEXT          NOT NULL,
                                        tipo_trabajador    TEXT          NOT NULL,
                                        sueldo             INTEGER       NOT NULL
                                    );
                                    '''
            cursor.execute(query_trabajador)

            # Crear la tabla Conserje
            query_conserje = '''
                                 CREATE TABLE IF NOT EXISTS Conserje (
                                    id_trabajador           CHAR(5)  NOT NULL PRIMARY KEY,
                                    nombre                  TEXT     NOT NULL,
                                    tipo_trabajador         TEXT     NOT NULL,
                                    horas_trabajadas        INTEGER  NOT NULL, 
                                    sueldo                  INTEGER  NOT NULL,
                                    FOREIGN KEY (id_trabajador) REFERENCES Trabajador(id_trabajador)
                                 );
                              '''
            cursor.execute(query_conserje)

            # Crear la tabla Secretaria
            query_secretaria = '''
                                 CREATE TABLE IF NOT EXISTS Secretaria (
                                    id_trabajador           CHAR(5)  NOT NULL PRIMARY KEY,
                                    nombre                  TEXT     NOT NULL,
                                    tipo_trabajador         TEXT     NOT NULL,
                                    horas_trabajadas        INTEGER  NOT NULL,
                                    incentivo               INTEGER,
                                    sueldo                  INTEGER  NOT NULL,
                                    FOREIGN KEY (id_trabajador) REFERENCES Trabajador(id_trabajador)
                                 );
                              '''
            cursor.execute(query_secretaria)

            # Crear la tabla Directivo
            query_directivo = '''
                                 CREATE TABLE IF NOT EXISTS Directivo (
                                    id_trabajador           CHAR(5)  NOT NULL PRIMARY KEY,
                                    nombre                  TEXT     NOT NULL,
                                    tipo_trabajador         TEXT     NOT NULL,
                                    base                    INTEGER  NOT NULL,
                                    metas                   INTEGER,
                                    dietas                  INTEGER,
                                    sueldo                  INTEGER  NOT NULL,
                                    FOREIGN KEY (id_trabajador) REFERENCES Trabajador(id_trabajador)
                                 );
                              '''
            cursor.execute(query_directivo)

        except Exception as e:
            print("ERROR: CREATE TABLE", e)    
    else:
        print("ERROR: CONEXION")

def insertar_datos_trabajador():
    conexion = obtener_conexion()
    if conexion is not None:
        cursor = conexion.cursor()
        try:
            query_trabajador = "INSERT INTO Trabajador (id_trabajador, nombre, tipo_trabajador, sueldo) VALUES(?,?,?,?);"
            for trabajador_d in trabajadores_ld:
                id_trabajador = trabajador_d['id_trabajador']
                nombre = trabajador_d['nombre']
                tipo_trabajador = trabajador_d['tipo_trabajador']
                sueldo = 0  # Aquí puedes calcular el sueldo según el tipo de trabajador, por ahora se asigna 0
                if tipo_trabajador == 'Conserje':
                    sueldo = 1500  # Sueldo base para Conserje
                elif tipo_trabajador == 'Secretaria':
                    sueldo = 2000  # Sueldo base para Secretaria
                elif tipo_trabajador == 'Directivo':
                    sueldo = 5000  # Sueldo base para Directivo
                cursor.execute(query_trabajador, (id_trabajador, nombre, tipo_trabajador, sueldo))
            conexion.commit()
            print("OK: INSERT TRABAJADOR")
        except Exception as e:
            print("ERROR: INSERT TRABAJADOR", e)
        finally:
            cursor.close()
            conexion.close()
    else:
        print("ERROR: CONEXION")


def insertar_datos_conserje():
    conexion = obtener_conexion()
    if conexion is not None:
        cursor = conexion.cursor()
        try:
            query_conserje = "INSERT INTO Conserje (id_trabajador, nombre, tipo_trabajador, horas_trabajadas, sueldo) VALUES(?,?,?,?,?);"
            for trabajador_d in trabajadores_ld:
                if trabajador_d['tipo_trabajador'] == 'Conserje':
                    id_trabajador = trabajador_d['id_trabajador']
                    nombre = trabajador_d['nombre']
                    tipo_trabajador = trabajador_d['tipo_trabajador']
                    horas_trabajadas = trabajador_d['horas_trabajadas']
                    sueldo = 1500  # Sueldo base para Conserje, ajustable
                    cursor.execute(query_conserje, (id_trabajador, nombre, tipo_trabajador, horas_trabajadas, sueldo))
            conexion.commit()
            print("OK: INSERT CONSERJE")
        except Exception as e:
            print("ERROR: INSERT CONSERJE", e)
        finally:
            cursor.close()
            conexion.close()
    else:
        print("ERROR: CONEXION")


def insertar_datos_secretaria():
    conexion = obtener_conexion()
    if conexion is not None:
        cursor = conexion.cursor()
        try:
            query_secretaria = "INSERT INTO Secretaria (id_trabajador, nombre, tipo_trabajador, horas_trabajadas, incentivo, sueldo) VALUES(?,?,?,?,?,?);"
            for trabajador_d in trabajadores_ld:
                if trabajador_d['tipo_trabajador'] == 'Secretaria':
                    id_trabajador = trabajador_d['id_trabajador']
                    nombre = trabajador_d['nombre']
                    tipo_trabajador = trabajador_d['tipo_trabajador']
                    horas_trabajadas = trabajador_d['horas_trabajadas']
                    incentivo = trabajador_d.get('incentivos', 0)
                    sueldo = 2000  # Sueldo base para Secretaria, ajustable
                    cursor.execute(query_secretaria, (id_trabajador, nombre, tipo_trabajador, horas_trabajadas, incentivo, sueldo))
            conexion.commit()
            print("OK: INSERT SECRETARIA")
        except Exception as e:
            print("ERROR: INSERT SECRETARIA", e)
        finally:
            cursor.close()
            conexion.close()
    else:
        print("ERROR: CONEXION")


def insertar_datos_directivo():
    conexion = obtener_conexion()
    if conexion is not None:
        cursor = conexion.cursor()
        try:
            query_directivo = "INSERT INTO Directivo (id_trabajador, nombre, tipo_trabajador, base, metas, dietas, sueldo) VALUES(?,?,?,?,?,?,?);"
            for trabajador_d in trabajadores_ld:
                if trabajador_d['tipo_trabajador'] == 'Directivo':
                    id_trabajador = trabajador_d['id_trabajador']
                    nombre = trabajador_d['nombre']
                    tipo_trabajador = trabajador_d['tipo_trabajador']
                    base = trabajador_d['base']
                    metas = trabajador_d['metas']
                    dietas = trabajador_d['dietas']
                    sueldo = 5000  # Sueldo base para Directivo, ajustable
                    cursor.execute(query_directivo, (id_trabajador, nombre, tipo_trabajador, base, metas, dietas, sueldo))
            conexion.commit()
            print("OK: INSERT DIRECTIVO")
        except Exception as e:
            print("ERROR: INSERT DIRECTIVO", e)
        finally:
            cursor.close()
            conexion.close()
    else:
        print("ERROR: CONEXION")




def ejemplo1():
    for trabajador_d in trabajadores_ld:
        if trabajador_d['tipo_trabajador'] == 'Conserje':
           trabajador = Conserje(trabajador_d['horas_trabajadas']) 
           print(trabajador_d['nombre'],trabajador_d['tipo_trabajador'],' Sueldo: ', trabajador.sueldo())
        if trabajador_d['tipo_trabajador'] == 'Secretaria':
           trabajador = Secretaria(trabajador_d['horas_trabajadas'],trabajador_d['incentivos']) 
           print(trabajador_d['nombre'],trabajador_d['tipo_trabajador'],' Sueldo: ', trabajador.sueldo())
        if trabajador_d['tipo_trabajador'] == 'Directivo':
           trabajador = Directivo(trabajador_d['base'],trabajador_d['dietas'],trabajador_d['metas']) 
           print(trabajador_d['nombre'],trabajador_d['tipo_trabajador'],' Sueldo: ', trabajador.sueldo())

def main():
    os.system("cls")
    # ejemplo1()
    crear_base_datos()


          
if __name__ == "__main__":
   main()
