from .requesttask import DRequestTask
from pbesa.social.worker.worker import Worker
from commons.dmas.requestworker.updateaction import UpdateAction

# --------------------------------------------------------
# Define el agente
# --------------------------------------------------------

class DRequestWorker(Worker):
    """ Agente trabajador de peticiones """
    
    def __init__(self, agentID):
        self.engine = None
        super().__init__(agentID)
    
    def build(self):
        """
        Method que define la estructura del agente
        """
        # Asigna el comortamiento de actulizacion de conocimiento.
        self.addBehavior('update')
        # Asigna una accion al comportamiento.
        self.bindAction('update', 'update_know_domain', UpdateAction())
        # Asigna la tarea al trabajador
        self.bindTask(DRequestTask())
        # Se suscribe al logger
        self.suscribeLogger('syslog')
        
    def shutdown(self):
        """ Metodo para liberar recursos """
        self.engine = None