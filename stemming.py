# Amogh Tolay
# Code to tokenize and stem a string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

class Stemmer:
    def tokenizeAndStemString(self, originalString):
        # Tokenize the string (using regex or static splitting)
        # and make the wordList containing the words

        wordList = wordpunct_tokenize(originalString);
        # Filter the words and remove stop words.
        filteredWords = [w for w in wordList if not w in stopwords.words('english')]
        # print filteredWords

        # Now stem the words using porter/snowball/lancester/corpus (lemmatizer) stemmer
        # wordNetLemmatizer = WordNetLemmatizer()
        # wnlStems = [wordNetLemmatizer.lemmatize(w) for w in filteredWords]
        # print "Stemmed based on WordNetLemmatizer:"
        # print wnlStems

        # print ""
        # print "Stemmed based on Porter Algorithm:"
        porterStemmer = PorterStemmer()
        porterStems = [porterStemmer.stem(w) for w in filteredWords]
        # print porterStems
        return porterStems


stem = Stemmer()
testString = "This is a sample string that I've written to test the tokenizer. I sincerely hope that this works."
stemmedList = stem.tokenizeAndStemString(testString)
# print stemmedList
