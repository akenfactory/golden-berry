import os
from commons.engine import Engine
from pbesa.kernel.agent.Action import Action

class LoadAction(Action):
    """ An action is a response to the occurrence of an event """

    def execute(self, data):
        """ 
        Response.
        @param data Event data 
        """
        # Define path and name file.
        destination_path = os.path.join('/app/files/', data['path'] + '.pdf')
        # Define engine.
        engine = Engine(data['use'])
        engine.set_logger(self.agent.log)
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
        # Update know domain of agents.
        dto = {
            'engine': engine
        }
        self.agent.broadcastEvent("update_know_domain", dto)
        
    def catchException(self, exception):
        """
        Catch the exception.
        @param exception Response exception
        """
        print("Error: %s" % exception)