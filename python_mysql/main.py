#!/usr/bin/env python
# -*- coding: utf8 -*-

import mysql.connector

def obtener_conexion():
    conexion = None
    try:
        print("Intentando conectar a la base de datos...")
        conexion = mysql.connector.connect(
            host="localhost",
            port=3307,
            user="root",
            password="12345678",
            database="test0001"
        )
        if conexion.is_connected():
            print("OK: CONEXION")
    except Exception as e:
        print(f"Error de conexión: {e}")
        conexion = None
    return conexion  # Retorna la conexión

def obtener_cliente(cliente_id):
    print(f"Buscando cliente con ID: {cliente_id}...")
    conexion = obtener_conexion()  # Usa la función para obtener la conexión
    if conexion is None:
        print("No se pudo establecer conexión. Terminando la función.")
        return  # Si no hay conexión, termina la función

    cursor = None
    try:
        cursor = conexion.cursor()
        query = "SELECT id, nombre, email FROM clientes WHERE id = %s"
        cursor.execute(query, (cliente_id,))
        cliente = cursor.fetchone()  # Obtener un solo registro
        if cliente:
            print(f"ID: {cliente[0]}, Nombre: {cliente[1]}, Email: {cliente[2]}")
        else:
            print("Cliente no encontrado.")
    except Exception as e:
        print(f"Error al obtener el cliente: {e}")
    finally:
        if cursor:
            cursor.close()
        if conexion.is_connected():
            conexion.close()


def main():
    cliente_id = 1  # Cambia este ID según sea necesario
    obtener_cliente(cliente_id)

if __name__ == "__main__":
   main()
