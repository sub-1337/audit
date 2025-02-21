from core.document_reader import DocumentReader

def CreateDocument(path : str):
    document = DocumentReader(path)
    return document.data