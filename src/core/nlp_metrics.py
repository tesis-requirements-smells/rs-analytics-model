from textblob import TextBlob
from src.utils import *
import src.core.nlp_utils as nlp_utils

SMELLS_URL = './data/smells-dictionary.json'


class NlpMetrics:    

    def __init__(self, text:str):
        self.text = text
        self.blob = TextBlob(text)
        self.words = self.blob.words
        self.NTT = len(self.words)
        self.upper_words = [word.upper() for word in self.words]
        self.smells_dict = read_json(SMELLS_URL)

    
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
        return 0
    

    def _evaluate_PTOR(self):
        #TODO Pendiente como abordar esta metrica
        return 0
    

    def _evaluate_PI(self):
        smells = nlp_utils.get_smells_by_ambiguity_type(['incompleteness'], self.smells_dict)

        # TODO

        return 0
    

    def _evaluate_PHTRS(self):
        #TODO Pendiente como abordar esta metrica
        return 0
    

    def _evaluate_NCCR(self):
        return 0
    