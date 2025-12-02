from flask import Flask, render_template, request, redirect, url_for, session, flash
from db_connection import get_db_connection
import mysql.connector
import hashlib

app = Flask(__name__)
app.secret_key = 'mi_secreto'  # Cambia esto por un valor seguro


@app.route('/contactar', methods=['GET', 'POST'])
def contactar():
    if 'username' not in session:
        flash('Debes iniciar sesión para acceder.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        celular = request.form['cel']
        horario = request.form['horario']
        tipo_ganado = request.form['tipo_ganado']

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO solicitudes (nombre, correo, celular, horario, tipo_ganado)
            VALUES (%s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (nombre, correo, celular, horario, tipo_ganado))
            conn.commit()
            flash('Tu solicitud fue enviada correctamente. Pronto nos pondremos en contacto.')
        except mysql.connector.Error as err:
            flash(f'Error al guardar la solicitud: {err}')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('dashboard'))

    return render_template('contactar.html', username=session['username'])


@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))
    cursor.close()
    conn.close()

# Ruta para el dashboard
@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()
    if 'username' not in session:
        flash('Debes iniciar sesión para acceder.')
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])
    cursor.close()
    conn.close()

@app.route('/productos')
def productos():
    return render_template('productos.html')  # Implementar la vista de productos

@app.route('/carrito')
def carrito():
    return render_template('carrito.html')  # Implementar la vista del carrito

# Ternero/a
@app.route('/ternero')
def ternero():
    if 'username' not in session:
        flash('Debes iniciar sesión para acceder.')
        return redirect(url_for('login'))
    lote_info = {
        'tipo': 'Ternero/a',
        'descripcion': 'Bovino joven generalmente al pie de la madre',
        'cantidad': 12,
        'precio': 'Gs. 1.200.000 por unidad'
    }
    return render_template('ternero.html', username=session['username'], lote=lote_info)

# Novillito
@app.route('/novillito')
def novillito():
    if 'username' not in session:
        flash('Debes iniciar sesión para acceder.')
        return redirect(url_for('login'))
    lote_info = {
        'tipo': 'Novillito',
        'descripcion': 'Macho castrado de más de dos años',
        'cantidad': 8,
        'precio': 'Gs. 2.000.000 por unidad'
    }
    return render_template('novillito.html', username=session['username'], lote=lote_info)


@app.route('/novillo')
def novillo():
    if 'username' not in session:
        flash('Debes iniciar sesión para acceder.')
        return redirect(url_for('login'))
    lote_info = {
        'tipo': 'Novillo',
        'descripcion': 'Macho castrado con más desarrollo que el novillito',
        'cantidad': 8,
        'precio': 'Gs. 3.200.000 por unidad'
    }
    return render_template('novillo.html', username=session['username'], lote=lote_info)

# Vaquillona
@app.route('/vaquillona')
def vaquillona():
    if 'username' not in session:
        flash('Debes iniciar sesión para acceder.')
        return redirect(url_for('login'))
    lote_info = {
        'tipo': 'Vaquillona',
        'descripcion': 'Hembra desde el destete hasta su primera parición',
        'cantidad': 10,
        'precio': 'Gs. 2.500.000 por unidad'
    }
    return render_template('vaquillona.html', username=session['username'], lote=lote_info)

# Vaca
@app.route('/vaca')
def vaca():
    if 'username' not in session:
        flash('Debes iniciar sesión para acceder.')
        return redirect(url_for('login'))
    lote_info = {
        'tipo': 'Vaca',
        'descripcion': 'Hembra adulta',
        'cantidad': 15,
        'precio': 'Gs. 3.000.000 por unidad'
    }
    return render_template('vaca.html', username=session['username'], lote=lote_info)

# Toro
@app.route('/toro')
def toro():
    if 'username' not in session:
        flash('Debes iniciar sesión para acceder.')
        return redirect(url_for('login'))
    lote_info = {
        'tipo': 'Toro',
        'descripcion': 'Macho entero (no castrado)',
        'cantidad': 5,
        'precio': 'Gs. 4.000.000 por unidad'
    }
    return render_template('toro.html', username=session['username'], lote=lote_info)


# Ruta para registro de usuario
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash de la contraseña
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insertar usuario en la base de datos
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        try:
            cursor.execute(query, (username, hashed_password))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            return f"Error: {err}"

    return render_template('register.html')

# Ruta para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash de la contraseña
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar usuario y contraseña
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, hashed_password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Usuario o contraseña incorrectos"

    return render_template('login.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)