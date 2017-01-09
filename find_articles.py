#!/usr/bin/python

import sys, json
import os
import re
from stemming.porter2 import stem


class tfidf:
  def __init__(self):
    self.weighted = False
    self.documents = []
    self.corpus_dict = {}

  def addDocument(self, doc_name):
    with open('tf/' + doc_name.split('.')[0] + '.json', 'r') as data_file:    
        length, doc_dict = json.load(data_file)

    for w in doc_dict.keys():
        self.corpus_dict[w] = self.corpus_dict.get(w, 0.0) + doc_dict[w]

    for k in doc_dict:
      doc_dict[k] = doc_dict[k] / length

    self.documents.append([doc_name, doc_dict])

  def similarities(self, list_of_words):
    query_dict = {}
    for w in list_of_words:
      query_dict[w] = query_dict.get(w, 0.0) + 1.0

    length = float(len(list_of_words))
    for k in query_dict:
      query_dict[k] = query_dict[k] / length

    sims = []
    for doc in self.documents:
      score = 0.0
      doc_dict = doc[1]
      for k in query_dict:
        if k in doc_dict:
          score += (query_dict[k] / self.corpus_dict[k]) + (doc_dict[k] / self.corpus_dict[k])
      sims.append([doc[0], score])

    return sims



search_tfidf = tfidf()
content = sys.argv[1]
set_of_docs = {}

words = [stem(word) for word in content.split(' ')]
sim_words = words[:]
no_more_words = False
for file in os.listdir("index"):
    if no_more_words:
        break
    with open("index/" + file, 'r') as index_file:
        for line in index_file:
            word, docs = line.split('\t')
            docs = [doc for doc in docs.split(',')]
            if word in words:
                if not set_of_docs:
                    set_of_docs = set(docs)
                else:
                    set_of_docs.intersection_update(set(docs))
                words.remove(word)

                if not words:
                    no_more_words = True
                    break


for doc in set_of_docs:
    search_tfidf.addDocument(doc)
scored_articles = search_tfidf.similarities(sim_words)
sorted_articles = sorted(scored_articles, key=lambda a: -a[1])
for article in sorted_articles:
    print article