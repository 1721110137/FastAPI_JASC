CREATE TABLE contactos(
    id_contacto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(50),
    email VARCHAR(50),
    telefono VARCHAR(50)
);

INSERT INTO contactos (nombre, email, telefono) VALUES
("Diana", "diana@email.com", "123456789"),
("Luis", "luis@email.com", "123456789"),
("Sandra", "sandra@email.com", "123456789");