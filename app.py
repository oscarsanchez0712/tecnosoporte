from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tecnosoporte_secret_key_2024'

# ─── Configuración de Base de Datos ───────────────────────────────────────────
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'user': os.environ.get('DB_USER', 'app_user'),
    'password': os.environ.get('DB_PASSWORD', 'AppPassword123!'),
    'database': os.environ.get('DB_NAME', 'soporte_tecnico'),
}

def get_db_connection():
    """Crea y retorna una conexión a MySQL."""
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

# ─── Rutas ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Página principal - listado de todos los tickets."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, cliente, telefono, problema, estado, fecha_registro
            FROM tickets
            ORDER BY fecha_registro DESC
        """)
        tickets = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('index.html', tickets=tickets)
    except Error as e:
        flash(f'Error al conectar con la base de datos: {e}', 'danger')
        return render_template('index.html', tickets=[])


@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo_ticket():
    """Formulario para registrar un nuevo ticket."""
    if request.method == 'POST':
        cliente  = request.form.get('cliente', '').strip()
        telefono = request.form.get('telefono', '').strip()
        problema = request.form.get('problema', '').strip()

        if not cliente or not telefono or not problema:
            flash('Todos los campos son obligatorios.', 'warning')
            return render_template('nuevo.html')

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tickets (cliente, telefono, problema, estado, fecha_registro)
                VALUES (%s, %s, %s, 'Pendiente', NOW())
            """, (cliente, telefono, problema))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Ticket registrado exitosamente.', 'success')
            return redirect(url_for('index'))
        except Error as e:
            flash(f'Error al guardar el ticket: {e}', 'danger')
            return render_template('nuevo.html')

    return render_template('nuevo.html')


@app.route('/editar/<int:ticket_id>', methods=['GET', 'POST'])
def editar_ticket(ticket_id):
    """Actualiza el estado de un ticket existente."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if request.method == 'POST':
            nuevo_estado = request.form.get('estado')
            if nuevo_estado not in ('Pendiente', 'En Proceso', 'Resuelto'):
                flash('Estado no válido.', 'warning')
                return redirect(url_for('index'))

            cursor.execute(
                "UPDATE tickets SET estado = %s WHERE id = %s",
                (nuevo_estado, ticket_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            flash('Estado actualizado correctamente.', 'success')
            return redirect(url_for('index'))

        # GET – cargar datos actuales
        cursor.execute("SELECT * FROM tickets WHERE id = %s", (ticket_id,))
        ticket = cursor.fetchone()
        cursor.close()
        conn.close()

        if not ticket:
            flash('Ticket no encontrado.', 'danger')
            return redirect(url_for('index'))

        return render_template('editar.html', ticket=ticket)

    except Error as e:
        flash(f'Error: {e}', 'danger')
        return redirect(url_for('index'))


@app.route('/eliminar/<int:ticket_id>', methods=['POST'])
def eliminar_ticket(ticket_id):
    """Elimina un ticket (opcional – efectos académicos)."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tickets WHERE id = %s", (ticket_id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Ticket eliminado.', 'success')
    except Error as e:
        flash(f'Error al eliminar: {e}', 'danger')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
