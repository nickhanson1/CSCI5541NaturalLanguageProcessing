import re
import sys
import math

def edit_dist(w1, w2):
	l1 = len(w1) + 1
	l2 = len(w2) + 1

	dist = []
	for i in range(l2):
		dist.append([0] * l1)

	for i in range(l2):
		dist[i][0] = i

	for i in range(l1):
		dist[0][i] = i

	for i in range(1,l2):
		for j in range(1,l1):
			d1 = dist[i - 1][j] + 1
			d2 = dist[i][j - 1] + 1
			d3 = dist[i - 1][j - 1] + (0 if w1[j - 1] == w2[i - 1] else 2)
			d = d1
			d = d2 if d2 < d else d
			d = d3 if d3 < d else d
			dist[i][j] = d 

	return dist[l2 - 1][l1 - 1]


def tokenize(stri):
	stri = stri.lower()
	letternumber = "[A-Za-z0-9]"
	notletter = "[^A-Za-z0-9]"
	alwayssep = "[\\?!:()\";/\\|`-]"
	clitic = "('|:|-|'S|'D|'M|'LL|'RE|'VE|N'T|'s|'d|'m|'ll|'re|'ve|n't)"
	abbr = ["Dr.", "Co.", "Inc.", "Jan.", "Feb.", "Mr.", "Ms.", "Mrs.", "Mar.", "Apr."]

	sub = re.sub(alwayssep, " ", stri)

	sub = re.sub(",[^0-9]", " ", sub)
	sub = re.sub("[^0-9],", " ", sub)
	sub = re.sub(notletter + "'(.*)'" + notletter, " \\1 ", sub)
	sub = re.sub("\. ", " ", sub)
	sub = re.sub("[^0-9]\.", " ", sub)


	tokens = sub.split()

	return_tokens = []

	for t in tokens:
		if t != "":
			return_tokens.append(t)

	return return_tokens


def suggest(word, wordlistname):
	wordlist = open(wordlistname, "r")
	suggest = []
	for i in range(3):
		line = wordlist.readline()[:-1]
		suggest.append([line, edit_dist(line, word)])

	line = wordlist.readline()
	length = len(word)
	while line != "":
		line = line[:-1]
		
		if(abs(len(line) - length) <= 1):
			dist = edit_dist(line ,word)
			if(dist < suggest[0][1]):
				suggest[0] = (line, dist)
			elif(dist < suggest[1][1]):
				suggest[1] = (line, dist)
			elif(dist < suggest[2][1]):
				suggest[2] = (line, dist)
		line = wordlist.readline()

	return_suggestions = []
	for i in range(3):
		return_suggestions.append(suggest[i][0])
	print(return_suggestions)

	return suggest



def correct(word, wordlistname):
	wordlist = open(wordlistname, "r")
	line = wordlist.readline()
	while line != "":
		line = line[:-1]
		if word == line:
			return True
		line = wordlist.readline()
	return False


def main(filename):
	dictname = "words"
	file = open(filename, "r")
	line = file.readline()
	linenum = 1

	cor_file = open("corrected_" + filename, "w")

	while line:
		tokens = tokenize(line)
		for t in tokens:
			if t != "":
				if not correct(t, dictname):
					suggestions = suggest(t, dictname)
					print("Misspelling on line", linenum, ": ", t)
					print("Suggestions:")
					print("\t", suggestions[0][0], "Levenshtein distance of ", suggestions[0][1])
					print("\t", suggestions[1][0], "Levenshtein distance of ", suggestions[1][1])
					print("\t", suggestions[2][0], "Levenshtein distance of ", suggestions[2][1])
					line = re.sub(t, suggestions[0][0], line)
		
		cor_file.write(line)
		linenum += 1
		line = file.readline()






main(sys.argv[1])