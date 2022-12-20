import sys
import copy

class Node:

	def __init__(self, label, name = None):
		self.label = label
		self.name = name
		self.parent_node = None
		self.children = []

	def add_child(self, node):
		self.children.append(node)

	
	def to_string(self):
		string = self.label
		string += " "
		if self.name != None:
			string =  self.name 
			return string 
		else:
			string += "("
			for c in self.children:
				string += c.to_string()
				string += ", "
			string = string[:-2]
			string += ")"
		return string

class Tree:
	def __init__(self, label, name=None):
		self.current_node = Node(label, name)
		self.root_node = self.current_node

	def go_up(self):
		self.current_node = self.current_node.parent_node

	def add_child(self, node):
		node.parent_node = self.current_node
		self.current_node.add_child(node)
		self.current_node = node

	def add_child(self, tree):
		tree.root_node.parent_node = self.current_node
		self.current_node.add_child(tree.root_node)
		self.current_node = tree.root_node

	def print(self):
		print(self.root_node.to_string())


def parser(config, sentence):
	grammar_file = open(config, "r")
	rules = []

	#parse config file
	lines = grammar_file.read().split("\n")
	for i in range(len(lines)):
		line = lines[i]
		if line == "":
			continue
		if line[0] == "#":
			continue

		linesplit = line.split("->")
		rule = [linesplit[0].strip()]


		variables = linesplit[1].split(" ")
		for k in range(0, len(variables)):
			symbol = variables[k]
			if symbol != "":
				rule.append(symbol.strip())

		rules.append(rule)

		line = grammar_file.readline()

	words = sentence.split(" ")

	failure = earley(rules, words)
	if failure:
		print("No matching parse trees for \"{}\"".format(sentence))

def earley(grammar, words):
	#initialization
	S = []
	for i in range(len(words) + 1):
		S.append([])


	first_rule = copy.deepcopy(grammar[0])
	root = Tree(first_rule[0], None)
	first_rule.insert(1,"`")
	first_rule.insert(0,0)     #origin position
	first_rule.insert(1,root)  #copy of full tree
	S[0].append(first_rule)

	for k in range(1,len(grammar)):
		rule = copy.deepcopy(grammar[k])
		rule.insert(1, "`")
		rule.insert(0,0)

		root = Tree(rule[1])

		rule.insert(1, root)
		S[0].append(rule)


	for k in range(len(words) + 1):
		for rule in S[k]:
			loc = rule.index("`")
			if loc != len(rule) - 1:
				if rule[loc + 1][0].isupper():
					predict = predictor(grammar, rule, k)
					non_duplicate = []
					for p in predict:
						duplicate = False
						for s in S[k]:	
							if is_identical(p,s):
								duplicate = True
								break
						if not duplicate:
							non_duplicate.append(p)

					S[k].extend(non_duplicate)
				else:
					if k == len(words):
						break
					if rule[loc + 1] == words[k]:
						scanned = scanner(grammar, rule)
						if not scanned in S[k+1]:
							S[k+1].append(scanned)
						#print(scanned)
			else:
				completed = complete(grammar, rule, S)
				for c in completed:
					if c in S[k]:
						completed.remove(c)
				#print(completed)
				S[k].extend(completed)

	fail = True
	for s in S[len(words)]:
		if(s[2] == grammar[0][0] and s[-1] == "`"):
			fail = False
			s[1].print()

	return fail

def predictor(grammar, rule, k):
	loc = rule.index("`")
	var = rule[loc + 1]
	return_list = []
	for r in grammar:
		if r[0] == var:
			new_r = copy.deepcopy(r)
			new_r.insert(0, k)
			new_r.insert(2, "`")
			#new_tree = copy.deepcopy(rule[1])
			new_tree = Tree(var)
			new_r.insert(1, new_tree)
			return_list.append(new_r)

	return return_list


def scanner(grammar, rule):
	loc = rule.index("`")
	new_rule = copy.deepcopy(rule)
	new_rule.remove("`")
	new_rule.insert(loc + 1, "`")
	new_tree = Tree("terminal", rule[loc + 1])
	new_rule[1].add_child(new_tree)
	new_rule[1].go_up()
	return new_rule


def complete(grammar, rule, states):
	var = rule[2]
	index = rule[0]
	return_list = []
	for s in states[index]:
		loc = s.index("`")
		if loc < (len(s) - 1) and s[loc + 1] == var:
			completed_rule = copy.deepcopy(s)
			old_dot_loc = completed_rule.index("`")
			#print(completed_rule[1].current_node.label)
			#new_node = Node(var, rule[rule.index("`")-1])
			#completed_rule[1].add_child(new_node)
			completed_rule[1].add_child(rule[1])

			completed_rule.remove("`")
			completed_rule[1].go_up()
			completed_rule.insert(old_dot_loc + 1, "`")

			return_list.append(completed_rule)
	return return_list


def is_identical(rule1, rule2):
	if rule1[0] != rule2[0]:
		return False

	comp_rule1 = copy.deepcopy(rule1)
	comp_rule1.remove("`")
	comp_rule1 = comp_rule1[2:]

	comp_rule2 = copy.deepcopy(rule2)
	comp_rule2.remove("`")
	comp_rule2 = comp_rule2[2:]


	if(len(comp_rule1) != len(comp_rule2)):
		return False

	for i in range(len(comp_rule1)):
		if comp_rule1[i] != comp_rule2[i]:
			return False

	return True

if len(sys.argv) < 3:
	print("Not enough arguments!")
else:
	parser(sys.argv[1], sys.argv[2])