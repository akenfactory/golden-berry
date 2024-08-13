import os
import base64
import random
import string
import traceback
from pathlib import Path
from pbesa.social.worker.task import Task

# ----------------------------------------------------------
# Define la accion
# ----------------------------------------------------------
class DRequestTask(Task):
        
    # Define function for generate response
    def generate_answer(self, question):
        topn_chunks = self.agent.engine.call(question)
        prompt = ""
        prompt += 'Buscar resultados:\n\n'
        for c in topn_chunks:
            prompt += c.text + '\n\n'
        prompt += "Instrucciones: Redacta una respuesta completa a la consulta utilizando los resultados de búsqueda proporcionados. "\
                "Si los resultados de búsqueda mencionan varios temas "\
                "con el mismo nombre, crea respuestas separadas para cada uno. Solo incluye información encontrada en los resultados "\
                "y no agregues información adicional. Asegúrate de que la respuesta sea correcta y no proporciones contenido falso. "\
                "Si el texto no se relaciona con la consulta, simplemente indica 'Consulta no encontrada'. Ignora los resultados "\
                "de búsqueda atípicos que no tengan nada que ver con la pregunta. Responde solo lo que se pregunta. La "\
                "respuesta debe ser breve y concisa."
        prompt += f"\nConsulta: {question}\nRespuesta:"
        return prompt

    def goHead(self, data):
        """
        Metodo de reaccion al evento.
        @param data Datos del evento
        """
        try:
            answer = self.generate_answer(data['prompt'])
            self.sendResponse(answer)
        except Exception as e:
            self.log.error("Se presento un error al generar la respuesta")
            self.log.error(e)
            traceback.print_exc()
            self.sendResponse(None)

    def catchException(self, exception):
        """
        Captura la excepcion.
        @param exception Excepcion
        """
        self.log.error(exception)
        self.sendResponse([[], '[001]: Could not respond to request'])