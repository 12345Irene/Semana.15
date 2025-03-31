import hashlib
import mysql.connector
from Conexion.conexion import get_connection

def verificar_usuario(username, password):
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM usuarios WHERE username = %s"
        cursor.execute(query, (username,))
        usuario = cursor.fetchone()

        if usuario:
            hashed_password = usuario['password']
            if hashlib.sha256(password.encode()).hexdigest() == hashed_password:
                return True
            else:
                return False
        return False
    except Exception as e:
        print(f"Error al verificar el usuario: {e}")
    finally:
        if connection:
            connection.close()
