# --------------------------------------------------------
# Define los recursos
# --------------------------------------------------------
from commons.dmas.requestcontroller.loadaction import LoadAction
from pbesa.social.poolcontroller.poolcontroller import PoolController

# ----------------------------------------------------------
# Define el agente
# ----------------------------------------------------------
class DRequestController(PoolController):
    """ Controlador de peticiones """
        
    def build(self):
        """
        Metodo que define la estructura del agente.
        """
        # Asigna el comortamiento de actulizacion de conocimiento.
        self.addBehavior('worker-update')
        # Asigna una accion al comportamiento.
        self.bindAction('worker-update', 'load_model', LoadAction())
        # Se suscribe al logger
        self.suscribeLogger('syslog')
        
    def shutdown(self):
        """ Metodo que libera recursos """
        pass