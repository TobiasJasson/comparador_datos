from Utils.measure import medir_tiempo_y_memoria

class ListMethods:
    @staticmethod
    @medir_tiempo_y_memoria
    def insertar_todo(lista_datos, dataset):
        for registro in dataset:
            lista_datos.append(registro)
        return lista_datos

    @staticmethod
    @medir_tiempo_y_memoria
    def buscar_por_codigo(lista_datos, codigo_buscado):
        for registro in lista_datos:
            if registro.get("codigo") == codigo_buscado:
                return registro
        return None

    @staticmethod
    @medir_tiempo_y_memoria
    def filtrar_por_edad(lista_datos, condicion_fn):
        return [r for r in lista_datos if condicion_fn(r.get("edad", 0))]
