from googletrans import Translator
from textblob import TextBlob
from src.domain.word_metadata import *

#translator = Translator()

tags_dict = {
    'CC': 'Conjunción coordinante',
    'CD': 'Número cardinal',
    'DT': 'Determinante',
    'EX': 'Existencial there',
    'FW': 'Palabra extranjera',
    'IN': 'Preposición o conjunción subordinante',
    'JJ': 'ADJETIVO', # Adjetivo
    'JJR': 'ADJETIVO', # Adjetivo comparativo
    'JJS': 'ADJETIVO', # Adjetivo superlativo
    'LS': 'Marcador de lista',
    'MD': 'Modalidad',
    'NN': 'SUSTANTIVO', # singular o masa
    'NNS': 'SUSTANTIVO', # plural
    'NNP': 'SUSTANTIVO', # propio singular
    'NNPS': 'SUSTANTIVO', # propio plural
    'PDT': 'Predeterminador',
    'POS': 'Posesivo final',
    'PRP': 'Pronombre personal',
    'PRP$': 'Pronombre posesivo',
    'RB': 'ADVERBIO', # Adverbio'
    'RBR': 'ADVERBIO', # Adverbio comparativo
    'RBS': 'ADVERBIO', # Adverbio superlativo
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
    'WRB': 'ADVERBIO' # Adverbio wh
}


def get_smells_by_ambiguity_type(ambiguity_types:list, smells:list):    
    result = []
    
    for elemento in smells:
        if any(elemento[campo] == 'X' for campo in ambiguity_types):
            result.append(elemento['word'].upper())

    return list(set(result))


# Función para verificar si las palabras de un término están presentes de forma contigua en upper_words
def words_in_sequence(smell:str, upper_words:list):
    # TODO sacar esto a un nivel anterior
    english_words = [translator.translate(word, src='es', dest='en').text for word in upper_words]
    blob = TextBlob(' '.join([word.lower() for word in english_words]))
    tags = blob.tags
    
    print(tags)

    smell = smell.upper()
    smell_words_list = smell.split()
    is_smell_template = True if '<' in smell and '>' in smell else False
    n = len(smell_words_list)
    for i in range(len(upper_words) - n + 1):
        sub_term = upper_words[i:i + n]

        print(f'validando smell { smell_words_list } contra palabra {sub_term}, is_smell_template: {is_smell_template}') 
        if is_smell_template:
            #print(f'validando smell { smell_words_list }') 
            if _word_match(smell_words_list, sub_term, tags, upper_words, english_words):
                print(f'template: match smell: {smell_words_list} con termino {sub_term}')
                return n       
        elif smell_words_list == sub_term:
            print(f'simple: match smell: {smell_words_list} con termino {sub_term}')
            return n
    return 0


def _word_match(word_template_list:list, words:list, tags:list, full_words_es:list, full_words_en:list):
    if len(word_template_list) == len(words):
        count = 0
        for i in range(0, len(word_template_list)):
            word_template = word_template_list[i]
            word = words[i]
            print(f'  word_template: |{word_template}| word: |{word}|')
            if '<' in word_template and '>' in word_template:
                #english_word = str(english_words[i])
                tag_tmp = _get_tag(word, tags)
                type = word_template.replace('<', '')
                type = type.replace('>', '')
                tag = tags_dict[tag_tmp]

                print(f'english_word: english_word tag: {tag} type: {type}')
                if tag != type:
                    return False
                
            elif word != word_template:
                return False
            count = count + 1
            if count == len(word_template_list):
                return True
            
    return False


def _get_tag(word:str, tags:list):    
    english_word = translator.translate(word, src='es', dest='en').text
    print(f'word: {word} english_word: {english_word} tags: {tags}')
    for tag in tags:
        word_tmp = tag[0]
        result = tag[1]
        if english_word.upper() == word_tmp.upper():
            print(f'--> {result}')
            return result
        




