from flask import Flask, jsonify, render_template, request,redirect, url_for,flash,session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesiones'

# Definir las rutas para cada página
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pacientes')
def centro_de_acciones():
    return render_template('paciente.html')

@app.route('/admin')
def admin():
    return render_template('index_admin.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Capturar los datos del formulario
        usuario = request.form['usuario']
        password = request.form['password']

        # Conectar a la base de datos
        conn = sqlite3.connect('bases de datos/clinica.db')
        cursor = conn.cursor()

        # Consultar si el usuario y contraseña coinciden
        query = "SELECT * FROM Cuenta WHERE usuario = ? AND password = ?"
        cursor.execute(query, (usuario, password))
        cuenta = cursor.fetchone()
        conn.close()

        if cuenta:  # Si existe la cuenta
            session['usuario'] = usuario  # Guardar al usuario en la sesión
            flash('Inicio de sesión exitoso', 'success')
            return redirect('/admin')
        else:  # Si no coincide la cuenta
            flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('login.html')

@app.route('/api/profesionales', methods=['GET'])
def obtener_profesionales():
    connection = sqlite3.connect('bases de datos//clinica.db')
    cursor = connection.cursor()
    try:
        # Consulta para obtener los datos de profesionales
        query = """
            SELECT 
                p.primer_nombre, p.segundo_nombre, p.primer_apellido, p.segundo_apellido, 
                t.titulo, d.nombre_departamento
            FROM 
                Profesional prof
            JOIN Persona p ON prof.rut_persona = p.rut
            JOIN Titulos_disponibles t ON prof.titulo = t.titulo
            JOIN Departamento d ON prof.ID_Depto = d.ID_Depto;
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        # Estructurar los datos como JSON
        profesionales = [
            {
                'nombre': f"{fila[0]} {fila[1] or ''} {fila[2]} {fila[3] or ''}".strip(),
                'titulo': fila[4],
                'departamento': fila[5]
            }
            for fila in resultados
        ]
        return jsonify(profesionales)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/api/departamentos', methods=['GET'])
def obtener_departamentos():
    connection = sqlite3.connect('bases de datos//clinica.db')
    cursor = connection.cursor()
    try:
        # Consulta para obtener los departamentos
        query = """
            SELECT ID_Depto, nombre_departamento
            FROM Departamento;
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        # Estructurar los datos como JSON
        departamentos = [
            {'id': fila[0], 'nombre': fila[1]} for fila in resultados
        ]
        return jsonify(departamentos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


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

@app.route('/consola_administrativos')
def consola_administrativos():
    conn = sqlite3.connect('bases de datos/clinica.db')
    cursor = conn.cursor()

    cursor.execute("SELECT rut, primer_nombre || ' ' || primer_apellido AS nombre FROM Persona WHERE rut IN (SELECT rut_persona FROM Profesional)")
    medicos = cursor.fetchall()
    print("Medicos:", medicos)  # Línea de depuración

    cursor.execute("SELECT rut, primer_nombre || ' ' || primer_apellido AS nombre FROM Persona WHERE rut IN (SELECT rut FROM Paciente)")
    pacientes = cursor.fetchall()
    print("Pacientes:", pacientes)  # Línea de depuración

    cursor.close()
    conn.close()

    administrativo_nombre = "Juan Pérez"  # Nombre del administrativo predeterminado
    return render_template('consola_administrativos.html', medicos=medicos, pacientes=pacientes, administrativo_nombre=administrativo_nombre)

@app.route('/dias_disponibles')
def dias_disponibles():
    medico = request.args.get('medico')
    print("Medico seleccionado:", medico)  # Línea de depuración
    conn = sqlite3.connect('bases de datos/clinica.db')
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT Dia_a_trabajar FROM Agenda WHERE Rut_p = ?", (medico,))
    dias = [row[0] for row in cursor.fetchall()]
    print("Días disponibles:", dias)  # Línea de depuración

    cursor.close()
    conn.close()
    return jsonify(dias=dias)

@app.route('/horas_disponibles')
def horas_disponibles():
    medico = request.args.get('medico')
    dia = request.args.get('dia')
    print("Medico seleccionado:", medico)  # Línea de depuración
    print("Día seleccionado:", dia)  # Línea de depuración
    conn = sqlite3.connect('bases de datos/clinica.db')
    cursor = conn.cursor()

    # Paso 1: Verificar los datos en la tabla Agenda
    cursor.execute("SELECT * FROM Agenda WHERE Rut_p = ? AND Dia_a_trabajar = ?", (medico, dia))
    agenda_data = cursor.fetchall()
    print("Datos de Agenda:", agenda_data)  # Línea de depuración

    # Paso 2: Verificar los datos en la tabla Bloque_esta_en_agenda
    cursor.execute("""
    SELECT BEA.* FROM Bloque_esta_en_agenda BEA
    JOIN Agenda A ON BEA.codigo_agenda = A.codigo_agenda
    WHERE A.Rut_p = ? AND A.Dia_a_trabajar = ?
    """, (medico, dia))
    bloque_data = cursor.fetchall()
    print("Datos de Bloque_esta_en_agenda:", bloque_data)  # Línea de depuración

    # Paso 3: Verificar los datos en la tabla Bloque_Horario
    cursor.execute("""
    SELECT B.* FROM Bloque_Horario B
    JOIN Bloque_esta_en_agenda BEA ON B.Numero_bloque = BEA.Bloque
    JOIN Agenda A ON BEA.codigo_agenda = A.codigo_agenda
    WHERE A.Rut_p = ? AND A.Dia_a_trabajar = ?
    """, (medico, dia))
    horario_data = cursor.fetchall()
    print("Datos de Bloque_Horario:", horario_data)  # Línea de depuración

    # Paso 4: Verificar los datos en la tabla Reserva
    cursor.execute("""
    SELECT R.* FROM Reserva R
    JOIN Bloque_esta_en_agenda BEA ON R.codigo_agenda = BEA.codigo_agenda AND R.Bloque = BEA.Bloque
    JOIN Agenda A ON BEA.codigo_agenda = A.codigo_agenda
    WHERE A.Rut_p = ? AND A.Dia_a_trabajar = ?
    """, (medico, dia))
    reserva_data = cursor.fetchall()
    print("Datos de Reserva:", reserva_data)  # Línea de depuración

    # Consulta original
    query = """
    SELECT B.Hora_inicio || ' - ' || B.Hora_fin AS hora
    FROM Agenda A
    JOIN Bloque_esta_en_agenda BEA ON A.codigo_agenda = BEA.codigo_agenda
    JOIN Bloque_Horario B ON BEA.Bloque = B.Numero_bloque
    LEFT JOIN Reserva R ON BEA.codigo_agenda = R.codigo_agenda AND BEA.Bloque = R.Bloque
    WHERE A.Rut_p = ? AND A.Dia_a_trabajar = ? AND (R.Codigo_reserva IS NULL OR R.estado_reserva != 'confirmada')
    ORDER BY B.Hora_inicio
    """
    cursor.execute(query, (medico, dia))
    horas = [row[0] for row in cursor.fetchall()]
    print("Horas disponibles:", horas)  # Línea de depuración

    cursor.close()
    conn.close()
    return jsonify(horas=horas)

@app.route('/reservar_cita', methods=['POST'])
def reservar_cita():
    medico = request.form.get('medico')
    paciente = request.form.get('paciente')
    dia = request.form.get('dia')
    hora = request.form.get('hora')
    print("Datos de la reserva - Medico:", medico, "Paciente:", paciente, "Día:", dia, "Hora:", hora)  # Línea de depuración

    conn = sqlite3.connect('bases de datos/clinica.db')
    cursor = conn.cursor()

    # Obtener el bloque y agenda correspondientes
    cursor.execute("""
    SELECT BEA.Bloque, A.codigo_agenda
    FROM Agenda A
    JOIN Bloque_esta_en_agenda BEA ON A.codigo_agenda = BEA.codigo_agenda
    JOIN Bloque_Horario B ON BEA.Bloque = B.Numero_bloque
    WHERE A.Rut_p = ? AND A.Dia_a_trabajar = ? AND B.Hora_inicio || ' - ' || B.Hora_fin = ?
    """, (medico, dia, hora))
    bloque, codigo_agenda = cursor.fetchone()
    print("Bloque y código de agenda obtenidos:", bloque, codigo_agenda)  # Línea de depuración

    # Insertar la reserva
    cursor.execute("""
    INSERT INTO Reserva (Bloque, codigo_agenda, estado_reserva, rut)
    VALUES (?, ?, 'no confirmada', ?)
    """, (bloque, codigo_agenda, paciente))
    codigo_reserva = cursor.lastrowid
    print("Código de reserva generado:", codigo_reserva)  # Línea de depuración

    # Insertar en Administrativo_agenda_Reserva
    cursor.execute("""
    INSERT INTO Administrativo_agenda_Reserva (rut_persona, Codigo_reserva)
    VALUES ('11111111-1', ?)
    """, (codigo_reserva,))  # Administrativo predeterminado

    conn.commit()
    cursor.close()
    conn.close()

    return "Reserva realizada exitosamente"

# Ruta para mostrar el formulario de login
@app.route('/login_profesional', methods=['GET','POST'])
def login_profesional():
    if request.method == 'POST':
        rut = request.form['rut']
        password = request.form['password']
        
        query = """
            SELECT * 
            FROM Cuenta 
            WHERE rut_persona = ? AND password = ?
        """
        params = (rut, password)

        conn = sqlite3.connect('bases de datos/clinica.db')
        cuenta = conn.execute(query, params).fetchone()
        conn.close()

        if cuenta is None:
            flash('RUT o Contraseña incorrecta', 'error')
            return redirect(url_for('login_profesional'))
        else:
            return redirect(url_for('mostrar_citas', rut_medico=rut))

    return render_template('login_profesional.html')

@app.route('/citas_medico')
def mostrar_citas():
    rut_medico = request.args.get('rut_medico')
    
    query = """
        SELECT 
            Agenda.dia_a_trabajar AS fecha,
            Bloque_Horario.hora_inicio AS hora_inicio,
            Bloque_Horario.hora_fin AS hora_fin,
            Profesional.rut_persona AS rut_medico,
            Persona.primer_nombre || ' ' || Persona.primer_apellido AS nombre_medico,
            Titulos_disponibles.titulo AS titulo_medico,
            Reserva.estado_reserva AS estado_reserva
        FROM Agenda
        JOIN Bloque_esta_en_agenda ON Agenda.codigo_agenda = Bloque_esta_en_agenda.codigo_agenda
        JOIN Bloque_Horario ON Bloque_esta_en_agenda.bloque = Bloque_Horario.numero_bloque
        LEFT JOIN Reserva ON Bloque_esta_en_agenda.codigo_agenda = Reserva.codigo_agenda
                          AND Bloque_esta_en_agenda.bloque = Reserva.bloque
        LEFT JOIN Profesional ON Agenda.rut_p = Profesional.rut_persona
        LEFT JOIN Persona ON Profesional.rut_persona = Persona.rut
        LEFT JOIN Titulos_disponibles ON Profesional.titulo = Titulos_disponibles.titulo
    """
    
    if rut_medico:
        query += " WHERE Profesional.rut_persona = ?"
        params = (rut_medico,)
    else:
        params = ()

    query += " ORDER BY Agenda.dia_a_trabajar, Bloque_Horario.hora_inicio"

    conn = sqlite3.connect('bases de datos/clinica.db')
    results = conn.execute(query, params).fetchall()
    conn.close()

    return render_template('citas.html', results=results)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
