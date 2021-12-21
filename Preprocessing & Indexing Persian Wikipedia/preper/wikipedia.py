import xml.etree.ElementTree as et
import preper


class Wikipedia:
    doc_store = []

    def __init__(self, path):
        normalizer = preper.Normalizer()
        file = open(path, 'r', encoding='utf-8')
        file_string = file.read()
        root = et.fromstring(file_string)
        counter = 0
        for doc in root.findall(r'doc'):
            if doc.find('title') is None or doc.find('abstract') is None:
                continue
            else:
                self.doc_store.append(preper.Document(doc.find('title').text, doc.find('abstract').text, counter))
            counter += 1

        for doc in self.doc_store:
            if doc.body is not None:
                doc.body = normalizer.normalize(doc.body)
            if doc.title is not None:
                doc.title = normalizer.normalize(doc.title)

    def get_docs(self):
        return self.doc_store
