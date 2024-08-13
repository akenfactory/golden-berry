from pbesa.kernel.agent.Action import Action

class UpdateAction(Action):
    """ An action is a response to the occurrence of an event """

    def execute(self, data):
        """ 
        Response.
        @param data Event data 
        """
        self.agent.engine = data['engine']
        self.agent.log.info("[%s]:[OK]: Dominio de conocimiento cargado." % self.agent.id)

    def catchException(self, exception):
        """
        Catch the exception.
        @param exception Response exception
        """
        print("Error: %s" % exception)