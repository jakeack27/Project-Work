import random
import re
import numpy as np
import os.path
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

if os.path.exists('conspiracyData.txt'):
    print('Program is running...')
else:
    print('conspiracyData.txt does not exist. Try running WebScraperFinal first.')
    quit()

'''This function is called at the end of the program and displays a small
menu the user can use to print the results they want to see. '''
def menu():
    
    print('Welcome.\n1 - Display NLTK Classifier Accuracy and Most Informative Features.\n2 - Display sklearn Classifier Predictions and Accuracy.\n3 - Display sklearn Cross Validation Scores.\n4 - Display Test Dataset Results.\n5 - Display Test Results.\nQ - Quit.')
    menu_input = input('>').lower()

    if menu_input == '1':
        print('NLTK Naive Bayes Classifier Accuracy Percent: ', nltk.classify.accuracy(classifier, test_set)*100)
        print(classifier.show_most_informative_features(10))
        print('\n')
        menu()
    elif menu_input == '2':
        print('Predictions: ')
        print('Multinomial Naive Bayes Predictions: ', MNB_model)
        print('Gaussian Naive Bayes Predictions: ', GNB_model)
        print('Berlouni Naive Bayes Predictions: ', BNB_model)
        print('\n')
        print('MNB Accuracy Percent: ', MNB_accuracy)
        print('GNB Accuracy Percent: ', GNB_accuracy)
        print('BNB Accuracy Percent: ', BNB_accuracy) 
        print('\n')
        menu()
    elif menu_input == '3':
        print('Multinomial Naive Bayes Cross Validation Score: ', cross_val_score(MNB_clf, vectorized_dataset, new_dataset['category'], cv=kf, n_jobs=1))
        print('Gaussian Naive Bayes Cross Validation Score: ', cross_val_score(GNB_clf, vectorized_dataset, new_dataset['category'], cv=kf, n_jobs=1))
        print('Berlouni Naive Bayes Cross Validation Score: ', cross_val_score(BNB_clf, vectorized_dataset, new_dataset['category'], cv=kf, n_jobs=1))
        print('\n')
        menu()
    elif menu_input == '4':
        print('Actual Results:')
        print(y_test)
        print('\n')
        menu()
    elif menu_input == '5':
        print('Testing Results:')
        ###TEST 1 CHECK IF DATASET HAS BEEN SHUFFLED###
        if pre_shuffled_dataset_order == post_shuffled_dataset_order:
            print('FAILED: Dataset has not been shuffled')
        else:
            print('PASSED: Dataset has been shuffled')
        ###TEST 2 CHECK IF THE DATA HAS BEEN FORMATTED AS A TUPLE###
        if type(total_docs[0]) == tuple:
            print('PASSED: Data has been formatted as a tuple')
        else:
            print('FAILED: Data has not been formated as a tuple')
        ###TEST 3 CHECK IF FEATURE SETS HAVE BEEN FORMATTED CORRECTLY###
        if featuresets_type[0] == dict and featuresets_type[1] == str:
            print('PASSED: Feature sets have been correctly formatted')
        else:
            print('FAILED: Feature sets have not been correctly formatted')
        menu()
    elif menu_input == 'q':
        quit()
    else:
        print('Invalid Input.')
        menu()
        

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

###This list and for loop is a part of the testing for TEST 1###
pre_shuffled_dataset_order = []
for i in dataset.index:
    pre_shuffled_dataset_order.append(i)
################################################################

dataset = dataset.sample(frac = 1)

###This list and for loop is a part of the testing for TEST 1###
post_shuffled_dataset_order = []
for i in dataset.index:
    post_shuffled_dataset_order.append(i)
################################################################
    
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

'''The featuresets variable stores a list of every word thats been selected and displays true or false for if that word is in the post.
The folowing two lines split the featuresets list in two with one set from training and the other for testing.'''       
featuresets = [(post_features(cont), cat) for (cont, cat) in total_docs]
train_set = featuresets[:15]
test_set = featuresets[10:]

###This list and for loop is a part of the testing for TEST 3###
featuresets_type = []
for i in featuresets[0]:
    featuresets_type.append(type(i))
################################################################

'''This line trains the NLTK classifier.''' 
classifier = nltk.NaiveBayesClassifier.train(train_set)

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

'''This line is responsible for splitting the data into testing and training sets.'''
x_train, x_test, y_train, y_test = train_test_split(vectorized_dataset, new_dataset['category'], test_size=0.4)

'''These three lines are responsible for creating the classifier.'''
MNB_clf.fit(x_train, y_train)
GNB_clf.fit(x_train, y_train)
BNB_clf.fit(x_train, y_train)

'''These three lines use the classifiers to create a model that can predict the results of the tesing set.'''
MNB_model = MNB_clf.predict(x_test)
BNB_model = BNB_clf.predict(x_test)
GNB_model = GNB_clf.predict(x_test)

'''These three lines are responsible for calculating the accuracy for each model.'''
MNB_accuracy = ((MNB_model == y_test).sum()/len(MNB_model)*100)
GNB_accuracy = ((GNB_model == y_test).sum()/len(GNB_model)*100)
BNB_accuracy = ((BNB_model == y_test).sum()/len(BNB_model)*100)

menu()
