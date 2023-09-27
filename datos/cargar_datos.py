import csv

archivo_costos = open("costo.csv")
archivo_volumenes = open("volumen.csv")

costos_lectura = csv.reader(archivo_costos)
volumenes_lectura = csv.reader(archivo_volumenes)

costos = []
volumenes = []

for row in costos_lectura:
    costos = row

for row in volumenes_lectura:
    volumenes = row

costos = [float(dato) for dato in costos]   
volumenes = [float(dato) for dato in volumenes]   