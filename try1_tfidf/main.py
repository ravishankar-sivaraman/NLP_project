
from glob import glob
# import nltk
# nltk.download()
import math
from nltk.corpus import stopwords
import sys
import heapq
import os,errno
reload(sys)
sys.setdefaultencoding('utf8')
stop = stopwords.words('portuguese')
# print stop
folder_year = ['/PT2010-2011','/PT2012-2013']
folder_type = "/docs"
directory_main = "PriberamCompressiveSummarizationCorpus"
def makelist(dir):
	articles_list = []
	# for fold in (dir + s for s in arrayforfolds):
	for fold in (dir + f + "/docs" for f in folder_year):
		# fold = fold + "*.sents"
		paths = glob(fold+"/*/")
		for folder in paths:
			folder = folder + "*.sents"
			files = glob(folder)
			# print files
			for file in files:

				fp = open(file,'r')
				article = []
				article.append(fp.read())
				article.append(file)
				articles_list.append(article)
	
	
	return articles_list


articles_corpus = makelist(directory_main)
idf_map = {}
# print "one"
for article in articles_corpus:
	actual_article = article[0]
	lines = actual_article.split()
	for word in lines:
		if word not in stop:
			idf_map[word] = 0

#code to create the idf map
for key in idf_map:
	for article in articles_corpus:
		
		if key in article[0]:
			idf_map[key] += 1
for key in idf_map:
	idf_map[key] = math.log(801*1.0/(1+idf_map[key]))
# for all the articles

for article in articles_corpus:
	# output = {}

	lines = article[0].split()
	tf_map = {}
	for word in lines:
		if word not in stop:
			if word not in tf_map:
				tf_map[word] = 0
			else:
				tf_map[word] += 1
	for key in tf_map:
		tf_map[key] = tf_map[key] * 1.0 * idf_map[key]
	#for each sentence calculate the tf-idf score
	lines = article[0].split('\n')
	sentence_dict = {}
	for line in lines:
		words = line.split()
		tf_idf_sum = 0
		sentence_length = 0
		for word in words:
			if word in tf_map:
				sentence_length += 1
				tf_idf_sum += tf_map[word]
		if sentence_length == 0:
			sentence_dict[line] = tf_idf_sum
		else:
			sentence_dict[line] = tf_idf_sum * 1.0/(sentence_length)
	# print "****************"

	# print heapq.nlargest(3, sentence_dict, key=sentence_dict.get)
	# print article
	# print "****************"
	# output["summary"] = heapq.nlargest(3, sentence_dict, key=sentence_dict.get)
	# output["article"] = article[0]
	filename = "outputSummaries/"+article[1]+"_summary.txt"
	if not os.path.exists(os.path.dirname(filename)):
		try:
			os.makedirs(os.path.dirname(filename))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise
	output = heapq.nlargest(3, sentence_dict, key=sentence_dict.get)
	with open(filename, "w") as f:
		f.write(output[0]+"\n"+output[1]+"\n"+output[2])
	# f.close()


# for the test article

# print idf_map


		
