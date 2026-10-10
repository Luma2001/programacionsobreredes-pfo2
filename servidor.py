# ==============================================
# IMPLEMENTAR los tres endpoints de la consigna:
# ==============================================

from flask import Flask, request, jsonify, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from database import obtener_conexion, inicializar_db

# --- Instancia de la aplicación Flask --- 
# El argumento __name__ indica que este archivo es el módulo principal.
app = Flask(__name__)

# =================================================
# 1. ENDPOINT: REGISTRO DE USUARIOS (POST/registro)
# =================================================
@app.route('/registro', methods=['POST']) #Asociamos la URL(/registro) con la función registro() y el método POST
def registro():
    """
    Función que procesa el registro de un nuevo usuario.
    Recibe {"usuario": "nombre", "contraseña": "password"} en formato JSON.
    Guarda el usuario con su contraseña hasheada en SQLite.
    """
    datos = request.get_json()

    # Validar que lleguen ambos campos(usuario y contraseña) y que no estén vacíos
    if not datos or 'usuario' not in datos or 'contraseña' not in datos:
        return jsonify({"error": "Debe enviar 'usuario' y 'contraseña'"}), 400

    # Extraer y limpiar los datos recibidos. Usamos strip() para quitar espacios en blanco accidentales
    usuario = datos['usuario'].strip()
    password = datos['contraseña'].strip()

    if not usuario or not password:
        return jsonify({"error": "Usuario y contraseña no pueden estar vacíos"}), 400

    # Hashear la contraseña antes de guardarla. Transforma la contraseña en un hash seguro para almacenamiento.
    password_hash = generate_password_hash(password)


    try:
        with obtener_conexion() as conexion: #Abre la conexion SQLite y with asegura que se cierre automáticamente al finalizar el bloque
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO usuarios (usuario, password_hash) VALUES (?, ?)",
                (usuario, password_hash)
            )
            conexion.commit()
            return jsonify({"mensaje": f"Usuario '{usuario}' registrado con éxito"}), 201



    except sqlite3.IntegrityError:
        # Ocurre si el usuario ya existe (debido al UNIQUE en la tabla)
        return jsonify({"error": "El nombre de usuario ya está registrado"}), 409
    except Exception as e:
        # Captura cualquier otro error inesperado y devuelve un mensaje genérico de error interno del servidor
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500


# =================================================
# 2. ENDPOINT: INICIO DE SESIÓN (LOGIN)
# =================================================
@app.route('/login', methods=['POST'])#Asociamos la URL(/login) con la función login() y el método POST
def login():
    """
    Recibe {"usuario": "nombre", "contraseña": "password"}.
    Comprueba las credenciales contra el hash guardado en SQLite.
    """
    datos = request.get_json()

    if not datos or 'usuario' not in datos or 'contraseña' not in datos:
        return jsonify({"error": "Debe enviar 'usuario' y 'contraseña'"}), 400

    usuario = datos['usuario'].strip()
    password = datos['contraseña'].strip()

    with obtener_conexion() as conexion:
        #Abrir base de datos y buscar el registro del usuario ingresado
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT * FROM usuarios WHERE usuario = ?",
            (usuario,)
        )
        usuario_db = cursor.fetchone() #Retorna la primera fila encontrada o None si el usuario no existe.

        # Autenticación:Si el usuario no existe o la contraseña no coincide con el hash
        if usuario_db is None or not check_password_hash(usuario_db['password_hash'], password):
            return jsonify({"error": "Credenciales inválidas"}), 401
        # Si las credenciales son correctas, devolvemos un mensaje de éxito y el ID del usuario
        return jsonify({
            "mensaje": f"Inicio de sesión exitoso. ¡Bienvenido {usuario}!",
            "usuario_id": usuario_db['id']
        }), 200


# =================================================
# 3. ENDPOINT: GESTIÓN DE TAREAS (HTML BIENVENIDA)
# =================================================
@app.route('/tareas', methods=['GET'])#Asociamos la URL(/tareas) con la función tareas() y el método GET
def tareas():
    """
    Crear un HTML simple de bienvenida según la consigna.
    """
    html_bienvenida = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Sistema de Gestión de Tareas</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background-color: #f4f6f8; }
            .card { background: white; padding: 30px; border-radius: 8px; display: inline-block; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; }
            p { color: #7f8c8d; font-size: 18px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Bienvenido al Sistema de Gestión de Tareas</h1>
            <p>API REST activa y conectada a la base de datos SQLite.</p>
        </div>
    </body>
    </html>
    """
    # render_template_string de Flask, que permite devolver contenido HTML directamente desde una cadena.
    # Renderizamos el HTML de bienvenida
    return render_template_string(html_bienvenida)


# --- Arranque del Servidor ---
if __name__ == '__main__':
    # Asegura que las tablas de la base de datos existan al arrancar
    inicializar_db()
    print("[Servidor] Iniciando API Flask en http://127.0.0.1:5000 ...")
    # app.run: Poner en funcionamiento el servidor
    # host='127.0.0.1', port=5000: Especificamos la dirección y puerto
    # debug=True reinicia automáticamente el servidor ante cambios en el archivo
    app.run(host='127.0.0.1', port=5000, debug=True)