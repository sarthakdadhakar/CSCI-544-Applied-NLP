# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 15:48:50 2020

@author: sarthak
"""

import glob
import math
import sys
import random

spam_dict = {}
all_dict ={}
ham_dict = {}
total_ham_words = 0
total_spam_words = 0
spam_file_list = []
ham_file_list = []
path = ""
len_spam_file = 0
len_ham_file = 0


def read_path():
    global path
    if len(sys.argv) >= 2:
        path = sys.argv[1]
    else:
        path = "train"

def get_spam_data():  
    global total_spam_words, spam_file_list, path, len_spam_file
    spam_file_list = glob.glob(path+"/*/spam/*.txt")
    print("Reading Spam Data...")
    len_spam = len(spam_file_list)
    len_spam_file = len_spam//10
    sample = random.choices(spam_file_list, k = len_spam_file)
    
    for spam_file in sample:
        file = open(spam_file, encoding="latin-1")
        file_words = file.read().split()
        for word in file_words:
            if word.isnumeric():
                word = 'digit_numeric_key'
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
    global total_ham_words, ham_file_list, path, len_ham_file
    ham_file_list = glob.glob(path+"/*/ham/*.txt")
    print("Reading Ham Data...")
    
    len_ham = len(ham_file_list)
    len_ham_file = len_ham//10
    sample = random.choices(ham_file_list, k = len_ham_file)
    
    for ham_file in sample:
        file = open(ham_file, encoding="latin-1")
        file_words = file.read().split()
        for word in file_words:
            if word.isnumeric():
                word = 'digit_numeric_key'
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
    global total_spam_words, total_ham_words, len_ham_file, len_spam_file
    total_words = total_spam_words+total_ham_words
    unique_words = len(all_dict)
    print("Training Set Description: ")
    # spam_probability = math.log((total_spam_words + 1)/(total_words+unique_words))
    # ham_probability = math.log((total_ham_words + 1)/(total_words+unique_words))
   
    print("SPAM EMAILS: ",len_spam_file)
    print("HAM EMAILS: ",len_ham_file)
    print("Total words: ",total_words)
    print("Training...")
    
    spam_probability = math.log((len_spam_file)/(len_spam_file+len_ham_file))
    ham_probability = math.log((len_ham_flie)/(len_spam_file+len_ham_file))
    
    
    
    output_file = open("nbmodel_reduced_data.txt", "w+", encoding="latin-1")
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