import src.core.nlp_utils as nlp_utils
from googletrans import Translator
from textblob import TextBlob
from src.core.nlp_metrics import NlpMetrics
import src.core.nlp_utils as nlp_utils


# Prueba de analisis de smell
"""
Inferior a          OK
Limpio              OK
rapidísimo          OK
mejor carro que     OK
Rápidamente         OK
mas feliz que
"""
"""
text = "El segundo lugar es inferior a lo esperado, pero el coche estaba limpio y Juan llegó rapidísimo. Él tiene el mejor carro que Luis y se sintió más feliz que nunca al saberlo. Rápidamente, se preparó para la próxima carrera."
nlp_metrics_object = NlpMetrics(text)
result = nlp_metrics_object._evaluate_PADI()
print(f'Resultado de PADI: {result}')
"""


text = "El segundo lugar es inferior a lo esperado, pero el coche estaba limpio y Juan llegó rapidísimo. Él tiene el mejor carro que Luis y se sintió más feliz que nunca al saberlo. Rápidamente, se preparó para la próxima carrera."
nlp_metrics_object = NlpMetrics(text)
result = nlp_metrics_object._evaluate_PADI()
print(f'Resultado de PADI: {result}')
