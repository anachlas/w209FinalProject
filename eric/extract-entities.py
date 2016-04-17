#!/usr/bin/python
import json
import re
import fileinput
import base64
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# Next 4 lines are for MITIE
# https://github.com/mit-nlp/MITIE
from mitie import *

print "loading NER model..."
ner = named_entity_extractor('data/MITIE-models/english/ner_model.dat')
print "\nTags output by this NER model:", ner.get_possible_ner_tags()

def extract_entities(text):
    tokens = tokenize(text)
    mitie_entities = ner.extract_entities(tokens)
    entities = []
    for e in mitie_entities:
        token_range = e[0]
        tag = e[1]
        entity_text = " ".join(tokens[i] for i in token_range)
        entity_record = {u'entity': entity_text, u'type': tag}
        entities.append(entity_record)
    return entities

infilename = ""
for line in fileinput.input():
    if infilename == "":
        infilename = fileinput.filename()
        if infilename == "<stdin>":
            print "ERROR: Can't read from stdin, need filename as argument"
            sys.exit(1)
        outfilename = re.sub('split.withText','entities',
            infilename)
        print "Writing to:", outfilename
        outfile = open(outfilename, "w")
    try:
        data = json.loads(line)
        title = base64.b64decode(data["title"])
        url = data["url"]
        text = base64.b64decode(data["text"])
        entities = extract_entities(text)
        data["entities"] = entities
        outfile.write(json.dumps(data) + '\n')
    except ValueError:
        pass
