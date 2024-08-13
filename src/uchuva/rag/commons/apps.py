import logging
import traceback
import tensorflow_hub as hub
from django.conf import settings
from django.apps import AppConfig
from commons.engine import Engine
from pbesa.kernel.system.Adm import Adm
from pbesa.social.poolcontroller.pooltype import PoolType
from commons.mas.requestworker.requestworker import RequestWorker
from commons.dmas.requestworker.requestworker import DRequestWorker
from commons.mas.requestcontroller.requestcontroller import RequestController
from commons.dmas.requestcontroller.requestcontroller import DRequestController


class CommonsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "commons"
    log = logging.getLogger('syslog')

    def ready(self):
        """Funcion de inicializacion del componente."""
        #---------------------------------------------
        from commons.models import UserEngine
        # Define el logger del sistema.
        self.log.info("Iniciando SMA de extractor...")
        try:
            # Carga los parametros
            bufferSize = 1
            poolSize = settings.POOL_SIZE
            WORD_COUNT = 30
            #-----------------------------------------
            # Load model.
            self.log.info("Carga el USE...")
            use = hub.load('https://tfhub.dev/google/universal-sentence-encoder/4')
            self.log.info("[OK]: USE cargado")
            engine = Engine(use)
            engine.set_logger(self.log)
            #-----------------------------------------
            # Define el SMA de extractor.
            #-----------------------------------------
            #-----------------------------------------
            # Inicia los agentes trabajadores
            rwList = []
            self.log.info("Creando agentes trabajadores...")
            for id in range(1, poolSize + 1):
                # Crea los agentes request
                agID = "cm_rq_%d" % id
                ag = RequestWorker(agID)
                ag.engine = engine
                ag.start()
                rwList.append(ag)
            self.log.info("[OK]: Agentes trabajadores creados")
            #-----------------------------------------
            # Crea el agente controlador
            self.log.info("Creando el agente controlador...")
            ctrID = 'cm_rq_ctr'
            requestController = RequestController(ctrID, PoolType.BLOCK, bufferSize, poolSize)
            for w in rwList:
                requestController.suscribeAgent(w)
            requestController.start()            
            self.log.info("[OK]: Agente controlador creado")
            self.log.info("[INFO]:[OK]: Poblacion de agentes de extractor inicializada")
            #-----------------------------------------
            # Define el SMA de Concocimiento.
            #-----------------------------------------
            # Obtiene los modelos existenes.
            user_engine_RS = UserEngine.objects.all()
            # Itera sobre los modelos.
            for user_engine in user_engine_RS:
                self.log.info("Crea DSMA Pool para %s..." % user_engine.path)
                # Inicia los agentes trabajadores
                rwList = []
                self.log.info("Creando agentes trabajadores...")
                for id in range(1, poolSize + 1):
                    # Crea los agentes request
                    agID = "d_rq_%s_%d" % (user_engine.path, id)
                    ag = DRequestWorker(agID)
                    ag.start()
                    rwList.append(ag)
                self.log.info("[OK]: Agentes trabajadores creados")
                # Crea el agente controlador del pool
                self.log.info("Creando el agente controlador %s..." % user_engine.path)
                ctrID = 'd_rq_ctr_%s' % user_engine.path
                requestController = DRequestController(ctrID, PoolType.BLOCK, bufferSize, poolSize)
                for w in rwList:
                    requestController.suscribeAgent(w)
                requestController.start()            
                self.log.info("[OK]: Agente controlador %s creado" % user_engine.path)
                # Envia evento de carga del modelo al contrlador.
                dto = {
                    "use": use,
                    "path": user_engine.path
                }
                Adm().sendEvent(ctrID, "load_model", dto)
        except Exception as e:
            self.log.error("Se presento un error al crear la poblacion de datos")
            self.log.error(e)
            traceback.print_exc()