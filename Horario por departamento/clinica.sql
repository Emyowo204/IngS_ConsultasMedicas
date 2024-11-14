-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

CREATE TABLE persona (
  rut VARCHAR(20) NOT NULL,
  primer_nombre VARCHAR(50) NOT NULL,
  segundo_nombre VARCHAR(50) DEFAULT NULL,
  primer_apellido VARCHAR(50) NOT NULL,
  segundo_apellido VARCHAR(50) DEFAULT NULL,
  fecha_nacimiento DATE NOT NULL,
  PRIMARY KEY (rut)
);

CREATE TABLE departamento (
  ID_Depto VARCHAR(100) NOT NULL,
  nombre_departamento VARCHAR(100) DEFAULT NULL,
  PRIMARY KEY (ID_Depto)
);

CREATE TABLE titulos_disponibles (
  titulo VARCHAR(100) NOT NULL,
  PRIMARY KEY (titulo)
);

CREATE TABLE profesional (
  rut_persona VARCHAR(20) NOT NULL,
  titulo VARCHAR(100) DEFAULT NULL,
  ID_Depto VARCHAR(100) DEFAULT NULL,
  PRIMARY KEY (rut_persona),
  FOREIGN KEY (rut_persona) REFERENCES persona (rut),
  FOREIGN KEY (titulo) REFERENCES titulos_disponibles (titulo),
  FOREIGN KEY (ID_Depto) REFERENCES departamento (ID_Depto)
);

CREATE TABLE paciente (
  rut VARCHAR(20) NOT NULL,
  PRIMARY KEY (rut),
  FOREIGN KEY (rut) REFERENCES persona (rut)
);

CREATE TABLE ficha_clinica (
  codigo_fc INT NOT NULL,
  rut VARCHAR(20) DEFAULT NULL,
  Falta_de_citas INT DEFAULT NULL,
  PRIMARY KEY (codigo_fc),
  FOREIGN KEY (rut) REFERENCES paciente (rut)
);

CREATE TABLE ficha_presenta_diagnostico (
  codigo_fc INT NOT NULL,
  Codigo_RM INT NOT NULL,
  PRIMARY KEY (codigo_fc, Codigo_RM),
  FOREIGN KEY (codigo_fc) REFERENCES ficha_clinica (codigo_fc),
  FOREIGN KEY (Codigo_RM) REFERENCES registro_medico (Codigo_RM)
);

CREATE TABLE registro_medico (
  Codigo_RM INT NOT NULL,
  Documentacion TEXT,
  ID_Cita INT DEFAULT NULL,
  PRIMARY KEY (Codigo_RM),
  FOREIGN KEY (ID_Cita) REFERENCES cita (ID_Cita)
);

CREATE TABLE cita (
  ID_Cita INT NOT NULL,
  codigo_reserva INT DEFAULT NULL,
  codigo_fc INT DEFAULT NULL,
  PRIMARY KEY (ID_Cita),
  FOREIGN KEY (codigo_reserva) REFERENCES reserva (Codigo_reserva),
  FOREIGN KEY (codigo_fc) REFERENCES ficha_clinica (codigo_fc)
);

CREATE TABLE reserva (
  Codigo_reserva INT NOT NULL,
  Bloque INT NOT NULL,
  codigo_agenda INT NOT NULL,
  estado_reserva VARCHAR(50) DEFAULT 'no confirmada',
  rut VARCHAR(20) DEFAULT NULL,
  PRIMARY KEY (Codigo_reserva),
  FOREIGN KEY (rut) REFERENCES persona (rut),
  FOREIGN KEY (Bloque, codigo_agenda) REFERENCES bloque_esta_en_agenda (Bloque, codigo_agenda)
);

CREATE TABLE agenda (
  codigo_agenda INT NOT NULL,
  Dia_a_trabajar DATE NOT NULL,
  Rut_p VARCHAR(20) DEFAULT NULL,
  PRIMARY KEY (codigo_agenda),
  FOREIGN KEY (Rut_p) REFERENCES profesional (rut_persona)
);

CREATE TABLE bloque_horario (
  Numero_bloque INT NOT NULL,
  Hora_inicio TIME NOT NULL,
  Hora_fin TIME NOT NULL,
  PRIMARY KEY (Numero_bloque),
  CHECK (Hora_inicio < Hora_fin)
);

CREATE TABLE bloque_esta_en_agenda (
  Bloque INT NOT NULL,
  codigo_agenda INT NOT NULL,
  PRIMARY KEY (Bloque, codigo_agenda),
  FOREIGN KEY (Bloque) REFERENCES bloque_horario (Numero_bloque),
  FOREIGN KEY (codigo_agenda) REFERENCES agenda (codigo_agenda)
);

CREATE TABLE administrativo (
  rut_persona VARCHAR(20) NOT NULL,
  Cargo VARCHAR(20) DEFAULT NULL,
  PRIMARY KEY (rut_persona),
  FOREIGN KEY (rut_persona) REFERENCES persona (rut)
);

CREATE TABLE administrativo_agenda_reserva (
  rut_persona VARCHAR(20) NOT NULL,
  Codigo_reserva INT NOT NULL,
  PRIMARY KEY (rut_persona, Codigo_reserva),
  FOREIGN KEY (rut_persona) REFERENCES administrativo (rut_persona),
  FOREIGN KEY (Codigo_reserva) REFERENCES reserva (Codigo_reserva)
);

-- Sample data insertions
INSERT INTO persona (rut, primer_nombre, primer_apellido, fecha_nacimiento) 
VALUES 
  ('12345678-9', 'María', 'González', '1980-04-15'),
  ('23456789-0', 'Luis', 'Fernández', '1975-09-20'),
  ('34567890-1', 'Ana', 'Martínez', '1985-06-30'),
  ('45678901-2', 'José', 'Ramírez', '1982-11-12'),
  ('56789012-3', 'Laura', 'Pérez', '1990-02-28'),
  ('67890123-4', 'Roberto', 'Morales', '1978-12-05');

INSERT INTO departamento (ID_Depto, nombre_departamento) 
VALUES 
  ('DEO003', 'Neurologia'), 
  ('DEP001', 'Cardiologia'), 
  ('DEP002', 'Oncologia'),
  ('DEP004', 'Oftalmologia'),
  ('DEP005', 'Urologia'),
  ('DEP006', 'Ginecologia');

INSERT INTO titulos_disponibles (titulo) 
VALUES 
  ('Cardiólogo'), 
  ('Ginecólogo'), 
  ('Neuróloga'), 
  ('Oftalmólogo'), 
  ('Oncóloga'), 
  ('Uróloga');

-- Continue with other necessary inserts as per your data
