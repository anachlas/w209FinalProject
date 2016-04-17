#!/usr/bin/python
import json
import fileinput
from collections import Counter
import base64
import operator
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

max_entity_name_len = 30

entity_counts = Counter()
entity_type_counts = {}
articles = {}
entities_to_articles = {}
entities_to_articles_meta = {}

def ename_to_html_filename(ename):
    return "".join([c for c in ename if c.isalpha() or c.isdigit() or c==' ']).rstrip() + ".html"

for line in fileinput.input():
    data = json.loads(line)
    articles[data['url']] = data
    article_entities = data['entities']
    for ae in article_entities:
        ae_name = ae['entity']
        ae_type = ae['type']
        if len(ae_name) > max_entity_name_len:
            break
        #print ae_name
        entity_counts[ae_name] += 1
        if ae_name not in entity_type_counts:
            entity_type_counts[ae_name] = Counter()
        entity_type_counts[ae_name][ae_type] += 1
        if ae_name not in entities_to_articles:
            entities_to_articles[ae_name] = []
            entities_to_articles_meta[ae_name] = []
        entities_to_articles[ae_name].append(data['url'])
        entities_to_articles_meta[ae_name].append({"url":data['url'],"title":data['title']})
        #print "url", data['url']

graph = {}
graph['nodes'] = []
graph['links'] = []

for entity in entity_counts.keys():
    if entity_counts[entity] > 10:
        entity_type = max(entity_type_counts[entity].iteritems(),
            key=operator.itemgetter(1))[0]
        group = ""
        if entity_type == "ORGANIZATION":
            group = "1"
        elif entity_type == "PERSON":
            group = "3"
        elif entity_type == "LOCATION":
            group = "2"
        url = ename_to_html_filename(entity)
        size = entity_counts[entity]
        if group != "":
            graph['nodes'].append({"name":entity, "group":group, "url":url, "size":size})

for i, ival in enumerate(graph['nodes']):
    i_articles = entities_to_articles[ival["name"]]
    for j, jval in enumerate(graph['nodes']):
        j_articles = entities_to_articles[jval["name"]]
        article_intersection = list(set(i_articles) & set(j_articles))
        if len(article_intersection) > 0:
            graph['links'].append({"source":i,"target":j,"value":len(article_intersection)})

for entity_name in entities_to_articles.keys():
    filename = ename_to_html_filename(entity_name)
    html_out = open(filename,"w")
    html_out.write("<html>\n<h1>" + entity_name + "</h1><br>\n")
    linklines = []
    #print "writing html file", filename
    for article in entities_to_articles_meta[entity_name]:
        title = base64.b64decode(article['title'])
        url = article['url']
        linkline = "<a href='" + url + "'>" + title + "</a><br>\n"
        linklines.append(linkline)
    for linkline in set(linklines):
        html_out.write(linkline)

    html_out.write("<html>")



print json.dumps(graph)
