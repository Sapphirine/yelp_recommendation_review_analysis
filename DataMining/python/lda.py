from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

# f = open('data.csv', 'r')
# lines = f.readlines()
# businessdict = {}
# doc_set = []

# for i in range(0, len(lines)):
# 	items = lines[i].split(',')
# 	if not items[1] in businessdict and len(businessdict) < 30000:
# 		businessdict[items[1]] = []
# 	if not items[1] in businessdict:
# 		continue
# 	businessdict[items[1]].append(len(doc_set))
# 	doc_set.append(items[2])

# print "read file done"
# print len(doc_set)

texts = []
# loop through document list

# nf = open('parsedata', 'w')
# for i in doc_set:
#     # clean and tokenize document string
#     tokens = tokenizer.tokenize(i)
#     # stem tokens
#     stemmed_tokens = [p_stemmer.stem(i) for i in tokens]
#     # add tokens to list
#     #texts.append(stemmed_tokens)

# nf.close()

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
texts = None
print "parse words 3 done"

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=30, id2word = dictionary, passes=20)

print "learn model done"

ldamodel.save('ldamodel')

print ldamodel.show_topics()


