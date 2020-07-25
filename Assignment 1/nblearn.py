# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 12:06:29 2020

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
    """
        Read path from system argument or set it for running locally
    """
    global path
    if len(sys.argv) >= 2:
        path = sys.argv[1]
    else:
        path = "train"

def get_spam_data():  
    """
        Reading Spam Data
        Generating spam_dict
    """
    global total_spam_words, spam_file_list, path
    spam_file_list = glob.glob(path+"/**/spam/*.txt",recursive=True)
    print("Reading Spam Data...")
    for spam_file in spam_file_list:
        file = open(spam_file, encoding="latin-1")
        file_words = file.read().split()
        for word in file_words:
            
            # if word.isnumeric():
            #     word = 'digit_numeric_key'
            
            total_spam_words+= 1
            word = word.lower()
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
    """
        Reading Ham Data
        Generating ham_dict
    """
    global total_ham_words, ham_file_list,path
    ham_file_list = glob.glob(path+"/**/ham/*.txt",recursive=True)
    print("Reading Ham Data...")
    for ham_file in ham_file_list:
        file = open(ham_file, encoding="latin-1")
        file_words = file.read().split()
        for word in file_words:
            
            # if word.isnumeric():
            #     word = 'digit_numeric_key'
            
            total_ham_words+= 1
            word = word.lower()
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
    """
        Compute Probabilities
        Generate nbmodel.txt
    """
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
    
    spam_probability = math.log((len_spam)/(len_spam+len_ham))
    ham_probability = math.log((len_ham)/(len_spam+len_ham))
    
    
    
    output_file = open("nbmodel.txt", "w+", encoding="latin-1")
    output_file.write("model_params "+str(spam_probability)+" "+str(ham_probability)+"\n")
    
    nbmodel = {}
    nbmodel["model_params"] = (spam_probability,ham_probability)
    for word in all_dict.keys():
        spam_count = 1
        if word in spam_dict:
            spam_count+= spam_dict[word]
        
        word_spam_probability = math.log(spam_count / (total_spam_words+unique_words))
        
        ham_count = 1
        if word in ham_dict:
            ham_count+= ham_dict[word]
        
        word_ham_probability = math.log(ham_count / (total_ham_words+unique_words))
        
        output_file.write(word+" "+str(word_spam_probability)+" "+str(word_ham_probability)+"\n")
        nbmodel[word] = (word_spam_probability, word_ham_probability)   
    
    print("nbmodel.txt generated successfully...")
    print("SPAM Probability: ",spam_probability)
    print("HAM Probability: ",ham_probability)
    output_file.close()  
    
        

read_path()
get_spam_data()
get_ham_data()
compute_probabilities()