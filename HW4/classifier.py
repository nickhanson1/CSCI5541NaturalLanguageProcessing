# CODE REPORT:
#
# The code is ran by the following
#      python3 classifier.py <authorlist> 
#      python3 classifier.py <authorlist> -test <testfile>
#
# Where <authorlist> is a test file containing the locations of the source files and 
#      <testfile> contains outside text to test the classifier on.
#
#
# This model runs on UTF-8 encoding.
# 
# To clean the text all apostrophes, quotation marks, and commas are removed. Further,
# 		all text is lowercase. Periods are kept to act as signallers to the models for
#       the end of a sentence. Contractions are kept but apostrophes are removed, for
#       example didn't is sent to didnt.
#
# This language model uses both trigrams and bigrams. Bigrams are the main tool used,
#       but trigrams and unigrams are used to calculate extra quantitis which sharpen
#       performance.
#
# I am using Good-Turing smoothing. The training method performs a first sweep of the 
#       tokens just counting uni-, bi-, and trigrams and calculating the naive 
#       probabilities. Another sweep is performed to count frequency of frequency for
#       each group of N-grams, and a discounted Turing-Good probability is then
#       calculated and assigned to each N-gram and a "missing mass" is found for
#       N-grams that do not occur in the training data.
#     
# I use Katz backoff during classification to improve results. In fact, the 
#       introduction of backoff improved results from near random to well over 50%. 
#       
# The output on the development set is as follows:
#      >Testing...
#      >authorship/tolstoy : 41 / 84
#      >authorship/dickens : 46 / 77
#      >authorship/austen : 60 / 90
#      >authorship/wilde : 46 / 78
#
#
import sys
import nltk
import re
import math

def clean(text):
	char_to_remove = ["\'","\"", ","]
	for c in char_to_remove:
		text.replace(c, '')
	return text.lower()

class NGramModel:
	def __init__(self, author_file_name, keep_dev_data, name):
		self.name = name
		# read file
		self.file_name = author_file_name
		file = open(author_file_name, "r")
		text = ""
		self.dev_text = ""
		
		#set aside several lines of text from the file if indicated. Otherwise store whole file		
		if keep_dev_data:
			dev_line_count = 100
			self.dev_text = ""
			for i in range(dev_line_count):
				line = file.readline()
				line = clean(line)
				if line == "\n":
					continue
				self.dev_text += line

			line = file.readline()
			line = clean(line)
			while line != "":
				text += line 
				text += "\n"
				line = file.readline()
				clean(line)

		if not keep_dev_data:
			text = file.read()
			text = clean(text)

		#tokenize
		self.training_set = nltk.word_tokenize(text)
		self.training_count = len(self.training_set)

		#create dictionaries for N-grams
		self.trigrams = dict()
		self.bigrams = dict()
		self.unigrams = dict()

		self.vocab = []

		print(name, "created.")




	def train(self):
		#unigrams first
		#info stored as (count, probability, discounted probability)
		for w in self.training_set:
			if w not in self.unigrams.keys():
				self.unigrams[w] = (1,(1.0 / self.training_count), 0)
			else:
				self.unigrams[w] = (self.unigrams[w][0] + 1, self.unigrams[w][1] + (1.0 / self.training_count), 0)

		#obtain vocab from unigrams
		vocab = self.unigrams.keys()
		self.vocab = vocab


		#bigrams
		#info also stored as (count, probability, discounted probability)
		for i in range(self.training_count - 1):
			w1 = self.training_set[i]
			w2 = self.training_set[i + 1]
			b = (w1,w2)
			if b not in self.bigrams.keys():
				self.bigrams[b] = (1,(1.0 / (self.training_count - 1)), 0)
			else:
				self.bigrams[b] = (self.bigrams[b][0] + 1, self.bigrams[b][1] + (1.0 / (self.training_count - 1)), 0)
		

		#trigrams
		#info also stored as (count, probability, discounted probability)
		for i in range(self.training_count - 2):
			w1 = self.training_set[i]
			w2 = self.training_set[i + 1]
			w3 = self.training_set[i + 2]
			b = (w1,w2, w3)
			if b not in self.trigrams.keys():
				self.trigrams[b] = (1,(1.0 / (self.training_count - 2)), 0)
			else:
				self.trigrams[b] = (self.trigrams[b][0] + 1, self.trigrams[b][1] + (1.0 / (self.training_count - 2)), 0)


		# calculate frequency of frequencies
		unigram_frequencies = dict()
		for w in self.unigrams.keys():
			c = self.unigrams[w][0]
			if c not in unigram_frequencies.keys():
				unigram_frequencies[c] = 1
			else:
				unigram_frequencies[c] = unigram_frequencies[c] + 1

		bigram_frequencies = dict()
		for w in self.bigrams.keys():
			c = self.bigrams[w][0]
			if c not in bigram_frequencies.keys():
				bigram_frequencies[c] = 1
			else:
				bigram_frequencies[c] = bigram_frequencies[c] + 1

		trigram_frequencies = dict()
		for w in self.trigrams.keys():
			c = self.trigrams[w][0]
			if c not in trigram_frequencies.keys():
				trigram_frequencies[c] = 1
			else:
				trigram_frequencies[c] = trigram_frequencies[c] + 1

		total = len(self.unigrams.keys())
		self.zero_prob_unigram = unigram_frequencies[1] / total 
		#calculate discounted count for N-grams
		for w in self.unigrams.keys():
			count = self.unigrams[w][0]
			discount = 0
			#total = len(self.unigrams.keys())
			if((count + 1) not in unigram_frequencies):
				discount = count
			else:
				discount = count * unigram_frequencies[count + 1] / unigram_frequencies[count]
			self.unigrams[w] = (self.unigrams[w][0], self.unigrams[w][1], discount / total)
		
		total = self.training_count - 1
		self.zero_prob_bigram = bigram_frequencies[1] / total

		for w in self.bigrams.keys():
			count = self.bigrams[w][0]
			discount = 0
			total = len(self.bigrams.keys())
			if((count + 1) not in bigram_frequencies):
				discount = count
			else:
				discount = count * bigram_frequencies[count + 1] / bigram_frequencies[count]
			self.bigrams[w] = (self.bigrams[w][0], self.bigrams[w][1], discount / total)

		total = self.training_count - 2
		self.zero_prob_trigram = trigram_frequencies[1] / total

		for w in self.trigrams.keys():
			count = self.trigrams[w][0]
			discount = 0
			total = len(self.bigrams.keys())
			if((count + 1) not in trigram_frequencies):
				discount = count
			else:
				discount = count * trigram_frequencies[count + 1] / trigram_frequencies[count]
			self.trigrams[w] = (self.trigrams[w][0], self.trigrams[w][1], discount / total)
		
		self.zero_prob_unigram /= len(vocab)
		self.zero_prob_bigram /= (len(vocab) ** 2 - len(self.bigrams.keys()))
		self.zero_prob_trigram /= (len(vocab) ** 3 - len(self.trigrams.keys()))


	#basic 2-gram model. Very bad! I do not use it
	def simple_2_gram(self, line):
		tokens = nltk.word_tokenize(line)
		log_prob = 0
		for i in range(len(tokens) - 1):
			w = (tokens[i], tokens[i+1])
			if(w not in self.bigrams.keys()):
				log_prob + math.log(self.zero_prob_bigram)
			else:
				log_prob = log_prob + math.log(self.bigrams[w][1], 10) 
		return log_prob

	#2-gram model using katz backoff. Very good! I use it
	def katz_2_gram(self, line):
		tokens = nltk.word_tokenize(line)
		log_prob = 0
		for i in range(len(tokens) - 1):
			w = (tokens[i], tokens[i+1])
			log_prob += math.log(self.katz_prob(w),10)
		return log_prob


	def get_filename(self):
		return self.file_name

	def get_test_data(self):
		return self.dev_text

	def get_name(self):
		return self.name

	def katz_prob(self,gram):
		if gram in self.bigrams.keys():
			return self.bigrams[gram][2]
		elif gram in self.unigrams.keys():
			return self.unigrams[gram][2]

		if len(gram) == 0:
			return self.zero_prob_unigram
		else:
			alpha = self.katz_alpha(gram)
			backoff = self.katz_prob(gram[1:])
			return alpha * backoff
		

	def katz_alpha(self, gram):
		if(len(gram) == 1):
			return self.zero_prob_unigram
		if(len(gram) == 2):
			beta = 0
			denom = 0
			for v in self.vocab:
				newgram1 = (gram[0],v)
				newgram2 = (gram[0], gram[1],v)

				if newgram2 in self.trigrams.keys():
					beta += self.trigrams[newgram2][1]
				if newgram1 in self.bigrams.keys():
					denom += self.bigrams[newgram1][1]
			beta = 1 - beta
			denom = 1 - denom
			return beta / denom





