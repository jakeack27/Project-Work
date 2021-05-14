import random
import re
import numpy as np
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

total_data = []
fdist = FreqDist()
MNB_clf = MultinomialNB()
GNB_clf = GaussianNB()
BNB_clf = BernoulliNB()
kf = KFold(n_splits=5)
tfidf = TfidfVectorizer()
punctuation = re.compile(r'[-.?!,:;()\/|]')
stop_words = set(stopwords.words("english"))
wn = nltk.WordNetLemmatizer()
datafile = 'conspiracyData.txt'

'''This function is responsible for pre processing the data by tokenizing the contents then taking out the punctuation and stop words
and then lemmitizing the data.'''
def pre_processing():   
    no_punctuation = []
    no_stop_words = []
    lem_words = []
        
    Content_tokens = word_tokenize(contents)
        
    for words in Content_tokens:
        word=punctuation.sub("", words)
        if len(word)>0:
            no_punctuation.append(word.lower())

    for words in no_punctuation:
        if words not in stop_words:
            no_stop_words.append(words)

    for words in no_stop_words:
        lem_words.append(wn.lemmatize(words))

    total_data.append(lem_words)
    #print("############NO PUNCTUATION#######################################################") 
    #print(no_punctuation)
    #print(len(no_punctuation))
    #print("#############NO STOP WORDS######################################################") 
    #print(no_stop_words)
    #print(len(no_stop_words))
    #print("#############LEM WORDS######################################################") 
    #print(lem_words)
    #print(len(lem_words))

'''This function, when called, is responsible for checking if a word is in a post and returning if its true of false.'''
def post_features(post):
    post_words = set(post)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in post_words)
    return features

'''This dataframe takes the contents from the file created by the 5G scraper program, preprocessing the contents, adding the contents to the dataframe,
and shuffling the dataframe.'''
dataset = pd.read_csv(datafile, sep='\t', header=None)
dataset.columns = ['category', 'contents']
original_contents = dataset.contents
     
for contents in original_contents:
    pre_processing()

dataset['preprocessed'] = total_data

###this list and for loop is a part of the testing###
pre_shuffled_dataset_order = []
for i in dataset.index:
    pre_shuffled_dataset_order.append(i)

dataset = dataset.sample(frac = 1)

post_shuffled_dataset_order = []

###TEST 1 CHECK IF DATASET HAS BEEN SHUFFLED###
print('TESTING RESULTS:')
for i in dataset.index:
    post_shuffled_dataset_order.append(i)

if pre_shuffled_dataset_order == post_shuffled_dataset_order:
    print('The dataset has not been shuffled')
else:
    print('The dataset has been shuffled')
    
pre_shuffled_dataset_order.clear()
post_shuffled_dataset_order.clear()
###############################################
    
'''This for loop retrieves the frequent distance of the data.'''
all_words = []
for element in dataset.preprocessed:
    for i in element:
        fdist[i]+=1
        
'''These two lines create a list that stores the first 2000 words from every post thats been collected.'''
all_words = fdist
word_features = list(all_words.keys())[:2000]

'''This for loop creates a list of tuples that contain a tokenized list of the words from a post along with its category.'''
total_docs = [] 
for i in dataset.index:
    total_docs.append((dataset.preprocessed[i], dataset.category[i]))

###TEST 2 CHECK IF THE DATA HAS BEEN FORMATTED AS A TUPLE###
if type(total_docs[0]) == tuple:
    print('The data has been formatted as a tuple')
else:
    print('The data has not been formated as a tuple')
#############################################################

'''The featuresets variable stores a list of every word thats been selected and displays true or false for if that word is in the post.
The folowing two lines split the featuresets list in two with one set from training and the other for testing.'''       
featuresets = [(post_features(cont), cat) for (cont, cat) in total_docs]
train_set = featuresets[:15]
test_set = featuresets[10:]

###TEST 3 CHECK IF FEATURE SETS HAVE BEEN FORMATTED CORRECTLY###
featuresets_type = []
for i in featuresets[0]:
    featuresets_type.append(type(i))

if featuresets_type[0] == dict and featuresets_type[1] == str:
    print('feature sets have been correctly formatted')
else:
    print('feature sets have not been correctly formatted')
    
featuresets_type.clear()
#################################################################
    
'''This line trains the NLTK classifier.''' 
classifier = nltk.NaiveBayesClassifier.train(train_set)
    
print('NLTK Naive Bayes Classifier Accuracy Percent: ', nltk.classify.accuracy(classifier, test_set)*100)
print(classifier.show_most_informative_features(10))
print('\n')

'''These two for loops take the preprocessed contents and the contents category and adding it to lists. The preprocessed
for loop has an extra step where the contents of each post are joined before being added to the list.'''
category_list = []
prepro_list = []
for i in dataset['preprocessed']:
    joined_str = ' '.join(i)
    prepro_list.append(joined_str)

for i in dataset['category']:
    category_list.append(i)

'''This new dataframe only contains the pre-precessed contents and its category. However in this dataframe the pre-processed contents
are one string instead of a tokenized list of words.''' 
new_dataset = pd.DataFrame({'category':category_list,
                            'preprocessed':prepro_list})

'''These two lines are responsible for vectorizing the contents of the preprocessed column and adding it to a new dataframe.
The dataframes columns are the words, the rows are the posts, and the cells contain the impoortance of each word to the post.'''
preprocessed_tfidf = tfidf.fit_transform(new_dataset['preprocessed'])
vectorized_dataset = pd.DataFrame(preprocessed_tfidf.toarray())

print('Multinomial Naive Bayes Cross Validation Score: ', cross_val_score(MNB_clf, vectorized_dataset, new_dataset['category'], cv=kf, n_jobs=1))
print('Gaussian Naive Bayes Cross Validation Score: ', cross_val_score(GNB_clf, vectorized_dataset, new_dataset['category'], cv=kf, n_jobs=1))
print('Berlouni Naive Bayes Cross Validation Score: ', cross_val_score(BNB_clf, vectorized_dataset, new_dataset['category'], cv=kf, n_jobs=1))
print('\n')

'''This line is responsible for splitting the data into testing and training sets.'''
x_train, x_test, y_train, y_test = train_test_split(vectorized_dataset, new_dataset['category'], test_size=0.4)

'''These three lines are responsible for creating the classifier.'''
MNB_clf.fit(x_train, y_train)
GNB_clf.fit(x_train, y_train)
BNB_clf.fit(x_train, y_train)

###Manual verification of the results###
print('Actual Results:')
print(y_test)
print('\n')

'''These three lines use the classifiers to create a model that can predict the results of the tesing set.'''
MNB_model = MNB_clf.predict(x_test)
BNB_model = BNB_clf.predict(x_test)
GNB_model = GNB_clf.predict(x_test)

print('Predictions: ')
print('Multinomial Naive Bayes Score: ', MNB_model)
print('Gaussian Naive Bayes Score: ', GNB_model)
print('Berlouni Naive Bayes Score: ', BNB_model)
print('\n')

'''These three lines are responsible for calculating the accuracy for each model.'''
MNB_accuracy = ((MNB_model == y_test).sum()/len(MNB_model)*100)
GNB_accuracy = ((GNB_model == y_test).sum()/len(GNB_model)*100)
BNB_accuracy = ((BNB_model == y_test).sum()/len(BNB_model)*100)

print('MNB Accuracy Percent: ', MNB_accuracy)
print('GNB Accuracy Percent: ', GNB_accuracy)
print('BNB Accuracy Percent: ', BNB_accuracy)    
