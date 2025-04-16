from core.document_reader import DocumentReader, InputData

def CreateDocument(path : str):
    document = DocumentReader(path)
    return document.data

def GetByDay(data : InputData):
    
    pass
