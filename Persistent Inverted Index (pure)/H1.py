import glob
import os
from collections import defaultdict, OrderedDict


def make_index():
    special_characters = ['!', '"', '#', '$', '%', '&', '(', ')', '*', '+', '/', ':', ';', '<', '=', '>', '@', '[',
                          '\\',
                          ']', '^', '`', '{', '|', '}', '~', '\t', '.', ',']

    folder_path = './txt'
    dic = defaultdict(set)
    books = set()

    for filename in glob.glob(os.path.join(folder_path, '*.txt')):
        with open(filename, 'r', encoding="utf8") as f:
            text = f.read()
            for i in special_characters:
                text = text.replace(i, '')
            text = text.lower()

            for x in text.split():
                dic[x].add(str(filename).replace("./txt\\", ""))
        books.add(str(filename).replace("./txt\\", ""))
        f.close()

    file0 = open("./persistent/books.txt", "w", encoding='utf8')
    file0.write(str(books))
    file0.close()

    ord_terms = OrderedDict()

    i = 0
    file1 = open("./persistent/postingList.txt", "w")
    for x in dic.keys():
        ord_terms[x] = i
        i += 1
        file1.write(str(dic.get(x)) + '\n')
    file1.close()

    file2 = open("./persistent/terms.txt", "w", encoding='utf8')
    file2.write(str(ord_terms) + '\n')
    file2.close()


def read_index():
    file3 = open("./persistent/terms.txt", "r", encoding='utf8')
    text = file3.read()
    terms_dictionary = eval(str(text))
    file3.close()

    file4 = open("./persistent/books.txt", "r", encoding='utf8')
    text = file4.read()
    books_dictionary = eval(str(text))
    file4.close()

    return terms_dictionary, books_dictionary


def get_posting_list(term):
    index = terms.get(term)
    if index is None:
        print("Sorry! No result was found for this query.")
        exit(0)
    with open("./persistent/postingList.txt") as fp:
        for z, line in enumerate(fp):
            if z == index:
                return eval(line)
    fp.close()
    return dict()


def search(term):
    return get_posting_list(term)


def AND(term1, term2):
    pos1 = get_posting_list(term1)
    pos2 = get_posting_list(term2)
    return set(pos1) & set(pos2)


def OR(term1, term2):
    pos1 = get_posting_list(term1)
    pos2 = get_posting_list(term2)
    return set(pos1) | set(pos2)


def NOT(term):
    pos = get_posting_list(term)
    return set(books) - set(pos)


if not os.path.isdir("./persistent") or not os.path.isfile("./persistent/postingList.txt"):
    try:
        os.makedirs("./persistent/")
    except FileExistsError:
        print(FileExistsError)
    make_index()

terms, books = read_index()


def inp():
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
                query_set[q] = NOT(query_set[q + 1])
                del query_set[q + 1]
                length -= 1
            q += 1

        length = len(query_set)
        q = 0
        while q < length:
            que = query_set[q]
            if que not in special_words and type(que) != set:
                query_set[q] = search(que)
            q += 1

        # if len([i for i in query_set if type(i) == dict]) > 0:
        #     print("Sorry! No result was found for this query.")
        #     return

        length = len(query_set)
        q = 0
        while q < length:
            que = query_set[q]
            if que == "AND":
                query_set[q + 1] = query_set[q - 1] & query_set[q + 1]
                del query_set[q]
                del query_set[q - 1]
                length -= 2
            if que == "OR":
                query_set[q + 1] = query_set[q - 1] | query_set[q + 1]
                del query_set[q]
                del query_set[q - 1]
                length -= 2
            q += 1

        result = query_set[0]

        if result.__len__() == 0:
            print("Sorry! No result was found for this query.")
        else:
            print(result)


# 


inp()
