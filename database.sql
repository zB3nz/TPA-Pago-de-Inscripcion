DROP DATABASE IF EXISTS sys_inscripciones;

CREATE DATABASE sys_inscripciones;
use sys_inscripciones;

CREATE TABLE administradores(
    id int(25) auto_increment not null,
    usuario varchar(32) not null,
    password varchar(255) not null,
    CONSTRAINT pk_administradores PRIMARY KEY(id),
    /* unique */
    CONSTRAINT uq_usuario UNIQUE(usuario)
)ENGINE = InnoDb;

CREATE TABLE alumnos(
    noControl int(10) not null,
    nombre varchar(100) not null,
    apellidos varchar(255) not null,
    carrera varchar(255) not null,
    adeudo int not null,
    email varchar(255),
    CONSTRAINT pk_alumnos PRIMARY KEY(noControl)
)ENGINE = InnoDb ;