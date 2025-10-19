DATASET_SIZES = [1000, 5000, 10000]   # tamaños a probar
REPEATS = 5                           # repeticiones para promedio
SEARCH_KEY = "codigo_777"             # clave a buscar (se insertará en el dataset)
FILTER_FIELD = "edad"                 # campo para filtrar
FILTER_CONDITION = lambda v: v > 50   # condición de filtrado para edad
RANDOM_SEED = 42

RESULTS_CSV = "results/results.csv"
PLOT_PATH = "results/plots/resumen_grafico.png"