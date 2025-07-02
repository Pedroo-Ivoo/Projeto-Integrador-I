DROP TABLE IF EXISTS motoristas;
DROP TABLE IF EXISTS regioes;
DROP TABLE IF EXISTS alunos;

CREATE TABLE regioes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(50) NOT NULL
);

CREATE TABLE motoristas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    rota VARCHAR(50) NOT NULL,
    regiao_id INTEGER NOT NULL,
    celular VARCHAR(15) NOT NULL,
    FOREIGN KEY (regiao_id) REFERENCES regioes(id)
);

CREATE TABLE alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    celular VARCHAR(15) NOT NULL,
    regiao_id INTEGER NOT NULL,
    motorista_id INTEGER,
    FOREIGN KEY (regiao_id) REFERENCES regioes(id)
    FOREIGN KEY (motorista_id) REFERENCES motoristas(id)
);

