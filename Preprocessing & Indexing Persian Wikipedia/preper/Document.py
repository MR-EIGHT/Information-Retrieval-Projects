class Document:

    def __init__(self, name, body, docid):
        self.docId = docid
        self.title = name
        self.body = body

    def get_body(self):
        return self.body

    def get_doc_id(self):
        return self.docId

    def __repr__(self) -> str:
        return "Document( DocId = " + str(self.docId) + ", title = " + str(self.title) + ", )"
