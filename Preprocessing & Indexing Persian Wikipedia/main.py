import os

from preper import Stemmer
from preper import Normalizer
from preper import Tokenizer
from preper import Wikipedia
import InvertedIndex

"""
preper is a persian text preprocessor package I've made.
This section is the basic tests of this package:
"""
stemmer = Stemmer()
print(stemmer.stem("گفتۀ"))
print(stemmer.stem("نویسنده هایش"))
print(stemmer.stem("نویسندگان"))
print(stemmer.stem("ستودگان"))
print(stemmer.stem("رفته ایم"))
print(stemmer.stem("حیوانات"))
print(stemmer.stem("جواهرات"))


normalizer = Normalizer()
print(normalizer.normalize("123 علیﻚ سلام"))
print(normalizer.normalize("كي به کی"))

tokenizer = Tokenizer()
print(tokenizer.tokenize(
    "علی و حسن، به مدرسه رفتند. و در راه بازگشت به خانه دوستانِ قدیمی شان را دیدند. آیا آنها خوشحال شدند؟ یا خیر؟! "
    "می‌خواهم بدانم."))

"""
This is the second part of the project. In which we had to index documents in the 'simple.xml' file.
"""
if not os.path.isdir("persistent") or not os.path.isfile("persistent/postingList.txt"):
    wiki = Wikipedia("./data/simple.xml")
    inv = InvertedIndex.InvertedIndex(wiki.doc_store)
else:
    inv = InvertedIndex.InvertedIndex([])
inv.inp()
print()
