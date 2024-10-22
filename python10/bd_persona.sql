-- 1. CREAR UNA TABLA

DROP TABLE IF EXISTS Persona;

CREATE TABLE Persona (
  id_persona        INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
  nombre            TEXT     NOT NULL,
  apellido          TEXT     NOT NULL,
  sexo              CHAR(1)  NOT NULL,
  fecha_nacimiento  TEXT
);

INSERT INTO Persona(nombre,apellido,sexo,fecha_nacimiento) VALUES('Luis','Roncal','H','12/05/95');

SELECT * FROM Persona;

