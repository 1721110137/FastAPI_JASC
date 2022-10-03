CREATE TABLE contactos(
    id_contacto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    telefono VARCHAR(50) NOT NULL
);

INSERT INTO contactos (nombre, email, telefono) VALUES
("Diana", "diana@email.com", "123456789"),
("Luis", "luis@email.com", "123456789"),
("Sandra", "sandra@email.com", "123456789");
