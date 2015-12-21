from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim

f = open('data.csv', 'r')
lines = f.readlines()
businessdict = {}
doc_set = []

for i in range(0, len(lines)):
	items = lines[i].split(',')
	if not items[1] in businessdict and len(businessdict) < 30000:
		businessdict[items[1]] = []
	if not items[1] in businessdict:
		continue
	businessdict[items[1]].append(len(doc_set))
	doc_set.append(items[2])

doc_set = []
lines = []

print "read file done"

texts = []

nf = open('parsedata', 'r')
lines = nf.readlines()
for i in range(0, len(lines)):
	texts.append(lines[i].split(','))
nf.close()

print "parse words 1 done"

# turn our tokenized documents into a id <-> term dictionary
dictionary = gensim.corpora.dictionary.Dictionary.load("dict")

print "parse words 2 done"

# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

print "parse words 3 done"

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel.load('ldamodel')

bus_topic = {}

# for business in businessdict:
# 	reviews = businessdict[business]
# 	for review in reviews:
# 		res = ldamodel.get_document_topics(corpus[review])
# 		result = max(res, key = lambda x : x[1])
# 		# print result
# 		if not business in bus_topic:
# 			bus_topic[business] = {}
# 		if not result[0] in bus_topic[business]:
# 			bus_topic[business][result[0]] = 0
# 		bus_topic[business][result[0]] += 1

# print "compute done"

# nf = open('bus_topic', 'w')
# for business in bus_topic:
# 	for topic in bus_topic[business]:
# 			nf.write(business + "," + str(topic) + "," +str(bus_topic[business][topic]) + "\n")
# nf.close()

count = 0
for business in businessdict:
	reviews = businessdict[business]
	for review in reviews:
		res = ldamodel.get_document_topics(corpus[review])
		result = max(res, key = lambda x : x[1])
		# print result
		words = ldamodel.show_topic(result[0], topn=30)
		count = 0
		for wordpair in words:
			word = wordpair[1]
			if count < 5 and len(word) > 3 and word in texts[review]:
				if not business in bus_topic:
					bus_topic[business] = {}
				if not word in bus_topic[business]:
					bus_topic[business][word] = 0
				bus_topic[business][word] += wordpair[0]
				count += 1
		count += 1

print "compute done"

nf = open('bus_category', 'w')
for business in bus_topic:
	newdict = sorted(bus_topic[business].iteritems(), key=lambda d : d[1], reverse = True)
	nf.write(business)
	for i in range(0, min(len(newdict), 5)):
		nf.write("," + newdict[i][0])
	nf.write("\n")
nf.close()


print "complete"



