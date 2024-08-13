#------------------------------------------
# Import the necessary modules
#------------------------------------------

import os
from cmdsim import CMDSim
from util import setup_mongo_logging
from model_manager import ModelHandler
from flask import Flask, request, jsonify
from security_manager import check_accsess

#------------------------------------------
# Defibe variables and constants
#------------------------------------------

# Define the DEBUG flag
DEBUG = os.getenv('ENVIRONMENT', 'dev').lower() == 'dev'

# Define flask app
app = Flask(__name__)

# Define the logger
log = setup_mongo_logging('angel_doc', 'documents-ms')

# Define the model handler
modelHandler = ModelHandler(DEBUG, log)

# Define the CMDSim object
cmd_sim = CMDSim(DEBUG, log)
cmd_sim.setup()

#------------------------------------------
# Define routes
#------------------------------------------
@app.route('/documents/alive', methods=['POST'])
def alive():
    data = request.get_json()
    # Check parameters
    if not data:
        return jsonify({'message': 'Bad request'}), 400
    log.info('Alive request received', extra={'log_data': {'key': data['key']}})
    return jsonify({'message': 'Hello, ' + data['key']}), 200

@app.route('/documents/get-documents', methods=['POST'])
def get_documents():
    data = request.get_json()
    # Check parameters
    if not data:
        return jsonify({'message': 'Bad request'}), 400
    try:
        # Check access
        if not check_accsess(data['token']):
            return jsonify({'message': 'Unauthorized'}), 401
        documents = modelHandler.process_document(data['doc'])
        return jsonify(documents), 200
    except Exception as e:
        log.error('Error processing document', extra={'log_data': {'error': str(e)}})
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/documents/get-citation', methods=['POST'])
def get_citation():
    data = request.get_json()
    # Check parameters
    if not data:
        return jsonify({'message': 'Bad request'}), 400
    try:
        # Check access
        if not check_accsess(data['token']):
            return jsonify({'message': 'Unauthorized'}), 401
        document = modelHandler.get_citation()
        return jsonify(document), 200
    except Exception as e:
        log.error('Error getting citation', extra={'log_data': {'error': str(e)}})
        return jsonify({'message': 'Internal server error'}), 500


@app.route('/documents/get-command', methods=['POST'])
def get_command():
    data = request.get_json()
    # Check parameters
    if not data:
        return jsonify({'message': 'Bad request'}), 400
    try:
        command = cmd_sim.get_command(data['text'])
        res = {
            'command': command
        }
        return jsonify(res), 200
    except Exception as e:
        log.error('Error getting command', extra={'log_data': {'error': str(e)}})
        return jsonify({'message': 'Internal server error'}), 500
    
#------------------------------------------
# Main
#------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)