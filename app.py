from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import UserModel
from models.modelsp import ProductoModel
from Conexion.conexion import get_connection
import mysql.connector
from flask_login import login_required


app = Flask(__name__)
app.secret_key = 'clave_secreta_super_segura'

@app.route('/')
def home():
    return redirect(url_for('login'))

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        clave = request.form['clave']

        if not correo or not clave:
            flash('Por favor completa todos los campos', 'danger')
            return redirect(url_for('login'))

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        usuario = cursor.fetchone()
        conn.close()

        if usuario and check_password_hash(usuario['clave'], clave):
            session['usuario_id'] = usuario['id']
            session['nombre'] = usuario['nombre']
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Correo o contraseña incorrectos', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        clave = request.form['clave']

        hashed_password = generate_password_hash(clave)

        try:
            UserModel.insert_user(nombre, correo, hashed_password)
            flash('Usuario registrado con éxito. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error al registrar usuario: {str(e)}', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        flash('Inicia sesión para acceder al panel', 'warning')
        return redirect(url_for('login'))
    return render_template('dashboard.html', nombre=session['nombre'])

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('login'))

@app.route('/inicio')
@login_required
def inicio():
    return 'Bienvenido a la página principal'

# -------------------------
# CRUD DE PRODUCTOS
# -------------------------

def get_db_connection():
    # Usa la misma función si quieres simplificar (ambas apuntan a MySQL)
    return get_connection()

# Ruta para ver todos los productos
@app.route('/productos')
def productos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()
    return render_template('productos.html', productos=productos)

# Ruta para crear un nuevo producto
@app.route('/crear', methods=['GET', 'POST'])
def crear_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']

        # Validar los datos antes de insertarlos
        if not nombre or not precio or not stock:
            flash('Todos los campos son obligatorios', 'danger')
        else:
            try:
                precio = float(precio)
                stock = int(stock)

                # Conectar a la base de datos y crear el producto
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)',
                               (nombre, precio, stock))
                conn.commit()
                conn.close()
                flash('Producto creado con éxito', 'success')
                return redirect(url_for('productos'))
            except ValueError:
                flash('El precio y el stock deben ser numéricos', 'danger')

    return render_template('formulario.html', action="Crear")

# Ruta para editar un producto
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM productos WHERE id_producto = %s', (id,))
    producto = cursor.fetchone()

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']

        # Validar los datos antes de actualizar
        if not nombre or not precio or not stock:
            flash('Todos los campos son obligatorios', 'danger')
        else:
            try:
                precio = float(precio)
                stock = int(stock)

                # Actualizar el producto
                cursor.execute('UPDATE productos SET nombre = %s, precio = %s, stock = %s WHERE id_producto = %s',
                               (nombre, precio, stock, id))
                conn.commit()
                conn.close()
                flash('Producto actualizado con éxito', 'success')
                return redirect(url_for('productos'))
            except ValueError:
                flash('El precio y el stock deben ser numéricos', 'danger')

    conn.close()
    return render_template('formulario.html', action="Editar", producto=producto)

# Ruta para eliminar un producto
@app.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar_producto(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM productos WHERE id_producto = %s', (id,))
    producto = cursor.fetchone()

    if request.method == 'POST':
        cursor.execute('DELETE FROM productos WHERE id_producto = %s', (id,))
        conn.commit()
        conn.close()
        flash('Producto eliminado con éxito', 'success')
        return redirect(url_for('productos'))

    conn.close()
    return render_template('confirmar_eliminacion.html', producto=producto)

if __name__ == '__main__':
    app.run(debug=True)
