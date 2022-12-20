import re


def eliza():
	print("Hello. Please tell me about your problems.")

	running = True

	while(running):
		original_input = input("")

		if(original_input == ""):
			continue

		original_input = original_input.lower()

		response = re.sub("goodbye", "Goodbye!", original_input)

		if(response != original_input):
			running = False

		response = re.sub("yes", "I see.", response)

		response = re.sub("no[^a-z]*$", "Why not?", response)

		response = re.sub(".+ you", "Let's not talk about me.", response)

		response = re.sub("what is ", "Why do you ask about ", response)

		response = re.sub("^i am (.*)", "Do you enjoy being \\1?", response)

		response = re.sub("why is (.*)", "Why do you think \\1?", response)

		response = re.sub("i am", "you are", response)


		# Extra responses
		#
		#
		response = re.sub("(.*) said (.*)", "Why do you think \\1 said \\2? How do you think \\1 feels?", response)

		response = re.sub("(.*)stress(ed|ing|)(.*)", "How much stress are you feeling? Have you had a break recently?", response)

		response = re.sub("my (.*) (is|are|have|do) (.*)", "How is this affecting your relationship with your \\1?",response)
		
		response = re.sub("i feel that (.*)", "Tell me more about how \\1.",response)

		response = re.sub("i ", "you ", response)

		response = re.sub("(.*)my (.*)", "your \\1", response)
		#
		#
		#

		response = re.sub("^my (.*)", "Your \\1.", response)

		if(response == original_input):
			response = "Please go on."
		

		print(response)

eliza()