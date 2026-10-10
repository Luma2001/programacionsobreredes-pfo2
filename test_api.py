import time
import requests

BASE_URL = "http://127.0.0.1:5000"

# ====================================================================================
# 1. TEST REGISTRO EXITOSO: un usuario nuevo con contraseña válida se guarda en SQLite
# ====================================================================================
def test_registro_exitoso():
    print("\n[TEST 1] Probando registro de usuario nuevo (201 Created)...")
    usuario_unico = f"usuario_test_{int(time.time())}" #Genera un nombre de usuario dinámico basado en la marca de tiempo actual para evitar duplicados en pruebas repetidas
    payload = {"usuario": usuario_unico, "contraseña": "passwordSeguro123"}

    # Realiza petición POST al endpoint /registro con los datos del usuario
    respuesta = requests.post(f"{BASE_URL}/registro", json=payload)

    # Verifica que el código de estado HTTP sea 201 (Created) y que el mensaje de éxito esté presente en la respuesta JSON
    # Si no lo es, interrumpe el script lanzando un AssertionError con un mensaje descriptivo
    assert (
        respuesta.status_code == 201
    ), f"Esperado 201, recibido {respuesta.status_code}"

    # Convertimos la respuesta a JSON
    datos = respuesta.json()

    # Verificamos que el mensaje de éxito contenga la frase esperada
    assert (
        "registrado con éxito" in datos.get("mensaje", "")
    ), "Mensaje de registro incorrecto"
    print(f"✔ PASÓ: Usuario '{usuario_unico}' registrado con código 201.")
    return usuario_unico, "passwordSeguro123"

# ====================================================================================
# 2. TEST REGISTRO DUPLICADO: un usuario existente no se puede registrar nuevamente
# ====================================================================================
def test_registro_duplicado(usuario):
    print(
        "\n[TEST 2] Probando rechazo de usuario duplicado (409 Conflict)..."
    )
    payload = {"usuario": usuario, "contraseña": "otraPassword"}

    respuesta = requests.post(f"{BASE_URL}/registro", json=payload)
    assert (
        respuesta.status_code == 409
    ), f"Esperado 409, recibido {respuesta.status_code}"
    datos = respuesta.json()
    assert (
        "ya está registrado" in datos.get("error", "")
    ), "Mensaje de error incorrecto"
    print("✔ PASÓ: El servidor rechazó el duplicado con código 409 Conflict.")

# ====================================================================================
# 3. TEST REGISTRO CAMPOS INCOMPLETOS: usuario con campos incompletos no se guarda
# ====================================================================================
def test_registro_campos_incompletos():
    print(
        "\n[TEST 3] Probando validación de campos vacíos (400 Bad Request)..."
    )
    payload = {"usuario": "usuarioIncompleto"}  # Falta 'contraseña'

    respuesta = requests.post(f"{BASE_URL}/registro", json=payload)
    assert (
        respuesta.status_code == 400
    ), f"Esperado 400, recibido {respuesta.status_code}"
    print(
        "✔ PASÓ: Petición sin campo obligatorio rechazada con código 400 Bad Request."
    )

# ====================================================================================
# 4. TEST LOGIN EXITOSO: un usuario registrado puede iniciar sesión con credenciales 
#                        válidas
# ====================================================================================
def test_login_exitoso(usuario, password):
    print("\n[TEST 4] Probando inicio de sesión exitoso (200 OK)...")
    payload = {"usuario": usuario, "contraseña": password}

    respuesta = requests.post(f"{BASE_URL}/login", json=payload)
    assert (
        respuesta.status_code == 200
    ), f"Esperado 200, recibido {respuesta.status_code}"
    datos = respuesta.json()
    assert (
        "Inicio de sesión exitoso" in datos.get("mensaje", "")
    ), "Mensaje de login incorrecto"
    print(
        "✔ PASÓ: Autenticación exitosa contra el hash de SQLite con código 200 OK."
    )

# ====================================================================================
# 5. TEST LOGIN CONTRASEÑA INCORRECTA: un usuario registrado no puede iniciar sesión 
#                                      con contraseña errónea
# ====================================================================================
def test_login_password_incorrecta(usuario):
    print(
        "\n[TEST 5] Probando login con contraseña errónea (401 Unauthorized)..."
    )
    payload = {"usuario": usuario, "contraseña": "claveCompletamenteErronea"}

    respuesta = requests.post(f"{BASE_URL}/login", json=payload)
    assert (
        respuesta.status_code == 401
    ), f"Esperado 401, recibido {respuesta.status_code}"
    print(
        "✔ PASÓ: Contraseña incorrecta rechazada con código 401 Unauthorized."
    )

# ====================================================================================
# 6. TEST LOGIN USUARIO INEXISTENTE: un usuario que no existe no puede iniciar sesión
# ====================================================================================
def test_login_usuario_inexistente():
    print(
        "\n[TEST 6] Probando login con usuario que no existe (401 Unauthorized)..."
    )
    payload = {
        "usuario": "noExistoEnLaBase123",
        "contraseña": "cualquiera",
    }

    respuesta = requests.post(f"{BASE_URL}/login", json=payload)
    assert (
        respuesta.status_code == 401
    ), f"Esperado 401, recibido {respuesta.status_code}"
    print("✔ PASÓ: Usuario inexistente rechazado con código 401 Unauthorized.")

# ====================================================================================
# 7. TEST ENDPOINT TAREAS: el endpoint GET /tareas devuelve la página HTML de 
#                          bienvenida
# ====================================================================================
def test_endpoint_tareas():
    print("\n[TEST 7] Probando endpoint GET /tareas (HTML de bienvenida)...")
    respuesta = requests.get(f"{BASE_URL}/tareas")
    assert (
        respuesta.status_code == 200
    ), f"Esperado 200, recibido {respuesta.status_code}"
    assert (
        "<!DOCTYPE html>" in respuesta.text
    ), "La respuesta no contiene HTML"
    assert (
        "Bienvenido al Sistema de Gestión de Tareas" in respuesta.text
    ), "Texto de bienvenida ausente"
    print("✔ PASÓ: Endpoint /tareas entregó la página HTML con código 200 OK.")

# ====================================================================================
# FUNCIÓN DE EJECUCIÓN DE PRUEBAS: Ejecuta todos los tests secuencialmente y reporta 
#                                  resultados.
# ====================================================================================
def ejecutar_todas_las_pruebas():
    print("======================================================")
    print("   BATERÍA DE PRUEBAS AUTOMATIZADAS - PFO 2 (FLASK)  ")
    print("======================================================")

    try:
        # Verificar que el servidor esté activo antes de correr los tests
        requests.get(f"{BASE_URL}/tareas")
    except requests.exceptions.ConnectionError:
        print(
            "❌ ERROR: El servidor Flask no está encendido. Ejecuta 'python servidor.py' primero."
        )
        return

    # Ejecución secuencial de los tests
    usuario, password = test_registro_exitoso()
    test_registro_duplicado(usuario)
    test_registro_campos_incompletos()
    test_login_exitoso(usuario, password)
    test_login_password_incorrecta(usuario)
    test_login_usuario_inexistente()
    test_endpoint_tareas()

    print("\n======================================================")
    print(" TODAS LAS PRUEBAS PASARON EXITOSAMENTE (7/7)")
    print("======================================================")

# --- Punto de Entrada ---
if __name__ == "__main__":
    ejecutar_todas_las_pruebas()