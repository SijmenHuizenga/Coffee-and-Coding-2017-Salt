import os
dict = {}
path1  = "/csr_files"
path2 = "/non_csr_files" 
file1 = open('results.txt', 'w')

for file_ in os.listdir(path1):
	file_ = open(file_, 'r')

	for line in file_:
		line = line.split()
		for word in line:
			if dict.has_key(word):
				dict[word] += 1
			else:
				dict[word] = 0 

list = dict.items()
for key,value in dict.iems():
	file1.write("%s:%s\n" %(key,value))

file1.close()



