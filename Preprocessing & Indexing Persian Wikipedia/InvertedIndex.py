import glob
import os
from collections import defaultdict, OrderedDict
from preper import Tokenizer


class InvertedIndex:

    def __init__(self, doc_store):
        self.check_persistency(doc_store)
        self.terms, self.docs = self.read_index()

    # making the index first time the user runs the script.
    def make_index(self, doc_store):
        dic = defaultdict(set)
        docs = dict()
        tokenizer = Tokenizer()

        # reading files and tokenizing them.
        for doc in doc_store:
            for term in tokenizer.tokenize(doc.body, True):
                dic[term].add(doc.docId)
            docs[doc.docId] = doc.title

        # storing the built indexes.

        file0 = open("./persistent/docs.txt", "w", encoding='utf8')
        file0.write(str(docs))
        file0.close()

        ord_terms = OrderedDict()

        i = 0
        file1 = open("persistent/postingList.txt", "w", encoding='utf8')
        for x in dic.keys():
            ord_terms[x] = i
            i += 1
            file1.write(str(dic.get(x)) + '\n')
        file1.close()

        file2 = open("persistent/terms.txt", "w", encoding='utf8')
        file2.write(str(ord_terms) + '\n')
        file2.close()

    # reading the stored indexes when the user runs the script for >= second time :)
    def read_index(self):
        file3 = open("persistent/terms.txt", "r", encoding='utf8')
        text = file3.read()
        terms_dictionary = eval(str(text))
        file3.close()

        file4 = open("persistent/docs.txt", "r", encoding='utf8')
        text = file4.read()
        docs_dictionary = eval(str(text))
        file4.close()

        return terms_dictionary, docs_dictionary

    # getting the desired posting-list by its index is postingList.txt file
    def get_posting_list(self, term):
        index = self.terms.get(term)
        if index is None:
            return set()
            # print("Sorry! No result was found for this query.")
            # exit(0)
        with open("persistent/postingList.txt", encoding='utf-8') as fp:
            for z, line in enumerate(fp):
                if z == index:
                    return eval(line)
        fp.close()
        return dict()

    # search function
    def search(self, term):
        return self.get_posting_list(term)

    # AND-ing two terms function
    def AND(self, term1, term2):
        pos1 = self.get_posting_list(term1)
        pos2 = self.get_posting_list(term2)
        return set(pos1) & set(pos2)

    # OR-ing two terms function
    def OR(self, term1, term2):
        pos1 = self.get_posting_list(term1)
        pos2 = self.get_posting_list(term2)
        return set(pos1) | set(pos2)

    # NOT-ing a term function -> returns list of books that the provided term is not in them.
    def NOT(self, term):
        pos = self.get_posting_list(term)
        return set(self.docs.keys()) - set(pos)

    # checks if the program is ready to read its sources or has to build them before
    def check_persistency(self, doc_store):
        if not os.path.isdir("persistent") or not os.path.isfile("persistent/postingList.txt"):
            try:
                os.makedirs("persistent/")
            except FileExistsError:
                print(FileExistsError)
            self.make_index(doc_store)
        self.terms, self.docs = self.read_index()

    # for more complex queries...
    def inp(self):
        special_words = ["AND", "OR", "NOT"]

        while True:
            result = set()
            query_set = input("Search: ").split(" ")
            if query_set[0] == "QUIT":
                exit(0)
            length = len(query_set)
            q = 0
            while q < length:

                que = query_set[q]
                if que == "NOT":
                    query_set[q] = self.NOT(query_set[q + 1])
                    del query_set[q + 1]
                    length -= 1
                q += 1

            length = len(query_set)
            q = 0
            while q < length:
                que = query_set[q]
                if que not in special_words and type(que) != set:
                    query_set[q] = self.search(que)
                q += 1

            length = len(query_set)
            q = 0
            while q < length:
                que = query_set[q]
                if que == "AND":
                    query_set[q + 1] = query_set[q - 1] & query_set[q + 1]
                    del query_set[q]
                    del query_set[q - 1]
                    length -= 2
                    q -= 1
                if que == "OR":
                    query_set[q + 1] = query_set[q - 1] | query_set[q + 1]
                    del query_set[q]
                    del query_set[q - 1]
                    length -= 2
                    q -= 1
                q += 1

            result = query_set[0]

            if result.__len__() == 0:
                print("Sorry! No result was found for this query.")
            else:
                for res in result:
                    print("{} -".format(self.docs.get(res)), end="  ")
                print()
