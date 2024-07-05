from textblob import TextBlob
import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('brown')

tags = {
    'CC': 'Conjunción coordinante',
    'CD': 'Número cardinal',
    'DT': 'Determinante',
    'EX': 'Existencial there',
    'FW': 'Palabra extranjera',
    'IN': 'Preposición o conjunción subordinante',
    'JJ': 'Adjetivo',
    'JJR': 'Adjetivo comparativo',
    'JJS': 'Adjetivo superlativo',
    'LS': 'Marcador de lista',
    'MD': 'Modalidad',
    'NN': 'Sustantivo singular o masa',
    'NNS': 'Sustantivo plural',
    'NNP': 'Sustantivo propio singular',
    'NNPS': 'Sustantivo propio plural',
    'PDT': 'Predeterminador',
    'POS': 'Posesivo final',
    'PRP': 'Pronombre personal',
    'PRP$': 'Pronombre posesivo',
    'RB': 'Adverbio',
    'RBR': 'Adverbio comparativo',
    'RBS': 'Adverbio superlativo',
    'RP': 'Partícula',
    'SYM': 'Símbolo',
    'TO': 'to',
    'UH': 'Interjección',
    'VB': 'Verbo base form',
    'VBD': 'Verbo pasado',
    'VBG': 'Verbo gerundio o presente participio',
    'VBN': 'Verbo pasado participio',
    'VBP': 'Verbo no 3ra persona singular, presente',
    'VBZ': 'Verbo 3ra persona singular, presente',
    'WDT': 'Determinante wh',
    'WP': 'Pronombre wh',
    'WP$': 'Pronombre posesivo wh',
    'WRB': 'Adverbio wh'
}

# Crear un objeto TextBlob con un texto dado
texto = "the quick brown fast fox jumped on the lazy white dog. The intelligent gray squirrel ran nimbly among the tall trees of the forest. The calm river flowed gently under the bright morning sun. The cheerful bird sang sweet melodies from the branch of the old oak"
#texto = "Fast"

blob = TextBlob(texto.lower())

# Análisis de sentimientos
#sentimiento = blob.sentiment
#print("Sentimiento:", sentimiento)

# Etiquetado de partes del discurso (POS tagging)
pos_tags_espanol = blob.tags
print(type(pos_tags_espanol))
print("Etiquetado de partes del discurso:\n")

resultados = []
lista_tuplas_actualizada = [(palabra, tags.get(tag, tag)) for palabra, tag in pos_tags_espanol]
for palabra, tag in lista_tuplas_actualizada:
    etiqueta = tags.get(tag, tag)
    resultados.append(f"{palabra}: {etiqueta}")

print('Resultados procesando todo el texto')
for resultado in resultados:
    print(resultado)



blob = TextBlob()
pos_tags_espanol = blob.tags
print(type(pos_tags_espanol))
print("Etiquetado de partes del discurso:\n")

resultados = []
lista_tuplas_actualizada = [(palabra, tags.get(tag, tag)) for palabra, tag in pos_tags_espanol]
for palabra, tag in lista_tuplas_actualizada:
    etiqueta = tags.get(tag, tag)
    resultados.append(f"{palabra}: {etiqueta}")

print('\nResultados palabra a palabra')
for resultado in resultados:
    print(resultado)


# Extracción de frases clave
#frases_clave = blob.noun_phrases
#print("Frases clave:", frases_clave)
