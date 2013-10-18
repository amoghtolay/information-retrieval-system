# Amogh Tolay
# Code to tokenize and stem a string
# or do some other NLTK procedures

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.stem.porter import PorterStemmer
import re

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

        porterStems = self.stemWordList(filteredWords)
        return porterStems

    def stemWordList(self, filteredWords):
        porterStemmer = PorterStemmer()
        if len(filteredWords) is 0:
            return []
        porterStems = [porterStemmer.stem(w) for w in filteredWords]
        return porterStems


class WordSenseTools:
    def getSynonymList(self, word):
        synSet = wn.synset(word + ".n.01").lemma_names
        return synSet

    def getPolynymList(self, word):
        return wn.synsets(word)


class SnippetExtractor:
    '''
    def getSnippetExptRegex(query, documentString):
        queryList = query.split()
        docWordList = documentString.split()

        This was supposed to be used as its regex matching,
        and should be much faster than iterating over each word
        of the document for each word of the query

        regexString = ""
        for word in queryList:
            regexString += '\\b' + re.escape(word) + '\\b|'
        regexString = regexString[:-1]
        p = re.compile(regexString, re.IGNORECASE)
        windowList = {}
        for m in p.finditer(docString):
            foundWord = m.group().lower()
            if foundWord not in windowList:
                windowList[m.group().lower()] = [m.start()]
            else:
                windowList[m.group().lower()].append(m.start()]
        '''

    def getSnippet(self, query, documentString):
        stemmer = Stemmer()
        queryList = stemmer.tokenizeAndStemString(query.lower())
        sentenceList = sent_tokenize(documentString)

        # Rank the sentences based on the query
        sentenceRanks = []
        for sentence in sentenceList:
            sentenceScore = 0
            if any(word in sentence.lower() for word in queryList):
                sentenceScore = 0
                for queryWord in queryList:
                    if queryWord in sentence.lower():
                        sentenceScore += 1
            sentenceRanks.append( (sentenceScore, sentence) )

        # Ranked sentences prepared
        sentenceRanks = sorted(sentenceRanks, key=lambda x: x[0], reverse = True)
        snippet = ""
        i = 0
        while len(snippet) < 150:
            snippet += ".." + sentenceRanks[i][1]
            i += 1
        snippet = snippet + ".."
        return snippet

    # TODO
    # Need to complete the HTML code of snippets
    def getSnippetHtml(snippetText, query):
        stemmer = Stemmer()
        queryList = stemmer.tokenizeAndStemString(query.lower())
        htmlText = ""


# Testing unit below:
def testSnippet():
    extractor = SnippetExtractor()
    query = "density based clustering support vector machine"
    docString = "Data categorization is challenging job in a current scenario. The growth rate of a multimedia data are increase day to day in an internet technology. For the better retrieval and efficient searching of a data, a process required for grouping the data. However, data mining can find out helpful implicit information in large databases. To detect the implicit useful information from large databases various data mining techniques are use. Data clustering is an important data mining technique for grouping data sets into different clusters and each cluster having same properties of data. In this paper we have taken image data sets and firstly applying the density based clustering to grouped the images, density based clustering grouped the images according to the nearest feature sets but not grouped outliers, then we used an important super hyperplane classifier support vector machine (SVM) which classify the all outlier left from density based clustering. This method improves the efficiency of image grouping and gives better results. Keywords: Classification, Clustering, DBSCAN, SVM"

    query1= "Google spell corrector"
    docString1 = '''In the past week, two friends (Dean and Bill) independently told me they were amazed at how Google does spelling correction so well and quickly. Type in a search like [speling] and Google comes back in 0.1 seconds or so with Did you mean: spelling. (Yahoo and Microsoft are similar.) What surprised me is that I thought Dean and Bill, being highly accomplished engineers and mathematicians, would have good intuitions about statistical language processing problems such as spelling
correction. But they didn't, and come to think of it, there's no reason they should: it was my expectations that were faulty, not their knowledge.
I figured they and many others could benefit from an explanation. The full details of an industrial-strength spell corrector are quite complex (you con read a little about it here or here). What I wanted to do here is to develop, in less than a page of code, a toy spelling corrector that achieves 80 or 90% accuracy at a processing speed of at least 10 words per second.So here, in 21 lines of Python 2.5 code, is the complete spelling corrector:
'''
    snippet = extractor.getSnippet(query1, docString1)
    print snippet

# Only for testing, remove after testing
# testSnippet()
