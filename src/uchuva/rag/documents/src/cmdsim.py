#------------------------------------------
# Import the necessary modules
#------------------------------------------

import os
import string
import difflib
import traceback
import numpy as np
import unicodedata
from joblib import load
from gensim import models
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#------------------------------------------
# Define variables and constants
#------------------------------------------

# Define el path del modelo w2v.
W2V_PATH = 'cmdW2v.mdl'

# Define el path del espacio vectorial.
DOC_DICT_PATH = 'cmdList.joblib'

# Define dimension del espacio
W2V_SIZE = 300

# Define el tamano de la ventana 
W2V_WINDOW = 5

# Define la cantidad minima de relaciones
W2V_MINCOUNT = 1

# Define las epocas del modelo de defensa
W2V_DEF_EPOCHS = 5

# Define el umbral de similitid de palabras
W_SIMILARITY_THRESHOLD = 0.8

# Define el umbral de similitid de documentos
DOC_SIMILARITY_THRESHOLD = 0.77

#------------------------------------------
# Define clasess
#------------------------------------------

class CMDSim:

    def __init__(self, debug=False, log=None):
        """Constructor de la clase."""
        self.log = log
        self.w2vModel = None
        self.docDict = None
        self.debug = debug
        self.add_path = ""
        # Define la lista de palabras sin significado
        self.stopwords = set(stopwords.words("spanish"))
        # Defina dimension del espacio
        self.w2vSize = W2V_SIZE
        # Define el tamano de la ventana 
        self.w2vWindow = W2V_WINDOW
        # Define la cantidad minima de relaciones
        self.w2vMinCount = W2V_MINCOUNT
        # Define las epocas
        self.w2vEpochs = W2V_DEF_EPOCHS
        # Define la lista de sentencias
        self.sentences = []
        # Define la lista de documentos
        self.docList = []
        # Define el vocabulario
        self.vocabulary = []
        # Define el diccionario de comandos
        self.commands = {
            'r':      'Registrarme',
            'is':     'Iniciar sesión',
            'cs':     'Cerrar sesión',
            'er':     'Recuperar contraseña',
            'ctb':    'Consulta texto bíblico',
            'obs':    'Ofrezco bienes o servicios',
            'bbs':    'Busco bienes o servicios',
            'apc':    'Adicionar persona a contactos',
            'lc':     'Listar contactos',
            'emc':    'Enviar mensaje a contacto',
            'cg':     'Crear grupo',
            'lg':     'Listar grupos',
            'el':     'Eliminar grupo',
            'apg':    'Adicionar persona a grupo',
            'epg':    'Eliminar persona de grupo',
            'lpg':    'Listar personas de grupo',
            'emg':    'Enviar mensaje a grupo',
            'cr':     'Crear recordatorio',
            'er':     'Eliminar recordatorio',
            'lr':     'Listar recordatorios',
            'cm':     'Compartir mensaje',
        }
        if self.debug:
            self.add_path = "../model/"
            
    def setup(self):
        """ Inicializa el componente """
        try:
            # Carga el espacio vectorial
            if os.path.isfile(self.add_path + W2V_PATH):
                self.w2vModel = models.Word2Vec.load(self.add_path + W2V_PATH)
            # Carga los vetores
            if os.path.isfile(self.add_path + DOC_DICT_PATH):
                self.docDict = load(self.add_path + DOC_DICT_PATH)
            # Carga el vocabulario
            if os.path.isfile(self.add_path + 'vocabulary.joblib'):
                self.vocabulary = load(self.add_path + 'vocabulary.joblib')
        except Exception as e:
            trace_err = traceback.format_exc()
            err = str(e) + " - " + trace_err
            self.log.error(err)
            self.log.error("No se pudo inicializar el espacio vectorial")
    
    def normalizeEText(self, text):
        """
        Metodo que normaliza un texto.
        @param text Texto a normalizar
        @param text el texto normalizado
        """
        if text:
            punctuation = str.maketrans('','',string.punctuation)
            text = text.lower()
            text = text.replace('\r', ' ')
            text = text.replace('\n', ' ')
            text = text.replace('\t', ' ')
            text = text.replace("'", '')
            text = ' '.join(text.split())
            text = text.translate(punctuation)
            text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore')
            return text.decode("utf-8")
        else:
            return ""
    
    def find_closest_word(self, vocabulary, partial_word):
        closest_matches = difflib.get_close_matches(partial_word, vocabulary, n=1, cutoff=W_SIMILARITY_THRESHOLD)
        if closest_matches:
            return closest_matches[0]
        else:
            return None
        
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
                    print("La palabra '%s' no esta en el vocabulario" % word)
                    similar = self.find_closest_word(self.vocabulary, word)
                    if similar:
                        print("La palabra %s se reemplaza por %s" % (word, similar))
                        try:
                            vec = self.w2vModel.wv[similar] 
                            wordVecs.append(vec)
                        except KeyError:
                            pass
            if len(wordVecs) == 0:
                return None
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
            doc_tokens = word_tokenize(doc)
            docVec = self.vectorize(doc_tokens)
            docID = None
            score = 0
            if docVec is not None:
                for item in self.docDict:
                    key = item['docID']
                    docVc = item
                    simScore = self.cosineSim(docVec, docVc['vector'])
                    if simScore > score:
                        docID = key
                        score = simScore
            return docID, score
        except Exception as e:
            trace_err = traceback.format_exc()
            err = str(e) + " - " + trace_err
            self.log.error(err)
            return None, 0
    
    def get_command(self, text):
        text = self.normalizeEText(text)
        docID, score = self.calculate_similarity(text)
        if docID:
            print("Documento: %s - Score: %f" % (docID, score))
            if score >= DOC_SIMILARITY_THRESHOLD:    
                key = docID.split("_")[0]
                print("Comando: %s - Score: %f" % (self.commands[key], score))
                cmd = self.commands[key]
                cmd = self.normalizeEText(cmd)
                return cmd
            else:
                print("No se encontro comando")
                return None
        else:
            print("No se encontro comando")
            return None