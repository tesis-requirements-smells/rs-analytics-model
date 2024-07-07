from googletrans import Translator

class WordMetadata:

    def __init__(self, word_es:str, word_en:str, tag_code:str, tag_desc:str, previous_word:str, next_word:str, word_position:int):
        self._translator = Translator()
        self.word_es = word_es
        self._word_en = word_en
        self.tag_code = tag_code
        self.tag_desc = tag_desc
        self.previous_word = previous_word
        self.next_word = next_word
        self.word_position = word_position

    
    def __str__(self):
        return (f'WordMetadata('
                f'word_es="{self.word_es}", '
                f'word_en="{self._word_en}", '
                f'tag_code="{self.tag_code}", '
                f'tag_desc="{self.tag_desc}", '
                f'previous_word="{self.previous_word}", '
                f'next_word="{self.next_word}")')


    # Se calcula solo si se necesita, para reducir las llamadas al API de traducción de Google    
    def get_word_en(self):
        if self._word_en == None:
            print('LLAMADA AL API DE GOOGLE PARA TRADUCIR PALABRA')
            self._word_en = self._translator.translate(self.word_es, src='es', dest='en').text
        return self._word_en