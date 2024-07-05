from src.core.nlp_metrics import NlpMetrics
from src.core.basic_metrics import BasicMetrics
from src.utils import *

# json files
REPORTS_URL = './data/reports.json'

# Métricas que aplican a varios requisitos
METRICS_GENERAL_URL = './data/metrics-general.json'

# Métricas que aplican a un único requisito
METRICS_BY_REQUIREMENT_URL = './data/metrics-by-requirement.json'


def evaluate(evaluation_data:dict, report_name:str):
    reports_resume = read_json(REPORTS_URL)
    new_id = find_max_id(reports_resume, 'report_id') + 1
    input_data_general = evaluation_data['input_data_general']
    input_data_by_requirement = evaluation_data['input_data_by_requirement']
    req_count = len(input_data_by_requirement)

    results_general = get_general_evaluation(input_data_general, req_count)   
    results_by_requirement = get_evaluation_by_requirement(input_data_by_requirement)

    new_report = {
        "report_id": new_id,
        "report_name": report_name,
        "report_date": get_current_date(),
        "report_overall_score": 0, # TODO
        "results_by_requirement": results_by_requirement,
        "results_general": results_general
    }

    return new_report


def get_general_evaluation(input_data_general:dict, req_count:int):
    basic_evaluator = BasicMetrics()
    metrics = read_json(METRICS_GENERAL_URL)
    
    # Si no llega NTR, se toma de la cantidad de requisitos de entrada
    ntr = input_data_general['NTR'] if 'NTR' in input_data_general else req_count
    input_data_general['NTR'] = ntr

    results = []
    for metric in metrics:
        required_params = metric['params']
        params_values = get_metric_params(input_data_general, required_params)
        metric_id = metric['metric_id']
        
        if params_values != None:
            result = basic_evaluator.evaluate_metric(metric_id, params_values)
            metric_result = get_metric_report(metric, result)
            results.append(metric_result)
        else:
            print(f'No se enviaron los parámetros suficientes para calcular la métrica general: { metric_id }')

    return results


def get_evaluation_by_requirement(evaluation_data:dict):
    basic_evaluator = BasicMetrics()
    metrics = read_json(METRICS_BY_REQUIREMENT_URL)
    results = []

    for req_data in evaluation_data:
        req_code = req_data['req_code']
        req_name = req_data['req_name']
        req_params = req_data['req_data']
        req_detail = req_params['REQUIREMENT_DESCRIPTION']        
        nlp_evaluator = NlpMetrics(req_detail)
        req_results = []
        print(f'Evaluando requisito { req_code }')

        for metric in metrics:
            is_nlp_metric = 'nlp_metric' in metric and metric['nlp_metric'] == True            
            metric_id = metric['metric_id']

            if is_nlp_metric:
                result = nlp_evaluator.evaluate_metric(metric_id)
                metric_result = get_metric_report(metric, result)
                req_results.append(metric_result)
            else:
                required_params = metric['params']
                params_values = get_metric_params(req_params, required_params)                
            
                if params_values != None:
                    result = basic_evaluator.evaluate_metric(metric_id, params_values)
                    metric_result = get_metric_report(metric, result)
                    req_results.append(metric_result)
                else:
                    print(f'No se enviaron los parámetros suficientes para calcular la métrica: { metric_id } para el requisito: { req_code }')

        req_result = {
            'req_code': req_code,
            'req_name': req_name,
            'req_detail': req_detail,
            'results': req_results
        }
        
        results.append(req_result)  

    return results


def get_metric_params(input:list, required_params:list):
    """ Obtiene los parametros necesarios para una metrica, en caso de que esten todos, de lo contrario, retorna nulo 
    """
    results = {}
    for required_param in required_params:        
        if required_param in input and str(input[required_param]) not in ['', 'None']:
            results[required_param] = input[required_param]
        else:
            return None

    return results


def get_metric_report(metric_info, result):
    """ Obtener el diccionario resultado de una metrica según el resultado
    """    
    ranges = metric_info['ranges']
    metric_id = metric_info['metric_id']
    classification = ''
    description = ''
    severity = ''

    for range in ranges:
        range_found = False
        min = int(range['min'])
        max = int(range['max'])
        #print(f'min: {min} max: {max} result: {result}')

        if result != None and (min <= result <= max):
            classification = range['classification']
            description = range['description']
            severity = range['severity']
            range_found = True
            break

    if not range_found:
        print(f'Error calculando métrica: { metric_id }: Valor fuera de los rangos permitosos. Valor: { result }')

    return {
        "metric_id": metric_id,
        "metric_name": metric_info['metric_name'],
        "score": result,
        "classification": classification,
        "description": description,
        "severity": severity,
        "tags": []
    }

