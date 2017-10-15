import os
from operator import itemgetter
main_words =['corporate', 'social', 'responsibility', 'corporate', 'conscience','csr','ethical','business', 'model']
key_words = [ 'ecomic', 'environmental','company','industry', 'self-regulation', 'standards','spirit', 'law','enterprise', 'conglomorate']
key_issues = ['environmental', 'management', 'eco-efficiency','responsible' ,'sourcing', 'stakeholders', 'engagement', 'labour', 'standards','conditions', 
				'employee','community' ,'relations', 'enquiry', 'gender','balance', 'human', 'rights', 'anti-corruption',' measure'
				'governance']
key_benefits = ['improve','brand','image', 'enhance', 'customer' ,'loyalty', 'better', 'decision', 'making']

list_of_lists = [main_words, key_words, key_issues, key_benefits]
main_words_points = 10
key_words_points = 5
key_issues_points = 3
key_benefits_points = 2

def csr(line):
	points = 0
	line = line.split();
	for i in range(len(line)):
		for j in list_of_lists:
			for k in j:
				if(k == line[i]):
					if list_of_lists[0]:
						points = points + main_words_points
					elif list_of_lists[1]:
						points = points + key_words_points
					elif list_of_lists[2]:
						points = points + key_issues_points
					elif list_of_lists[3]:
						points = points + key_benefits_points
	return points
def dostuff(test_text):
	diction = {}
	path1  = "./csr-txt"
	path2 = "./non-csr-txt"
	counter = 0
	file1 = open('results.txt', 'w')
	mostusedwords = ["the", "be", "to", "of", "and", "a", "in", "that", "have", "I", "it", "for", "not", "on", "with", "he", "as", "you", "do", "at", "this", "but",
						"his", "by", "from", "they", "we", "say", "her", "she", "or", "an","is","are","|" "will", "my", "one", "all", "would", "there", "their", "what", "so", "up",
						"out", "if","about", "who", "get", "which", "go", "me", "when", "make", "can", "like", "time", "no", "just", "him", "know", "take", "people",
						"into", "year", "your", "good", "some", "could", "them", "see", "other", "than", "then", "now", "look", "only", "come", "its", "over", "think",
						 "also", "back", "after", "use", "two", "how", "our", "work", "first", "well", "way", "even", "new", "want", "because", "any", "these", "give",
						 "day", "most", "us", "-", "&"]

	for file_ in os.listdir(path1):
		file_ = open("./csr-txt/"+file_, 'r', errors="ignore")
		for line in file_:
			line = line.split()
			for word in line:
				counter= counter+1
				if word  not in mostusedwords:
					if word in diction:
						diction[word] += 1
					else:
						diction[word] = 1

	lists = sorted(diction.items(), key=itemgetter(1))
	max_count = lists[len(lists)-1][1]
	threshold = 99/100 * max_count
	index =0
	words = []
	for item in lists:
		if item[1] < threshold:
			lists.pop(index)
			
		else:
			words.append(item)
		index = index + 1


	index =0
	word_prob = []
	word_prob_train = {}

	for item in lists:
		item = (item[0],item[1]/counter *100)
		word_prob.append(item)
		word_prob_train[item[0]]=  item[1]
		index = index +1

	file1.close()



	test_text = test_text.lower()
	test_text_str = test_text
	test_text = test_text.split()
	counter =0
	word_prob_test = {}

	for word in test_text:
		counter= counter+1
		if word  not in mostusedwords:
			if word in word_prob_test:
				word_prob_test[word] += 1
			else:
				word_prob_test[word] = 1

	for item in word_prob_test:
		word_prob_test[item] =  word_prob_test[item]/counter *100

	positive = 0
	negative = 0
	for item in word_prob_test:
		if item not in mostusedwords: 
			if item in word_prob_train:
				if(word_prob_test[item] > word_prob_train[item]/10):
					positive += 1
				else:
					negative +=1
			else:
				negative +=1

	positive = positive + csr(test_text_str)
	total = positive + negative
	CSR = False
	if positive > 4/5 *total:
		CSR = True
	print("CSR = ", CSR)
