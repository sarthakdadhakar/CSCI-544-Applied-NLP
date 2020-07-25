# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 16:17:24 2020

@author: sarthak
"""

import glob
import math
import sys

spam_dict = {}
all_dict ={}
ham_dict = {}
total_ham_words = 0
total_spam_words = 0
spam_file_list = []
ham_file_list = []
path = ""

def read_path():
    global path
    if len(sys.argv) >= 2:
        path = sys.argv[1]
    else:
        path = "train"

def get_spam_data():  
    global total_spam_words, spam_file_list, path
    spam_file_list = glob.glob(path+"/*/spam/*.txt")
    print("Reading Spam Data...")
    for spam_file in spam_file_list:
        file = open(spam_file, encoding="latin-1")
        file_words = file.read().split()
        for word in file_words:
            if word.isnumeric():
                word = 'digit_numeric_key'
            word = word.lower()
            if not check_stopword(word):
                total_spam_words+= 1
                if word in spam_dict:
                    spam_dict[word] += 1
                else:
                    spam_dict[word] = 1
                
                if word in all_dict:
                    all_dict[word] += 1
                else:
                    all_dict[word] = 1
        file.close()

def get_ham_data():
    global total_ham_words, ham_file_list,path
    ham_file_list = glob.glob(path+"/*/ham/*.txt")
    print("Reading Ham Data...")
    for ham_file in ham_file_list:
        file = open(ham_file, encoding="latin-1")
        file_words = file.read().split()
        for word in file_words:
            if word.isnumeric():
                word = 'digit_numeric_key'
            word = word.lower()
            if not check_stopword(word):
                total_ham_words+= 1
                if word in ham_dict:
                    ham_dict[word] += 1
                else:
                    ham_dict[word] = 1
                
                if word in all_dict:
                    all_dict[word] += 1
                else:
                    all_dict[word] = 1
        file.close()
        

def compute_probabilities():
    global total_spam_words, total_ham_words
    total_words = total_spam_words+total_ham_words
    unique_words = len(all_dict)
    print("Training Set Description: ")
    
    len_ham = len(ham_file_list)
    len_spam = len(spam_file_list)
    print("SPAM EMAILS: ",len_spam)
    print("HAM EMAILS: ",len_ham)
    print("Total words: ",total_words)
    print("Training...")
    
    spam_probability = math.log((total_spam_words + 1)/(total_words+unique_words))
    ham_probability = math.log((total_ham_words + 1)/(total_words+unique_words))
    
    # spam_probability = math.log((len_spam)/(len_spam+len_ham))
    # ham_probability = math.log((len_ham)/(len_spam+len_ham))
    
    
    
    output_file = open("nbmodel_enhanced.txt", "w+", encoding="latin-1")
    output_file.write("model_params "+str(spam_probability)+" "+str(ham_probability)+"\n")
    
    nbmodel = {}
    nbmodel["model_params"] = (spam_probability,ham_probability)
    for word in all_dict.keys():
        spam_count = 0.01
        if word in spam_dict:
            spam_count+= spam_dict[word]
        
        word_spam_probability = math.log(spam_count / (total_spam_words+unique_words*0.01))
        
        ham_count = 0.01
        if word in ham_dict:
            ham_count+= ham_dict[word]
        
        word_ham_probability = math.log(ham_count / (total_ham_words+unique_words*0.01))
        
        output_file.write(word+" "+str(word_spam_probability)+" "+str(word_ham_probability)+"\n")
        nbmodel[word] = (word_spam_probability, word_ham_probability)   
    
    print("nbmodel_enhanced.txt generated successfully...")
    print("SPAM Probability: ",spam_probability)
    print("HAM Probability: ",ham_probability)
    output_file.close()  

def check_stopword(word):
    #stop word list taken from 
    stopword_list = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
                     'you', "you're", "you've", "you'll", "you'd", 'your', 
                     'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 
                     'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', 
                     "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 
                     'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 
                     "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 
                     'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 
                     'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 
                     'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 
                     'for', 'with', 'about', 'against', 'between', 'into', 'through', 
                     'during', 'before', 'after', 'above', 'below', 'to', 'from', 
                     'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 
                     'again', 'further', 'then', 'once', 'here', 'there', 'when', 
                     'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 
                     'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 
                     'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 
                     't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 
                     'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 
                     "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', 
                     "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', 
                     "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 
                     'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 
                     'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 
                     'won', "won't", 'wouldn', "wouldn't", 'subject']
    return word in stopword_list
    
        

read_path()
get_spam_data()
get_ham_data()
compute_probabilities()