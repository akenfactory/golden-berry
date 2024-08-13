#------------------------------------------
# Import the necessary modules
#------------------------------------------

import os
import json
import pymongo
import traceback
import numpy as np
from joblib import load
from gensim import models

#------------------------------------------
# Define variables and constants
#------------------------------------------

# Define el path del modelo w2v.
W2V_PATH = 'w2v.mdl'

# Define el path del espacio vectorial.
DOC_DICT_PATH = 'docList.joblib'

# Define el path del archivo de libros.
BOOKS_PATH = 'book_normalized.json'

#------------------------------------------
# Define clasess
#------------------------------------------

class DocSim:

    def __init__(self, debug=False, log=None):
        """Constructor de la clase."""
        self.log = log
        self.w2vModel = None
        self.docDict = None
        self.debug = debug
        self.add_path = ""
        if self.debug:
            self.add_path = "../model/"
            
    def set_up(self):
        """ Inicializa el componente """
        try:
            # Carga el espacio vectorial
            if os.path.isfile(self.add_path + W2V_PATH):
                self.w2vModel = models.Word2Vec.load(self.add_path + W2V_PATH)
            # Carga los vetores
            if os.path.isfile(self.add_path + DOC_DICT_PATH):
                self.docDict = load(self.add_path + DOC_DICT_PATH)
        except Exception as e:
            trace_err = traceback.format_exc()
            err = str(e) + " - " + trace_err
            self.log.error(err)
            self.log.error("No se pudo inicializar el espacio vectorial")
    
    def vectorize(self, words):
        """
        Vectoriza el texto tokenizado
        @param words token de la sentencia
        @retun el vector correspondiente
        """
        try:
            wordVecs = []
            for word in words:
                try:
                    vec = self.w2vModel.wv[word] 
                    wordVecs.append(vec)
                except KeyError:
                    pass
            vector = np.mean(wordVecs, axis=0)
            return vector
        except Exception as e:
            trace_err = traceback.format_exc()
            err = str(e) + " - " + trace_err
            self.log.error(err)
            return None

    def cosineSim(self, vecA, vecB):
        """ 
        Calcula la distancia de coseno 
        @param vecA Vector A
        @param vecB Vector B
        @return Distancia
        """
        try:
            csim = np.dot(vecA, vecB) / (np.linalg.norm(vecA) * np.linalg.norm(vecB))
            if np.isnan(np.sum(csim)):
                return 0
            return csim
        except Exception as e:
            trace_err = traceback.format_exc()
            err = str(e) + " - " + trace_err
            self.log.error(err)
            return 0

    def calculate_similarity(self, doc):
        """
        Calcula la similaridad dado un umbral
        @param doc la sentencia a evaluar
        @return el resultado de la comparacion
        """
        try:
            doc_tokens = doc.split()
            docVec = self.vectorize(doc_tokens)
            documents_index = [{
                'docID': '',
                'score': 0
            },{
                'docID': '',
                'score': 0
            },{
                'docID': '',
                'score': 0
            },]
            for item in self.docDict:
                key = item['docID']
                docVc = item
                simScore = self.cosineSim(docVec, docVc['vector'])
                for index in documents_index:
                    if simScore > index['score']:
                        index['docID'] = key
                        index['score'] = simScore
                        break
            return documents_index
        except Exception as e:
            trace_err = traceback.format_exc()
            err = str(e) + " - " + trace_err
            self.log.error(err)
            return []

class ModelHandler:

    def __init__(self, debug=False, log=None):
        """Constructor de la clase."""
        try:
            self.log = log
            self.debug = debug
            self.docSim = DocSim(self.debug, self.log)
            self.docSim.set_up()
            # Define el path del modelo w2v.
            self.add_path = ""
            if self.debug:
                self.add_path = "../model/"
            # Load book_normalized.json file
            self.books = None
            self.books = json.load(open(self.add_path + BOOKS_PATH, 'r'))
            # Connect to MongoDB
            mongo_uri = f"mongodb://192.168.0.22:27017"
            client = pymongo.MongoClient(mongo_uri)
            self.db = client.angel
        except Exception as e:
            trace_err = traceback.format_exc()
            err = str(e) + " - " + trace_err
            self.log.error(err)
        
    def process_document(self, doc):
        """
        Calcula la similaridad dado un umbral
        @param doc la sentencia a evaluar
        @return el resultado de la comparacion
        """
        try:
            documents = []
            documents_index = self.docSim.calculate_similarity(doc)
            for item in documents_index:
                key_split = item['docID'].split('_')
                book = self.books[key_split[0]]
                chapter = book['chapters'][key_split[1]]
                verse = chapter['verses'][key_split[2]]
                documents.append({
                    'book': key_split[0],
                    'chapter': key_split[1],
                    'verse': key_split[2],
                    'text': verse['text']
                }) 
            return documents
        except Exception as e:
            trace_err = traceback.format_exc()
            err = str(e) + " - " + trace_err
            self.log.error(err)
            return []
    
    def get_citation(self):
        try:
            attemps = 0
            document = None
            while document is None and attemps < 10:
                # Generate random
                random_number = np.random.randint(0, 2246)
                # Get document by name from mongodb
                document = self.db.citations.find_one({"index": str(random_number)})
                attemps += 1
            # Transform document to dictionary
            document = {
                'text': document['text']
            }
            return document
        except Exception as e:
            trace_err = traceback.format_exc()
            err = str(e) + " - " + trace_err
            self.log.error(err)
            return None