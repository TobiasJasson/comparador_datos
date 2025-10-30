import os, csv
from config import DATASET_SIZES, REPEATS, SEARCH_KEY, FILTER_CONDITION, RESULTS_CSV, PLOT_PATH
from Utils.dataset import generar_dataset
from metodos.list_methods import ListMethods
from metodos.pandas_methods import PandasMethods
from metodos.sqlite_methods import SQLiteMethods
from metodos.redis_methods import MetodoRedis

import matplotlib.pyplot as plt
import pandas as pd

os.makedirs("results/plots", exist_ok=True)
os.makedirs("results", exist_ok=True)

ENCABEZADOS = [
    "biblioteca", "tamano_dataset", "repeticion",
    "operacion", "segundos", "pico_kb", "extra"
]

def ejecutar_un_tamano(n, indice_repeticion):
    dataset = generar_dataset(n, inject_search_key=SEARCH_KEY)
    resultados = []

    # 1) LISTAS
    lista = []
    _, tiempo_insertar, pico_insertar = ListMethods.insertar_todo(lista, dataset)
    resultados.append(("listas", n, indice_repeticion, "insertar", tiempo_insertar, pico_insertar, len(lista)))

    _, tiempo_buscar, pico_buscar = ListMethods.buscar_por_codigo(lista, SEARCH_KEY)
    resultados.append(("listas", n, indice_repeticion, "buscar", tiempo_buscar, pico_buscar, "OK"))

    _, tiempo_filtrar, pico_filtrar = ListMethods.filtrar_por_edad(lista, FILTER_CONDITION)
    resultados.append(("listas", n, indice_repeticion, "filtrar", tiempo_filtrar, pico_filtrar, "OK"))

    # 2) PANDAS
    df = pd.DataFrame(columns=["id","nombre","edad","codigo"])
    df, tiempo_insertar_p, pico_insertar_p = PandasMethods.insertar_todo(df, dataset)
    resultados.append(("pandas", n, indice_repeticion, "insertar", tiempo_insertar_p, pico_insertar_p, len(df)))

    _, tiempo_buscar_p, pico_buscar_p = PandasMethods.buscar_por_codigo(df, SEARCH_KEY)
    resultados.append(("pandas", n, indice_repeticion, "buscar", tiempo_buscar_p, pico_buscar_p, "OK"))

    _, tiempo_filtrar_p, pico_filtrar_p = PandasMethods.filtrar_por_edad(df, FILTER_CONDITION)
    resultados.append(("pandas", n, indice_repeticion, "filtrar", tiempo_filtrar_p, pico_filtrar_p, "OK"))

    # 3) SQLITE
    sql = SQLiteMethods()
    _, tiempo_insertar_s, pico_insertar_s = sql.insertar_todo(dataset)
    resultados.append(("sqlite", n, indice_repeticion, "insertar", tiempo_insertar_s, pico_insertar_s, "OK"))

    _, tiempo_buscar_s, pico_buscar_s = sql.buscar_por_codigo(SEARCH_KEY)
    resultados.append(("sqlite", n, indice_repeticion, "buscar", tiempo_buscar_s, pico_buscar_s, "OK"))

    _, tiempo_filtrar_s, pico_filtrar_s = sql.filtrar_por_edad(FILTER_CONDITION)
    resultados.append(("sqlite", n, indice_repeticion, "filtrar", tiempo_filtrar_s, pico_filtrar_s, "OK"))

    sql.cerrar()

    
    # 4) REDIS
    redis = MetodoRedis()
    _, tiempo_insertar_r, pico_insertar_r = redis.insertar_todo(dataset)
    resultados.append(("redis", n, indice_repeticion, "insertar", tiempo_insertar_r, pico_insertar_r, "OK"))

    _, tiempo_buscar_r, pico_buscar_r = redis.buscar_por_codigo(SEARCH_KEY)
    resultados.append(("redis", n, indice_repeticion, "buscar", tiempo_buscar_r, pico_buscar_r, "OK"))

    _, tiempo_filtrar_r, pico_filtrar_r = redis.filtrar_por_edad(FILTER_CONDITION)
    resultados.append(("redis", n, indice_repeticion, "filtrar", tiempo_filtrar_r, pico_filtrar_r, "OK"))

    redis.cerrar()
    return resultados


def main():
    with open(RESULTS_CSV, "w", newline='', encoding='utf-8') as f:
        escritor = csv.writer(f)
        escritor.writerow(ENCABEZADOS)

        for n in DATASET_SIZES:
            for r in range(1, REPEATS + 1):
                print(f"Ejecutando tamaño={n}, repetición={r}")
                res = ejecutar_un_tamano(n, r)
                for fila in res:
                    escritor.writerow(fila)

    print(f"Resultados guardados en {RESULTS_CSV}")

    # Graficar resultados promedios
    df = pd.read_csv(RESULTS_CSV)
    df.to_excel("results/resultados.xlsx", index=False)
    df_insertar = df[df["operacion"] == "insertar"]
    promedio = df_insertar.groupby(["biblioteca", "tamano_dataset"])["segundos"].mean().unstack(level=0)
    promedio.plot(marker='o')
    plt.title("Tiempo promedio de inserción por biblioteca")
    plt.xlabel("Tamaño del dataset")
    plt.ylabel("Segundos")
    plt.grid(True)
    plt.savefig(PLOT_PATH)
    print(f"Gráfico guardado en {PLOT_PATH}")


if __name__ == "__main__":
    main()
