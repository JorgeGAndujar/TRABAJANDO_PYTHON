-- (1) ELIMINAR LA BASE DATOS SI EXISTE

DROP DATABASE IF EXISTS test;

-- (2) CREAR LA BASE DE DATOS SI NO EXISTE

CREATE DATABASE IF NOT EXISTS test;

-- (3) SELECCIONARA LA BASE DE DATOS A USAR

USE test;

-- (4) CREAR LA TABLA SI NO EXISTE

CREATE TABLE IF NOT EXISTS Cliente (
    id_cliente        INT           NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nombre            VARCHAR(50)   NOT NULL,
    edad              INT           NOT NULL,
    ingresos          DECIMAL(10,2) NOT NULL,
    historial_compras INT           NOT NULL 
);

-- (5) MOSTRAR LA ESTRUCTURA DE LA TABLA

DESCRIBE Cliente; 

-- (6) INSERTAR REGISTROS EN LA TABLA

INSERT INTO Cliente (nombre, edad, ingresos, historial_compras) VALUES
('Juan Alva', 25, 50000, 3),
('María Roncal', 30, 75000, 5),
('Pedro Jauregui', 22, 40000, 2),
('Ana Ledezma', 35, 90000, 7),
('Luis Vazquez', 28, 60000, 2),
('Juan Cuba', 25, 60000, 1),
('Ana Prado', 25, 90000, 7),
('Ismael Castillo', 28, 75000, 2),
('María Rabanal', 30, 40000, 2),
('Liz Ponce', 30, 50000, 5);

-- (7) MOSTRAR TODOS LOS REGISTROS

SELECT * FROM Cliente;

-- (8) NOTAS

-- historial_compras: Indica la frecuencia o cantidad de compras que un cliente ha realizado