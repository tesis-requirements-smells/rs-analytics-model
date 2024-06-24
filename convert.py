import csv
import json

# Ruta del archivo CSV y del archivo JSON de salida
csv_file_path = './test.csv'
json_file_path = './output.json'

# Lista de claves para los diccionarios
keys = ['word', 'type', 'lexical', 'syntactic', 'semantic', 'vagueness', 'incompleteness']

# Leer el archivo CSV y convertirlo a una lista de diccionarios
data = []
with open(csv_file_path, mode='r', encoding='latin1') as csvfile:
    csv_reader = csv.DictReader(csvfile, fieldnames=keys)
    for row in csv_reader:
        data.append(row)

# Escribir la lista de diccionarios en un archivo JSON
with open(json_file_path, mode='w', encoding='utf-8') as jsonfile:
    json.dump(data, jsonfile, indent=4, ensure_ascii=False)

print(f"Archivo JSON generado en: {json_file_path}")