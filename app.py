from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

# Definir las rutas para cada página
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/horarios')
def horarios():
    conn = sqlite3.connect('bases de datos//clinica.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
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
    conn.close()
    return render_template('horario.html', departments=departments)


@app.route('/cancelar_reserva')
def mostrarcitas():
    conn = sqlite3.connect('bases de datos/clinica.db')
    cursor = conn.cursor()

    query = """
    SELECT 
        R.Codigo_reserva AS id_reserva,
        A.Dia_a_trabajar AS fecha, 
        B.Hora_inicio AS hora_inicio, 
        B.Hora_fin AS hora_fin,
        PR.rut_persona AS rut_medico,
        CONCAT(P.primer_nombre, ' ', P.primer_apellido) AS nombre_medico,
        T.titulo AS titulo_medico,
        R.estado_reserva AS estado_reserva,
        PAC.rut AS rut_paciente,
        CONCAT(PAC_P.primer_nombre, ' ', PAC_P.primer_apellido) AS nombre_paciente
    FROM 
        Reserva R
    JOIN 
        Bloque_esta_en_agenda BEA ON R.codigo_agenda = BEA.codigo_agenda AND R.Bloque = BEA.Bloque
    JOIN 
        Agenda A ON BEA.codigo_agenda = A.codigo_agenda
    JOIN 
        Bloque_Horario B ON BEA.Bloque = B.Numero_bloque
    LEFT JOIN 
        Profesional PR ON A.Rut_p = PR.rut_persona
    LEFT JOIN 
        Persona P ON PR.rut_persona = P.rut
    LEFT JOIN 
        Titulos_disponibles T ON PR.titulo = T.titulo
    LEFT JOIN 
        Persona PAC_P ON R.rut = PAC_P.rut
    LEFT JOIN 
        Paciente PAC ON PAC.rut = PAC_P.rut
    ORDER BY 
        A.Dia_a_trabajar, 
        B.Hora_inicio;
    """
    cursor.execute(query)
    citas = cursor.fetchall()
    conn.close()

    return render_template('cancelar.html', citas=citas)

# Ruta para eliminar la reserva
@app.route('/eliminar_reserva', methods=['POST'])
def eliminar_reserva():
    # Obtener el ID de la reserva desde el formulario
    codigo_reserva = request.form.get('codigo_reserva')

    conn = sqlite3.connect('bases de datos/clinica.db')
    cursor = conn.cursor()

    # Ejecutar las tres consultas DELETE
    try:
        cursor.execute("""
        DELETE FROM Cita
        WHERE codigo_reserva = ?;
        """, (codigo_reserva,))

        cursor.execute("""
        DELETE FROM Administrativo_agenda_Reserva
        WHERE Codigo_reserva = ?;
        """, (codigo_reserva,))

        cursor.execute("""
        DELETE FROM Reserva
        WHERE Codigo_reserva = ?;
        """, (codigo_reserva,))

        conn.commit()  # Confirmar cambios
        mensaje = "Reserva eliminada exitosamente."

    except Exception as e:
        conn.rollback()  # Si hay un error, deshacer cambios
        mensaje = f"Error al eliminar la reserva: {str(e)}"
        print(mensaje)
    
    finally:
        conn.close()

    # Redirigir de vuelta a la lista de citas con el mensaje
    return mostrarcitas()

@app.route('/citas_actuales')
def citas_actuales():
    conn = sqlite3.connect('bases de datos/clinica.db')
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
    app.run(host='0.0.0.0',debug=True)
