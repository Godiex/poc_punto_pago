import PyKCS11
import queue

from PyKCS11.LowLevel import CKF_SERIAL_SESSION, CKF_RW_SESSION, CKR_USER_ALREADY_LOGGED_IN


class HsmConnectionPool:
    def __init__(self, max_connections, user_pin):
        # Ruta de biblioteca PKCS #11 de SoftHSM (simulación)
        self.pkcs11_lib_path = "C:\\SoftHSM2\\lib\\softhsm2-x64.dll"
        self.max_connections = max_connections
        self.user_pin = user_pin
        self.connections = queue.Queue(maxsize=max_connections)
        self.slot_id = 1201457871
        self.initialize_connections()

    def initialize_connections(self):
        """Inicializa el pool con sesiones de conexión simuladas al HSM."""
        for _ in range(self.max_connections):
            pkcs11 = PyKCS11.PyKCS11Lib()
            try:
                pkcs11.load(self.pkcs11_lib_path)

                # Busca el primer slot disponible con un token
                slots = pkcs11.getSlotList(tokenPresent=True)
                if not slots:
                    raise Exception("No se encontraron tokens en los slots disponibles.")

                slot_id = slots[0]  # Usa el primer slot con token
                session = pkcs11.openSession(slot_id, CKF_SERIAL_SESSION | CKF_RW_SESSION)

                try:
                    session.login(self.user_pin)
                except PyKCS11.PyKCS11Error as e:
                    if e.args[0] == CKR_USER_ALREADY_LOGGED_IN:
                        print("Usuario ya autenticado. Continuando...")
                    else:
                        raise

                self.connections.put((pkcs11, session))
                print("Sesión iniciada y agregada al pool")

            except PyKCS11.PyKCS11Error as e:
                print(f"Error en la inicialización de la conexión: {e}")
                raise

    def get_connection(self):
        """Obtiene una sesión de conexión del pool."""
        return self.connections.get()

    def return_connection(self, connection):
        """Retorna la sesión al pool."""
        self.connections.put(connection)

    def close_all_connections(self):
        """Cierra todas las conexiones del pool."""
        while not self.connections.empty():
            pkcs11, session = self.connections.get()
            try:
                session.logout()  # Cierra la sesión de usuario
            except PyKCS11.PyKCS11Error as e:
                print(f"Error al cerrar la sesión: {e}")
            session.closeSession()
            print("Conexión cerrada")
