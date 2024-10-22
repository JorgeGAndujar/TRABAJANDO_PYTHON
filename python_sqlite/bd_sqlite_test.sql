-- (1) BORRAR LA TABLA SI EXISTE Y LUEGO CREAR LA TABLA SI NO EXISTE

DROP TABLE IF EXISTS Cliente;

CREATE TABLE IF NOT EXISTS Cliente (
    id_cliente        INTEGER       PRIMARY KEY AUTOINCREMENT,
    nombre            TEXT          NOT NULL,
    edad              INTEGER       NOT NULL,
    ingresos          REAL          NOT NULL,
    historial_compras INTEGER       NOT NULL 
);

-- (2) MOSTRAR LAS TABLAS DE UNA BASE DE DATOS 

SELECT * FROM sqlite_master WHERE type = "table";

-- (3) MOSTRAR LA ESTRUCTURA DE UNA TABLA

PRAGMA table_info(Cliente);

-- (4) INSERTAR REGISTROS EN LA TABLA

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

-- (3) MOSTRAR TODOS LOS REGISTROS

SELECT * FROM Cliente;

-- (4) NOTAS
-- historial_compras: Indica la frecuencia o cantidad de compras que un cliente ha realizado