import time
import tracemalloc
from functools import wraps

def medir_tiempo_y_memoria(func):
    """
    Decorador que mide tiempo (segundos) y memoria (KB) de una función.
    Devuelve: (resultado, segundos_transcurridos, pico_kb)
    """
    @wraps(func)
    def envoltura(*args, **kwargs):
        tracemalloc.start()
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        duracion = time.perf_counter() - inicio
        _, pico = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        pico_kb = pico / 1024.0
        return resultado, duracion, pico_kb
    return envoltura
