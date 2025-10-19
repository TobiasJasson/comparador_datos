import sqlite3
from Utils.measure import medir_tiempo_y_memoria

DB_PATH = ":memory:"

class SQLiteMethods:
    def __init__(self, db_path=None):
        self.db_path = db_path or DB_PATH
        self.conn = sqlite3.connect(self.db_path)
        self._crear_tabla()

    def _crear_tabla(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS personas (
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            edad INTEGER,
            codigo TEXT
        )
        """)
        self.conn.commit()

    @medir_tiempo_y_memoria
    def insertar_todo(self, dataset):
        cur = self.conn.cursor()
        filas = [(d["id"], d["nombre"], d["edad"], d["codigo"]) for d in dataset]
        cur.executemany("INSERT INTO personas (id, nombre, edad, codigo) VALUES (?, ?, ?, ?)", filas)
        self.conn.commit()
        return len(filas)

    @medir_tiempo_y_memoria
    def buscar_por_codigo(self, codigo_buscado):
        cur = self.conn.cursor()
        cur.execute("SELECT id, nombre, edad, codigo FROM personas WHERE codigo = ? LIMIT 1", (codigo_buscado,))
        fila = cur.fetchone()
        if fila is None:
            return None
        claves = ["id", "nombre", "edad", "codigo"]
        return dict(zip(claves, fila))

    @medir_tiempo_y_memoria
    def filtrar_por_edad(self, condicion_fn):
        cur = self.conn.cursor()
        cur.execute("SELECT id, nombre, edad, codigo FROM personas")
        filas = cur.fetchall()
        claves = ["id", "nombre", "edad", "codigo"]
        registros = [dict(zip(claves, f)) for f in filas]
        filtrados = [r for r in registros if condicion_fn(r["edad"])]
        return filtrados

    def cerrar(self):
        self.conn.close()
