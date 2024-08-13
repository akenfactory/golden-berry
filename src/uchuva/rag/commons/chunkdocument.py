class ChunkDocument(object):
    """
    Clase que representa un documento.
    """
    def __init__(self, page_number, text):
        """
        Constructor de la clase.
        """
        self.page_number = page_number 
        self.text = text