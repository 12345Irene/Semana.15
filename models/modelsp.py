from Conexion.conexion import get_connection

class ProductoModel:
    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        conn.close()
        return productos

    @staticmethod
    def get_by_id(id_producto):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos WHERE id = %s", (id_producto,))
        producto = cursor.fetchone()
        conn.close()
        return producto

    @staticmethod
    def insert(nombre, descripcion, precio):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (nombre, descripcion, precio) VALUES (%s, %s, %s)", (nombre, descripcion, precio))
        conn.commit()
        conn.close()

    @staticmethod
    def update(id_producto, nombre, descripcion, precio):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE productos SET nombre = %s, descripcion = %s, precio = %s WHERE id = %s", (nombre, descripcion, precio, id_producto))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(id_producto):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = %s", (id_producto,))
        conn.commit()
        conn.close()
