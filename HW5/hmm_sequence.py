import sys
import nltk


def hmm_sequence(model, file):
	A, B, C, tags = decode_model(model)
	sentence_file = open(file, "r")
	sentence = sentence_file.read()

	tagged_words = sentence.split(" ")

	words = []
	for w in tagged_words:
		word_and_tag = w.split("_")
		words.append((word_and_tag[0], word_and_tag[1]))

	probability = 1

	for i in range(len(words)):
		w = words[i][0].lower()
		tag = words[i][1]
		prev_tag = words[i-1][1] if i != 0 else "<S>"

		if w not in B[tag].keys():
			probability *= 0
			break

		probability *= B[tag][w]
		probability *= A[(prev_tag, tag)]

	print("The probability of the sentence occuring is (ignoring the denominator) is:")
	print(probability)



def decode_model(model):
	data = open(model, "r")

	lines = data.readlines()

	tags_str = lines[0]
	Cstr = lines[1]
	Astr = lines[2]
	Bstr = lines[3]

	tags = eval(tags_str)
	A = eval(Astr)
	B = eval(Bstr)
	C = eval(Cstr)

	return (A,B,C,tags)



if len(sys.argv) < 3:
	print("Missing arguments!")
else:
	hmm_sequence(sys.argv[1], sys.argv[2])
