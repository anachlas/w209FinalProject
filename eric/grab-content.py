#!/usr/bin/python
import json
import fileinput
import base64
import re
from goose import Goose
import sys
reload(sys)
sys.setdefaultencoding('utf8')

g = Goose()
infilename = ""
for line in fileinput.input():
    if infilename == "":
        infilename = fileinput.filename()
        if infilename == "<stdin>":
            print "ERROR: Can't read from stdin, need filename as argument"
            sys.exit(1)
        outfilename = re.sub('split','split.withText', infilename)
        outfile = open(outfilename, "w")
    data = json.loads(line)
    article = g.extract(url=data["url"])
    title = base64.b64encode(article.title)
    text = base64.b64encode(article.cleaned_text)
    data['title'] = title
    data['text'] = text
    outfile.write(json.dumps(data) + '\n')
