class Tokenizer:

    def __init__(self):
        self.english_punctuations = {'.', ',', ':', ';', '!', '#', '@', '$', '%', '^', '&', '*', '(', ')', '"', "'",
                                     '?'}
        self.persian_punctuations = {'.', '،', ':', '؛', '!', '#', '@', '$', '^', '&', '*', '(', ')', '"', "'", '؟',
                                     '[', ']', '-', '/', '=', "«", "»", "٪", u'\u200c', '<', '>', '{', '}', '|', '[',
                                     ']', '\\', '/'}
        self.tokens = []

    def tokenize(self, text, only_persian=False):
        self.tokens = []
        tok = []
        for i in range(0, len(text)):
            if not self.__issplitter__(text[i], only_persian):
                tok.append(text[i])
            elif len(tok) > 0:
                self.tokens.append("".join(tok))
                tok.clear()
        if len(tok) > 0:
            self.tokens.append("".join(tok))

        return self.tokens

    def __issplitter__(self, char, only_persian=False):
        return char in self.persian_punctuations or char in self.english_punctuations or char.isspace() or (
                only_persian and char.isascii())
