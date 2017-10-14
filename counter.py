import os
dict = {}
path1  = "/csr_files"
path2 = "/non_csr_files" 
file1 = open('results.txt', 'w')
mostusedwords = ["the", "be", "to", "of", "and", "a", "in", "that", "have", "I", "it", "for", "not", "on", "with", "he", "as", "you", "do", "at", "this", "but", 
		"his", "by", "from", "they", "we", "say", "her", "she", "or", "an", "will", "my", "one", "all", "would", "there", "their", "what", "so", "up", 
		"out", "if","about", "who", "get", "which", "go", "me", "when", "make", "can", "like", "time", "no", "just", "him", "know", "take", "people", 
		"into", "year", "your", "good", "some", "could", "them", "see", "other", "than", "then", "now", "look", "only", "come", "its", "over", "think",
		"also", "back", "after", "use", "two", "how", "our", "work", "first", "well", "way", "even", "new", "want", "because", "any", "these", "give", 
		"day", "most", "us"]

for file_ in os.listdir(path1):
	file_ = open(file_, 'r')

	for line in file_:
		line = line.split()
		for word in line:
			for word not in mostusedwords:
				if dict.has_key(word):
					dict[word] += 1
				else:
					dict[word] = 0 

list = dict.items()
for key,value in dict.iems():
	file1.write("%s:%s\n" %(key,value))

file1.close()





