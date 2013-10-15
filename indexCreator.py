# Code modified from http://www.ardendertat.com/2012/01/11/implementing-search-engines/
# Our acknowledgements to Arden.

#!/usr/bin/env python

import sys
import re
import cPickle as pickle
import gzip
from collections import defaultdict
from array import array
import math
from stemming import Stemmer
from patricia import trie

stemmer = Stemmer()

class IndexBuilder:

    def __init__(self):
        self.index=defaultdict(list)    #the inverted index
        self.tf=defaultdict(list)       #term frequencies of terms in documents
                                        #documents in the same order as in the main index
        self.df=defaultdict(int)        #document frequencies of terms in the corpus
        self.docCount=0

    def parseArgs(self):
        param=sys.argv
        self.datasetFile=param[1]
        self.trieIndexFile=param[2]
        self.postingListFile=param[3]

    def ngramConversion(self, query):
        words = stemmer.tokenizeAndStemString(query)

        ngram = words
        ngram += [ a+b for a,b in zip(words,words[1:]) ]
        ngram += [ a+b+c for a,b,c in zip(words,words[1:],words[2:]) ]
        return ngram

    def getTokens(self, line):
        line=line.lower()
        # replace weird chars by spaces
        line=re.sub(r'[^a-z0-9 ]',' ',line)
        line = stemmer.tokenizeAndStemString(line)
        # line = self.ngramConversion(line)
        return line


    def parseDataset(self):
        # Parsing the XML file to get relevant fields in the document
        doc=[]
        for line in self.dataset:
            if line.strip()=='</document>':
                break
            doc.append(line)

        curPage=''.join(doc)
        pageid=re.search('<id>(.*?)</id>', curPage, re.DOTALL)
        pagetitle=re.search('<title>(.*?)</title>', curPage, re.DOTALL)
        pageabstract=re.search('<abstract>(.*?)</abstract>', curPage, re.DOTALL)
        pageauthors=re.search('<authors>(.*?)</authors>', curPage, re.DOTALL)

        if pageid==None:
            return {}

        d={}
        d['id']=pageid.group(1)

        if pagetitle != None:
            d['title']=pagetitle.group(1)
        else:
            d['title']=''

        if pageabstract != None:
            d['abstract']=pageabstract.group(1)
        else:
            d['abstract']=''

        if pageauthors != None:
            d['authors']=pageauthors.group(1)
        else:
            d['authors']=''

        return d

    def writePostingListToFile(self):
        # Writes the posting list to file for evaluation
        # Gzip enables an improvement in the size requirement
        # f=open(self.postingListFile, 'w')
        f=gzip.GzipFile(self.postingListFile, 'w')

        # first line is the number of documents
        print >>f, self.docCount
        self.docCount=float(self.docCount)
        for term in self.index.iterkeys():
            postinglist=[]
            for p in self.index[term]:
                docID=p[0]
                positions=p[1]
                postinglist.append(':'.join([str(docID) ,','.join(map(str,positions))]))
            postingData=';'.join(postinglist)
            print >> f, '|'.join((term, postingData))
        f.close()


    def constructTrieIndex(self):
		self.trieIndex = trie('root')
		for termPage, postingList in self.index.iteritems():
			idfData = math.log(float(self.docCount)/float(self.df[termPage]), 10)
			self.trieIndex[termPage] = (postingList, self.tf[termPage], idfData)

    def saveTrieIndexToFile(self):
        pickleDumpProtocol = -1
        # dumpFile = open(self.trieIndexFile, "wb")
        dumpFile = gzip.GzipFile(self.trieIndexFile, "wb")
        print self.trieIndex
        pickle.dump(self.trieIndex, dumpFile, pickleDumpProtocol)
        dumpFile.close()

    def findNormalizationConst(self, termdictPage):
        normalizationConst=0
        for term, posting in termdictPage.iteritems():
            normalizationConst+=len(posting[1])**2
        normalizationConst=math.sqrt(normalizationConst)
    	return normalizationConst

    def buildIndex(self):
        self.parseArgs()
        self.dataset=open(self.datasetFile,'r')

        pagedict={}
        pagedict=self.parseDataset()
        while pagedict != {}:
            lines='\n'.join((pagedict['title'],pagedict['abstract'],pagedict['authors']))
            pageid=int(pagedict['id'])
            terms=self.getTokens(lines)

            self.docCount+=1

            # current page
            termdictPage={}
            for position, term in enumerate(terms):
                try:
                    termdictPage[term][1].append(position)
                except:
                    termdictPage[term]=[pageid, array('I',[position])]

            normalizationConst=self.findNormalizationConst(termdictPage)

            # Find TFs and DFs
            for term, posting in termdictPage.iteritems():
                self.tf[term].append('%.4f' % (len(posting[1])/normalizationConst))
                self.df[term]+=1

            # current page now being added to main index
            for termPage, postingPage in termdictPage.iteritems():
                self.index[termPage].append(postingPage)

            # Increments and reads and parses the next doc
            pagedict=self.parseDataset()

        self.constructTrieIndex()
        self.writePostingListToFile()
        self.saveTrieIndexToFile()


if __name__=="__main__":
    invertedIndex = IndexBuilder()
    invertedIndex.buildIndex()
