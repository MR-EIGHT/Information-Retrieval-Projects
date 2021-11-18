import glob
import os
from collections import defaultdict, OrderedDict

'''
Usage Guide:
There are two ways to use this project:
1-	Comment the “inp()” function, and run these functions: 
Print(search(term))
Print(AND(term1,term2))
Print(OR(term1,term2))
2-	Use the “inp()” function and run the project it will ask user the query to search. The query has to be in the following format:
alice 
alice AND sherlock
alice AND sherlock OR hello
NOT alice AND hello
Alice AND hello AND sherlock AND…
Note that operands like “AND, OR, NOT” have to be in uppercase and the desired terms  have to be in lowercase.
Please read the report for further information.
'''


# making the index first time the user runs the script.
def make_index():
    special_characters = ['!', '"', '#', '$', '%', '&', '(', ')', '*', '+', '/', ':', ';', '<', '=', '>', '@', '[',
                          '\\',
                          ']', '^', '`', '{', '|', '}', '~', '\t', '.', ',']

    folder_path = './txt'
    dic = defaultdict(set)
    books = set()

    # reading files and tokenizing them.
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

    # storing the built indexes.

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


# reading the stored indexes when the user runs the script for >= second time :)
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


# getting the desired posting-list by its index is postingList.txt file
def get_posting_list(term):
    index = terms.get(term)
    if index is None:
        return set()
        # print("Sorry! No result was found for this query.")
        # exit(0)
    with open("./persistent/postingList.txt") as fp:
        for z, line in enumerate(fp):
            if z == index:
                return eval(line)
    fp.close()
    return dict()


# search function
def search(term):
    return get_posting_list(term)


# AND-ing two terms function
def AND(term1, term2):
    pos1 = get_posting_list(term1)
    pos2 = get_posting_list(term2)
    return set(pos1) & set(pos2)


# OR-ing two terms function
def OR(term1, term2):
    pos1 = get_posting_list(term1)
    pos2 = get_posting_list(term2)
    return set(pos1) | set(pos2)


# NOT-ing a term function -> returns list of books that the provided term is not in them.
def NOT(term):
    pos = get_posting_list(term)
    return set(books) - set(pos)


# checks if the program is ready to read its sources or has to build them before
if not os.path.isdir("./persistent") or not os.path.isfile("./persistent/postingList.txt"):
    try:
        os.makedirs("./persistent/")
    except FileExistsError:
        print(FileExistsError)
    make_index()

terms, books = read_index()


# for more complex queries...
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
            print(result)


inp()
