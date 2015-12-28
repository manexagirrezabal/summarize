from nltk import corpus, tokenize


__all__ = ['LanguageProcessor']


class LanguageProcessor(object):
    def __init__(self, language):
        self.language = language
        self.stopwords = corpus.stopwords.words(language)

    def split_sentences(self, text):
        return tokenize.sent_tokenize(text, self.language)

    def extract_significant_words(self, sentence):
        return set(
            word for word in tokenize.word_tokenize(sentence)
            if word.isalnum() and word not in self.stopwords
        )
