import redis
import json
import time

class MetodoRedis:
    def __init__(self):
        # Conexión local a Redis
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
        self.clave_base = "dataset_items"
        self.r.flushdb()  # Limpiamos la DB antes de cada prueba

    def guardar_datos(self, datos):
        inicio = time.time()
        for i, item in enumerate(datos):
            # Guardamos cada registro como JSON
            self.r.set(f"{self.clave_base}:{i}", json.dumps(item))
        fin = time.time()
        return fin - inicio

    def buscar_dato(self, clave_busqueda, valor):
        inicio = time.time()
        resultados = []
        for key in self.r.scan_iter(f"{self.clave_base}:*"):
            item = json.loads(self.r.get(key))
            if item.get(clave_busqueda) == valor:
                resultados.append(item)
        fin = time.time()
        return resultados, fin - inicio

    def filtrar_datos(self, condicion):
        inicio = time.time()
        resultados = []
        for key in self.r.scan_iter(f"{self.clave_base}:*"):
            item = json.loads(self.r.get(key))
            if condicion(item):
                resultados.append(item)
        fin = time.time()
        return resultados, fin - inicio

    def tamaño(self):
        # Calculamos tamaño total en bytes de todas las keys
        total = 0
        for key in self.r.scan_iter(f"{self.clave_base}:*"):
            total += len(self.r.dump(key))
        return total / 1024  # en KB
