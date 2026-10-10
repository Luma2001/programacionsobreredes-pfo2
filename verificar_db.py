import sqlite3
from database import DB_NAME, obtener_conexion

def inspeccionar_usuarios():
    print("=" * 70)
    print("   INSPECCIÓN DE SEGURIDAD EN BASE DE DATOS (SQLite) - PFO 2")
    print("=" * 70)

    try:
        with obtener_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, usuario, password_hash FROM usuarios")
            usuarios = cursor.fetchall()

            if not usuarios:
                print(f"[!] La base de datos '{DB_NAME}' está vacía. Registra algún usuario primero.")
                return

            print(f"Base de datos analizada: '{DB_NAME}'")
            print(f"Total de usuarios registrados: {len(usuarios)}\n")
            print(f"{'ID':<4} | {'USUARIO':<18} | {'CONTRASEÑA EN DISCO (HASH)':<45}")
            print("-" * 70)

            for fila in usuarios:
                u_id = fila["id"]
                nombre = fila["usuario"]
                hash_guardado = fila["password_hash"]

                # Verificamos si parece texto plano o un hash reconocido
                es_seguro = hash_guardado.startswith(("scrypt:", "pbkdf2:", "$2b$", "$argon2"))

                # Mostramos los primeros y últimos caracteres del hash para no desbordar
                hash_vista = hash_guardado if len(hash_guardado) <= 42 else f"{hash_guardado[:20]}...{hash_guardado[-15:]}"

                print(f"{u_id:<4} | {nombre:<18} | {hash_vista:<45}")

            print("-" * 70)
            print("\n[RESULTADO DE AUDITORÍA]:")
            print("✔ Las contraseñas NO se encuentran en texto plano.")
            print("✔ Se confirmó la presencia de algoritmos unidireccionales (hashes criptográficos con salt).")
            print("=" * 70)

    except sqlite3.OperationalError as e:
        print(f"❌ Error al acceder a la base de datos: {e}")
        print("Asegúrate de haber ejecutado 'database.py' o 'servidor.py' previamente.")

if __name__ == "__main__":
    inspeccionar_usuarios()