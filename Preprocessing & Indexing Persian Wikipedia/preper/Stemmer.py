class Stemmer:

    def __init__(self):
        self.ends = ['ات', 'گان', 'ان', 'ترین', 'تر', 'م', 'ت', 'ش', 'یی', 'ی', 'ها', 'ٔ', '‌ا', '‌', 'ۀ']
        self.verb_ends = ['ام', 'ای', 'ایم', 'اید', 'اند']

    def stem(self, word):
        if len(word) < 4:
            return word.strip()
        for end in self.verb_ends + self.ends:
            if word.endswith(end):
                word = word[:-len(end)]

        return word.strip()

    def list_stem(self, word_set):
        for i in range(0, len(word_set)):
            if len(word_set[i]) < 4:
                word_set[i] = word_set[i].strip()
            for end in self.ends:
                if word_set[i].endswith(end):
                    word_set[i] = word_set[i][:-len(end)]
            return word_set
