# Amogh Tolay
# Testing jig to see if synonyms and polynyms can improve a query
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.stem.porter import PorterStemmer
import re
from textProcessing import Stemmer
stemmer = Stemmer()

def preprocessQuery(query):
    query = query.lower()
    query = re.sub(r'[^a-z0-9 ]',' ',query)
    wordListAll = wordpunct_tokenize(query);
    # Now combine wordList with operators also
    # So, wordList now contains (word, Operator) before we do stop word removal
    wordList = []
    i = 0
    while i < len(wordListAll):
        if wordListAll[i] == "AND" or wordListAll[i] == "and":
            wordList.append( (wordListAll[i+1], "AND") )
            i += 2
        elif wordListAll[i] == "OR" or wordListAll[i] == "or":
            wordList.append( (wordListAll[i+1], "OR") )
            i += 2
        else:
            wordList.append( (wordListAll[i], "OR") )
            i += 1

    # Filter the words and remove stop words.
    filteredWords = [w for w in wordList if not w[0] in stopwords.words('english')]

    queryTuples = []
    queryLen = len(filteredWords)
    if queryLen > 15:
        queryTuples = filteredWords
    else:
        for word, operator in filteredWords:
            synonymList = getSynonymList(word)
            queryTuples.append((word, operator))
            for synCount, syn in enumerate(synonymList):
                if synCount > 3:
                    break
                # Adding operator OR in synonyms list if its not a stop word
                syn = re.sub(r'[^a-z0-9 ]', ' ', syn)
                synList = syn.split()
                for synOneTerm in synList:
                    if not synOneTerm in stopwords.words('english'):
                        queryTuples.append((synOneTerm, "OR"))


    # queryTuples list is ready (filtered). Now need to stem this list,
    # ensuring no duplicacy, same order and operator values
    finalQueryList = []
    porterStemmer = PorterStemmer()
    for word, operator in queryTuples:
        finalQueryList.append( (porterStemmer.stem(word), operator) )

    # Now removing duplicate items from list
    seenSet = set()
    uniqueList = []
    for q in finalQueryList:
        stemWord = q[0]
        if stemWord in seenSet:
            continue
        uniqueList.append(q)
        seenSet.add(q[0])

    return uniqueList

def getSynonymList(word):
    synSets = wn.synsets(word)
    # lemmaSetNames = list ( set( [s.lemmas[0].name for s in syns] ) )
    synonymList = list(set([l.name for s in synSets for l in s.lemmas]))
    return synonymList

# Testing the query preprocessor module
print preprocessQuery("documents OR good AND boys clustering density-based clustering")
