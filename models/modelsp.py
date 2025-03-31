import mysql.connector
from Conexion.conexion import get_connection

def obtener_productos():
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        return productos
    except Exception as e:
        print(f"Error al obtener productos: {e}")
    finally:
        if connection:
            connection.close()

def agregar_producto(nombre, precio, stock):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)"
        cursor.execute(query, (nombre, precio, stock))
        connection.commit()
    except Exception as e:
        print(f"Error al agregar producto: {e}")
    finally:
        if connection:
            connection.close()

def obtener_producto_por_id(id_producto):
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM productos WHERE id_producto = %s"
        cursor.execute(query, (id_producto,))
        producto = cursor.fetchone()
        return producto
    except Exception as e:
        print(f"Error al obtener producto por ID: {e}")
    finally:
        if connection:
            connection.close()

def actualizar_producto(id_producto, nombre, precio, stock):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = "UPDATE productos SET nombre = %s, precio = %s, stock = %s WHERE id_producto = %s"
        cursor.execute(query, (nombre, precio, stock, id_producto))
        connection.commit()
    except Exception as e:
        print(f"Error al actualizar producto: {e}")
    finally:
        if connection:
            connection.close()

def eliminar_producto(id_producto):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = "DELETE FROM productos WHERE id_producto = %s"
        cursor.execute(query, (id_producto,))
        connection.commit()
    except Exception as e:
        print(f"Error al eliminar producto: {e}")
    finally:
        if connection:
            connection.close()
