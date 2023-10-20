import random
from typing import List
from datos import costos, volumenes
from copy import copy


class ModeloBase:
    costos: List[float] = costos
    volumenes: List[float] = volumenes

    porcentaje_elegibles: float = 0.1
    indice_vol_maximo: float = 2 / 3

    lista_binaria: List[int]

    @property
    def numero_de_elementos(self) -> int:
        return len(self.costos)

    @property
    def costo_volumen(self) -> list:
        return [round(costo / valor, 5) for costo, valor in zip(self.costos, self.volumenes)]

    @property
    def costo_total(self) -> float:
        return sum(self.costos)

    @property
    def volumen_total(self) -> float:
        return sum(self.volumenes)

    @property
    def volumen_maximo(self) -> float:
        return round(self.volumen_total * self.indice_vol_maximo)

    @property
    def numero_elegibles(self) -> float:
        return round(self.numero_de_elementos * self.porcentaje_elegibles)

    def obtener_menores(
        self,
        lista: List,
        numero_menores: int = 1,
        indices: bool = False,
        valores: bool = False,
    ) -> List:
        menores_elementos = []

        for _ in range(0, numero_menores):
            menor_elemento = min(lista)
            indice_menor_elemento = lista.index(menor_elemento)

            if indices and valores:
                menores_elementos.append((menor_elemento, indice_menor_elemento))
            elif indices and not valores:
                menores_elementos.append(indice_menor_elemento)
            else:
                menores_elementos.append(menor_elemento)

            lista.pop(indice_menor_elemento)

        return menores_elementos

    def obtener_mayores(
        self,
        lista: List,
        numero_mayores: int = 1,
        indices: bool = False,
        valores: bool = False,
    ) -> List:
        mayores_elementos = []

        for _ in range(0, numero_mayores):
            menor_elemento = max(lista)
            indice_menor_elemento = lista.index(menor_elemento)

            if indices and valores:
                mayores_elementos.append((menor_elemento, indice_menor_elemento))
            elif indices and not valores:
                mayores_elementos.append(indice_menor_elemento)
            else:
                mayores_elementos.append(menor_elemento)

            lista.pop(indice_menor_elemento)

        return mayores_elementos

    def marcar_indices_birarios(self, indices: List):
        for indice in indices:
            self.lista_binaria[indice] = 1

    @property
    def costo_total_binario(self):
        return sum(
            [item_a * item_b for item_a, item_b in zip(self.costos, self.lista_binaria)]
        )

    @property
    def volumen_total_binario(self):
        return sum(
            [
                item_a * item_b
                for item_a, item_b in zip(self.volumenes, self.lista_binaria)
            ]
        )

    @property
    def costo_volumen_total_binario(self):
        return sum(
            [
                item_a * item_b
                for item_a, item_b in zip(self.costo_volumen, self.lista_binaria)
            ]
        )


    @property
    def infactivibidad(self) -> int:
        return self.volumen_total_binario < self.volumen_maximo

    def eliminar_elementos(self, indices: List, lista: List) -> List:
        lista_aux = copy(lista)

        for indice in indices:
            lista_aux[indice] = 0

        return lista_aux

    def porcentajes_probabilidad(self, datos: List) -> List:
        total_datos = sum(datos)
        return [item / total_datos for item in datos]

    def porcentajes_probabilidad_acumulados(self, datos: List) -> List:
        acumulados = []
        primera_flag = True
        for item in datos:
            if primera_flag:
                primera_flag = False
                acumulados.append(item)
                continue

            acumulados.append(acumulados[-1] + item)

        return acumulados

    def obtener_elemento_random(self, lista: List) -> int | None:

        if not lista:
            return
        
        aleatorio = random.uniform(0, 1)

        # Inicializa las variables para el índice y la diferencia mínima
        indice_mas_cercano = 0
        diferencia_minima = abs(lista[0] - aleatorio)

        # Recorre la lista para encontrar el índice del elemento más cercano a n
        for i in range(1, len(lista)):
            diferencia_actual = abs(lista[i] - aleatorio)
            if diferencia_actual < diferencia_minima:
                diferencia_minima = diferencia_actual
                indice_mas_cercano = i

        return indice_mas_cercano
