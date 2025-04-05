from Conexion.conexion import get_connection

class UserModel:
    @staticmethod
    def get_all_users():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        conn.close()
        return usuarios

    @staticmethod
    def get_user_by_id(id_usuario):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id_usuario,))
        usuario = cursor.fetchone()
        conn.close()
        return usuario

    @staticmethod
    def insert_user(nombre, correo, clave):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, correo, clave) VALUES (%s, %s, %s)", (nombre, correo, clave))
        conn.commit()
        conn.close()

    @staticmethod
    def update_user(id_usuario, nombre, correo, clave):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET nombre = %s, correo = %s, clave = %s WHERE id = %s", (nombre, correo, clave, id_usuario))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_user(id_usuario):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id_usuario,))
        conn.commit()
        conn.close()
