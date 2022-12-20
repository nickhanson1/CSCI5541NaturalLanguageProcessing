import sys
import nltk
import re
import math
import numpy as np
import copy

import itertools


from nltk.corpus import brown


def hmm_model_build():
	nltk.download('brown')
	corpus = brown.tagged_sents()
	
	tags = []
	for w in corpus:
		for t in w:
			if t[1] not in tags:
				tags.append(t[1])

	tags.append("<S>")

	data = open("model.dat", "w")
	data.write(str(tags))
	data.write("\n")

	tag_pairs = [(t1,t2) for t1 in tags for t2 in tags]

	C = dict.fromkeys(tags, 0)

	count = 0
	for w in corpus:
		for t in w:
			C[t[1]] += 1
			count += 1

	for w in corpus:
		for t in tags:
			C[t] /= count

	data.write(str(C))
	data.write("\n")

	A = dict.fromkeys(tag_pairs, 0)

	for line in corpus:
		A[("<S>", line[0][1])] += 1
		for i in range(len(line) - 1):
			first_tag = line[i][1]
			next_tag = line[i+1][1]
			tag_list = (first_tag, next_tag)
			A[tag_list] += 1


	for tag1 in tags:
		count = 0
		for tag2 in tags:
			if (tag1,tag2) in A.keys():
				count += A[(tag1, tag2)]
		if count == 0:
			continue
		for tag2 in tags:
			 A[(tag1,tag2)] /= count

	data.write(str(A))
	data.write("\n")

	B = dict.fromkeys(tags, None)
	
	for k in B.keys():
		B[k] = dict()

	for line in corpus:
		for word in line:
			tag = word[1]
			w = word[0].lower()
			if w not in B[tag].keys():
				B[tag][w] = 1
			else:
				B[tag][w] += 1

	for t in tags:
		count = 0
		for w in B[t].keys():
			count += B[t][w]
		for w in B[t].keys():
			B[t][w] /= count


	data.write(str(B))
	data.write("\n")

	data.close()

hmm_model_build()