#Holds models to test them out on a line, choose largest log probability, and report the line under that models author
class Classifier:
	def __init__(self, file_list, do_testing):
		self.model_list = []
		print("Creating classifier!")
		for l in file_list:
			model = NGramModel(l, not do_testing, l[:-9])
			self.model_list.append(model)

	#Train all models
	def train(self):
		print("Beginning Training...")
		for m in self.model_list:
			print("Training classifier for", m.get_filename())
			m.train()


	def test_line(self, line):
		largest_prob = -10000
		classification = "NONE"
		#print(line)
		for m in self.model_list:
			log_prob = m.katz_2_gram(line)
			#print(m.get_name(), log_prob)
			if log_prob > largest_prob:
				classification = m.name
				largest_prob = log_prob
		return classification


	def test(self):
		print("Testing...")
		for m in self.model_list:
			total = 0
			correct = 0
			name = m.get_name()
			data = m.get_test_data()
			data_lines = data.split("\n")
			for line in data_lines:
				total = total + 1
				choice = self.test_line(line)
				if choice == m.get_name():
					correct = correct + 1

			print(m.get_name(), ":", correct, "/", total)



def main(args):
	#parse arguments
	author_list_file_name = args[1]
	test_file_name = ""
	do_testing = False
	if len(args) > 2:
		if args[2] == "-test":
			test_file_name = args[3]
			do_testing = True
		else:
			print("Unknown flag")
			return


	#get author file locations from author list
	author_list_file = open(author_list_file_name, "r")
	author_list = author_list_file.read()
	author_list = author_list.split("\n")
	author_list = [v for v in author_list if v != '']
	
	classifier = []

	nltk.download("punkt")

	if not do_testing:
		classifier = Classifier(author_list, do_testing)
		classifier.train()
		classifier.test()
	if do_testing:
		classifier = Classifier(author_list, not do_testing)
		test_file = open(test_file_name, "r")
		test_text = test_file.read()
		test_text = clean(test_text)
		test_text = test_text.split("\n")

		test_text = [l for l in test_text if (l != "" or l != "\n")]

		classifier.train()


		print("Testing on", test_file_name)
		for i in range(len(test_text)):
			line = test_text[i]
			print("Line",i,":",classifier.test_line(line))













main(sys.argv)