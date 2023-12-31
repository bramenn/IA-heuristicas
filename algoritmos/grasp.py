import csv
from copy import copy
import random
from typing import List
from .modelo_base import ModeloBase
import math


class Grasp(ModeloBase):
    aux_costos: List = []
    aux_volumenes: List = []
    aux_costo_volumen: List = []


    datos_grasp_data_costo = []
    datos_grasp_data_volumen = []
    datos_grasp_data_costo_volumen = []
    datos_grasp_data_lista_binaria = []

    tamano_ranquin: int = random.randint(3, 4)

    def __init__(self) -> None:
        self.lista_binaria = [0] * self.numero_de_elementos
        self.aux_costos = copy(self.costos)
        self.aux_volumenes = copy(self.volumenes)
        self.aux_costo_volumen = copy(self.costo_volumen)

        self.probabilidades = [
            self.prob_gaussiana,
            self.prob_x_distante,
            self.prob_logaritmica,
        ]
        super().__init__()

    def algoritmo(self):

        self.imprimir_listas()
        # print("Lista original volumenes:", self.volumenes)

        # print(
        #     f"Selecionando a los {self.numero_elegibles} menores elementos de la lista costo/volumen"
        # )
        menores_indices_costo_volumen = self.obtener_menores(
            numero_menores=self.numero_elegibles, lista=self.costo_volumen, indices=True
        )

        #########################

        # print("Elementos selecionados por indice: ", menores_indices_costo_volumen)

        self.actualizar_listas_por_indice(menores_indices_costo_volumen)

        # print("Esquema inicial: ", self.lista_binaria)
        # print("Lista volumenes sin los elementos ya selecionados: ", self.aux_volumenes)
        # print("\n")

        while self.infactivibidad:
            self.tamano_ranquin = random.randint(3, 4)

            # print("Infactivilidad: ", self.infactivibidad)

            # print(f"Obtener ranquin de los {self.tamano_ranquin} proximos elementos")

            ranquin = self.obtener_ranquin(self.aux_costo_volumen)
            # print(f"{self.tamano_ranquin} mejores elementos: ", ranquin)

            random_porb = random.randint(0, len(self.probabilidades) - 1)

            lista_probabilidades = self.probabilidades[random_porb](ranquin)

            # print(
            #     f"proabilidad {self.probabilidades[random_porb].__name__}: ",
            #     lista_probabilidades,
            # )

            porcentajes_prob = self.porcentajes_probabilidad(lista_probabilidades)
            # print("Calcular porcentajes segun probabilidad: ", porcentajes_prob)

            porcentajes_probabilidad_acumulados = (
                self.porcentajes_probabilidad_acumulados(porcentajes_prob)
            )
            # print(
            #     "Calcular porcentajes acumulados segun probabilidad: ",
            #     porcentajes_probabilidad_acumulados,
            # )

            nuevo_elemento_elegido = self.obtener_elemento_random(
                porcentajes_probabilidad_acumulados
            )
            # print(
            #     "Obtenemos el indice mas cercano dado un random: ",
            #     nuevo_elemento_elegido,
            # )

            elemento_seleccionado = ranquin[nuevo_elemento_elegido]
            # print("Elemento elegido del ranquin: ", elemento_seleccionado)

            indice_elemento_seleccionado = self.aux_costo_volumen.index(
                elemento_seleccionado
            )
            self.actualizar_listas_por_indice([indice_elemento_seleccionado])

            self.imprimir_listas()

        print("Costo obtenido:", self.costo_total_binario)
        print("Volumen obtenido:", self.volumen_total_binario)
        print("Costo/Volumen obtenido:", self.costo_volumen_total_binario)
        self.guardar_resultados()

    def obtener_ranquin(self, lista: List) -> List:
        return sorted(lista, reverse=True)[0 : self.tamano_ranquin]

    def prob_gaussiana(self, ranquin: List) -> List:
        return [math.exp(-i) for i in range(1, len(ranquin) + 1)]

    def prob_x_distante(self, ranquin: List) -> List:
        return [i / len(ranquin) for i in range(1, len(ranquin) + 1)]

    def prob_logaritmica(self, ranquin: List) -> List:
        return [1 / math.log(i + 1) for i in range(1, len(ranquin) + 1)]

    def actualizar_listas_por_indice(self, indices: int):
        self.aux_volumenes = self.eliminar_elementos(indices, self.aux_volumenes)
        self.aux_costos = self.eliminar_elementos(indices, self.aux_costos)
        self.aux_costo_volumen = self.eliminar_elementos(
            indices, self.aux_costo_volumen
        )
        self.marcar_indices_birarios(indices)

    def imprimir_listas(self):

        self.datos_grasp_data_costo.append(self.aux_costos)
        self.datos_grasp_data_volumen.append(self.aux_volumenes)
        self.datos_grasp_data_costo_volumen.append(self.aux_costo_volumen)
        self.datos_grasp_data_lista_binaria.append(self.lista_binaria)

        print("Costo:\t", self.aux_costos)
        print("Volumenes:\t", self.aux_volumenes)
        print("Costo/Volumen:\t", self.aux_costo_volumen)
        print("Binario\t", self.lista_binaria)
        print("\n")

    def guardar_resultados(self):
        
        # grasp_full_data = open(f"grasp_full_data.csv",'w')
        grasp_data_costo = open(f"grasp_data_costo.csv",'w')
        grasp_data_volumen = open(f"grasp_data_volumen.csv",'w')
        grasp_data_costo_volumen = open(f"grasp_data_costo_volumen.csv",'w')
        grasp_data_lista_binaria = open(f"grasp_data_lista_binaria.csv",'w')
        # grasp_full_data_csv = csv.writer(grasp_full_data)
        grasp_data_costo_csv = csv.writer(grasp_data_costo)
        grasp_data_volumen_csv = csv.writer(grasp_data_volumen)
        grasp_data_costo_volumen_csv = csv.writer(grasp_data_costo_volumen)
        grasp_data_lista_binaria_csv = csv.writer(grasp_data_lista_binaria)
        # grasp_full_data_csv.writerows([self.aux_costos, self.aux_volumenes, self.aux_costo_volumen, self.lista_binaria, []])
        grasp_data_costo_csv.writerows(self.datos_grasp_data_costo)
        grasp_data_volumen_csv.writerows(self.datos_grasp_data_volumen)
        grasp_data_costo_volumen_csv.writerows(self.datos_grasp_data_costo_volumen)
        grasp_data_lista_binaria_csv.writerows(self.datos_grasp_data_lista_binaria)
        # grasp_full_data.close()
        grasp_data_costo.close()
        grasp_data_volumen.close()
        grasp_data_costo_volumen.close()
        grasp_data_lista_binaria.close()
