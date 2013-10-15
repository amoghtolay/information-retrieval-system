def parseQrels(filename):
    qrels = open(filename)

    results = {}
    line = qrels.readline()
    while (line != ""):
        wordList = line.split(' ')
        if (str(int(wordList[0])) in results.keys()):
            results[str(int(wordList[0]))].append(wordList[1])
        else:
            results[str(int(wordList[0]))] = [ wordList[1] ]
        line = qrels.readline()
    return results

def parseResults(resultFilename):
    results = open(resultFilename)
    testResults = {}
    line = results.readline()

    while (line != ""):
        id = line.strip()
        line = results.readline()
        testResults[str(int(id))] = line.strip('[]\n').split(', ')
        line = results.readline()
    return testResults


def computeMap(qrels, testResults):
    totalPrecision = 0
    totalResults = 0
    for id, qrelsList in qrels.iteritems():
        truePos = 0
        tempList = testResults[id]

        if (tempList != ['']):
            for testResult in tempList:
                if testResult in qrelsList:
                    truePos += 1
            curPrecision = (float(truePos) / float(len(tempList)))
            print "ID: ", id, "Precision: ", curPrecision
            totalPrecision += curPrecision
            totalResults += 1
        else:
            print "ID: ", id, "No Precision."

    meanAvgPrecision = float(totalPrecision) / float(totalResults)

    return meanAvgPrecision

qrels = parseQrels("qrels.text")
testResults = parseResults("resultsTrie.text")
# print "Qrels: ", qrels
# print "Results: ", testResults

meanAvgPrecision = computeMap(qrels, testResults)
print "Mean Average Precision: ", meanAvgPrecision

