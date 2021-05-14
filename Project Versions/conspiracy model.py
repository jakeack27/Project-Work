import nltk
import random
import glob, os
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

all_words = []
word_list = []
seperator = ', '
con_category = 'con'
non_category = 'non'
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
    
    ###Frequent distance of the words###
    #for word in lem_words:
        #fdist[word]+=1
    
    #fdist_total = fdist.most_common(len(lem_words))

    '''
    print("############NO PUNCTUATION#######################################################") 
    print(no_punctuation)
    #print(len(no_punctuation))
    print("#############NO STOP WORDS######################################################") 
    print(no_stop_words)
    #print(len(no_stop_words))
    print("#############LEM WORDS######################################################") 
    print(lem_words)
    #print(len(lem_words))

    #num_of_words_per_post = len(lem_words)

    #total_num_of_words = num_of_words_per_post + total_num_of_words
    '''
    
    #print("#############FREQ DIST###############################################################") 
    #print(fdist_total)
    
    #new_contents = convertstr(lem_words, seperator)
    new_contents = lem_words
    #print(lem_words)
    #print(new_contents)
    #print(type(new_contents))
    word_list.append(new_contents)
    #lem_words.pop(0)
    

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
    
#print(len(all_words))
    
#print(all_words)
random.shuffle(all_words)

#all_words = nltk.FreqDist(all_words)
#for word in all_words:
    #fdist[word]+=1

for i in all_words:
    for j in i:
        list_words = isinstance(j, list)
        if list_words == True:
            for f in j:
                fdist[f]+=1
                #print(f)

print(fdist.most_common)
            
        #if j == type(list):
            #print(j)
        #print(j)
        #print(type(j))
        #for h in j:
            #print(h)

#print(fdist.most_common(10))    
#print(all_words)
#print(type(all_words))
#print(len(all_words))


#all_words = []

for words in potential_conspiracy_list:
    all_words.append(words[0].lower())

    word_features = nltk.FreqDist(all_words)

    #word_tokens = word_tokenize(word_features)

def document_features(document):
    document_words = set(document)
    features = {}
    for w in word_features:
        features['contains({})'.format(w)] = (w in document_words)
    return features

#print(document_features(con_test))

featuresets = [(document_features(d), c) for (d, c) in potential_conspiracy_list]
train_set, test_set = featuresets[8:], featuresets[:7]

#print(type(document_feattures(d), c))
#print(featuresets)
#classifier = nltk.NaiveBayesClassifier.train(train_set)

#print(type(classifier))

#print(nltk.classify.accuracy(classifier, test_set))

#print(classifier.show_most_informative_features(5))'''

