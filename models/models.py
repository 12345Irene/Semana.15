from flask_login import UserMixin
from Conexion.conexion import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(UserMixin):
    def __init__(self, id_usuario, nombre, email, password):
        self.id = id_usuario
        self.nombre = nombre
        self.email = email
        self.password = password

    @staticmethod
    def obtener_por_email(email):
        """
        Obtiene un usuario de la base de datos utilizando el correo electrónico.
        """
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        cursor.close()
        conexion.close()
        if usuario:
            return Usuario(usuario["id_usuario"], usuario["nombre"], usuario["email"], usuario["password"])
        return None

    @staticmethod
    def crear_usuario(nombre, email, password):
        """
        Crea un nuevo usuario en la base de datos.
        La contraseña es encriptada antes de almacenarse.
        """
        conexion = get_connection()
        cursor = conexion.cursor()

        # Encriptar la contraseña antes de almacenarla
        password_encriptada = generate_password_hash(password)

        try:
            cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                           (nombre, email, password_encriptada))
            conexion.commit()
        except Exception as e:
            conexion.rollback()  # Si ocurre un error, deshacer los cambios
            print(f"Error al registrar el usuario: {e}")
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def verificar_contraseña(password, password_encriptada):
        """
        Verifica si la contraseña ingresada coincide con la almacenada en la base de datos.
        """
        return check_password_hash(password_encriptada, password)
