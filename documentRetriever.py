# Code modified from http://www.ardendertat.com/2012/01/11/implementing-search-engines/
# Our acknowledgements to Arden.

#!/usr/bin/env python

import sys
import re
import copy
import gzip
import cPickle as pickle
import math
import time
from stemming import Stemmer
from collections import defaultdict

stemmer = Stemmer()

class DocumentRetriever:

    def __init__(self):
        self.index = {}
        self.tf = {}
        self.idf = {}

    def ngramConversion(self, query):
        words = stemmer.tokenizeAndStemString(query)
        ngram = [ a+b for a,b in zip(words,words[1:]) ]
        return ngram


    def preprocessQuery(self, query):
        query = query.lower()
        query = re.sub(r'[^a-z0-9 ]',' ',query)
        query = stemmer.tokenizeAndStemString(query)
        # line = self.ngramConversion(line)
        return query


    def readTrieIndex(self):
		f = gzip.open(self.trieIndexFile, 'rb')
		self.trieIndex = pickle.load(f)


    def dotProduct(self, vec1, vec2):
        if len(vec1) != len(vec2):
            return 0
        return sum([ float(x) * float(y) for x,y in zip(vec1,vec2) ])


    def trieRankDocuments(self, terms, docs):
	threshold = -1
        documentVectors = defaultdict(lambda: [0]*len(terms))
        queryVector = [0]*len(terms)
        for termIndex, term in enumerate(terms):
            try:
                if self.trieIndex.key(term) != term:
                    continue
                matchTermTuple = self.trieIndex.value(term)
                self.tf[term] = matchTermTuple[1]
                self.idf[term] = (matchTermTuple[2])
                queryVector[termIndex] = matchTermTuple[2]

                for docIndex, (doc, postings) in enumerate(matchTermTuple[0]):
                    if doc in docs:
			documentVectors[doc][termIndex] = self.tf[term][docIndex]
            except:
                pass

    	docScores = [ [self.dotProduct(curDocVec, queryVector), doc] for doc, curDocVec in documentVectors.iteritems() ]
        docScores.sort(reverse=True)
        resultDocs=[x[1] for x in docScores][:threshold]

        print resultDocs


    def getRelevantDocuments(self, q):
        q = self.preprocessQuery(q)
        if len(q) == 0:
	        print ''
	        return

    	documentList = set()
        for term in q:
            try:
                if self.trieIndex.key(term) != term:
                    continue
                termPage, (postingList, tf, idf) = self.trieIndex.item(term)
                docs = [x[0] for x in postingList]
                # if len(documentList) == 0:
                #    documentList = set(docs)
                documentList = documentList | set(docs)
            except:
	    	pass

        documentList = list(documentList)
        self.trieRankDocuments(q, documentList)


    def getParams(self):
        param = sys.argv
        self.trieIndexFile = param[1]


    def setupDocumentRetriever(self):
        self.getParams()
        self.readTrieIndex()
        while True:
            q = sys.stdin.readline()
   	    self.getRelevantDocuments(q)


    def parseMultiLine(self, dataset):
        # Parsing the dataset
        text = ""
        line = dataset.readline()
        while line != "" and line[0] != ".":
            text = text + line.strip()
            if text[-1] == "\n":
                text = text[:-1]

            text = text + " "
            line = dataset.readline()
        return text.rstrip(),line

    def evaluateOnQuerySet(self, queryFile, outputFile):
        self.getParams()
        self.readTrieIndex()

        document = {}
        dataset = open(queryFile)
        output = open(outputFile,'w')
        line = dataset.readline()
        while (line != ""):
            if line[:2] == ".I":
                segments = line.split()
                line = dataset.readline()

            elif line[:2] == ".W":
                document[segments[1]],line = self.parseMultiLine(dataset)

            else:
                line = dataset.readline()

        for id, q in document.iteritems():
            # DEBUG (to compute MAP)
            if q != '':
                start = int(round(time.time() * 1000))
                self.getRelevantDocuments(q)
                stop = int(round(time.time() * 1000))
                print id, stop-start


if __name__=='__main__':
    q = DocumentRetriever()
    # q.setupDocumentRetriever()
    # DEBUG
    q.evaluateOnQuerySet("query.text", "results.text")
