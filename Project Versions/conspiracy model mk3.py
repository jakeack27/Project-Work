import nltk
from random import randrange
import re
import pickle
import pandas as pd
import os.path
import sklearn
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB

total_data = []
category_list = []
preprocessed_list = []
fdist = FreqDist()
punctuation = re.compile(r'[-.?!,:;()\/|]')
stop_words = set(stopwords.words("english"))
wn = nltk.WordNetLemmatizer()
datafile = 'conspiracyDataManual.txt'
classifier_filename = 'loadedClassifier'

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
    
dispdataset = pd.read_csv(datafile, sep='\t', header=None)
dispdataset.columns = ['category', 'contents']
original_contents = dispdataset.contents
        
for contents in original_contents:
    pre_processing()

dispdataset['preprocessed'] = total_data

for i in dispdataset.category:
    category_list.append(i)
for i in dispdataset.preprocessed:
    preprocessed_list.append(i)
    
dispdataset.drop(dispdataset.index, inplace=True)

'''This function is responsible for pre-processing the data when called
    by tokenizing, getting rid of punctuation, getting rid of stop words,
    lemmitizing the data'''
def menu():
    
    print("Welcome to the main menu.\nPress 1 to Train a Model.\nPress Q to Quit.")
    main_input = input("->")

    if main_input == '1':
        train()        
        
    elif main_input.lower() == 'q':
        print('Are you sure you would like to quit? (Y/N)')
        quit_input = input('>')
        if quit_input.lower() == 'y':
            exit()
        elif quit_input.lower() == 'n':
            menu()
        else:
            print('Invalid Input. Returning to Menu.')
            
    else:
        print('Invalid Input. Returning to Menu.')
        menu()

def train():
    
    def document_features(document):
        document_words = set(document)
        features = {}
        for word in word_features:
            features['contains({})'.format(word)] = (word in document_words)
        return features

    dataset = pd.DataFrame({'category':category_list,
                           'preprocessed':preprocessed_list})

    dataset = dataset.sample(frac = 1)

    all_words = []
    
    for element in dataset.preprocessed:
        for i in element:
            fdist[i]+=1

    all_words = fdist
    word_features = list(all_words.keys())[:2000]
    
    total_docs = []
    for i in range(0, len(dataset)):
        #print(i)
        total_docs.append((dataset.preprocessed[i], dataset.category[i]))

    featuresets = [(document_features(cont), cat) for (cont, cat) in total_docs]
    train_set = featuresets[:15]
    test_set = featuresets[10:]
    
    classifier = nltk.NaiveBayesClassifier.train(train_set)

    if os.path.exists(classifier_filename):
            classifier_f = open(classifier_filename, 'rb')
            classifier = pickle.load(classifier_f)
            classifier_f.close()
    else:
        print('Cannot load classifier. Try saving a classifier before loading one.\nReturning to main menu.')
    
    print('RegularNB: ', nltk.classify.accuracy(classifier, test_set)*100)
    print(classifier.show_most_informative_features(10))

    print('Model Trained. What next?')
    print('Press 1 to re-train model.\nPress S to Save the Model.\nPress D to Delete Loaded Classifier.\nPress B to Return to the Main Menu')
    train_input = input('>')

    if train_input == '1':
        train()
    elif train_input.lower() == 'b':
        menu()
    elif train_input.lower() == 's':
        save_classifier = open(classifier_filename, 'wb')
        pickle.dump(classifier, save_classifier)
        save_classifier.close()
        menu()
    elif train_input.lower() == 'd':
        if os.path.exists(classifier_filename):
            os.remove(classifier_filename)
            print('Classifier Removed')
            menu()
        else:
            print('Classifier Doesnt Exist')
            menu()
    else:
        print('Invalid Input.')
        menu()

menu()
