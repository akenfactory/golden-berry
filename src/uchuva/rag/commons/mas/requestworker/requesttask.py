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
class RequestTask(Task):
    
    def generate_random_filename(self, length=10):
        """Generate a random filename with the given length."""
        letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
        return ''.join(random.choice(letters) for _ in range(length))

    # Define function for generate response
    def generate_answer(self, dto):
        try:
            # Define path and name file.
            random_filename = self.generate_random_filename(10)
            destination_path = os.path.join('/app/files/', random_filename + '.pdf')
            # Create PDF file from data.
            # Decode the base64 string into bytes
            pdf_bytes = base64.b64decode(dto['documento'])
            # Write the bytes to a file with a .pdf extension
            with open(destination_path, 'wb') as output_file:
                output_file.write(pdf_bytes)
            # Check if file exists.
            if not Path(destination_path).is_file():
                return {
                    "status": False,
                    "data": "No se pudo procesar el archivo"
                }
            # Read the pdf file.
            page_list = self.agent.engine.get_text_from_pdf(destination_path)
            print("Count page: ", len(page_list))
            # Define chuncks.
            chunks = []
            page_number = 1
            for page in page_list:
                doc_chunks = self.agent.engine.text_to_chunks(page, 30, page_number)
                chunks.extend(doc_chunks)
                page_number += 1
            # Fit NN.
            self.agent.engine.fit(chunks)
            # Get nearest chunks for each property.
            nearest_chunks_list = []
            propiedades = dto['propiedades'].lower()
            questions = propiedades.split(',')
            for question in questions:
                nearest_chunks = self.agent.engine.call(question)
                nearest_chunks_list.extend(nearest_chunks)
            # Delete file.
            os.remove(destination_path)
            # Generate text.
            texto = ""
            for chunk in nearest_chunks_list:
                texto += chunk.text + "\n"
            # Generate format.
            formato = ""
            for question in questions:
                formato += question + ": valor\n"
            # Generate prompt.
            promtp = """
                Del siguiente texto: "{texto}"
                indicame cual es {propiedades}. 
                Respondiendo en el siguiente formato {formato}.
            """.format_map({
                "texto": texto,
                "propiedades": propiedades,
                "formato": dto['propiedades']
            })
            print(promtp)
            return {
                "status": True,
                "data": promtp
            }
        except Exception as e:
            print(traceback.format_exc())
            return {
                "status": False,
                "data": str(e)
            }

    def goHead(self, data):
        """
        Metodo de reaccion al evento.
        @param data Datos del evento
        """
        try:
            answer = self.generate_answer(data)
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