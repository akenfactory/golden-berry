# --------------------------------------------------------
# Define los recursos
# --------------------------------------------------------
from pbesa.social.poolcontroller.poolcontroller import PoolController

# ----------------------------------------------------------
# Define el agente
# ----------------------------------------------------------
class RequestController(PoolController):
    """ Controlador de peticiones """
        
    def build(self):
        """
        Metodo que define la estructura del agente.
        """
        # Se suscribe al logger
        self.suscribeLogger('syslog')
        
    def shutdown(self):
        """ Metodo que libera recursos """
        pass