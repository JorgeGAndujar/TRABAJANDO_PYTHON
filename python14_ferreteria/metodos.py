import mysql.connector

def obtener_conexion():
    conexion = None
    try:
        print("Intentando conectar a la base de datos...")
        conexion = mysql.connector.connect(
        host="localhost",
        port="3307",
        user="root",
        password="12345678",
        database="ferreteria")
        if conexion.is_connected():
               print("OK: CONEXION")
    except Exception as e:
        print(f"Error de conexión: {e}")
        conexion = None
    return conexion  # Retorna la conexión

def obtener_productos_disponibles():
    conexion = obtener_conexion()
    if conexion != None:
        try:
            cursor = conexion.cursor()
            query = "SELECT id_producto, nombre, precio, stock FROM Producto WHERE stock > 0"
            cursor.execute(query)
            productos_lt = cursor.fetchall()
            productos_disponibles_d = {}
            productos_disponibles_d = {f'{p[0]} - {p[1]}': p for p in productos_lt}
            #print(productos_lt)
        except Exception as e:
            print("ERROR: QUERY SELECT")
    else: 
        print("ERROR: CONEXION")
    return productos_disponibles_d              

if __name__ == "__main__":
    obtener_productos_disponibles()