# Módulo de sistema de python. Se utiliza más adelante para terminar la ejecución del programa de forma limpia(sys.exit(0))
import sys 

#Módulo de requests para realizar peticiones HTTP al servidor Flask
import requests

# URL base del servidor Flask
BASE_URL = "http://127.0.0.1:5000"

# ========================================================================
# 1. FUNCIÓN REGISTRAR USUARIOS: ENCARGADA DEL FLUJO DE ALTA DE USUARIOS
# ========================================================================
def registrar_usuario():
    """Solicitar credenciales y enviar petición POST a /registro."""
    print("\n--- REGISTRO DE USUARIO ---")
    #.input(...).strip() solicitamos por consola nombre y contrasena. .strip() elimina espacios en blanco al inicio y final de la cadena ingresada
    usuario = input("Ingresa nombre de usuario: ").strip()
    password = input("Ingresa contraseña: ").strip()

    #Validación previa: Si el usuario o la contraseña están vacíos, se muestra un mensaje de error y se retorna sin hacer la petición
    if not usuario or not password:
        print("[Error] El usuario y la contraseña no pueden estar vacíos.")
        return

    # Creamos un diccionario con los datos a enviar en formato JSON
    payload = {"usuario": usuario, "contraseña": password}

    # Iniciamos bloque protegido contra fallos.
    try:
        #petición HTTP con método POST al endpoint /registro enviando los datos en formato JSON
        respuesta = requests.post(f"{BASE_URL}/registro", json=payload)
        datos = respuesta.json()

        #consulta del código de estado HTTP recibido. 
        #201, el registro fue exitoso; de lo contrario, hubo un error (por ejemplo, usuario ya registrado)
        if respuesta.status_code == 201:
            print(f"✔ Éxito (HTTP {respuesta.status_code}): {datos.get('mensaje')}")
        else:
            print(f"❌ Error (HTTP {respuesta.status_code}): {datos.get('error')}")
    # Bloque except para capturar errores de conexión, como cuando el servidor no está corriendo o hay problemas de red.
    except requests.exceptions.ConnectionError:
        print("❌ Error de red: No se pudo conectar al servidor. Asegúrate de que servidor.py esté corriendo.")


# ========================================================================
# 2. FUNCIÓN INICIAR SESIÓN: ENCARGADA DEL FLUJO DE INICIO DE SESIÓN
# ========================================================================
def iniciar_sesion():
    """Solicitar credenciales, enviar POST a /login y, si es correcto, acceder a /tareas."""
    print("\n--- INICIO DE SESIÓN ---")
    usuario = input("Ingresa tu usuario: ").strip()
    password = input("Ingresa tu contraseña: ").strip()

    payload = {"usuario": usuario, "contraseña": password}

    try:
        respuesta = requests.post(f"{BASE_URL}/login", json=payload)
        datos = respuesta.json()

        if respuesta.status_code == 200:
            print(f"✔ Éxito (HTTP {respuesta.status_code}): {datos.get('mensaje')}")
            # Si el login es exitoso, consultamos el endpoint /tareas
            ver_pantalla_tareas()
        else:
            print(f"❌ Error (HTTP {respuesta.status_code}): {datos.get('error')}")

    except requests.exceptions.ConnectionError:
        print("❌ Error de red: No se pudo conectar al servidor.")


# =============================================================================
# 3. FUNCIÓN VER PANTALLA DE TAREAS: ENCARGADA DE CONSULTAR EL ENDPOINT /TAREAS
# =============================================================================
def ver_pantalla_tareas():
    """Realizar petición GET a /tareas para verificar acceso."""
    print("\n--- CONSULTANDO ENDPOINT DE TAREAS ---")
    try:
        #Enviamos petición GET al endpoint /tareas para verificar que el usuario logueado pueda acceder a la página de bienvenida
        respuesta = requests.get(f"{BASE_URL}/tareas")
        # Si la respuesta es 200, significa que el usuario tiene acceso a la página de bienvenida
        if respuesta.status_code == 200:
            print(f"✔ Acceso concedido a /tareas (HTTP 200 OK)")
            print("✔ El servidor entregó la página HTML de bienvenida correctamente.")
            print("👉 Puedes verla con diseño visual abriendo en tu navegador:")
            print("   http://127.0.0.1:5000/tareas")
        else:
            print(f"❌ Error al consultar tareas (HTTP {respuesta.status_code})")
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar con el servidor.")


def menu_principal():
    """Bucle principal de la interfaz de consola."""
    # while True: Mantiene el menú en un bucle interactivo infinito 
    # para que el usuario pueda realizar múltiples acciones sin tener 
    # que volver a ejecutar el comando python cliente.py cada vez.
    while True:
        print("\n===============================")
        print("   SISTEMA DE GESTIÓN DE TAREAS")
        print("===============================")
        print("1. Registrar nuevo usuario")
        print("2. Iniciar sesión")
        print("3. Consultar /tareas directamente")
        print("4. Salir")
        
        opcion = input("Selecciona una opción (1-4): ").strip()
        #Lee la opción ingresada por el usuario y ejecuta la función correspondiente.    
        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            iniciar_sesion()
        elif opcion == "3":
            ver_pantalla_tareas()
        elif opcion == "4":#ejecuta sys.exit(0) para finalizar el bucle ysalir del programa de forma limpia
            print("Saliendo del cliente...")
            sys.exit(0)
        else:
            print("Opción no válida. Por favor ingresa un número del 1 al 4.")

# --- Punto de Entrada ---
if __name__ == "__main__":
    menu_principal()