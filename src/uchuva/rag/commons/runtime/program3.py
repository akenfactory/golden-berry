#--------------------------------------
# Import package.
#--------------------------------------
import os
import base64
import logging
import datetime
import traceback
from pathlib import Path
import tensorflow_hub as hub
from django.conf import settings
from commons.engine import Engine
from commons.models import UserEngine
from pbesa.kernel.system.Adm import Adm
from pbesa.social.poolcontroller.pooltype import PoolType
from commons.dmas.requestworker.requestworker import DRequestWorker
from commons.dmas.requestcontroller.requestcontroller import DRequestController

#--------------------------------------
# Define functions.
#--------------------------------------

# Define logger.
log = logging.getLogger('wikilog')

def update_know_domain(dto):
    """Update know domain of robot."""
    try:
        # Define varibles.
        poolSize = settings.POOL_SIZE
        # Load USE.
        use = hub.load('https://tfhub.dev/google/universal-sentence-encoder/4')
        # Define path and name file.
        destination_path = os.path.join('/app/files/', dto['path'] + '.pdf')
        # Decode the base64 string into bytes
        pdf_bytes = base64.b64decode(dto['documento'])
        # Check if file exists.
        if Path(destination_path).is_file():
            os.remove(destination_path)
        # Write the bytes to a file with a .pdf extension
        with open(destination_path, 'wb') as output_file:
            output_file.write(pdf_bytes)
        # Check if file exists.
        if not Path(destination_path).is_file():
            return False
        # Define engine.
        engine = Engine(use)
        engine.set_logger(log)
        # Read the pdf file.
        page_list = engine.get_text_from_pdf(destination_path)
        # Define chuncks.
        chunks = []
        page_number = 1
        for page in page_list:
            doc_chunks = engine.text_to_chunks(page, 30, page_number)
            chunks.extend(doc_chunks)
            page_number += 1
        # Fit NN.
        engine.fit(chunks)
        #--------------------------------------
        # Update know domain or create agent.
        #--------------------------------------
        user_engine_RS = UserEngine.objects.filter(path=dto['path'])
        if user_engine_RS and len(user_engine_RS) > 0:
            n_dto = {
                'engine': engine
            }
            # Update know domain of existing agents.
            for id in range(1, poolSize + 1):
                agID = "d_rq_%s_%d" % (dto['path'], id)
                Adm().sendEvent(agID, "update_know_domain", n_dto)
        else:
            # Create new agents.
            # Inicia los agentes trabajadores
            rwList = []
            log.info("Creando agentes trabajadores...")
            for id in range(1, poolSize + 1):
                # Crea los agentes request
                agID = "d_rq_%s_%d" % (dto['path'], id)
                ag = DRequestWorker(agID)
                ag.engine = engine
                ag.start()
                rwList.append(ag)
            log.info("[OK]: Agentes trabajadores creados")
            # Crea el agente controlador del pool
            log.info("Creando el agente controlador %s..." % dto['path'])
            ctrID = 'd_rq_ctr_%s' % dto['path']
            requestController = DRequestController(ctrID, PoolType.BLOCK, 1, poolSize)
            for w in rwList:
                requestController.suscribeAgent(w)
            requestController.start()
            # Register in database.
            user_engine = UserEngine()
            user_engine.User = dto['user']
            user_engine.path = dto['path']
            user_engine.created = datetime.datetime.utcnow()
            user_engine.save()
        return True
    except Exception as e:
        print("Error: ", e)
        traceback.print_exc()
        return False