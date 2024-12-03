import sqlite3
import random
from datetime import datetime, timedelta

# Conectar a la base de datos (se creará si no existe)
conn = sqlite3.connect('bases de datos//clinica.db')
cursor = conn.cursor()

# Poblar la tabla Departamento
cursor.execute("""
INSERT INTO Departamento (ID_Depto, nombre_departamento)
VALUES
('DEP001', 'Cardiología'),
('DEP002', 'Neurología'),
('DEP003', 'Medicina Interna'),
('DEP004', 'Pediatría');
""")

# Poblar la tabla Titulos_disponibles
cursor.execute("""
INSERT INTO Titulos_disponibles (titulo)
VALUES
('Doctor en Medicina'),
('Especialista en Medicina Interna'),
('Especialista en Neurología Pediátrica'),
('Máster en Neurología Clínica');
""")

# Poblar la tabla Persona
cursor.execute("""
INSERT INTO Persona (rut, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, fecha_nacimiento)
VALUES
('11111111-1', 'Juan', 'Carlos', 'Pérez', 'López', '1980-05-12'),
('22222222-2', 'María', 'Fernanda', 'Gómez', 'Ramírez', '1990-03-08'),
('33333333-3', 'Pedro', 'Luis', 'Hernández', 'Martínez', '1985-10-22'),
('44444444-4', 'Ana', 'Sofía', 'García', 'Castro', '1992-07-15'),
('55555555-5', 'Luis', 'Miguel', 'Rodríguez', 'Sánchez', '1983-01-17'),
('66666666-6', 'Laura', 'Beatriz', 'Martín', 'González', '1987-09-23'),
('77777777-7', 'Carlos', 'Eduardo', 'Fernández', 'Ruiz', '1991-11-30'),
('88888888-8', 'Elena', 'Patricia', 'Díaz', 'Morales', '1995-04-05');
""")

# Poblar la tabla Cuenta
cursor.execute("""
INSERT INTO Cuenta (usuario, password, correo, telefono, rut_persona)
VALUES
('jcperez', 'password123', 'juan.perez@mail.com', '123456789', '11111111-1'),
('mfgomez', 'password456', 'maria.gomez@mail.com', '987654321', '22222222-2'),
('plhernandez', 'password789', 'pedro.hernandez@mail.com', '456789123', '33333333-3'),
('asgarcia', 'password321', 'ana.garcia@mail.com', '789123456', '44444444-4'),
('lmrodriguez', 'password654', 'luis.rodriguez@mail.com', '321654987', '55555555-5'),
('lbmartin', 'password987', 'laura.martin@mail.com', '654987321', '66666666-6'),
('cefernandez', 'password321', 'carlos.fernandez@mail.com', '789456123', '77777777-7'),
('epdiaz', 'password654', 'elena.diaz@mail.com', '123789456', '88888888-8');
""")

# Poblar la tabla Profesional
cursor.execute("""
INSERT INTO Profesional (rut_persona, titulo, ID_Depto)
VALUES
('11111111-1', 'Doctor en Medicina', 'DEP001'),
('22222222-2', 'Especialista en Neurología Pediátrica', 'DEP002'),
('55555555-5', 'Especialista en Medicina Interna', 'DEP003'),
('66666666-6', 'Máster en Neurología Clínica', 'DEP004');
""")

# Poblar la tabla Administrativo
cursor.execute("""
INSERT INTO Administrativo (rut_persona, Cargo)
VALUES
('33333333-3', 'Recepción'),
('77777777-7', 'Coord. Agenda');
""")

# Poblar la tabla Paciente
cursor.execute("""
INSERT INTO Paciente (rut)
VALUES
('44444444-4'),
('88888888-8');
""")

# Poblar la tabla Bloque_Horario
cursor.execute("""
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
(9, '16:00:00', '17:00:00'),
(10, '17:00:00', '18:00:00'),
(11, '18:00:00', '19:00:00'),
(12, '19:00:00', '20:00:00');
""")


# Poblar la tabla Agenda con más días por médico
start_date = datetime.strptime('2024-11-12', '%Y-%m-%d')
medicos = ['11111111-1', '22222222-2', '55555555-5', '66666666-6']
codigo_agenda = 105

for medico in medicos:
    for _ in range(50):  # 50 additional days per medico
        random_days = random.randint(0, 30)
        dia_a_trabajar = start_date + timedelta(days=random_days)
        cursor.execute("""
        INSERT INTO Agenda (codigo_agenda, Dia_a_trabajar, Rut_p)
        VALUES (?, ?, ?);
        """, (codigo_agenda, dia_a_trabajar.strftime('%Y-%m-%d'), medico))
        codigo_agenda += 1

# Poblar la tabla Bloque_esta_en_agenda
for codeA in range(105, 305):  # Asegúrate de que este rango cubra todos los códigos de agenda
    for Bloq in range(1, 13):
        cursor.execute("""
        INSERT INTO Bloque_esta_en_agenda (Bloque, codigo_agenda)
        VALUES (?, ?);
        """, (Bloq, codeA))


# Poblar la tabla Ficha_Clinica
cursor.execute("""
INSERT INTO Ficha_Clinica (codigo_fc, rut, Falta_de_citas)
VALUES
(1001, '44444444-4', 2),
(1002, '88888888-8', 0);
""")

# Poblar la tabla Reserva
cursor.execute("""
INSERT INTO Reserva (Codigo_reserva, Bloque, codigo_agenda, estado_reserva, rut)
VALUES
(1, 1, 101, 'confirmada', '44444444-4'),
(2, 2, 102, 'no confirmada', '88888888-8');
""")

# Poblar la tabla Administrativo_agenda_Reserva
cursor.execute("""
INSERT INTO Administrativo_agenda_Reserva (rut_persona, Codigo_reserva)
VALUES
('33333333-3', 1),
('77777777-7', 2);
""")

# Poblar la tabla Cita
cursor.execute("""
INSERT INTO Cita (ID_Cita, codigo_reserva, codigo_fc)
VALUES
(1, 1, 1001),
(2, 2, 1002);
""")

# Poblar la tabla Registro_medico
cursor.execute("""
INSERT INTO Registro_medico (Codigo_RM, Documentacion, ID_Cita)
VALUES
(10001, 'Diagnóstico inicial: Hipertensión', 1),
(10002, 'Diagnóstico inicial: Migraña crónica', 2);
""")

# Poblar la tabla Ficha_presenta_diagnostico
cursor.execute("""
INSERT INTO Ficha_presenta_diagnostico (codigo_fc, Codigo_RM)
VALUES
(1001, 10001),
(1002, 10002);
""")

# Confirmar los cambios
conn.commit()

# Cerrar la conexión
conn.close()