from textblob import TextBlob

# Texto de ejemplo
texto = "La rápida zorra marrón saltó sobre el perezoso perro blanco."

# Crear un objeto TextBlob con el texto
blob = TextBlob(texto)

# Obtener una lista de palabras en el texto
palabras = blob.words

print(type(palabras))

# Imprimir la lista de palabras
print("Palabras identificadas en el texto:")
for palabra in palabras:
    print(f'{palabra} : { str(palabra) } : {type(palabra)}')
