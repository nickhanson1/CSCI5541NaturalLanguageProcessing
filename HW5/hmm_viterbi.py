import sys
import nltk


def hmm_viterbi(model, file):
	A, B, C, tags = decode_model(model)
	sentence_file = open(file, "r")
	sentence = sentence_file.read()

	words = sentence.split(" ")
	if words[-1] == "":
		words.remove("")

	length = len(words)

	for i in range(len(words)):
		words[i] = words[i].lower()

	v_keys = ((w, t) for w in sentence for t in tags)

	v_mat = dict.fromkeys(v_keys, 0)

	for t in tags:
		bigram = ("<S>", t)
		if words[0] not in B[t].keys():
			v_mat[(words[0], t)] = 0
		else:
			v_mat[(words[0], t)] = A[bigram] * B[t][words[0]]

	backtrace = dict.fromkeys(v_keys, "")


	for i in range(1, len(words)):
		prev_word = words[i-1]
		for t in tags:
			max_tag = None
			max_val = -1
			for prev_tag in tags:
				val = -1
				if prev_word not in B[prev_tag].keys():
					val = 0
				else:
					val = v_mat[(prev_word, prev_tag)] * A[(prev_tag, t)] * B[prev_tag][prev_word]
				if val > max_val:
					max_val = val
					max_tag = prev_tag
			v_mat[(words[i], t)] = max_val
			backtrace[(words[i], t)] = max_tag


	final_tag = []

	max_val = -1
	max_tag = ""
	for t in tags:
		val = v_mat[(words[length - 1], t)]
		if val > max_val:
			max_val = val
			max_tag = t 

	print(words[length - 1])
	print(max_tag)
	final_tag.append(max_tag)

	for i in range(length - 1, 0, -1):
		final_tag.append(backtrace[(words[i], final_tag[-1])])

	final_tag.reverse()
	tagged_string = ""
	for i in range(len(words)):
		w = words[i]
		tagged_string += w
		tagged_string += "_"
		tagged_string += final_tag[i]
		tagged_string += " "
	print(tagged_string)

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
	hmm_viterbi(sys.argv[1], sys.argv[2])
