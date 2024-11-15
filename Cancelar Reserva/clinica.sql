-- Poblar la tabla Departamento
INSERT INTO Departamento (ID_Depto, nombre_departamento)
VALUES
('DEP001', 'Cardiología'),
('DEP002', 'Neurología'),
('DEP003', 'Medicina Interna'),
('DEP004', 'Pediatría');

-- Poblar la tabla Titulos_disponibles
INSERT INTO Titulos_disponibles (titulo)
VALUES
('Doctor en Medicina'),
('Especialista en Medicina Interna'),
('Especialista en Neurología Pediátrica'),
('Máster en Neurología Clínica');

-- Poblar la tabla Persona
INSERT INTO Persona (rut, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, fecha_nacimiento)
VALUES
('11111111-1', 'Juan', 'Carlos', 'Pérez', 'López', '1980-05-12'),
('22222222-2', 'María', 'Fernanda', 'Gómez', 'Ramírez', '1990-03-08'),
('33333333-3', 'Pedro', 'Luis', 'Hernández', 'Martínez', '1985-10-22'),
('44444444-4', 'Ana', 'Sofía', 'García', 'Castro', '1992-07-15');

-- Poblar la tabla Cuenta
INSERT INTO Cuenta (usuario, password, correo, telefono, rut_persona)
VALUES
('jcperez', 'password123', 'juan.perez@mail.com', '123456789', '11111111-1'),
('mfgomez', 'password456', 'maria.gomez@mail.com', '987654321', '22222222-2'),
('plhernandez', 'password789', 'pedro.hernandez@mail.com', '456789123', '33333333-3'),
('asgarcia', 'password321', 'ana.garcia@mail.com', '789123456', '44444444-4');

-- Poblar la tabla Profesional
INSERT INTO Profesional (rut_persona, titulo, ID_Depto)
VALUES
('11111111-1', 'Doctor en Medicina', 'DEP001'),
('22222222-2', 'Especialista en Neurología Pediátrica', 'DEP002'),
('33333333-3', 'Especialista en Medicina Interna', 'DEP003'),
('44444444-4', 'Máster en Neurología Clínica', 'DEP004');

-- Poblar la tabla Administrativo
INSERT INTO Administrativo (rut_persona, Cargo) 
VALUES 
('11111111-1', 'Recepción'), 
('22222222-2', 'Coord. Agenda');
-- Poblar la tabla Paciente
INSERT INTO Paciente (rut)
VALUES
('33333333-3'),
('44444444-4');

-- Poblar la tabla Bloque_Horario
INSERT INTO Bloque_Horario (Numero_bloque, Hora_inicio, Hora_fin)
VALUES
(1, '08:00:00', '09:00:00'),
(2, '09:00:00', '10:00:00'),
(3, '10:00:00', '11:00:00'),
(4, '11:00:00', '12:00:00'),
(5, '12:00:00', '13:00:00'),
(6, '13:00:00', '14:00:00'),
(7, '14:00:00', '15:00:00'),
(8, '15:00:00', '16:00:00'),
(9, '16:00:00', '17:00:00');


-- Poblar la tabla Agenda
INSERT INTO Agenda (codigo_agenda, Dia_a_trabajar, Rut_p)
VALUES
(101, '2024-11-12', '11111111-1'),
(102, '2024-11-13', '22222222-2');

-- Poblar la tabla Ficha_Clinica
INSERT INTO Ficha_Clinica (codigo_fc, rut, Falta_de_citas)
VALUES
(1001, '33333333-3', 2),
(1002, '44444444-4', 0);

-- Poblar la tabla Bloque_esta_en_agenda
INSERT INTO Bloque_esta_en_agenda (Bloque, codigo_agenda)
VALUES
(1, 101),
(2, 102);

-- Poblar la tabla Reserva
INSERT INTO Reserva (Codigo_reserva, Bloque, codigo_agenda, estado_reserva, rut)
VALUES
(1, 1, 101, 'confirmada', '33333333-3'),
(2, 2, 102, 'no confirmada', '44444444-4');

-- Poblar la tabla Administrativo_agenda_Reserva
INSERT INTO Administrativo_agenda_Reserva (rut_persona, Codigo_reserva)
VALUES
('22222222-2', 1),
('11111111-1', 2);

-- Poblar la tabla Cita
INSERT INTO Cita (ID_Cita, codigo_reserva, codigo_fc)
VALUES
(1, 1, 1001),
(2, 2, 1002);

-- Poblar la tabla Registro_medico
INSERT INTO Registro_medico (Codigo_RM, Documentacion, ID_Cita)
VALUES
(10001, 'Diagnóstico inicial: Hipertensión', 1),
(10002, 'Diagnóstico inicial: Migraña crónica', 2);

-- Poblar la tabla Ficha_presenta_diagnostico
INSERT INTO Ficha_presenta_diagnostico (codigo_fc, Codigo_RM)
VALUES
(1001, 10001),
(1002, 10002);
