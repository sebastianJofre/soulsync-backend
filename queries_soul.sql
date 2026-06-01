CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE parejas (
    id SERIAL PRIMARY KEY,
    usuario_1 INT REFERENCES usuarios(id),
    usuario_2 INT REFERENCES usuarios(id),
    codigo_union VARCHAR(20) UNIQUE NOT NULL,
    fecha_union TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    racha_actual INT DEFAULT 0,
    estado_relacion VARCHAR(50) DEFAULT 'Conexion Inicial'
);

CREATE TABLE preguntas (
    id SERIAL PRIMARY KEY,
    pregunta TEXT NOT NULL,
    categoria VARCHAR(50),
    nivel INT DEFAULT 1,
    activa BOOLEAN DEFAULT TRUE
);

CREATE TABLE respuestas (
    id SERIAL PRIMARY KEY,
    pregunta_id INT REFERENCES preguntas(id),
    usuario_id INT REFERENCES usuarios(id),
    respuesta TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE recompensas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    dias_requeridos INT
);

INSERT INTO preguntas (pregunta, categoria, nivel)
VALUES
('¿Qué fue lo primero que pensaste de mí?', 'conexion', 1),
('¿Qué gesto mío te hace sentir más amado/a?', 'emocional', 1),
('¿Qué sueño te gustaría cumplir conmigo?', 'futuro', 2),
('¿Qué momento contigo nunca olvidaré?', 'recuerdos', 2);