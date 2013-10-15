# Achal Shah and Praful Johari

import xml.etree.cElementTree as ET
from xml.dom import minidom

def prettyPrintXML(elem):
    # Return a pretty-printed XML string for the Element.
    generatedXML = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(generatedXML)
    return reparsed.toprettyxml(indent="  ")

def addDocument(batchRoot, documentID, documentData):
    document = ET.SubElement(batchRoot, "document")
    # document.set("id", documentID)
    idElement = ET.SubElement(document, "id");
    idElement.text = documentID;
    for tag, value in documentData.iteritems():
        # print tag, value
        tagElement = ET.SubElement(document, tag)
        tagElement.text = value

def parseMultiLine(dataset):
    # Parsing the dataset
    # print "Started Multiline Parse"
    text = ""
    line = dataset.readline()
    while line != "" and line[0] != ".":
        text = text + line.strip()
        if text[-1] == "\n":
            text = text[:-1]

        text = text + " "
        line = dataset.readline()
    return text.rstrip(),line

def parseDataset(filename, batchRoot):
    dataset = open(filename)

    # Begin document parse
    document = {}
    line = dataset.readline()
    ident = -1
    while (line != ""):
        if line[:2] == ".I":
            if document.has_key('title'):
                addDocument(batchRoot, ident, document)
            document = {}
            segments = line.split()
            ident = segments[1]

            line = dataset.readline()

        elif line[:2] == ".T":
            document['title'],line = parseMultiLine(dataset)

        elif line[:2] == ".B":
            document['details'],line = parseMultiLine(dataset)

        elif line[:2] == ".W":
            document['abstract'],line = parseMultiLine(dataset)

        elif line[:2] == ".A":
            author_list = []
            line = dataset.readline()
            while line != "" and line[0] != ".":
                author_list.append(line[:-1])
                line = dataset.readline()

            document['authors'] = str(author_list)[1:-1]

        else:
            line = dataset.readline()

    addDocument(batchRoot, ident, document)

# Generating XML
dataFileObject = open("dataset.xml", "w")

root = ET.Element("root")

parseDataset("cacm.all", root)

# tree = ET.ElementTree(root)
# tree.write("filename.xml")

tree = prettyPrintXML(root)
dataFileObject.write(tree)
dataFileObject.close()
