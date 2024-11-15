from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# Ruta para mostrar la lista de citas actuales
@app.route('/')
def mostrar_citas():
    conn = sqlite3.connect('clinica.db')
    cursor = conn.cursor()

    # Adjusted query to match existing columns
    query = """
   SELECT 
    A.Dia_a_trabajar AS fecha, 
    B.Hora_inicio AS hora_inicio, 
    B.Hora_fin AS hora_fin, 
    PR.rut_persona AS rut_medico,
    CONCAT(P.primer_nombre, ' ', P.primer_apellido) AS nombre_medico, 
    T.titulo AS titulo_medico,
    R.estado_reserva AS estado_reserva
    FROM 
    Agenda A
    JOIN 
    Bloque_esta_en_agenda BEA ON A.codigo_agenda = BEA.codigo_agenda
    JOIN 
    Bloque_Horario B ON BEA.Bloque = B.Numero_bloque
    LEFT JOIN 
    Reserva R ON BEA.codigo_agenda = R.codigo_agenda AND BEA.Bloque = R.Bloque
    LEFT JOIN 
    Profesional PR ON A.Rut_p = PR.rut_persona
    LEFT JOIN 
    Persona P ON PR.rut_persona = P.rut
    LEFT JOIN 
    Titulos_disponibles T ON PR.titulo = T.titulo
    ORDER BY 
    A.Dia_a_trabajar, 
    B.Hora_inicio;
    """

    cursor.execute(query)
    citas = cursor.fetchall()
    conn.close()

    return render_template('citas.html', citas=citas)

if __name__ == '__main__':
    app.run(debug=True)