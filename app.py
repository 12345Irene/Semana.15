from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from Conexion.conexion import get_connection
from models.modelsp import obtener_productos

app = Flask(__name__)
app.secret_key = 'secret_key'


# Conexión a la base de datos MySQL
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345',  # Asegúrate de cambiar esto por tu contraseña de MySQL
        database='desarrollo'
    )
    return conn


# Ruta principal de la página
@app.route('/')
def index():
    return redirect(url_for('productos'))


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
        # Eliminar el producto
        cursor.execute('DELETE FROM productos WHERE id_producto = %s', (id,))
        conn.commit()
        conn.close()
        flash('Producto eliminado con éxito', 'success')
        return redirect(url_for('productos'))

    conn.close()
    return render_template('confirmar_eliminacion.html', producto=producto)

if __name__ == '__main__':
    app.run(debug=True)
