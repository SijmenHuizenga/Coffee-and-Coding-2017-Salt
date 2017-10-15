import os
from operator import itemgetter

dick = {}
path1 = "./csr-txt"
path2 = "/non_csr_files"
file1 = open('results.txt', 'w')
mostusedwords = ["the", "be", "to", "of", "and", "a", "in", "that", "have", "I", "it", "for", "not", "on", "with", "he",
                 "as", "you", "do", "at", "this", "but",
                 "his", "by", "from", "they", "we", "say", "her", "she", "or", "an", "is", "are", "|" "will", "my",
                 "one", "all", "would", "there", "their", "what", "so", "up",
                 "out", "if", "about", "who", "get", "which", "go", "me", "when", "make", "can", "like", "time", "no",
                 "just", "him", "know", "take", "people",
                 "into", "year", "your", "good", "some", "could", "them", "see", "other", "than", "then", "now", "look",
                 "only", "come", "its", "over", "think",
                 "also", "back", "after", "use", "two", "how", "our", "work", "first", "well", "way", "even", "new",
                 "want", "because", "any", "these", "give",
                 "day", "most", "us"]

for file_ in os.listdir(path1):
    print("filename ", file_)
    file_ = open("./csr-txt/" + file_, 'r', errors="ignore")
    for line in file_:
        line = line.split()
        for word in line:
            if word not in mostusedwords:
                if word in dick:
                    dick[word] += 1
                else:
                    dick[word] = 1
lists = sorted(dick.items(), key=itemgetter(1))
for item in lists:
    file1.write("%s:%s\n" % item)
file1.close()
