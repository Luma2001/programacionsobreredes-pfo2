import sqlite3

DB_NAME = "tareas.db"

def obtener_conexion():
    """Crear y devolver una conexión a la base de datos SQLite."""
    conexion = sqlite3.connect(DB_NAME)
    # Accedemos a las columnas por su nombre
    conexion.row_factory = sqlite3.Row
    return conexion

def inicializar_db():
    """Crear tablas de usuarios y tareas si aún no existen."""
    with obtener_conexion() as conexion:
        cursor = conexion.cursor()
        
        # 1. Tabla de usuarios (con contraseña protegida por hash)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)
        
        # 2. Tabla de tareas asociadas a los usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                titulo TEXT NOT NULL,
                estado TEXT DEFAULT 'pendiente',
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        """)
        
        conexion.commit()
        print("[DB] Base de datos 'tareas.db' y tablas inicializadas correctamente.")

if __name__ == "__main__":
    # crear base de datos de prueba
    inicializar_db()