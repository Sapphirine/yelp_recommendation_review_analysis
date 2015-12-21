from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from MinerDemo.models import Business
from MinerDemo.models import Review
from MinerDemo.models import LDADict
from MinerDemo.models import Categories
from django.shortcuts import render_to_response
import os
import json
import sys
import traceback

from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim

# Create your views here.

ldamodel = gensim.models.ldamodel.LdaModel.load(
	os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resource/files/ldamodel')
	)
dictionary = gensim.corpora.dictionary.Dictionary.load(
	os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resource/files/dict')
	)
tokenizer = RegexpTokenizer('[a-z]\w+')
en_stop = get_stop_words('en')
p_stemmer = PorterStemmer()

print "Done"

def parseWord(word):
	res = []
	raw = word.lower()
	tokens = tokenizer.tokenize(raw)
	stopped_tokens = [i for i in tokens if not i in en_stop]
	stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
	for string in stemmed_tokens:
		if len(string) > 2:
			res.append(string)
	return res

def computeTopicId(words, single):
	res = ldamodel.get_document_topics(dictionary.doc2bow(words))
	result = max(res, key = lambda x : x[1])
	maxtopic = result[0]
	keywords = []
	if single:
		return maxtopic
	topwords = ldamodel.show_topic(result[0], topn=100)
	count = 0
	for wordpair in topwords:
		word = wordpair[1]
		if count < 5 and len(word) > 2 and word in words:
			keywords.append(word)
	return maxtopic, keywords

#get top business with the review's topic and keyword's topic
def computeTopTopic(topicA, topicB):
	res = []
	businesses = Review.objects.filter(topic_id = topicA).order_by("score")
	if not topicB:
		for business in businesses:
			res.append(business.business_id)
			if len(res) > 10:
				break
		return res
	else:
		obusinesses = Review.objects.filter(topic_id = topicB)
		businessdict = {}
		for business in businesses:
			businessdict[business.business_id] = 1
		for business in obusinesses:
			if business.business_id in businessdict:
				res.append(business.business_id)
			if len(res) > 10:
				break
		return res

# def computeTopicCategory(topic, amount):
# 	res = []
# 	ldas = LDADict.objects.filter(topic_id = topic).order_by("score")[amount]
# 	for lda in ldas:
# 		res.append(lda.word)
# 	return res

def getBusinessDetail(business):
	detail = Business.objects.get(business_id = business)
	res = {
		"name" : detail.name,
		"address" : detail.address,
		"starts" : detail.starts,
		"review_count" : detail.review_count,
		"categories" : detail.categories
	}
	return res

def index(request):
	return render_to_response('resource/html/MinerDemo.html')

def searchReview(request):
	final = {
		"status" : "false"
	}
	try:
		review = request.GET.get('review', None)
		keyword = request.GET.get('keyword', None)
		if keyword == "None":
			keyword = None
		else:
			keyword = keyword.split(',')
		if review:
			topic, keywords = computeTopicId(parseWord(review), False)
			astopic = None
			if keyword and len(keyword) > 0:
				astopic = computeTopicId(keyword, True)
			businessIds = computeTopTopic(topic, astopic)
			if len(keywords) > 0 and len(businessIds) > 0:
				final = {
					"keywords" : ", ".join(keywords),
					"businesses" : [getBusinessDetail(business) for business in businessIds],
					"status" : "true"
				}
	except Exception as e:
		print e
	return HttpResponse(json.dumps(final))

# def saveBusiness(request):
# 	path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resource/files/yelp_academic_dataset_business.json')
# 	file = open(path, 'r')
# 	count = 0
# 	for line in file.readlines():
# 		line =line.strip('\n')
# 		business = json.loads(line)
# 		newbus = Business(business_id = business['business_id'],
# 					name = business['name'], 
# 					address = business['full_address'], 
# 					starts = business['stars'], 
# 					review_count = business['review_count'],
# 					categories = ",".join(business['categories']))
# 		newbus.save()
# 		print count
# 		count += 1
# 	return HttpResponse("complete")

# def saveRelation(request):
# 	path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resource/files/bus_topic')
# 	file = open(path, 'r')
# 	for line in file.readlines():
# 		line =line.strip('\n')
# 		items = line.split(',')
# 		if int(items[2]) < 2:
# 			continue
# 		newrel = Review(review_id = "0", 
# 					business_id = items[0], 
# 					topic_id = items[1], 
# 					score = int(items[2])
# 					)
# 		newrel.save()
# 	return HttpResponse("complete")

# def saveCategories(request):
# 	file = open('bus_category', 'r')
# 	for line in file.readlines():
# 		line =line.strip('\n')
# 		items = line.split(',')
# 		if len(items) <= 1:
# 			continue
# 		id = items[0]
# 		cates = ",".join(items[1:])
# 		newcat = Categories(business_id = id, categories = cates)
# 		newcat.save()
# 	return HttpResponse("complete")

