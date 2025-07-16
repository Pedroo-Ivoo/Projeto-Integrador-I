DROP TABLE IF EXISTS alunos;
DROP TABLE IF EXISTS motoristas;
DROP TABLE IF EXISTS regioes;

CREATE TABLE regioes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL
);

CREATE TABLE motoristas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    rota VARCHAR(50) NOT NULL,
    regiao_id INTEGER NOT NULL,
    celular VARCHAR(15) NOT NULL,
    FOREIGN KEY (regiao_id) REFERENCES regioes(id) ON DELETE CASCADE
);

CREATE TABLE alunos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    celular VARCHAR(15) NOT NULL,
    regiao_id INTEGER NOT NULL,
    motorista_id INTEGER,
    FOREIGN KEY (regiao_id) REFERENCES regioes(id) ON DELETE SET NULL,
    FOREIGN KEY (motorista_id) REFERENCES motoristas(id) ON DELETE SET NULL
);

Insert into regioes (nome)
values ('Norte'),
 		('Sul'),
 		('Leste'),
 		('Oeste');