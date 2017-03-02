
import gensim
from gensim.models.doc2vec import  *

from preprocessor.cleaner import Preprocessor as preprocessor

cleaner = preprocessor()

class LabeledLineSentence(object):
    def __init__(self, doc_list, labels_list):
       self.labels_list = labels_list
       self.doc_list = doc_list

    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
            yield TaggedDocument(words=cleaner.cleanMePlease(doc.decode('utf-8')),tags=[self.labels_list[idx]])