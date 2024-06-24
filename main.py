from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin
import random
from src.utils import *
import src.core.evaluator as evaluator


app = Flask(__name__)
CORS(app)

BASE_URL = 'reqsmells'
PORT = 8080

# Campos del reporte que deberian salir en resumenes
REPORTS_RESUME_FIELDS = ['report_id', 'report_name', 'report_date', 'report_overall_score']
EVALUATIONS_RESUME_FIELDS = ['input_id', 'input_modification_date', 'input_status']

# json files
REPORTS_URL = './data/reports.json'
EVALUATION_DATA_URL = './data/evaluation-data.json'
EVALUATION_EXAMPLE = './data/evaluation.json'


@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origins'] = '*' #'http://localhost:8080,http://localhost:8081'
    response.headers['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Headers, Origin, X-Requested-With, Content-Type, Accept, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, HEAD'
    response.headers['Access-Control-Expose-Headers'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response


# Listado de reportes resumido, sin paginación
@app.route(f'/{BASE_URL}/get-reports-resume', methods=['GET'])
@cross_origin(origin='*')
def get_reports_resume(): 
    reports_resume = read_json(REPORTS_URL)

    # Devolver solo los campos de resumen
    reports_resume = [{field: d[field] for field in REPORTS_RESUME_FIELDS} for d in reports_resume]

    response = jsonify({
        'reports' : reports_resume
    })

    return response


# Listado de reportes resumido, paginado
@app.route(f'/{BASE_URL}/get-reports-resume/<int:page>/<int:page_size>', methods=['GET'])
@cross_origin(origin='*')
def get_paged_reports_resume(page: int, page_size:int): 
    reports_resume = read_json(REPORTS_URL)

    # Devolver solo los campos de resumen
    reports_resume = [{field: d[field] for field in REPORTS_RESUME_FIELDS} for d in reports_resume]
    paged_list, pages_count = paginate_list(reports_resume, page, page_size)

    return jsonify({
        'reports' : paged_list,
        'page': page,
        'pages_count': pages_count
    })


# Obtener detalle de un reporte
@app.route(f'/{BASE_URL}/get-report/<int:report_id>', methods=['GET'])
@cross_origin(origin='*')
def get_report_by_id(report_id:int): 
    reports = read_json(REPORTS_URL)

    # search
    reports = [d for d in reports if d['report_id'] == report_id]
    report = reports[0] if reports != None and len(reports) > 0 else None

    # prepare response    
    error_message = 'No se pudo encontrar el reporte'
    status = 200 if report != None else 404
    response = {'report': report} if report != None else {'message': error_message}

    return jsonify(response), status


# Eliminar reporte
@app.route(f'/{BASE_URL}/delete-report/<int:report_id>', methods=['DELETE'])
@cross_origin(origin='*')
def delete_report(report_id:int):    
    reports_resume = read_json(REPORTS_URL)
    previous_len = len(reports_resume)

    # delete 
    reports_resume = [d for d in reports_resume if d['report_id'] != report_id]
    write_json(REPORTS_URL, reports_resume)

    # prepare response
    report_found = len(reports_resume) < previous_len
    response_message = 'Registro eliminado exitosamente' if report_found else 'No se pudo encontrar reporte para eliminar'
    status = 200 if report_found else 404    

    return jsonify({'message' : response_message}), status


# Obtener listado de datos de evaluacion, filtrados por estado
# ALL: todos
# DRAFT: Evaluaciones pendientes
# EVALUATED: Datos que ya se evaluaron
@app.route(f'/{BASE_URL}/get-evaluation-resume/<status>', methods=['GET'])
@cross_origin(origin='*')
def get_evaluation_data_list(status:str): 
    evaluation_data = read_json(EVALUATION_DATA_URL)

    # Devolver solo los campos de resumen
    evaluation_data = [{field: d[field] for field in EVALUATIONS_RESUME_FIELDS} for d in evaluation_data]

    # Filtrar por estado
    if status != 'ALL':
        evaluation_data = [d for d in evaluation_data if d['input_status'] == status]

    return jsonify({
        'results' : evaluation_data
    })


# Obtener listado de datos de evaluacion paginado, filtrados por estado
# ALL: todos
# DRAFT: Evaluaciones pendientes
# EVALUATED: Datos que ya se evaluaron
@app.route(f'/{BASE_URL}/get-evaluation-resume/<status>/<int:page>/<int:page_size>', methods=['GET'])
@cross_origin(origin='*')
def get_paged_evaluation_data_list(status:str, page: int, page_size:int): 
    evaluation_data = read_json(EVALUATION_DATA_URL)

    # Devolver solo los campos de resumen
    evaluation_data = [{field: d[field] for field in EVALUATIONS_RESUME_FIELDS} for d in evaluation_data]

    paged_list, pages_count = paginate_list(evaluation_data, page, page_size)

    # Filtrar por estado
    if status != 'ALL':
        evaluation_data = [d for d in evaluation_data if d['input_status'] == status]

    return jsonify({
        'results' : paged_list,
        'page': page,
        'pages_count': pages_count
    })


# Obtener detalle de los datos de entrada de una evaluación
@app.route(f'/{BASE_URL}/get-evaluation/<int:input_id>', methods=['GET'])
@cross_origin(origin='*')
def get_evaluation_by_id(input_id:int): 
    evaluation_data = read_json(EVALUATION_DATA_URL)

    # search
    evaluation_data = [d for d in evaluation_data if d['input_id'] == input_id]
    report = evaluation_data[0] if evaluation_data != None and len(evaluation_data) > 0 else None

    # prepare response    
    error_message = 'No se pudo encontrar los datos de entrada'
    status = 200 if report != None else 404
    response = {'results': report} if report != None else {'message': error_message}

    return jsonify(response), status


# Guardar datos de una evaluacion
@app.route(f'/{BASE_URL}/save-evaluation-data', methods=['POST'])
@cross_origin(origin='*')
def save_evaluation_data():
    input_data = request.json
    evaluation_data = read_json(EVALUATION_DATA_URL)
    input_id = None

    # Validar si se está creando una nueva evaluacion o actualizando
    if 'input_id' in input_data:
        input_id = int(input_data['input_id'])

        # Buscar registro a actualizar
        raw_to_update = [d for d in evaluation_data if d['input_id'] == input_id]
        
        # Actualizar solo si existe el registro
        if len(raw_to_update) >= 1:
            evaluation_data = [d for d in evaluation_data if d['input_id'] != input_id]
        else:
            return jsonify({'message' : "No se pudo encontrar el registro para actualizar"}), 404
        
    else:
        new_id = find_max_id(evaluation_data, 'input_id') + 1
        input_data['input_id'] = new_id
        input_id = new_id

    # actualizar fecha de modificacion y estado
    input_data['input_modification_date'] = get_current_date()
    input_data['input_status'] = 'DRAFT'

    evaluation_data.append(input_data)
    write_json(EVALUATION_DATA_URL, evaluation_data)

    return jsonify({'message': "Datos de entrada guardados exitosamente", 'input_data': input_data}), 200


# Eliminar evaluacion
@app.route(f'/{BASE_URL}/delete-evaluation-data/<int:input_id>', methods=['DELETE'])
@cross_origin(origin='*')
def delete_evaluation_data(input_id:int):    
    evaluation_data = read_json(EVALUATION_DATA_URL)
    previous_len = len(evaluation_data)

    # delete 
    evaluation_data = [d for d in evaluation_data if d['input_id'] != input_id]
    write_json(EVALUATION_DATA_URL, evaluation_data)

    # prepare response
    report_found = len(evaluation_data) < previous_len
    response_message = 'Registro eliminado exitosamente' if report_found else 'No se pudo encontrar el registro para eliminar'
    status = 200 if report_found else 404    

    return jsonify({'message' : response_message}), status


# Evaluar datos de entrada (antiguo)
@app.route(f'/{BASE_URL}/evaluate-deprecated', methods=['POST'])
@cross_origin(origin='*')
def evaluate_data_deprecated():
    input_data = request.json
    input_id = int(input_data['input_id'])
    report_name = input_data['report_name']

    # Obtener datos a evaluar
    evaluation_data = read_json(EVALUATION_DATA_URL)
    evaluation_data = [d for d in evaluation_data if d['input_id'] == input_id]
    evaluation_data = evaluation_data[0] if evaluation_data != None and len(evaluation_data) > 0 else None    
    if evaluation_data is None:
        return jsonify({'message': 'No se pudieron encontrar los datos a evaluar'}), 404
    
    # Simular evaluacion
    evaluation = read_json(EVALUATION_EXAMPLE)
    reports_resume = read_json(REPORTS_URL)
    new_id = find_max_id(reports_resume, 'report_id') + 1
    new_report = {
        "report_id": new_id,
        "report_name": report_name,
        "report_date": get_current_date(),
        "report_overall_score": round(random.uniform(0, 100), 2),
        "results_by_requirement": evaluation['results_by_requirement'],
        "results_general": evaluation['results_general']
    }
    reports_resume.append(new_report)
    write_json(REPORTS_URL, reports_resume)

    return jsonify({
            'message': 'Reporte generado exitosamente',
            'report': new_report
        }), 200   


# Evaluar datos de entrada
@app.route(f'/{BASE_URL}/evaluate', methods=['POST'])
@cross_origin(origin='*')
def evaluate_data():
    input_data = request.json
    input_id = int(input_data['input_id'])
    report_name = input_data['report_name']
    reports_resume = read_json(REPORTS_URL)

    # Obtener datos a evaluar
    evaluation_data = read_json(EVALUATION_DATA_URL)
    evaluation_data = [d for d in evaluation_data if d['input_id'] == input_id]
    evaluation_data = evaluation_data[0] if evaluation_data != None and len(evaluation_data) > 0 else None    
    if evaluation_data is None:
        return jsonify({'message': 'No se pudieron encontrar los datos a evaluar'}), 404
    
    # Realizar evaluacion
    new_report = evaluator.evaluate(evaluation_data, report_name)

    reports_resume.append(new_report)
    write_json(REPORTS_URL, reports_resume)

    return jsonify({
            'message': 'Reporte generado exitosamente',
            'report': new_report
        }), 200



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT, debug=True)