from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# Conectar a la base de datos SQLite (archivo en el proyecto)
DATABASE_PATH = 'clinica.db'

def get_db_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre
    return connection

@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
    SELECT d.nombre_departamento, p.primer_nombre, p.primer_apellido, a.Dia_a_trabajar, bh.Hora_inicio, bh.Hora_fin
    FROM Departamento d
    JOIN Profesional pr ON pr.ID_Depto = d.ID_Depto
    JOIN Persona p ON p.rut = pr.rut_persona
    JOIN Agenda a ON a.Rut_p = pr.rut_persona
    JOIN Bloque_esta_en_agenda bea ON bea.codigo_agenda = a.codigo_agenda
    JOIN Bloque_Horario bh ON bh.Numero_bloque = bea.Bloque
    ORDER BY d.nombre_departamento, a.Dia_a_trabajar, bh.Hora_inicio;
    """
    cursor.execute(query)
    resultados = cursor.fetchall()

    # Estructura de datos para pasar al HTML
    departments = {}
    for row in resultados:
        departamento = row['nombre_departamento']
        if departamento not in departments:
            departments[departamento] = []
        departments[departamento].append({
            "nombre": row['primer_nombre'],
            "apellido": row['primer_apellido'],
            "dia": row['Dia_a_trabajar'],
            "hora_inicio": row['Hora_inicio'],
            "hora_fin": row['Hora_fin']
        })

    cursor.close()
    connection.close()
    return render_template('horario-consulta.html', departments=departments)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
