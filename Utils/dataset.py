import random, string
from config import RANDOM_SEED

random.seed(RANDOM_SEED)

def generar_registro(i):
    """Genera un registro como diccionario simple."""
    nombre = "nombre_" + ''.join(random.choices(string.ascii_lowercase, k=6))
    edad = random.randint(18, 90)
    codigo = f"codigo_{i}"
    return {"id": i, "nombre": nombre, "edad": edad, "codigo": codigo}

def generar_dataset(n, inject_search_key=None):
    """
    Devuelve una lista de diccionarios (dataset),
    con opción de inyectar una fila para búsqueda por código.
    """
    data = [generar_registro(i) for i in range(n)]
    if inject_search_key:
        idx = n // 2
        data[idx]["codigo"] = inject_search_key
    return data
