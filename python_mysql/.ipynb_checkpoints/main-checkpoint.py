#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, mysql.connector


def obtener_conexion():
    conexion = None
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            port="3307",
            user="root",
            password="12345678",
            database="test0001"
        )
    except:
        conexion = None
    if conexion != None:
       print("OK: CONEXION")
    else:
       print("ERROR: CONEXION")   

def main():
    conexion = obtener_conexion()

if __name__ == "__main__":
   main()

