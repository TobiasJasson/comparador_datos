import pandas as pd
from Utils.measure import medir_tiempo_y_memoria

class PandasMethods:
    @staticmethod
    @medir_tiempo_y_memoria
    def insertar_todo(df, dataset):
        nuevo_df = pd.DataFrame(dataset)
        df_resultado = pd.concat([df, nuevo_df], ignore_index=True)
        return df_resultado

    @staticmethod
    @medir_tiempo_y_memoria
    def buscar_por_codigo(df, codigo_buscado):
        if df.empty:
            return None
        subset = df[df["codigo"] == codigo_buscado]
        if subset.empty:
            return None
        return subset.iloc[0].to_dict()

    @staticmethod
    @medir_tiempo_y_memoria
    def filtrar_por_edad(df, condicion_fn):
        mascara = df["edad"].apply(condicion_fn)
        return df[mascara]
