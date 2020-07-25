# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 16:24:24 2020

@author: sarthak
"""

import glob,sys

nbmodel = {}
spam_probability, ham_probability = 0, 0
correct = 0
wrong = 0
path = ""

def read_path():
    """
        Read path from system argument or set it for running locally
    """
    global path
    if len(sys.argv) >= 2:
        path = sys.argv[1]
    else:
        path = "dev"


def read_model():
    """
        Reading nbmodel.txt
    """
    file = open("nbmodel.txt","r", encoding="latin-1")
    global nbmodel, spam_probability, ham_probability
    for line in file:
       arr =  line.split()
       nbmodel[arr[0]] = (float(arr[1]),float(arr[2]))
    
    model_params = nbmodel["model_params"]
    spam_probability = model_params[0]
    ham_probability = model_params[1]
    
def predict_test():
    """
        Reading files from test/dev set
        Prediciting if file/email is spam or ham
        Writing it to output file
    """
    global spam_probability, ham_probability
    test_file_list = glob.glob(path+"/**/*.txt",recursive=True)
    output_file = open("nboutput.txt","w+", encoding="latin-1")
    for test_file in test_file_list:
        file_spam_prob, file_ham_prob = predict(test_file)
        if file_ham_prob > file_spam_prob:
            output_file.writelines("ham\t"+test_file+"\n")
        else:
            output_file.writelines("spam\t"+test_file+"\n")
            

def predict(file):
    """
        Calculating spam and ham probability
        Returning the result
    """
    global spam_probability, ham_probability
    file = open(file, encoding="latin-1")
    file_words = file.read().split()
    file_spam_prob = spam_probability
    file_ham_prob = ham_probability
   
    for word in file_words:
        
        # if word.isnumeric():
        #     word = 'digit_numeric_key'
        
        word = word.lower()
        if word in nbmodel:
            word_probability = nbmodel[word]
            file_spam_prob+= word_probability[0]
            file_ham_prob+= word_probability[1]
            
    return file_spam_prob,file_ham_prob

read_path()
read_model()
predict_test()