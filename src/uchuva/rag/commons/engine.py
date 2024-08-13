import re
import openai
import pdfplumber
import numpy as np
from lxml import html
from sklearn.neighbors import NearestNeighbors
from commons.chunkdocument import ChunkDocument

# Define el motor de IA.
class Engine:
    
    def __init__(self, use):
        # Obtiene universal sentence encoder
        self.use = use
        self.fitted = False
        self.log = None

    def set_logger(self, log):
        """Asigna el logger."""
        self.log = log
    
    def clear_text(self, text):
        """Limpiar el texto de caracteres no deseados."""
        text = text.lower()
        # Transforma el texto en un árbol de elementos.
        tree = html.fromstring(text)    
        # Remuve todas las etiquetas y obtiene el contenido del texto.
        clean_text = tree.text_content()
        # Remueve los saltos de línea y espacios adicionales.
        clean_text = re.sub('\n+', '\n', clean_text)
        clean_text = re.sub('\s+', ' ', clean_text)
        clean_text = clean_text.replace('[[_TOC_]]', '')
        # Remueve los caracteres no deseados.
        clean_text = re.sub(r'\*\*(.*?)\*\*', r'\1', clean_text)
        clean_text = re.sub(r'\*(.*?)\*', r'\1', clean_text) 
        return clean_text

    def get_text_from_pdf(self, pdf_path):
        """Obtiene el texto de un archivo PDF."""
        page_list = []
        with pdfplumber.open(pdf_path) as pdf:
            # Obtiene el número de páginas del PDF.
            self.log.info("Number of pages: " +  str(len(pdf.pages)))
            page_number = 1
            for page in pdf.pages:
                # Obtiene el texto de la página.
                self.log.info("Page number: " + str(page_number))
                page_list.append(page.extract_text())
                page_number += 1
        return page_list

    def split_sentence_by_word_count(self, sentence, wordNumber):
        """Divide una oración en varias oraciones de acuerdo al número de palabras."""
        words = sentence.split()
        result = [' '.join(words[i:i+wordNumber]) for i in range(0, len(words), wordNumber)]
        return result

    def text_to_chunks(self, page, word_count=30, page_number=1):
        """Divide un texto en fragmentos de acuerdo al número de palabras."""
        chunks = []
        text = self.clear_text(page)
        split_sentence = self.split_sentence_by_word_count(text, word_count)
        for fit_chunk in split_sentence:
            chunk = ChunkDocument(page_number, fit_chunk)
            chunks.append(chunk)
        return chunks
    
    def fit(self, data, batch=1000, n_neighbors=5):
        """ Efectua el entrenamiento del componente de vecinos más cercanos. """
        self.data = data
        # Obtiene los embeddings de los textos.
        self.embeddings = self.get_text_embedding(data, batch=batch)
        # Se calula el número máximo de vecinos más cercanos
        # a considerar basado en el parámetro n_neighbors
        # y el número de embeddings.
        n_neighbors = min(n_neighbors, len(self.embeddings))
        # Inicia el modelo para la búsqueda de vecinos más cercanos.
        self.nn = NearestNeighbors(n_neighbors=n_neighbors)
        # Se entrena el modelo con los embeddings.
        self.nn.fit(self.embeddings)
        self.fitted = True
    
    def call(self, text, return_data=True):
        # Genera los embeddings para el texto de entrada.
        inp_emb = self.use([text])
        # Obtiene los vecinos más cercanos para el vector
        # de representación del texto de entrada y
        # retorna los índices de los vecinos en el
        # conjunto de datos original.
        neighbors = self.nn.kneighbors(inp_emb, return_distance=False)[0]    
        if return_data:
            return [self.data[i] for i in neighbors]
        else:
            return neighbors
    
    def get_text_embedding(self, chunk_doc_list, batch=1000):
        """ Obtiene los embeddings de los textos."""
        embeddings = []
        for i in range(0, len(chunk_doc_list), batch):
            chunk_batch = chunk_doc_list[i:(i+batch)]
            text_batch = [doc.text for doc in chunk_batch]
            emb_batch = self.use(text_batch)
            embeddings.append(emb_batch)
        embeddings = np.vstack(embeddings)
        return embeddings
    
    def generate_text(self, endpoint, openAI_key, prompt, engine="gpt-35-turbo"):
        openai.api_type = "azure"
        openai.api_base = endpoint
        openai.api_version = "2023-03-15-preview"
        openai.api_key = openAI_key
        response = openai.ChatCompletion.create(
            engine="gpt-35-turbo",
            messages = [{"role":"user","content":prompt}],
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        self.log.info("Respuesta:", response)
        message = response.choices[0]['message']['content']
        return message
