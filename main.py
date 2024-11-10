from threading import Thread
import time
from hms_connection_pool import HsmConnectionPool
from simulation_operations import simulated_cryptographic_operation


def main():
    pool = HsmConnectionPool(max_connections=3, user_pin="1234")

    start_time = time.time()

    threads = [Thread(target=simulated_cryptographic_operation, args=(pool,)) for _ in range(5)]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()  # Termina el contador de tiempo
    total_time = end_time - start_time
    print(f"Tiempo total de ejecución con pool de conexiones: {total_time:.2f} segundos")

    pool.close_all_connections()


if __name__ == "__main__":
    main()
