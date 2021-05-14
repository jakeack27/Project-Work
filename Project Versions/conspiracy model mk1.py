import nltk
import random
import glob, os
import re
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

all_words = []
word_list = []
fdist = FreqDist()
punctuation = re.compile(r'[-.?!,:;()\/|]')
stop_words = set(stopwords.words("english"))
wn = nltk.WordNetLemmatizer()

non_path = r"C:\Users\Jake\Desktop\conspiracy_data\nons"
con_path = r"C:\Users\Jake\Desktop\conspiracy_data\cons"

def pre_processing():
    
    no_punctuation = []
    no_stop_words = []
    lem_words = []
###### pre-processing/NLTK - punctuation included ######
    Content_tokens = word_tokenize(contents)
    
    ###Gets rid of punctuation###
    for words in Content_tokens:
        word=punctuation.sub("", words)
        if len(word)>0:
            no_punctuation.append(word.lower())

    ###Gets rid of Stop Words###
    for words in no_punctuation:
        if words not in stop_words:
            no_stop_words.append(words)

    ###Lemmatizing the words###
    for words in no_stop_words:
        lem_words.append(wn.lemmatize(words))
    
    new_contents = lem_words
    word_list.append(new_contents)   

os.chdir(non_path)
for file in glob.glob("*.txt"):
    editted_file = '/' + file
    full_filename = non_path + editted_file
    myfile = open(full_filename)
    contents = myfile.read()
    pre_processing()
    
for i in range(0, len(word_list)):
    newer_contents = word_list[i]
    all_words.append((newer_contents, 'non'))
    
word_list.clear()




os.chdir(con_path)
for file in glob.glob("*.txt"):
    editted_file = '/' + file
    full_filename = con_path + editted_file
    myfile = open(full_filename)
    contents = myfile.read()
    pre_processing()

for i in range(0, len(word_list)):
    newer_contents = word_list[i]
    all_words.append((newer_contents, 'con'))

random.shuffle(all_words)

for i in all_words:
    for j in i:
        list_words = isinstance(j, list)
        if list_words == True:
            for f in j:
                fdist[f]+=1

print(fdist.most_common)
