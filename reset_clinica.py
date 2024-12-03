import sqlite3

# Conectar a la base de datos (se creará si no existe)
conn = sqlite3.connect('bases de datos//clinica.db')
cursor = conn.cursor()

# Eliminar datos de las tablas dependientes
cursor.execute("DELETE FROM Ficha_presenta_diagnostico;")
cursor.execute("DELETE FROM Registro_medico;")
cursor.execute("DELETE FROM Cita;")
cursor.execute("DELETE FROM Administrativo_agenda_Reserva;")
cursor.execute("DELETE FROM Reserva;")
cursor.execute("DELETE FROM Bloque_esta_en_agenda;")
cursor.execute("DELETE FROM Ficha_Clinica;")
cursor.execute("DELETE FROM Agenda;")

# Eliminar datos de tablas relacionadas con entidades
cursor.execute("DELETE FROM Paciente;")
cursor.execute("DELETE FROM Administrativo;")
cursor.execute("DELETE FROM Profesional;")
cursor.execute("DELETE FROM Cuenta;")

# Eliminar datos de tablas maestras
cursor.execute("DELETE FROM Bloque_Horario;")
cursor.execute("DELETE FROM Titulos_disponibles;")
cursor.execute("DELETE FROM Departamento;")
cursor.execute("DELETE FROM Persona;")

# Confirmar los cambios
conn.commit()

# Cerrar la conexión
conn.close()