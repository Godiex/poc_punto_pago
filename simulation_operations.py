import time


def simulated_cryptographic_operation(pool_connections):
    """Función que simula una operación criptográfica usando el pool de conexiones."""
    pkcs11, session = pool_connections.get_connection()
    try:
        print("Realizando operación criptográfica simulada con una conexión del pool.")
        time.sleep(1)  # Simula el tiempo de la operación criptográfica
    finally:
        pool_connections.return_connection((pkcs11, session))
        print("Conexión devuelta al pool.")
