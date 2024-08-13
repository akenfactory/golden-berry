from .requesttask import RequestTask
from pbesa.social.worker.worker import Worker

# --------------------------------------------------------
# Define el agente
# --------------------------------------------------------

class RequestWorker(Worker):
    """ Agente trabajador de peticiones """
    
    def __init__(self, agentID):
        self.engine = None
        super().__init__(agentID)
    
    def build(self):
        """
        Method que define la estructura del agente
        """
        # Asigna la tarea al trabajador
        self.bindTask(RequestTask())
        # Se suscribe al logger
        self.suscribeLogger('syslog')
        
    def shutdown(self):
        """ Metodo para liberar recursos """
        self.engine = None