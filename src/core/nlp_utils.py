from src.domain.word_metadata import *

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
    tmp_list = []
    
    for elemento in smells:
        if any(campo in elemento and elemento[campo] == 'X' for campo in ambiguity_types):
            lower_smell = elemento['word'].lower() 

            if lower_smell not in tmp_list:
                tmp_list.append(lower_smell)
                result.append({
                    'word': lower_smell,
                    'justification': elemento['justification'] if 'justification' in elemento else 'NO DISPONIBLE'
                })

    return result


def is_word_an_smell(word:WordMetadata, smell_list:list, tags:list):
    for smell in smell_list:
        # Validar olor de una sola palabra
        word_match_result = _word_match(word, smell, tags)
        if word_match_result[0] > 0:
            return word_match_result

    return (0, None, None)


def _word_match(word:WordMetadata, smell_dict:dict, tags:list = None):
    word_es = word.word_es.lower()
    word_prefix = word.previous_word.lower()
    word_sufix = word.next_word.lower()
    smell_word = smell_dict['word']
    smell_desc = smell_dict['justification']
    composed_smell = smell_word.split('|')
    clean_smell = smell_word.replace('|', ' ')    
    smell = smell_word.lower()
    composed_word = ''

    if word_es == smell:
        print(f'Smell encontrado, coincidencia exacta en palabra <{word_es}>')
        composed_word = word_es
        return (1, composed_word, smell_desc)
    if smell.startswith('<') and smell.endswith('ísimo>') and word_es.endswith('ísimo'):
        print(f'Smell encontrado en palabra <{word_es}> para smell genérico <{smell}>')
        composed_word = word_es
        return (1, composed_word, smell_desc)
    
    # terminos de dos palabras basicas
    if len(composed_smell) == 2 and word_prefix != '':
        composed_word_tmp = ' '.join([word.previous_word, word.word_es])        
        if composed_word_tmp.lower() == clean_smell.lower():
            print(f'Smell compuesto de 2 encontrado, coincidencia exacta en término <{clean_smell}>')
            composed_word = composed_word_tmp
            return (2, composed_word, smell_desc)
    # terminos de tres palabras basicas
    if len(composed_smell) == 3 and word_prefix != '' and word_sufix != '':
        composed_word_tmp = ' '.join([word.previous_word, word.word_es, word.next_word])
        if composed_word_tmp.lower() == clean_smell.lower():
            print(f'Smell compuesto de 3 encontrado, coincidencia exacta en término <{clean_smell}>')
            composed_word = composed_word_tmp
            return (3, composed_word, smell_desc)

    if '<' in smell and '>' in smell and len(composed_smell) == 3:
        smell_scope = 1            
        smell_prefix = composed_smell[0].lower()
        smell_sufix = composed_smell[2].lower()

        if word_prefix == smell_prefix and word_sufix == smell_sufix:           
            word_es_type = composed_smell[1].replace('<', '')
            word_es_type = word_es_type.replace('>', '')
            word_en = word.get_word_en()

            for tag in tags:
                tag_word = tag[0]
                                
                if tag_word == word_en:
                    if word_es == 'feliz': 
                        print(f'4. {word}')
                    tag_code = tag[1]
                    tag_desc = tags_dict[tag_code]

                    if tag_desc.upper() == word_es_type.upper():  
                        smell_scope = smell_scope + 1 if smell_prefix != '' else smell_scope
                        smell_scope = smell_scope + 1 if smell_sufix != '' else smell_scope

                        if smell_scope == 3: composed_word = ' '.join([word.previous_word, word.word_es, word.next_word])
                        if smell_scope == 2: composed_word = ' '.join([word.previous_word, word.word_es])

                        print(f'Smell encontrado en término <{composed_word}> para smell genérico <{clean_smell}>, scope: <{smell_scope}>')
                        return (smell_scope, composed_word, smell_desc)
                    else:
                        return (0, composed_word, None)
    
    return (0, composed_word, None)
