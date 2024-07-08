from textblob import TextBlob
from src.utils import *
from src.domain.word_metadata import *
import src.core.nlp_utils as nlp_utils
from googletrans import Translator

SMELLS_URL = './data/smells-dictionary.json'

TAGS_DICT = {
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


class NlpMetrics:    

    def __init__(self, original_text:str):
        translator = Translator()

        self.text_es = original_text
        self.blob_es = TextBlob(original_text)
        self.words_es_list = self.blob_es.words
        self.NTT = len(self.words_es_list)
        self.smells_dict = read_json(SMELLS_URL)
        print('LLAMADA AL API DE GOOGLE PARA TRADUCIR TEXTO')      
        self.text_en = translator.translate(self.text_es, src='es', dest='en').text

        self.blob_en = TextBlob(self.text_en)
        self.tags = self.blob_en.tags
        self.words_en_list = self.blob_en.words
        self.words_metadata = self.get_words_metadata(self.words_es_list) 

        print('Objeto NlpMetrics creado. Valores:')
        print('========= self.text_es')     
        print(self.text_es)
        print('========= self.words_es_list')     
        print(self.words_es_list)
        print('========= self.NTT')     
        print(self.NTT)
        print('========= self.text_en')     
        print(self.text_en)
        print('========= self.tags')     
        print(self.tags)
        print('========= self.words_en_list')     
        print(self.words_en_list)
        #print('========= self.words_metadata')     
        #print([str(wmd) for wmd in self.words_metadata])
        print('========= ')     
        print()


    def get_words_metadata(self, words_es_list):
        words = []

        for i in range(0, len(words_es_list)):
            word_es = words_es_list[i]
            word_en = None # Se calcula cuando se necesite para reducir las llamadas al API de Google
            tag_code = None # Se calcula cuando se necesite para reducir las llamadas al API de Google
            tag_desc = None # Se calcula cuando se necesite para reducir las llamadas al API de Google
            previous_word = words_es_list[i - 1] if i > 0 else ''
            next_word = words_es_list[i + 1] if i < (len(words_es_list) - 1) else ''
            word_position = i

            words.append(WordMetadata(word_es, word_en, tag_code, tag_desc, previous_word, next_word, word_position))

        return words

    
    def evaluate_metric(self, metric_id):
        if metric_id == 'PADI':
            return self._evaluate_PADI()
        elif metric_id == 'PTOR':
            return self._evaluate_PTOR()
        elif metric_id == 'PI':
            return self._evaluate_PI()
        elif metric_id == 'PHTRS':
            return self._evaluate_PHTRS()
        elif metric_id == 'NCCR':
            return self._evaluate_NCCR()
        else:
            print(f'La métrica de NLP { metric_id } no es válida')
            return None


    def _evaluate_PADI(self):
        ambiguity_types = ['lexical', 'syntactic', 'semantic', 'vagueness']
        smells_list = nlp_utils.get_smells_by_ambiguity_type(ambiguity_types, self.smells_dict)  
        NTA = 0
        metric_tags = []

        for word in self.words_metadata:
            evaluation_result = nlp_utils.is_word_an_smell(word, smells_list, self.tags)
            words_affected = evaluation_result[0]
            
            if words_affected > 0:
                NTA = NTA + words_affected
                metric_tags.append({
                    'key': evaluation_result[1],
                    'value': evaluation_result[2]
                    #'scope': words_affected,
                    #'position': word.word_position
                }) 

        metric_result = (int(NTA) / int(self.NTT)) * 100 
        print(f'Smells detectados para métrica PADI: {NTA}, resultado de PADI: {metric_result}')

        return (metric_result, metric_tags)
    

    def _evaluate_PTOR(self):
        #TODO Pendiente como abordar esta metrica
        return (0, [])
    

    def _evaluate_PI(self):         
        ambiguity_types = ['incompleteness']
        smells_list = nlp_utils.get_smells_by_ambiguity_type(ambiguity_types, self.smells_dict)  
        NTI = 0
        metric_tags = []

        for word in self.words_metadata:
            evaluation_result = nlp_utils.is_word_an_smell(word, smells_list, self.tags)
            words_affected = evaluation_result[0]
            
            if words_affected > 0:
                NTI = NTI + words_affected
                metric_tags.append({
                    'key': evaluation_result[1],
                    'value': evaluation_result[2]
                    #'scope': words_affected,
                    #'position': word.word_position
                }) 

        metric_result = (int(NTI) / int(self.NTT)) * 100 
        print(f'Smells detectados para métrica PI: {NTI}, resultado de PI: {metric_result}')

        return (metric_result, metric_tags)
    

    def _evaluate_PHTRS(self):
        #TODO Pendiente como abordar esta metrica
        return (0, [])
    

    def _evaluate_NCCR(self):
        ambiguity_types = ['cc']
        smells_list = nlp_utils.get_smells_by_ambiguity_type(ambiguity_types, self.smells_dict)  
        NCCR = 0
        metric_tags = []

        for word in self.words_metadata:
            evaluation_result = nlp_utils.is_word_an_smell(word, smells_list, self.tags)
            words_affected = evaluation_result[0]
            
            if words_affected > 0:
                NCCR = NCCR + words_affected
                metric_tags.append({
                    'key': evaluation_result[1],
                    'value': evaluation_result[2]
                    #'scope': words_affected,
                    #'position': word.word_position
                }) 

        print(f'Smells detectados para métrica NCCR: {NCCR}')
        return (NCCR, metric_tags)
    